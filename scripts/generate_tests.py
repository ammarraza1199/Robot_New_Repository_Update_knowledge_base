
import json
import random
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

# Templates for natural language generation
TEMPLATES = {
    "en": {
        "simple": ["Where is {kw}?", "{kw} location", "I need {kw}", "{kw} please"],
        "long": [
            "Hello, I have been suffering from {kw} for a few days, where should I go?",
            "Can you please tell me the way to {kw}, I am new here.",
            "I need to consult a doctor for {kw}, please guide me.",
            "Is there any specialist for {kw} available right now?"
        ],
        "noise": ["uh... {kw}", "{kw}...", "umm {kw} please"]
    },
    "hi": {
        "simple": ["{kw} कहां है?", "{kw} जाना है", "{kw} के लिए रास्ता", "{kw} किधर है"],
        "long": [
            "नमस्ते, मुझे {kw} की समस्या है, कृपया बताएं कहां जाना है?",
            "मेरे पिताजी को {kw} है, डॉक्टर कहां मिलेंगे?",
            "क्या आप मुझे {kw} का रास्ता बता सकते हैं?",
            "मुझे {kw} के लिए अपॉइंटमेंट चाहिए।"
        ],
        "noise": ["जी {kw}", "{kw} चाहिए", "अरे {kw} किधर है"]
    },
    "te": {
        "simple": ["{kw} ఎక్కడ ఉంది?", "{kw} కి దారి", "{kw} వెళ్ళాలి", "{kw} ఉందా?"],
        "long": [
            "నమస్కారం, నాకు {kw} సమస్య ఉంది, ఎక్కడికి వెళ్ళాలి?",
            "మా అమ్మగారికి {kw} ఉంది, ఏ డాక్టర్ ని కలవాలి?",
            "దయచేసి {kw} వైపు వెళ్ళే దారి చెప్పండి.",
            "ఇక్కడ {kw} డాక్టర్ అందుబాటులో ఉన్నారా?"
        ],
        "noise": ["అది {kw}", "{kw} అండి", "{kw} కావాలి"]
    }
}

