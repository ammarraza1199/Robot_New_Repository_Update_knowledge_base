import json
import os

KB_PATH = "hospital_knowledge_base.json"
RESULT_FILE = "load_result.txt"

def test_loading():
    try:
        with open(KB_PATH, "r", encoding="utf-8") as f:
            kb = json.load(f)
        
        departments = kb.get("departments", [])
        interactions = kb.get("interactions", [])
        
        found_dept = False
        neuro_entry = None
        
        with open(RESULT_FILE, "w", encoding="utf-8") as out:
            out.write(f"Departments count: {len(departments)}\n")
            
            for dept in departments:
                if dept.get("canonical_name") == "Neurology":
                    found_dept = True
                    neuro_entry = dept
                    out.write(f"Neurology FOUND in departments list.\n")
                    break
            
            if not found_dept:
                out.write("Neurology NOT FOUND in departments list.\n")
            else:
                out.write(f"Neurology keywords (en): {neuro_entry.get('keywords', {}).get('en')}\n")

    except Exception as e:
        with open(RESULT_FILE, "w", encoding="utf-8") as out:
            out.write(f"CRASH: {e}\n")

if __name__ == "__main__":
    test_loading()
