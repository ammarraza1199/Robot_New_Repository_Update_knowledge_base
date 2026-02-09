import os
import sys
import logging

# Configure logging to console
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("Verification")

try:
    from interaction_process import InteractionProcess
except ImportError:
    # Add current dir to path if needed
    sys.path.append(os.getcwd())
    from interaction_process import InteractionProcess

def verify():
    # Set dummy API key to avoid crash on init
    os.environ["GROQ_API_KEY"] = "dummy_key"
    
    logger.info("Initializing InteractionProcess...")
    # Pass mocks for queues
    try:
        from unittest.mock import MagicMock
        ip = InteractionProcess(MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock())
    except Exception as e:
        logger.error(f"Failed to init IP: {e}")
        return

    test_queries = [
        ("neurology", "en"),
        ("user query variation 0 for neurology", "en"),
        ("consult cardiologist", "en")
    ]

    print("--- Starting Verification ---")
    for query, lang in test_queries:
        print(f"Testing: '{query}' ({lang})")
        dept = ip.find_department(query, lang)
        
        if dept:
            print(f"RESULT: MATCH -> {dept.get('canonical_name')}")
        else:
            print("RESULT: NO MATCH")
            
            # Debug why
            print(f"Debug: Keywords in index for {lang}: {len(ip.keyword_index.get(lang, {}))}")
            if "neurology" in ip.keyword_index.get(lang, {}):
                 print("Debug: 'neurology' key exists in index.")
            else:
                 print("Debug: 'neurology' key MISSING from index.")

if __name__ == "__main__":
    verify()
