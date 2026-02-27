
import json
import logging
# Minimal mock of interaction process logic
import difflib
import re

class MockInteraction:
    def __init__(self):
        self.department_map = {}
        self.keyword_index = {"en": {}, "hi": {}, "te": {}}
        # Simulating load_knowledge_base
        try:
            with open('hospital_knowledge_base.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for dept in data['departments']:
                dept_cname = dept['canonical_name']
                self.department_map[dept_cname] = dept
                for lang, keywords in dept['keywords'].items():
                    if lang not in self.keyword_index: self.keyword_index[lang] = {}
                    for kw in keywords:
                        self.keyword_index[lang][kw] = dept_cname
        except Exception as e:
            print(f"Error loading KB: {e}")

    def find_department(self, user_text, lang):
        # EXACT LOGIC COPY FROM INTERACTION_PROCESS.PY (Simulated)
        # 1. Exact/Regex match
        matched_departments = set()
        sorted_keywords = sorted(self.keyword_index[lang].items(), key=lambda item: len(item[0]), reverse=True)
        processed_text = user_text.lower()
        
        for kw, dept_cname in sorted_keywords:
            if lang == 'en':
                pattern = r'\b' + re.escape(kw) + r'\b'
            else:
                pattern = r'(?:^|\s)' + re.escape(kw)
            
            if re.search(pattern, processed_text):
                return dept_cname # Return first match for simplicity

        # 2. Fuzzy match
        user_words = user_text.lower().split()
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
                if ratio > 0.65:
                    return dept_cname
        return None

def run_verification():
    print("Loading questions.txt...")
    try:
        with open('questions.txt', 'r', encoding='utf-8') as f:
            questions = json.load(f)
    except Exception as e:
        print(f"Error loading questions.txt: {e}")
        return

    bot = MockInteraction()
    results = {"resolved": 0, "unresolved": 0, "total": len(questions)}
    unresolved = {}

    for q_item in questions:
        q_text = q_item["question"]["en"]
        cat = q_item.get("category", "Unknown")
        
        match = bot.find_department(q_text, "en")
        
        if match:
            results["resolved"] += 1
        else:
            results["unresolved"] += 1
            if cat not in unresolved: unresolved[cat] = []
            unresolved[cat].append(q_text)

    print(json.dumps(results, indent=2))
    print("\nUNRESOLVED_SAMPLE:")
    for cat, qs in unresolved.items():
        print(f"{cat}: {qs[:2]}") # Show 2 examples per category

if __name__ == "__main__":
    run_verification()
