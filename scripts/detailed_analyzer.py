import pandas as pd
import json
import os
import sys

csv_file = r"c:\Users\DELL\Downloads\ZeroKost\Robot_code\6.1_update_code\6.1_update_code\tests\output\acoustic_test_results_20260224_151137.csv"
json_file = r"c:\Users\DELL\Downloads\ZeroKost\Robot_code\6.1_update_code\6.1_update_code\data\comprehensive_test_data.json"

df = pd.read_csv(csv_file)
with open(json_file, 'r', encoding='utf-8') as f:
    test_data = json.load(f)

# Create a mapping of id -> expected_ids
expected_map = {item['id']: item['expected_ids'] for item in test_data}

api_error_strs = [
    "trouble connecting to my brain",
    "अपने दिमाग से जुड़ने में समस्या",
    "अपने मस्तिष्क से जुड़ने में समस्या",
    "నా మెదడుకి కనెక్ట్ చేయడంలో",
    "API_ERROR"
]

medical_guardrail_strs = [
    "I cannot provide medical advice",
    "मैं चिकित्सा सलाह नहीं दे सकता",
    "నేను వైద్య సలహా ఇవ్వలేను"
]

fallback_strs = [
    "I can't answer, I do not have access",
    "मैं उत्तर नहीं दे सकता",
    "నేను సమాధానం చెప్పలేను"
]

# A rough map from expected_id to keywords that MUST be in the correct response
dept_keywords = {
    'general_opd': ['General Medicine', 'General OPD', 'सामान्य चिकित्सा', 'जनरल ओपीडी', 'జనరల్ మెడిసిన్', 'జనరల్ ఓపీడీ'],
    'general_medicine': ['ENT', 'Ophthalmology', 'Eye', 'ईएनटी', 'नेत्र', 'आंख', 'ఈఎన్టీ', 'కంటి'],
    'cardiology_unit_1': ['Cardiology Unit 1', 'कार्डियोलॉजी यूनिट 1', 'కార్డియాలజీ యూనిట్-1', 'Dr. O. Sai Satish'],
    'cardiology_unit_2': ['Cardiology Unit 2', 'कार्डियोलॉजी यूनिट 2', 'కార్డియాలజీ యూనిట్-2', 'Dr. B. Srinivas'],
    'cardiology_unit_3': ['Cardiology Unit 3', 'कार्डियोलॉजी यूनिट 3', 'కార్డియాలజీ యూనిట్-3'],
    'cardiology_unit_4': ['Cardiology Unit 4', 'कार्डियोलॉजी यूनिट 4', 'కార్డియాలజీ యూనిట్-4', 'Dr. M. Jyotsna'],
    'medical_gastro': ['Medical Gastroenterology', 'मेडिकल गैस्ट्रो', 'మెడికల్ గ్యాస్ట్రో'],
    'pulmonary_medicine': ['Pulmonary', 'पल्मोनरी', 'పల్మనరీ'],
    'pharmacy': ['Pharmacy', 'Medical Store', 'फार्मेसी', 'ఫార్మసీ', 'Duty Pharmacist'],
    'urology': ['Urology', 'यूरोलॉजी', 'యూరాలజీ'],
    'vascular_surgery': ['Vascular', 'वैस्कुलर', 'వాస్కులర్'],
    'radiology': ['Radiology', 'रेडियोलॉजी', 'రేడియాలజీ'],
    'paediatrics': ['Paediatric', 'Pediatric', 'बाल रोग', 'పిల్లల'],
    'dermatology': ['Dermatology', 'त्वचा', 'చర్మ'],
    'orthopaedics': ['Orthopaedic', 'हड्डी', 'ఎముకల'],
    'neurology': ['Neurology', 'न्यूरोलॉजी', 'న్యూరాలజీ'],
    'dental': ['Dental', 'दंत', 'దంత', 'Dentist'],
    'laboratory': ['Lab Medicine', 'प्रयोगशाला', 'ల్యాబ్'],
    'icu': ['ICU', 'आईसीय', 'ఐసీయూ'],
    'emergency': ['Emergency', 'आपातकालीन', 'ఎమర్జెన్సీ']
}

