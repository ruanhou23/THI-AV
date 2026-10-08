import json
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total items in data.json: {len(data)}")
for i in [0, 6, 31, 69]:
    if i < len(data):
        print(f"\nItem {i+1}:")
        for k, v in data[i].items():
            print(f"  {k}: {str(v)[:80]}")
