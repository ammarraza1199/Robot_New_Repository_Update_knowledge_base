
import json
import difflib
import re
import logging
import sys

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("Test")

class MockInteractionProcess:
    """
    matches the EXACT logic of the current interaction_process.py
    but removes hardware dependencies (Microphone, Motor, Audio).
    """
    def __init__(self):
        # 1. Load Knowledge Base
        self.departments = []
        self.faqs = []
        self.keyword_index = {"en": {}, "hi": {}, "te": {}}
        self.department_map = {}
        self.REDIRECT_DEPARTMENTS = {
            "ophthalmology": "general_medicine",
            "eye": "general_medicine",
            "ent": "general_medicine"
        }
        self.EXIT_COMMANDS = {
            "en": ["exit now", "quit application", "stop interaction", "end conversation", "bye", "stop"],
            "hi": ["baat khatam", "band karo", "ab nahi", "ruko", "vida"],
            "te": ["sare chalu", "aapandi", "inka vaddu", "aapu", "vaddu"]
        }
        
        try:
            with open('hospital_knowledge_base.json', 'r', encoding='utf-8') as f:
                kb = json.load(f)
            self.departments = kb["departments"]
            self.faqs = kb.get("faqs", [])
            
            for dept_data in self.departments:
                cname = dept_data["canonical_name"]
                self.department_map[cname] = dept_data
                for lang, kws in dept_data["keywords"].items():
                    if lang not in self.keyword_index:
                        self.keyword_index[lang] = {}
                    for kw in kws:
                        self.keyword_index[lang][kw.lower()] = cname
        except Exception as e:
            logger.error(f"Failed to load KB: {e}")

    # --- LOGIC COPIED FROM interaction_process.py ---

    def find_department(self, user_text, lang):
        user_text = user_text.lower()
        
        # 1. Search in Requested Language
        dept = self._search_dept_in_lang(user_text, lang)
        if dept: return dept
            
        # 2. Fallback: Search in other languages
        other_langs = [l for l in ['en', 'hi', 'te'] if l != lang]
        for fallback_lang in other_langs:
            dept = self._search_dept_in_lang(user_text, fallback_lang)
            if dept: return dept
        return None

    def _search_dept_in_lang(self, user_text, lang):
        if lang not in self.keyword_index: return None
        
        # Exact/Regex
        best_match_dept = None
        longest_match_len = 0
        for kw, dept_cname in self.keyword_index[lang].items():
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, user_text):
                if len(kw) > longest_match_len:
                    longest_match_len = len(kw)
                    best_match_dept = dept_cname

        if best_match_dept:
            dept_cname_lower = best_match_dept.lower()
            if dept_cname_lower in self.REDIRECT_DEPARTMENTS:
                return self.REDIRECT_DEPARTMENTS[dept_cname_lower]
            return best_match_dept

        # Fuzzy
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

    def find_faq(self, user_text, lang):
        if not self.faqs: return None
        user_text_lower = user_text.lower()
        
        # 1. Search in Requested Language
        answer, score = self._search_faq_in_lang(user_text, lang)
        if answer: return answer
        
        # 2. Fallback
        other_langs = [l for l in ['en', 'hi', 'te'] if l != lang]
        for fallback_lang in other_langs:
            answer, score = self._search_faq_in_lang(user_text, fallback_lang)
            if answer: return answer
        return None

    def _search_faq_in_lang(self, user_text, target_lang):
        best_ans = None
        best_r = 0.0
        FAQ_THRESHOLD = 0.7
        user_text_lower = user_text.lower()

        for faq in self.faqs:
            if "question" in faq and target_lang in faq["question"]:
                q_text = faq["question"][target_lang].lower()
                
                if user_text_lower in q_text or q_text in user_text_lower:
                    r = difflib.SequenceMatcher(None, user_text_lower, q_text).ratio()
                    if len(user_text_lower) < 5:
                        if user_text_lower == q_text:
                            return faq["answer"].get(target_lang), 1.0
                    elif r > 0.5:
                        if r > best_r:
                            best_r = r
                            best_ans = faq["answer"].get(target_lang)
                
                r = difflib.SequenceMatcher(None, user_text_lower, q_text).ratio()
                if r > FAQ_THRESHOLD and r > best_r:
                    best_r = r
                    best_ans = faq["answer"].get(target_lang)
        return best_ans, best_r

    def is_medical_query(self, text):
        medical_keywords = [
            "what is", "symptoms of", "causes of", "treatment for", "diagnose", "medicine for", "pain in", "cure for", "heal",
            "kya hai", "lakshan", "ilaaj", "upchar", "chikitsa", "dawa", "dard", "taklif", "bimari", "rog",
            "noppi", "mandhu", "nivarana", "samasya", "baadha", "rogam", "jabbulu", "chikitsa"
        ]
        return any(keyword in text for keyword in medical_keywords)

    def check_exit(self, command):
        for lang_code, phrases in self.EXIT_COMMANDS.items():
            if any(cmd in command for cmd in phrases):
                return True
        return False

