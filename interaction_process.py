import speech_recognition as sr
import requests
import os
import logging
import time
import hashlib
import csv
from datetime import datetime
from gtts import gTTS
from dotenv import load_dotenv
import re
import sys
import concurrent.futures
<<<<<<< HEAD
=======
from multiprocessing import Queue
from queue import Empty
>>>>>>> db2b1d0 (Initial commit)
import multiprocessing
import random
import numpy as np
from collections import deque
from logging_config import setup_logging
<<<<<<< HEAD
import json # Added for JSON loading

# --- Full Multilingual Knowledge Base (with expanded keywords) ---
# Removed hardcoded DEPARTMENT_KEYWORDS, DEPARTMENT_ROOMS_TE/EN/HI,
# DEPARTMENT_DOCTORS, DEPARTMENT_NAMES_TELUGU
=======
import json
from pydub import AudioSegment
from shared_state import STATE_IDLE, STATE_LISTENING, STATE_SPEAKING, STATE_PROCESSING, STATE_ERROR
import difflib
from indic_transliteration import sanscript
>>>>>>> db2b1d0 (Initial commit)

load_dotenv()
logger = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_CACHE_DIR = os.path.join(SCRIPT_DIR, "audio_cache")
CONVERSATION_LOG_FILE = os.path.join(SCRIPT_DIR, "conversations.csv")
<<<<<<< HEAD
KB_PATH = os.path.join(SCRIPT_DIR, "hospital_knowledge_base.json") # New KB path
=======
KB_PATH = os.path.join(SCRIPT_DIR, "hospital_knowledge_base.json")
>>>>>>> db2b1d0 (Initial commit)

if not os.path.exists(AUDIO_CACHE_DIR):
    os.makedirs(AUDIO_CACHE_DIR)

class InteractionProcess:
<<<<<<< HEAD
    REDIRECT_DEPARTMENTS = {
        "ophthalmology": "general_medicine",
        "eye": "general_medicine",
        "ent": "general_medicine"
    }
    def __init__(self, audio_queue, motor_queue, shutdown_flag, audio_playing_flag, device_index=None):
        self.audio_queue = audio_queue
        self.motor_queue = motor_queue
        self.shutdown_flag = shutdown_flag
        self.audio_playing_flag = audio_playing_flag
        
=======
    def __init__(self, audio_queue, motor_queue, audio_feedback_queue, shutdown_flag, shared_interaction_state, device_index=None):
        self.audio_queue = audio_queue
        self.motor_queue = motor_queue
        self.audio_feedback_queue = audio_feedback_queue
        self.shutdown_flag = shutdown_flag
        self.shared_interaction_state = shared_interaction_state
        
        self.stop_listening_handle = None
        self.is_listening = multiprocessing.Event()

        # Initialize all knowledge base indexes
        self.department_map = {}
        self.keyword_index = {"en": {}, "hi": {}, "te": {}}
        self.people_map = {}
        self.people_index = {}
        self.locations_index = {}
        self.processes_index = {}
        self.policies = {}
        self.policy_keywords = {}
        self.interactions = []

>>>>>>> db2b1d0 (Initial commit)
        logger.info("Initializing speech recognizer...")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=device_index, sample_rate=48000, chunk_size=1024)
        
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        if not self.groq_api_key:
            logger.error("FATAL: GROQ_API_KEY environment variable not set.")
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        
        self.recognizer.energy_threshold = 1000
        self.recognizer.dynamic_energy_threshold = True
<<<<<<< HEAD
=======
        self.recognizer.pause_threshold = 2.0

>>>>>>> db2b1d0 (Initial commit)
        self.SUDDEN_SOUND_THRESHOLD_MULTIPLIER = 2.5
        self.SUDDEN_SOUND_COOLDOWN = 10
        self.last_sudden_sound_time = 0
        self.last_unrecognized_speech_time = 0
        self.UNRECOGNIZED_SPEECH_COOLDOWN = 10

        self.load_knowledge_base()
        self.initialize_conversation_log()

<<<<<<< HEAD
        # Moved anchor and exit commands definition here for clarity
        self.english_anchors = [
            "what is", "where is", "how can i", "how do i", "when should i", "who is",
            "can you tell me", "i want to know", "please tell me", "i am looking for",
            "i have problem", "i am having", "i feel", "i need help", "guide me",
            "where should i go", "which department", "which doctor", "where can i find",
            "please", "help me"
        ]

        self.hindi_anchors = [
            "क्या है", "कहाँ है", "कैसे करूँ", "कब जाना", "कौन सा",
            "मुझे बताइए", "मदद चाहिए", "जानना है", "मैं चाहता हूँ",
            "मुझे समस्या है", "मुझे दर्द है", "मुझे तकलीफ है",
            "किस विभाग", "किस डॉक्टर", "कहाँ जाना", "ओपीडी कहाँ",
            "कृपया", "प्लीज"
        ]

        self.telugu_anchors = [
            "ఏమిటి", "ఎక్కడ ఉంది", "ఎలా చేయాలి", "ఎప్పుడు రావాలి", "ఎవరు",
            "నాకు సహాయం కావాలి", "చెప్పగలరా",
            "నాకు సమస్య ఉంది", "నాకు నొప్పి ఉంది", "నాకు ఇబ్బంది ఉంది",
            "ఏ విభాగం", "ఏ డాక్టర్", "ఎక్కడికి వెళ్లాలి", "ఓపీడి ఎక్కడ",
            "దయచేసి", "ప్లీజ్"
        ]

        self.EXIT_COMMANDS = {
            "en": [
                "exit now", "quit application", "stop interaction",
                "end conversation", "bye bye", "thank you goodbye", "exit", "quit", "stop", "bye"
            ],
            "hi": [
                "बात खत्म", "बंद करो", "अब नहीं", "धन्यवाद अलविदा", "बंद", "रुको", "विदा"
            ],
            "te": [
                "సరే చాలు", "ఆపండి", "ఇంకా వద్దు", "ధన్యవాదాలు", "ఆపు", "వద్దు", "బై"
            ]
        }

        # SYSTEM_PROMPTS for LLM
