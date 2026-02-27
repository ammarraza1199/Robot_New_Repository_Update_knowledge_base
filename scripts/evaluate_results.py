import pandas as pd
import json

RESULTS_CSV = 'tests/output/acoustic_test_results_20260221_212312.csv'
DATA_JSON = 'data/robust_acoustic_test_data.json'

try:
    df = pd.read_csv(RESULTS_CSV)
    
    with open(DATA_JSON, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
        
    expected_map = {item['id']: item.get('expected_department') for item in test_data}
    
    total = len(df)
    correct_count = 0
    api_error_count = 0
    hallucination_count = 0
    fallback_correct_count = 0
    
    fallback_texts = [
        "I can't answer, I do not have access to that information",
        "मैं उत्तर नहीं दे सकता, मेरे पास उस जानकारी तक पहुंच नहीं है",
        "నేను సమాధానం చెప్పలేను, నాకు ఆ సమాచారానికి యాక్సెస్ లేదు"
    ]
    
    for index, row in df.iterrows():
        resp = str(row['robot_response'])
        q_id = row['id']
        expected = expected_map.get(q_id)
        
        # Check API errors
        if "having trouble connecting" in resp or "API_ERROR" in resp:
            api_error_count += 1
            continue
            
        is_fallback = any(fb in resp for fb in fallback_texts)
        
        if expected is None:
            # Out of scope question
            if is_fallback:
                fallback_correct_count += 1
                correct_count += 1
            else:
                # Gave an answer to an out of scope question
                hallucination_count += 1
        else:
            # Expected a department
            if expected.lower() in resp.lower() or (expected == "General Medicine" and "सामान्य चिकित्सा" in resp) or (expected == "General Medicine" and "జనరల్" in resp):
                correct_count += 1
                # Simplified check for now (Assuming match_success could also be used)
            elif is_fallback:
                # Needed a department but fell back
                hallucination_count += 1 # technically not a hallucination but a miss. Let's call it a miss.
                pass
            else:
                # Gave wrong department
                hallucination_count += 1
                
    print(f"Total Questions: {total}")
    print(f"Correct Answers: {correct_count} ({(correct_count/total)*100:.2f}%)")
    print(f"Expected Fallbacks Executed: {fallback_correct_count}")
    print(f"Hallucinations (Wrong Dept or Answered when shouldn't): {hallucination_count} ({(hallucination_count/total)*100:.2f}%)")
    print(f"API Rate Limit Errors: {api_error_count} ({(api_error_count/total)*100:.2f}%)")

except Exception as e:
    print(f"Error: {e}")
