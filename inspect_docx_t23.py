import zipfile
import xml.etree.ElementTree as ET
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

for t in [2, 3]:
    fname = f"Listening practice test {t}/TOEIC_Test_{t}_Listening_Transcript.docx" if t==2 else f"Listening practice test {t}/TOEIC_Practice_Test_{t}_Listening_Transcript.docx"
    with zipfile.ZipFile(fname, 'r') as z:
        xml_content = z.read('word/document.xml')
        root = ET.fromstring(xml_content)
        texts = []
        for p in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            p_text = "".join(t.text for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text)
            if p_text.strip():
                texts.append(p_text.strip())
        print(f"\n=== Test {t} Docx ({len(texts)} paragraphs) ===")
        for line in texts[:12]:
            print(" ", line[:100])
