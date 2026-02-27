import collections
import re

report_path = r"c:\Users\DELL\Downloads\ZeroKost\Robot_code\6.1_update_code\6.1_update_code\scripts\detailed_analyzer_report.txt"

with open(report_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

hallucinations = []
mismatches = []
hallucination_responses = collections.Counter()
mismatch_responses = collections.Counter()
mismatch_expected = collections.defaultdict(list)

for line in lines:
    line = line.strip()
    if line.startswith("Hallucination:"):
        # Format: Hallucination: ID ..., Expected: [...], Got: ...
        match = re.search(r"Got: (.*)", line)
        if match:
            resp = match.group(1).strip()
            hallucination_responses[resp] += 1
            hallucinations.append(line)
    elif line.startswith("Mismatch:"):
        match = re.search(r"Expected: \[(.*?)\], Got: (.*)", line)
        if match:
            expected = match.group(1)
            resp = match.group(2).strip()
            mismatch_responses[resp] += 1
            mismatches.append(line)
            mismatch_expected[resp].append(expected)


out_file = r"c:\Users\DELL\Downloads\ZeroKost\Robot_code\6.1_update_code\6.1_update_code\scripts\analyze_summary.md"

with open(out_file, 'w', encoding='utf-8') as f:
    f.write("=== TOP 10 HALLUCINATED RESPONSES ===\n")
    for resp, count in hallucination_responses.most_common(10):
        f.write(f"{count} times: {resp[:100]}\n")

    f.write("\n=== TOP 10 MISMATCHED RESPONSES ===\n")
    for resp, count in mismatch_responses.most_common(10):
        # Get a sample of what we expected when we got this mismatch
        exp_sample = list(set(mismatch_expected[resp]))[:3]
        f.write(f"{count} times: {resp[:100]} | Expected: {exp_sample}\n")

    f.write("\n=== ANALYZING POTENTIAL MISCLASSIFICATIONS ===\n")
    nav_robot_count_smalltalk = 0
    nav_robot_count_dept = 0
    for h in hallucinations:
        if "I am a navigation robot" in h:
            if "int_" in h:
                nav_robot_count_smalltalk += 1
            elif "dept_" in h:
                nav_robot_count_dept += 1
    f.write(f"'I am a navigation robot...' response - For smalltalk (int_): {nav_robot_count_smalltalk}, For departments (dept_): {nav_robot_count_dept}\n")

print("Analysis complete. Check analyze_summary.md")


