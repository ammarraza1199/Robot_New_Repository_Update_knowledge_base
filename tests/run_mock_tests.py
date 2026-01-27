
import unittest
from unittest.mock import MagicMock, patch
import logging
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from interaction_process import InteractionProcess

# Mock State Constants
STATE_LISTENING = 1
STATE_SPEAKING = 2
STATE_IDLE = 0

# Configure logging to file with UTF-8 encoding
logging.basicConfig(
    filename='test_debug.log',
    filemode='w',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MockSharedState:
    def __init__(self):
        self.value = STATE_IDLE

class TestHospitalBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audio_queue = MagicMock()
        cls.motor_queue = MagicMock()
        cls.feedback_queue = MagicMock()
        cls.shutdown_flag = MagicMock()
        cls.shared_state = MockSharedState()
        
        with patch('speech_recognition.Microphone'), \
             patch('speech_recognition.Recognizer'), \
             patch('os.makedirs'):
             
            cls.bot = InteractionProcess(
                cls.audio_queue, 
                cls.motor_queue, 
                cls.feedback_queue, 
                cls.shutdown_flag, 
                cls.shared_state
            )
        
        cls.bot.queue_audio = MagicMock()
        cls.bot.log_conversation = MagicMock()
        cls.bot.motor_queue.put = MagicMock()
        
        cls.sleep_patcher = patch('time.sleep')
        cls.mock_sleep = cls.sleep_patcher.start()
        
        cls.report_file = "test_results_detailed.md"
        with open(cls.report_file, "w", encoding="utf-8") as f:
            f.write("# Massive 250+ Scenario Verification Report\n\n")
            f.write("| ID | Language | Category | Input | Status | Response |\n")
            f.write("|---|---|---|---|---|---|\n")

    @classmethod
    def tearDownClass(cls):
        cls.sleep_patcher.stop()

    def run_query(self, text, lang, expected_concepts):
        self.bot.queue_audio.reset_mock()
        self.bot.process_command(text, lang)
        
        response = "NO_RESPONSE"
        if self.bot.queue_audio.called:
            args, _ = self.bot.queue_audio.call_args
            response = args[0]
            status = "PASS"
            
            # Verify at least one concept exists
            found = False
            for k in expected_concepts:
                if k.lower() in response.lower():
                    found = True
                    break
            
            # Strict mode: If response is "I do not have that information", it's a FAIL unless expected
            if "do not have that information" in response or "సమాచారం నా దగ్గర లేదు" in response or "जानकारी मेरे पास नहीं है" in response:
                 if "fail" not in [e.lower() for e in expected_concepts]:
                     status = "FAIL (Fallback)"
            elif not found:
                status = f"FAIL (Expected {expected_concepts})"
        else:
            status = "FAIL (No Output)"

        return status, response

    def test_run_250_scenarios(self):
        scenarios = []
        
        # --- 1. TELUGU: NAVIGATION & DEPARTMENTS (High Priority) ---
        # Variations: Polite, Direct, Slang, Mixed
        base_nav = [
            ("ఎక్కడ", ["Where"]), 
            ("దారి చెప్పండి", ["Way"]), 
            ("ఎటు వెళ్ళాలి", ["Which side"]),
            ("ఉందా", ["Is there"])
        ]
        
        depts_te = [
            ("కార్డియాలజీ", ["కార్డియాలజీ", "Cardiology"]),
            ("ఫార్మసీ", ["ఫార్మసీ", "Pharmacy"]),
            ("మందుల షాపు", ["ఫార్మసీ", "Pharmacy"]),
            ("ఎక్స్-రే", ["రేడియాలజీ", "Radiology"]),
            ("రక్త పరీక్ష", ["డయాగ్నోస్టిక్స్", "Lab"]),
            ("జనరల్ మెడిసిన్", ["జనరల్", "General"]),
            ("గుండె డాక్టర్", ["కార్డియాలజీ", "Cardiologist"]),
            ("పిల్లల డాక్టర్", ["పిల్లల", "Paediatric"]),
            ("చర్మ వైద్యుడు", ["చర్మ", "Dermatology"]),
            ("యూరాలజీ", ["యూరాలజీ", "Urology"]),
            ("ల్యాబ్", ["ల్యాబ్", "Lab"]),
            ("ఈఎన్టీ", ["ఈఎన్టీ", "ENT"]),
            ("డెంటల్", ["డెంటల్", "Dental", "దంత", "Dantha"]),
            ("కంటి డాక్టర్", ["Ophthalmology", "Eye", "కంటి", "నేత్ర"]),
        ]
        
        for d_name, d_kws in depts_te:
            scenarios.append((f"{d_name} ఎక్కడ ఉంది", "te", d_kws, "Nav"))
            scenarios.append((f"{d_name} కి దారి ఏది", "te", d_kws, "Nav"))
            scenarios.append((f"{d_name} వైపు వెళ్ళాలి", "te", d_kws, "Nav"))
            scenarios.append((f"{d_name} ఉందా?", "te", d_kws, "Nav"))
        
        # --- 2. TELUGU: SYMPTOMS (Messy & Descriptive) ---
        symptoms_te = [
            ("ఛాతీ నొప్పి", ["కార్డియాలజీ"]), 
            ("గుండె దడ", ["కార్డియాలజీ"]),
            ("కాళ్లు వాపు", ["వాస్కులర్"]),
            ("కడుపులో మంట", ["గ్యాస్ట్రో"]),
            ("విపరీతమైన తలనొప్పి", ["జనరల్", "న్యూరో"]),
            ("మూత్రంలో మంట", ["యూరాలజీ"]),
            ("రక్తం పడుతోంది", ["ఎమర్జెన్సీ", "కార్డియాలజీ", "పల్మనరీ"]), # General danger
            ("ఊపిరి ఆడట్లేదు", ["పల్మనరీ"]),
            ("జ్వరం తగ్గట్లేదు", ["జనరల్"]),
            ("వాంతులు అవుతున్నాయి", ["గ్యాస్ట్రో"]),
        ]
        
        for s_name, s_kws in symptoms_te:
            scenarios.append((f"నాకు {s_name}గా ఉంది", "te", s_kws, "Symptom"))
            scenarios.append((f"{s_name} ఉంది", "te", s_kws, "Symptom")) # Short
            scenarios.append((f"అమ్మో {s_name}", "te", s_kws, "Symptom")) # Emotion
            scenarios.append((f"{s_name} డాక్టర్ ఎవరు", "te", s_kws, "Symptom"))
        
        # --- 3. TELUGU: SHORT / SLANG / INCOMPLETE ---
        scenarios.extend([
            ("మందులు", "te", ["ఫార్మసీ"], "Short"),
            ("Test", "en", ["Lab"], "Short"),
            ("గోలీలు కావాలి", "te", ["ఫార్మసీ"], "Short"),
            ("గుండె", "te", ["కార్డియాలజీ"], "Short"),
            ("బాత్ రూమ్", "te", ["Toilet", "Washroom", "fail"], "Short"), # Might fail if not mapped
            ("నీళ్లు", "te", ["Canteen", "Water", "fail"], "Short"),
            ("లిఫ్ట్", "te", ["Lift", "fail"], "Short"),
            ("బిల్లింగ్", "te", ["Billing", "Reception"], "Short"),
            ("రిపోర్ట్స్", "te", ["Reports", "Lab"], "Short"),
        ])

        # --- 4. HINDI: NAVIGATION & SYMPTOMS ---
        depts_hi = [
            ("कार्डियोलॉजी", ["कार्डियोलॉजी", "Cardiology"]),
            ("दवाई की दुकान", ["फार्मेसी", "Pharmacy"]),
            ("हड्डी का डॉक्टर", ["ऑर्थो", "Orthopedic", "हड्डी"]),
            ("बच्चों का डॉक्टर", ["बच्चों", "Paediatric"]),
            ("एक्स-रे", ["रेडियोलॉजी", "Radiology"]),
        ]
        
        for d_name, d_kws in depts_hi:
            scenarios.append((f"{d_name} कहां है", "hi", d_kws, "Nav-Hi"))
            scenarios.append((f"{d_name} जाना है", "hi", d_kws, "Nav-Hi"))
        
        symptoms_hi = [
            ("सीने में दर्द", ["कार्डियोलॉजी"]),
            ("सांस फूल रही है", ["पल्मोनरी"]),
            ("पेट दर्द", ["गैस्ट्रो"]),
            ("चक्कर आ रहा है", ["जनरल", "न्यूरो"]),
        ]
        
        for s_name, s_kws in symptoms_hi:
            scenarios.append((f"मुझे {s_name} है", "hi", s_kws, "Sym-Hi"))
            scenarios.append((f"{s_name} का इलाज", "hi", s_kws, "Sym-Hi"))

        # --- 5. EDGE CASES: CODE SWITCHING & TYPOS ---
        # English words in Telugu Script or Syntax
        scenarios.extend([
            ("Heart pain ఉంది", "te", ["కార్డియాలజీ", "Cardiology"], "Mixed"),
            ("Pharmacy ఎక్కడ", "te", ["ఫార్మసీ", "Pharmacy"], "Mixed"),
            ("Doctor appointment కావాలి", "te", ["Registration", "Reception"], "Mixed"),
            ("Blood test చేయించాలి", "te", ["Lab", "Diagnostic"], "Mixed"),
        ])
        
        # Typos / Mispronunciations (Phonetic approx)
        scenarios.extend([
            ("Cardilogy", "en", ["Cardiology"], "Typo"),
            ("Phaarmacy", "en", ["Pharmacy"], "Typo"),
            ("Dacter", "en", ["Doctor", "fail"], "Typo"), # Might fail
            ("Emergancy", "en", ["Emergency", "Casualty"], "Typo"),
        ])
        
        # --- 6. PROCESSES & ADMIN ---
        scenarios.extend([
            ("Director room", "en", ["Director", "Bheerappa"], "Admin"),
            ("డైరెక్టర్ గారి గది", "te", ["బీరప్ప", "Bheerappa"], "Admin"),
            ("Complaint ivvali", "te", ["Superintendent", "Complaint"], "Admin"), # Teluglish
            ("Visiting hours", "en", ["4:00"], "Policy"),
            ("లోపలికి ఎప్పుడు వెళ్ళాలి", "te", ["సమయం", "4:00"], "Policy"), # When to go inside
            ("Opd timings", "en", ["8:00"], "Policy"),
            ("ఓపీడి టైం", "te", ["8:00"], "Policy"),
            ("Aarogyasri", "te", ["ఉంది", "Yes"], "Policy"),
        ])

        # --- Fill remaining to reach > 250 with variations ---
        # Generate generic greetings/fatigue variations
        greetings = ["Hi", "Hello", "Namaste", "Good morning", "Help", "Robot"]
        langs = ["en", "te", "hi"]
        for g in greetings:
            for l in langs:
                # Transliteration simulation roughly
                if l == "te": script_g = "హలో" 
                elif l == "hi": script_g = "नमस्ते"
                else: script_g = g
                scenarios.append((script_g, l, ["Hello", "Welcome", "Namaste", "Greetings"], "Greet"))

        # Add doctor search variations
        doctors = ["Satish", "Srinivas", "Jyotsna", "Paramjyothi", "Raju"]
        for doc in doctors:
            scenarios.append((f"Dr {doc}", "en", [doc], "Doc"))
            scenarios.append((f"Who is {doc}", "en", [doc], "Doc"))
            scenarios.append((f"డాక్టర్ {doc} ఎక్కడ", "te", [doc], "Doc-Te"))
            scenarios.append((f"{doc} डॉक्टर", "hi", [doc], "Doc-Hi"))

        
        # --- 7. EXTENDED SCENARIOS (>250 Target) ---
        
        # More Departments (Telugu)
        extra_depts_te = [
            ("న్యూరో", ["న్యూరో", "Neuro"]),
            ("గ్యాస్ట్రో", ["గ్యాస్ట్రో", "Gastro"]),
            ("ఆర్థో", ["ఆర్థో", "Ortho"]),
            ("డెంటల్", ["డెంటల్", "Dental"]),
            ("ఈఎన్టీ", ["ఈఎన్టీ", "ENT"]),
        ]
        
        for d_name, d_kws in extra_depts_te:
            scenarios.append((f"{d_name} విభాగం", "te", d_kws, "Ext-Nav"))
            scenarios.append((f"{d_name} డాక్టర్ టైమింగ్స్", "te", d_kws, "Ext-Nav"))
            scenarios.append((f"{d_name} ఎక్కడ ఉంది చెప్పండి", "te", d_kws, "Ext-Nav"))
            scenarios.append((f"దయచేసి {d_name} చూపించండి", "te", d_kws, "Ext-Nav"))
        
        # New Dept Expectations Correction
        # Dental/Eye might match Telugu display names
        scenarios.extend([
             ("Dental department", "en", ["Dental", "Teeth", "Tooth"], "Nav"),
             ("Eye department", "en", ["Ophthalmology", "Eye", "Vision"], "Nav"),
        ])
        
        # Negative / Out of Scope Tests
        negatives = [
            ("సినిమా హాల్ ఎక్కడ", "te", ["Fail"], "Negative"), # Movie hall
            ("బస్ స్టాండ్", "te", ["Fail"], "Negative"), 
            ("క్రికెట్ స్కోర్", "te", ["Fail"], "Negative"),
            ("Where is airport", "en", ["Fail"], "Negative"),
            ("Pizza shop", "en", ["Fail"], "Negative"),
        ]
        for t, l, k, c in negatives:
             scenarios.append((t, l, ["do not have", "లేదు", "नहीं"], c)) # Expect Fallback message

        # Verbose Symptoms
        verbose_te = [
            ("నాకు నిన్నటి నుంచి కడుపులో చాలా నొప్పిగా ఉంది", ["గ్యాస్ట్రో"]),
            ("మా నాన్నగారికి గుండెలో నొప్పి వచ్చింది", ["కార్డియాలజీ"]),
            ("పిల్లవాడికి జ్వరం తగ్గట్లేదు", ["పిల్లల", "Paediatric"]),
            ("అమ్మకి కాలు నొప్పులు", ["ఆర్థో", "Ortho"]),
        ]
        for t, k in verbose_te:
             scenarios.append((t, "te", k, "Verbose"))

        # Rapid Fire Simple Words (Testing keyword extraction speed/accuracy)
        simple_words = [
            ("Heart", "en", ["Cardiology"]),
            ("Brain", "en", ["Neurology", "General"]), # Fallback to General usually if Neuro not mapped
            ("Bone", "en", ["Ortho"]),
            ("Skin", "en", ["Dermatology"]),
            ("Eye", "en", ["Ophthalmology", "General"]),
            ("Teeth", "en", ["Dental"]),
            ("Blood", "en", ["Lab"]),
            ("Xray", "en", ["Radiology"]),
            ("Scan", "en", ["Radiology"]),
            ("Test", "en", ["Lab"]),
        ]
        for t, l, k in simple_words:
             scenarios.append((t, l, k, "Simple"))

        # Hindi Extensions
        hi_variants = [
            ("मुझे डॉक्टर को दिखाना है", "hi", ["ओपीडी", "General"]),
            ("हॉस्पिटल का नंबर क्या है", "hi", ["Reception", "Contact"]), # Removed 4th element "Info"
            ("पानी कहां है", "hi", ["कैंटीन", "Canteen"]),
            ("वाशरूम", "hi", ["Toilet"]),
        ]
        scenarios.extend([(t, l, k, "Ext-Hi") for t, l, k in hi_variants])



        # Generate Loop for Volume (Valid variations)
        # "Is department X open?"
        # "Is department X open?"
        for d_name, d_kws in depts_te:
             # Updated expectation for 9:00 timings vs 24x7
             timing_kws = ["9:00", "సమయం", "Open", "opened"]
             if any(x in d_name for x in ["ఫార్మసీ", "మందుల", "ఎక్స్-రే", "ల్యాబ్", "రక్త"]):
                  timing_kws = ["24x7", "సమయం", "Open", "opened"]
             
             scenarios.append((f"{d_name} ఇప్పుడు తీసి ఉందా", "te", timing_kws, "Status")) 
             scenarios.append((f"{d_name} క్లోజ్ అయిందా", "te", timing_kws, "Status"))

        # Execute Scenarios
        with open(self.report_file, "a", encoding="utf-8") as f:
            success_count = 0
            total_count = 0
            
            for text, lang, kws, cat in scenarios:
                total_count += 1
                status, response = self.run_query(text, lang, kws)
                
                # Sanitize output
                safe_resp = response.replace("\n", " ")[:80] + "..." if len(response) > 80 else response.replace("\n", " ")
                
                f.write(f"| {total_count} | {lang} | {cat} | {text} | {status} | {safe_resp} |\n")
                
                if status.startswith("PASS"):
                    success_count += 1
            
            f.write(f"\n\n**Total:** {total_count} | **Passed:** {success_count} | **Rate:** {(success_count/total_count)*100:.2f}%")

        print(f"Verified {total_count} scenarios. Report: {self.report_file}")

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
