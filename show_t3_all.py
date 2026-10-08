with open("docx_dump_test3.txt", "r", encoding="utf-8") as f:
    text = f.read()

import re
convs = re.split(r"Questions?\s*(\d+)[–\-](\d+)", text)
# convs[0] is header, then (start, end, content)
print("Found conversations:", len(convs) // 3)
for i in range(1, len(convs), 3):
    s = convs[i]
    e = convs[i+1]
    body = convs[i+2].strip()
    print(f"\n==================== TEST 3: Q{s}-{e} ====================")
    lines = [l.strip() for l in body.split('\n') if l.strip()]
    for line in lines:
        print(line)
