import logging
import multiprocessing
import time
import os
import wave
import pyaudio
from pydub import AudioSegment
from logging_config import setup_logging

logger = logging.getLogger(__name__)

<<<<<<< HEAD
class PyAudioPlayer:
    def __init__(self, audio_queue, audio_playing_flag, audio_dir="audio_cache"):
        self.audio_queue = audio_queue
        self.audio_playing_flag = audio_playing_flag
=======

class PyAudioPlayer:
    SUPPORTED_RATE = 48000 # Centralized supported sample rate

    def __init__(self, audio_queue, audio_feedback_queue, audio_dir="audio_cache"):
        self.audio_queue = audio_queue
        self.audio_feedback_queue = audio_feedback_queue # New queue for feedback
>>>>>>> db2b1d0 (Initial commit)
        self.audio_dir = audio_dir
        self.shutdown_flag = multiprocessing.Event()
        
        self.p = None
        self.stream = None
        self.wf = None
        self.playing_file_name = None
        self.CHUNK_SIZE = 1024
        
<<<<<<< HEAD
        self.output_device_index = 2
=======
        self.output_device_index = -1 # Will be set dynamically

    def _find_output_device_index(self):
        logger.info("Attempting to find a suitable output audio device...")
        if not self.p:
            logger.error("PyAudio not initialized, cannot find devices.")
            return -1

        num_devices = self.p.get_host_api_info_by_index(0).get('deviceCount')
        preferred_names = ["USB Audio Device", "speaker", "pulse", "default"] # Prioritized list
        
        # First, try to find a device by preferred name
        for preferred_name in preferred_names:
            for i in range(num_devices):
                device_info = self.p.get_device_info_by_host_api_device_index(0, i)
                device_name = device_info.get('name', '').lower()

                if preferred_name.lower() in device_name and device_info.get('maxOutputChannels') > 0:
                    # Check if the device supports the SUPPORTED_RATE
                    try:
                        # Test with the minimum number of channels for output (1 or 2)
                        output_channels_to_test = min(device_info.get('maxOutputChannels'), 2)
                        if output_channels_to_test == 0: continue # Skip if no output channels to test with

                        if self.p.is_format_supported(
                            rate=self.SUPPORTED_RATE,
                            input_device=device_info.get('index') if device_info.get('maxInputChannels') > 0 else -1,
                            input_channels=min(device_info.get('maxInputChannels'), 1), # Check with 1 channel for input format
                            input_format=pyaudio.paInt16,
                            output_device=device_info.get('index'),
                            output_channels=output_channels_to_test,
                            output_format=pyaudio.paInt16
                        ):
                            logger.info(f"Found suitable output device '{device_info.get('name')}' at index {i} (preferred: '{preferred_name}').")
                            return i
                    except ValueError:
                        logger.debug(f"Device '{device_name}' (index {i}) does not support {self.SUPPORTED_RATE}Hz with paInt16, {output_channels_to_test} channel(s).")
                    except Exception as e:
                        logger.warning(f"Error checking format for device '{device_name}' (index {i}): {e}")

        logger.warning(f"No preferred output device found supporting {self.SUPPORTED_RATE}Hz. Falling back to default output device if available.")

        # Fallback to the PyAudio default output device
        try:
            default_output_device_info = self.p.get_default_output_device_info()
            default_index = default_output_device_info.get('index')
            default_name = default_output_device_info.get('name')
            
            # Final check to ensure default supports the rate
            if self.p.is_format_supported(
                rate=self.SUPPORTED_RATE,
                input_device=default_output_device_info.get('index') if default_output_device_info.get('maxInputChannels') > 0 else -1,
                input_channels=min(default_output_device_info.get('maxInputChannels'), 1),
                input_format=pyaudio.paInt16,
                output_device=default_output_device_info.get('index'),
                output_channels=min(default_output_device_info.get('maxOutputChannels'), 2), # Test default with max 2 channels
                output_format=pyaudio.paInt16
            ):
                logger.info(f"Using PyAudio default output device: '{default_name}' at index {default_index} (supports {self.SUPPORTED_RATE}Hz).")
                return default_index
            else:
                logger.warning(f"PyAudio default output device '{default_name}' (index {default_index}) does not support {self.SUPPORTED_RATE}Hz. Searching generic devices.")

        except Exception as e:
            logger.error(f"Could not get PyAudio default output device: {e}")
            
        # Last resort: iterate all output devices and pick the first one supporting the rate
        for i in range(num_devices):
            device_info = self.p.get_device_info_by_host_api_device_index(0, i)
            if device_info.get('maxOutputChannels') > 0:
                try:
                    output_channels_to_test = min(device_info.get('maxOutputChannels'), 2)
                    if output_channels_to_test == 0: continue

                    if self.p.is_format_supported(
                        rate=self.SUPPORTED_RATE,
                        input_device=device_info.get('index') if device_info.get('maxInputChannels') > 0 else -1,
                        input_channels=min(device_info.get('maxInputChannels'), 1),
                        input_format=pyaudio.paInt16,
                        output_device=device_info.get('index'),
                        output_channels=output_channels_to_test,
                        output_format=pyaudio.paInt16
                    ):
                        logger.info(f"Using generic output device '{device_info.get('name')}' at index {i} (supports {self.SUPPORTED_RATE}Hz).")
                        return i
                except ValueError:
                    pass
                except Exception as e:
                    logger.warning(f"Error checking generic device '{device_info.get('name')}' (index {i}): {e}")

        logger.critical(f"CRITICAL: No suitable output device found at all that supports {self.SUPPORTED_RATE}Hz. Audio playback will fail.")
        return -1
