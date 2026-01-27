from interaction_process import InteractionProcess
import logging
import os
import sys

# Configure logging to stdout
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("interaction_process")
logger.setLevel(logging.INFO)

class TestInteraction(InteractionProcess):
    def __init__(self):
        # Setup minimal state required for find_department
        self.keyword_index = {"en": {}, "hi": {}, "te": {}}
        self.department_map = {}
        self.REDIRECT_DEPARTMENTS = {
            "ophthalmology": "general_medicine",
            "eye": "general_medicine",
            "ent": "general_medicine"
        }
        # Call the real load_knowledge_base
        self.load_knowledge_base()

def run_tests():
    print("--- Starting Fuzzy Matching Tests ---\n")
    try:
        tester = TestInteraction()
    except Exception as e:
        print(f"Failed to initialize TestInteraction: {e}")
        return

    test_cases = [
        # Exact matches (Baseline)
        ("cardiology", "en", "Cardiology Unit-1"), # Assuming mapping
        
        # Substring matches (The core requirement)
        ("cardiol", "en", "Cardiology Unit-1"),
        ("gastro", "en", "Medical Gastroenterology"),
        ("pulmonar", "en", "Pulmonary Medicine"),
        ("neurolo", "en", None), # Should fail if neurology not in KB
        
        # Typos (Fuzzy Ratio)
        ("cardiologgy", "en", "Cardiology Unit-1"),
        ("gastrenterology", "en", "Medical Gastroenterology"),
        
        # Short words (Should be skipped)
        ("car", "en", None), 
        ("the", "en", None),
        
        # Hindi/Telugu Transliterated-ish or partials
        ("dil", "hi", "Cardiology Unit-1"), # Exact match in Hindi ks
    ]

    passed = 0
    for text, lang, expected in test_cases:
        print(f"Testing input: '{text}' ({lang})...")
        result = tester.find_department(text, lang)
        
        # Determine success
        if expected is None:
            is_pass = (result is None)
        else:
            # We assume result might be any of the units for generic terms like "cardio"
            # So if expected is "Cardiology Unit-1" but we get "Cardiology Unit-2", that's acceptable for "cardio" 
            # as long as it's a cardiology unit.
            if result and expected.split()[0] in result: 
                is_pass = True
            else:
                is_pass = (result == expected)
        
        status = "PASS" if is_pass else f"FAIL (Expected {expected}, Got {result})"
        print(f"  -> {status}\n")
        if is_pass: passed += 1

    print(f"Tests Completed. {passed}/{len(test_cases)} Passed.")

if __name__ == "__main__":
    run_tests()
