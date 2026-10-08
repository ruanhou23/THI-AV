import json

data = json.load(open("toeic_app_data.json", encoding="utf-8"))
t1_p3 = [q for q in data if q["test"] == 1 and q["part"] == 3]

print(f"Total T1 P3: {len(t1_p3)}")
for q in t1_p3:
    print(f"Q{q['questionNum']}: {q['prompt']} -> Ans: {q['correctAnswer']}")
