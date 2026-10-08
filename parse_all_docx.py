import zipfile, xml.etree.ElementTree as ET, re

docs = [
    (1, r"Listening practice test 1\Listening practice test 1.docx"),
    (2, r"Listening practice test 2\TOEIC_Test_2_Listening_Transcript.docx"),
    (3, r"Listening practice test 3\TOEIC_Practice_Test_3_Listening_Transcript.docx"),
    (4, r"Listening practice test 4\TOEIC_Practice_Test_4_Listening_Transcript.docx")
]

for t_num, doc_path in docs:
    with zipfile.ZipFile(doc_path) as z:
        tree = ET.fromstring(z.read("word/document.xml"))
    texts = [node.text for node in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text]
    full_text = "\n".join(texts)
    
    # Find all "Questions XX-YY" in the doc
    q_ranges = re.findall(r"Questions?\s*(\d+)[–\-](\d+)", full_text)
    print(f"=== TEST {t_num} ({doc_path}) ===")
    print("Question ranges found in docx:", q_ranges[:15])
    
    # Check if docx has Questions and Options (A) (B) (C) (D)
    q_matches = re.findall(r"Question\s*(\d+):?\s*([^\n\r]+)", full_text)
    print(f"Questions found: {len(q_matches)}")
    if q_matches:
        for q_id, q_text in q_matches[:4]:
            print(f"  Q{q_id}: {q_text[:80]}")
