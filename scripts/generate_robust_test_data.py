import json
import os
import itertools
import random

# Use the full path for the data files
KB_PATH = r"c:\Users\DELL\Downloads\ZeroKost\Robot_code\6.1_update_code\6.1_update_code\data\hospital_knowledge_base.json"
OUTPUT_PATH = r"c:\Users\DELL\Downloads\ZeroKost\Robot_code\6.1_update_code\6.1_update_code\data\robust_acoustic_test_data.json"

def generate_variations():
    print("Loading Knowledge Base...")
    try:
        with open(KB_PATH, 'r', encoding='utf-8') as f:
            kb = json.load(f)
    except Exception as e:
        print(f"Error loading KB: {e}")
        return

    # Base templates for generating 15+ variations per keyword
    templates = {
        "en": [
            "I have a {kw}.",
            "I'm suffering from {kw}.",
            "Where do I go for {kw}?",
            "Which department handles {kw}?",
            "My friend has {kw}, where is the doctor?",
            "Can you help me with {kw}?",
            "I need treatment for {kw}.",
            "Tell me the direction for {kw} department.",
            "I am experiencing severe {kw} right now.",
            "Is there a specialist for {kw} here?",
            "Please guide me to the {kw} ward.",
            "Who treats {kw} in this hospital?",
            "I've been dealing with {kw} since yesterday.",
            "Show me the way to {kw} doctor.",
            "I want to check my {kw}."
        ],
        "hi": [
            "मुझे {kw} है।",
            "मैं {kw} से परेशान हूँ।",
            "मुझे {kw} के लिए कहाँ जाना चाहिए?",
            "कौन सा विभाग {kw} देखता है?",
            "मेरे दोस्त को {kw} है, डॉक्टर कहाँ है?",
            "क्या आप {kw} में मेरी मदद कर सकते हैं?",
            "मुझे {kw} का इलाज चाहिए।",
            "कृपया {kw} विभाग का रास्ता बताएं।",
            "मुझे अभी बहुत तेज {kw} हो रहा है।",
            "क्या यहाँ {kw} का कोई विशेषज्ञ है?",
            "कृपया मुझे {kw} वार्ड का रास्ता दिखाएं।",
            "इस अस्पताल में {kw} का इलाज कौन करता है?",
            "मुझे कल से {kw} की शिकायत है।",
            "मुझे {kw} वाले डॉक्टर के पास जाना है।",
            "मुझे अपनी {kw} की जांच करवानी है।"
        ],
        "te": [
            "నాకు {kw} ఉంది.",
            "నేను {kw} తో బాధపడుతున్నాను.",
            "నేను {kw} కోసం ఎక్కడికి వెళ్ళాలి?",
            "ఏ విభాగం {kw} చూస్తుంది?",
            "నా స్నేహితుడికి {kw} ఉంది, డాక్టర్ ఎక్కడ?",
            "మీరు నాకు {kw} తో సహాయం చేయగలరా?",
            "నాకు {kw} కి చికిత్స కావాలి.",
            "దయచేసి {kw} విభాగానికి దారి చెప్పండి.",
            "నాకు ఇప్పుడు తీవ్రమైన {kw} వస్తోంది.",
            "ఇక్కడ {kw} నిపుణుడు ఉన్నారా?",
            "దయచేసి నాకు {kw} వార్డ్ కి దారి చూపించండి.",
            "ఈ ఆసుపత్రిలో {kw} కి ఎవరు చికిత్స చేస్తారు?",
            "నిన్నటి నుండి నాకు {kw} సమస్యగా ఉంది.",
            "నాకు {kw} గురిచి డాక్టర్ కి చూపించండి.",
            "నేను నా {kw} ని చెక్ చేయించుకోవాలి."
        ]
    }

    test_data = []
    test_id_counter = 1000

    print("Generating Variations...")
    for dept in kb.get('departments', []):
        cname = dept.get('canonical_name', '')
        # Only target a few key departments and their core symptoms to avoid millions of rows
        if cname not in ["General Medicine", "Cardiology Unit-1", "Medical Gastroenterology", "Orthopaedics"]:
            continue

        keywords = dept.get('keywords', {})
        
        for lang, kws in keywords.items():
            if lang not in templates: continue
            
            # Select 3 core keywords per department per language to explode
            core_kws = kws[:3] 
            
            for kw in core_kws:
                for template in templates[lang]:
                    variation_text = template.replace("{kw}", kw)
                    test_case = {
                        "id": f"TEST_{lang.upper()}_{test_id_counter}",
                        "lang": lang,
                        "text": variation_text,
                        "expected_department": cname,
                        "category": "direct_symptom"
                    }
                    test_data.append(test_case)
                    test_id_counter += 1

    # Add False Positive / Unknown queries to ensure fallback logic holds
    unknown_queries = [
        {"id": "TEST_EN_UNKNOWN_1", "lang": "en", "text": "Where is the nearest cinema?", "expected_department": None, "category": "fallback"},
        {"id": "TEST_EN_UNKNOWN_2", "lang": "en", "text": "Who is the prime minister of India?", "expected_department": None, "category": "fallback"},
        {"id": "TEST_HI_UNKNOWN_1", "lang": "hi", "text": "ताजमहल कहाँ है?", "expected_department": None, "category": "fallback"},
        {"id": "TEST_TE_UNKNOWN_1", "lang": "te", "text": "సినిమా టికెట్లు ఎక్కడ దొరుకుతాయి?", "expected_department": None, "category": "fallback"}
    ]
    test_data.extend(unknown_queries)

    print(f"Total Variations Generated: {len(test_data)}")

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully saved robust test dataset to: {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_variations()
