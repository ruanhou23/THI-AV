import os
import re
import json

with open("TOEIC_Listening_Test1_anki.txt", "r", encoding="utf-8") as f:
    content = f.read()

lines = [line.strip() for line in content.split("\n") if line.strip() and not line.startswith("#")]

items = []
part1_counter = 1

for line in lines:
    parts = line.split("\t")
    if len(parts) < 2:
        continue
    front = parts[0]
    back = parts[1]
    
    # Identify part
    part_match = re.search(r"Part\s*(\d+)", front)
    part_num = int(part_match.group(1)) if part_match else 0
    
    # Identify number / question
    num_match = re.search(r"(?:Number|Questions?)\s*([\d–-]+)", front)
    q_num = num_match.group(1) if num_match else ""
    
    image_file = None
    if part_num == 1:
        image_file = f"image{part1_counter}.png"
        part1_counter += 1

    # Extract options
    options = re.findall(r"\(([A-D])\)\s*([^<]+)", front)
    
    # Extract answer
    ans_match = re.search(r"Đáp án:\s*\(?([A-D])\)?", back)
    correct_letter = ans_match.group(1) if ans_match else ""
    
    items.append({
        "id": len(items) + 1,
        "part": f"Part {part_num}",
        "partNum": part_num,
        "questionNum": q_num,
        "front": front,
        "back": back,
        "image": image_file,
        "correctOption": correct_letter,
        "options": [{"letter": opt[0], "text": opt[1].strip()} for opt in options]
    })

print(f"Parsed {len(items)} questions.")

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

# Generate Anki file with images for Part 1
anki_with_images_lines = [
    "#separator:tab",
    "#html:true",
    "#tags:TOEIC Listening Test1",
    ""
]

for item in items:
    front = item["front"]
    if item["image"]:
        front = f'<img src="{item["image"]}"><br><br>' + front
    anki_with_images_lines.append(f"{front}\t{item['back']}")

with open("TOEIC_Listening_Test1_with_images_anki.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(anki_with_images_lines) + "\n")

print("Generated TOEIC_Listening_Test1_with_images_anki.txt successfully.")
