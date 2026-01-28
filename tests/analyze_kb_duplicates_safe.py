import json
import os
from collections import defaultdict

def analyze_duplicates_safe():
    kb_path = "hospital_knowledge_base.json"
    output_path = "kb_duplicates_report_safe.txt"
    
    try:
        with open(kb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading KB: {e}")
        return

    # Store keywords: keyword -> list of (source_type, source_id, lang)
    keyword_map = defaultdict(list)

    # 1. Departments
    print("Scanning Departments...")
    for dept in data.get("departments", []):
        dept_id = dept["id"]
        if "keywords" in dept:
            for lang, kws in dept["keywords"].items():
                for kw in kws:
                    keyword_map[kw.lower().strip()].append(f"Department: {dept_id} ({lang})")
        if "aliases" in dept:
            for alias in dept["aliases"]:
                keyword_map[alias.lower().strip()].append(f"Department Alias: {dept_id}")

    # 2. Interactions
    print("Scanning Interactions...")
    for interaction in data.get("interactions", []):
        int_id = interaction["id"]
        if "keywords" in interaction:
            for lang, kws in interaction["keywords"].items():
                for kw in kws:
                    keyword_map[kw.lower().strip()].append(f"Interaction: {int_id} ({lang})")

    # 3. Find Collisions
    # A collision is real if the SAME keyword maps to DIFFERENT IDs.
    # If "fever" maps to "General OPD" (hi) and "General OPD" (te), that is NOT a collision.
    # If "fever" maps to "General OPD" and "General Medicine", that IS a collision.

    real_collisions = {}

    for kw, sources in keyword_map.items():
        # extract unique IDs
        unique_ids = set()
        for s in sources:
            # "Department: general_opd (hi)" -> "general_opd"
            # "Department Alias: general_opd" -> "general_opd"
            # "Interaction: greeting (en)" -> "greeting"
            if ": " in s:
                id_part = s.split(": ")[1].split(" (")[0]
                unique_ids.add(id_part)
            else:
                unique_ids.add(s)
        
        if len(unique_ids) > 1:
            real_collisions[kw] = sources

    print(f"Found {len(real_collisions)} overlapping keywords.")

    # Write report directly to file with utf-8
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("-" * 80 + "\n")
        f.write(f"{'KEYWORD':<30} | {'OCCURRENCES'}\n")
        f.write("-" * 80 + "\n")
        
        for kw, sources in sorted(real_collisions.items()):
            line = f"{kw:<30} | {', '.join(sources)}\n"
            f.write(line)

    print(f"Report saved to {output_path}")

if __name__ == "__main__":
    analyze_duplicates_safe()
