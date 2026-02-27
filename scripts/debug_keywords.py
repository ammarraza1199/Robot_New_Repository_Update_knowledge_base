
import sys
import os
import logging
from unittest.mock import MagicMock

# Configure logging to see what's happening
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add current dir to sys.path
sys.path.append(os.getcwd())

try:
    from interaction_process import InteractionProcess
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def debug_kb():
    print("--- DEBUGGING KB LOADING ---")
    aq = MagicMock()
    mq = MagicMock()
    sf = MagicMock()
    apf = MagicMock()
    afq = MagicMock()
    
    # Initialize InteractionProcess
    # We pass None for device_index to avoid microphone initialization issues
    ip = InteractionProcess(aq, mq, sf, apf, afq, device_index=None)
    
    print(f"KB_PATH in InteractionProcess: {ip.KB_PATH if hasattr(InteractionProcess, 'KB_PATH') else 'N/A'}")
    # Note: InteractionProcess defines KB_PATH as a global or class variable?
    # Actually it's defined at the module level in interaction_process.py (line 36)
    
    import interaction_process
    print(f"Module-level KB_PATH: {interaction_process.KB_PATH}")
    print(f"File exists at KB_PATH: {os.path.exists(interaction_process.KB_PATH)}")
    
    print(f"Departments loaded: {len(ip.department_map)}")
    print(f"FAQs loaded: {len(ip.faqs)}")
    print(f"Keywords in 'en': {len(ip.keyword_index.get('en', {}))}")
    print(f"Keywords in 'hi': {len(ip.keyword_index.get('hi', {}))}")
    print(f"Keywords in 'te': {len(ip.keyword_index.get('te', {}))}")
    
    # Test a match
    test_queries = [
        ("fever", "en"),
        ("букхар", "hi"), # बुखार (phonetic approx for test script if typing issues)
        ("fever", "hi"),
        ("weakness", "en"),
        ("జ్వరం", "te") # జ్వరం
    ]
    
    # Let's try to find 'बुखार' specifically
    test_queries.append(("बुखार", "hi"))

    print("\n--- TESTING MATCHES ---")
    for q, lang in test_queries:
        match = ip.find_department(q, lang)
        print(f"Query: '{q}' ({lang}) -> Match: {match}")

if __name__ == "__main__":
    debug_kb()
