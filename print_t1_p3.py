import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('TOEIC_Listening_Test1_Audio_Interactive.txt', 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]

print(f"Total cards: {len(lines)}")
# Print lines from index 34 (Question 35) to 69 (Question 70)
for idx, l in enumerate(lines[34:], start=35):
    print(f"--- Q{idx} ---")
    front, back = l.split('\t')
    print("FRONT:", front[:120])
    print("BACK:", back[:100])
