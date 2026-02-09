
import json
import difflib
import re

# Mock Logic (Mirroring the Refactored code)
class MockInteraction:
    def __init__(self):
        self.keyword_index = {"en": {}, "hi": {}, "te": {}}
        self.REDIRECT_DEPARTMENTS = {"ophthalmology": "general_medicine"}
        # Load KB
        with open('hospital_knowledge_base.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        for dept in data.get('departments', []):
            cname = dept['canonical_name']
            if 'keywords' in dept:
                for lang, kws in dept['keywords'].items():
                    if lang not in self.keyword_index:
                         self.keyword_index[lang] = {}
                    for k in kws:
                        self.keyword_index[lang][k.lower()] = cname

    def find_department(self, user_text, lang):
        user_text = user_text.lower()
        dept = self._search_dept_in_lang(user_text, lang)
        if dept: return dept
            
        other_langs = [l for l in ['en', 'hi', 'te'] if l != lang]
        for fallback_lang in other_langs:
            dept = self._search_dept_in_lang(user_text, fallback_lang)
            if dept: return dept
        return None

    def _search_dept_in_lang(self, user_text, lang):
        if lang not in self.keyword_index: return None
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

        user_words = user_text.split()
        best_fuzzy_dept = None
        best_ratio = 0.0

        for kw, dept_cname in self.keyword_index[lang].items():
            kw_lower = kw.lower()
            for user_word in user_words:
                if len(user_word) < 4: continue
                if len(kw_lower) > 4 and (user_word in kw_lower or kw_lower in user_word):
                     if len(user_word) / len(kw_lower) > 0.5:
                         return dept_cname
                ratio = difflib.SequenceMatcher(None, user_word, kw_lower).ratio()
                if ratio > 0.65 and ratio > best_ratio:
                    best_ratio = ratio
                    best_fuzzy_dept = dept_cname
        return best_fuzzy_dept

def run_test():
    bot = MockInteraction()
    print("--- Verifying Cross-Lingual DEPARTMENT Fallback ---")
    
    # Text, Detected Lang, Detection Description
    tests = [
        ("Cardiology", "hi", "English Keyword, Detected as Hindi"),
        ("Dil ka daura", "en", "Hindi Keyword, Detected as English (Heart Attack)"),
        ("Opthalmology", "te", "English Keyword (Typo+Redirect), Detected as Telugu"),
        ("Mutrapindalu", "en", "Telugu Keyword (Kidneys), Detected as English")
    ]
    
    passed = 0
    for text, wrong_lang, desc in tests:
        print(f"\nTest: '{text}' | Detected as: '{wrong_lang}' ({desc})")
        dept = bot.find_department(text, wrong_lang)
        if dept:
            print(f"RESULT: PASSED -> Found '{dept}'")
            passed += 1
        else:
            print(f"RESULT: FAILED")

    if passed == len(tests):
        print("\nSUCCESS: All Department Fallback tests passed.")

if __name__ == "__main__":
    run_test()
