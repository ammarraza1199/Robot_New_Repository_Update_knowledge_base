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
    def __init__(self, audio_queue, audio_feedback_queue, audio_dir="audio_cache"):
        self.audio_queue = audio_queue
        self.audio_feedback_queue = audio_feedback_queue # New queue for feedback
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
            # Send a 'finished' message anyway so the interaction process doesn't get stuck
            self.audio_feedback_queue.put({'status': 'finished', 'error': 'File not found'})
            return

        try:
            logger.debug(f"Loading and converting '{file_name}' from MP3 to AudioSegment.")
            audio_segment = AudioSegment.from_mp3(mp3_path)
            
            # --- Start of new simplified resampling logic ---
            SUPPORTED_RATE = 44100
            logger.debug(f"Enforcing standard sample rate of {SUPPORTED_RATE}Hz.")
            audio_segment = audio_segment.set_frame_rate(SUPPORTED_RATE)
            # --- End of new simplified resampling logic ---

            logger.debug(f"Exporting AudioSegment to WAV (in memory) at {audio_segment.frame_rate}Hz.")
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
            # The audio_playing_flag is no longer set here.

        except Exception as e:
            logger.critical(f"CRITICAL: Failed to start playback for {file_name}: {e}", exc_info=True)
            self.stop_playback() # This will send the feedback message

    def stop_playback(self):
        """Stops audio playback and cleans up resources. Does NOT send feedback."""
        if not self.playing_file_name:
            # Nothing to do if we are not playing.
            return
            
        logger.debug(f"Stopping playback for '{self.playing_file_name}'.")
        if self.stream:
            try:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                logger.error(f"Error while stopping/closing stream: {e}")
            finally:
                self.stream = None
                logger.debug("PyAudio stream stopped and closed.")
        
        if self.wf:
            self.wf.close()
            self.wf = None
            logger.debug("Wave file object closed.")
            
        logger.info(f"Playback has been stopped for '{self.playing_file_name}'.")
        self.playing_file_name = None

    def stream_audio_chunk(self):
        if not self.stream or not self.wf or not self.playing_file_name:
            return

        try:
            data = self.wf.readframes(self.CHUNK_SIZE)
            if data:
                self.stream.write(data)
            else:
                # Playback finished naturally
                file_that_finished = self.playing_file_name
                logger.info(f"Finished playing '{file_that_finished}' naturally.")
                self.stop_playback() # Clean up resources
                # NOW send the feedback message
                logger.info("Sending 'finished' status to audio_feedback_queue.")
                self.audio_feedback_queue.put({'status': 'finished', 'file': file_that_finished})
        except IOError as e:
            logger.error(f"Stream IO Error during audio playback: {e}", exc_info=True)
            self.stop_playback()
            # Also send feedback on error to un-stick the other process
            logger.error("Sending 'finished' status after IO error.")
            self.audio_feedback_queue.put({'status': 'finished', 'error': 'IOError'})

def pyaudio_player_process(audio_queue, audio_feedback_queue, shutdown_flag):
    """The target function for the multiprocessing.Process."""
    setup_logging()
    logger.info("Setting up PyAudioPlayer process.")
    player = PyAudioPlayer(audio_queue, audio_feedback_queue)
    player.shutdown_flag = shutdown_flag
    player.start()