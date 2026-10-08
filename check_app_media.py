import json
import os

with open('toeic_app_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

media_files = set(os.listdir('media'))
missing = []

for q in data:
    img = q.get('image')
    aud = q.get('audio')
    if img:
        fname = os.path.basename(img)
        if fname not in media_files:
            missing.append(('img', q['id'], fname))
    if aud:
        fname = os.path.basename(aud)
        if fname not in media_files:
            missing.append(('aud', q['id'], fname))

print(f"Total questions: {len(data)}")
print(f"Missing media references: {len(missing)}")
if missing:
    for m in missing[:15]:
        print(" ", m)
