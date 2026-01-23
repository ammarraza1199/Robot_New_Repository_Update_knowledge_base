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
import multiprocessing
import random
import numpy as np
from collections import deque
from logging_config import setup_logging
import json # Added for JSON loading

# --- Full Multilingual Knowledge Base (with expanded keywords) ---
# Removed hardcoded DEPARTMENT_KEYWORDS, DEPARTMENT_ROOMS_TE/EN/HI,
# DEPARTMENT_DOCTORS, DEPARTMENT_NAMES_TELUGU

load_dotenv()
logger = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_CACHE_DIR = os.path.join(SCRIPT_DIR, "audio_cache")
CONVERSATION_LOG_FILE = os.path.join(SCRIPT_DIR, "conversations.csv")
KB_PATH = os.path.join(SCRIPT_DIR, "hospital_knowledge_base.json") # New KB path

if not os.path.exists(AUDIO_CACHE_DIR):
    os.makedirs(AUDIO_CACHE_DIR)

class InteractionProcess:
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
        
        logger.info("Initializing speech recognizer...")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=device_index, sample_rate=48000, chunk_size=1024)
        
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
        
        time.sleep(1)
        self.motor_queue.put("turn_to:0")

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
