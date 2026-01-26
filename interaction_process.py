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
from multiprocessing import Queue
from queue import Empty
import multiprocessing
import random
import numpy as np
from collections import deque
from logging_config import setup_logging
import json
from pydub import AudioSegment
from shared_state import STATE_IDLE, STATE_LISTENING, STATE_SPEAKING, STATE_PROCESSING, STATE_ERROR
import difflib

load_dotenv()
logger = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_CACHE_DIR = os.path.join(SCRIPT_DIR, "audio_cache")
CONVERSATION_LOG_FILE = os.path.join(SCRIPT_DIR, "conversations.csv")
KB_PATH = os.path.join(SCRIPT_DIR, "hospital_knowledge_base.json")

if not os.path.exists(AUDIO_CACHE_DIR):
    os.makedirs(AUDIO_CACHE_DIR)

class InteractionProcess:
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

        logger.info("Initializing speech recognizer...")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=device_index, sample_rate=48000, chunk_size=1024)
        
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        if not self.groq_api_key:
            logger.error("FATAL: GROQ_API_KEY environment variable not set.")
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        
        self.recognizer.energy_threshold = 1000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 2.0

        self.SUDDEN_SOUND_THRESHOLD_MULTIPLIER = 2.5
        self.SUDDEN_SOUND_COOLDOWN = 10
        self.last_sudden_sound_time = 0
        self.last_unrecognized_speech_time = 0
        self.UNRECOGNIZED_SPEECH_COOLDOWN = 10

        self.load_knowledge_base()
        self.initialize_conversation_log()

        self.english_anchors = ["what is", "where is", "how can i", "how do i", "when should i", "who is", "can you tell me", "i want to know", "please tell me", "i am looking for", "i have problem", "i am having", "i feel", "i need help", "guide me", "where should i go", "which department", "which doctor", "where can i find", "please", "help me"]
        self.hindi_anchors = ["क्या है", "कहाँ है", "कैसे करूँ", "कब जाना", "कौन सा", "मुझे बताइए", "मदद चाहिए", "जानना है", "मैं चाहता हूँ", "मुझे समस्या है", "मुझे दर्द है", "मुझे तकलीफ है", "किस विभाग", "किस डॉक्टर", "कहाँ जाना", "ओपीडी कहाँ", "कृपया", "प्लीज"]
        self.telugu_anchors = ["ఏమిటి", "ఎక్కడ ఉంది", "ఎలా చేయాలి", "ఎప్పుడు రావాలి", "ఎవరు", "నాకు సహాయం కావాలి", "చెప్పగలరా", "నాకు సమస్య ఉంది", "నాకు నొప్పి ఉంది", "నాకు ఇబ్బంది ఉంది", "ఏ విభాగం", "ఏ డాక్టర్", "ఎక్కడికి వెళ్లాలి", "ఓపీడి ఎక్కడ", "దయచేసి", "ప్లీజ్"]
        self.EXIT_COMMANDS = {"en": ["exit", "quit", "stop", "bye"], "hi": ["बंद", "रुको", "विदा"], "te": ["ఆపు", "వద్దు", "బై"]}
        self.SYSTEM_PROMPTS = {
            'en': "You are a hospital navigation assistant. Your ONLY job is to match user-reported symptoms to the most relevant department from the provided list. Respond ONLY with the department information in the requested format. Do not diagnose, offer advice, or have any other conversation.",
            'hi': "आप एक अस्पताल नेविगेशन सहायक हैं। आपका एकमात्र काम उपयोगकर्ता द्वारा बताए गए लक्षणों को प्रदान की गई सूची से सबसे प्रासंगिक विभाग से मिलाना है। केवल अनुरोधित प्रारूप में विभाग की जानकारी के साथ प्रतिक्रिया दें। निदान, सलाह या कोई अन्य बातचीत न करें।",
            'te': "మీరు హాస్పిటల్ నావిగేషన్ అసిస్టెంట్. వినియోగదారు నివేదించిన లక్షణాలను అందించిన జాబితా నుండి అత్యంత సంబంధిత విభాగానికి సరిపోల్చడం మాత్రమే మీ పని. అభ్యర్థించిన ఫార్మాట్‌లో మాత్రమే విభాగం సమాచారంతో ప్రతిస్పందించండి. నిర్ధారణ, సలహా లేదా మరే ఇతర సంభాషణ చేయవద్దు."
        }

    def initialize_conversation_log(self):
        if not os.path.exists(CONVERSATION_LOG_FILE):
            with open(CONVERSATION_LOG_FILE, mode='w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(["timestamp", "language", "status", "question", "answer"])

    def log_conversation(self, question, answer, language, status="SUCCESS"):
        with open(CONVERSATION_LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow([datetime.now().isoformat(), language, status, question, answer])



    def load_knowledge_base(self):
        logger.info("--- Starting Knowledge Base Load ---")
        try:
            with open(KB_PATH, "r", encoding="utf-8") as f:
                kb = json.load(f)

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
        clean_text = re.sub(r'[\*#\-]', '', text)
        hash_object = hashlib.md5((clean_text + lang).encode())
        audio_filename = f"interaction_{hash_object.hexdigest()}.mp3"
        file_path = os.path.join(AUDIO_CACHE_DIR, audio_filename)
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
        score = len(text)
        if any(re.search(r'\b' + re.escape(a) + r'\b', text) for a in self.english_anchors + self.hindi_anchors + self.telugu_anchors): score += 10
        if any(re.search(r'\b' + re.escape(kw) + r'\b', text) for kw in self.keyword_index.get(lang, {})): score += 15
        return score

    def process_command(self, command, lang):
        logger.info(f"--- Processing command: '{command}' (lang: {lang}) ---")
        self.motor_queue.put(f"turn_to:{random.randint(-45, 45)}")
        response_text = ""

        if any(re.search(r'\b' + re.escape(cmd) + r'\b', command) for cmd in self.EXIT_COMMANDS.get(lang, [])):
            response_text = "Goodbye!"
            self.shutdown_flag.set()
        else:
            item = None
            response_text = ""
            
            # 1. Low Latency Keyword/Fuzzy Match (Tier 1)
            ia_match = self.find_interaction(command, lang)
            if ia_match:
                 response_text = ia_match
            
            if not response_text:
                 # 2. Existing logic (Tier 2 & 3)
                 # Removed find_policy(command) as it is now covered by find_interaction (Tier 1)
                 item = self.find_process(command) or self.find_person(command) or self.find_location(command)
            if item:
                if item['type'] == 'process': response_text = self._format_process_response(item, lang)
                elif item['type'] == 'person': response_text = self._format_person_response(item, lang)
                elif item['type'] == 'location': response_text = self._format_location_response(item, lang)
                # Policy type handling removed
            else:
                matched_depts = self.find_department(command, lang)
                logger.info(f"find_department returned: {matched_depts}")
                
                if len(matched_depts) == 1:
                    # Check for Status/Timing Query
                    if self.is_status_query(command, lang):
                        response_text = self._format_status_response(self.department_map.get(matched_depts[0]), lang)
                    else:
                        response_text = self._format_guidance_response(matched_depts[0], lang)
                elif len(matched_depts) > 1:
                    response_text = self._format_multiple_department_response(matched_depts, lang)
                elif self.is_medical_query(command):
                    response_text = self.get_medical_advice_response(lang)
                else:
                    response_text = self.query_llama(command, lang) or self.get_fallback_response(lang)
        
        if response_text:
            logger.info(f"Generated response text: '{response_text}'")
            self.log_conversation(command, response_text, lang)
            self.queue_audio(response_text, lang)
        else:
            logger.error(f"--- No response generated for: '{command}' ---")
            self.shared_interaction_state.value = STATE_LISTENING
            self.start_listening()
        
        time.sleep(1)
        self.motor_queue.put("turn_to:0")

    def find_interaction(self, text, lang):
        if not self.interactions: return None
        
        text = text.lower().strip()
        best_ratio = 0.0
        best_answer = None
        
        # 1. Exact/Substring Match on Keywords (High Precision)
        for item in self.interactions:
            # Check keywords if they exist
            keywords = item.get("keywords", {}).get(lang, [])

            matched_count = 0
            if keywords:
                for kw in keywords:
                    # Use same regex pattern as find_department for consistency
                    if lang == 'en':
                        # Strict boundary for English
                        pattern = r'\b' + re.escape(kw) + r'\b'
                    else:
                        # Relaxed right-boundary for Telugu/Hindi
                        pattern = r'(?:^|\s)' + re.escape(kw)
                    
                    if re.search(pattern, text, re.IGNORECASE):
                        matched_count += 1
                
                if matched_count >= 1:
                     return item.get("answer", {}).get(lang)

        # 2. Fuzzy Match on Question Text (Fallback for natural language)
        for item in self.interactions:
            question = item.get("question", {}).get(lang, "")
            if question:
                ratio = difflib.SequenceMatcher(None, text, question.lower()).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_answer = item.get("answer", {}).get(lang)

        # Threshold for fuzzy match
        # 0.75 is good for short sentences.
        if best_ratio > 0.75:
            return best_answer
        
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