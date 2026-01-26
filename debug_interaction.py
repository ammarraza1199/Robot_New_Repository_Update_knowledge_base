
import json
import re
import os

def check():
    try:
        with open('hospital_knowledge_base.json', 'r', encoding='utf-8') as f:
            kb = json.load(f)
        
        interactions = kb.get("interactions", [])
        if isinstance(interactions, dict) and 'value' in interactions:
            interactions = interactions['value']
            
        print(f"Loaded {len(interactions)} interactions.")
        
        text = "Hi"
        lang = "en"
        
        for item in interactions:
            keywords = item.get("keywords", {}).get(lang, [])
            print(f"Checking item {item.get('id')} keywords: {keywords}")
            for kw in keywords:
                if lang == 'en':
                    pattern = r'\b' + re.escape(kw) + r'\b'
                else:
                    pattern = r'(?:^|\s)' + re.escape(kw)
                
                if re.search(pattern, text, re.IGNORECASE):
                    print(f"MATCH FOUND: {kw} in {text}")
                    return
        print("NO MATCH FOUND")

    except Exception as e:
        print(f"Error: {e}")

check()
