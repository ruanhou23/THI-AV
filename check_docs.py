import zipfile, xml.etree.ElementTree as ET, sys

docs = [
    r"Listening practice test 1\Listening practice test 1.docx",
    r"Listening practice test 2\TOEIC_Test_2_Listening_Transcript.docx",
    r"Listening practice test 3\TOEIC_Practice_Test_3_Listening_Transcript.docx",
    r"Listening practice test 4\TOEIC_Practice_Test_4_Listening_Transcript.docx"
]

for idx, d in enumerate(docs, 1):
    try:
        with zipfile.ZipFile(d) as z:
            tree = ET.fromstring(z.read("word/document.xml"))
        texts = [node.text for node in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text]
        full_text = "\n".join(texts)
        print(f"=== DOC {idx}: {d} ===")
        print(f"Total length: {len(full_text)}")
        for target in ["Questions 32", "Questions 35", "Questions 68"]:
            pos = full_text.find(target)
            if pos != -1:
                print(f"--- {target} snippet ---")
                print(full_text[pos:pos+300].strip())
    except Exception as e:
        print(f"Error {d}: {e}")
