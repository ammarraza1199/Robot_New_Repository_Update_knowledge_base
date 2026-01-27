import json
import os

def migrate():
    # Load Questions
    if not os.path.exists('questions.txt'):
        print("questions.txt not found.")
        return
    
    with open('questions.txt', 'r', encoding='utf-8') as f:
        new_questions = json.load(f)
    print(f"Loaded {len(new_questions)} questions from questions.txt")

    # Load KB
    kb_path = 'hospital_knowledge_base.json'
    if not os.path.exists(kb_path):
        print("Knowledge base not found.")
        return

    with open(kb_path, 'r', encoding='utf-8') as f:
        kb_data = json.load(f)

    # Initialize FAQs list if not present
    if 'faqs' not in kb_data:
        kb_data['faqs'] = []
    
    # Create a set of existing IDs to avoid duplicates
    existing_ids = {item['id'] for item in kb_data['faqs']}
    
    added_count = 0
    for q_item in new_questions:
        if q_item['id'] not in existing_ids:
            # We want to store it in a clean format
            # Structure in questions.txt is already good:
            # { "category":..., "id":..., "question": {...}, "answer": {...} }
            kb_data['faqs'].append(q_item)
            added_count += 1
            existing_ids.add(q_item['id'])
    
    # Save KB
    with open(kb_path, 'w', encoding='utf-8') as f:
        json.dump(kb_data, f, ensure_ascii=False, indent=2)
    
    print(f"Migration complete. Added {added_count} new FAQs. Total FAQs: {len(kb_data['faqs'])}")

if __name__ == "__main__":
    migrate()