=======
        self.english_anchors = ["what is", "where is", "how can i", "how do i", "when should i", "who is", "can you tell me", "i want to know", "please tell me", "i am looking for", "i have problem", "i am having", "i feel", "i need help", "guide me", "where should i go", "which department", "which doctor", "where can i find", "please", "help me", "cough", "weeks", "fever", "pain", "symptoms", "duration"]

        self.hindi_anchors = ["क्या है", "कहाँ है", "कैसे करूँ", "कब जाना", "कौन सा", "मुझे बताइए", "मदद चाहिए", "जानना है", "मैं चाहता हूँ", "मुझे समस्या है", "मुझे दर्द है", "मुझे तकलीफ है", "किस विभाग", "किस डॉक्टर", "कहाँ जाना", "ओपीडी कहाँ", "कृपया", "प्लीज", "मुझे", "हफ्तों", "खांसी", "हो रही है", "बुखार", "लक्षण", "समय", "अवधि", "दर्द", "तकलीफ"]
        self.telugu_anchors = ["ఏమిటి", "ఎక్కడ ఉంది", "ఎలా చేయాలి", "ఎప్పుడు రావాలి", "ఎవరు", "నాకు సహాయం కావాలి", "చెప్పగలరా", "నాకు సమస్య ఉంది", "నాకు నొప్పి ఉంది", "నాకు ఇబ్బంది ఉంది", "ఏ విభాగం", "ఏ డాక్టర్", "ఎక్కడికి వెళ్లాలి", "ఓపీడి ఎక్కడ", "దయచేసి", "ప్లీజ్"]
        self.EXIT_COMMANDS = {"en": ["exit", "quit", "stop", "bye"], "hi": ["बंद", "रुको", "विदा"], "te": ["ఆపు", "వద్దు", "బై"]}
>>>>>>> db2b1d0 (Initial commit)
        self.SYSTEM_PROMPTS = {
            'en': "You are a hospital navigation assistant. Your ONLY job is to match user-reported symptoms to the most relevant department from the provided list. Respond ONLY with the department information in the requested format. Do not diagnose, offer advice, or have any other conversation.",
            'hi': "आप एक अस्पताल नेविगेशन सहायक हैं। आपका एकमात्र काम उपयोगकर्ता द्वारा बताए गए लक्षणों को प्रदान की गई सूची से सबसे प्रासंगिक विभाग से मिलाना है। केवल अनुरोधित प्रारूप में विभाग की जानकारी के साथ प्रतिक्रिया दें। निदान, सलाह या कोई अन्य बातचीत न करें।",
            'te': "మీరు హాస్పిటల్ నావిగేషన్ అసిస్టెంట్. వినియోగదారు నివేదించిన లక్షణాలను అందించిన జాబితా నుండి అత్యంత సంబంధిత విభాగానికి సరిపోల్చడం మాత్రమే మీ పని. అభ్యర్థించిన ఫార్మాట్‌లో మాత్రమే విభాగం సమాచారంతో ప్రతిస్పందించండి. నిర్ధారణ, సలహా లేదా మరే ఇతర సంభాషణ చేయవద్దు."
        }
