import os, glob, re

target = "Where most likely are the speakers"
for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith((".txt", ".docx", ".json", ".js")):
            p = os.path.join(root, f)
            try:
                content = open(p, "r", encoding="utf-8", errors="ignore").read()
                if target in content:
                    print(f"Found '{target}' in: {p}")
            except:
                pass
