import os
import sys
import sqlite3
import shutil
import tempfile
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

base_dir = r"c:\Users\hau\Desktop\AV_THI\tachaudio"
appdata = os.environ.get('APPDATA', '')
media_dir = os.path.join(appdata, "Anki2", "Người dùng 1", "collection.media")
db_path = os.path.join(appdata, "Anki2", "Người dùng 1", "collection.anki2")

print("--- 1. CHECK IMAGES IN MEDIA_DIR & BASE_DIR ---")
for t in range(1, 5):
    media_imgs = [f for f in os.listdir(media_dir) if f.endswith(".png") and (f"test{t}" in f or (t == 1 and f.startswith("part1")))]
    base_imgs = [f for f in os.listdir(base_dir) if f.endswith(".png") and (f"test{t}" in f or (t == 1 and f.startswith("part1")))]
    print(f"Test {t}:")
    print(f"  In media_dir: {sorted(media_imgs)}")
    print(f"  In base_dir:  {sorted(base_imgs)}")

print("\n--- 2. CHECK NOTES IN ANKI DB ---")
temp_db = os.path.join(tempfile.gettempdir(), "temp_t1_check.anki2")
shutil.copy2(db_path, temp_db)
conn = sqlite3.connect(temp_db)
cur = conn.cursor()

cur.execute("SELECT id, tags, flds FROM notes")
rows = cur.fetchall()

print(f"Total notes in DB: {len(rows)}")
for nid, tags, flds in rows:
    first_field = flds.split("\x1f")[0] if "\x1f" in flds else flds.split("\t")[0]
    # Check which test this belongs to
    # If not tagged or Test 1
    if "Test1" in tags or "Test1" in first_field or "Number" in first_field or "part1_q" in first_field or "test1" in first_field:
        q_title = first_field.split("<br>")[0] if "<br>" in first_field else first_field[:30]
        # print first 5 and last 5 or summary
        pass

# Group notes by detected test
test_notes = {1: [], 2: [], 3: [], 4: [], 'other': []}
for nid, tags, flds in rows:
    t_clean = tags.strip()
    if "TOEIC_Listening_Test2" in t_clean:
        test_notes[2].append((nid, flds))
    elif "TOEIC_Listening_Test3" in t_clean:
        test_notes[3].append((nid, flds))
    elif "TOEIC_Listening_Test4" in t_clean:
        test_notes[4].append((nid, flds))
    elif "TOEIC_Listening_Test1" in t_clean or "Test 1" in flds or "part1_q" in flds:
        test_notes[1].append((nid, flds))
    else:
        test_notes['other'].append((nid, t_clean, flds))

print(f"Notes assigned to Test 1: {len(test_notes[1])}")
print(f"Notes assigned to Test 2: {len(test_notes[2])}")
print(f"Notes assigned to Test 3: {len(test_notes[3])}")
print(f"Notes assigned to Test 4: {len(test_notes[4])}")
print(f"Notes in 'other': {len(test_notes['other'])}")

if test_notes['other']:
    print("Sample 'other' notes:")
    for nid, t_clean, flds in test_notes['other'][:5]:
        print(f"  tag='{t_clean}' flds={flds[:60]}")

print("\nWhat questions are present in Test 1 in Anki?")
p1_cnt = 0
p2_cnt = 0
p3_cnt = 0
for nid, flds in test_notes[1]:
    first_fld = flds.split("\x1f")[0]
    if "Part 1" in first_fld:
        p1_cnt += 1
    elif "Part 2" in first_fld:
        p2_cnt += 1
    elif "Part 3" in first_fld:
        p3_cnt += 1
    else:
        print("  Unknown part:", first_fld[:40])

print(f"Test 1 in Anki has: Part 1 = {p1_cnt}, Part 2 = {p2_cnt}, Part 3 = {p3_cnt}")

# Check what the interactive file for Test 1 has
t1_txt = os.path.join(base_dir, "TOEIC_Listening_Test1_Audio_Interactive.txt")
with open(t1_txt, "r", encoding="utf-8") as f:
    t1_lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
print(f"Test 1 interactive TXT file has: {len(t1_lines)} cards")
