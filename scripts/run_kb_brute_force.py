import sys
import os
import json
import logging
import queue
import threading
from collections import defaultdict
import time

# Add parent directory to path to import interaction_process
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock speech_recognition to avoid PyAudio dependency
import unittest.mock as mock
import sys

# Create a mock for speech_recognition module if it's not fully mocking, 
# but specifically we need to mock Microphone before InteractionProcess inits it.
# Ideally, we mock it via sys.modules or just patch the class if imported.

# But simpler: import speech_recognition first, then mock Microphone
try:
    import speech_recognition as sr
except ImportError:
    # If sr itself is missing, we need to mock the whole thing
    sr = mock.MagicMock()
    sys.modules["speech_recognition"] = sr

# Mock Microphone class
sr.Microphone = mock.MagicMock()

from interaction_process import InteractionProcess

# Setup Logging
logging.basicConfig(level=logging.ERROR) # Keep it quiet mostly, we'll print report manually

def run_brute_force_test():
    print("Loading Knowledge Base and Initializing Interaction Process...")
    
    # Mock Queues
    audio_queue = queue.Queue()
    motor_queue = queue.Queue()
    shutdown_flag = threading.Event()
    audio_playing_flag = threading.Event()
    audio_feedback_queue = queue.Queue()
    
    # Initialize
    try:
        ip = InteractionProcess(audio_queue, motor_queue, shutdown_flag, audio_playing_flag, audio_feedback_queue)
    except Exception as e:
        print(f"FATAL: Failed to initialize InteractionProcess: {e}")
        return

    # Load raw JSON to iterate
    kb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hospital_knowledge_base.json")
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb_data = json.load(f)

    # Metrics
    stats = {
        "departments": {"total": 0, "passed": 0, "failed": 0},
        "interactions": {"total": 0, "passed": 0, "failed": 0}
    }
    failures = []

    print("\n--- STARTING BRUTE FORCE DEPARTMENT TEST ---")
    
    # 1. Test Departments
    for dept in kb_data.get("departments", []):
        dept_id = dept["id"]
        canonical_name = dept.get("canonical_name", dept_id)
        
        # Test Keywords per language
        if "keywords" in dept:
            for lang, keywords in dept["keywords"].items():
                for kw in keywords:
                    stats["departments"]["total"] += 1
                    
                    found_dept_cname = ip.find_department(kw, lang)
                    
                    # Convert found cname back to ID if possible or compare names
                    # InteractionProcess returns the 'canonical_name' usually
                    # We need to verify if 'found_dept_cname' matches 'canonical_name'
                    
                    match = False
                    if found_dept_cname:
                         # Normalize for comparison
                        if found_dept_cname.lower() == canonical_name.lower():
                            match = True
                        # Check redirects
                        elif found_dept_cname.lower() in ip.REDIRECT_DEPARTMENTS:
                             target = ip.REDIRECT_DEPARTMENTS[found_dept_cname.lower()]
                             # Ideally we map this target back to our current dept. 
                             # But for now, let's just see if it matches the ID or canonical name
                             if target.lower() == canonical_name.lower():
                                 match = True
                    
                    if match:
                        stats["departments"]["passed"] += 1
                    else:
                        stats["departments"]["failed"] += 1
                        failures.append({
                            "type": "Department",
                            "id": dept_id,
                            "lang": lang,
                            "input": kw,
                            "expected": canonical_name,
                            "got": found_dept_cname
                        })

        # Test Aliases (usually treated as English or cross-lingual exact matches depending on implementation)
        # InteractionProcess adds aliases to the 'en' keyword index usually, or checks them separately.
        # Let's check how load_knowledge_base handles aliases.
        # Actually aliases are added to self.keyword_index['en'] usually.
        # Let's test them as English input.
        if "aliases" in dept:
            for alias in dept["aliases"]:
                stats["departments"]["total"] += 1
                found_dept_cname = ip.find_department(alias, "en")
                
                match = False
                if found_dept_cname and found_dept_cname.lower() == canonical_name.lower():
                    match = True
                
                if match:
                    stats["departments"]["passed"] += 1
                else:
                    stats["departments"]["failed"] += 1
                    failures.append({
                            "type": "Department Alias",
                            "id": dept_id,
                            "lang": "en",
                            "input": alias,
                            "expected": canonical_name,
                            "got": found_dept_cname
                        })

    print("\n--- STARTING BRUTE FORCE INTERACTION TEST ---")
    
    # 2. Test Interactions
    for interaction in kb_data.get("interactions", []):
        interaction_id = interaction["id"]
        
        # Test keywords
        if "keywords" in interaction:
            for lang, keywords in interaction["keywords"].items():
                for kw in keywords:
                    stats["interactions"]["total"] += 1
                    
                    # find_faq returns the ANSWER text, not the ID.
                    # So we verify if the returned answer matches the expected answer for that lang.
                    expected_answer = interaction["answer"].get(lang, "")
                    found_answer = ip.find_faq(kw, lang)
                    
                    if found_answer == expected_answer:
                        stats["interactions"]["passed"] += 1
                    else:
                        stats["interactions"]["failed"] += 1
                        failures.append({
                            "type": "Interaction",
                            "id": interaction_id,
                            "lang": lang,
                            "input": kw,
                            "expected": expected_answer[:30] + "...",
                            "got": (found_answer[:30] + "...") if found_answer else "None"
                        })

    # Output Results
    print("\n" + "="*50)
    print("BRUTE FORCE TEST RESULTS")
    print("="*50)
    
    print(f"\nDEPARTMENTS:")
    print(f"Total Tests: {stats['departments']['total']}")
    print(f"Passed:      {stats['departments']['passed']}")
    print(f"Failed:      {stats['departments']['failed']}")
    print(f"Pass Rate:   {(stats['departments']['passed'] / stats['departments']['total'] * 100) if stats['departments']['total'] else 0:.2f}%")

    print(f"\nINTERACTIONS:")
    print(f"Total Tests: {stats['interactions']['total']}")
    print(f"Passed:      {stats['interactions']['passed']}")
    print(f"Failed:      {stats['interactions']['failed']}")
    print(f"Pass Rate:   {(stats['interactions']['passed'] / stats['interactions']['total'] * 100) if stats['interactions']['total'] else 0:.2f}%")

    # Save failures to JSON for report generation - DO THIS FIRST to avoid print crashes
    try:
        with open("kb_brute_force_failures.json", "w", encoding='utf-8') as f:
            json.dump(failures, f, indent=4, ensure_ascii=False)
        print("\nFailures saved to 'kb_brute_force_failures.json'.")
    except Exception as e:
        print(f"Error saving JSON: {e}")

    if failures:
        print("\n\nFAILURES LIST (First 20 only to avoid encoding errors - see JSON for full list):")
        print("-" * 80)
        print(f"{'Type':<15} | {'ID':<20} | {'Lang':<5} | {'Input':<30} | {'Expected vs Got'}")
        print("-" * 80)
        for i, f in enumerate(failures[:20]): # Limit to 20
            try:
                # Safe print
                safe_input = f['input'].encode('ascii', 'replace').decode('ascii')
                safe_exp = f['expected'].encode('ascii', 'replace').decode('ascii')
                safe_got = str(f['got']).encode('ascii', 'replace').decode('ascii')
                
                print(f"{f['type']:<15} | {f['id']:<20} | {f['lang']:<5} | {safe_input:<30} | Exp: {safe_exp}")
                print(f"{'':<76} | Got: {safe_got}")
                print("-" * 80)
            except Exception:
                print(f"Error printing failure {i}")

if __name__ == "__main__":
    run_brute_force_test()
