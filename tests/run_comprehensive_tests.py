import os
import sys

# Ensure the root directory is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import time
from interaction_process import InteractionProcess

def run_comprehensive_tests():
    # Load test data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'comprehensive_test_data.json')
    
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            test_cases = json.load(f)
    except FileNotFoundError:
        print(f"Error: {data_path} not found. Run generate_tests.py first.")
        sys.exit(1)

    print(f"Loaded {len(test_cases)} test cases.")

    # Initialize Robot Process
    # Mock queues for initialization
    from multiprocessing import Queue, Value
    from unittest.mock import MagicMock
    import sys
    
    # Mock speech_recognition and pyttsx3 to avoid hardware/driver errors
    sys.modules['speech_recognition'] = MagicMock()
    sys.modules['pyttsx3'] = MagicMock()
    
    # Re-import interaction_process after mocking if it was already imported, 
    # but here it is imported at top level. 
    # Since InteractionProcess logic we need (find_interaction) doesn't use the hardware, 
    # we just need __init__ to pass.
    
    # Actually, we need to mock the `sr` used INSIDE interaction_process.
    # Since we imported InteractionProcess already, `sr` is already imported there.
    # We need to patch it in that module.
    import interaction_process
    interaction_process.sr = MagicMock()
    interaction_process.pyttsx3 = MagicMock()
    interaction_process.gTTS = MagicMock()
    
    # Mock conversation logging and audio queuing to avoid side effects/network during tests
    InteractionProcess.initialize_conversation_log = MagicMock()
    InteractionProcess.log_conversation = MagicMock()
    InteractionProcess.queue_audio = MagicMock()

    audio_queue = Queue()
    motor_queue = Queue()
    audio_feedback_queue = Queue()
    shutdown_flag = Value('b', False)
    shared_interaction_state = Value('i', 0)

    try:
        robot = InteractionProcess(audio_queue, motor_queue, audio_feedback_queue, shutdown_flag, shared_interaction_state)
    except Exception as e:
        print(f"Warning: Failed to init robot cleanly: {e}")
        # If init fails (e.g. some other dependency), we might still be able to use the class methods if we instantiate carefully 
        # or if we just use the class without full init if possible (unlikely).
        # Let's try to proceed.
        # If we can't init, we can't test.
        # Let's try to just Instantiate and assume the mocks work.
        pass
    # Mock voice specifically to avoid sound generation if needed, though interaction_process might handles it.
    # checking interaction_process usage... it seems to be independent of voice for find_interaction method.

    results = []
    passed_count = 0
    start_time = time.time()

    print(f"{'ID':<30} | {'Type':<15} | {'Lang':<5} | {'Status':<6} | {'Query'}")
    print("-" * 100)

    # Helper to simulate validation logic without side effects
    def get_robot_response(robot, command, lang):
        # 1. Departments Match
        matched_dept = robot.find_department(command, lang)
        if matched_dept:
            return robot._format_guidance_response(matched_dept, lang)

        # 2. FAQ Match
        faq_answer = robot.find_faq(command, lang)
        if faq_answer:
            return faq_answer

        # 3. Medical Advice Check
        if robot.is_medical_query(command):
            return "I cannot provide medical advice. Please consult a doctor."
            
        # 4. Fallback (Simulated, as LLM is skipped in basic tests)
        if lang == "hi":
            return "जानकारी मेरे पास नहीं है। असुविधा के लिए मुझे खेद है। कृपया उत्तर के लिए पास के अस्पताल के कर्मचारियों से पूछें। धन्यवाद।"
        elif lang == "te":
            return "సమాచారం నా దగ్గర లేదు. అసౌకర్యానికి చింతిస్తున్నాను. దయచేసి సమాధానం కోసం దగ్గర్లోని ఆసుపత్రి సిబ్బందిని అడగండి. ధన్యవాదాలు."
        else:
            return "The information is not with me. I am sorry for your inconvenience. Please ask the nearby hospital staff for the answer. Thank you."

    for case in test_cases:
        test_id = case['id']
        query = case['text']
        lang = case['lang']
        expected_ids = case['expected_ids']
        test_type = case.get('type', 'Unknown')

        response = get_robot_response(robot, query, lang)
        
        status = "FAIL"
        
        # Validation Logic
        if "MEDICAL_ADVICE_REFUSAL" in expected_ids:
            # Check for localized medical refusal phrases
            advice_phrases = [
                "I cannot provide medical advice", 
                "चिकित्सकीय सलाह नहीं दे सकता", 
                "వైద్య సలహా ఇవ్వలేను"
            ]
            if response and any(phrase in response for phrase in advice_phrases):
                status = "PASS"

        elif "FALLBACK_RESPONSE" in expected_ids:
            # Check for localized fallback phrases
            fallback_phrases = [
                "I do not have that information",
                "जानकारी मेरे पास नहीं है",
                "సమాచారం నా దగ్గర లేదు"
            ]
            if response and any(phrase in response for phrase in fallback_phrases):
                status = "PASS"
            # Also acceptable if it returns None in our simulator (mocking the silence/listening loop)
            # But get_robot_response actually returns None if no match.
            # In real system, None -> "I do not have that information" (via get_fallback_response) IF we queried Llama, 
            # but here query_llama returns None, so it hits get_fallback_response.
            # Wait, look at InteractionProcess code:
            # else: response_text = self.query_llama(...) or self.get_fallback_response(lang)
            # So it ALWAYS returns a fallback string if nothing else matches.
            # So response MUST match the fallback string.
        
        elif response:
             # Regular positive match validation
             # Check if it's NOT a refusal or fallback if we expected a match
             refusal_phrases = [
                "I cannot provide medical advice", "चिकित्सकीय सलाह नहीं दे सकता", "వైద్య సలహా ఇవ్వలేను",
                "I do not have that information", "जानकारी मेरे पास नहीं है", "సమాచారం నా దగ్గర లేదు"
             ]
             if not any(phrase in response for phrase in refusal_phrases):
                 status = "PASS"
        
        if status == "PASS":
            passed_count += 1
            
        results.append({
            "id": test_id,
            "query": query,
            "lang": lang,
            "type": test_type,
            "expected_ids": expected_ids,
            "actual_response": str(response).replace('\n', ' '), # sanitize for CSV
            "status": status
        })

    # Generate Full CSV Log
    log_path = os.path.join(script_dir, "full_test_log.csv")
    with open(log_path, "w", encoding="utf-8", newline='') as csvfile:
        import csv
        fieldnames = ["id", "type", "lang", "status", "query", "expected_ids", "actual_response"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)
    print(f"Full test log written to {log_path}")
        
        # print(f"{test_id:<30} | {test_type:<15} | {lang:<5} | {status:<6} | {query[:40]}...")

    duration = time.time() - start_time
    pass_rate = (passed_count / len(test_cases)) * 100

    print("-" * 100)
    print(f"Completed {len(test_cases)} tests in {duration:.2f}s")
    print(f"Passed: {passed_count}")
    print(f"Failed: {len(test_cases) - passed_count}")
    print(f"Pass Rate: {pass_rate:.2f}%")

    # Generate Detailed Markdown Report
    generate_report(results, len(test_cases), passed_count, pass_rate, duration, script_dir)

