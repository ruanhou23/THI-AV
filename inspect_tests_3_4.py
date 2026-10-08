import zipfile
import xml.etree.ElementTree as ET
import os
import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

for t in [3, 4]:
    folder = f"Listening practice test {t}"
    docx = [f for f in os.listdir(folder) if f.endswith('.docx')][0]
    full_path = os.path.join(folder, docx)
    print(f"\n=================== TEST {t}: {docx} ===================")
    with zipfile.ZipFile(full_path) as z:
        doc_xml = z.read('word/document.xml').decode('utf-8')
        rels_xml = z.read('word/_rels/document.xml.rels').decode('utf-8')
        
        rel_to_media = dict(re.findall(r'Id="([^"]+)"[^>]*Target="media/([^"]+)"', rels_xml))
        ordered_rids = re.findall(r'r:embed="([^"]+)"', doc_xml)
        ordered_imgs = [rel_to_media.get(r) for r in ordered_rids if r in rel_to_media]
        print(f"Ordered images: {ordered_imgs}")

        tree = ET.fromstring(doc_xml)
        w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        paragraphs = []
        for p in tree.iter(f'{w}p'):
            txt = ''.join(p.itertext()).strip()
            if txt:
                paragraphs.append(txt)
        
        print(f"Total paragraphs: {len(paragraphs)}")
        out_txt = f"test{t}_paragraphs.txt"
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write("\n".join(paragraphs))
        print(f"Saved {out_txt}")
