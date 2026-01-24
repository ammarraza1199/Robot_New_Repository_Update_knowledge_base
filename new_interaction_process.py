import speech_recognition as sr
import requests
import os
import logging
import time
import hashlib
from gtts import gTTS
from dotenv import load_dotenv
import re
import concurrent.futures
import random
import numpy as np
import json

# -------------------- ENV & LOGGING --------------------

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("InteractionProcess")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_CACHE_DIR = os.path.join(SCRIPT_DIR, "audio_cache")
os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)

# -------------------- MAIN CLASS --------------------

class InteractionProcess:
    def __init__(self, audio_queue, motor_queue, shutdown_flag, audio_playing_flag, device_index=None):
        self.audio_queue = audio_queue
        self.motor_queue = motor_queue
        self.shutdown_flag = shutdown_flag
        self.audio_playing_flag = audio_playing_flag

        # Speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(
            device_index=device_index,
            sample_rate=48000,
            chunk_size=1024
        )

        # LLM config
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"

        # Audio thresholds
        self.recognizer.energy_threshold = 1000
        self.recognizer.dynamic_energy_threshold = True
        self.SUDDEN_SOUND_THRESHOLD_MULTIPLIER = 2.5
        self.SUDDEN_SOUND_COOLDOWN = 10
        self.last_sudden_sound_time = 0
        self.last_unrecognized_speech_time = 0
        self.UNRECOGNIZED_SPEECH_COOLDOWN = 10

        # Load KB
        self.load_knowledge_base()

        # -------------------- IMPROVED LANGUAGE ANCHORS --------------------

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

        # -------------------- SAFE EXIT COMMANDS --------------------

        self.EXIT_COMMANDS = {
            "en": [
                "exit now", "quit application", "stop interaction",
                "end conversation", "bye bye", "thank you goodbye"
            ],
            "hi": [
                "बात खत्म", "बंद करो", "अब नहीं", "धन्यवाद अलविदा"
            ],
            "te": [
                "సరే చాలు", "ఆపండి", "ఇంకా వద్దు", "ధన్యవాదాలు"
            ]
        }

    # -------------------- KNOWLEDGE BASE --------------------

    def load_knowledge_base(self):
        kb_path = os.path.join(SCRIPT_DIR, "hospital_knowledge_base.json")
        with open(kb_path, "r", encoding="utf-8") as f:
            kb = json.load(f)

        self.departments = kb["departments"]
        self.keyword_index = {"en": {}, "hi": {}, "te": {}}
        self.department_map = {}

        for dept in self.departments:
            cname = dept["canonical_name"]
            self.department_map[cname] = dept
            for lang, kws in dept["keywords"].items():
                for kw in kws:
                    self.keyword_index[lang][kw.lower()] = cname

        logger.info("Knowledge base loaded successfully.")

    # -------------------- AUDIO OUTPUT --------------------

    def queue_audio(self, text, lang, interrupt=True):
        if not text:
            return

        if interrupt:
            self.audio_queue.put({'command': 'stop'})
            time.sleep(0.1)

        clean_text = re.sub(r'[\*#\-]', '', text)
        audio_hash = hashlib.md5((clean_text + lang).encode()).hexdigest()
        file_path = os.path.join(AUDIO_CACHE_DIR, f"{audio_hash}.mp3")

        if not os.path.exists(file_path):
            gTTS(text=clean_text, lang=lang).save(file_path)

        self.audio_queue.put({
            'command': 'play',
            'file': os.path.basename(file_path)
        })

    # -------------------- UTILS --------------------

    def _calculate_db(self, audio_data):
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        if len(audio_array) == 0:
            return 0
        rms = np.sqrt(np.mean(audio_array.astype(np.float64) ** 2))
        return 20 * np.log10(rms + 1e-9)

    # -------------------- CORE LOGIC --------------------

    def find_department(self, text, lang):
        text = text.lower()
        for kw, dept in self.keyword_index.get(lang, {}).items():
            if kw in text:
                logger.info(f"Matched keyword '{kw}' → {dept}")
                return dept
        return None

    def _format_guidance_response(self, dept_name, lang):
        dept = self.department_map.get(dept_name)
        if not dept:
            return None

        name = dept["display_name"].get(lang, dept_name)
        loc = dept["location"].get(lang, "N/A")
        doc = dept["doctors"][0]["name"] if dept.get("doctors") else "Available doctor"

        if lang == "te":
            return f"విభాగం {name}. డాక్టర్ {doc}. చిరునామా {loc}."
        elif lang == "hi":
            return f"विभाग {name}. डॉक्टर {doc}. पता {loc}."
        else:
            return f"The department is {name}. Doctor is {doc}. Location is {loc}."

    def process_command(self, text, lang):
        self.motor_queue.put(f"turn_to:{random.randint(-45, 45)}")

        if any(cmd in text for cmd in self.EXIT_COMMANDS.get(lang, [])):
            self.queue_audio("Goodbye!", lang)
            self.shutdown_flag.set()
            return

        dept = self.find_department(text, lang)
        if dept:
            response = self._format_guidance_response(dept, lang)
            if response:
                self.queue_audio(response, lang)

        time.sleep(1)
        self.motor_queue.put("turn_to:0")

    # -------------------- BACKGROUND LISTENER --------------------

    def _background_callback(self, recognizer, audio):
        if self.audio_playing_flag.is_set():
            return

        candidates = []
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(
                        recognizer.recognize_google,
                        audio,
                        language=f"{lang}-IN"
                    ): lang
                    for lang in ["en", "hi", "te"]
                }

                for future in concurrent.futures.as_completed(futures):
                    lang = futures[future]
                    try:
                        text = future.result().lower()
                        anchors = {
                            "en": self.english_anchors,
                            "hi": self.hindi_anchors,
                            "te": self.telugu_anchors
                        }[lang]

                        score = len(text) + (10 * sum(1 for a in anchors if a in text))
                        candidates.append({
                            "lang": lang,
                            "text": text,
                            "score": score
                        })
                    except:
                        pass

            if candidates:
                best = max(candidates, key=lambda x: x["score"])
                self.process_command(best["text"], best["lang"])
            else:
                current_time = time.time()
                if (current_time - self.last_unrecognized_speech_time) > self.UNRECOGNIZED_SPEECH_COOLDOWN:
                    self.last_unrecognized_speech_time = current_time
                    if not self.audio_playing_flag.is_set():
                        logger.info("No speech recognized, asking user to repeat.")
                        self.queue_audio("Sorry, I didn't catch that. Please can you ask your question once again?", "en", interrupt=False)

        except Exception as e:
            logger.error(f"Background callback error: {e}")

    # -------------------- START --------------------

    def start(self):
        self.queue_audio("Hello, how can I help you?", "en", interrupt=False)

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

        self.recognizer.listen_in_background(
            self.microphone,
            self._background_callback,
            phrase_time_limit=15
        )

        while not self.shutdown_flag.is_set():
            time.sleep(0.5)

# -------------------- PROCESS ENTRY --------------------

def interaction_process_func(
    audio_queue,
    motor_queue,
    shutdown_flag,
    audio_playing_flag,
    mic_name="miniDSP"
):
    device_index = None
    try:
        for i, name in enumerate(sr.Microphone.list_microphone_names()):
            if mic_name.lower() in name.lower():
                device_index = i
                break
    except:
        pass

    InteractionProcess(
        audio_queue,
        motor_queue,
        shutdown_flag,
        audio_playing_flag,
        device_index
    ).start()
