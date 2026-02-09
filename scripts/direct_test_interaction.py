
import sys
import os
import logging
# Configure logging to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Mock modules BEFORE importing interaction_process
from unittest.mock import MagicMock
sys.modules["speech_recognition"] = MagicMock()
sys.modules["gtts"] = MagicMock()
sys.modules["playsound"] = MagicMock()

from interaction_process import InteractionProcess

# Create a dummy SharedState
class MockSharedState:
    def __init__(self):
        self.value = 0

def test():
    print("Initializing InteractionProcess...")
    # Mock queues
    bot = InteractionProcess(MagicMock(), MagicMock(), MagicMock(), MagicMock(), MockSharedState())
    
    print(f"Interactions loaded: {len(bot.interactions)}")
    
    text = "Hi"
    lang = "en"
    print(f"Testing find_interaction('{text}', '{lang}')")
    
    match = bot.find_interaction(text, lang)
    print(f"Result: {match}")
    
    if match:
        print("SUCCESS")
    else:
        print("FAILURE")

    # Debug specific item
    for item in bot.interactions:
        if item['id'] == 'greet_hi':
            print(f"Found greet_hi: {item}")
            keywords = item.get("keywords", {}).get(lang, [])
            print(f"Keywords: {keywords}")
            import re
            for kw in keywords:
                pattern = r'\b' + re.escape(kw) + r'\b'
                print(f"Testing pattern '{pattern}' against '{text.lower()}'")
                if re.search(pattern, text.lower(), re.IGNORECASE):
                    print("MATCHED in loop")

if __name__ == "__main__":
    test()
