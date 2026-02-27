import sys
import os
import json
import re

import logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Add path
sys.path.append(os.getcwd())
from interaction_process import InteractionProcess
from unittest.mock import MagicMock

def debug_nlu():
    try:
        ip = InteractionProcess(MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock())
    except Exception as e:
        print(f"FAILED TO INITIALIZE: {e}")
        import traceback
        traceback.print_exc()
        return
    
    test_inputs = [
        ("Hello bro how are you", "en"),
        ("Where is water?", "en"),
        ("నొప్పి తగ్గడానికి ఏదైనా ట్యాబ్లెట్ ఇస్తావా?", "te"),
        ("Neurology", "en")
    ]
    
    for text, lang in test_inputs:
        print(f"\n--- DEBUG: '{text}' ({lang}) ---")
        try:
            is_med = ip.is_medical_query(text)
            print(f"Medical Safety: {is_med}")
            
            dept = ip.find_department(text, lang)
            print(f"Department Match: {dept}")
            
            faq = ip.find_faq(text, lang)
            print(f"FAQ Match: {faq}")
            
            if dept:
                # Find which keyword matched
                for kw, cname in ip.keyword_index.get(lang, {}).items():
                    if re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE):
                        print(f"  Matched Keyword: '{kw}' -> {cname}")
        except Exception as e:
            print(f"  ERROR DURING PROCESSING '{text}': {e}")

if __name__ == "__main__":
    debug_nlu()
