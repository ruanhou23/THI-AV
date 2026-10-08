import json, zipfile, xml.etree.ElementTree as ET

# Read Test 1 docx
with zipfile.ZipFile(r"Listening practice test 1\Listening practice test 1.docx") as z:
    tree = ET.fromstring(z.read("word/document.xml"))
texts = [node.text for node in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text]
full_text = "\n".join(texts)

data = json.load(open("toeic_app_data.json", encoding="utf-8"))
t1_p3 = [q for q in data if q["test"] == 1 and q["part"] == 3]

print("=== CHECKING TEST 1 PART 3 ===")
# Check for each conversation
ranges = [
    (32, 34), (35, 37), (38, 40), (41, 43), (44, 46),
    (47, 49), (50, 52), (53, 55), (56, 58), (59, 61),
    (62, 64), (65, 67), (68, 70)
]
for start_q, end_q in ranges:
    tag = f"Questions {start_q}"
    pos = full_text.find(tag)
    # Check questions in data
    qs = [q for q in t1_p3 if start_q <= q["questionNum"] <= end_q]
    print(f"\nConversation Q{start_q}-{end_q}:")
    if pos != -1:
        snippet = full_text[pos:pos+250].replace('\n', ' ')
        print(f"  Transcript: {snippet[:120]}...")
    for q in qs:
        print(f"  App Q{q['questionNum']}: {q['prompt']} | Ans: {q['correctAnswer']} | Opt A: {q['options'][0]['text'] if q['options'] else 'None'}")
