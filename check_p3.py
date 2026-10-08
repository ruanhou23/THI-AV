import sys
import json

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

data = json.load(open('toeic_app_data.json', encoding='utf-8'))

for t in range(1, 5):
    p3 = [q for q in data if q['test'] == t and q['part'] == 3]
    print(f"==================== TEST {t} PART 3 ({len(p3)} questions) ====================")
    for q in p3[:6]:
        opts = ', '.join([f"({o['key']}) {o['text']}" for o in q['options']])
        print(f"{q['id']} Q{q['questionNum']} [Audio: {q['audio']}] Ans: {q['correctAnswer']}")
        print(f"   Prompt: {q['prompt']}")
        print(f"   Opts: {opts}")
        exp_first = q['explanation'].splitlines()[0] if q['explanation'] else ''
        print(f"   Expl: {exp_first[:100]}")