def generate_report(results, total, passed, rate, duration, output_dir):
    filename = os.path.join(output_dir, "comprehensive_test_report.md")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Comprehensive Test Suite Report\n\n")
        f.write(f"- **Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **Total Tests**: {total}\n")
        f.write(f"- **Passed**: {passed}\n")
        f.write(f"- **Failed**: {total - passed}\n")
        f.write(f"- **Pass Rate**: {rate:.2f}%\n")
        f.write(f"- **Duration**: {duration:.2f}s\n\n")
        
        f.write("## Failure Analysis by Category\n")
        # Group by type
        by_type = {}
        for r in results:
            t = r['type']
            if t not in by_type: by_type[t] = {"total": 0, "pass": 0}
            by_type[t]["total"] += 1
            if r['status'] == "PASS": by_type[t]["pass"] += 1
            
        f.write("| Type | Total | Passed | Failed | Rate |\n")
        f.write("|------|-------|--------|--------|------|\n")
        for t, stats in by_type.items():
            p = stats['pass']
            tot = stats['total']
            fail = tot - p
            r = (p/tot)*100 if tot > 0 else 0
            f.write(f"| {t} | {tot} | {p} | {fail} | {r:.1f}% |\n")
        
        f.write("\n## Failed Test Cases\n")
        f.write("| ID | Lang | Query | Expected | Response |\n")
        f.write("|----|------|-------|----------|----------|\n")
        
        for r in results:
            if r['status'] == "FAIL":
                r_text = str(r['actual_response']).replace('\n', ' ')[:50]
                expect = str(r['expected_ids'])
                f.write(f"| {r['id']} | {r['lang']} | {r['query']} | {expect} | {r_text} |\n")

    print(f"Report generated: {filename}")

if __name__ == "__main__":
    run_comprehensive_tests()
