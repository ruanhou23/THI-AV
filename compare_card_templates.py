import os
import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

base_dir = r"c:\Users\hau\Desktop\AV_THI\tachaudio"

for t in range(1, 5):
    fname = os.path.join(base_dir, f"TOEIC_Listening_Test{t}_Audio_Interactive.txt")
    with open(fname, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    print(f"\n=================== TEST {t} ({len(lines)} cards) ===================")
    for q_idx in [0, 6, 31]:  # Q1, Q7, Q32
        parts = lines[q_idx].split("\t")
        front = parts[0]
        back = parts[1] if len(parts) > 1 else ""
        print(f"\n--- Card {q_idx+1} ---")
        print("FRONT:", front[:200])
        print("BACK: ", back[:120])
        # Check script presence
        has_script = "<script>" in front or "<script>" in back
        print("Has script embedded?", has_script)
