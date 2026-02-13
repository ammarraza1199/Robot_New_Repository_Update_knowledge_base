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
import difflib
import multiprocessing
import random
import numpy as np
from collections import deque
from logging_config import setup_logging
import json # Added for JSON loading
import pyaudio # Add this

# --- Full Multilingual Knowledge Base (with expanded keywords) ---
# Removed hardcoded DEPARTMENT_KEYWORDS, DEPARTMENT_ROOMS_TE/EN/HI,
# DEPARTMENT_DOCTORS, DEPARTMENT_NAMES_TELUGU

load_dotenv()
logger = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_CACHE_DIR = os.path.join(SCRIPT_DIR, "audio_cache")
CONVERSATION_LOG_FILE = os.path.join(SCRIPT_DIR, "logs", "conversations.csv")
KB_PATH = os.path.join(SCRIPT_DIR, '..', 'data', "hospital_knowledge_base.json") # Optimized KB v4.1.1

if not os.path.exists(AUDIO_CACHE_DIR):
    os.makedirs(AUDIO_CACHE_DIR)

class InteractionProcess:
    REDIRECT_DEPARTMENTS = {
        "ophthalmology": "general_medicine",
        "eye": "general_medicine",
        "ent": "general_medicine"
    }
    def __init__(self, audio_queue, motor_queue, shutdown_flag, audio_playing_flag, audio_feedback_queue, device_index=None):
        self.audio_queue = audio_queue
        self.motor_queue = motor_queue
        self.shutdown_flag = shutdown_flag
        self.audio_playing_flag = audio_playing_flag
        self.audio_feedback_queue = audio_feedback_queue
        
        self.speech_cooldown_period = 1.5  # Cooldown in seconds
        self.last_speech_time = 0

        logger.info("Initializing speech recognizer...")
        self.recognizer = sr.Recognizer()
        # The device lock is resolved. Reverting to auto-detection for all parameters,
        # which should now succeed on the available device.
        self.microphone = sr.Microphone(device_index=device_index)
        
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        if not self.groq_api_key:
            logger.error("FATAL: GROQ_API_KEY environment variable not set.")
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        
        self.recognizer.energy_threshold = 1000
        self.recognizer.dynamic_energy_threshold = True
        self.SUDDEN_SOUND_THRESHOLD_MULTIPLIER = 2.5
        self.SUDDEN_SOUND_COOLDOWN = 10
        self.last_sudden_sound_time = 0
        self.last_unrecognized_speech_time = 0
        self.UNRECOGNIZED_SPEECH_COOLDOWN = 10

        self.load_knowledge_base()
        self.initialize_conversation_log()

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
        self.SYSTEM_PROMPTS = {
            'en': "You are a hospital navigation assistant. Your ONLY job is to match user-reported symptoms to the most relevant department from the provided list. Respond ONLY with the department information in the requested format. Do not diagnose, offer advice, or have any other conversation.",
            'hi': "आप एक अस्पताल नेविगेशन सहायक हैं। आपका एकमात्र काम उपयोगकर्ता द्वारा बताए गए लक्षणों को प्रदान की गई सूची से सबसे प्रासंगिक विभाग से मिलाना है। केवल अनुरोधित प्रारूप में विभाग की जानकारी के साथ प्रतिक्रिया दें। निदान, सलाह या कोई अन्य बातचीत न करें।",
            'te': "మీరు హాస్పిటల్ నావిగేషన్ అసిస్టెంట్. వినియోగదారు నివేదించిన లక్షణాలను అందించిన జాబితా నుండి అత్యంత సంబంధిత విభాగానికి సరిపోల్చడం మాత్రమే మీ పని. అభ్యర్థించిన ఫార్మాట్‌లో మాత్రమే విభాగం సమాచారంతో ప్రతిస్పందించండి. నిర్ధారణ, సలహా లేదా మరే ఇతర సంభాషణ చేయవద్దు."
        }


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
        try:
            with open(KB_PATH, "r", encoding="utf-8") as f:
                kb = json.load(f)

            self.departments = kb.get("departments", [])
            self.interactions = kb.get("interactions", [])
            self.keyword_index = {"en": {}, "hi": {}, "te": {}}
            self.department_map = {} # This will store the full department objects
            self.faqs = []

            # Process both lists for FAQs and Departments
            all_items = self.departments + self.interactions
            for item in all_items:
                # Check if it's a real department or an FAQ/Interaction
                if "canonical_name" in item:
                    cname = item["canonical_name"]
                    self.department_map[cname] = item
                    for lang, kws in item.get("keywords", {}).items():
                        for kw in kws:
                            self.keyword_index[lang][kw.lower()] = cname
                elif "question" in item and "answer" in item:
                    # This is an FAQ/Interaction block
                    self.faqs.append(item)
                elif "keywords" in item and "answer" in item:
                    # Support for keyword-only FAQs
                    self.faqs.append(item)
            
            logger.info(f"Knowledge base loaded: {len(self.department_map)} departments, {len(self.faqs)} FAQs.")

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

        clean_text = re.sub(r'[\*#\-]', '', text)
        hash_object = hashlib.md5((clean_text + lang).encode())
        audio_filename = f"interaction_{hash_object.hexdigest()}.mp3"
        file_path = os.path.join(AUDIO_CACHE_DIR, audio_filename)
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
        self.audio_playing_flag.set()
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

        # New cooldown logic to prevent hearing its own speech
        current_time = time.time()
        if (current_time - self.last_speech_time) < self.speech_cooldown_period:
            logger.debug("BACKGROUND_CALLBACK: Skipping microphone input due to post-speech cooldown.")
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
                        logger.error(f"Recognition error for {lang}-IN: {e}", exc_info=True)

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
        
        # Robust Exit Check: Check ALL languages, not just the detected one
        is_exit = False
        for lang_code, phrases in self.EXIT_COMMANDS.items():
            if any(cmd in command for cmd in phrases):
                is_exit = True
                logger.info(f"Exit command detected (matched '{lang_code}'). Shutting down.")
                break
                
        if is_exit:
            response_text = "Goodbye!"
            self.shutdown_flag.set()
        else:
            # 1. PRIORITY: Medical Safety Check
            if self.is_medical_query(command):
                response_text = "I cannot provide medical advice. Please consult a doctor."
            else:
                # 2. Match Departments or FAQs
                matched_dept = self.find_department(command, lang)
                faq_answer = self.find_faq(command, lang)
                
                if matched_dept:
                    response_text = self._format_guidance_response(matched_dept, lang)
                elif faq_answer:
                    response_text = faq_answer
                else:
                    llm_response = self.query_llama(command, lang)
                    if llm_response:
                        response_text = llm_response
                    else: # Fallback if no department, not medical query, AND LLM gave no specific answer
                        if lang == "hi":
                            response_text = "जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद है। कृपया उत्तर के लिए पास के अस्पताल के कर्मचारियों से पूछें। धन्यवाद।"
                        elif lang == "te":
                            response_text = "సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాను. దయచేసి సమాధానం కోసం దగ్గర్లోని ఆసుపత్రి సిబ్బందిని అడగండి. ధన్యవాదాలు."
                        else: # Default to English
                            response_text = "The information is not with me. I am sorry for your inconvenience. Please ask the nearby hospital staff for the answer. Thank you."
        
        if response_text:
            logger.info(f"--- FINAL AUDIO OUTPUT --- Language: {lang} | Text: '{response_text}'")
            self.log_conversation(command, response_text, lang)
            self.queue_audio(response_text, lang, interrupt=True)
        
        time.sleep(1)
        self.motor_queue.put("turn_to:0")

    def find_department(self, user_text, lang):
        """
        Identifies if the user is asking for a specific department or describing symptoms relevant to one.
        Uses exact keyword matching, regex patterns, and fuzzy logic.
        Implements Cross-Lingual Fallback: If not found in 'lang', checks 'en', 'hi', 'te'.
        """
        user_text = user_text.lower()
        
        # 1. Search in Requested Language
        dept = self._search_dept_in_lang(user_text, lang)
        if dept:
            logger.info(f"--- DEPT MATCH ({lang}) --- -> {dept}")
            return dept
            
        # 2. Fallback: Search in other languages
        other_langs = [l for l in ['en', 'hi', 'te'] if l != lang]
        for fallback_lang in other_langs:
            dept = self._search_dept_in_lang(user_text, fallback_lang)
            if dept:
                logger.warning(f"--- DEPT MATCH (Fallback: {fallback_lang}) --- User sent '{lang}' but matched '{fallback_lang}' -> {dept}")
                return dept
        
        logger.debug("No department keyword match found (Exact or Fuzzy) in any language.")
        return None

    def _search_dept_in_lang(self, user_text, lang):
        """Helper to search for department in a specific language."""
        if lang not in self.keyword_index:
            return None
        
        # --- Exact/Regex Match ---
        best_match_dept = None
        longest_match_len = 0
        matched_kw_log = ""

        for kw, dept_cname in self.keyword_index[lang].items():
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, user_text, re.IGNORECASE):
                if len(kw) > longest_match_len:
                    longest_match_len = len(kw)
                    best_match_dept = dept_cname
                    matched_kw_log = kw

        # --- COMBINATION KEYWORDS (English Only) ---
        if not best_match_dept and lang == 'en':
            COMBINATION_KEYWORDS = {
                "Vascular Surgery": [("foot", "wound"), ("leg", "wound"), ("foot", "healing"), ("leg", "healing")],
            }
            for dept, combos in COMBINATION_KEYWORDS.items():
                for combo in combos:
                    if all(re.search(r'\b' + re.escape(word) + r'\b', user_text, re.IGNORECASE) for word in combo):
                         return dept

        if best_match_dept:
            dept_cname_lower = best_match_dept.lower()
            if dept_cname_lower in self.REDIRECT_DEPARTMENTS:
                return self.REDIRECT_DEPARTMENTS[dept_cname_lower]
            return best_match_dept

        # --- Fuzzy Match ---
        user_words = user_text.split()
        best_fuzzy_dept = None
        best_ratio = 0.0

        for kw, dept_cname in self.keyword_index[lang].items():
            kw_lower = kw.lower()
            for user_word in user_words:
                if len(user_word) < 4: continue
                
                # Substring
                if len(kw_lower) > 4 and (user_word in kw_lower or kw_lower in user_word):
                     if len(user_word) / len(kw_lower) > 0.5:
                         return dept_cname

                # Ratio
                ratio = difflib.SequenceMatcher(None, user_word, kw_lower).ratio()
                if ratio > 0.65 and ratio > best_ratio:
                    best_ratio = ratio
                    best_fuzzy_dept = dept_cname
        
        return best_fuzzy_dept

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
        """
        Detects if the user is asking for medical advice, symptoms, or prescriptions.
        Prioritizes safety by blocking these queries.
        """
        medical_keywords = [
            # English - Verbs and nouns
            "what is", "symptoms of", "causes of", "treatment for", "diagnose", "medicine for", "pain in", "cure for", "heal",
            "tablet", "pills", "pill", "medicine", "medication", "dose", "dosage", "prescription", "prescribe", "prescribing",
            "paracetamol", "antibiotic", "ointment", "cream", "injection", "syrup", "capsule",
            "how to take", "when to take", "side effects", "dosage for",
            # Hindi
            "kya hai", "lakshan", "ilaaj", "upchar", "chikitsa", "dawa", "dard", "taklif", "bimari", "rog",
            "dawai", "goli", "parchi", "khana hai", "lagana hai", "dawaein",
            # Telugu - Phonetic and Script
            "noppi", "mandhu", "nivarana", "samasya", "baadha", "rogam", "jabbulu", "chikitsa", "mandulu",
            "నొప్పి", "మందు", "నివారణ", "సమస్య", "బాధ", "రోగం", "జబ్బులు", "చికిత్స",
            "మాత్రలు", "మాత్ర", "ట్యాబ్లెట్", "టాబ్లెట్", "మందులు", "ప్రిస్క్రిప్షన్", "మింగాలి", "వేసుకోవాలి"
        ]
        
        text_lower = text.lower().strip()
        
        # Check substrings for safety
        for keyword in medical_keywords:
            kw_low = keyword.lower()
            if kw_low in text_lower:
                logger.warning(f"--- MEDICAL SAFETY TRIGGER --- Found keyword '{kw_low}' in input '{text_lower}'")
                return True
        
        # Word boundary check for English (prevents matching "painter" for "pain")
        en_keywords = ["pain", "pill", "dose", "cure"]
        for kw in en_keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                logger.warning(f"--- MEDICAL SAFETY TRIGGER (Regex) --- Found keyword '{kw}'")
                return True

        return False

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


    def find_faq(self, user_text, lang):
        """
        Searches for FAQs using both keyword matching and fuzzy matching on the question text.
        Implements Cross-Lingual Fallback.
        """
        if not hasattr(self, 'faqs') or not self.faqs:
            return None

        user_text_lower = user_text.lower()
        FAQ_THRESHOLD = 0.7 
        
        # Helper to search in a specific language
        def search_in_lang(target_lang):
            best_ans = None
            best_r = 0.0
            
            for faq in self.faqs:
                # 1. Keyword check (High Priority)
                if "keywords" in faq and target_lang in faq["keywords"]:
                    for kw in faq["keywords"][target_lang]:
                        if kw.lower() in user_text_lower:
                            # Higher priority than fuzzy match
                            return faq["answer"].get(target_lang), 0.95 

                # 2. Question fuzzy match
                if "question" in faq and target_lang in faq["question"]:
                    q_text = faq["question"][target_lang].lower()
                    
                    # Direct check or Substring
                    if user_text_lower in q_text or q_text in user_text_lower:
                        r = difflib.SequenceMatcher(None, user_text_lower, q_text).ratio()
                        if len(user_text_lower) < 5: 
                            if user_text_lower == q_text:
                                return faq["answer"].get(target_lang), 1.0
                        elif r > 0.5:
                            if r > best_r:
                                best_r = r
                                best_ans = faq["answer"].get(target_lang)
                    
                    # Fuzzy match
                    r = difflib.SequenceMatcher(None, user_text_lower, q_text).ratio()
                    if r > FAQ_THRESHOLD and r > best_r:
                        best_r = r
                        best_ans = faq["answer"].get(target_lang)
            return best_ans, best_r

        # 1. Try Requested Language
        answer, score = search_in_lang(lang)
        if answer:
            try:
                with open("debug_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"MATCH: '{user_text}' -> Answer: '{str(answer)[:50]}...' (Score: {score})\n")
            except:
                pass
            logger.info(f"--- FAQ MATCH ({lang}) --- Score: {score:.2f}")
            return answer
        
        # 2. Fallback: Try other languages
        other_langs = [l for l in ['en', 'hi', 'te'] if l != lang]
        for fallback_lang in other_langs:
            answer, score = search_in_lang(fallback_lang)
            if answer:
                logger.warning(f"--- FAQ MATCH (Fallback: {fallback_lang}) --- Score: {score:.2f}")
                # We return the answer in the MATCHED language if the original requested one is missing
                # But ideally we want it in the 'lang' if possible.
                return answer.get(lang, list(answer.values())[0]) if isinstance(answer, dict) else answer
                
        return None

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
            self.recognizer.adjust_for_ambient_noise(source, duration=3.0)
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
            try:
                feedback = self.audio_feedback_queue.get_nowait()
                if feedback.get('status') == 'finished':
                    self.audio_playing_flag.clear()
                    self.last_speech_time = time.time()  # Record the time speech finished
                    logger.info(f"Audio finished playing: {feedback.get('file')}. Flag cleared, cooldown started.")
            except multiprocessing.queues.Empty:
                pass  # No feedback, continue
            except Exception as e:
                logger.error(f"Error processing audio feedback queue: {e}", exc_info=True)

            time.sleep(0.1)  # Shorter sleep to be more responsive

        logger.info("Shutting down Interaction Process...")
        stop_listening(wait_for_stop=False)
        logger.info("Background listener stopped.")

def interaction_process_func(audio_queue, motor_queue, shutdown_flag, audio_playing_flag, audio_feedback_queue, mic_name="miniDSP"):
    setup_logging()
    logger = logging.getLogger(__name__)

    p = None # Initialize p to None
    device_index = None
    target_mic_index = None
    first_input_mic_index = None
    
    try:
        try:
            logger.info("Attempting to initialize PyAudio.")
            p = pyaudio.PyAudio() # Initialize PyAudio
        except Exception as py_audio_e:
            logger.critical(f"CRITICAL ERROR: Failed to initialize PyAudio. This often means there's an issue with your system's audio backend (e.g., JACK server not running, ALSA misconfiguration). Exception: {py_audio_e}", exc_info=True)
            # If PyAudio fails to initialize, no devices can be found. device_index will remain None.
            return # Exit function early, as we can't proceed without PyAudio.
            
        logger.info("Starting PyAudio device enumeration.")
        logger.info("Searching for available microphones...")
        num_devices = p.get_device_count()
        logger.info(f"PyAudio detected {num_devices} audio devices.") # New log line
        
        for i in range(num_devices):
            device_info = p.get_device_info_by_index(i)
            device_name = device_info.get('name', 'Unknown')
            
            logger.debug(f"Device {i}: '{device_name}' (Max Input Channels: {device_info.get('maxInputChannels')}, Max Output Channels: {device_info.get('maxOutputChannels')})") # Added Max Output Channels for more info

            if device_info.get('maxInputChannels') > 0: # Check if it's an input device
                logger.info(f"Input Device Found: Index {i}, Name: '{device_name}', Max Input Channels: {device_info.get('maxInputChannels')}") # New log for input devices
                if first_input_mic_index is None:
                    first_input_mic_index = i # Store the first input device found
                    
                if mic_name.lower() in device_name.lower():
                    target_mic_index = i
                    logger.info(f"SUCCESS: Found target microphone '{mic_name}' at index {i}.")
                    # Do NOT break here, continue iterating to ensure all devices are logged for debugging
        
        if target_mic_index is not None:
            device_index = target_mic_index
        elif first_input_mic_index is not None:
            device_index = first_input_mic_index
            first_mic_info = p.get_device_info_by_index(first_input_mic_index)
            logger.warning(f"WARNING: Target microphone '{mic_name}' not found. Falling back to first available input microphone at index {first_input_mic_index}: '{first_mic_info.get('name', 'Unknown')}'.")
        else:
            logger.critical("No input microphones found on the system. Cannot proceed with speech recognition.")
            # device_index remains None here
            # We still pass device_index=None to InteractionProcess, which will lead to the original OSError.
            # This is correct if no input device is truly available.

    except Exception as e:
        logger.error(f"ERROR: Exception caught during microphone detection: {e}", exc_info=True) # New log
        device_index = None # Reset to None if error occurs during detection


    finally:
        p.terminate() # Terminate PyAudio instance

    logger.info(f"Final chosen device_index for sr.Microphone: {device_index}") # New log

    interaction_system = InteractionProcess(audio_queue, motor_queue, shutdown_flag, audio_playing_flag, audio_feedback_queue, device_index=device_index)
    interaction_system.start()
