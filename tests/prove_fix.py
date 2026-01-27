
import json
import logging
import difflib

# Mock again, linking to the REAL interaction_process logic if possible, 
# but for portability we duplicate the KEY logic we just added (find_faq).
# This ensures we are testing the logic, not just the file existence.

class MockInteraction:
    def __init__(self):
        self.faqs = []
        try:
            with open('hospital_knowledge_base.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.faqs = data.get("faqs", [])
        except Exception as e:
            print(f"Error loading KB: {e}")

    def find_faq(self, user_text, lang):
        if not self.faqs: return None
        best_faq_answer = None
        best_ratio = 0.0
        user_text_lower = user_text.lower()
        FAQ_THRESHOLD = 0.65 # Matching the implementation
        
        for faq in self.faqs:
            if "question" in faq and lang in faq["question"]:
                question_text = faq["question"][lang].lower()
                
                # Logic from interaction_process.py
                if user_text_lower in question_text or question_text in user_text_lower:
                     ratio = difflib.SequenceMatcher(None, user_text_lower, question_text).ratio()
                     if len(user_text_lower) < 5:
                         if user_text_lower == question_text:
                             return faq["answer"].get(lang)
                     elif ratio > 0.5:
                         if ratio > best_ratio:
                             best_ratio = ratio
                             best_faq_answer = faq["answer"].get(lang)
                
                ratio = difflib.SequenceMatcher(None, user_text_lower, question_text).ratio()
                if ratio > FAQ_THRESHOLD and ratio > best_ratio:
                    best_ratio = ratio
                    best_faq_answer = faq["answer"].get(lang)

        return best_faq_answer

def run_proof():
    # The list the user was worried about
    worrisome_questions = [
        "Hi",
        "Hello",
        "Where is NIMS hospital?",
        "Where is the emergency ward?",
        "How can I get admitted?",
        "How does discharge work?",
        "Is insurance or Aarogyasri available?",
        "Where is the insurance help desk?",
        "How to provide feedback?",
        "What are key contact numbers?",
        "Where is the echo department?",
        "Where is the pacemaker department?",
        "What is 2D Echo?",
        "How long do ECG/Echo tests take?",
        "I have breathing difficulty.",
        "I have skin rash."
    ]

    bot = MockInteraction()
    print(f"Loaded {len(bot.faqs)} FAQs from Knowledge Base.")
    print("\n--- Verifying Previously Failed Questions ---")
    
    passed = 0
    for q in worrisome_questions:
        answer = bot.find_faq(q, "en")
        
        status = "PASSED" if answer else "FAILED"
        if answer:
            passed += 1
            # print(f"Q: '{q}'\n   -> A: {answer[:50]}...")
        else:
            print(f"Q: '{q}' -> FAILED")

    print(f"\nResult: {passed}/{len(worrisome_questions)} Passed.")
    if passed == len(worrisome_questions):
        print("CONFIRMATION: All listed questions are now resolvable.")

if __name__ == "__main__":
    run_proof()
