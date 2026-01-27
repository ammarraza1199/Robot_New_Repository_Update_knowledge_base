import speech_recognition as sr
import requests
import os
import logging
import time
import hashlib
from gtts import gTTS
from dotenv import load_dotenv
import pygame
import re # Added import for regular expressions
import sys # Added for stderr suppression
import concurrent.futures # Added for parallel execution

class SuppressStderr:
    """A context manager for suppressing stderr."""
    def __enter__(self):
        self.original_stderr_fd = sys.stderr.fileno()
        self.saved_stderr_fd = os.dup(self.original_stderr_fd)
        self.devnull_fd = os.open(os.devnull, os.O_WRONLY)
        os.dup2(self.devnull_fd, self.original_stderr_fd)
        
    def __exit__(self, exc_type, exc_value, traceback):
        os.dup2(self.saved_stderr_fd, self.original_stderr_fd)
        os.close(self.devnull_fd)
        os.close(self.saved_stderr_fd)


# --- Knowledge Base from patient_guidance_doctor.py ---

# DEPARTMENT KEYWORDS
DEPARTMENT_KEYWORDS = {
    "Cardiology Unit-1": ["heart", "chest pain", "palpitation", "angina", "bp", "blood pressure", "cardiac", "heart problem", "heart issue", "high bp", "low bp", "heartbeat", "cholesterol"],
    "Cardiology Unit-2": ["irregular heartbeat", "arrhythmia", "breathlessness", "breathing problem", "breath"],
    "Cardiology Unit-3": ["coronary artery", "echo", "ecg", "ekg", "heart test"],
    "Cardiology Unit-4": ["heart attack", "myocardial infarction", "heart failure"],
    "Cardio Thoracic Surgery Unit-1": ["bypass", "valve replacement", "open heart surgery", "cabg", "pacemaker", "heart surgery"],
    "Cardio Thoracic Surgery Unit-2": ["lung surgery", "thoracic", "aortic aneurysm", "chest surgery"],
    "Medical Gastroenterology": ["stomach pain", "indigestion", "gas", "acidity", "liver", "pancreas", "ulcer", "jaundice", "stomach", "belly pain", "abdomen pain", "stomach ache", "vomiting", "loose motion", "diarrhea"],
    "Surgical Gastroenterology": ["stomach surgery", "gall bladder surgery", "hernia surgery", "appendicitis", "colon surgery", "intestine surgery", "appendix", "gallstones"],
    "Medical Genetics": ["genetic", "dna", "inherited", "chromosome", "down syndrome", "sickle cell", "hereditary", "family history", "genetic disorder", "birth defect"],
    "Pulmonary Medicine": ["lungs", "asthma", "cough", "tb", "pneumonia", "shortness of breath", "respiratory", "lung problem", "breathing", "breathing difficulty", "wheezing", "tuberculosis"],
    "Surgical Oncology": ["cancer surgery", "tumor", "breast cancer", "colon cancer", "lung cancer", "biopsy", "cancer", "tumor removal", "cancer growth"],
    "Urology": ["urine", "kidney stone", "bladder", "prostate", "urinary infection", "incontinence", "kidney", "urinary problem", "urinary", "prostate gland", "burning urine"],
    "Vascular Surgery": ["veins", "arteries", "blood clot", "varicose veins", "circulation", "diabetic foot", "blood vessel", "leg pain", "swelling in legs"],
}

