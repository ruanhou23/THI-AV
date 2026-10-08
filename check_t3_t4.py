import json

data = json.load(open("toeic_app_data.json", encoding="utf-8"))
for t in [3, 4]:
    tp3 = [q for q in data if q["test"] == t and q["part"] == 3]
    print(f"==================== TEST {t} PART 3 ({len(tp3)}) ====================")
    for q in tp3:
        print(f"Q{q['questionNum']}: {q['prompt']} -> Ans: {q['correctAnswer']}")
