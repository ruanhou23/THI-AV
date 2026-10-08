import os
import sys
import shutil

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Paths
SOURCE_BASE = "Listening practice test 1"
SPLIT_BASE = os.path.join(SOURCE_BASE, "audio_split")
IMAGES_DIR = "images"

# Local Anki Media folder
LOCAL_MEDIA_DIR = "anki_media"
os.makedirs(LOCAL_MEDIA_DIR, exist_ok=True)

# Anki Collection Media path
appdata = os.environ.get('APPDATA', '')
ANKI_MEDIA_DIR = os.path.join(appdata, "Anki2", "Người dùng 1", "collection.media")

print(f"[*] Thư mục local media: {os.path.abspath(LOCAL_MEDIA_DIR)}")
print(f"[*] Thư mục Anki media: {ANKI_MEDIA_DIR}")
print(f"    Tồn tại: {os.path.exists(ANKI_MEDIA_DIR)}")

# 1. Prepare images (part1_q01.png -> part1_q06.png)
for i in range(1, 7):
    src_img = os.path.join(IMAGES_DIR, f"image{i}.png")
    dst_name = f"part1_q{i:02d}.png"
    if os.path.exists(src_img):
        # copy to local
        shutil.copy2(src_img, os.path.join(LOCAL_MEDIA_DIR, dst_name))
        # copy to anki
        if os.path.exists(ANKI_MEDIA_DIR):
            shutil.copy2(src_img, os.path.join(ANKI_MEDIA_DIR, dst_name))
        print(f"  -> Đã chép ảnh: {dst_name}")

# 2. Prepare Part 1 audio (part1_q01.mp3 -> part1_q06.mp3)
p1_dir = os.path.join(SPLIT_BASE, "Part 1")
for i in range(1, 7):
    src_mp3 = os.path.join(p1_dir, f"Part1_Q{i:02d}.mp3")
    dst_name = f"part1_q{i:02d}.mp3"
    if os.path.exists(src_mp3):
        shutil.copy2(src_mp3, os.path.join(LOCAL_MEDIA_DIR, dst_name))
        if os.path.exists(ANKI_MEDIA_DIR):
            shutil.copy2(src_mp3, os.path.join(ANKI_MEDIA_DIR, dst_name))
        print(f"  -> Đã chép audio: {dst_name}")

# 3. Prepare Part 2 audio (part2_q07.mp3 -> part2_q31.mp3)
p2_dir = os.path.join(SPLIT_BASE, "Part 2")
for i in range(7, 32):
    src_mp3 = os.path.join(p2_dir, f"Part2_Q{i:02d}.mp3")
    dst_name = f"part2_q{i:02d}.mp3"
    if os.path.exists(src_mp3):
        shutil.copy2(src_mp3, os.path.join(LOCAL_MEDIA_DIR, dst_name))
        if os.path.exists(ANKI_MEDIA_DIR):
            shutil.copy2(src_mp3, os.path.join(ANKI_MEDIA_DIR, dst_name))
        print(f"  -> Đã chép audio: {dst_name}")

# 4. Prepare Part 3 audio (part3_c32_34.mp3, etc.)
p3_dir = os.path.join(SPLIT_BASE, "Part 3")
src_mp3 = os.path.join(p3_dir, "Part3_Q32_34.mp3")
dst_name = "part3_c32_34.mp3"
if os.path.exists(src_mp3):
    shutil.copy2(src_mp3, os.path.join(LOCAL_MEDIA_DIR, dst_name))
    if os.path.exists(ANKI_MEDIA_DIR):
        shutil.copy2(src_mp3, os.path.join(ANKI_MEDIA_DIR, dst_name))
    print(f"  -> Đã chép audio: {dst_name}")

# Also copy all other Part 3 audio files with part3_cXX_YY.mp3 naming
conv_ranges = [
    (32, 34), (35, 37), (38, 40), (41, 43), (44, 46),
    (47, 49), (50, 52), (53, 55), (56, 58), (59, 61),
    (62, 64), (65, 67), (68, 70)
]
for s, e in conv_ranges:
    src_mp3 = os.path.join(p3_dir, f"Part3_Q{s}_{e}.mp3")
    dst_name = f"part3_c{s}_{e}.mp3"
    if os.path.exists(src_mp3):
        shutil.copy2(src_mp3, os.path.join(LOCAL_MEDIA_DIR, dst_name))
        if os.path.exists(ANKI_MEDIA_DIR):
            shutil.copy2(src_mp3, os.path.join(ANKI_MEDIA_DIR, dst_name))

print("\n[+] ĐÃ HOÀN TẤT SAO CHÉP TOÀN BỘ FILE AUDIO VÀ ẢNH VÀO ANKI COLLECTION.MEDIA!")
