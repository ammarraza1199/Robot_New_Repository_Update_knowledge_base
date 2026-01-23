import logging
import multiprocessing
import time
import os
import wave
import pyaudio
from pydub import AudioSegment
from logging_config import setup_logging

logger = logging.getLogger(__name__)

class PyAudioPlayer:
    def __init__(self, audio_queue, audio_playing_flag, audio_dir="audio_cache"):
        self.audio_queue = audio_queue
        self.audio_playing_flag = audio_playing_flag
        self.audio_dir = audio_dir
        self.shutdown_flag = multiprocessing.Event()
        
        self.p = None
        self.stream = None
        self.wf = None
        self.playing_file_name = None
        self.CHUNK_SIZE = 1024
        
        self.output_device_index = 2

    def initialize_audio_system(self):
        try:
            logger.debug("Initializing PyAudio system...")
            self.p = pyaudio.PyAudio()
            logger.info("PyAudio initialized successfully.")
            return True
        except Exception as e:
            logger.critical(f"CRITICAL: Failed to initialize PyAudio: {e}", exc_info=True)
            return False

    def cleanup_audio_system(self):
        logger.debug("Cleaning up PyAudio resources.")
        self.stop_playback()
        if self.p:
            self.p.terminate()
            logger.info("PyAudio terminated.")

    def start(self):
        if not self.initialize_audio_system():
            logger.error("Could not initialize audio system. Player process terminating.")
            return

        logger.info("PyAudio Player Process Started. Waiting for commands...")
        while not self.shutdown_flag.is_set():
            self.check_for_commands()
            self.stream_audio_chunk()
            # A short sleep is necessary to prevent this busy-loop from consuming 100% CPU.
            # However, the previous 0.01s was too long, causing buffer underruns.
            # 0.001s is a much safer value that should still be efficient.
            time.sleep(0.001)

        self.cleanup_audio_system()
        logger.info("PyAudio Player Shutting Down")

    def _is_sample_rate_supported(self, sample_rate, num_channels, pa_format):
        logger.debug(f"Checking support for rate={sample_rate}, channels={num_channels}, format={pa_format}")
        if not self.p:
            logger.warning("PyAudio not initialized, cannot check sample rate support.")
            return False
        try:
            is_supported = self.p.is_format_supported(
                rate=sample_rate,
                input_device=None,
                input_channels=0,
                input_format=pyaudio.paInt16,
                output_device=self.output_device_index,
                output_channels=num_channels,
                output_format=pa_format
            )
            logger.debug(f"Device support for rate {sample_rate}Hz: {is_supported}")
            return is_supported
        except ValueError as e:
            logger.warning(f"Format check failed for rate {sample_rate}Hz with ValueError: {e}")
            return False
        except Exception as e:
            logger.error(f"Error checking sample rate {sample_rate}Hz: {e}", exc_info=True)
            return False

    def check_for_commands(self):
        try:
            message = self.audio_queue.get_nowait()
            logger.info(f"Received message from queue: {message}")
            
            if not isinstance(message, dict):
                logger.warning(f"Ignoring non-dict message: {message}")
                return

            if message.get('command') == "shutdown":
                logger.info("Shutdown command received.")
                self.shutdown_flag.set()
                return

            command = message.get('command')
            if command == 'play':
                self.start_playback(message.get('file'))
            elif command == 'stop':
                logger.info("Stop command received, stopping playback.")
                self.stop_playback()
            else:
                logger.warning(f"Unknown command received: {command}")

        except multiprocessing.queues.Empty:
            pass
        except Exception as e:
            logger.error(f"Error checking for commands: {e}", exc_info=True)


    def start_playback(self, file_name):
        logger.debug(f"start_playback called with file: '{file_name}'")
        if self.playing_file_name:
            logger.debug("Playback in progress, stopping it first.")
            self.stop_playback()

        if not file_name:
            logger.error("Play command received without a file name.")
            return

        mp3_path = os.path.join(self.audio_dir, file_name)
        logger.debug(f"Full path to audio file: {mp3_path}")
        if not os.path.exists(mp3_path):
            logger.error(f"Audio file does not exist: '{mp3_path}'")
            return

        try:
            logger.debug(f"Loading and converting '{file_name}' from MP3 to AudioSegment.")
            audio_segment = AudioSegment.from_mp3(mp3_path)
            
            original_sample_rate = audio_segment.frame_rate
            num_channels = audio_segment.channels
            sample_width = audio_segment.sample_width
            pa_format = self.p.get_format_from_width(sample_width)

            target_sample_rate = original_sample_rate
            if not self._is_sample_rate_supported(original_sample_rate, num_channels, pa_format):
                logger.warning(f"Original sample rate {original_sample_rate}Hz not supported by device {self.output_device_index}. Attempting negotiation.")
                common_sample_rates = [44100, 48000, 22050, 16000]
                found_supported_rate = False
                for rate in common_sample_rates:
                    if self._is_sample_rate_supported(rate, num_channels, pa_format):
                        target_sample_rate = rate
                        found_supported_rate = True
                        logger.info(f"Found supported sample rate: {target_sample_rate}Hz. Resampling audio.")
                        audio_segment = audio_segment.set_frame_rate(target_sample_rate)
                        break
                
                if not found_supported_rate:
                    logger.critical(f"CRITICAL: No common sample rates supported. Playback may fail.")
            
            logger.debug(f"Exporting AudioSegment to WAV (in memory) at {target_sample_rate}Hz.")
            wav_io = audio_segment.export(format="wav")
            self.wf = wave.open(wav_io, 'rb')
            
            logger.debug(f"Opening PyAudio stream on device index {self.output_device_index}.")
            self.stream = self.p.open(
                format=self.p.get_format_from_width(self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
                rate=self.wf.getframerate(),
                output=True,
                output_device_index=self.output_device_index
            )
            logger.info(f"Stream opened. Rate: {self.wf.getframerate()}Hz, Channels: {self.wf.getnchannels()}")
            
            self.playing_file_name = file_name
            self.audio_playing_flag.set()
            logger.info(f"AUDIO_FLAG: Set to True (now playing: {file_name}).")

        except Exception as e:
            logger.critical(f"CRITICAL: Failed to start playback for {file_name}: {e}", exc_info=True)
            self.stop_playback()

    def stop_playback(self, delay=0.0):
        if not self.playing_file_name:
            return
            
        logger.debug(f"Stopping playback for '{self.playing_file_name}'.")
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            logger.debug("PyAudio stream stopped and closed.")
        
        if self.wf:
            self.wf.close()
            self.wf = None
            logger.debug("Wave file object closed.")
            
        logger.info(f"Playback stopped for '{self.playing_file_name}'.")
        self.playing_file_name = None
        
        if delay > 0:
            logger.debug(f"Holding audio flag for {delay}s to prevent echo...")
            time.sleep(delay)
            
        self.audio_playing_flag.clear()
        logger.info("AUDIO_FLAG: Cleared.")

    def stream_audio_chunk(self):
        if not self.stream or not self.wf or not self.playing_file_name:
            return

        try:
            data = self.wf.readframes(self.CHUNK_SIZE)
            if data:
                self.stream.write(data)
            else:
                logger.info(f"Finished playing '{self.playing_file_name}' naturally.")
                # Add a delay before clearing the flag to prevent the mic from picking up the tail end (Echo Cancellation)
                self.stop_playback(delay=0.5)
        except IOError as e:
            logger.error(f"Stream IO Error during audio playback: {e}", exc_info=True)
            self.stop_playback()

def pyaudio_player_process(audio_queue, audio_playing_flag, shutdown_flag):
    """The target function for the multiprocessing.Process."""
    setup_logging()
    logger.info("Setting up PyAudioPlayer process.")
    player = PyAudioPlayer(audio_queue, audio_playing_flag)
    player.shutdown_flag = shutdown_flag
    player.start()
