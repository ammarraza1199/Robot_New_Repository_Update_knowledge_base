
import json
import re

try:
    with open('hospital_knowledge_base.json', 'r', encoding='utf-8') as f:
        kb = json.load(f)
    print("JSON Load Success")
except Exception as e:
    print(f"JSON Check Fail: {e}")
    exit(1)

interactions = kb.get("interactions", [])
print(f"Total Interactions: {len(interactions)}")

admin_ids = [x['id'] for x in interactions if 'director' in x['id'] or 'complaint' in x['id']]
print(f"Admin IDs found: {admin_ids}")

sym_ids = [x['id'] for x in interactions if 'sym_bleeding' in x['id']]
print(f"Symptom IDs found: {sym_ids}")

# Check keywords for bleeding
for item in interactions:
    if item['id'] == 'sym_bleeding':
        print(f"Bleeding Keywords (te): {item['keywords'].get('te')}")