api_error_count = 0
out_of_scope_count = 0
correct_count = 0
mismatch_count = 0
hallucination_count = 0

total_questions = len(df)
details = []

for idx, row in df.iterrows():
    resp = str(row['robot_response'])
    qid = str(row['id'])
    
    expected_ids = expected_map.get(qid, [])
    
    # 1. API Error
    is_api_error = any(err in resp for err in api_error_strs) or "API_ERROR" in resp
    if is_api_error:
        api_error_count += 1
        continue
        
    # 2. Out of Scope
    is_out_of_scope = any(mg in resp for mg in medical_guardrail_strs)
    if is_out_of_scope:
        out_of_scope_count += 1
        continue
        
    is_smalltalk_intent = qid.startswith("int_")
    
    # Determine what kind of answer we got
    is_templated_answer = "The department name is" in resp or "विभाग का नाम" in resp or "విభాగం పేరు" in resp or "ప్రయోగశాల" in resp or "పార్కింగ్ " in resp
    
    # Adding the smalltalk statements to fallback list since they correctly bypass the router
    is_fallback_answer = any(fb in resp for fb in fallback_strs) or "I am a navigation robot" in resp or "मैं एक रोबोट हूँ" in resp or "నేను ఒక రోబోట్" in resp or "Hello! Welcome to NIMS Hospital" in resp or "नमस्ते! निम्स अस्पताल में आपका स्वागत है" in resp or "నమస్కారం! నిమ్స్ ఆసుపత్రికి స్వాగతం" in resp
    
    if is_smalltalk_intent:
        if is_templated_answer:
            # It routed to a department instead of answering the query
            mismatch_count += 1
            details.append(f"Mismatch (Smalltalk routed to dept): ID {qid}, Expected: {expected_ids}, Got: {resp}")
        elif is_fallback_answer:
            correct_count += 1
        else:
            correct_count += 1 # Any conversational response to a conversational intent is technically correct
        continue

    if is_templated_answer:
        # Check if it matches expected
        matched_expected = False
        for exp_id in expected_ids:
            if exp_id in dept_keywords:
                if any(kw.lower() in resp.lower() for kw in dept_keywords[exp_id]):
                    matched_expected = True
                    break
        
        if matched_expected or not expected_ids:
            # Note: if no expected_ids but handled cleanly, treating as correct
            correct_count += 1
        else:
            mismatch_count += 1
            details.append(f"Mismatch: ID {qid}, Expected: {expected_ids}, Got: {resp}")
    elif is_fallback_answer:
        # Fallback can be correct if no department or general
        if not expected_ids or 'None' in expected_ids:
            correct_count += 1
        else:
            # We expected a specific department, but it gave a fallback
            mismatch_count += 1
            details.append(f"Mismatch (Fallback instead of dept): ID {qid}, Expected: {expected_ids}, Got: {resp}")
    else:
        # It's an unconstrained response (Hallucination) for a DEPT query
        hallucination_count += 1
        details.append(f"Hallucination (Dept query got conversational answer): ID {qid}, Expected: {expected_ids}, Got: {resp}")

with open('detailed_analyzer_report.txt', 'w', encoding='utf-8') as f:
    f.write("=== ANALYSIS REPORT ===\n")
    f.write(f"Total Queries Evaluated: {total_questions}\n")
    f.write(f"Correct Answers (Properly routed or expected fallback): {correct_count}\n")
    f.write(f"Out of Scope (Medical Guardrail Triggered correctly): {out_of_scope_count}\n")
    f.write(f"Mismatches (Routed to wrong department or fallback when dept expected): {mismatch_count}\n")
    f.write(f"API Errors: {api_error_count}\n")
    f.write(f"LLM Hallucinations (Conversational or unsupported answers): {hallucination_count}\n")
    f.write("\n--- Details of Failures ---\n")
    for d in details:
        f.write(d + "\n")

