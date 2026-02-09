
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
    PREFERRED_RATES = [48000, 44100, 24000, 16000] # List of preferred sample rates

    def __init__(self, audio_queue, audio_feedback_queue, audio_dir="audio_cache"):
        self.audio_queue = audio_queue
        self.audio_feedback_queue = audio_feedback_queue
        self.audio_dir = audio_dir
        self.shutdown_flag = multiprocessing.Event()
        
        self.p = None
        self.stream = None
        self.wf = None
        self.playing_file_name = None
        self.CHUNK_SIZE = 1024
        
        self.output_device_index = -1
        self.supported_rate = None # Will be set dynamically

    def _find_output_device_and_rate(self):
        logger.info("Attempting to find a suitable output audio device and sample rate...")
        if not self.p:
            logger.error("PyAudio not initialized, cannot find devices.")
            return -1, None

        num_devices = self.p.get_host_api_info_by_index(0).get('deviceCount')
        preferred_names = ["USB Audio Device", "speaker", "pulse", "default"]

        # Iterate through preferred rates first, then devices
        for rate in self.PREFERRED_RATES:
            # First, try to find a device by preferred name
            for preferred_name in preferred_names:
                for i in range(num_devices):
                    device_info = self.p.get_device_info_by_host_api_device_index(0, i)
                    device_name = device_info.get('name', '').lower()

                    if preferred_name.lower() in device_name and device_info.get('maxOutputChannels') > 0:
                        try:
                            output_channels_to_test = min(device_info.get('maxOutputChannels'), 2)
                            if output_channels_to_test == 0: continue

                            if self.p.is_format_supported(
                                rate=rate,
                                output_device=device_info.get('index'),
                                output_channels=output_channels_to_test,
                                output_format=pyaudio.paInt16
                            ):
                                logger.info(f"Found suitable device '{device_info.get('name')}' (index {i}) supporting {rate}Hz.")
                                return i, rate
                        except ValueError:
                            logger.debug(f"Device '{device_name}' (index {i}) does not support {rate}Hz.")
                        except Exception as e:
                            logger.warning(f"Error checking format for device '{device_name}' (index {i}) at {rate}Hz: {e}")
            
            # Fallback: Check default device for the current rate
            try:
                default_output_device_info = self.p.get_default_output_device_info()
                default_index = default_output_device_info.get('index')
                default_name = default_output_device_info.get('name')
                
                if self.p.is_format_supported(
                    rate=rate,
                    output_device=default_index,
                    output_channels=min(default_output_device_info.get('maxOutputChannels'), 2),
                    output_format=pyaudio.paInt16
                ):
                    logger.info(f"Using PyAudio default output device '{default_name}' (index {default_index}) supporting {rate}Hz.")
                    return default_index, rate
            except Exception as e:
                 logger.debug(f"Could not get or validate default output device for {rate}Hz: {e}")

            # Last resort for this rate: check all devices
            for i in range(num_devices):
                device_info = self.p.get_device_info_by_host_api_device_index(0, i)
                if device_info.get('maxOutputChannels') > 0:
                    try:
                        output_channels_to_test = min(device_info.get('maxOutputChannels'), 2)
                        if output_channels_to_test == 0: continue

                        if self.p.is_format_supported(
                            rate=rate,
                            output_device=device_info.get('index'),
                            output_channels=output_channels_to_test,
                            output_format=pyaudio.paInt16
                        ):
                            logger.info(f"Using generic output device '{device_info.get('name')}' (index {i}) supporting {rate}Hz.")
                            return i, rate
                    except ValueError:
                        pass # Format not supported, expected

        logger.critical("CRITICAL: No suitable output device found supporting any of the preferred rates.")
        return -1, None


    def initialize_audio_system(self):
        try:
            logger.debug("Initializing PyAudio system...")
            self.p = pyaudio.PyAudio()
            logger.info("PyAudio initialized successfully.")
            
            self.output_device_index, self.supported_rate = self._find_output_device_and_rate()
            
            if self.output_device_index == -1 or not self.supported_rate:
                logger.critical("CRITICAL: Failed to find a valid output audio device and supported rate. Aborting audio system.")
                self.cleanup_audio_system()
                return False

            logger.info(f"Selected output device index: {self.output_device_index} with a supported rate of {self.supported_rate}Hz.")
            return True
        except Exception as e:
            logger.critical(f"CRITICAL: Failed to initialize PyAudio: {e}", exc_info=True)
            return False

    def cleanup_audio_system(self):
        logger.debug("Cleaning up PyAudio resources.")
        if self.stream:
            try:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                logger.error(f"Error while stopping/closing stream during cleanup: {e}")
            finally:
                self.stream = None
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
            self.audio_feedback_queue.put({'status': 'finished', 'error': 'File not found'})
            return

        try:
            logger.debug(f"Loading '{file_name}' and resampling to {self.supported_rate}Hz.")
            audio_segment = AudioSegment.from_mp3(mp3_path)
            audio_segment = audio_segment.set_frame_rate(self.supported_rate)

            logger.debug(f"Exporting AudioSegment to WAV (in memory) at {audio_segment.frame_rate}Hz.")
            wav_io = audio_segment.export(format="wav")
            self.wf = wave.open(wav_io, 'rb')
            
            logger.debug(f"Opening PyAudio stream on device index {self.output_device_index}.")
            self.stream = self.p.open(
                format=self.p.get_format_from_width(self.wf.getsampwidth()),
                channels=2, # Force stereo output
                rate=self.supported_rate,
                output=True,
                output_device_index=self.output_device_index
            )
            logger.info(f"Stream opened. Rate: {self.supported_rate}Hz, Channels: {self.wf.getnchannels()}")
            
            self.playing_file_name = file_name

        except Exception as e:
            logger.critical(f"CRITICAL: Failed to start playback for {file_name}: {e}", exc_info=True)
            self.stop_playback()

    def stop_playback(self):
        """Stops audio playback and cleans up resources."""
        if not self.playing_file_name:
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
                file_that_finished = self.playing_file_name
                logger.info(f"Finished playing '{file_that_finished}' naturally.")
                self.stop_playback()
                logger.info("Sending 'finished' status to audio_feedback_queue.")
                self.audio_feedback_queue.put({'status': 'finished', 'file': file_that_finished})
        except IOError as e:
            logger.error(f"Stream IO Error during audio playback: {e}", exc_info=True)
            self.stop_playback()
            logger.error("Sending 'finished' status after IO error.")
            self.audio_feedback_queue.put({'status': 'finished', 'error': 'IOError'})

def pyaudio_player_process(audio_queue, audio_feedback_queue, shutdown_flag):
    """The target function for the multiprocessing.Process."""
    setup_logging()
    logger.info("Setting up PyAudioPlayer process.")
    player = PyAudioPlayer(audio_queue, audio_feedback_queue)
    player.shutdown_flag = shutdown_flag
    player.start()
