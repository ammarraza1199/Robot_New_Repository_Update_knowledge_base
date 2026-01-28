
import json
import difflib
import logging
# Mock class again
class MockInteraction:
    def __init__(self):
        self.logger = logging.getLogger("Mock")
        self.faqs = []
        try:
            with open('hospital_knowledge_base.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.faqs = data.get("faqs", [])
        except Exception as e:
            print(f"Error: {e}")

    def find_faq(self, user_text, lang):
        if not self.faqs: return None
        best_faq_answer = None
        best_ratio = 0.0
        user_text_lower = user_text.lower()
        FAQ_THRESHOLD = 0.7 
        
        for faq in self.faqs:
            if "question" in faq and lang in faq["question"]:
                question_text = faq["question"][lang].lower()
                
                # Direct check
                if user_text_lower in question_text or question_text in user_text_lower:
                     ratio = difflib.SequenceMatcher(None, user_text_lower, question_text).ratio()
                     if len(user_text_lower) < 5:
                         if user_text_lower == question_text:
                             return faq["answer"].get(lang)
                     elif ratio > 0.5:
                         if ratio > best_ratio:
                             best_ratio = ratio
                             best_faq_answer = faq["answer"].get(lang)
                
                # Fuzzy
                ratio = difflib.SequenceMatcher(None, user_text_lower, question_text).ratio()
                if ratio > FAQ_THRESHOLD and ratio > best_ratio:
                    best_ratio = ratio
                    best_faq_answer = faq["answer"].get(lang)

        return best_faq_answer

def run_tests():
    with open('questions.txt', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    bot = MockInteraction()
    
    langs = ['en', 'hi', 'te']
    stats = {l: {'pass': 0, 'fail': 0, 'total': 0} for l in langs}
    
    print("--- Verifying Multilingual FAQs ---")
    
    for q_item in questions:
        for lang in langs:
            # Some entries might not have all langs? questions.txt looks consistent though.
            if lang in q_item['question']:
                q_text = q_item['question'][lang]
                expected = q_item['answer'][lang] # We don't check exact answer match, just that we got *an* answer
                
                stats[lang]['total'] += 1
                
                result = bot.find_faq(q_text, lang)
                
                if result:
                    stats[lang]['pass'] += 1
                else:
                    stats[lang]['fail'] += 1
                    if stats[lang]['fail'] <= 3: # Print first 3 failures
                        print(f"[{lang.upper()} FAIL] Q: '{q_text}' -> Got None")

    print("\n--- Summary ---")
    for lang in langs:
        s = stats[lang]
        pct = (s['pass'] / s['total']) * 100 if s['total'] > 0 else 0
        print(f"Language {lang.upper()}: {s['pass']}/{s['total']} ({pct:.1f}%)")

if __name__ == "__main__":
    run_tests()
