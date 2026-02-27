import json
import difflib
import os

KB_PATH = "hospital_knowledge_base.json"

def debug_fuzzy():
    with open(KB_PATH, "r", encoding="utf-8") as f:
        kb = json.load(f)
    
    faqs = []
    # Collect all FAQs like InteractionProcess does
    all_items = kb.get("departments", []) + kb.get("interactions", [])
    for item in all_items:
        if ("question" in item and "answer" in item) or ("keywords" in item and "answer" in item):
            # Exclude actual departments if they snuck in
            if "canonical_name" not in item:
                faqs.append(item)
    
    user_text = "neurology"
    user_text_lower = user_text.lower()
    FAQ_THRESHOLD = 0.7
    
    with open("result.txt", "w", encoding="utf-8") as out:
        out.write(f"Loaded {len(faqs)} FAQs.\n")
        out.write(f"Checking fuzzy match for '{user_text}'...\n")
        
        for faq in faqs:
            for lang in ['en', 'hi', 'te']:
                # Check keywords
                if "keywords" in faq and lang in faq["keywords"]:
                    for kw in faq["keywords"][lang]:
                        if kw.lower() in user_text_lower:
                            out.write(f"KEYWORD MATCH ({lang}): '{kw}' in '{user_text}' -> ID: {faq.get('id')}\n")
                
                # Check questions
                if "question" in faq and lang in faq["question"]:
                    q_text = faq["question"][lang].lower()
                    r = difflib.SequenceMatcher(None, user_text_lower, q_text).ratio()
                    if r > 0.6: # Show close matches
                        out.write(f"FUZZY MATCH ({lang}): '{q_text}' Score: {r:.4f} -> ID: {faq.get('id')}\n")

if __name__ == "__main__":
    debug_fuzzy()
