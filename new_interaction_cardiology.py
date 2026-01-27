# ===================== IMPORTS =====================
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
import concurrent.futures
import random
import numpy as np
import json
from logging_config import setup_logging

# ===================== SETUP =====================
load_dotenv()
logger = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_CACHE_DIR = os.path.join(SCRIPT_DIR, "audio_cache")
CONVERSATION_LOG_FILE = os.path.join(SCRIPT_DIR, "conversations.csv")
KB_PATH = os.path.join(SCRIPT_DIR, "hospital_knowledge_base.json")

os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)

# ===================== INTERACTION PROCESS =====================
class InteractionProcess:

    def __init__(self, audio_queue, motor_queue, shutdown_flag, audio_playing_flag, device_index=None):
        self.audio_queue = audio_queue
        self.motor_queue = motor_queue
        self.shutdown_flag = shutdown_flag
        self.audio_playing_flag = audio_playing_flag

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=device_index, sample_rate=48000, chunk_size=1024)

        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"

        self.recognizer.energy_threshold = 1000
        self.recognizer.dynamic_energy_threshold = True

        self.load_knowledge_base()
        self.initialize_conversation_log()

        self.english_anchors = ["what", "where", "which", "department", "doctor", "help"]
        self.hindi_anchors = ["क्या", "कहाँ", "कौन", "विभाग", "डॉक्टर"]
        self.telugu_anchors = ["ఏమిటి", "ఎక్కడ", "ఏ విభాగం", "డాక్టర్"]

        self.EXIT_COMMANDS = {
            "en": ["exit", "quit", "stop", "bye"],
            "hi": ["बंद", "रुको", "विदा"],
            "te": ["ఆపు", "వద్దు", "బై"]
        }

    # ===================== LOGGING =====================
    def initialize_conversation_log(self):
        if not os.path.exists(CONVERSATION_LOG_FILE):
            with open(CONVERSATION_LOG_FILE, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["timestamp", "language", "question", "answer"])

    def log_conversation(self, q, a, lang):
        with open(CONVERSATION_LOG_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([datetime.now().isoformat(), lang, q, a])

    # ===================== KNOWLEDGE BASE =====================
    def load_knowledge_base(self):
        with open(KB_PATH, "r", encoding="utf-8") as f:
            kb = json.load(f)

        self.departments = kb["departments"]
        self.default_redirect = kb.get("default_redirect_department", "general_opd")

        self.department_map = {}
        self.keyword_index = {"en": {}, "hi": {}, "te": {}}

        for dept in self.departments:
            cname = dept["canonical_name"]
            self.department_map[cname] = dept
            for lang, kws in dept["keywords"].items():
                for kw in kws:
                    self.keyword_index[lang][kw.lower()] = cname

        logger.info("Knowledge base loaded")

    # ===================== AUDIO =====================
    def queue_audio(self, text, lang, interrupt=True):
        if interrupt:
            self.audio_queue.put({"command": "stop"})
            time.sleep(0.1)

        clean = re.sub(r"[^\w\s]", "", text)
        fname = hashlib.md5((clean + lang).encode()).hexdigest() + ".mp3"
        path = os.path.join(AUDIO_CACHE_DIR, fname)

        if not os.path.exists(path):
            gTTS(clean, lang=lang).save(path)

        self.audio_queue.put({"command": "play", "file": fname})

    # ===================== DEPARTMENT RESOLUTION (CORE FIX) =====================
    def resolve_department_or_fallback(self, text, lang):
        text = text.lower()

        # 1️⃣ Keyword match
        for kw, dept in self.keyword_index.get(lang, {}).items():
            if kw in text:
                return dept

        # 2️⃣ Explicit department name mention
        for cname, dept in self.department_map.items():
            if cname.lower() in text:
                return cname
            display = dept["display_name"].get(lang, "").lower()
            if display and display in text:
                return cname

        # 3️⃣ HARD SAFE FALLBACK
        return self.default_redirect

    # ===================== RESPONSE =====================
    def _format_guidance_response(self, dept_name, lang):
        dept = self.department_map.get(dept_name)
        if not dept:
            return None

        name = dept["display_name"].get(lang, dept_name)
        loc = dept["location"].get(lang, "N/A")
        doc = dept["doctors"][0]["name"]

        if lang == "hi":
            return f"कृपया {name} जाएं। डॉक्टर {doc}। स्थान {loc}।"
        elif lang == "te":
            return f"{name}కి వెళ్లండి. డాక్టర్ {doc}. చిరునామా {loc}."
        return f"Please visit {name}. Doctor {doc}. Location {loc}."

    # ===================== PROCESS =====================
    def process_command(self, text, lang):
        self.motor_queue.put(f"turn_to:{random.randint(-30,30)}")

        if any(cmd in text for cmd in self.EXIT_COMMANDS.get(lang, [])):
            self.queue_audio("Goodbye!", lang)
            self.shutdown_flag.set()
            return

        dept = self.resolve_department_or_fallback(text, lang)
        response = self._format_guidance_response(dept, lang)

        if response:
            self.log_conversation(text, response, lang)
            self.queue_audio(response, lang)

        self.motor_queue.put("turn_to:0")

    # ===================== SPEECH CALLBACK =====================
    def _background_callback(self, recognizer, audio):
        for lang in ["en", "hi", "te"]:
            try:
                text = recognizer.recognize_google(audio, language=f"{lang}-IN").lower()
                self.process_command(text, lang)
                return
            except:
                pass

    # ===================== START =====================
    def start(self):
        self.queue_audio("Hello, how can I help you?", "en", interrupt=False)
        with self.microphone as src:
            self.recognizer.adjust_for_ambient_noise(src)

        stop = self.recognizer.listen_in_background(self.microphone, self._background_callback)
        while not self.shutdown_flag.is_set():
            time.sleep(0.5)
        stop(wait_for_stop=False)

# ===================== ENTRY =====================
def interaction_process_func(audio_queue, motor_queue, shutdown_flag, audio_playing_flag, mic_name="miniDSP"):
    setup_logging()
    idx = None
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        if mic_name.lower() in name.lower():
            idx = i
            break

    InteractionProcess(audio_queue, motor_queue, shutdown_flag, audio_playing_flag, idx).start()
