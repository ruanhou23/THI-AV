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
c.execute("SELECT flds FROM notes")
rows = c.fetchall()

used_media = set()
for r in rows:
    fld = r[0]
    imgs = re.findall(r'<img[^>]+src="([^">]+)"', fld)
    sounds = re.findall(r'\[sound:([^\]]+)\]', fld)
    used_media.update(imgs)
    used_media.update(sounds)

conn.close()
os.remove(temp_db)

anki_media = os.path.join(os.environ['APPDATA'], 'Anki2', 'Người dùng 1', 'collection.media')
disk_files = set(os.listdir(anki_media))

unused = disk_files - used_media
# Anki ignores files starting with _
unused = {f for f in unused if not f.startswith('_')}

print(f"Total files on disk: {len(disk_files)}")
print(f"Total media referenced in notes: {len(used_media)}")
print(f"Unused files count: {len(unused)}")

# Group unused files
test3_4_files = {f for f in unused if f.startswith('test3_') or f.startswith('test4_')}
other_unused = unused - test3_4_files

print(f"\n1. Test 3 & Test 4 files (chưa import thẻ Test 3 & 4): {len(test3_4_files)}")
for f in sorted(test3_4_files)[:10]:
    print("   ", f)
if len(test3_4_files) > 10:
    print(f"    ... và {len(test3_4_files) - 10} file khác")

print(f"\n2. Các file không liên quan / file thừa khác: {len(other_unused)}")
for f in sorted(other_unused):
    print("   ", f)
