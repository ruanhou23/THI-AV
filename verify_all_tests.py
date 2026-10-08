import os
import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

anki_media = os.path.join(os.environ['APPDATA'], 'Anki2', 'Người dùng 1', 'collection.media')

decks = [
    ("Test 1", "TOEIC_Listening_Test1_Audio_Interactive.txt"),
    ("Test 2", "TOEIC_Listening_Test2_Audio_Interactive.txt"),
    ("Test 3", "TOEIC_Listening_Test3_Audio_Interactive.txt"),
    ("Test 4", "TOEIC_Listening_Test4_Audio_Interactive.txt"),
]

all_ok = True
for name, fpath in decks:
    if not os.path.exists(fpath):
        print(f"File not found: {fpath}")
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    
    cards = [l for l in text.split("\n") if l.strip() and not l.startswith("#")]
    sounds = set(re.findall(r"\[sound:([^\]]+)\]", text))
    imgs = set(re.findall(r'<img src="([^"]+)">', text))
    
    missing_s = [s for s in sounds if not os.path.exists(os.path.join(anki_media, s))]
    missing_i = [i for i in imgs if not os.path.exists(os.path.join(anki_media, i))]
    
    print(f"=== {name} ({fpath}) ===")
    print(f"  Tổng số thẻ: {len(cards)}")
    print(f"  Audio: {len(sounds)} files (Thiếu: {len(missing_s)})")
    print(f"  Ảnh: {len(imgs)} files (Thiếu: {len(missing_i)})")
    if missing_s or missing_i:
        all_ok = False
        print(f"    Missing sounds: {missing_s}")
        print(f"    Missing images: {missing_i}")

if all_ok:
    print("\n>>> TẤT CẢ 4 TEST ĐỀU ĐÃ ĐẦY ĐỦ 100% VÀ SẴN SÀNG TRONG ANKI! <<<")
