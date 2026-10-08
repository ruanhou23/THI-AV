import os
import sys
import shutil
import zipfile
import sqlite3
import re
import tempfile

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

base_dir = r"c:\Users\hau\Desktop\AV_THI\tachaudio"
appdata = os.environ.get('APPDATA', '')
media_dir = os.path.join(appdata, "Anki2", "Người dùng 1", "collection.media")
db_path = os.path.join(appdata, "Anki2", "Người dùng 1", "collection.anki2")

print(f"Base dir: {base_dir}")
print(f"Anki Media dir: {media_dir}")
os.makedirs(media_dir, exist_ok=True)

# -------------------------------------------------------------
# 1. EXTRACT TEST 4 IMAGES FROM DOCX (if not all 6 extracted)
# -------------------------------------------------------------
docx_t4 = os.path.join(base_dir, "Listening practice test 4", "TOEIC_Practice_Test_4_Listening_Transcript.docx")
if os.path.exists(docx_t4):
    with zipfile.ZipFile(docx_t4, 'r') as z:
        # Check order from document.xml.rels
        import xml.etree.ElementTree as ET
        rels_xml = z.read('word/_rels/document.xml.rels')
        doc_xml = z.read('word/document.xml').decode('utf-8', errors='ignore')
        root_rels = ET.fromstring(rels_xml)
        rel_map = {r.attrib['Id']: r.attrib['Target'] for r in root_rels if 'Target' in r.attrib and 'Id' in r.attrib}
        
        embed_ids = re.findall(r'r:embed="([^"]+)"', doc_xml)
        image_targets = [rel_map.get(eid) for eid in embed_ids if eid in rel_map and 'media/' in rel_map[eid]]
        print(f"Found {len(image_targets)} image references in Test 4 docx: {image_targets}")
        
        for idx, target in enumerate(image_targets, start=1):
            if idx > 6:
                break
            full_zip_path = 'word/' + target.replace('\\', '/')
            if full_zip_path in z.namelist():
                out_name = f"test4_part1_q0{idx}.png"
                out_path = os.path.join(base_dir, out_name)
                with open(out_path, 'wb') as f_out:
                    f_out.write(z.read(full_zip_path))
                print(f"Extracted Test 4 Image {idx} -> {out_name}")

# Also ensure test4_media folder exists
t4_media_dir = os.path.join(base_dir, "test4_media")
os.makedirs(t4_media_dir, exist_ok=True)
for i in range(1, 7):
    src = os.path.join(base_dir, f"test4_part1_q0{i}.png")
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(t4_media_dir, f"test4_part1_q0{i}.png"))

# -------------------------------------------------------------
# 2. COPY ALL MEDIA (TEST 1, 2, 3, 4) TO ANKI MEDIA DIR
# -------------------------------------------------------------
conv_ranges = [
    (32, 34), (35, 37), (38, 40), (41, 43), (44, 46),
    (47, 49), (50, 52), (53, 55), (56, 58), (59, 61),
    (62, 64), (65, 67), (68, 70)
]

def copy_to_media(src_path, dst_names):
    if not os.path.exists(src_path):
        return
    for name in dst_names:
        dst = os.path.join(media_dir, name)
        # copy if doesn't exist or size is 0
        if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src_path):
            shutil.copy2(src_path, dst)

print("\n--- Synchronizing Test 1 Media ---")
t1_split = os.path.join(base_dir, "Listening practice test 1", "audio_split")
for i in range(1, 7):
    # Test 1 images
    for candidate in [os.path.join(base_dir, f"test1_part1_q0{i}.png"), os.path.join(base_dir, f"part1_q0{i}.png")]:
        if os.path.exists(candidate):
            copy_to_media(candidate, [f"part1_q0{i}.png", f"test1_part1_q0{i}.png", f"test1_p1_q0{i}.png"])
            break
    # Test 1 audio part 1
    a_src = os.path.join(t1_split, "Part 1", f"Part1_Q{i:02d}.mp3")
    copy_to_media(a_src, [f"part1_q{i:02d}.mp3", f"test1_part1_q{i:02d}.mp3", f"test1_p1_q{i:02d}.mp3"])

for i in range(7, 32):
    a_src = os.path.join(t1_split, "Part 2", f"Part2_Q{i:02d}.mp3")
    copy_to_media(a_src, [f"part2_q{i:02d}.mp3", f"test1_part2_q{i:02d}.mp3", f"test1_p2_q{i:02d}.mp3"])

for s, e in conv_ranges:
    a_src = os.path.join(t1_split, "Part 3", f"Part3_Q{s}_{e}.mp3")
    copy_to_media(a_src, [f"part3_c{s}_{e}.mp3", f"test1_part3_c{s}_{e}.mp3", f"test1_p3_c{s}_{e}.mp3"])

print("\n--- Synchronizing Test 2 Media ---")
t2_split = os.path.join(base_dir, "Listening practice test 2", "audio_split")
for i in range(1, 7):
    # Test 2 images
    for candidate in [os.path.join(base_dir, f"test2_part1_q0{i}.png"), os.path.join(base_dir, f"test2_p1_q0{i}.png")]:
        if os.path.exists(candidate):
            copy_to_media(candidate, [f"test2_part1_q0{i}.png", f"test2_p1_q0{i}.png"])
            break
    # Test 2 audio part 1
    a_src = os.path.join(t2_split, "Part 1", f"Part1_Q{i:02d}.mp3")
    copy_to_media(a_src, [f"test2_part1_q{i:02d}.mp3", f"test2_p1_q{i:02d}.mp3"])

