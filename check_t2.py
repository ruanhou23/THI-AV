import json

data = json.load(open("toeic_app_data.json", encoding="utf-8"))
t2_p3 = [q for q in data if q["test"] == 2 and q["part"] == 3]

print(f"Total T2 P3: {len(t2_p3)}")
for q in t2_p3:
    print(f"Q{q['questionNum']}: {q['prompt']} -> Ans: {q['correctAnswer']}")
