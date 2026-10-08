import sqlite3
import re
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

db_path = r"C:\Users\hau\AppData\Roaming\Anki2\Người dùng 1\collection.anki2"
media_dir = r"C:\Users\hau\AppData\Roaming\Anki2\Người dùng 1\collection.media"

import shutil
import tempfile

temp_db = os.path.join(tempfile.gettempdir(), "temp_collection.anki2")
shutil.copy2(db_path, temp_db)
conn = sqlite3.connect(temp_db)
cur = conn.cursor()

cur.execute("SELECT flds FROM notes")
rows = cur.fetchall()

images = set()
sounds = set()

img_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']')
snd_pattern = re.compile(r'\[sound:([^\]]+)\]')

for r in rows:
    flds = r[0]
    for img in img_pattern.findall(flds):
        images.add(img)
    for snd in snd_pattern.findall(flds):
        sounds.add(snd)

print(f"Total notes in DB: {len(rows)}")
print(f"Total referenced images: {len(images)}")
print(f"Total referenced sounds: {len(sounds)}")

existing = set(os.listdir(media_dir))
missing_images = [img for img in images if img not in existing]
missing_sounds = [snd for snd in sounds if snd not in existing]

print(f"\nMissing images ({len(missing_images)}):")
for img in sorted(missing_images):
    print(" ", img)

print(f"\nMissing sounds ({len(missing_sounds)}):")
for snd in sorted(missing_sounds):
    print(" ", snd)
