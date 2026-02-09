
import multiprocessing
import time
import os
from gtts import gTTS
from queue import Empty
from pydub import AudioSegment
from pyaudio_player import pyaudio_player_process
import logging
from logging_config import setup_logging

# Setup basic logging for the test script
setup_logging()
logger = logging.getLogger(__name__)

AUDIO_DIR = "audio_cache"
TEST_AUDIO_FILENAME_MP3 = "speaker_test.mp3"
TEST_AUDIO_FILENAME_WAV = "speaker_test.wav"
TEST_PHRASE = "Speaker test successful."

def generate_test_audio():
    """Generates the test MP3 and converts it to a stereo WAV file."""
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)
        logger.info(f"Created audio cache directory: {AUDIO_DIR}")

    mp3_path = os.path.join(AUDIO_DIR, TEST_AUDIO_FILENAME_MP3)
    wav_path = os.path.join(AUDIO_DIR, TEST_AUDIO_FILENAME_WAV)

    try:
        # Generate MP3 only if it doesn't exist to save time/network
        if not os.path.exists(mp3_path):
            logger.info(f"Generating test audio with phrase: '{TEST_PHRASE}'...")
            tts = gTTS(text=TEST_PHRASE, lang='en', slow=False)
            tts.save(mp3_path)
            logger.info(f"Successfully saved test audio to '{mp3_path}'.")
        else:
            logger.info(f"MP3 file '{mp3_path}' already exists. Skipping generation.")

        # Always regenerate the WAV from the MP3 to ensure it's the correct format
        logger.info(f"Converting '{mp3_path}' to stereo WAV format...")
        audio = AudioSegment.from_mp3(mp3_path)
        audio = audio.set_channels(2) # Ensure WAV is stereo
        audio.export(wav_path, format="wav")
        logger.info(f"Successfully saved/updated test WAV file to '{wav_path}'.")
            
        return True
    except Exception as e:
        logger.critical(f"Failed to generate test audio files: {e}", exc_info=True)
        print("\n---")
        print("ERROR: Could not generate the test audio files.")
        print("Please check your internet connection or file permissions.")
        print("---\n")
        return False

def run_speaker_test():
    """
    Initializes the audio player process, sends a play command, and waits for completion.
    """
    if not generate_test_audio():
        return

    audio_queue = multiprocessing.Queue()
    audio_feedback_queue = multiprocessing.Queue()
    shutdown_flag = multiprocessing.Event()

    # Start the audio player process
    player_process = multiprocessing.Process(
        target=pyaudio_player_process,
        args=(audio_queue, audio_feedback_queue, shutdown_flag),
        name="AudioPlayerProcess"
    )
    player_process.daemon = True
    player_process.start()
    
    # Give the player a moment to initialize
    time.sleep(2)

    if not player_process.is_alive():
        logger.critical("Audio player process failed to start. Aborting test.")
        print("\n---")
        print("ERROR: The audio player process failed to start.")
        print("This could be due to a missing audio device or a configuration issue.")
        print("Please check the 'logs/robot_run.log' file for detailed errors.")
        print("---\n")
        return

    logger.info(f"Sending 'play' command for file: {TEST_AUDIO_FILENAME_MP3}")
    print("\n---")
    print(f"▶️  Attempting to play test sound via Python script... You should hear: '{TEST_PHRASE}'")
    print("---\n")
    audio_queue.put({'command': 'play', 'file': TEST_AUDIO_FILENAME_MP3})

    try:
        feedback = audio_feedback_queue.get(timeout=15)
        logger.info(f"Received feedback from player: {feedback}")
        if feedback.get('status') == 'finished' and 'error' not in feedback:
            print("\n---")
            print("✅ SUCCESS (Python Script): The audio player reported that playback finished successfully.")
            print("If you heard the test phrase, your speaker connection is working.")
            print("---\n")
        else:
            error_msg = feedback.get('error', 'Unknown error')
            logger.error(f"Playback failed with error: {error_msg}")
            print("\n---")
            print(f"❌ FAILURE (Python Script): The audio player reported an error: {error_msg}")
            print("---\n")
            
    except Empty:
        logger.error("Test timed out. No feedback received from the audio player.")
        print("\n---")
        print("❌ FAILURE (Python Script): Test timed out.")
        print("This likely means the player process crashed or is stuck.")
        print("---\n")
        
    finally:
        logger.info("Shutting down the audio player process.")
        shutdown_flag.set()
        time.sleep(1)
        if player_process.is_alive():
            player_process.terminate()
        player_process.join(timeout=5)
        logger.info("Python script test finished.")

if __name__ == "__main__":
    run_speaker_test()

