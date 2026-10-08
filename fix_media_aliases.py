import os
import sys
import shutil

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

anki_media = os.path.join(os.environ['APPDATA'], 'Anki2', 'Người dùng 1', 'collection.media')
print(f"[*] Đang bổ sung các tên alias vào Anki media: {anki_media}")

# For Test 2: map test2_partX -> test2_pX
for i in range(1, 7):
    # Image: test2_part1_qXX.png -> test2_p1_qXX.png
    src_img = os.path.join(anki_media, f"test2_part1_q{i:02d}.png")
    dst_img = os.path.join(anki_media, f"test2_p1_q{i:02d}.png")
    if os.path.exists(src_img):
        shutil.copy2(src_img, dst_img)
        print(f"  -> Created image alias: {os.path.basename(dst_img)}")
    
    # Audio: test2_part1_qXX.mp3 -> test2_p1_qXX.mp3
    src_snd = os.path.join(anki_media, f"test2_part1_q{i:02d}.mp3")
    dst_snd = os.path.join(anki_media, f"test2_p1_q{i:02d}.mp3")
    if os.path.exists(src_snd):
        shutil.copy2(src_snd, dst_snd)
        print(f"  -> Created sound alias: {os.path.basename(dst_snd)}")

# Part 2 Audio
for i in range(7, 32):
    src_snd = os.path.join(anki_media, f"test2_part2_q{i:02d}.mp3")
    dst_snd = os.path.join(anki_media, f"test2_p2_q{i:02d}.mp3")
    if os.path.exists(src_snd):
        shutil.copy2(src_snd, dst_snd)

# Part 3 Audio
conv_ranges = [
    (32, 34), (35, 37), (38, 40), (41, 43), (44, 46),
    (47, 49), (50, 52), (53, 55), (56, 58), (59, 61),
    (62, 64), (65, 67), (68, 70)
]
for s, e in conv_ranges:
    src_snd = os.path.join(anki_media, f"test2_part3_c{s}_{e}.mp3")
    dst_snd = os.path.join(anki_media, f"test2_p3_c{s}_{e}.mp3")
    if os.path.exists(src_snd):
        shutil.copy2(src_snd, dst_snd)

# Do the same for Test 1, Test 3, Test 4 just in case user imports short names
for t in [1, 3, 4]:
    for i in range(1, 7):
        # Images
        src_img = os.path.join(anki_media, f"test{t}_part1_q{i:02d}.png")
        dst_img = os.path.join(anki_media, f"test{t}_p1_q{i:02d}.png")
        if os.path.exists(src_img):
            shutil.copy2(src_img, dst_img)
        # Audio
        src_snd = os.path.join(anki_media, f"test{t}_part1_q{i:02d}.mp3")
        dst_snd = os.path.join(anki_media, f"test{t}_p1_q{i:02d}.mp3")
        if os.path.exists(src_snd):
            shutil.copy2(src_snd, dst_snd)
    
    # Part 2
    for i in range(7, 32):
        src_snd = os.path.join(anki_media, f"test{t}_part2_q{i:02d}.mp3")
        dst_snd = os.path.join(anki_media, f"test{t}_p2_q{i:02d}.mp3")
        if os.path.exists(src_snd):
            shutil.copy2(src_snd, dst_snd)
    
    # Part 3
    for s, e in conv_ranges:
        src_snd = os.path.join(anki_media, f"test{t}_part3_c{s}_{e}.mp3")
        dst_snd = os.path.join(anki_media, f"test{t}_p3_c{s}_{e}.mp3")
        if os.path.exists(src_snd):
            shutil.copy2(src_snd, dst_snd)

# Also for Test 1 where user named without 'test1_':
# part1_q01.png vs p1_q01.png vs test1_part1_q01.png
for i in range(1, 7):
    src_img = os.path.join(anki_media, f"part1_q{i:02d}.png")
    if os.path.exists(src_img):
        shutil.copy2(src_img, os.path.join(anki_media, f"test1_part1_q{i:02d}.png"))
        shutil.copy2(src_img, os.path.join(anki_media, f"test1_p1_q{i:02d}.png"))
        shutil.copy2(src_img, os.path.join(anki_media, f"image{i}.png"))
    
    src_snd = os.path.join(anki_media, f"part1_q{i:02d}.mp3")
    if os.path.exists(src_snd):
        shutil.copy2(src_snd, os.path.join(anki_media, f"test1_part1_q{i:02d}.mp3"))
        shutil.copy2(src_snd, os.path.join(anki_media, f"test1_p1_q{i:02d}.mp3"))

print("\n[+] ĐÃ HOÀN TẤT TẠO TOÀN BỘ CÁC TÊN TƯƠNG THÍCH (ALIAS) VÀO ANKI MEDIA!")
