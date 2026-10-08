import os
import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

base_dir = r"c:\Users\hau\Desktop\AV_THI\tachaudio"
out_dir = os.path.join(base_dir, "tach_theo_part")
os.makedirs(out_dir, exist_ok=True)

# Read 4 final test files
test_cards = {}
for t in range(1, 5):
    fname = os.path.join(base_dir, f"TOEIC_Listening_Test{t}_FINAL.txt")
    with open(fname, "r", encoding="utf-8") as f:
        cards = [l.strip() for l in f if '\t' in l]
    test_cards[t] = cards
    print(f"Test {t}: {len(cards)} cards loaded")

# Structure by Part
# Part 1: Q1 to Q6 (indices 0..5)
# Part 2: Q7 to Q31 (indices 6..30)
# Part 3: Q32 to Q70 (indices 31..69)

parts_data = {
    1: {"name": "Part 1 - Mô tả tranh (Photographs)", "slice": (0, 6), "expected": 6},
    2: {"name": "Part 2 - Hỏi & Đáp (Question - Response)", "slice": (6, 31), "expected": 25},
    3: {"name": "Part 3 - Đoạn hội thoại (Short Conversations)", "slice": (31, 70), "expected": 39}
}

# 1. TẠO 12 FILE THEO TỪNG TEST VÀ TỪNG PART
print("\n--- Tạo 12 file theo từng Test và từng Part ---")
for t in range(1, 5):
    cards = test_cards[t]
    for p_num, p_info in parts_data.items():
        start, end = p_info["slice"]
        p_cards = cards[start:end]
        
        filename = f"Test{t}_Part{p_num}.txt"
        filepath = os.path.join(out_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("#separator:tab\n")
            f.write("#html:true\n")
            f.write(f"#tags:TOEIC_Listening_Test{t} TOEIC_Part{p_num}\n\n")
            for c in p_cards:
                f.write(c + "\n")
        print(f"  [+] {filename}: {len(p_cards)} thẻ")

# 2. TẠO 3 FILE TỔNG HỢP THEO PART CHO CẢ 4 TEST
print("\n--- Tạo 3 file tổng hợp gom Part của cả 4 Test ---")
for p_num, p_info in parts_data.items():
    start, end = p_info["slice"]
    all_p_cards = []
    
    filename_all = f"TOEIC_Listening_ALL_Part{p_num}.txt"
    filepath_all = os.path.join(out_dir, filename_all)
    # Also save in base_dir for convenience
    filepath_base = os.path.join(base_dir, filename_all)
    
    with open(filepath_all, "w", encoding="utf-8") as f:
        f.write("#separator:tab\n")
        f.write("#html:true\n\n")
        for t in range(1, 5):
            f.write(f"#tags:TOEIC_Part{p_num} TOEIC_Listening_Test{t}\n")
            cards = test_cards[t]
            p_cards = cards[start:end]
            for c in p_cards:
                # Add [Test X] to the card title if not present to make it easy to identify
                front, back = c.split("\t")
                if not front.startswith(f"Test {t}") and not front.startswith(f"[Test {t}]"):
                    front_labeled = f"<b>[Test {t}]</b> " + front
                else:
                    front_labeled = front
                f.write(f"{front_labeled}\t{back}\n")
            f.write("\n")
            all_p_cards.extend(p_cards)
            
    # Copy to base_dir
    import shutil
    shutil.copy2(filepath_all, filepath_base)
    print(f"  [+] {filename_all}: {len(all_p_cards)} thẻ (Đủ cả 4 Test)")

print("\nHoàn tất tạo các file tách Part!")
