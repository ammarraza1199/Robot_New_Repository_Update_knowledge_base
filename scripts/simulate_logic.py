import json
import re
import difflib

# 1. Mock Data from JSON (Simplified)
# We replicate the state after loading JSON
departments = [
    {"canonical_name": "General Medicine", "keywords": {"en": ["back ache", "eye"]}},
    {"canonical_name": "Ophthalmology", "keywords": {"en": ["eye", "ophthalmology"]}},
    {"canonical_name": "Orthopaedics", "keywords": {"en": ["back ache", "orthopedics"]}}
]

interactions = [] # Mock empty

# 2. Mock Logic from interaction_process.py
REDIRECT_DEPARTMENTS = {
    "ophthalmology": "general_medicine",
    "eye": "general_medicine",
    "ent": "general_medicine"
}

keyword_index = {"en": {}}
department_map = {}

# Load Data (Simulation)
# Note: In real app, departments are loaded from list. List order matters.
# JSON list order: General Medicine is usually first. Ophthalmology/Orthopaedics are usually last.
for d in departments:
    cname = d["canonical_name"]
    department_map[cname] = d
    for lang, kws in d.get("keywords", {}).items():
        for kw in kws:
            keyword_index[lang][kw.lower()] = cname

def find_department(user_text, lang="en"):
    user_text = user_text.lower()
    
    best_match_dept = None
    longest_match_len = 0
    
    # Keyword Search
    if lang in keyword_index:
        for kw, dept_cname in keyword_index[lang].items():
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, user_text, re.IGNORECASE):
                if len(kw) > longest_match_len:
                    longest_match_len = len(kw)
                    best_match_dept = dept_cname

    if best_match_dept:
        print(f"  [Match Found] Keyword: '{user_text}' -> Dept: '{best_match_dept}'")
        dept_cname_lower = best_match_dept.lower()
        if dept_cname_lower in REDIRECT_DEPARTMENTS:
            redirected = REDIRECT_DEPARTMENTS[dept_cname_lower]
            print(f"  [Redirect Triggered] '{best_match_dept}' -> '{redirected}'")
            return redirected
        return best_match_dept
    
    return None

# 3. Test Cases
inputs = [
    "I have back ache",
    "Where is ophthalmology",
    "I have eye pain"
]

print("--- Simulation Start ---")
for text in inputs:
    print(f"Input: '{text}'")
    result = find_department(text)
    print(f"Result: {result}\n")
