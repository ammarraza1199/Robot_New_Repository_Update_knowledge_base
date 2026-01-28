import json
import collections

def generate_report():
    input_file = "kb_brute_force_failures.json"
    output_file = r"c:\Users\DELL\.gemini\antigravity\brain\dacc373c-5922-4628-a5b0-021e7d2cf0e2\KB_FAILURES_BREAKDOWN.md"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            failures = json.load(f)
    except FileNotFoundError:
        print("Failures file not found.")
        return

    # Categorize
    missed = [] # Got: None
    wrong = []  # Got: Wrong Dept
    
    for fail in failures:
        if fail['got'] is None:
            missed.append(fail)
        else:
            wrong.append(fail)
            
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Knowledge Base Failure Analysis\n\n")
        f.write("## Summary\n")
        f.write(f"- **Total Failures:** {len(failures)}\n")
        f.write(f"- **NLU Misses (No Match):** {len(missed)} (Safer failure - Robot asks again)\n")
        f.write(f"- **Misclassifications (Wrong Dept):** {len(wrong)} (Risk of wrong transfer)\n\n")
        
        f.write("## 1. Misclassifications (The Dangerous Pattern)\n")
        f.write("These are keywords that mapped to the WRONG department. These are high priority fixes.\n\n")
        
        # Group by pattern: Expected -> Got
        pattern_map = collections.defaultdict(list)
        for w in wrong:
            key = f"{w['expected']} -> {w['got']}"
            pattern_map[key].append(w)
            
        # Sort by frequency
        sorted_patterns = sorted(pattern_map.items(), key=lambda x: len(x[1]), reverse=True)
        
        for pattern, items in sorted_patterns:
            f.write(f"### Pattern: {pattern} ({len(items)} cases)\n")
            f.write("| Lang | Input Question | Type |\n")
            f.write("| :--- | :--- | :--- |\n")
            for item in items:
                f.write(f"| {item['lang']} | {item['input']} | {item['type']} |\n")
            f.write("\n")

        f.write("## 2. NLU Misses (The Safe Failures)\n")
        f.write("These questions returned `None`. This usually happens for multi-word phrases that fuzzy matching missed.\n")
        f.write("To fix these, we can lower `fuzzy_threshold` or add more specific keywords.\n\n")
        
        # Group by Dept -> Lang
        miss_map = collections.defaultdict(list)
        for m in missed:
            key = f"{m['expected']} ({m['lang']})"
            miss_map[key].append(m)
            
        sorted_misses = sorted(miss_map.items(), key=lambda x: x[0])
        
        for group, items in sorted_misses:
            f.write(f"### {group}\n")
            for item in items:
                f.write(f"- {item['input']}\n")
            f.write("\n")

    print(f"Report generated: {output_file}")

if __name__ == "__main__":
    generate_report()
