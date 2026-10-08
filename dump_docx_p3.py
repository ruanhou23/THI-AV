import zipfile, xml.etree.ElementTree as ET, re, sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

for t_num, doc_path in [(3, r"Listening practice test 3\TOEIC_Practice_Test_3_Listening_Transcript.docx"), (4, r"Listening practice test 4\TOEIC_Practice_Test_4_Listening_Transcript.docx")]:
    with zipfile.ZipFile(doc_path) as z:
        tree = ET.fromstring(z.read("word/document.xml"))
    texts = [node.text for node in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text]
    full_text = "\n".join(texts)
    
    out_file = f"docx_dump_test{t_num}.txt"
    pos = full_text.find("Questions 32")
    if pos != -1:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(full_text[pos:])
        print(f"Dumped Test {t_num} Part 3 to {out_file}, length {len(full_text[pos:])}")
