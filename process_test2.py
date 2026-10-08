import zipfile
import xml.etree.ElementTree as ET
import os
import sys
import re
import shutil

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

docx_path = "Listening practice test 2/TOEIC_Test_2_Listening_Transcript.docx"

with zipfile.ZipFile(docx_path) as z:
    doc_xml = z.read('word/document.xml').decode('utf-8')
    rels_xml = z.read('word/_rels/document.xml.rels').decode('utf-8')
    
    # 1. Media mapping
    rel_to_media = dict(re.findall(r'Id="([^"]+)"[^>]*Target="media/([^"]+)"', rels_xml))
    ordered_rids = re.findall(r'r:embed="([^"]+)"', doc_xml)
    ordered_imgs = [rel_to_media.get(r) for r in ordered_rids if r in rel_to_media]
    print("Ordered images in Test 2:", ordered_imgs)
    
    # Extract images to local and anki media
    os.makedirs("test2_media", exist_ok=True)
    appdata = os.environ.get('APPDATA', '')
    anki_media = os.path.join(appdata, "Anki2", "Người dùng 1", "collection.media")
    
    for idx, img_name in enumerate(ordered_imgs):
        q_num = idx + 1
        img_data = z.read(f"word/media/{img_name}")
        target_name = f"test2_part1_q{q_num:02d}.png"
        
        # save local
        with open(os.path.join("test2_media", target_name), "wb") as f:
            f.write(img_data)
        # save anki
        if os.path.exists(anki_media):
            with open(os.path.join(anki_media, target_name), "wb") as f:
                f.write(img_data)
        print(f"Extracted image {q_num} -> {target_name}")

    # 2. Parse text content
    tree = ET.fromstring(doc_xml)
    w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    
    paragraphs = []
    for p in tree.iter(f'{w}p'):
        text = ''.join(p.itertext()).strip()
        if text:
            paragraphs.append(text)

print(f"\nTotal paragraphs: {len(paragraphs)}")
with open("test2_paragraphs.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(paragraphs))

print("Saved test2_paragraphs.txt for inspection.")
