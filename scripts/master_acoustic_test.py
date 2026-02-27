import os
import sys
import json
import time
import csv
import logging
import argparse
import random
import difflib
import multiprocessing
import queue
import wave
try:
    import pyaudio
except ImportError:
    pyaudio = None
    
try:
    import speech_recognition as sr
except ImportError:
    sr = None

from gtts import gTTS
from pydub import AudioSegment
from datetime import datetime

# Ensure we can import from the root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# Mock/Import necessary modules from the project
try:
    from interaction_process import InteractionProcess
    from logging_config import setup_logging
except ImportError:
    print("Error: Could not import 'InteractionProcess' or 'logging_config'. Make sure you are running this from the project root or the 'scripts' folder.")
    sys.path.append(os.getcwd())
    from interaction_process import InteractionProcess
    from logging_config import setup_logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AcousticTest")

# Constants
CACHE_DIR = os.path.join(project_root, "audio_cache", "test_questions")
RESULTS_FILE = os.path.join(project_root, "tests", "output", f"acoustic_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
DATA_FILE = os.path.join(project_root, "data", "comprehensive_test_data.json")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)
if not os.path.exists(os.path.dirname(RESULTS_FILE)):
    os.makedirs(os.path.dirname(RESULTS_FILE))


class TestInteractionRecorder(InteractionProcess):
    """
    Subclass of InteractionProcess to capture responses instead of playing them.
    """
    def __init__(self, *args, **kwargs):
        # Initialize parent with dummy queues
        super().__init__(multiprocessing.Queue(), multiprocessing.Queue(), multiprocessing.Event(), multiprocessing.Event(), multiprocessing.Queue(), **kwargs)
        self.last_response_text = None
        self.last_response_lang = None
        self.last_reasoning = "Unknown"

    def queue_audio(self, text: str, lang: str, interrupt: bool = True):
        """Override to capture text instead of generating/playing audio."""
        self.last_response_text = text
        self.last_response_lang = lang
        logger.info(f"Captured Robot Response: [{lang}] {text}")

    def log_conversation(self, question, answer, language):
        """Override to capture reasoning context if available."""
        pass # We handle logging in the main test loop

    def process_command_wrapper(self, text, lang):
        """Wrapper to trigger checking and return the result."""
        self.last_response_text = None
        self.last_response_lang = None
        
        # Call the logic directly
        self.process_command(text, lang)
        
        return {
            "response_text": self.last_response_text,
            "response_lang": self.last_response_lang
        }

def find_minidsp_device_index():
    """Locates the miniDSP microphone index."""
    if pyaudio is None:
        logger.warning("PyAudio not installed. Cannot search for microphones.")
        return None
        
    p = pyaudio.PyAudio()
    count = p.get_device_count()
    index = None
    logger.info("Scanning for miniDSP microphone...")
    for i in range(count):
        info = p.get_device_info_by_index(i)
        name = info.get('name', '')
        if 'minidsp' in name.lower() and info.get('maxInputChannels') > 0:
            logger.info(f"Found miniDSP at index {i}: {name}")
            index = i
            break
    p.terminate()
    return index

def play_audio(file_path):
    """Plays an audio file using PyAudio."""
    if pyaudio is None:
        logger.warning("PyAudio not installed. Cannot play audio.")
        return False
        
    chunk = 1024
    try:
        # Convert to wav for PyAudio if needed, or just standard read
        # Using pydub to genericize loading
        audio = AudioSegment.from_file(file_path)
        
        p = pyaudio.PyAudio()
        
        # Convert to 16-bit PCM for PyAudio
        if audio.sample_width != 2:
            audio = audio.set_sample_width(2)
        if audio.channels != 2: # Force Stereo if system prefers, or Auto
             pass 
             
        stream = p.open(format=p.get_format_from_width(audio.sample_width),
                        channels=audio.channels,
                        rate=audio.frame_rate,
                        output=True)

        data = audio.raw_data
        
        # Write in chunks
        for i in range(0, len(data), chunk):
            stream.write(data[i:i+chunk])

        stream.stop_stream()
        stream.close()
        p.terminate()
        return True
    except Exception as e:
        logger.error(f"Failed to play audio {file_path}: {e}")
        return False

def generate_tts_question(text, lang, cache_dir):
    """Generates TTS audio for the test question if not cached."""
    filename = f"q_{lang}_{hash(text)}.mp3"
    path = os.path.join(cache_dir, filename)
    if not os.path.exists(path):
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(path)
            # Small delay to ensure save complete
            time.sleep(0.2)
        except Exception as e:
            logger.error(f"TTS Generation failed: {e}")
            return None
    return path

