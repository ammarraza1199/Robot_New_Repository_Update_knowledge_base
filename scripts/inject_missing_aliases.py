import json
import os
import shutil
import unicodedata

def normalize_text(text):
    if isinstance(text, str):
        return unicodedata.normalize('NFC', text).lower().strip()
    return text

INJECTIONS = [
    {"id": "cardiology_unit_1", "lang": "te", "phrases": ["ఛాతీలో బిగుతుగా ఉండటం"]},
    {"id": "cardiology_unit_2", "lang": "hi", "phrases": ["धड़कन बढ़ना"]},
    {"id": "cardiology_unit_2", "lang": "te", "phrases": ["శ్వాస బరువుగా వుంది"]},
    {"id": "ent", "lang": "en", "phrases": ["otorhinolaryngology"]},
    {"id": "ent", "lang": "hi", "phrases": ["गला"]},
    {"id": "general_medicine", "lang": "te", "phrases": ["చలి"]},
    # "కంటి శాస్త్ర విభాగము" (Eye Dept) should be Ophthalmology, not Gen Med
    {"id": "ophthalmology", "lang": "te", "phrases": ["కంటి శాస్త్ర విభాగము"]}, 
    {"id": "general_opd", "lang": "en", "phrases": ["psychiatry", "homoeopathy", "ayurveda"]},
    {"id": "general_opd", "lang": "hi", "phrases": ["डॉक्टर को दिखाना है"]},
    {"id": "general_opd", "lang": "te", "phrases": ["సలహా కోసం"]},
    {"id": "medical_gastro", "lang": "hi", "phrases": ["बार-बार उल्टी होना"]},
    # Re-mapped "Blood in stool" to Gastro (was failing as expected Lab in test, but Gastro is medically correct)
    {"id": "medical_gastro", "lang": "te", "phrases": ["మలం లో రక్తం"]}, 
    {"id": "ophthalmology", "lang": "hi", "phrases": ["दिखाई नहीं दे रहा"]},
    {"id": "pharmacy", "lang": "hi", "phrases": ["दवा"]},
    {"id": "pulmonary_medicine", "lang": "hi", "phrases": ["दमा", "फेफड़ों की बीमारी"]},
    {"id": "pulmonary_medicine", "lang": "te", "phrases": ["శ్వాస తీసుకోవడంలో ఇబ్బంది", "కఫం"]},
    {"id": "urology", "lang": "te", "phrases": ["మూత్ర విసర్జనలో ఇబ్బంది"]},
    {"id": "vascular_surgery", "lang": "hi", "phrases": ["पैर में घाव जो ठीक न हो", "पैर में खून का थक्का"]},
    {"id": "vascular_surgery", "lang": "te", "phrases": ["మానని పాదాల పుండు", "పాదాల పుండు"]}
]

def inject_aliases():
    kb_path = "hospital_knowledge_base.json"
    backup_path = "hospital_knowledge_base.json.bak_inject"
    
    if not os.path.exists(backup_path):
        shutil.copy(kb_path, backup_path)
        print(f"Backed up KB to {backup_path}")

    with open(kb_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    count = 0
    for injection in INJECTIONS:
        target_id = injection["id"]
        lang = injection["lang"]
        phrases = injection["phrases"]
        
        # Find Dept
        found = False
        for dept in data.get("departments", []):
            if dept["id"] == target_id:
                found = True
                if "keywords" not in dept:
                    dept["keywords"] = {}
                if lang not in dept["keywords"]:
                    dept["keywords"][lang] = []
                
                current_keywords = dept["keywords"][lang]
                # Add only if not present (normalized check)
                norm_current = set(normalize_text(k) for k in current_keywords)
                
                for p in phrases:
                    if normalize_text(p) not in norm_current:
                        current_keywords.append(p)
                        print(f"Injected [{target_id}][{lang}]: {p}")
                        count += 1
                    else:
                        print(f"Skipped [{target_id}][{lang}]: {p} (Already exists)")
                break
        
        if not found:
            print(f"WARNING: Target department '{target_id}' not found!")

    with open(kb_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"\nInjection Complete. Added {count} new keywords.")

if __name__ == "__main__":
    inject_aliases()
