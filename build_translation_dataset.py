import json
import re
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

with open('toeic_app_data.json', 'r', encoding='utf-8') as f:
    listening_qs = json.load(f)

with open('toeic_reading_data.json', 'r', encoding='utf-8') as f:
    reading_qs = json.load(f)

vocab_dict = {
    "insert": ("chèn, cắm vào", "v"),
    "cord": ("dây điện, dây cáp", "n"),
    "outlet": ("ổ cắm điện", "n"),
    "bench": ("ghế dài ngoài trời", "n"),
    "picnic area": ("khu vực dã ngoại ngoài trời", "n"),
    "shovel": ("xúc, cào tuyết", "v"),
    "walkway": ("lối đi bộ", "n"),
    "gallery": ("phòng trưng bày nghệ thuật", "n"),
    "cushion": ("gối đệm tựa", "n"),
    "rack": ("giá, kệ treo đồ", "n"),
    "display": ("trưng bày", "v"),
    "suspended": ("treo lơ lửng", "adj"),
    "shutter": ("cửa chớp", "n"),
    "clear off": ("dọn dẹp sạch sẽ", "v"),
    "utensil": ("dụng cụ ăn uống/nhà bếp", "n"),
    "discard": ("bỏ đi, vứt bỏ", "v"),
    "rolling chair": ("ghế xoay có bánh xe", "n"),
    "canopy": ("mái che, rạp bạt", "n"),
    "luggage": ("hành lý", "n"),
    "escalator": ("thang cuốn", "n"),
    "work order": ("yêu cầu sửa chữa/công việc", "n"),
    "tenant": ("người thuê nhà/căn hộ", "n"),
    "vendor": ("nhà cung cấp", "n"),
    "maintenance": ("bảo trì, sửa chữa", "n"),
    "budget": ("ngân sách", "n"),
    "increase": ("tăng lên", "v"),
    "reschedule": ("dời lịch, xếp lại lịch", "v"),
    "demonstration": ("buổi trình diễn, chạy thử", "n"),
    "innovative": ("đổi mới, sáng tạo", "adj"),
    "feature": ("tính năng, đặc điểm", "n"),
    "warranty": ("bảo hành", "n"),
    "brochure": ("tờ rơi, tập gấp thông tin", "n"),
    "dock": ("cập bến, cập cảng", "v"),
    "port": ("bến cảng", "n"),
    "delay": ("trì hoãn, chậm trễ", "n"),
    "machinery": ("máy móc, thiết bị", "n"),
    "engine room": ("buồng máy", "n"),
    "fitness": ("thể dục, thể hình", "n"),
    "discount": ("giảm giá", "n"),
    "facility": ("cơ sở vật chất", "n"),
    "restoration": ("sự phục chế, trùng tu", "n"),
    "acquire": ("thu nhận, mua lại", "v"),
    "investigate": ("điều tra, nghiên cứu kỹ", "v"),
    "color palette": ("bảng màu", "n"),
    "anniversary": ("lễ kỷ niệm", "n"),
    "presentation": ("bài thuyết trình", "n"),
    "experiment": ("thí nghiệm", "n"),
    "congratulate": ("chúc mừng", "v"),
    "commercial": ("thương mại", "adj"),
    "irrigation": ("hệ thống tưới tiêu", "n"),
    "convention": ("hội nghị, đại hội", "n"),
    "seedling": ("cây giống", "n"),
    "excavate": ("khai quật", "v"),
    "archaeologist": ("nhà khảo cổ học", "n"),
    "thunderstorm": ("bão sấm sét", "n"),
    "requested": ("được yêu cầu", "adj"),
    "appropriately": ("một cách phù hợp, thích hợp", "adv"),
    "schedule": ("lên lịch trình", "v"),
    "delivery": ("sự giao hàng", "n"),
    "assembly": ("sự lắp ráp", "n"),
    "manufacture": ("sản xuất", "v"),
    "enrollment": ("sự ghi danh, đăng ký học", "n"),
    "accessible": ("dễ dàng tiếp cận", "adj"),
    "record": ("hồ sơ ghi chép", "n"),
    "banquet": ("tiệc chiêu đãi lớn", "n"),
    "shareholder": ("cổ đông", "n"),
    "beverage": ("đồ uống, giải khát", "n"),
    "enlarge": ("mở rộng", "v"),
    "workforce": ("lực lượng lao động", "n"),
    "certified": ("được chứng nhận", "adj"),
    "mountain": ("ngọn núi, dãy núi", "n"),
    "in the distance": ("ở phía xa xa", "phrase"),
    "arrange": ("sắp xếp, cắm (hoa)", "v"),
    "vase": ("bình hoa, lọ hoa", "n"),
    "guitar": ("đàn ghi-ta", "n"),
    "fireplace": ("lò sưởi", "n")
}

def clean_html(text):
    return re.sub(r'<[^>]+>', ' ', text).strip()

def extract_vocab(text):
    words = []
    text_lower = text.lower()
    for k, (meaning, pos) in vocab_dict.items():
        if k in text_lower:
            words.append({"word": f"{k} ({pos})", "meaning": meaning})
            if len(words) >= 4:
                break
    return words

translation_cards = []