def run_acoustic_test(limit=None, simulate=False):
    logger.info("Starting Master Test Framework...")
    if simulate:
        logger.info("[MODE] SIMULATION (Text Injection) - Microphone/Speaker Disabled")
    else:
        logger.info("[MODE] ACOUSTIC (Speaker -> Mic) - Full Hardware Loop")
    
    # 1. Initialize Robot Logic
    logger.info("Initializing Interaction Logic...")
    robot_brain = TestInteractionRecorder() # No queues needed for mock

    # 2. Initialize Microphone (Skip in Simulation)
    recognizer = None
    microphone = None
    if not simulate:
        mic_index = find_minidsp_device_index()
        if mic_index is None:
            logger.warning("miniDSP not found, using default microphone.")
        
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 1000
        recognizer.dynamic_energy_threshold = True 
        microphone = sr.Microphone(device_index=mic_index)

    # 3. Load Test Data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    if limit:
        test_data = test_data[:limit]

    # 4. Initialize result CSV
    fieldnames = ['id', 'question_text_orig', 'language', 'audio_file', 'heard_text', 'heard_lang', 'robot_response', 'robot_response_lang', 'match_success', 'reason']
    with open(RESULTS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

    logger.info(f"Loaded {len(test_data)} tests. Starting execution...")

    # Context Manager for Mic (Conditional)
    context_manager = microphone if microphone else open(os.devnull) # Dummy context if no mic

    with context_manager as source:
        if not simulate:
            logger.info("Calibrating microphone for ambient noise (3s)...")
            recognizer.adjust_for_ambient_noise(source, duration=3)

        for i, case in enumerate(test_data):
            logger.info(f"--- Test {i+1}/{len(test_data)}: [{case['id']}] ---")
            
            heard_text = ""
            stt_lang = case['lang']
            audio_path = "SIMULATED"

            if simulate:
                # Direct Injection
                logger.debug(f"Injecting Text: '{case['text']}'")
                heard_text = case['text'] # Perfect hearing
                # Simulate small processing delay removed for speed
                
            else:
                # Step A: Generate Audio for Question
                audio_path = generate_tts_question(case['text'], case['lang'], CACHE_DIR)
                if not audio_path:
                    logger.error("Skipping due to TTS failure.")
                    continue

                # Step B: Play Audio (Speaker)
                logger.info(f"Speaking: '{case['text']}'")
                play_audio(audio_path)

                # Step C: Listen (Microphone)
                logger.info("Listening...")
                try:
                    # Listen with a timeout to avoid hanging if the speaker volume is too low
                    audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    
                    # Step D: Recognize (STT)
                    # Try recognizing in the expected language first, then others if needed
                    language_map = {'en': 'en-IN', 'hi': 'hi-IN', 'te': 'te-IN'}
                    stt_lang_code = language_map.get(case['lang'], 'en-IN')
                    
                    try:
                        heard_text = recognizer.recognize_google(audio_data, language=stt_lang_code)
                        logger.info(f"Heard: '{heard_text}'")
                    except sr.UnknownValueError:
                        logger.warning("Microphone heard nothing interpretable.")
                        heard_text = ""
                    except sr.RequestError as e:
                        logger.error(f"STT API Error: {e}")
                        heard_text = "API_ERROR"

                except sr.WaitTimeoutError:
                    logger.warning("Listening timed out (No audio detected). Check volume?")
                    heard_text = "TIMEOUT"

            # Step E: Process via Robot Brain
            result = robot_brain.process_command_wrapper(heard_text, case['lang'])
            
            # Step F: Validate
            # Simple validation: Did Transcribed Text match Original? Did Robot give a response?
            text_match = difflib.SequenceMatcher(None, case['text'].lower(), heard_text.lower()).ratio()
            match_success = text_match > 0.7
            
            log_row = {
                'id': case['id'],
                'question_text_orig': case['text'],
                'language': case['lang'],
                'audio_file': audio_path,
                'heard_text': heard_text,
                'heard_lang': stt_lang,
                'robot_response': result['response_text'],
                'robot_response_lang': result['response_lang'],
                'match_success': match_success,
                'reason': f"Text Match Ratio: {text_match:.2f}"
            }
            
            # Write to CSV immediately
            with open(RESULTS_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow(log_row)
            
            # Small delay between tests
            if not simulate: time.sleep(1)

    logger.info(f"Test Complete. Results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run acoustic end-to-end tests.")
    parser.add_argument("--limit", type=int, help="Limit number of tests to run (for debugging)", default=None)
    parser.add_argument("--simulate", action="store_true", help="Run in simulation mode (no mic/speaker, direct text injection)")
    args = parser.parse_args()
    
    run_acoustic_test(limit=args.limit, simulate=args.simulate)