def load_kb():
    kb_path = os.path.join(ROOT_DIR, 'hospital_knowledge_base.json')
    with open(kb_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_test_cases():
    kb = load_kb()
    tests = []
    
    # 1. Departments
    for dept in kb.get("departments", []):
        dept_id = dept['id']
        expected = [dept_id]
        
        # Checking redirects/aliases logic
        # For this test, we expect the NLU to identify the *intended* department or the redirect target.
        # But strictly speaking, the NLU returns the department ID matching the keyword.
        
        for lang in ['en', 'hi', 'te']:
            keywords = dept.get("keywords", {}).get(lang, [])
            # Limit to top 3 keywords per lang to avoid explosion
            for kw in keywords[:3]:
                if len(kw) < 3: continue 
                
                # 1. Exact Keyword
                tests.append({
                    "id": f"dept_{dept_id}_{lang}_exact",
                    "text": kw,
                    "lang": lang,
                    "expected_ids": expected,
                    "type": "Exact"
                })
                
                # 2. Simple Sentence
                tmpl = random.choice(TEMPLATES[lang]["simple"])
                tests.append({
                    "id": f"dept_{dept_id}_{lang}_simple",
                    "text": tmpl.format(kw=kw),
                    "lang": lang,
                    "expected_ids": expected,
                    "type": "Simple"
                })
                
                # 3. Long/Complex - Sampled to avoid explosion (1 in 3 chance per keyword)
                if random.random() < 0.33:
                    tmpl = random.choice(TEMPLATES[lang]["long"])
                    tests.append({
                        "id": f"dept_{dept_id}_{lang}_long",
                        "text": tmpl.format(kw=kw),
                        "lang": lang,
                        "expected_ids": expected,
                        "type": "Long"
                    })

    # 2. Interactions
    for item in kb.get("interactions", []):
        item_id = item['id']
        # Interactions return text answers, not Dept IDs. 
        # But our NLU logic might return the item ID or content. 
        # In this mock, we assume the test runner checks if the response != "I do not have info".
        # We will store expected_id as the INTERACTION ID for validation.
        
        for lang in ['en', 'hi', 'te']:
            keywords = item.get("keywords", {}).get(lang, [])
            for kw in keywords:
                # Interaction matching is often exact or strict substring
                tests.append({
                    "id": f"int_{item_id}_{lang}",
                    "text": kw,
                    "lang": lang,
                    "expected_ids": [item_id], 
                    "type": "Interaction"
                })
                # Attempt a simple sentence wrapper for interactions too
                if lang in TEMPLATES and random.random() < 0.5:
                     tmpl = random.choice(TEMPLATES[lang]["noise"]) # Use noise/short wrappers for interactions
                     tests.append({
                        "id": f"int_{item_id}_{lang}_noise",
                        "text": tmpl.format(kw=kw),
                        "lang": lang,
                        "expected_ids": [item_id],
                        "type": "Interaction+Noise"
                    })

    # 3. Services / Diagnostics
    for service in kb.get("services", []):
        service_id = service['id']
        # We need to map service to Dept ID if possible, but let's just track it triggers SOMETHING found
        keywords = service.get("keywords", [])
        for kw in keywords:
             tests.append({
                    "id": f"serv_{service_id}_en", # Services mainly En keywords in JSON?
                    "text": f"Where is {kw}?",
                    "lang": "en",
                    "expected_ids": ["SERVICE_MATCH"], # Placeholder
                    "type": "Service"
                })

    # 4. Medical Advice Scenarios (Should be refused)
    medical_queries = {
        "en": [
            "What medicine should I take for fever?",
            "Treat my headache",
            "Diagnose my stomach pain",
            "suggest causes for vomiting",
            "I need medicine for high bp", # careful, 'medicine' might trigger pharmacy, but sentence structure matters? 
                                          # 'medicine' is a keyword for pharmacy. 
                                          # However, 'need medicine' -> pharmacy.
                                          # 'what medicine should i take' -> medical advice.
                                          # let's stick to 'treatment', 'causes' which are in is_medical_query list
            "What are the causes of cancer?",
            "give me treatment for cold"
        ],
        "hi": [
            "मुझे बुखार के लिए कौन सी दवा लेनी चाहिए?",
            "मेरे सिरदर्द का इलाज करें",
            "पेट दर्द का निदान करें",
            "उल्टी के कारण बताएं", 
            "कैंसर के कारण क्या हैं?"
        ],
        "te": [
            "జ్వరానికి నేను ఏ మందు వాడాలి?",
            "నా తలనొప్పికి చికిత్స చేయండి",
            "పొత్తికడుపు నొప్పిని నిర్ధారించండి",
            "వాంతులు కావడానికి కారణాలు చెప్పండి",
            "క్యాన్సర్ రావడానికి కారణాలు ఏమిటి?"
        ]
    }
    
    for lang, queries in medical_queries.items():
        for i, q in enumerate(queries):
            tests.append({
                "id": f"medical_advice_{lang}_{i}",
                "text": q,
                "lang": lang,
                "expected_ids": ["MEDICAL_ADVICE_REFUSAL"],
                "type": "MedicalAdvice"
            })

    # 5. Out of Scope / Fallback Scenarios
    fallback_queries = {
        "en": ["Where is the nearest cinema?", "Who is the prime minister?", "askldfjasldkf", "blabla random text"],
        "hi": ["सिनेमा हॉल कहाँ है?", "प्रधानमंत्री कौन है?", "अबजडफ"],
        "te": ["సినిమా హాల్ ఎక్కడ ఉంది?", "ముఖ్యమంత్రి ఎవరు?", "అచ్చట ముచ్చట"]
    }

    for lang, queries in fallback_queries.items():
        for i, q in enumerate(queries):
             tests.append({
                "id": f"fallback_{lang}_{i}",
                "text": q,
                "lang": lang,
                "expected_ids": ["FALLBACK_RESPONSE"],
                "type": "Fallback"
            })

    print(f"Generated {len(tests)} test cases.")
    data_path = os.path.join(SCRIPT_DIR, 'comprehensive_test_data.json')
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(tests, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    generate_test_cases()