# DEPARTMENT ROOMS (Original Telugu)
DEPARTMENT_ROOMS_TE = {
    "Cardiology Unit-1": "గ్రౌండ్ ఫ్లోర్, గది నం 2,4,6",
    "Cardiology Unit-2": "గ్రౌండ్ ఫ్లోర్, గది నం 3,5",
    "Cardiology Unit-3": "గ్రౌండ్ ఫ్లోర్, గది నం 3,5",
    "Cardiology Unit-4": "గ్రౌండ్ ఫ్లోర్, గది నం 2,4,6",
    "Cardio Thoracic Surgery Unit-1": "గ్రౌండ్ ఫ్లోర్, గది నం 10",
    "Cardio Thoracic Surgery Unit-2": "గ్రౌండ్ ఫ్లోర్, గది నం 10",
    "Medical Gastroenterology": "5వ అంతస్తు, గది నం 502",
    "Surgical Gastroenterology": "5వ అంతస్తు, గది నం 503",
    "Medical Genetics": "4వ అంతస్తు, గది నం 409",
    "Pulmonary Medicine": "4వ అంతస్తు, గది నం 403 మరియు 404",
    "Surgical Oncology": "4వ అంతస్తు, గది నం 410",
    "Urology": "6వ అంతస్తు, గది నం 609-611",
    "Vascular Surgery": "5వ అంతస్తు, గది నం 501",
}

# DEPARTMENT ROOMS (English)
DEPARTMENT_ROOMS_EN = {
    "Cardiology Unit-1": "Ground floor, room no 2,4,6",
    "Cardiology Unit-2": "Ground floor, room no 3,5",
    "Cardiology Unit-3": "Ground floor, room no 3,5",
    "Cardiology Unit-4": "Ground floor, room no 2,4,6",
    "Cardio Thoracic Surgery Unit-1": "Ground floor, room no 10",
    "Cardio Thoracic Surgery Unit-2": "Ground floor, room no 10",
    "Medical Gastroenterology": "5th floor, room no 502",
    "Surgical Gastroenterology": "5th floor, room no 503",
    "Medical Genetics": "4th floor, room no 409",
    "Pulmonary Medicine": "4th floor, room no 403 and 404",
    "Surgical Oncology": "4th floor, room no 410",
    "Urology": "6th floor, room no 609-611",
    "Vascular Surgery": "5th floor, room no 501",
}

# DEPARTMENT ROOMS (Hindi)
DEPARTMENT_ROOMS_HI = {
    "Cardiology Unit-1": "ग्राउंड फ्लोर, कमरा नंबर 2,4,6",
    "Cardiology Unit-2": "ग्राउंड फ्लोर, कमरा नंबर 3,5",
    "Cardiology Unit-3": "ग्राउंड फ्लोर, कमरा नंबर 3,5",
    "Cardiology Unit-4": "ग्राउंड फ्लोर, कमरा नंबर 2,4,6",
    "Cardio Thoracic Surgery Unit-1": "ग्राउंड फ्लोर, कमरा नंबर 10",
    "Cardio Thoracic Surgery Unit-2": "ग्राउंड फ्लोर, कमरा नंबर 10",
    "Medical Gastroenterology": "5वीं मंजिल, कमरा नंबर 502",
    "Surgical Gastroenterology": "5वीं मंजिल, कमरा नंबर 503",
    "Medical Genetics": "4वीं मंजिल, कमरा नंबर 409",
    "Pulmonary Medicine": "4वीं मंजिल, कमरा नंबर 403 और 404",
    "Surgical Oncology": "4वीं मंजिल, कमरा नंबर 410",
    "Urology": "6वीं मंजिल, कमरा नंबर 609-611",
    "Vascular Surgery": "5वीं मंजिल, कमरा नंबर 501",
}

# DOCTOR NAMES PER DEPARTMENT
DEPARTMENT_DOCTORS = {
    "Cardiology Unit-1": "Dr. O. Sai Satish",
    "Cardiology Unit-2": "Dr. B. Srinivas",
    "Cardiology Unit-3": "Dr. N. Rama Kumari",
    "Cardiology Unit-4": "Dr. M. Jyotsna",
    "Cardio Thoracic Surgery Unit-1": "Dr. R. V. Kumar",
    "Cardio Thoracic Surgery Unit-2": "Dr. M. Amaresh Rao",
    "Medical Gastroenterology": "Dr. Y. Satyanarayana Raju",
    "Surgical Gastroenterology": "Dr. N. Bheerappa",
    "Medical Genetics": "Dr. Prajnya Ranganath",
    "Pulmonary Medicine": "Dr. G. K. Paramjyothi",
    "Surgical Oncology": "Dr. Rajshekar Shantappa",
    "Urology": "Dr. Ch. Ram Reddy",
    "Vascular Surgery": "Dr. Sandeep Mahapatra",
}

