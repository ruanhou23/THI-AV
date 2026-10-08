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

all_imgs = set()
all_sounds = set()
for r in rows:
    fld = r[0]
    imgs = re.findall(r'<img[^>]+src="([^">]+)"', fld)
    sounds = re.findall(r'\[sound:([^\]]+)\]', fld)
    all_imgs.update(imgs)
    all_sounds.update(sounds)

conn.close()
os.remove(temp_db)

anki_media = os.path.join(os.environ['APPDATA'], 'Anki2', 'Người dùng 1', 'collection.media')
existing_media = set(os.listdir(anki_media))

missing_imgs = [img for img in all_imgs if img not in existing_media]
missing_sounds = [snd for snd in all_sounds if snd not in existing_media]

print(f"Total unique images referenced in Anki database: {len(all_imgs)}")
print(f"Missing images in Anki: {len(missing_imgs)}")
for m in sorted(missing_imgs):
    print(f"  MISSING IMG: {m}")

print(f"\nTotal unique sounds referenced in Anki database: {len(all_sounds)}")
print(f"Missing sounds in Anki: {len(missing_sounds)}")
for m in sorted(missing_sounds):
    print(f"  MISSING SOUND: {m}")
