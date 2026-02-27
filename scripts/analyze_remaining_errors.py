import re
from collections import Counter
import os

report_file = r'c:\Users\DELL\Downloads\ZeroKost\Robot_code\6.1_update_code\6.1_update_code\detailed_analyzer_report.txt'

if not os.path.exists(report_file):
    print("Report file not found!")
    exit(1)

with open(report_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

mismatches = [line.strip() for line in lines if line.startswith('Mismatch')]
hallucinations = [line.strip() for line in lines if line.startswith('Hallucination')]

print(f"Total Mismatches found in report: {len(mismatches)}")
print(f"Total Hallucinations found in report: {len(hallucinations)}")

def extract_id(line):
    match = re.search(r'ID\s+([\w_]+),', line)
    return match.group(1) if match else None

def get_lang(id_str):
    parts = id_str.split('_')
    if len(parts) > 2:
        return parts[-2]
    return "unknown"

def get_intent(id_str):
    parts = id_str.split('_')
    if len(parts) > 3 and id_str.startswith('dept_'):
        return '_'.join(parts[1:-2])
    elif len(parts) > 2 and id_str.startswith('int_'):
        return '_'.join(parts[1:-1])
    return id_str

mismatch_ids = [extract_id(m) for m in mismatches if extract_id(m)]

print("\n--- Mismatches by Language ---")
lang_c = Counter([get_lang(id) for id in mismatch_ids])
for lang, count in lang_c.most_common():
    print(f"  {lang}: {count}")

print("\n--- Top 15 Mismatched Departments ---")
dept_c = Counter([get_intent(id) for id in mismatch_ids])
for d, c in dept_c.most_common(15):
    print(f"  {d}: {c}")

print("\n--- Fallbacks Instead of Depts ---")
fallbacks = [m for m in mismatches if "Fallback instead of dept" in m]
print(f"  Total: {len(fallbacks)}")
fallback_depts = Counter([get_intent(extract_id(f)) for f in fallbacks if extract_id(f)])
for d, c in fallback_depts.most_common(10):
    print(f"  {d}: {c}")

print("\n--- Hallucinations Analysis ---")
for h in hallucinations:
    print(f"  {h}")
