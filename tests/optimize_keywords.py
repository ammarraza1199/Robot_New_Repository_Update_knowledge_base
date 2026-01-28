import json
import os
import re

def clean_te_keyword(kw):
    # Typo corrections
    kw = kw.replace("నిప్పి", "నొప్పి")
    kw = kw.replace("గుండే", "గుండె")
    kw = kw.replace("మంటగవుంది", "మంటగా ఉంది")
    kw = kw.replace("గుంజు తున్నాయ్", "గుంజుతున్నాయి")
    kw = kw.replace("కల్లు తిరగటం", "తల తిరగడం")
    kw = kw.replace("ఆరి చేతులు", "అరి చేతులు")
    
    # Generic cleanup
    kw = kw.strip()
    kw = re.sub(r'\s+', ' ', kw)
    
    return kw

def is_litter(kw):
    litter_patterns = [
        "నిన్నటి నుంచి",
        "ఈరోజు",
        "చాలా",
        "చాలాగా",
        "ఉంది",
        "అవుతున్నాయి",
        "పోయింది",
        "వచ్చింది",
        "వుంది",
        "వుండి",
        "పడ్డాయి",
        "పడుతున్నాయి",
        "కుంటుంది",
        "కుంటున్నాయి",
        "గుంజుతున్నాయి",
        "రావడం",
        "తగ్గట్లేదు",
        "బాగాలేదు",
        "చేసింది",
        "వచ్చింది",
    ]
    
    # Check for litter patterns in the keyword
    for pattern in litter_patterns:
        if pattern in kw:
            # If it's a longer phrase (litter usually isn't in short keywords)
            if len(kw.split()) > 2:
                return True
    
    # Aggressively remove very long sentences
    if len(kw.split()) > 4:
        return True
                
    # Specific filtering for very generic phrases that should be in general_opd or removed
    if kw in ["డాక్టర్", "డాక్టర్ ని చూడాలి", "వైద్యం", "జబ్బు", "చీటీ", "డాక్టర్ కావాలి", "ఓపీ చిటీ"]:
        return "generic"
        
    return False

def optimize_knowledge_base(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for dept in data.get('departments', []):
        dept_id = dept.get('id')
        te_keywords = dept.get('keywords', {}).get('te', [])
        
        cleaned_keywords = []
        seen = set()
        
        for kw in te_keywords:
            cleaned = clean_te_keyword(kw)
            
            litter_check = is_litter(cleaned)
            
            # Special case: generic terms only in general_opd
            if litter_check == "generic" and dept_id != "general_opd":
                continue
            
            if litter_check is True:
                # print(f"Removing litter: {cleaned}")
                continue
                
            if cleaned and cleaned not in seen:
                cleaned_keywords.append(cleaned)
                seen.add(cleaned)
        
        dept['keywords']['te'] = cleaned_keywords

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"Optimized knowledge base saved to: {output_file}")

if __name__ == "__main__":
    optimize_knowledge_base('hospital_knowledge_base_updated.json', 'hospital_knowledge_base_optimized.json')
