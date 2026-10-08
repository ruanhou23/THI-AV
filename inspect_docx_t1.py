import docx
import sys
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

doc = docx.Document(r"Listening practice test 1\Listening practice test 1.docx")
full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

print("Doc length:", len(full_text))
# Find questions 32 to 70
q_matches = list(re.finditer(r'(?:Questions?\s*(\d+)|(\d+)\.\s*[A-Z])', full_text))
print("Found question patterns:", len(q_matches))
print("First 500 chars of doc:")
print(full_text[:500])
