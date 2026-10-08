import zipfile, xml.etree.ElementTree as ET, re

for t_num, doc_path in [(1, r"Listening practice test 1\Listening practice test 1.docx"), (2, r"Listening practice test 2\TOEIC_Test_2_Listening_Transcript.docx")]:
    with zipfile.ZipFile(doc_path) as z:
        tree = ET.fromstring(z.read("word/document.xml"))
    texts = [node.text for node in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text]
    full_text = "\n".join(texts)
    print(f"==================== TEST {t_num} ====================")
    # Check if there are answers at the end of the docx!
    for kw in ["Answer Key", "Key", "Answers", "ĐÁP ÁN", "Đáp án", "ANSWER"]:
        pos = full_text.find(kw)
        if pos != -1:
            print(f"Found keyword '{kw}' at {pos}:")
            print(full_text[pos:pos+400])
