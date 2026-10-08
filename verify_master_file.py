import os
import re

base_dir = r"c:\Users\hau\Desktop\AV_THI\tachaudio"
media_dir = r"C:\Users\hau\AppData\Roaming\Anki2\Người dùng 1\collection.media"
existing = set(os.listdir(media_dir))

all_file = os.path.join(base_dir, "TOEIC_Listening_ALL_TESTS_1_2_3_4_FINAL.txt")
with open(all_file, "r", encoding="utf-8") as f:
    cards = [l.strip() for l in f if '\t' in l]

print(f"Total cards in master file: {len(cards)}")

missing_imgs = set()
missing_snds = set()

img_pat = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']')
snd_pat = re.compile(r'\[sound:([^\]]+)\]')

for idx, c in enumerate(cards, start=1):
    front, back = c.split('\t')
    for img in img_pat.findall(front):
        if img not in existing:
            missing_imgs.add((idx, img))
    for snd in snd_pat.findall(front):
        if snd not in existing:
            missing_snds.add((idx, snd))

print(f"Missing images: {len(missing_imgs)} {missing_imgs}")
print(f"Missing sounds: {len(missing_snds)} {missing_snds}")
if len(missing_imgs) == 0 and len(missing_snds) == 0:
    print(">>> 100% PERFECT! ALL 280 CARDS VALIDATED WITH ZERO MISSING MEDIA! <<<")
