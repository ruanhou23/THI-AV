import zipfile
import xml.etree.ElementTree as ET
import sys
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with zipfile.ZipFile(r"Listening practice test 1\Listening practice test 1.docx", 'r') as z:
    xml_content = z.read('word/document.xml')
    root = ET.fromstring(xml_content)
    texts = []
    for p in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        p_text = "".join(t.text for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text)
        if p_text.strip():
            texts.append(p_text.strip())

print(f"Total paragraphs: {len(texts)}")
# Search for Question 35 to 70
for i, t in enumerate(texts):
    if "35" in t or "Questions 35" in t or "Question 35" in t or "32" in t:
        print(f"[{i}] {t[:80]}")
