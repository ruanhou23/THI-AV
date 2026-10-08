import json
import re
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

with open('anki_reading_b1_all_tests.txt', 'r', encoding='utf-8') as f:
    cards = [l.strip() for l in f if '\t' in l]

print(f"Total reading cards: {len(cards)}")

reading_data = []

for idx, c in enumerate(cards, start=1):
    parts = c.split('\t')
    front = parts[0]
    back = parts[1]
    tag = parts[2] if len(parts) > 2 else ''

    # Test and Part
    m_tag = re.search(r'Reading::Test(\d+)::Part(\d+)', tag)
    if m_tag:
        test_num = int(m_tag.group(1))
        part_num = int(m_tag.group(2))
    else:
        test_num = ((idx - 1) // 50) + 1
        q_test_idx = ((idx - 1) % 50) + 1
        if q_test_idx <= 30: part_num = 1
        elif q_test_idx <= 46: part_num = 2
        else: part_num = 3

    q_in_test = ((idx - 1) % 50) + 1

    # Part name
    if part_num == 1:
        part_name = "Part 5 (Reading Part 1) - Incomplete Sentences (Điền vào câu)"
    elif part_num == 2:
        part_name = "Part 6 (Reading Part 2) - Text Completion (Điền đoạn văn)"
    else:
        part_name = "Part 7 (Reading Part 3) - Reading Comprehension (Đọc hiểu đoạn văn / hội thoại)"

    # Correct Answer
    m_ans = re.search(r'Đáp án(?:\s*đúng)?:\s*([A-D])', back)
    correct_ans = m_ans.group(1) if m_ans else ''

    # Options
    opt_matches = re.findall(r'(?:<br>|\n|^)\s*(?:\(([A-D])\)|([A-D])[\.\)])\s*([^<\n\r]+)', front)
    options = []
    for m in opt_matches:
        letter = m[0] or m[1]
        text = m[2].strip()
        options.append({'key': letter, 'text': text})

    # Find where options start in front to separate prompt/passage
    first_opt_pattern = re.search(r'(?:<br>|\n|^)\s*(?:\([A-D]\)|[A-D][\.\)])\s*', front)
    if first_opt_pattern:
        question_header_html = front[:first_opt_pattern.start()].strip()
    else:
        question_header_html = front.strip()

    # Clean up trailing <br>
    question_header_html = re.sub(r'(?:<br\s*/?>\s*)+$', '', question_header_html).strip()

    # Passage vs Prompt
    # In Part 3, there's often <b>Đoạn văn...</b> or <b>Đoạn chat...</b> followed by <b>Q_num. Question?</b>
    passage_html = ""
    prompt_text = ""

    if part_num == 3:
        # Split passage and question prompt
        m_q_split = re.search(r'(<br\s*/?>\s*)*<b>(\d+\.\s*[^<]+)</b>', question_header_html)
        if m_q_split:
            passage_html = question_header_html[:m_q_split.start()].strip()
            prompt_text = m_q_split.group(2).strip()
        else:
            prompt_text = question_header_html
    else:
        # Part 1 and Part 2
        # Header is like <b>[Test 1 - Part 1] Câu 1:</b><br>The document...
        m_title = re.search(r'<b>\[Test\s*\d+\s*-\s*Part\s*\d+\]\s*Câu\s*\d+:</b>\s*(?:<br\s*/?>)*\s*(.+)', question_header_html, flags=re.DOTALL)
        if m_title:
            prompt_text = m_title.group(1).strip()
        else:
            prompt_text = question_header_html

    q_obj = {
        "id": f"r_t{test_num}_q{q_in_test}",
        "skill": "reading",
        "test": test_num,
        "part": part_num,
        "partName": part_name,
        "questionNum": q_in_test,
        "passage": passage_html,
        "prompt": prompt_text,
        "audio": None,
        "image": None,
        "options": options,
        "correctAnswer": correct_ans,
        "explanation": back.strip()
    }
    reading_data.append(q_obj)

print(f"Parsed {len(reading_data)} reading questions successfully!")

# Summary
for t in range(1, 5):
    t_qs = [q for q in reading_data if q["test"] == t]
    p1 = sum(1 for q in t_qs if q["part"] == 1)
    p2 = sum(1 for q in t_qs if q["part"] == 2)
    p3 = sum(1 for q in t_qs if q["part"] == 3)
    print(f"Test {t}: {len(t_qs)} questions (Part 1: {p1}, Part 2: {p2}, Part 3: {p3})")

# Save JSON and JS
with open('toeic_reading_data.json', 'w', encoding='utf-8') as f:
    json.dump(reading_data, f, ensure_ascii=False, indent=2)

with open('toeic_reading_data.js', 'w', encoding='utf-8') as f:
    f.write("// Dữ liệu TOEIC Reading B1 (Test 1 - 4: 200 câu hỏi)\n")
    f.write("window.TOEIC_READING_DATA = ")
    json.dump(reading_data, f, ensure_ascii=False)
    f.write(";\n")

print("Saved toeic_reading_data.json & toeic_reading_data.js successfully!")