<<<<<<< HEAD


    def initialize_conversation_log(self):
        """Creates the conversation log CSV file with a header if it doesn't exist."""
        logger.debug("Initializing conversation log...")
        try:
            # Create file with header if it's new
            if not os.path.exists(CONVERSATION_LOG_FILE):
                with open(CONVERSATION_LOG_FILE, mode='w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["timestamp", "language", "question", "answer"])
                logger.info(f"Created new conversation log file: {CONVERSATION_LOG_FILE}")
        except Exception as e:
            logger.error(f"Failed to initialize conversation log: {e}", exc_info=True)

    def log_conversation(self, question, answer, language):
        """Appends a new interaction to the conversation log CSV."""
        logger.debug(f"Logging conversation: lang={language}, question='{question}', answer='{answer[:50]}...'")
        try:
            with open(CONVERSATION_LOG_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([datetime.now().isoformat(), language, question, answer])
        except Exception as e:
            logger.error(f"Failed to write to conversation log: {e}", exc_info=True)


    def load_knowledge_base(self):
        """Loads and prepares the multilingual knowledge base from JSON."""
        logger.info("Loading knowledge base from JSON...")
=======
        # --- Transliteration normalization (English spoken in Telugu/Hindi script) ---
        self.transliteration_map = {
            # Telugu → English
            "ఐ హావ్": "i have",
            "హావ్": "have",
            "చెస్ట్": "chest",
            "పెయిన్": "pain",
            "హార్ట్": "heart",
            "బ్రీతింగ్": "breathing",
            "ప్రాబ్లమ్": "problem",
            "డాక్టర్": "doctor",

            # Hindi → English (safe to include)
            "चेस्ट": "chest",
            "पेन": "pain",
            "दिल": "heart",
            "सांस": "breathing",
            "डिसचार्ज": "discharge",
            "प्रक्रिया": "process"
        }

        # --- Emergency keywords (from your KB) ---
        self.EMERGENCY_KEYWORDS = [
            "chest pain",
            "heart pain",
            "breathing problem",
            "breathlessness",
            "shortness of breath",
            "heart attack",
            "sudden chest pain",
            "severe chest pain",

            # Telugu
            "ఛాతీ నొప్పి",
            "గుండె నొప్పి",
            "శ్వాస ఆడకపోవడం",
            "గుండెపోటు",

            # Hindi
            "सीने में दर्द",
            "दिल का दर्द",
            "सांस फूलना"
        ]


    def initialize_conversation_log(self):
        if not os.path.exists(CONVERSATION_LOG_FILE):
            with open(CONVERSATION_LOG_FILE, mode='w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(["timestamp", "language", "status", "question", "answer"])

    def log_conversation(self, question, answer, language, status="SUCCESS"):
        with open(CONVERSATION_LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow([datetime.now().isoformat(), language, status, question, answer])



    def load_knowledge_base(self):
        logger.info("--- Starting Knowledge Base Load ---")
>>>>>>> db2b1d0 (Initial commit)
        try:
            with open(KB_PATH, "r", encoding="utf-8") as f:
                kb = json.load(f)

<<<<<<< HEAD
            self.departments = kb["departments"]
            self.keyword_index = {"en": {}, "hi": {}, "te": {}}
            self.department_map = {} # This will store the full department objects

            for dept_data in self.departments:
                cname = dept_data["canonical_name"]
                self.department_map[cname] = dept_data # Store the full object

                for lang, kws in dept_data["keywords"].items():
                    for kw in kws:
                        self.keyword_index[lang][kw.lower()] = cname
            
            logger.info("Knowledge base loaded successfully from JSON.")

        except FileNotFoundError:
            logger.error(f"Knowledge base file not found at {KB_PATH}. Interaction will be limited.")
            self.departments = []
            self.keyword_index = {"en": {}, "hi": {}, "te": {}}
            self.department_map = {}
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON knowledge base at {KB_PATH}: {e}. Interaction will be limited.")
            self.departments = []
            self.keyword_index = {"en": {}, "hi": {}, "te": {}}
            self.department_map = {}
        except Exception as e:
            logger.error(f"An unexpected error occurred while loading knowledge base: {e}")
            self.departments = []
            self.keyword_index = {"en": {}, "hi": {}, "te": {}}
            self.department_map = {}

    def queue_audio(self, text: str, lang: str, interrupt: bool = True):
        logger.debug(f"queue_audio started with text: '{text[:30]}...', lang: {lang}, interrupt: {interrupt}")
        if not text:
            logger.warning("queue_audio received empty text. Aborting.")
            return
            
        if interrupt:
            logger.debug("Interrupt is True, sending 'stop' command to audio queue.")
            self.audio_queue.put({'command': 'stop'})
            time.sleep(0.1) # Give a moment for the stop command to be processed

=======
            # 1. Departments
            for dept_data in kb.get("departments", []):
                cname = dept_data.get("canonical_name")
                if cname:
                    self.department_map[cname] = dept_data
                    for lang, kws in dept_data.get("keywords", {}).items():
                        if lang in self.keyword_index:
                            for kw in kws: self.keyword_index[lang][kw.lower()] = cname
                    for alias in dept_data.get("aliases", []):
                        for lang in self.keyword_index: self.keyword_index[lang][alias.lower()] = cname

            # 2. People (Management & Doctors)
            all_people = kb.get("management", []) + kb.get("doctors_directory", [])
            for person in all_people:
                pid, name = person.get("id"), person.get("name")
                if pid and name:
                    self.people_map[pid] = person
                    self.people_index[name.lower()] = pid
                    parts = name.split()
                    if len(parts) > 1:
                        self.people_index[f"dr {parts[-1]}".lower()] = pid
                        self.people_index[f"doctor {parts[-1]}".lower()] = pid
                    for kw in person.get("keywords", []): self.people_index[kw.lower()] = pid
            
            # 3. Locations (Services, Diagnostics, Wards, ICUs)
            for key in ["services", "diagnostics", "wards", "icus"]:
                for item in kb.get(key, []):
                    item_id, name = item.get("id"), item.get("name")
                    if item_id and name:
                        item_with_type = item.copy()
                        item_with_type['type'] = key[:-1] # 'services' -> 'service'
                        self.locations_index[name.lower()] = item_with_type
                        for kw in item.get("keywords", []):
                            self.locations_index[kw.lower()] = item_with_type
            
            # 4. Processes
            for process in kb.get("processes", []):
                pid, name = process.get("id"), process.get("name")
                if pid and name: self.processes_index[name.lower()] = process

            # 5. Policies
            self.policies = kb.get("policies", {})
            self.policy_keywords = {
                "visiting hours": "hospital_hours", "how many people": "attendants_allowed",
                "attendants": "attendants_allowed", "lost and found": "lost_and_found",
                "pharmacy hours": "pharmacy_hours"
            }

            # 6. Low Latency Interactions
            self.interactions = kb.get("interactions", [])
            # Handle potential nested 'value' structure from previous merge issues
            if isinstance(self.interactions, dict) and 'value' in self.interactions:
                self.interactions = self.interactions['value']
            
            logger.info(f"Loaded {len(self.interactions)} interaction Q&A pairs.")

            # Manual Patches
            if "pulmonary_medicine" in self.department_map:
                self.keyword_index["te"]["tv"] = "pulmonary_medicine"
                self.keyword_index["hi"]["tv"] = "pulmonary_medicine"
            
            logger.info("--- Knowledge Base Load Complete ---")

        except Exception as e:
            logger.error(f"FATAL: Failed to load knowledge base: {e}", exc_info=True)

    def queue_audio(self, text: str, lang: str):
        if not text:
            self.shared_interaction_state.value = STATE_LISTENING
            self.start_listening()
            return
        self.stop_listening()
        self.shared_interaction_state.value = STATE_SPEAKING
        logger.info(f"STATE: -> SPEAKING ({STATE_SPEAKING})")
>>>>>>> db2b1d0 (Initial commit)
        clean_text = re.sub(r'[\*#\-]', '', text)
        hash_object = hashlib.md5((clean_text + lang).encode())
        audio_filename = f"interaction_{hash_object.hexdigest()}.mp3"
        file_path = os.path.join(AUDIO_CACHE_DIR, audio_filename)
<<<<<<< HEAD
        logger.debug(f"Generated audio filename: {audio_filename}")

        if not os.path.exists(file_path):
            logger.info(f"Audio cache miss. Generating new audio for '{clean_text[:30]}...' in '{lang}'")
            try:
                tts = gTTS(text=clean_text, lang=lang, slow=False)
                tts.save(file_path)
                logger.debug(f"Successfully saved new audio file to {file_path}")
            except Exception as e:
                logger.error(f"gTTS failed to generate or save audio: {e}")
                return
        else:
            logger.debug("Audio cache hit. Using existing file.")
        
        audio_request = {'command': 'play', 'file': audio_filename}
        logger.info(f"Putting audio request on queue: {audio_request}")
        self.audio_queue.put(audio_request)
        logger.debug("Request put on queue successfully.")

    def _calculate_db(self, audio_data):
        """Helper to calculate dB of a raw audio chunk."""
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        if len(audio_array) == 0: return 0
        rms = np.sqrt(np.mean(audio_array.astype(np.float64)**2))
        return 20 * np.log10(rms + 1e-9) if rms > 0 else 0

    def _background_callback(self, recognizer, audio_data):
        """
        This function is called in a background thread whenever audio is detected.
        It attempts to recognize speech and, if that fails, checks for loud sounds.
        """
        logger.debug("BACKGROUND_CALLBACK: Entered _background_callback.")
        if self.audio_playing_flag.is_set():
            logger.debug("BACKGROUND_CALLBACK: Skipping microphone input because audio is playing.")
            return

        candidates = []
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_lang = {executor.submit(recognizer.recognize_google, audio_data, language=f"{lang}-IN"): lang for lang in ['en', 'hi', 'te']}
                for future in concurrent.futures.as_completed(future_to_lang):
                    lang = future_to_lang[future] # lang_simple is just lang here
                    try:
                        text = future.result().lower()
                        if text:
                            logger.info(f"Potential speech match in {lang}: '{text}'")
                            candidates.append({'lang': lang, 'text': text})
                    except sr.UnknownValueError:
                        logger.debug(f"Recognition for {lang}-IN: No speech detected.")
                    except Exception as e:
                        logger.error(f"Recognition error for {lang}-IN: {e}", exc_info=True) # Added exc_info=True

            logger.debug(f"Found {len(candidates)} speech candidates.")
            if candidates:
                # New language selection logic with anchor words
                best_match = None
                highest_score = -1
                
                # Strong anchors represent core grammar words unique to each language
                strong_anchors = {
                    'en': ['the', 'is', 'are', 'am', 'where', 'what', 'can', 'please', 'should', 'would', 'could', 'how', 'when', 'who', 'help', 'want', 'know', 'tell', 'looking', 'find', 'guide', 'give', 'have', 'which', 'go', 'to', 'with', 'from', 'searching', 'i', 'my'],
                    'hi': ['है', 'కहाँ', 'कैसे', 'कब', 'कौन', 'चाहिए', 'बताइए', 'जानना', 'हूँ', 'दर्द', 'तकलीफ', 'समस्या', 'जाना', 'रुको', 'बंद'],
                    'te': ['ఉంది', 'ఎక్కడ', 'ఎలా', 'ఎప్పుడు', 'కావాలి', 'చెప్పగలరా', 'సమస్య', 'నొప్పి', 'ఇబ్బంది', 'వెళ్లాలి', 'చాలు', 'ఆపండి', 'వద్దు']
                }

                for candidate in candidates:
                    text = candidate['text']
                    lang = candidate['lang']
                    
                    # Base score is just the length (to favor longer, more complete sentences)
                    score = len(text)
                    
                    # 1. Strong Anchor Bonus (Grammar Check)
                    # We check how many "strong" grammar words appear in the text.
                    # If we find at least 2, we give a MASSIVE bonus. 
                    # This confirms the "structure" of the language is present.
                    anchors = strong_anchors.get(lang, [])
                    anchor_count = sum(1 for a in anchors if f" {a} " in f" {text} " or text.startswith(a) or text.endswith(a))
                    
                    if anchor_count >= 1:
                        score += 10 # Small boost for 1 anchor
                    if anchor_count >= 2:
                        score += 40 # Huge boost for 2+ anchors (High certainty of language)
                        logger.debug(f"Candidate '{lang}' has {anchor_count} strong anchors. Applying +40 boost.")
                    
                    # 2. Keyword Bonus (Intent Check)
                    # If the text also contains a relevant department keyword, give a boost
                    if lang in self.keyword_index:
                         for kw in self.keyword_index[lang]:
                             if kw in text:
                                 score += 15
                                 break

                    logger.debug(f"Candidate '{lang}' final score: {score}")
                    if score > highest_score:
                        highest_score = score
                        best_match = candidate
                
                MIN_CONFIDENCE_THRESHOLD = 20

                if best_match and highest_score >= MIN_CONFIDENCE_THRESHOLD:
                    logger.info(f"Language detected as '{best_match['lang']}' with score {highest_score} (Text: '{best_match['text']}')")
                    self.process_command(best_match['text'], best_match['lang'])
                elif best_match:
                    logger.warning(f"Ignored speech '{best_match['text']}' in '{best_match['lang']}' due to low confidence score: {highest_score} < {MIN_CONFIDENCE_THRESHOLD}")
                
                return
            else: # No candidates found
                current_time = time.time()
                if (current_time - self.last_unrecognized_speech_time) > self.UNRECOGNIZED_SPEECH_COOLDOWN:
                    self.last_unrecognized_speech_time = current_time
                    if not self.audio_playing_flag.is_set():
                        logger.info("No speech recognized, asking user to repeat.")
                        self.queue_audio("Sorry, I didn't catch that. Please can you ask your question once again?", "en", interrupt=False)

        except Exception as e:
            logger.error(f"Error during speech recognition in callback: {e}", exc_info=True)

        current_time = time.time()
        audio_db = self._calculate_db(audio_data.get_raw_data())
        dynamic_energy_threshold = recognizer.energy_threshold * self.SUDDEN_SOUND_THRESHOLD_MULTIPLIER

        if audio_db > dynamic_energy_threshold:
            if (current_time - self.last_sudden_sound_time) > self.SUDDEN_SOUND_COOLDOWN:
                if not self.audio_playing_flag.is_set():
                    self.last_sudden_sound_time = current_time
                    logger.warning(f"Sudden sound detected (Cough/Sneeze?): {audio_db:.1f} dB > {dynamic_energy_threshold:.1f} dB")
                    self.audio_queue.put({'command': 'play', 'file': 'cough_sneeze.mp3'})

    def process_command(self, command, lang):
        """Processes a recognized text command."""
        logger.debug(f"Processing command '{command}' in language '{lang}'")
        self.motor_queue.put(f"turn_to:{random.randint(-45, 45)}")

        response_text = ""
        if any(cmd in command for cmd in self.EXIT_COMMANDS.get(lang, [])):
            response_text = "Goodbye!"
            self.shutdown_flag.set()
        else:
            matched_dept = self.find_department(command, lang)
            if matched_dept:
                response_text = self._format_guidance_response(matched_dept, lang)
            elif self.is_medical_query(command):
                response_text = "I cannot provide medical advice. Please consult a doctor."
            else:
                llm_response = self.query_llama(command, lang)
                if llm_response:
                    response_text = llm_response
                else: # Fallback if no department, not medical query, AND LLM gave no specific answer
                    if lang == "hi":
                        response_text = "जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेద है। कृपया उत्तर के लिए पास के अस्पताल के कर्मचारियों से पूछें। धन्यवाद।"
                    elif lang == "te":
                        response_text = "సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాను. దయచేసి సమాధానం కోసం దగ్గర్లోని ఆసుపత్రి సిబ్బందిని అడగండి. ధన్యవాదాలు."
                    else: # Default to English
                        response_text = "The information is not with me. I am sorry for your inconvenience. Please ask the nearby hospital staff for the answer. Thank you."
        
        if response_text:
            logger.info(f"--- FINAL AUDIO OUTPUT --- Language: {lang} | Text: '{response_text}'")
            self.log_conversation(command, response_text, lang)
            self.queue_audio(response_text, lang, interrupt=True)
=======
        if not os.path.exists(file_path):
            try:
                gTTS(text=clean_text, lang=lang, slow=False).save(file_path)
            except Exception as e:
                logger.error(f"gTTS failed: {e}", exc_info=True)
                self.audio_feedback_queue.put({'status': 'finished', 'error': 'gTTS failure'})
                return
        self.audio_queue.put({'command': 'play', 'file': audio_filename})

    def _background_callback(self, recognizer, audio_data):
        try:
            self.shared_interaction_state.value = STATE_PROCESSING
            logger.info(f"STATE: -> PROCESSING ({STATE_PROCESSING})")
            candidates = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(recognizer.recognize_google, audio_data, language=f"{lang}-IN"): lang for lang in ['en', 'hi', 'te']}
                for future in concurrent.futures.as_completed(futures):
                    try:
                        text = future.result().lower()
                        text = self.normalize_transliterated_text(text)
                        if text: candidates.append({'lang': futures[future], 'text': text})
                    except sr.UnknownValueError: pass
            if not candidates: 
                self.shared_interaction_state.value = STATE_LISTENING
                return
            best_match = max(candidates, key=self.score_candidate)
            if self.score_candidate(best_match) >= 20: self.process_command(best_match['text'], best_match['lang'])
        except Exception as e:
            self.shared_interaction_state.value = STATE_ERROR
            logger.error(f"FATAL ERROR in _background_callback: {e}", exc_info=True)

    def score_candidate(self, candidate):
        text, lang = candidate['text'], candidate['lang']
        score = 0
        is_phonetic = False

        # --------------------------------------------------
        # 1. Base score: length (neutral, capped)
        # --------------------------------------------------
        score += min(len(text), 40)  # prevent long-text bias

        # --------------------------------------------------
        # 2. Detect phonetic English (robust + fallback)
        # --------------------------------------------------
        if lang != 'en' and not text.isascii():
            source_script = (
                sanscript.DEVANAGARI if lang == 'hi'
                else sanscript.TELUGU if lang == 'te'
                else None
            )

            if source_script:
                try:
                    latin_text = sanscript.transliterate(
                        text, source_script, sanscript.HK
                    ).lower()

                    if any(anchor in latin_text for anchor in self.english_anchors):
                        is_phonetic = True

                except Exception as e:
                    logger.warning(
                        f"Transliteration failed for '{text}': {e}. Falling back."
                    )

            if not is_phonetic:
                is_phonetic = self.is_phonetic_english(text)

        # --------------------------------------------------
        # 3. Meaning confidence (EQUAL for all languages)
        # --------------------------------------------------
        if is_phonetic:
            score += 25  # English meaning detected

        if lang == 'en':
            score += 25  # Native English meaning

        if lang != 'en' and not text.isascii() and not is_phonetic:
            score += 25  # Native Hindi/Telugu meaning

        # --------------------------------------------------
        # 4. Intent anchors (language-agnostic, high weight)
        # --------------------------------------------------
        if any(
            re.search(r'\b' + re.escape(a) + r'\b', text)
            for a in self.english_anchors + self.hindi_anchors + self.telugu_anchors
        ):
            score += 30

        # --------------------------------------------------
        # 5. Knowledge-base keyword evidence (strongest)
        # --------------------------------------------------
        if any(
            re.search(r'\b' + re.escape(kw) + r'\b', text)
            for kw in self.keyword_index.get(lang, {})
        ):
            score += 35

        logger.debug(
            f"Scored candidate: "
            f"{{lang: {lang}, text: '{text}', "
            f"is_phonetic: {is_phonetic}, final_score: {score}}}"
        )

        return score

        
    def normalize_transliterated_text(self, text: str) -> str:
        """
        Converts English words written in Indian scripts into real English
        Example: 'ఐ హావ్ చెస్ట్ పెయిన్' -> 'i have chest pain'
        """
        normalized = text.lower()
        for k, v in self.transliteration_map.items():
            normalized = normalized.replace(k.lower(), v)
        return normalized


    def is_phonetic_english(self, text: str) -> bool:
        """
        Detects English meaning written in non-English script
        """
        english_markers = [
            "chest", "pain", "heart", "breathing",
            "doctor", "problem", "help", "bp", "sugar",
            "what", "where", "when", "who", "why", "how",
            "is", "the", "are", "a", "an", "i", "you", "me",
            "my", "to", "go", "process", "discharge", "appointment",
            "visiting", "hours", "name", "address", "number"
        ]
        normalized = self.normalize_transliterated_text(text)
        return any(m in normalized for m in english_markers)


    def is_emergency(self, text: str) -> bool:
        """
        Hard emergency detector (medical safety)
        """
        text = text.lower()
        return any(kw in text for kw in self.EMERGENCY_KEYWORDS)


    def process_command(self, command, lang):
        logger.info(f"--- Processing command: '{command}' (lang: {lang}) ---")
        normalized_command = self.normalize_transliterated_text(command)

        # 🚨 EMERGENCY OVERRIDE (MEDICAL SAFETY)
        if self.is_emergency(normalized_command):
            logger.warning("EMERGENCY DETECTED — forcing Cardiology/Emergency response")

            response_text = {
                'en': "This may be an emergency. Please go to Cardiology / Emergency immediately. Ground Floor, Main Entrance.",
                'hi': "यह आपातकाल हो सकता है। कृपया तुरंत कार्डियोलॉजी / इमरजेंसी में जाएं।",
                'te': "ఇది అత్యవసర పరిస్థితి కావచ్చు. దయచేసి వెంటనే కార్డియాలజీ / ఎమర్జెన్సీకి వెళ్లండి."
            }.get(lang, 'en')

            self.log_conversation(command, response_text, lang, status="EMERGENCY")
            self.queue_audio(response_text, lang)
            return

        self.motor_queue.put(f"turn_to:{random.randint(-45, 45)}")
        response_text = ""

        if any(re.search(r'\b' + re.escape(cmd) + r'\b', command) for cmd in self.EXIT_COMMANDS.get(lang, [])):
            response_text = "Goodbye!"
            self.shutdown_flag.set()
        else:
            # Tier 1: Attempt to find a direct, low-latency interaction match first.
            response_text = self.find_interaction(command, lang)

            # Tier 2 & 3: If no interaction is found, proceed to more complex entity recognition.
            if not response_text:
                item = self.find_process(command) or self.find_person(command) or self.find_location(command)
                if item:
                    if item['type'] == 'process':
                        response_text = self._format_process_response(item, lang)
                    elif item['type'] == 'person':
                        response_text = self._format_person_response(item, lang)
                    elif item['type'] == 'location':
                        response_text = self._format_location_response(item, lang)
                else:
                    # Tier 4: If no specific item found, search for departments.
                    matched_depts = self.find_department(command, lang)
                    logger.info(f"find_department returned: {matched_depts}")
                    
                    if len(matched_depts) == 1:
                        if self.is_status_query(command, lang):
                            response_text = self._format_status_response(self.department_map.get(matched_depts[0]), lang)
                        else:
                            response_text = self._format_guidance_response(matched_depts[0], lang)
                    elif len(matched_depts) > 1:
                        response_text = self._format_multiple_department_response(matched_depts, lang)
                    elif self.is_medical_query(command):
                        response_text = self.get_medical_advice_response(lang)
                    else:
                        # Fallback if no other category matches
                        response_text = self.query_llama(command, lang) or self.get_fallback_response(lang)
        
        if response_text:
            logger.info(f"Generated response text: '{response_text}'")
            self.log_conversation(command, response_text, lang)
            self.queue_audio(response_text, lang)
        else:
            logger.error(f"--- No response generated for: '{command}' ---")
            self.shared_interaction_state.value = STATE_LISTENING
            self.start_listening()
>>>>>>> db2b1d0 (Initial commit)
        
        time.sleep(1)
        self.motor_queue.put("turn_to:0")

<<<<<<< HEAD
    def find_department(self, user_text, lang):
        logger.debug(f"Finding department for text: '{user_text}' in lang: '{lang}'")
        user_text = user_text.lower()
        if lang not in self.keyword_index:
            return None
            
        # Sort keywords by length (descending) to prioritize longer, specific matches first
        # This helps if one keyword is a substring of another, though regex helps too.
        # But mostly, we want "chest pain" matched before just "pain".
        # Since keyword_index is a dict, we can't sort it directly, so we iterate carefully.
        
        # We'll gather all matches and pick the longest one to be safe.
        best_match_dept = None
        longest_match_len = 0
        matched_kw_log = ""

        for kw, dept_cname in self.keyword_index[lang].items():
            # Escape the keyword to treat special characters (like + or .) literally
            # \b ensures whole word matching
            pattern = r'\b' + re.escape(kw) + r'\b'
            
            if re.search(pattern, user_text):
                if len(kw) > longest_match_len:
                    longest_match_len = len(kw)
                    best_match_dept = dept_cname
                    matched_kw_log = kw

        # --- Secondary Check: Intent-Based Keyword Combinations ---
        # If no direct keyword match was found, look for combinations of words
        if not best_match_dept and lang == 'en':
            COMBINATION_KEYWORDS = {
                "Vascular Surgery": [("foot", "wound"), ("leg", "wound"), ("foot", "healing"), ("leg", "healing")],
                # Add more combinations here as needed
            }
            
            for dept, combos in COMBINATION_KEYWORDS.items():
                for combo in combos:
                    # Check if ALL words in the combination exist in the user text as whole words
                    if all(re.search(r'\b' + re.escape(word) + r'\b', user_text) for word in combo):
                        logger.info(f"--- COMBINATION MATCH --- Found combination {combo} in user text. Mapped to: '{dept}'")
                        return dept

        if best_match_dept:
             # Check for redirection
            dept_cname_lower = best_match_dept.lower()
            if dept_cname_lower in self.REDIRECT_DEPARTMENTS:
                redirect_target = self.REDIRECT_DEPARTMENTS[dept_cname_lower]
                logger.info(f"--- KEYWORD MATCH --- Found '{matched_kw_log}' (whole word) in user text. Mapped to: '{best_match_dept}' (Redirected to: '{redirect_target}')")
                return redirect_target
            else:
                logger.info(f"--- KEYWORD MATCH --- Found '{matched_kw_log}' (whole word) in user text. Mapped to: '{best_match_dept}'")
                return best_match_dept

        logger.debug("No department keyword match found.")
        return None

    def _format_guidance_response(self, dept_cname, lang):
        """Formats the guidance response."""
        dept = self.department_map.get(dept_cname)
        if not dept:
            return None

        name = dept["display_name"].get(lang, dept_cname)
        loc = dept["location"].get(lang, "N/A")
        # Ensure 'doctors' list is not empty before accessing index 0
        doc = dept["doctors"][0]["name"] if dept.get("doctors") and len(dept["doctors"]) > 0 else "Available doctor"
        
        response = ""
        if lang == 'te': response = f"విభాగం పేరు {name}, డాక్టర్ పేరు {doc}, మరియు చిరునామా {loc}."
        elif lang == 'hi': response = f"विभाग का नाम {name}, डॉक्टर का नाम {doc}, और पता {loc} है।"
        else: response = f"The department name is {name}, the doctor's name is {doc}, and the address is {loc}."
        logger.debug(f"Formatted guidance response: {response}")
        return response

    def is_medical_query(self, text):
        medical_keywords = ["what is", "symptoms of", "causes of", "treatment for", "diagnose", "medicine for", "pain in", "kya hai", "lakshan", "ilaaj", "noppi", "mandhu"]
        is_query = any(keyword in text for keyword in medical_keywords)
        logger.debug(f"is_medical_query check for text '{text}': {is_query}")
        return is_query

    def query_llama(self, user_text, lang):
        """Queries the Llama 3.1 model via Groq API."""
        logger.debug(f"Querying LLM for text: '{user_text}'")
        
        context_parts = []
        for dept_cname, dept_data in self.department_map.items():
            name = dept_data["display_name"].get(lang, dept_cname)
            loc = dept_data["location"].get(lang, "N/A")
            doc = dept_data["doctors"][0]["name"] if dept_data.get("doctors") and len(dept_data["doctors"]) > 0 else "Available doctor"
            
            # Add keywords to context so LLM knows what the department HANDLES
            keywords = ", ".join(dept_data["keywords"].get(lang, []))
            context_parts.append(f"- Department: {name}, Doctor: {doc}, Location: {loc}, Treats/Symptoms: {keywords}")
            
        context = "Here is the hospital data:\n" + "\n".join(context_parts)

        system_prompt = self.SYSTEM_PROMPTS.get(lang, self.SYSTEM_PROMPTS['en']) + context
        headers = {"Authorization": f"Bearer {self.groq_api_key}", "Content-Type": "application/json"}
        payload = {"model": "llama-3.1-8b-instant", "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_text}], "max_tokens": 150}
        
        start_time = time.time()
        try:
            logger.debug(f"Sending request to Groq API at {self.groq_url}...")
            response = requests.post(self.groq_url, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            llm_response = data["choices"][0]["message"]["content"].strip()
            end_time = time.time()
            logger.info(f"LLM request completed in {end_time - start_time:.2f} seconds. Response: '{llm_response[:50]}...'")
            return llm_response
        except requests.exceptions.RequestException as e:
            end_time = time.time()
            logger.error(f"Groq API request failed after {end_time - start_time:.2f} seconds: {e}", exc_info=True)
            return "Sorry, I'm having trouble connecting to my brain."

    def start(self):
        """Main entry point for the interaction process."""
        if not self.groq_api_key:
            logger.error("Interaction process cannot start without GROQ_API_KEY.")
            return

        # Added delay to ensure audio player is fully initialized before speaking
        logger.info("Interaction Process: Waiting 5 seconds for audio player and other services to warm up...")
        time.sleep(5)

        logger.info("Interaction Process running...")
        logger.info("Attempting to queue welcome message...")
        self.queue_audio("Hello, how can I help you?", "en", interrupt=False)
        logger.info("Welcome message queued.")

        with self.microphone as source:
            logger.info("Calibrating for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
            logger.info(f"Ambient energy threshold set to: {self.recognizer.energy_threshold:.2f}")

        # The old `listen_in_background` takes a `microphone` object.
        # The new logic needs access to `self.microphone` from the `InteractionProcess` instance.
        # The `_background_callback` itself does not need the `microphone` argument, only the `recognizer` and `audio_data`.
        # However, `listen_in_background` expects the `audio_source` (which is `self.microphone`)
        # It seems the `speech_recognition` library handles passing the `audio_data` implicitly.
        # The important part is that `self.microphone` (the AudioSource) needs to be initialized.
        stop_listening = self.recognizer.listen_in_background(self.microphone, self._background_callback, phrase_time_limit=15)
        logger.info("Background listener started.")

        while not self.shutdown_flag.is_set():
            time.sleep(0.5)

        logger.info("Shutting down Interaction Process...")
        stop_listening(wait_for_stop=False)
        logger.info("Background listener stopped.")

def interaction_process_func(audio_queue, motor_queue, shutdown_flag, audio_playing_flag, mic_name="miniDSP"):
    setup_logging()
    logger = logging.getLogger(__name__)

    device_index = None
    try:
        logger.info("Searching for available microphones...")
        mic_names = sr.Microphone.list_microphone_names()
        logger.debug(f"Available microphones: {mic_names}")
        for i, name in enumerate(mic_names):
            if mic_name.lower() in name.lower():
                device_index = i
                logger.info(f"SUCCESS: Found microphone '{mic_name}' at index {i}.")
                break
        if device_index is None:
            logger.warning(f"WARNING: Microphone '{mic_name}' not found. Falling back to default microphone.")
    except Exception as e:
        logger.error(f"Could not list microphones: {e}. Using default microphone.")

    interaction_system = InteractionProcess(audio_queue, motor_queue, shutdown_flag, audio_playing_flag, device_index=device_index)
    interaction_system.start()
=======
    def find_interaction(self, text, lang):
        logger.info(f"find_interaction: Searching for interaction in text: '{text}' (lang: {lang})")
        if not self.interactions:
            logger.warning("find_interaction: No interactions loaded.")
            return None
        
        text = text.lower().strip()
        
        best_match_score = 0
        best_answer = None

        # 1. Exact/Substring Match on Keywords (High Precision)
        for item in self.interactions:
            keywords = item.get("keywords", {}).get(lang, [])
            if not keywords:
                continue

            matched_keywords_score = 0
            for kw in keywords:
                if lang == 'en':
                    pattern = r'\b' + re.escape(kw) + r'\b'
                else:
                    pattern = r'(?:^|\s)' + re.escape(kw)
                
                if re.search(pattern, text, re.IGNORECASE):
                    # Longer keywords get a higher score
                    matched_keywords_score += len(kw)

            if matched_keywords_score > best_match_score:
                best_match_score = matched_keywords_score
                best_answer = item.get("answer", {}).get(lang)

        if best_answer:
            logger.info(f"find_interaction: Found best keyword match with score {best_match_score}. Best answer: {best_answer}")
            return best_answer

        # 2. Fuzzy Match on Question Text (Fallback for natural language)
        logger.info("find_interaction: No keyword match found. Trying fuzzy match on question text.")
        best_ratio = 0.0
        for item in self.interactions:
            question = item.get("question", {}).get(lang, "")
            if question:
                ratio = difflib.SequenceMatcher(None, text, question.lower()).ratio()
                logger.debug(f"find_interaction: Fuzzy match ratio for '{text}' vs '{question.lower()}': {ratio}")
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_answer = item.get("answer", {}).get(lang)

        # Threshold for fuzzy match
        if best_ratio > 0.75:
            logger.info(f"find_interaction: Found fuzzy match with ratio {best_ratio}. Best answer: {best_answer}")
            return best_answer
        
        logger.info("find_interaction: No interaction found.")
        return None

    def find_process(self, text):
        for kw, process_obj in self.processes_index.items():
            if re.search(r'\b' + re.escape(kw) + r'\b', text.lower()):
                return {**process_obj, 'type': 'process'}
        return None

    def find_person(self, text):
        for kw, pid in self.people_index.items():
            if re.search(r'\b' + re.escape(kw) + r'\b', text.lower()):
                return {**self.people_map.get(pid, {}), 'type': 'person'}
        return None

    def find_location(self, text):
        for kw, loc_obj in self.locations_index.items():
            if re.search(r'\b' + re.escape(kw) + r'\b', text.lower()):
                return {**loc_obj, 'type': 'location'}
        return None

    # find_policy removed


    def find_department(self, text, lang):
        logger.info(f"find_department: Searching for all departments in text: '{text}' (lang: {lang})")
        if lang not in self.keyword_index:
            logger.info(f"find_department: Language '{lang}' not in keyword_index.")
            return []
        
        matched_departments = set()
        sorted_keywords = sorted(self.keyword_index[lang].items(), key=lambda item: len(item[0]), reverse=True)
        
        # Create a copy of the text to mark matched parts
        processed_text = text.lower()

        for kw, dept_cname in sorted_keywords:
            if lang == 'en':
                # Strict boundary for English to avoid partial matches
                pattern = r'\b' + re.escape(kw) + r'\b'
            else:
                # Relaxed right-boundary for Hindi/Telugu (Agglutinative)
                # Match start of word (boundary or space), but allow suffix
                pattern = r'(?:^|\s)' + re.escape(kw)

            # Use re.finditer to find all non-overlapping matches
            for match in re.finditer(pattern, processed_text):
                # Check if this part of the string has already been "claimed" by a longer keyword
                # This is a simple way to prioritize longer matches, e.g., "General Medicine" over "Medicine"
                start, end = match.span()
                if all(c == ' ' for c in processed_text[start:end]): # crude check if it's already masked
                    continue

                logger.info(f"find_department: Matched keyword '{kw}' to department '{dept_cname}'.")
                matched_departments.add(dept_cname)
                
                # Mask the found keyword so it's not matched again by a shorter sub-keyword
                processed_text = processed_text[:start] + ' ' * (end - start) + processed_text[end:]

        if not matched_departments:
            logger.info(f"find_department: No department found for text: '{text}'.")
        
        return list(matched_departments)

    def _format_process_response(self, data, lang):
        steps = data.get('steps', [])
        if not steps: return None
        name = data.get('name', 'the process')
        response = f"The process for {name} is as follows: " + ". ".join([f"Step {i+1}, {step}" for i, step in enumerate(steps)])
        return response
        
    def _format_person_response(self, data, lang):
        name = data.get("name", "that person")
        role = data.get("role") or data.get("designation")
        dept = data.get("department")
        if role and dept: return f"{name} is the {role} in the {dept} department."
        elif role: return f"That person is {name}, who is the {role}."
        return f"I have information for {name}, but not their specific role."

    def _format_location_response(self, data, lang):
        name = data.get("name", "that location")
        loc = data.get("location", "an unknown location")
        return f"You can find {name} at: {loc}."

    # _format_policy_response removed as explicit policy lookup is deprecated in favor of interactions


    def _format_guidance_response(self, dept_cname, lang):
        dept = self.department_map.get(dept_cname, {})
        name = dept.get("display_name", {}).get(lang, dept_cname)
        loc = dept.get("location", {}).get(lang, "N/A")
        doc = (dept.get("doctors") or [{}])[0].get("name", "Available doctor")
        formats = {
            'te': f"విభాగం పేరు {name}, డాక్టర్ పేరు {doc}, మరియు చిరునామా {loc}.",
            'hi': f"विभाग का नाम {name}, डॉक्टर का नाम {doc}, और पता {loc} है।",
            'en': f"The department name is {name}, the doctor's name is {doc}, and the address is {loc}."
        }
        return formats.get(lang, formats['en'])

    def _format_multiple_department_response(self, dept_cnames, lang):
        dept_names = [self.department_map.get(cname, {}).get("display_name", {}).get(lang, cname) for cname in dept_cnames]
        
        if lang == 'hi':
            response = f"मुझे कई मिलते-जुलते विभाग मिले हैं: {', '.join(dept_names)}। आप किसके बारे में जानना चाहेंगे?"
        elif lang == 'te':
            response = f"నాకు అనేక సరిపోలే విభాగాలు దొరికాయి: {', '.join(dept_names)}. మీరు దేని గురించి తెలుసుకోవాలనుకుంటున్నారు?"
        else: # Default to English
            response = f"I found multiple matching departments: {', '.join(dept_names)}. Which one would you like to know about?"
            
        return response

    def is_status_query(self, text, lang):
        text = text.lower()
        keywords = {
            'en': ['open', 'close', 'time', 'timing', 'when', 'available', 'hours'],
            'hi': ['खुला', 'बंद', 'समय', 'कब', 'टटाइम', 'टाइम', 'घंटे'],
            'te': ['తీసి', 'మూసి', 'సమయం', 'టైం', 'ఎప్పుడు', 'గంటలు', 'open', 'close', 'time', 'ఓపెన్', 'క్లోజ్'] 
        }
        return any(kw in text for kw in keywords.get(lang, keywords['en']))

    def _format_status_response(self, dept_data, lang):
        if not dept_data: return None
        name = dept_data.get("display_name", {}).get(lang, dept_data.get("canonical_name"))
        timings = dept_data.get("timings", "9:00 AM - 4:00 PM")
        
        formats = {
            'en': f"The {name} represents open from {timings}.", 
            'hi': f"{name} {timings} तक खुला रहता है।",
            'te': f"{name} {timings} వరకు తెరిచి ఉంటుంది."
        }
        return formats.get(lang, formats['en'])

    def is_medical_query(self, text):
        keywords = [
            "symptoms", "causes", "treatment", "diagnose", "medicine", "drug", "cure", "tablet", "pills", # English
            "लक्षण", "इलाज", "दवा", "चिकित्सा", "कारण", "निदान", "बीमारी", # Hindi
            "లక్షణాలు", "చికిత్స", "మందు", "కారణాలు", "నిర్ధారణ", "తగ్గడం", "నొప్పి" # Telugu
        ]
        return any(kw in text.lower() for kw in keywords)

    def get_medical_advice_response(self, lang):
        return {
            'hi': "मैं चिकित्सकीय सलाह नहीं दे सकता। कृपया डॉक्टर से संपर्क करें।",
            'te': "నేను వైద్య సలహా ఇవ్వలేను. దయచేసి డాక్టర్‌ని సంప్రదించండి.",
            'en': "I cannot provide medical advice. Please consult a doctor."
        }.get(lang, 'en')

    def get_fallback_response(self, lang):
        return {'hi': "जानकारी मेरे पास नहीं है।", 'te': "సమాచారం నా దగ్గర లేదు.", 'en': "I do not have that information."}.get(lang, 'en')

    def query_llama(self, user_text, lang):
        # This can be simplified or removed if the local search is comprehensive enough
        return None 

    def stop_listening(self):
        if self.is_listening.is_set() and self.stop_listening_handle:
            self.stop_listening_handle(wait_for_stop=False)
            self.is_listening.clear()
            logger.info("Background listener stopped.")

    def start_listening(self):
        if not self.is_listening.is_set():
            self.shared_interaction_state.value = STATE_LISTENING
            logger.info(f"STATE: -> LISTENING ({STATE_LISTENING})")
            self.is_listening.set()
            self.stop_listening_handle = self.recognizer.listen_in_background(self.microphone, self._background_callback, phrase_time_limit=15)
            logger.info("Background listener started.")

    def start(self):
        if not self.groq_api_key: return logger.error("GROQ_API_KEY not set.")
        logger.info("Waiting 5s for services to warm up...")
        time.sleep(5)
        
        with sr.Microphone(device_index=self.microphone.device_index, sample_rate=48000, chunk_size=1024) as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
        
        self.queue_audio("Welcome to NIMS hospital guiding system", "en")

        while not self.shutdown_flag.is_set():
            try:
                message = self.audio_feedback_queue.get(timeout=1.0)
                if message.get('status') == 'finished':
                    self.start_listening()
            except Empty:
                if self.shared_interaction_state.value == STATE_SPEAKING: continue
                elif not self.is_listening.is_set():
                    self.start_listening()

        self.stop_listening()
        logger.info("Interaction Process Shutting Down.")

def interaction_process_func(audio_queue, motor_queue, audio_feedback_queue, shutdown_flag, shared_interaction_state):
    setup_logging()
    device_index = None
    try:
        for i, name in enumerate(sr.Microphone.list_microphone_names()):
            if "miniDSP".lower() in name.lower():
                device_index = i
                break
    except Exception as e:
        logger.error(f"Could not list mics: {e}. Using default.")

    interaction_system = InteractionProcess(audio_queue, motor_queue, audio_feedback_queue, shutdown_flag, shared_interaction_state, device_index=device_index)
    interaction_system.start()
    
>>>>>>> db2b1d0 (Initial commit)