# --- TEST SUITE ---
def run_tests():
    bot = MockInteractionProcess()
    print("=========================================================")
    print("      ROBUST MOCK TEST REPORT - ALL FEATURES")
    print("=========================================================\n")

    test_categories = {
        "Departments (Normal)": [
            ("Where is Cardiology?", "en", "cardiology"),
            ("Dil section", "hi", "cardiology"),
            ("Mutrapindalu", "te", "urology")
        ],
        "Departments (Fuzzy/Typo)": [
            ("Where is Cardiolgy?", "en", "cardiology"),  # Typo
            ("Opthalmology", "en", "general_medicine"), # Redirect
        ],
        "Departments (Cross-Lingual Fallback)": [
            ("Cardiology", "hi", "cardiology"), # English word, Hindi lang
            ("Dil ka daura", "en", "cardiology"), # Hindi word, English lang
            ("Mutrapindalu", "en", "urology"), # Telugu word, English lang
        ],
        "FAQs (Normal)": [
            ("Where is NIMS hospital?", "en", "exists"),
            ("NIMS aspatal kahan hai?", "hi", "exists"),
            ("Visiting hours?", "en", "exists")
        ],
        "FAQs (Cross-Lingual Fallback)": [
            ("Where is NIMS hospital?", "hi", "exists"), # English Q, Hindi Lang
            ("NIMS aspatal kahan hai?", "en", "exists"), # Hindi Q, English Lang
        ],
        "Exit Commands (Robust)": [
            ("stop interaction", "en", True),
            ("ruko", "en", True), # Hindi cmd, En lang -> Should Exit
            ("aapandi", "hi", True), # Telugu cmd, Hi lang -> Should Exit
        ],
        "Medical Queries (Robust)": [
            ("What is cancer?", "en", True),
            ("Cancer ka upchar", "en", True), # Hindi keyword, En lang
            ("Naku noppi undi", "en", True), # Telugu keyword, En lang
        ]
    }

    total_pass = 0
    total_tests = 0

    for category, tests in test_categories.items():
        print(f"--- {category} ---")
        for input_text, lang, expected in tests:
            total_tests += 1
            result = None
            passed = False
            
            # Dispatch based on category type
            if "Department" in category:
                res = bot.find_department(input_text.lower(), lang)
                # Check for substring match in canonical name (e.g. "cardiology" in "cardiology_wing_1")
                if res and expected in res.lower(): passed = True
                result = res
                
            elif "FAQ" in category:
                res = bot.find_faq(input_text, lang)
                if res: passed = True
                result = "Answer Found" if res else "No Answer"

            elif "Exit" in category:
                res = bot.check_exit(input_text.lower())
                if res == expected: passed = True
                result = "EXIT" if res else "CONTINUE"

            elif "Medical" in category:
                res = bot.is_medical_query(input_text.lower())
                if res == expected: passed = True
                result = "MEDICAL_QUERY" if res else "NORMAL_QUERY"

            status = "PASS" if passed else "FAIL"
            if passed: total_pass += 1
            print(f"[{status}] In: '{input_text}' ({lang}) -> Out: {result}")
        print("")

    score = (total_pass / total_tests) * 100
    print("=========================================================")
    print(f"FINAL SCORE: {total_pass}/{total_tests} ({score:.1f}%)")
    print("=========================================================")

if __name__ == "__main__":
    run_tests()
