import zipfile, xml.etree.ElementTree as ET, re

for t_num, doc_path in [(3, r"Listening practice test 3\TOEIC_Practice_Test_3_Listening_Transcript.docx"), (4, r"Listening practice test 4\TOEIC_Practice_Test_4_Listening_Transcript.docx")]:
    with zipfile.ZipFile(doc_path) as z:
        tree = ET.fromstring(z.read("word/document.xml"))
    texts = [node.text for node in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text]
    full_text = "\n".join(texts)
    print(f"\n==================== TEST {t_num} ====================")
    # Find all question blocks: Question XX: ... up to next Question or Questions
    q_nums = re.findall(r"Question\s*(\d+):", full_text)
    print("Found Question numbers:", q_nums)
    
    # Check how many have (A) (B) (C) (D)
    has_opts = 0
    for q in range(32, 71):
        pos = full_text.find(f"Question {q}:")
        if pos != -1:
            snippet = full_text[pos:pos+400]
            if "(A)" in snippet and "(B)" in snippet:
                has_opts += 1
            else:
                print(f"  Q{q} MISSING OPTIONS! Snippet: {snippet[:100]}")
    print(f"Total Part 3 questions with options in docx: {has_opts}/39")
