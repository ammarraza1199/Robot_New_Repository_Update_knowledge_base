import json
import collections
import os
import sys

# Force UTF-8 output for Windows console
sys.stdout.reconfigure(encoding='utf-8')

KB_PATH = r"c:/Users/DELL/Downloads/ZeroKost/Robot_code/6.1_update_code/6.1_update_code/data/hospital_knowledge_base.json"

def analyze_kb():
    if not os.path.exists(KB_PATH):
        print(f"Error: File not found at {KB_PATH}")
        return

    with open(KB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    departments = data.get("departments", [])
    print(f"Loaded {len(departments)} departments.\n")

    # 1. List all Departments
    print("--- Department List ---")
    dept_names = []
    for d in departments:
        print(f"ID: {d.get('id')} | Canonical: {d.get('canonical_name')}")
        dept_names.append(d.get('canonical_name'))
    print("\n")

    # 2. Search for Suspicious Terms
    suspicious_terms = ["ophthalmology", "orthopedics", "orthopaedics", "eye", "bone", "opthalmology"]
    print(f"--- Searching for {suspicious_terms} ---")
    
    found = False
    for d in departments:
        d_str = json.dumps(d).lower()
        for term in suspicious_terms:
            if term in d_str:
                print(f"Found '{term}' in Department: {d.get('canonical_name')}")
                # Dig deeper to see where
                if term in d.get('id', '').lower(): print(f"  - In ID")
                if term in d.get('canonical_name', '').lower(): print(f"  - In Canonical Name")
                for lang, kws in d.get('keywords', {}).items():
                    for kw in kws:
                        if term in kw.lower():
                            print(f"  - In Keyword ({lang}): '{kw}'")
                found = True
    
    if not found:
        print("No matches found for suspicious terms in departments.")
    print("\n")

    # 3. Check for Duplicate Keywords
    print("--- Checking for Duplicate Keywords ---")
    # keyword -> [list of departments containing it]
    kw_map = {
        "en": collections.defaultdict(list),
        "hi": collections.defaultdict(list),
        "te": collections.defaultdict(list)
    }

    for d in departments:
        cname = d.get('canonical_name')
        for lang, kws in d.get('keywords', {}).items():
            for kw in kws:
                kw_lower = kw.lower()
                kw_map[lang][kw_lower].append(cname)

    duplicates_found = False
    for lang in kw_map:
        for kw, depts in kw_map[lang].items():
            if len(depts) > 1:
                print(f"[{lang}] Duplicate Keyword '{kw}' found in: {depts}")
                duplicates_found = True

    if not duplicates_found:
        print("No duplicate keywords found.")

if __name__ == "__main__":
    analyze_kb()
