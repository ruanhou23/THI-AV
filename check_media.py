import os
import re

anki_media = os.path.join(os.environ['APPDATA'], 'Anki2', 'Người dùng 1', 'collection.media')
with open('TOEIC_Listening_Test2_Audio_Interactive.txt', 'r', encoding='utf-8') as f:
    text = f.read()

sounds = set(re.findall(r'\[sound:([^\]]+)\]', text))
imgs = set(re.findall(r'<img src="([^"]+)">', text))

missing_s = [s for s in sounds if not os.path.exists(os.path.join(anki_media, s))]
missing_i = [i for i in imgs if not os.path.exists(os.path.join(anki_media, i))]

print("Missing sounds:", missing_s)
print("Missing images:", missing_i)
print(f"Total sounds verified: {len(sounds)}")
print(f"Total images verified: {len(imgs)}")