# 1. PROCESS LISTENING (280 questions)
for q in listening_qs:
    part = q["part"]
    test = q["test"]
    q_num = q["questionNum"]
    qid = q["id"]
    audio = q.get("audio")
    image = q.get("image")
    exp = q.get("explanation", "")
    
    exp_clean = clean_html(exp)
    vi_match = re.search(r'(?:Dịch nghĩa|Giải thích|Ngữ cảnh)\s*:\s*(.+)', exp_clean)
    if vi_match:
        vi_sentence = vi_match.group(1).strip()
    else:
        vi_sentence = re.sub(r'^Đáp án(?:\s*đúng)?:\s*\([A-D]\)\s*', '', exp_clean).strip()

    if part == 1:
        correct_key = q.get("correctAnswer", "A")
        correct_opt = next((o["text"] for o in q.get("options", []) if o["key"] == correct_key), "")
        en_sentence = f"({correct_key}) {correct_opt}"
        grammar_note = "📌 Cấu trúc mô tả tranh TOEIC: S + is/are + V-ing (mô tả hành động của người) hoặc S + have/has been + V3/ed (mô tả trạng thái của đồ vật)."
        context_note = f"Listening Part 1 (Test {test} - Câu {q_num})"
    elif part == 2:
        prompt = q.get("prompt", "")
        correct_key = q.get("correctAnswer", "A")
        correct_opt = next((o["text"] for o in q.get("options", []) if o["key"] == correct_key), "")
        en_sentence = f"Q: \"{prompt}\"\n→ ({correct_key}) \"{correct_opt}\""
        grammar_note = "📌 Kỹ thuật Part 2: Nhận diện câu hỏi WH-question (Who, Where, When, Why, How), Yes/No question, câu hỏi lựa chọn (Or) hoặc câu gián tiếp."
        context_note = f"Listening Part 2 (Test {test} - Câu {q_num})"
    else:
        prompt = q.get("prompt", "")
        m_trans = re.search(r'(?:Transcript(?: trích đoạn)?:\s*</i>?\s*["“]?)([^"”<]+)', exp)
        transcript_snippet = m_trans.group(1).strip() if m_trans else ""
        correct_key = q.get("correctAnswer", "")
        correct_opt = next((o["text"] for o in q.get("options", []) if o["key"] == correct_key), "")
        if transcript_snippet:
            en_sentence = f"\"{transcript_snippet}\"\n(Hỏi: {prompt} → Đáp án: {correct_opt})"
        else:
            en_sentence = f"Question {q_num}: {prompt}\n→ ({correct_key}) {correct_opt}"
        grammar_note = "📌 Kỹ thuật Part 3: Chú ý kỹ năng Paraphrasing (từ đồng nghĩa giữa nội dung hội thoại và đáp án trắc nghiệm)."
        context_note = f"Listening Part 3 (Test {test} - Câu {q_num})"

    translation_cards.append({
        "id": f"trans_{qid}",
        "skill": "listening",
        "test": test,
        "part": part,
        "questionNum": q_num,
        "en": en_sentence,
        "vi": vi_sentence,
        "audio": audio,
        "image": image,
        "vocabulary": extract_vocab(en_sentence),
        "grammar": grammar_note,
        "context": context_note
    })

# 2. PROCESS READING (200 questions)
for q in reading_qs:
    part = q["part"]
    test = q["test"]
    q_num = q["questionNum"]
    qid = q["id"]
    exp = q.get("explanation", "")
    prompt = q.get("prompt", "")
    correct_key = q.get("correctAnswer", "")
    correct_opt = next((o["text"] for o in q.get("options", []) if o["key"] == correct_key), "")
    
    # Check if there is complete sentence in exp
    m_comp = re.search(r'Câu hoàn chỉnh:</i>\s*(?:<br\s*/?>)*\s*(.+)', exp)
    if m_comp:
        en_sentence = clean_html(m_comp.group(1))
    else:
        # replace blank in prompt with correct option
        en_sentence = re.sub(r'\(?\d+\)?\s*_{3,}', f"[{correct_opt}]", prompt)
        if en_sentence == prompt and '_______' in prompt:
            en_sentence = prompt.replace('_______', f"[{correct_opt}]")

    # Vietnamese explanation / meaning
    m_vi = re.search(r'(?:Giải thích:|Dịch nghĩa:)\s*(.+)', exp)
    if m_vi:
        vi_sentence = clean_html(m_vi.group(1))
    else:
        vi_sentence = clean_html(exp)

    grammar_note = "📌 Kỹ thuật TOEIC Reading: Xác định thành phần câu (S + V + O), thì của động từ, loại từ (N, V, Adj, Adv) cần điền vào chỗ trống."
    context_note = f"Reading Part {part} (Test {test} - Câu {q_num})"

    translation_cards.append({
        "id": f"trans_{qid}",
        "skill": "reading",
        "test": test,
        "part": part,
        "questionNum": q_num,
        "en": en_sentence,
        "vi": vi_sentence,
        "audio": None,
        "image": None,
        "vocabulary": extract_vocab(en_sentence),
        "grammar": grammar_note,
        "context": context_note
    })

print(f"Total translation cards: {len(translation_cards)} (Listening: 280, Reading: 200)")

# Save to JS and JSON
with open('toeic_translation_data.js', 'w', encoding='utf-8') as f:
    f.write("// Dữ liệu Luyện Dịch Câu Song Ngữ TOEIC (Listening: 280 + Reading: 200 = 480 câu)\n")
    f.write("window.TRANSLATION_DATA = ")
    json.dump(translation_cards, f, ensure_ascii=False)
    f.write(";\n")

with open('toeic_translation_data.json', 'w', encoding='utf-8') as f:
    json.dump(translation_cards, f, ensure_ascii=False, indent=2)

print("Saved toeic_translation_data.js & toeic_translation_data.json successfully!")