# TELUGU DEPARTMENT NAMES
DEPARTMENT_NAMES_TELUGU = {
    "Cardiology Unit-1": "కార్డియాలజీ యూనిట్-1",
    "Cardiology Unit-2": "కార్డియాలజీ యూనిట్-2",
    "Cardiology Unit-3": "కార్డియాలజీ యూనిట్-3",
    "Cardiology Unit-4": "కార్డియాలజీ యూనిట్-4",
    "Cardio Thoracic Surgery Unit-1": "కార్డియో థోరాసిక్ సర్జరీ యూనిట్-1",
    "Cardio Thoracic Surgery Unit-2": "కార్డియో థోరాసిక్ సర్జరీ యూనిట్-2",
    "Medical Gastroenterology": "మెడికల్ గ్యాస్ట్రోఎంటరాలజీ",
    "Surgical Gastroenterology": "సర్జికల్ గ్యాస్ట్రోఎంటరాలజీ",
    "Medical Genetics": "మెడికల్ జెనెటిక్స్",
    "Pulmonary Medicine": "పల్మనరీ మెడిసిన్",
    "Surgical Oncology": "సర్జికల్ ఆంకాలజీ",
    "Urology": "యూరాలజీ",
    "Vascular Surgery": "వాస్కులర్ సర్జరీ",
}

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Determine the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_CACHE_DIR = os.path.join(SCRIPT_DIR, "audio_cache")

if not os.path.exists(AUDIO_CACHE_DIR):
    os.makedirs(AUDIO_CACHE_DIR)