for i in range(7, 32):
    a_src = os.path.join(t2_split, "Part 2", f"Part2_Q{i:02d}.mp3")
    copy_to_media(a_src, [f"test2_part2_q{i:02d}.mp3", f"test2_p2_q{i:02d}.mp3"])

for s, e in conv_ranges:
    a_src = os.path.join(t2_split, "Part 3", f"Part3_Q{s}_{e}.mp3")
    copy_to_media(a_src, [f"test2_part3_c{s}_{e}.mp3", f"test2_p3_c{s}_{e}.mp3"])

print("\n--- Synchronizing Test 3 Media ---")
t3_split = os.path.join(base_dir, "Listening practice test 3", "audio_split")
for i in range(1, 7):
    # Test 3 images
    for candidate in [
        os.path.join(base_dir, f"test3_part1_q0{i}.png"),
        os.path.join(base_dir, "test3_media", f"test3_part1_q0{i}.png")
    ]:
        if os.path.exists(candidate):
            copy_to_media(candidate, [f"test3_part1_q0{i}.png", f"test3_p1_q0{i}.png"])
            break
    # Test 3 audio part 1
    a_src = os.path.join(t3_split, "Part 1", f"Part1_Q{i:02d}.mp3")
    copy_to_media(a_src, [f"test3_part1_q{i:02d}.mp3", f"test3_p1_q{i:02d}.mp3"])

for i in range(7, 32):
    a_src = os.path.join(t3_split, "Part 2", f"Part2_Q{i:02d}.mp3")
    copy_to_media(a_src, [f"test3_part2_q{i:02d}.mp3", f"test3_p2_q{i:02d}.mp3"])

for s, e in conv_ranges:
    a_src = os.path.join(t3_split, "Part 3", f"Part3_Q{s}_{e}.mp3")
    names = [f"test3_part3_c{s}_{e}.mp3", f"test3_p3_c{s}_{e}.mp3"]
    if (s, e) == (59, 61):
        names.extend(["test3_part3_c60_61.mp3", "test3_p3_c60_61.mp3"])
    copy_to_media(a_src, names)

print("\n--- Synchronizing Test 4 Media ---")
t4_split = os.path.join(base_dir, "Listening practice test 4", "audio_split")
for i in range(1, 7):
    # Test 4 images
    for candidate in [
        os.path.join(base_dir, f"test4_part1_q0{i}.png"),
        os.path.join(base_dir, "test4_media", f"test4_part1_q0{i}.png")
    ]:
        if os.path.exists(candidate):
            copy_to_media(candidate, [f"test4_part1_q0{i}.png", f"test4_p1_q0{i}.png"])
            break
    # Test 4 audio part 1
    a_src = os.path.join(t4_split, "Part 1", f"Part1_Q{i:02d}.mp3")
    copy_to_media(a_src, [f"test4_part1_q{i:02d}.mp3", f"test4_p1_q{i:02d}.mp3"])

for i in range(7, 32):
    a_src = os.path.join(t4_split, "Part 2", f"Part2_Q{i:02d}.mp3")
    copy_to_media(a_src, [f"test4_part2_q{i:02d}.mp3", f"test4_p2_q{i:02d}.mp3"])

for s, e in conv_ranges:
    a_src = os.path.join(t4_split, "Part 3", f"Part3_Q{s}_{e}.mp3")
    names = [f"test4_part3_c{s}_{e}.mp3", f"test4_p3_c{s}_{e}.mp3"]
    copy_to_media(a_src, names)

print("\n--- Verification against Anki DB ---")
temp_db = os.path.join(tempfile.gettempdir(), "temp_check.anki2")
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

existing = set(os.listdir(media_dir))
missing_images = [img for img in images if img not in existing]
missing_sounds = [snd for snd in sounds if snd not in existing]

print(f"Total notes in Anki: {len(rows)}")
print(f"Total referenced images in Anki: {len(images)}")
print(f"Missing images in Anki: {len(missing_images)}")
if missing_images:
    for m in sorted(missing_images):
        print(f"  MISSING IMG: {m}")

print(f"Total referenced sounds in Anki: {len(sounds)}")
print(f"Missing sounds in Anki: {len(missing_sounds)}")
if missing_sounds:
    for m in sorted(missing_sounds):
        print(f"  MISSING SND: {m}")

print(f"\nTotal files in collection.media: {len(existing)}")
for prefix in ['part1_', 'part2_', 'part3_', 'test1', 'test2', 'test3', 'test4']:
    matched = [f for f in existing if f.startswith(prefix)]
    print(f"  Count for '{prefix}*': {len(matched)}")

if len(missing_images) == 0 and len(missing_sounds) == 0:
    print("\n>>> ALL ANKI MEDIA FILES ARE 100% COMPLETE & VERIFIED! <<<")
