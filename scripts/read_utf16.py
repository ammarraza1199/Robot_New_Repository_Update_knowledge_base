import sys

try:
    with open("git_commit_log.txt", "r", encoding="utf-16-le") as f:
        content = f.read()
except FileNotFoundError:
    print("File not found")
    sys.exit(1)
except Exception as e:
    print(f"Error reading utf-16: {e}")
    # Try utf-8 just in case
    try:
        with open("kb_test_output.txt", "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e2:
        print(f"Error reading utf-8: {e2}")
        sys.exit(1)

with open("kb_test_output_clean.txt", "w", encoding="utf-8") as f:
    f.write(content)

print("Conversion complete.")