class UnifiedInteractionManager:
    def __init__(self, audio_queue, motor_queue, device_index=None):
        self.audio_queue = audio_queue
        self.motor_queue = motor_queue
        
        logger.info("UnifiedInteractionManager: Initializing speech recognizer...")
        self.recognizer = sr.Recognizer()
        logger.info(f"UnifiedInteractionManager: Initializing microphone with device_index={device_index}...")
        self.microphone = sr.Microphone(device_index=device_index)
        logger.info("UnifiedInteractionManager: Microphone initialized.")
        
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        self.is_ready = bool(self.groq_api_key)
        if not self.is_ready:
            logger.error("FATAL: GROQ_API_KEY environment variable not set.")

        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.is_active = False
        
        logger.info("UnifiedInteractionManager: Initializing Pygame mixer...")
        try:
            pygame.mixer.init()
            logger.info("UnifiedInteractionManager: Pygame mixer initialized for audio playback.")
        except Exception as e:
            logger.error(f"UnifiedInteractionManager: Failed to initialize pygame mixer: {e}")

        self.SYSTEM_PROMPTS = {
            'en': "You are a helpful AI assistant for a hospital. Your primary role is to guide patients to the correct department. Do not answer any medical questions or attempt to diagnose any disease. If a user asks a medical question, you must respond by saying 'I am not qualified to answer medical questions. Please consult a doctor for diagnosis and treatment.' Answer briefly in English. Medical terms like 'hospital', 'pharmacy', 'tablets' can be in English.",
            'hi': "आप एक अस्पताल के लिए एक सहायक AI हैं। आपकी मुख्य भूमिका मरीजों को सही विभाग में मार्गदर्शन करना है। हिंग्लिश (हिंदी और अंग्रेजी का मिश्रण) में संक्षिप्त उत्तर दें। विभाग और डॉक्टरों के नाम जैसे तकनीकी शब्द अंग्रेजी में रखें। यदि कोई उपयोगकर्ता मेडिकल प्रश्न पूछता है, तो आपको यह कहकर जवाब देना होगा 'मैं चिकित्सा प्रश्नों का उत्तर देने के लिए योग्य नहीं हूं। कृपया निदान और उपचार के लिए डॉक्टर से परामर्श लें।'",
            'te': "మీరు ఆసుపత్రికి సహాయపడే AI అసిస్టెంట్. రోగులను సరైన విభాగానికి మార్గనిర్దేశం చేయడం మీ ప్రాథమిక పాత్ర. 'తెంగ్లిష్' (తెలుగు మరియు ఆంగ్ల మిశ్రమం)లో క్లుప్తంగా సమాధానం ఇవ్వండి. వినియోగదారుడు జాబితాను అడిగితే, పూర్తి జాబితాను అందించండి. విభాగం మరియు డాక్టర్ పేర్లు వంటి సాంకేతిక పదాలను ఆంగ్లంలో ఉంచండి. ఒకవేళ వినియోగదారుడు వైద్యపరమైన ప్రశ్న అడిగితే, 'నేను వైద్యపరమైన ప్రశ్నలకు సమాధానం ఇవ్వడానికి అర్హుడను కాదు. దయచేసి వ్యాధి నిర్ధారణ మరియు చికిత్స కోసం డాక్టర్‌ను సంప్రదించండి.' అని చెప్పి సమాధానం ఇవ్వాలి."
        }
        self.EXIT_COMMANDS = {
            'en': ["exit", "quit", "stop", "bye", "goodbye"],
            'hi': ["बंद", "रुको", "विदा", "अलविदा", "समाप्त", "बाई"],
            'te': ["ఆపు", "వద్దు", "బైబై", "వెళ్ళిపో"]
        }

        self.load_knowledge_base()

    def load_knowledge_base(self):
        """Loads and prepares the multilingual knowledge base."""
        logger.info("Loading department knowledge base...")
        self.department_doctors = DEPARTMENT_DOCTORS
        self.department_names_telugu = DEPARTMENT_NAMES_TELUGU
        self.department_rooms_te = DEPARTMENT_ROOMS_TE
        self.department_rooms_en = DEPARTMENT_ROOMS_EN
        self.department_rooms_hi = DEPARTMENT_ROOMS_HI

        self.multilang_keywords = {
            'en': DEPARTMENT_KEYWORDS,
            'hi': {
                "Cardiology Unit-1": ["दिल", "छाती में दर्द", "हृदय", "उच्च रक्तचाप", "निम्न रक्तचाप", "धड़कन", "कोलेस्ट्रॉल", "सीने में", "जकड़न", "घबराहट"],
                "Pulmonary Medicine": ["फेफड़े", "खांसी", "सांस", "दमा", "सांस लेने में दिक्कत", "घरघराहट", "टीबी"],
                "Urology": ["मूत्र", "गुर्दे", "किडनी", "पेशाब", "पेशाब में जलन"],
                "Medical Gastroenterology": ["पेट दर्द", "पेट", "यकृत", "लीवर", "उल्टी", "दस्त", "गैस"],
                "Surgical Oncology": ["कैंसर", "ट्यूमर", "गांठ"],
                "Vascular Surgery": ["नसों में दर्द", "पैर में सूजन"]
            },
            'te': {
                "Cardiology Unit-1": ["గుండె", "ఛాతీ నొప్పి", "రక్తపోటు", "గుండె దడ"],
                "Pulmonary Medicine": ["ఊపిరితిత్తులు", "దగ్గు", "ఆయాసం", "ఉబ్బసం", "శ్వాస తీసుకోవడంలో ఇబ్బంది", "క్షయ"],
                "Urology": ["మూత్ర", "కిడ్నీ", "మూత్రపిండాలు", "మూత్రంలో మంట", "కిడ్నీలో రాళ్లు"],
                "Medical Gastroenterology": ["కడుపు నొప్పి", "కడుపు", "కాలేయం", "వాంతులు", "విరేచనాలు", "గ్యాస్"],
                "Surgical Oncology": ["క్యాన్సర్", "కణితి", "కంతి"],
                "Vascular Surgery": ["కాళ్ళ వాపు", "రక్త ప్రసరణ"]
            }
        }
        
        logger.info("Augmenting keywords with department names...")
        # English
        for dept_name in self.multilang_keywords['en'].keys():
            self.multilang_keywords['en'][dept_name].append(dept_name.lower())
        
        # Add general English medical keywords that might not map to a specific unit but confirm the language is English
        self.english_anchors = ["i am", "i'm", "i have", "i've", "my", "this is", "can you", "please", "facing", "having", "suffering", "pain", "headache", "stomach", "fever", "doctor"]

        # For Hindi and Telugu, add the English name as a searchable keyword
        for dept_name_en in self.department_names_telugu.keys():
            if dept_name_en in self.multilang_keywords['hi']:
                 self.multilang_keywords['hi'][dept_name_en].append(dept_name_en.lower())
            if dept_name_en in self.multilang_keywords['te']:
                 self.multilang_keywords['te'][dept_name_en].append(dept_name_en.lower())
        
        # Add the specific Telugu department names to the Telugu keywords
        for dept_name_en, dept_name_te in self.department_names_telugu.items():
            if dept_name_en in self.multilang_keywords['te']:
                self.multilang_keywords['te'][dept_name_en].append(dept_name_te.lower())

        logger.info("Knowledge base loaded and augmented.")

    def speak(self, text: str, lang: str):
        if not text: return
        
        # Sanitize text to remove common markdown characters that TTS might read aloud
        clean_text = re.sub(r'[\*#\-]', '', text) # Remove asterisks, hashes, hyphens
        
        hash_object = hashlib.md5((clean_text + lang).encode()) # Use clean_text for hash
        filename = f"interaction_{hash_object.hexdigest()}.mp3"
        file_path = os.path.join(AUDIO_CACHE_DIR, filename)

        if not os.path.exists(file_path):
            logger.info(f"Generating new audio file for '{clean_text[:20]}...' in '{lang}'")
            try:
                tts = gTTS(text=clean_text, lang=lang, slow=False) # Use clean_text for TTS
                tts.save(file_path)
            except Exception as e:
                logger.error(f"gTTS failed to generate audio file: {e}")
                return
        
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except Exception as e:
            logger.error(f"Failed to play audio with pygame: {e}")

    def listen_and_recognize(self):
        with self.microphone as source:
            logger.info("Listening for user input...")
            try:
                audio = self.recognizer.listen(source, timeout=7, phrase_time_limit=15)
            except sr.WaitTimeoutError:
                logger.warning("Listening timed out. No speech detected.")
                return None, None

        logger.info("Processing speech...")
        
        # Helper to run recognition in thread
        def recognize_worker(audio_data, lang_code):
            try:
                # show_all=True returns the raw API response (dict) with confidence scores
                result = self.recognizer.recognize_google(audio_data, language=lang_code, show_all=True)
                return result
            except Exception:
                return None

        candidates = []

        # Try to recognize all three languages in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_lang = {
                executor.submit(recognize_worker, audio, lang): lang
                for lang in ['en-IN', 'hi-IN', 'te-IN']
            }
            
            for future in concurrent.futures.as_completed(future_to_lang):
                lang_full = future_to_lang[future]
                lang_simple = lang_full.split('-')[0]
                
                try:
                    data = future.result()
                    # data format: {'alternative': [{'transcript': '...', 'confidence': 0.95}, ...], 'final': True}
                    if data and isinstance(data, dict) and 'alternative' in data and len(data['alternative']) > 0:
                        best_alt = data['alternative'][0]
                        text = best_alt.get('transcript', '')
                        # If confidence is missing, default to 0.5 (it happens sometimes)
                        confidence = best_alt.get('confidence', 0.5)
                        
                        if text:
                            logger.info(f"Recognized as {lang_full}: '{text}' (Confidence: {confidence})")
                            candidates.append({
                                'lang': lang_simple,
                                'text': text.lower(),
                                'confidence': confidence
                            })
                except Exception as e:
                    logger.error(f"Error processing {lang_full} result: {e}")

        if not candidates:
            logger.warning("No recognition in any language.")
            return None, None

        # --- SMART SELECTION LOGIC ---
        # Adjust scores based on keyword matching AND sentence length
        for cand in candidates:
            cand['score'] = cand['confidence']
            text = cand['text']
            lang = cand['lang']
            
            # 1. Keyword Bonus
            found_keyword = False
            if lang in self.multilang_keywords:
                for dept, keywords in self.multilang_keywords[lang].items():
                    for keyword in keywords:
                        if keyword in text:
                            found_keyword = True
                            break
                    if found_keyword: break
            
            if found_keyword:
                cand['score'] += 0.6 # Increased boost for relevant keywords
                logger.info(f"Keyword matched in '{lang}'. Boost +0.6")

            # 2. Length Bonus: Penalize very short fragments, reward longer sentences
            # Shorter fragments (< 4 words) often occur in wrong languages simply due to phonetic matching.
            # We add 0.05 per word.
            word_count = len(text.split())
            length_bonus = word_count * 0.05
            cand['score'] += length_bonus
            logger.info(f"Length bonus for '{lang}' ({word_count} words): +{length_bonus:.2f}")

            # 3. English Anchor Bonus
            # If the language is English and contains common sentence starters, it's almost certainly English.
            if lang == 'en':
                for anchor in self.english_anchors:
                    # Check for exact word matches or phrase availability
                    if f" {anchor} " in f" {text} " or text.startswith(anchor):
                        cand['score'] += 0.5
                        logger.info(f"English Anchor '{anchor}' found. Huge boost +0.5")
                        break

        # Sort candidates by adjusted score (descending)
        candidates.sort(key=lambda x: x['score'], reverse=True)
        
        best_match = candidates[0]
        logger.info(f"Final decision: Selected '{best_match['lang']}' with adjusted score {best_match['score']}")
        
        return best_match['text'], best_match['lang']




    def get_department_guidance(self, user_text, lang):
        if lang not in self.multilang_keywords or not user_text:
            return None
            
        for dept, keywords in self.multilang_keywords[lang].items():
            for keyword in keywords:
                if keyword in user_text:
                    logger.info(f"Keyword match found: '{keyword}' -> {dept}")
                    return self._format_guidance_response(dept, lang)
        return None

    def _format_guidance_response(self, dept, lang):
        doctor = self.department_doctors.get(dept, "details not available")
        
        if lang == 'te':
            dept_name = self.department_names_telugu.get(dept, dept)
            room_info = self.department_rooms_te.get(dept, "గది వివరాలు అందుబాటులో లేవు")
            # Applying new template for Telugu
            return f"సరే, మీకు వ్యాధిని పరిష్కరించడానికి కొంత సమస్య ఉంది, మీరు {dept_name} విభాగానికి వెళ్లవచ్చు. విభాగం యొక్క స్థానం {room_info}. అక్కడ మీరు డాక్టర్ {doctor}ను కనుగొంటారు, అతను మీ తనిఖీ చేస్తారు."

        if lang == 'hi':
            room_info = self.department_rooms_hi.get(dept, "कमरे की जानकारी उपलब्ध नहीं है")
            # Applying new template for Hindi
            return f"ठीक है, आपको बीमारी के समाधान के लिए कुछ समस्या है, आप {dept} विभाग जा सकते हैं। विभाग का स्थान {room_info} है और वहां आपको डॉक्टर {doctor} मिलेंगे जो आपकी जांच करेंगे।"

        # Default to English
        room_info = self.department_rooms_en.get(dept, "Room details are not available")
        return f"Okay, you have some problem. To resolve the issue, you can go to the {dept} department. The location of the department is {room_info}, and you will find Doctor {doctor} over there who will do your checkup."

    def query_llama(self, user_text: str, lang: str):
        if lang not in self.SYSTEM_PROMPTS: lang = 'en'
        
        # --- Build the context string ---
        logger.info("Building context-rich prompt for LLM...")
        context = "\n\nHere is the complete list of hospital departments, their locations, and doctors. Use this information to answer the user's question.\n\n"
        if lang == 'hi':
            context = "\n\nअस्पताल के विभागों, उनके स्थानों और डॉक्टरों की पूरी सूची यहाँ दी गई है। उपयोगकर्ता के प्रश्न का उत्तर देने के लिए इस जानकारी का उपयोग करें।\n\n"
        elif lang == 'te':
            context = "\n\nహాస్పిటల్ విభాగాలు, వాటి స్థానాలు మరియు డాక్టర్ల పూర్తి జాబితా ఇక్కడ ఉంది. వినియోగదారుడి ప్రశ్నకు సమాధానం ఇవ్వడానికి ఈ సమాచారాన్ని ఉపయోగించండి.\n\n"

        for dept_en, doc in self.department_doctors.items():
            loc_en = self.department_rooms_en.get(dept_en, "Not available")
            loc_hi = self.department_rooms_hi.get(dept_en, "उपलब्ध नहीं है")
            loc_te = self.department_rooms_te.get(dept_en, "అందుబాటులో లేదు")
            dept_te = self.department_names_telugu.get(dept_en, dept_en)

            if lang == 'hi':
                context += f"- विभाग: {dept_en}, डॉक्टर: {doc}, स्थान: {loc_hi}\n"
            elif lang == 'te':
                context += f"- విభాగం: {dept_te}, డాక్టర్: {doc}, స్థానం: {loc_te}\n"
            else: # English
                context += f"- Department: {dept_en}, Doctor: {doc}, Location: {loc_en}\n"
        
        # Combine base prompt with the new context
        system_prompt = self.SYSTEM_PROMPTS[lang] + context
        
        headers = {"Authorization": f"Bearer {self.groq_api_key}", "Content-Type": "application/json"}
        payload = {"model": "llama-3.1-8b-instant", "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_text}], "temperature": 0.7, "max_tokens": 200}

        logger.info(f"Querying LLM with payload: {payload}")

        try:
            response = requests.post(self.groq_url, headers=headers, json=payload, timeout=20)
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            
            data = response.json()
            llm_response = data["choices"][0]["message"]["content"].strip()
            logger.info(f"LLM Response: '{llm_response}'")
            return llm_response
        except requests.exceptions.RequestException as e:
            error_message = f"Groq API request failed: {e}"
            # Check if the exception has a response object and log it for more detail
            if hasattr(e, 'response') and e.response is not None:
                error_message += f"\nStatus Code: {e.response.status_code}\nResponse Body: {e.response.text}"
            logger.error(error_message)
            
            if lang == 'hi':
                return "मुझे कनेक्ट करने में समस्या आ रही है।"
            elif lang == 'te':
                return "కనెక్ట్ చేయడంలో నాకు సమస్య ఉంది."
            else:
                return "Sorry, I'm having trouble connecting."

    def is_medical_query(self, text):
        # Multilingual medical keywords
        medical_keywords = [
            # English
            "what is", "define", "symptoms of", "causes of", "treatment for", "how to cure", "remedy for", "diagnose",
            "medicine for", "tablet for", "pain in", "suffering from",
            # Hindi
            "kya hai", "lakshan", "karan", "ilaaj", "upchar", "dawa", "goli", "dard", "bimari", "thik kaise",
            # Telugu
            "emi", "lakshanalu", "karanam", "mandhu", "tablet", "noppi", "taggatle", "treatment", "nivarana"
        ]
        text = text.lower()
        for keyword in medical_keywords:
            if keyword in text:
                return True
        return False

    def start_sequence(self):
        """
        Speaks welcome messages and then calibrates the microphone.
        """
        # --- Welcome Messages ---
        logger.info("start_sequence: Speaking English welcome message...")
        self.speak("Hello, how can I help you?", "en")
        logger.info("start_sequence: English welcome message spoken.")
        
        logger.info("start_sequence: Speaking Telugu welcome message...")
        self.speak("మీకు ఎలా సహాయపడగలను?", "te") # Added Telugu welcome
        logger.info("start_sequence: Telugu welcome message spoken.")

        # --- Manually set energy threshold instead of calibrating ---
        # This is a temporary workaround to bypass the hanging adjust_for_ambient_noise() call
        self.recognizer.energy_threshold = 4000 
        logger.info(f"start_sequence: Microphone energy threshold manually set to {self.recognizer.energy_threshold}.")

    def run_one_cycle(self):
        if not self.is_ready:
            logger.error("InteractionManager is not ready (missing API key).")
            time.sleep(10)
            return

        if self.motor_queue:
            self.motor_queue.put("turn_to:0")
        
        command, lang = self.listen_and_recognize()

        if not command or not lang:
            self.speak("Sorry, I didn't catch that. Please can you ask your question once again?", "en")
            return
        
        # --- Log user input ---
        logger.info(f"\n\n--- User Input Detected ---\n  Text: '{command}'\n  Language: '{lang}'\n---------------------------\n")

        response_text = None
        is_exit = any(cmd in command.lower().split() for cmd in self.EXIT_COMMANDS.get(lang, []))
        
        if is_exit:
            logger.info("Exit command received. Shutting down interaction loop.")
            goodbye_map = {'en': "Goodbye!", 'hi': "अलविदा!", 'te': "వెళ్ళొస్తాను!"}
            response_text = goodbye_map.get(lang, "Goodbye!")
            self.is_active = False # Set flag to stop the loop
        else:
            response_text = self.get_department_guidance(command, lang)
            
            if response_text is None:
                if self.is_medical_query(command):
                    department_guidance = self.get_department_guidance(command, lang)
                    if department_guidance:
                        response_text = department_guidance
                    else:
                        if lang == 'hi':
                            response_text = "मैं मेडिकल सलाह नहीं दे सकता। कृपया डॉक्टर से सलाह लें।"
                        elif lang == 'te':
                            response_text = "నేను వైద్య సలహా ఇవ్వలేను. దయచేసి డాక్టర్‌ను సంప్రదించండి."
                        else:
                            response_text = "I cannot provide medical advice. Please consult a doctor."
                else:
                    response_text = self.query_llama(command, lang)

        if response_text:
            # --- Log system output ---
            logger.info(f"\n--- System Response ---\n  Text: '{response_text}'\n  Language: '{lang}'\n-----------------------\n")
            self.speak(response_text, lang)
        
        time.sleep(2.0)


def unified_interaction_process(audio_queue, motor_queue):
    logger.info("Unified interaction process started.")
    try:
        manager = UnifiedInteractionManager(audio_queue, motor_queue, device_index=None)
        manager.is_active = True
        
        manager.speak("Hello, how can I help you?", "en")
        
        while manager.is_active:
            manager.run_one_cycle()

    except KeyboardInterrupt:
        logger.info("Unified interaction process interrupted by user.")
    except Exception as e:
        logger.error(f"Fatal error in unified_interaction_process: {e}", exc_info=True)
    finally:
        logger.info("Unified interaction process stopped.")

if __name__ == "__main__":
    logger.info("Unified interaction process started for standalone demo.")
    try:
        # Pass None for queues and device_index=None for the default microphone
        manager = UnifiedInteractionManager(audio_queue=None, motor_queue=None, device_index=None)
        manager.is_active = True
        
        # Run the startup sequence (welcome messages and calibration)
        manager.start_sequence()
        
        logger.info("********************************************************")
        logger.info("Startup complete. The robot is now listening.")
        logger.info("********************************************************")
        
        while manager.is_active:
            manager.run_one_cycle()

    except KeyboardInterrupt:
        logger.info("Unified interaction process interrupted by user.")
    except Exception as e:
        logger.error(f"Fatal error in standalone execution: {e}", exc_info=True)
    finally:
        logger.info("Unified interaction process stopped.")
