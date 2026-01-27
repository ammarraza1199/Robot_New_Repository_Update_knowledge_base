
import json
import logging
from interaction_process import InteractionProcess
import sys

# Mocking the InteractionProcess to avoid hardware init
class MockInteraction(InteractionProcess):
    def __init__(self):
        # Initialize only what's needed for logic
        self.logger = logging.getLogger("MockInteraction")
        self.department_map = {}
        self.keyword_index = {"en": {}, "hi": {}, "te": {}}
        # Manually load KB (simulating the load_knowledge_base method or calling it if safe)
        # We'll use the real helper method from the class if possible, or reimplement lightweight version
        self.REDIRECT_DEPARTMENTS = {
            "ophthalmology": "general_medicine",
            "eye": "general_medicine",
            "ent": "general_medicine"
        }
        self.load_knowledge_base()
        
    def load_knowledge_base(self):
        # Simplified load to ensure we are using the exact logic from the file
        try:
            with open('hospital_knowledge_base.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for dept in data['departments']:
                dept_id = dept['id']
                dept_cname = dept['canonical_name']
                self.department_map[dept_cname] = dept
                
                # Index keywords
                for lang, keywords in dept['keywords'].items():
                    if lang not in self.keyword_index: self.keyword_index[lang] = {}
                    for kw in keywords:
                        self.keyword_index[lang][kw] = dept_cname
                        
        except Exception as e:
            print(f"Error loading KB: {e}")

def run_verification():
    print("Loading questions.txt...")
    try:
        with open('questions.txt', 'r', encoding='utf-8') as f:
            questions = json.load(f)
    except Exception as e:
        print(f"Error loading questions.txt: {e}")
        return

    bot = MockInteraction()
    
    results = {
        "resolved": 0,
        "unresolved": 0,
        "total": len(questions)
    }
    
    unresolved_categories = {}

    print("\n--- Verifying Questions ---")
    for q_item in questions:
        q_id = q_item.get("id", "unknown")
        category = q_item.get("category", "Unknown")
        
        # Test English Question
        q_text_en = q_item["question"]["en"]
        
        # Try to resolve locally
        match = bot.find_department(q_text_en, "en")
        
        if match:
            results["resolved"] += 1
            # print(f"[PASS] {q_id}: '{q_text_en}' -> {match}")
        else:
            results["unresolved"] += 1
            if category not in unresolved_categories:
                unresolved_categories[category] = []
            unresolved_categories[category].append(q_text_en)
            # print(f"[FAIL] {q_id}: '{q_text_en}' -> No local match")

    print("\n--- Verification Summary ---")
    print(f"Total Questions: {results['total']}")
    print(f"Locally Resolved: {results['resolved']}")
    print(f"Unresolved (LLM Dependent): {results['unresolved']}")
    print(f"Coverage: {(results['resolved']/results['total'])*100:.1f}%")
    
    print("\n--- Unresolved by Category ---")
    for cat, qs in unresolved_categories.items():
        print(f"{cat}: {len(qs)} failures")
        # Print first 3 examples
        for q in qs[:3]:
            print(f"  - {q}")

if __name__ == "__main__":
    run_verification()