>>>>>>> db2b1d0 (Initial commit)

    def initialize_audio_system(self):
        try:
            logger.debug("Initializing PyAudio system...")
            self.p = pyaudio.PyAudio()
            logger.info("PyAudio initialized successfully.")
<<<<<<< HEAD
=======
            
            self.output_device_index = self._find_output_device_index()
            if self.output_device_index == -1:
                logger.critical("CRITICAL: Failed to select a valid output audio device. Aborting audio system initialization.")
                self.cleanup_audio_system() # Clean up PyAudio if partially initialized
                return False

            logger.info(f"Selected output device index: {self.output_device_index}")
>>>>>>> db2b1d0 (Initial commit)
            return True
        except Exception as e:
            logger.critical(f"CRITICAL: Failed to initialize PyAudio: {e}", exc_info=True)
            return False

    def cleanup_audio_system(self):
        logger.debug("Cleaning up PyAudio resources.")
<<<<<<< HEAD
        self.stop_playback()
=======
        if self.stream: # Check if stream exists before trying to stop/close
            try:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                logger.error(f"Error while stopping/closing stream during cleanup: {e}")
            finally:
                self.stream = None
>>>>>>> db2b1d0 (Initial commit)
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
<<<<<<< HEAD
            # A short sleep is necessary to prevent this busy-loop from consuming 100% CPU.
            # However, the previous 0.01s was too long, causing buffer underruns.
            # 0.001s is a much safer value that should still be efficient.
=======
>>>>>>> db2b1d0 (Initial commit)
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
<<<<<<< HEAD
=======
            # Send a 'finished' message anyway so the interaction process doesn't get stuck
            self.audio_feedback_queue.put({'status': 'finished', 'error': 'File not found'})
>>>>>>> db2b1d0 (Initial commit)
            return

        try:
            logger.debug(f"Loading and converting '{file_name}' from MP3 to AudioSegment.")
            audio_segment = AudioSegment.from_mp3(mp3_path)
            
<<<<<<< HEAD
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
=======
            logger.debug(f"Enforcing standard sample rate of {self.SUPPORTED_RATE}Hz.")
            audio_segment = audio_segment.set_frame_rate(self.SUPPORTED_RATE)
            # --- End of new simplified resampling logic ---

            logger.debug(f"Exporting AudioSegment to WAV (in memory) at {audio_segment.frame_rate}Hz.")
>>>>>>> db2b1d0 (Initial commit)
            wav_io = audio_segment.export(format="wav")
            self.wf = wave.open(wav_io, 'rb')
            
            logger.debug(f"Opening PyAudio stream on device index {self.output_device_index}.")
            self.stream = self.p.open(
                format=self.p.get_format_from_width(self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
<<<<<<< HEAD
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
=======
                rate=self.SUPPORTED_RATE,
                output=True,
                output_device_index=self.output_device_index
            )
            logger.info(f"Stream opened. Rate: {self.SUPPORTED_RATE}Hz, Channels: {self.wf.getnchannels()}")
            
            self.playing_file_name = file_name
            # The audio_playing_flag is no longer set here.

        except Exception as e:
            logger.critical(f"CRITICAL: Failed to start playback for {file_name}: {e}", exc_info=True)
            self.stop_playback() # This will send the feedback message

    def stop_playback(self):
        """Stops audio playback and cleans up resources. Does NOT send feedback."""
        if not self.playing_file_name:
            # Nothing to do if we are not playing.
>>>>>>> db2b1d0 (Initial commit)
            return
            
        logger.debug(f"Stopping playback for '{self.playing_file_name}'.")
        if self.stream:
<<<<<<< HEAD
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            logger.debug("PyAudio stream stopped and closed.")
=======
            try:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                logger.error(f"Error while stopping/closing stream: {e}")
            finally:
                self.stream = None
                logger.debug("PyAudio stream stopped and closed.")
>>>>>>> db2b1d0 (Initial commit)
        
        if self.wf:
            self.wf.close()
            self.wf = None
            logger.debug("Wave file object closed.")
            
<<<<<<< HEAD
        logger.info(f"Playback stopped for '{self.playing_file_name}'.")
        self.playing_file_name = None
        
        if delay > 0:
            logger.debug(f"Holding audio flag for {delay}s to prevent echo...")
            time.sleep(delay)
            
        self.audio_playing_flag.clear()
        logger.info("AUDIO_FLAG: Cleared.")
=======
        logger.info(f"Playback has been stopped for '{self.playing_file_name}'.")
        self.playing_file_name = None
>>>>>>> db2b1d0 (Initial commit)

    def stream_audio_chunk(self):
        if not self.stream or not self.wf or not self.playing_file_name:
            return

        try:
            data = self.wf.readframes(self.CHUNK_SIZE)
            if data:
                self.stream.write(data)
            else:
<<<<<<< HEAD
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
=======
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
            SUPPORTED_RATE = 48000
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
                rate=SUPPORTED_RATE,
                output=True,
                output_device_index=self.output_device_index
            )
            logger.info(f"Stream opened. Rate: {SUPPORTED_RATE}Hz, Channels: {self.wf.getnchannels()}")
            
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
>>>>>>> db2b1d0 (Initial commit)
    player.shutdown_flag = shutdown_flag
    player.start()
