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
    print(f"\n==================== TEST {t_num} ====================")
    # Find Q32 in full_text
    pos = full_text.find("Question 32")
    pos_end = full_text.find("Questions 38", pos)
    if pos != -1:
        snippet = full_text[pos:pos+1500] if pos_end == -1 else full_text[pos:pos_end]
        print(snippet)
