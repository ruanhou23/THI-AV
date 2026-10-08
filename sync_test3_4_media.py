import os
import sys
import shutil
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

appdata = os.environ.get('APPDATA', '')
ANKI_MEDIA_DIR = os.path.join(appdata, "Anki2", "Người dùng 1", "collection.media")
mc_script = """<script>function checkMC(btn, choice){var parent = btn.parentElement; if(parent.dataset.answered) return; parent.dataset.answered = "true"; var correct = parent.dataset.ans; var btns = parent.getElementsByTagName("button"); for(var i=0; i<btns.length; i++){ if(btns[i].textContent.trim().startsWith("(" + correct + ")")){ btns[i].style.background = "#28a745"; btns[i].style.color = "#fff"; } } if(choice !== correct){ btn.style.background = "#dc3545"; btn.style.color = "#fff"; }}</script>"""

conv_ranges = [
    (32, 34), (35, 37), (38, 40), (41, 43), (44, 46),
    (47, 49), (50, 52), (53, 55), (56, 58), (59, 61),
    (62, 64), (65, 67), (68, 70)
]

# =========================================================================
# TEST 3 PROCESSING
# =========================================================================
print("================= SYNCING MEDIA TEST 3 =================")
t3_local_media = "test3_media"
os.makedirs(t3_local_media, exist_ok=True)
t3_split = "Listening practice test 3/audio_split"

# Part 1 audio & images
for i in range(1, 7):
    # Image
    img_src = f"test3_part1_q0{i}.png"
    if os.path.exists(img_src):
        shutil.copy2(img_src, os.path.join(t3_local_media, img_src))
        if os.path.exists(ANKI_MEDIA_DIR):
            shutil.copy2(img_src, os.path.join(ANKI_MEDIA_DIR, img_src))
    # Audio
    a_src = os.path.join(t3_split, "Part 1", f"Part1_Q{i:02d}.mp3")
    a_dst = f"test3_part1_q{i:02d}.mp3"
    if os.path.exists(a_src):
        shutil.copy2(a_src, os.path.join(t3_local_media, a_dst))
        if os.path.exists(ANKI_MEDIA_DIR):
            shutil.copy2(a_src, os.path.join(ANKI_MEDIA_DIR, a_dst))

# Part 2 audio
for i in range(7, 32):
    a_src = os.path.join(t3_split, "Part 2", f"Part2_Q{i:02d}.mp3")
    a_dst = f"test3_part2_q{i:02d}.mp3"
    if os.path.exists(a_src):
        shutil.copy2(a_src, os.path.join(t3_local_media, a_dst))
        if os.path.exists(ANKI_MEDIA_DIR):
            shutil.copy2(a_src, os.path.join(ANKI_MEDIA_DIR, a_dst))

# Part 3 audio
for s, e in conv_ranges:
    a_src = os.path.join(t3_split, "Part 3", f"Part3_Q{s}_{e}.mp3")
    a_dst = f"test3_part3_c{s}_{e}.mp3"
    if os.path.exists(a_src):
        shutil.copy2(a_src, os.path.join(t3_local_media, a_dst))
        if os.path.exists(ANKI_MEDIA_DIR):
            shutil.copy2(a_src, os.path.join(ANKI_MEDIA_DIR, a_dst))

print("[+] Đã đồng bộ media Test 3 vào Anki!")

# =========================================================================
# TEST 4 PROCESSING
# =========================================================================
print("================= SYNCING MEDIA TEST 4 =================")
t4_local_media = "test4_media"
os.makedirs(t4_local_media, exist_ok=True)
t4_split = "Listening practice test 4/audio_split"

# Part 1 audio & images (3 images for Q1-Q3)
for i in range(1, 7):
    # Image (if exists)
    img_src = f"test4_part1_q0{i}.png"
    if os.path.exists(img_src):
        shutil.copy2(img_src, os.path.join(t4_local_media, img_src))
        if os.path.exists(ANKI_MEDIA_DIR):
            shutil.copy2(img_src, os.path.join(ANKI_MEDIA_DIR, img_src))
    # Audio
    a_src = os.path.join(t4_split, "Part 1", f"Part1_Q{i:02d}.mp3")
    a_dst = f"test4_part1_q{i:02d}.mp3"
    if os.path.exists(a_src):
        shutil.copy2(a_src, os.path.join(t4_local_media, a_dst))
        if os.path.exists(ANKI_MEDIA_DIR):
            shutil.copy2(a_src, os.path.join(ANKI_MEDIA_DIR, a_dst))

# Part 2 audio
for i in range(7, 32):
    a_src = os.path.join(t4_split, "Part 2", f"Part2_Q{i:02d}.mp3")
    a_dst = f"test4_part2_q{i:02d}.mp3"
    if os.path.exists(a_src):
        shutil.copy2(a_src, os.path.join(t4_local_media, a_dst))
        if os.path.exists(ANKI_MEDIA_DIR):
            shutil.copy2(a_src, os.path.join(ANKI_MEDIA_DIR, a_dst))

# Part 3 audio
for s, e in conv_ranges:
    a_src = os.path.join(t4_split, "Part 3", f"Part3_Q{s}_{e}.mp3")
    a_dst = f"test4_part3_c{s}_{e}.mp3"
    if os.path.exists(a_src):
        shutil.copy2(a_src, os.path.join(t4_local_media, a_dst))
        if os.path.exists(ANKI_MEDIA_DIR):
            shutil.copy2(a_src, os.path.join(ANKI_MEDIA_DIR, a_dst))

print("[+] Đã đồng bộ media Test 4 vào Anki!")
