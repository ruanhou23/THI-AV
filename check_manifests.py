import json

for t in [3, 4]:
    manifest = json.load(open(rf"Listening practice test {t}\audio_split\audio_split_manifest.json", encoding="utf-8"))
    p3 = manifest["parts"]["Part 3"]
    print(f"=== MANIFEST TEST {t} PART 3 ({len(p3)} segments) ===")
    for item in p3:
        print(f"  {item['questions']}: {item['file']} ({item['duration']:.1f}s, start: {item['start']:.1f}, end: {item['end']:.1f})")
