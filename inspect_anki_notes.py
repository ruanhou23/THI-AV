import sqlite3
import os
import sys
import shutil
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

db_path = os.path.join(os.environ['APPDATA'], 'Anki2', 'Người dùng 1', 'collection.anki2')
temp_db = 'temp_collection.anki2'
shutil.copy2(db_path, temp_db)

conn = sqlite3.connect(temp_db)
c = conn.cursor()
c.execute("SELECT id, mid, flds, tags FROM notes WHERE flds LIKE '%Part 1%'")
rows = c.fetchall()
print(f"Total Part 1 notes found: {len(rows)}")
for r in rows:
    fld = r[2].replace('\x1f', ' | ')
    imgs = re.findall(r'<img[^>]+>', fld)
    print(f"ID: {r[0]} | Tag: {r[3]} | Imgs: {imgs} | Snippet: {fld[:90]}")
conn.close()
os.remove(temp_db)
