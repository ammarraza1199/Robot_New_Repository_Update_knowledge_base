import json
import os
from collections import Counter

def analyze_json(file_path):
    print(f"\nAnalyzing: {file_path}")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_te_keywords = []
    dept_keyword_map = {}

    for dept in data.get('departments', []):
        dept_id = dept.get('id')
        te_keywords = dept.get('keywords', {}).get('te', [])
        
        # 1. Duplicates within department
        counts = Counter(te_keywords)
        duplicates = [kw for kw, count in counts.items() if count > 1]
        if duplicates:
            print(f"  [{dept_id}] Duplicates: {duplicates}")
        
        dept_keyword_map[dept_id] = set(te_keywords)
        all_te_keywords.extend(te_keywords)

    # 2. Overlap between departments
    overlap_report = {}
    depts = list(dept_keyword_map.keys())
    for i in range(len(depts)):
        for j in range(i + 1, len(depts)):
            d1, d2 = depts[i], depts[j]
            overlap = dept_keyword_map[d1].intersection(dept_keyword_map[d2])
            if overlap:
                overlap_report[f"{d1} & {d2}"] = list(overlap)

    if overlap_report:
        print("\n  Keyword Overlap between departments:")
        for pair, items in overlap_report.items():
            print(f"    {pair}: {items}")

    # 3. Long keywords (potential litter)
    long_keywords = [kw for kw in set(all_te_keywords) if len(kw.split()) > 3]
    if long_keywords:
        print(f"\n  Long Keywords (>3 words): {len(long_keywords)}")
        for kw in sorted(long_keywords)[:20]: # Show first 20
             print(f"    - {kw}")

    # 4. Total unique keywords
    print(f"\n  Total unique TE keywords: {len(set(all_te_keywords))}")
    print(f"  Total TE keywords (including duplicates): {len(all_te_keywords)}")

if __name__ == "__main__":
    import sys
    # Redirect stdout to a file with utf-8 encoding
    with open('analysis_report.txt', 'w', encoding='utf-8') as sys.stdout:
        analyze_json('hospital_knowledge_base.json')
        analyze_json('hospital_knowledge_base_updated.json')
        analyze_json('hospital_knowledge_base_optimized.json')

