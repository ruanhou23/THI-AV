import os
import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

base_dir = r"c:\Users\hau\Desktop\AV_THI\tachaudio"

mc_script = """<script>function checkMC(btn, choice){var parent = btn.parentElement; if(parent.dataset.answered) return; parent.dataset.answered = "true"; var correct = parent.dataset.ans; var btns = parent.getElementsByTagName("button"); for(var i=0; i<btns.length; i++){ if(btns[i].textContent.trim().startsWith("(" + correct + ")")){ btns[i].style.background = "#28a745"; btns[i].style.color = "#fff"; btns[i].style.borderColor = "#28a745"; } } if(choice !== correct){ btn.style.background = "#dc3545"; btn.style.color = "#fff"; btn.style.borderColor = "#dc3545"; }}</script>"""

# Load existing files
decks = {}
for t in range(1, 5):
    fname = os.path.join(base_dir, f"TOEIC_Listening_Test{t}_Audio_Interactive.txt")
    with open(fname, "r", encoding="utf-8") as f:
        cards = [l.strip() for l in f if '\t' in l]
    decks[t] = cards
    print(f"Loaded Test {t}: {len(cards)} cards")

# Ensure all cards have proper formatting
# For each card:
# 1. Front should have mc_script embedded or available
# 2. In Test 4 Part 1 Q4, Q5, Q6: ensure img is present
clean_decks = {}
for t in range(1, 5):
    clean_cards = []
    for idx, card in enumerate(decks[t], start=1):
        front, back = card.split("\t")
        
        # Remove any stray <script> inside front to avoid duplicate mess
        front = re.sub(r'<script.*?</script>', '', front, flags=re.DOTALL)
        
        # In Test 4 Q4, Q5, Q6: add image if missing
        if t == 4 and idx in [4, 5, 6]:
            img_tag = f'<img src="test4_p1_q0{idx}.png"><br>'
            if f'test4_p1_q0{idx}.png' not in front and f'test4_part1_q0{idx}.png' not in front:
                front = front.replace(f'[sound:test4_p1_q0{idx}.mp3]', f'{img_tag}[sound:test4_p1_q0{idx}.mp3]')
                front = front.replace(f'[sound:test4_part1_q0{idx}.mp3]', f'{img_tag}[sound:test4_part1_q0{idx}.mp3]')
        
        # Add script to every front
        clean_front = front + mc_script
        clean_cards.append(f"{clean_front}\t{back}")
    clean_decks[t] = clean_cards

# Write individual files
for t in range(1, 5):
    out_file = os.path.join(base_dir, f"TOEIC_Listening_Test{t}_FINAL.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("#separator:tab\n")
        f.write("#html:true\n")
        f.write(f"#tags:TOEIC_Listening_Test{t}\n\n")
        for c in clean_decks[t]:
            f.write(c + "\n")
    print(f"Wrote {len(clean_decks[t])} cards to TOEIC_Listening_Test{t}_FINAL.txt")

# Write All-in-one file
all_file = os.path.join(base_dir, "TOEIC_Listening_ALL_TESTS_1_2_3_4_FINAL.txt")
with open(all_file, "w", encoding="utf-8") as f:
    f.write("#separator:tab\n")
    f.write("#html:true\n\n")
    for t in range(1, 5):
        f.write(f"#tags:TOEIC_Listening_Test{t}\n")
        for c in clean_decks[t]:
            f.write(c + "\n")
        f.write("\n")
print(f"Wrote ALL 280 cards to TOEIC_Listening_ALL_TESTS_1_2_3_4_FINAL.txt")
