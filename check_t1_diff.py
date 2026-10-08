import os
import sys
import re
import sqlite3
import shutil
import tempfile

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

appdata = os.environ.get('APPDATA', '')
db_path = os.path.join(appdata, 'Anki2', 'Người dùng 1', 'collection.anki2')
temp_db = os.path.join(tempfile.gettempdir(), 'temp_t1_p3.anki2')
shutil.copy2(db_path, temp_db)
conn = sqlite3.connect(temp_db)
cur = conn.cursor()
cur.execute("SELECT flds FROM notes WHERE tags LIKE '%Test1%'")
rows = cur.fetchall()
anki_q_nums = set()
for r in rows:
    fld = r[0]
    m = re.search(r'Part\s*(\d+)\s*[-–]\s*(?:Number|Câu)\s*(\d+)', fld)
    if m:
        anki_q_nums.add((int(m.group(1)), int(m.group(2))))

print("Questions in Anki for Test 1 count:", len(anki_q_nums))
print("Questions in Anki for Test 1:", sorted(list(anki_q_nums)))

txt_path = r'c:\Users\hau\Desktop\AV_THI\tachaudio\TOEIC_Listening_Test1_Audio_Interactive.txt'
with open(txt_path, 'r', encoding='utf-8') as f:
    txt_lines = f.readlines()

txt_q_nums = set()
for l in txt_lines:
    m = re.search(r'Part\s*(\d+)\s*[-–]\s*(?:Number|Câu)\s*(\d+)', l)
    if m:
        txt_q_nums.add((int(m.group(1)), int(m.group(2))))

print("Questions in TXT file for Test 1 count:", len(txt_q_nums))
missing_in_anki = sorted(list(txt_q_nums - anki_q_nums))
print(f"Số câu trong TXT nhưng chưa có trong Anki ({len(missing_in_anki)} câu):")
print(missing_in_anki)
