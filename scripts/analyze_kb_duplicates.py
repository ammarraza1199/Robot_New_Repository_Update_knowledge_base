import json
import os
from collections import defaultdict

def analyze_duplicates():
    kb_path = "hospital_knowledge_base.json"
    with open(kb_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Store keywords: keyword -> list of (source_type, source_id, lang)
    keyword_map = defaultdict(list)

    # 1. Departments
    print("Scanning Departments...")
    for dept in data.get("departments", []):
        dept_id = dept["id"]
        # Keywords
        if "keywords" in dept:
            for lang, kws in dept["keywords"].items():
                for kw in kws:
                    keyword_map[kw.lower().strip()].append(f"Department: {dept_id} ({lang})")
        
        # Aliases (usually treated as English/Universal)
        if "aliases" in dept:
            for alias in dept["aliases"]:
                # Assuming aliases act as English keywords for collision checks
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
    collisions = {k: v for k, v in keyword_map.items() if len(v) > 1}

    print(f"\nTotal Unique Keywords: {len(keyword_map)}")
    print(f"Total Collisions found: {len(collisions)}\n")

    # Group by pattern
    # e.g. "fever" -> [General OPD, General Medicine]
    
    print("-" * 80)
    print(f"{'KEYWORD':<30} | {'OCCURRENCES'}")
    print("-" * 80)
    
    for kw, sources in sorted(collisions.items()):
        # Filter out cases where it's just the same dept in different languages? 
        # No, collision logic usually cares about conflicts. 
        # But if "fever" is in hi and te for the SAME dept, that's fine.
        # If "fever" is in Dept A (en) and Dept B (en), that's a collision.
        
        # Let's simplify: check if simple set of sources (ignoring lang/type details for a second) has > 1 ID
        # Extract just IDs
        ids = set()
        for s in sources:
            # Extract ID usually after ": " and before " ("
            try:
                part = s.split(": ")[1].split(" (")[0]
                ids.add(part)
            except:
                ids.add(s)
        
        if len(ids) > 1:
            print(f"{kw:<30} | {', '.join(sources)}")

if __name__ == "__main__":
    analyze_duplicates()
