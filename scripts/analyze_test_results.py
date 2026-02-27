
import csv
import json
import re
import sys
from collections import defaultdict

# Configure stdout for UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def load_kb_departments(kb_path):
    try:
        with open(kb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # data['departments'] is a list of dicts
            departments = set()
            for dept in data.get('departments', []):
                departments.add(dept.get('id', '').lower())
                departments.add(dept.get('canonical_name', '').lower())
                # Add check keywords if needed
            return departments
    except Exception as e:
        print(f"Error loading KB: {e}")
        return set()

def normalize_text(text):
    if not text:
        return ""
    # Remove punctuation but keep characters from all languages
    # This regex keeps alphanumeric characters from any language (including Hindi/Telugu)
    # and spaces.
    return re.sub(r'[^\w\s]', ' ', text.lower())

def analyze_results(csv_path, kb_path):
    print(f"Analyzing {csv_path}...")
    
    stats = {
        "total": 0,
        "correct": 0,
        "api_failure": 0,
        "safe_fallback": 0,
        "hallucination": 0, 
        "lang_stats": defaultdict(lambda: {"total": 0, "correct": 0, "failure": 0})
    }
    
    hallucination_examples = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                stats["total"] += 1
                test_id = row['id']
                lang = row['language']
                response = row['robot_response']
                question = row['question_text_orig']
                
                stats["lang_stats"][lang]["total"] += 1

                # Check for API Failure
                if "trouble connecting" in response or "connection error" in response.lower():
                    stats["api_failure"] += 1
                    stats["lang_stats"][lang]["failure"] += 1
                    continue

                # Check for Safe Fallback
                if "cannot provide medical advice" in response or "consult a doctor" in response.lower():
                    stats["safe_fallback"] += 1
                    # Treat safe fallback as Correct for analysis stats? 
                    # User asked for "correct", usually implies "gave the right answer".
                    # But for "body pain", "consult a doctor" IS the right answer if not specific.
                    # Let's count it as correct for stats, but track it separately too.
                    stats["correct"] += 1
                    stats["lang_stats"][lang]["correct"] += 1
                    continue

                # Determine expected department from ID
                expected_dept_key = ""
                if "general_opd" in test_id or "general_medicine" in test_id:
                    expected_dept_key = "general"
                elif "cardiology" in test_id:
                    expected_dept_key = "cardio"
                elif "orthopaedics" in test_id:
                    expected_dept_key = "ortho" # orthopedics, spine
                elif "neurology" in test_id:
                    expected_dept_key = "neuro"
                elif "gastro" in test_id:
                    expected_dept_key = "gastro"
                elif "dermatology" in test_id:
                    expected_dept_key = "derma" # skin
                elif "urology" in test_id:
                    expected_dept_key = "uro"
                elif "ent" in test_id:
                    expected_dept_key = "ent"
                elif "paediatrics" in test_id:
                    expected_dept_key = "paed" # pediatric, child
                elif "pulmonary" in test_id:
                    expected_dept_key = "pulm" # lung, respiratory
                elif "radiology" in test_id:
                    expected_dept_key = "radio" # x-ray, scan
                elif "pharmacy" in test_id:
                    expected_dept_key = "pharm"
                elif "vascular" in test_id:
                    expected_dept_key = "vascular"
                elif "ophthalmology" in test_id:
                    expected_dept_key = "opthal"
                elif "greet" in test_id:
                     expected_dept_key = "greet"

                # Check correctness
                normalized_resp = normalize_text(response)
                is_correct = False
                
                # Multilingual Keywords
                if expected_dept_key == "general":
                    keywords = [
                        "general", "emergency", "medicine", "opd", "physician", "doctor",
                        "समान्य", "इमरजेंसी", "चिकित्सा", "ओपीडी", "डाक्टर", "आपातकालीन",
                        "జనరల్", "ఎమర్జెన్సీ", "వైద్య", "ఓపీడీ", "డాక్టర్", "అత్యవసర"
                    ]
                    if any(x in normalized_resp for x in keywords): is_correct = True

                elif expected_dept_key == "cardio":
                    keywords = [
                        "cardio", "heart", "cardiac",
                        "हृदय", "दिल", "कार्डियो", 
                        "గుండె", "కార్డియాలజీ", "హృదయ"
                    ]
                    if any(x in normalized_resp for x in keywords): is_correct = True

                elif expected_dept_key == "ortho":
                    keywords = [
                        "ortho", "bone", "spine", "joint", "fracture",
                        "हड्डी", "जोड़", "ऑर्थो", "स्पाइन",
                        "ఎముక", "కీళ్ళ", "ఆర్థో", "స్పైన్"
                    ]
                    if any(x in normalized_resp for x in keywords): is_correct = True

                elif expected_dept_key == "neuro":
                    keywords = [
                        "neuro", "brain", "mental", "nerve",
                        "न्यूरो", "दिमाग", "मस्तिष्क", "नस",
                        "న్యూరో", "మెదడు", "నరాల"
                    ]
                    if any(x in normalized_resp for x in keywords): is_correct = True

                elif expected_dept_key == "gastro":
                    keywords = [
                        "gastro", "stomach", "liver", "digestive",
                        "गैस्ट्रो", "पेट", "liver", "पाचन",
                        "గ్యాస్ట్రో", "కడుపు", "జీర్ణ"
                    ]
                    if any(x in normalized_resp for x in keywords): is_correct = True

                elif expected_dept_key == "derma":
                    keywords = [
                        "derma", "skin", "rash",
                        "त्वचा", "चर्म", "derma",
                        "చర్మ", "డెర్మా"
                    ]
                    if any(x in normalized_resp for x in keywords): is_correct = True

                elif expected_dept_key == "uro":
                    keywords = [
                        "uro", "urine", "kidney", "renal",
                        "यूरो", "पेशाब", "गुर्दा", "किडनी",
                        "యూరో", "మూత్ర", "కిడ్నీ"
                    ]
                    if any(x in normalized_resp for x in keywords): is_correct = True

                elif expected_dept_key == "ent":
                    keywords = [
                        "ent", "ear", "nose", "throat", "otorhinolaryngology",
                        "ईएनटी", "कान", "नाक", "गदा", "गला",
                        "ఈఎన్టీ", "చెవి", "ముక్కు", "గొంతు"
                    ]
                    if any(x in normalized_resp for x in keywords): is_correct = True

                elif expected_dept_key == "paed":
                    keywords = [
                        "paed", "child", "baby", "infant",
                        "बाल", "बच्चा", "शिशु", "पीडियाट्रिक्स",
                        "పిల్లల", "శిశు", "పీడియాట్రిక్స్"
                    ]
                    if any(x in normalized_resp for x in keywords): is_correct = True

                elif expected_dept_key == "pulm":
                    keywords = [
                        "pulmo", "respiratory", "lung", "chest", "breathing",
                        "फेफड़े", "सांस", "पल्मोनरी", "छाती",
                        "ఊపిరితిత్తుల", "శ్వాస", "పల్మనరీ", "ఛాతీ"
                    ]
                    if any(x in normalized_resp for x in keywords): is_correct = True

                elif expected_dept_key == "radio":
                    keywords = [
                        "radio", "xray", "scan", "imaging", "mri", "ct",
                        "रेडियोलॉजी", "एक्स-रे", "स्कैन",
                        "రేడియాలజీ", "ఎక్స్-రే", "స్కానింగ్"
                    ]
                    if any(x in normalized_resp for x in keywords): is_correct = True

                elif expected_dept_key == "pharm":
                    keywords = [
                        "pharm", "medi", "drug", "store", "chemist",
                        "फार्मेसी", "दवा", "मेडिकल",
                        "ఫార్మసీ", "మందుల", "మెడికల్"
                    ]
                    if any(x in normalized_resp for x in keywords): is_correct = True

                elif expected_dept_key == "vascular":
                    keywords = [
                        "vascular", "vein", "artery",
                        "वास्कुलर", "नस", "रक्त वाहिका",
                        "వాస్క్యులర్", "నరాల" # overlap with neuro but specific enough usually
                    ]
                    if any(x in normalized_resp for x in keywords): is_correct = True

                elif expected_dept_key == "opthal":
                    keywords = [
                        "opthal", "eye", "vision",
                        "नेत्र", "आंख", "दृष्टि",
                        "నేత్ర", "కన్ను"
                    ]
                    if any(x in normalized_resp for x in keywords): is_correct = True

                elif expected_dept_key == "greet":
                     # Greetings usually return lists or welcome messages
                     # Check length or keywords like "welcome", "hospital", "services"
                     keywords = ["welcome", "hospital", "assist", "help", "department", 
                                "स्वागत", "अस्पताल", "मदद", 
                                "స్వాగతం", "ఆసుపత్రి", "సహాయం"]
                     if len(normalized_resp) > 5 or any(x in normalized_resp for x in keywords): is_correct = True

                if is_correct:
                    stats["correct"] += 1
                    stats["lang_stats"][lang]["correct"] += 1
                else:
                    stats["hallucination"] += 1
                    hallucination_examples.append({
                        "id": test_id,
                        "question": question,
                        "response": response,
                        "expected_approx": expected_dept_key
                    })

    except Exception as e:
        print(f"Error processing CSV: {e}")
        return

    print("="*30)
    print("ANALYSIS REPORT")
    print("="*30)
    print(f"Total Questions Processed: {stats['total']}")
    
    # Correct = Explicit Correct + Safe Fallback
    total_correct = stats['correct'] 
    # (Note: I already added safe_fallback to stats['correct'] in the loop)
    
    print(f"Correct Answers (Incl. Safe Fallbacks): {total_correct} ({total_correct/stats['total']*100:.1f}%)")
    print(f"  - Logic/LLM Matches: {total_correct - stats['safe_fallback']}")
    print(f"  - Safe Fallbacks: {stats['safe_fallback']}")
    
    print(f"API Connection Failures: {stats['api_failure']} ({stats['api_failure']/stats['total']*100:.1f}%)")
    print(f"Potential Hallucinations/Mismatches: {stats['hallucination']} ({stats['hallucination']/stats['total']*100:.1f}%)")
    print("-" * 20)
    print("Language Breakdown:")
    for lang in ["en", "hi", "te"]:
        s = stats["lang_stats"].get(lang, {"total": 0, "correct": 0, "failure": 0})
        if s['total'] > 0:
            print(f"  {lang.upper()}: {s['correct']} Correct / {s['failure']} Failed / {s['total']} Total")
    print("-" * 20)
    print("Top 20 Hallucination/Mismatch Examples:")
    for ex in hallucination_examples[:20]:
        print(f"  ID: {ex['id']}")
        print(f"  Q: {ex['question']}")
        print(f"  R: {ex['response']}")
        print(f"  Expected: {ex['expected_approx']}")
        print("  ---")

if __name__ == "__main__":
    analyze_results(
        r"tests/output/acoustic_test_results_20260220_114146.csv",
        r"data/hospital_knowledge_base.json"
    )
