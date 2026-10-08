import json
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

with open('toeic_app_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i in [0, 1, 6, 7, 31, 32]:
    q = data[i]
    print(f"\n================ Question {q['id']} (Part {q['part']}) ================")
    print("PROMPT:", q.get('prompt'))
    print("OPTIONS:", q.get('options'))
    print("CORRECT:", q.get('correctAnswer'))
    print("EXPLANATION:", q.get('explanation'))
