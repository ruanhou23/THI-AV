import os
import sys
import shutil
import re
import json

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

base_dir = r"c:\Users\hau\Desktop\AV_THI\tachaudio"
anki_media = os.path.join(os.environ.get('APPDATA', ''), "Anki2", "Người dùng 1", "collection.media")
app_media_dir = os.path.join(base_dir, "media")
os.makedirs(app_media_dir, exist_ok=True)

final_all_file = os.path.join(base_dir, "TOEIC_Listening_ALL_TESTS_1_2_3_4_FINAL.txt")

with open(final_all_file, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f if '\t' in l]

print(f"Total lines in final file: {len(lines)}")

# We have 4 tests, each 70 cards
tests_data = []

current_test = 0
for idx, line in enumerate(lines):
    test_num = (idx // 70) + 1
    q_in_test = (idx % 70) + 1
    
    front, back = line.split("\t")
    
    # 1. Determine Part
    if q_in_test <= 6:
        part_num = 1
        part_name = "Part 1 - Photographs (Mô tả tranh)"
    elif q_in_test <= 31:
        part_num = 2
        part_name = "Part 2 - Question & Response (Hỏi & Đáp)"
    else:
        part_num = 3
        part_name = "Part 3 - Conversations (Đoạn hội thoại)"
        
    # 2. Extract Audio
    audio_match = re.search(r'\[sound:([^\]]+)\]', front)
    audio_file = audio_match.group(1) if audio_match else None
    
    # 3. Extract Image
    img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', front)
    image_file = img_match.group(1) if img_match else None
    
    # 4. Extract Correct Answer
    ans_match = re.search(r'data-ans=["\']([A-D])["\']', front)
    correct_ans = ans_match.group(1) if ans_match else ""
    if not correct_ans:
        # Fallback to back
        ans_back = re.search(r'Đáp án(?:\s*đúng)?:\s*\(([A-D])\)', back)
        if ans_back:
            correct_ans = ans_back.group(1)
            
    # 5. Extract Options
    # Options are inside <button class="mc-btn" onclick="..."> (A) text </button>
    btn_matches = re.findall(r'<button[^>]*>\(([A-D])\)\s*([^<]+)</button>', front)
    options = []
    for letter, text in btn_matches:
        options.append({
            "key": letter.strip(),
            "text": text.strip()
        })
        
    # 6. Extract Question Prompt / Title
    # Look for <b>Question X: ...</b> or <b>Câu hỏi:</b> ... or Part 1 prompt
    prompt = ""
    q_text_match = re.search(r'<b>(?:Question\s*\d+:|Câu hỏi:)?\s*([^<]+)</b>', front)
    if q_text_match:
        prompt = q_text_match.group(1).strip()
    elif part_num == 1:
        prompt = "Listen to the four statements and choose the one that best describes the image."
    elif part_num == 2:
        prompt = "Listen to the question or statement and choose the best response (A, B, or C)."
    else:
        prompt = f"Question {q_in_test}"
        
    # 7. Extract Explanation & Transcript from Back
    explanation_clean = back.strip()
    
    # 8. Copy media files to app_media_dir
    if audio_file:
        src_audio = os.path.join(anki_media, audio_file)
        dst_audio = os.path.join(app_media_dir, audio_file)
        if os.path.exists(src_audio) and not os.path.exists(dst_audio):
            shutil.copy2(src_audio, dst_audio)
            
    if image_file:
        src_img = os.path.join(anki_media, image_file)
        dst_img = os.path.join(app_media_dir, image_file)
        if os.path.exists(src_img) and not os.path.exists(dst_img):
            shutil.copy2(src_img, dst_img)

    q_obj = {
        "id": f"t{test_num}_q{q_in_test}",
        "test": test_num,
        "part": part_num,
        "partName": part_name,
        "questionNum": q_in_test,
        "prompt": prompt,
        "audio": f"media/{audio_file}" if audio_file else None,
        "image": f"media/{image_file}" if image_file else None,
        "options": options,
        "correctAnswer": correct_ans,
        "explanation": explanation_clean
    }
    tests_data.append(q_obj)

print(f"\nParsed {len(tests_data)} questions successfully!")

# Summary by Test
for t in range(1, 5):
    t_qs = [q for q in tests_data if q["test"] == t]
    opts_cnt = sum(1 for q in t_qs if len(q["options"]) >= 3)
    imgs_cnt = sum(1 for q in t_qs if q["image"])
    auds_cnt = sum(1 for q in t_qs if q["audio"])
    print(f"Test {t}: {len(t_qs)} questions | with options: {opts_cnt} | with images: {imgs_cnt} | with audio: {auds_cnt}")

# Save to JSON
json_path = os.path.join(base_dir, "toeic_app_data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(tests_data, f, ensure_ascii=False, indent=2)
print(f"Saved: {json_path}")

# Save to JS for direct offline file:// loading without CORS issues
js_path = os.path.join(base_dir, "toeic_app_data.js")
with open(js_path, "w", encoding="utf-8") as f:
    f.write("// Dữ liệu câu hỏi TOEIC Listening Test 1, 2, 3, 4\n")
    f.write("window.TOEIC_DATA = ")
    json.dump(tests_data, f, ensure_ascii=False)
    f.write(";\n")
print(f"Saved: {js_path}")
