import os
import sys
import sqlite3
import shutil
import tempfile
import re
from collections import Counter

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

base_dir = r"c:\Users\hau\Desktop\AV_THI\tachaudio"
appdata = os.environ.get('APPDATA', '')
media_dir = os.path.join(appdata, "Anki2", "Người dùng 1", "collection.media")
db_path = os.path.join(appdata, "Anki2", "Người dùng 1", "collection.anki2")

print("="*60)
print("1. KIỂM TRA CÁC FILE TEXT IMPORT (TOEIC_Listening_TestX_Audio_Interactive.txt)")
print("="*60)

for t in range(1, 5):
    fname = os.path.join(base_dir, f"TOEIC_Listening_Test{t}_Audio_Interactive.txt")
    if not os.path.exists(fname):
        print(f"❌ Test {t}: Không tìm thấy file {fname}")
        continue
    with open(fname, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    
    # Check parts
    p1 = sum(1 for l in lines if "Part 1" in l)
    p2 = sum(1 for l in lines if "Part 2" in l)
    p3 = sum(1 for l in lines if "Part 3" in l)
    print(f"✅ Test {t}: Tổng {len(lines)} thẻ (Part 1: {p1}, Part 2: {p2}, Part 3: {p3})")

print("\n" + "="*60)
print("2. KIỂM TRA FILE AUDIO & ẢNH ĐÃ CẮT TRÊN MÁY")
print("="*60)

conv_ranges = [
    (32, 34), (35, 37), (38, 40), (41, 43), (44, 46),
    (47, 49), (50, 52), (53, 55), (56, 58), (59, 61),
    (62, 64), (65, 67), (68, 70)
]

for t in range(1, 5):
    split_dir = os.path.join(base_dir, f"Listening practice test {t}", "audio_split")
    p1_audio = [f for f in os.listdir(os.path.join(split_dir, "Part 1")) if f.endswith(".mp3")] if os.path.exists(os.path.join(split_dir, "Part 1")) else []
    p2_audio = [f for f in os.listdir(os.path.join(split_dir, "Part 2")) if f.endswith(".mp3")] if os.path.exists(os.path.join(split_dir, "Part 2")) else []
    p3_audio = [f for f in os.listdir(os.path.join(split_dir, "Part 3")) if f.endswith(".mp3")] if os.path.exists(os.path.join(split_dir, "Part 3")) else []
    
    # images
    imgs = [f for f in os.listdir(base_dir) if f.startswith(f"test{t}_part1_q") and f.endswith(".png")]
    if t == 1 and not imgs:
        imgs = [f for f in os.listdir(base_dir) if f.startswith("part1_q") and f.endswith(".png")]
    
    print(f"Test {t}:")
    print(f"  - Ảnh Part 1: {len(imgs)}/6 ảnh ({'Đủ' if len(imgs) >= 6 else 'Thiếu'})")
    print(f"  - Audio Part 1: {len(p1_audio)}/6 file ({'Đủ' if len(p1_audio) >= 6 else 'Thiếu'})")
    print(f"  - Audio Part 2: {len(p2_audio)}/25 file ({'Đủ' if len(p2_audio) >= 25 else 'Thiếu'})")
    print(f"  - Audio Part 3: {len(p3_audio)}/13 file hội thoại ({'Đủ' if len(p3_audio) >= 13 else 'Thiếu'})")

print("\n" + "="*60)
print("3. KIỂM TRA TRONG ANKI DATABASE")
print("="*60)

temp_db = os.path.join(tempfile.gettempdir(), "temp_check_reqs.anki2")
shutil.copy2(db_path, temp_db)
conn = sqlite3.connect(temp_db)
cur = conn.cursor()

# Get deck names
cur.execute("SELECT decks FROM col")
col_row = cur.fetchone()
decks_json = col_row[0]

cur.execute("SELECT id, nid, did FROM cards")
cards = cur.fetchall()

cur.execute("SELECT id, tags, flds FROM notes")
notes = cur.fetchall()

print(f"Tổng số notes trong Anki: {len(notes)}")
print(f"Tổng số cards trong Anki: {len(cards)}")

tag_notes = Counter()
for nid, tags, flds in notes:
    tag_clean = tags.strip()
    tag_notes[tag_clean] += 1

print("\nPhân bổ theo tags:")
for tag, cnt in tag_notes.items():
    print(f"  Tag: '{tag}' -> {cnt} notes")

# Check test by test in notes
print("\nKiểm tra chi tiết từng test trong Anki DB:")
existing_media = set(os.listdir(media_dir))

img_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']')
snd_pattern = re.compile(r'\[sound:([^\]]+)\]')
btn_pattern = re.compile(r'<button')

for t in range(1, 5):
    t_notes = [n for n in notes if f"Test {t}" in n[2] or f"Test{t}" in n[2] or f"test{t}" in n[2] or f"Test{t}" in n[1] or f"test{t}" in n[1]]
    if t == 1:
        # also match Test 1 if tags don't explicitly say
        t1_extra = [n for n in notes if "Part 1 - Number" in n[2] or "Part 1 - Câu" in n[2] and n not in t_notes]
        t_notes.extend([n for n in t1_extra if n not in t_notes])
    
    missing_imgs = set()
    missing_snds = set()
    has_button_cnt = 0
    
    for nid, tags, flds in t_notes:
        for img in img_pattern.findall(flds):
            if img not in existing_media:
                missing_imgs.add(img)
        for snd in snd_pattern.findall(flds):
            if snd not in existing_media:
                missing_snds.add(snd)
        if btn_pattern.search(flds):
            has_button_cnt += 1
            
    print(f"Test {t}:")
    print(f"  - Số thẻ trong Anki: {len(t_notes)}")
    print(f"  - Số thẻ có nút bấm tương tác (<button>): {has_button_cnt}/{len(t_notes)}")
    print(f"  - Ảnh thiếu trong collection.media: {len(missing_imgs)} {missing_imgs if missing_imgs else ''}")
    print(f"  - Audio thiếu trong collection.media: {len(missing_snds)} {missing_snds if missing_snds else ''}")

print("\n" + "="*60)
print("TỔNG KẾT KIỂM TRA")
print("="*60)
