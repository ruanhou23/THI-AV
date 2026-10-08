import json

test3_p3 = [
    # Q41 - Q43 (Audio: media/test3_part3_c41_43.mp3)
    {
        "id": "t3_q41", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 41,
        "prompt": "Why is a train platform closed?",
        "audio": "media/test3_part3_c41_43.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Safety inspections are being conducted."},
            {"key": "B", "text": "New escalators are being installed."},
            {"key": "C", "text": "Tracks are being repaired."},
            {"key": "D", "text": "Waiting areas are being remodeled."}
        ],
        "correctAnswer": "C",
        "explanation": "<b>Đáp án đúng: (C) Tracks are being repaired.</b><br><br><i>Transcript:</i> Woman: \"Unfortunately, some tracks are being repaired, so no trains are departing from this platform.\"<br><br><b>Dịch nghĩa:</b> Đường ray tàu đang được sửa chữa nên ga tạm thời không có tàu khởi hành."
    },
    {
        "id": "t3_q42", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 42,
        "prompt": "What does the man say he is upset about?",
        "audio": "media/test3_part3_c41_43.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Misunderstanding some instructions"},
            {"key": "B", "text": "Being late for an appointment"},
            {"key": "C", "text": "Losing a travel pass"},
            {"key": "D", "text": "Boarding the wrong train"}
        ],
        "correctAnswer": "B",
        "explanation": "<b>Đáp án đúng: (B) Being late for an appointment.</b><br><br><i>Transcript:</i> Man: \"I had no idea this was happening, and I'm upset that now I'm late for an appointment.\"<br><br><b>Dịch nghĩa:</b> Người đàn ông bực bội vì sự cố này khiến anh ta bị muộn cuộc hẹn."
    },
    {
        "id": "t3_q43", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 43,
        "prompt": "What will the man most likely do next?",
        "audio": "media/test3_part3_c41_43.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Purchase a snack"},
            {"key": "B", "text": "Take a shuttle bus"},
            {"key": "C", "text": "File a complaint"},
            {"key": "D", "text": "Download a map"}
        ],
        "correctAnswer": "B",
        "explanation": "<b>Đáp án đúng: (B) Take a shuttle bus.</b><br><br><i>Transcript:</i> Woman: \"Well, they're providing free bus service to the next few stations. You can catch a shuttle bus from the south side of the station.\"<br><br><b>Dịch nghĩa:</b> Người đàn ông sẽ đi xe buýt trung chuyển (shuttle bus) miễn phí ở phía nam nhà ga."
    },

    # Q44 - Q46 (Audio: media/test3_part3_c44_46.mp3)
    {
        "id": "t3_q44", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 44,
        "prompt": "Why does the man call the woman?",
        "audio": "media/test3_part3_c44_46.mp3", "image": None,
        "options": [
            {"key": "A", "text": "To provide an update on his project"},
            {"key": "B", "text": "To get approval on some design changes"},
            {"key": "C", "text": "To receive the woman's feedback on a prototype"},
            {"key": "D", "text": "To persuade the woman to invest in his business"}
        ],
        "correctAnswer": "D",
        "explanation": "<b>Đáp án đúng: (D) To persuade the woman to invest in his business.</b><br><br><i>Transcript:</i> Woman: \"I understand from your email that you're looking for investors in your business. Man: Yes.\"<br><br><b>Dịch nghĩa:</b> Người đàn ông gọi điện để thuyết phục người phụ nữ đầu tư vào dự án kinh doanh giá để xe đạp trong nhà của anh ấy."
    },
    {
        "id": "t3_q45", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 45,
        "prompt": "According to the man, what is unique about a product?",
        "audio": "media/test3_part3_c44_46.mp3", "image": None,
        "options": [
            {"key": "A", "text": "It is inexpensive."},
            {"key": "B", "text": "It is easy to assemble."},
            {"key": "C", "text": "It is adjustable."},
            {"key": "D", "text": "It is lightweight."}
        ],
        "correctAnswer": "C",
        "explanation": "<b>Đáp án đúng: (C) It is adjustable.</b><br><br><i>Transcript:</i> Man: \"Most indoor racks are one size, but not all bikes are the same. My product can be adjusted to suit different types of bicycles.\"<br><br><b>Dịch nghĩa:</b> Điểm độc đáo của sản phẩm là có thể điều chỉnh linh hoạt cho phù hợp với nhiều loại xe đạp."
    },
    {
        "id": "t3_q46", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 46,
        "prompt": "Why does the woman request some documents?",
        "audio": "media/test3_part3_c44_46.mp3", "image": None,
        "options": [
            {"key": "A", "text": "To open a customer account"},
            {"key": "B", "text": "To issue a certificate"},
            {"key": "C", "text": "To make some copies"},
            {"key": "D", "text": "To evaluate a proposal"}
        ],
        "correctAnswer": "D",
        "explanation": "<b>Đáp án đúng: (D) To evaluate a proposal.</b><br><br><i>Transcript:</i> Woman: \"Send me your business model. I need to determine if you have a reasonable plan for expanding production and increasing sales before I make any decisions.\"<br><br><b>Dịch nghĩa:</b> Người phụ nữ yêu cầu gửi bản mô hình kinh doanh để đánh giá bản đề xuất trước khi quyết định đầu tư."
    },

    # Q47 - Q49 (Audio: media/test3_part3_c47_49.mp3)
    {
        "id": "t3_q47", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 47,
        "prompt": "What are the speakers preparing for?",
        "audio": "media/test3_part3_c47_49.mp3", "image": None,
        "options": [
            {"key": "A", "text": "A construction-site visit"},
            {"key": "B", "text": "A safety inspection"},
            {"key": "C", "text": "An interview"},
            {"key": "D", "text": "A film festival"}
        ],
        "correctAnswer": "C",
        "explanation": "<b>Đáp án đúng: (C) An interview.</b><br><br><i>Transcript:</i> Woman: \"Alberto, it's time to leave the studio and head over to the Central Bank for our interview with the director.\"<br><br><b>Dịch nghĩa:</b> Hai người đang chuẩn bị máy quay phim để đến Ngân hàng Trung ương thực hiện một cuộc phỏng vấn giám đốc."
    },
    {
        "id": "t3_q48", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 48,
        "prompt": "What is the woman concerned about?",
        "audio": "media/test3_part3_c47_49.mp3", "image": None,
        "options": [
            {"key": "A", "text": "A lighting issue"},
            {"key": "B", "text": "A script mistake"},
            {"key": "C", "text": "A material shortage"},
            {"key": "D", "text": "A revenue decrease"}
        ],
        "correctAnswer": "A",
        "explanation": "<b>Đáp án đúng: (A) A lighting issue.</b><br><br><i>Transcript:</i> Woman: \"And make sure you have the special low-light lenses. I'm concerned about the poor lighting at the bank. It's pretty dark in there...\"<br><br><b>Dịch nghĩa:</b> Người phụ nữ lo lắng về điều kiện ánh sáng yếu tại ngân hàng sẽ làm hỏng khung hình."
    },
    {
        "id": "t3_q49", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 49,
        "prompt": "Who is Marcel Lambert?",
        "audio": "media/test3_part3_c47_49.mp3", "image": None,
        "options": [
            {"key": "A", "text": "A company accountant"},
            {"key": "B", "text": "A possible client"},
            {"key": "C", "text": "A supervisor"},
            {"key": "D", "text": "An intern"}
        ],
        "correctAnswer": "D",
        "explanation": "<b>Đáp án đúng: (D) An intern.</b><br><br><i>Transcript:</i> Man: \"And by the way, our new intern Marcel Lambert is interested in joining us.\"<br><br><b>Dịch nghĩa:</b> Marcel Lambert là một thực tập sinh mới của công ty."
    },

    # Q50 - Q52 (Audio: media/test3_part3_c50_52.mp3)
    {
        "id": "t3_q50", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 50,
        "prompt": "What does the woman thank the man for?",
        "audio": "media/test3_part3_c50_52.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Distributing some fliers"},
            {"key": "B", "text": "Completing some calculations"},
            {"key": "C", "text": "Placing a catering order"},
            {"key": "D", "text": "Preparing some paper copies"}
        ],
        "correctAnswer": "D",
        "explanation": "<b>Đáp án đúng: (D) Preparing some paper copies.</b><br><br><i>Transcript:</i> Woman: \"Waseem, I know you've been very busy this morning, but did you have time to take care of the photocopies I asked for? Man: Oh, yes. Those are all ready. Woman: Excellent, thanks.\"<br><br><b>Dịch nghĩa:</b> Người phụ nữ cảm ơn vì người đàn ông đã chuẩn bị xong các bản photocopy tài liệu giấy."
    },
    {
        "id": "t3_q51", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 51,
        "prompt": "Why is a gathering being planned?",
        "audio": "media/test3_part3_c50_52.mp3", "image": None,
        "options": [
            {"key": "A", "text": "A colleague was promoted."},
            {"key": "B", "text": "The company won an award."},
            {"key": "C", "text": "A colleague will be retiring."},
            {"key": "D", "text": "The company will be training employees."}
        ],
        "correctAnswer": "C",
        "explanation": "<b>Đáp án đúng: (C) A colleague will be retiring.</b><br><br><i>Transcript:</i> Woman: \"By the way, how are the preparations coming along for Sabine Hoffmann's retirement party?\"<br><br><b>Dịch nghĩa:</b> Buổi gặp mặt được tổ chức để chia tay đồng nghiệp Sabine Hoffmann nghỉ hưu."
    },
    {
        "id": "t3_q52", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 52,
        "prompt": "What does the man imply when he says, \"I've booked conference room B\"?",
        "audio": "media/test3_part3_c50_52.mp3", "image": None,
        "options": [
            {"key": "A", "text": "He will need to reserve a larger room."},
            {"key": "B", "text": "A meeting was rescheduled."},
            {"key": "C", "text": "Conference room B is currently occupied."},
            {"key": "D", "text": "Audio equipment is missing."}
        ],
        "correctAnswer": "A",
        "explanation": "<b>Đáp án đúng: (A) He will need to reserve a larger room.</b><br><br><i>Transcript:</i> Woman: \"I'm sure she would love to celebrate with her former colleagues from other teams as well... Man: Sure. I've booked conference room B, but I'll go ahead and change that.\"<br><br><b>Dịch nghĩa:</b> Vì sẽ mời thêm nhiều đồng nghiệp từ các nhóm khác nên phòng họp B sẽ không đủ chỗ, anh ấy ngụ ý sẽ đổi sang phòng lớn hơn."
    },

    # Q53 - Q55 (Audio: media/test3_part3_c53_55.mp3)
    {
        "id": "t3_q53", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 53,
        "prompt": "What type of event is the man planning?",
        "audio": "media/test3_part3_c53_55.mp3", "image": None,
        "options": [
            {"key": "A", "text": "An awards ceremony"},
            {"key": "B", "text": "A company retreat"},
            {"key": "C", "text": "A product exhibition"},
            {"key": "D", "text": "A press conference"}
        ],
        "correctAnswer": "B",
        "explanation": "<b>Đáp án đúng: (B) A company retreat.</b><br><br><i>Transcript:</i> Man: \"I have an appointment with Ms. Ishikawa to view your hotel facilities for my company's upcoming retreat.\"<br><br><b>Dịch nghĩa:</b> Người đàn ông đang lên kế hoạch cho chuyến nghỉ dưỡng/dã ngoại của công ty (company retreat)."
    },
    {
        "id": "t3_q54", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 54,
        "prompt": "Why was Ms. Ishikawa delayed?",
        "audio": "media/test3_part3_c53_55.mp3", "image": None,
        "options": [
            {"key": "A", "text": "She was stuck in traffic."},
            {"key": "B", "text": "She was at lunch."},
            {"key": "C", "text": "She was setting up a room."},
            {"key": "D", "text": "She was on the phone."}
        ],
        "correctAnswer": "D",
        "explanation": "<b>Đáp án đúng: (D) She was on the phone.</b><br><br><i>Transcript:</i> Woman 1: \"I know that she's been expecting you, and she just wrapped up an urgent phone call. She's on her way now.\"<br><br><b>Dịch nghĩa:</b> Cô Ishikawa bị trễ một chút vì vừa phải kết thúc một cuộc điện thoại khẩn cấp."
    },
    {
        "id": "t3_q55", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 55,
        "prompt": "What does the man inquire about?",
        "audio": "media/test3_part3_c53_55.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Internet access in guest rooms"},
            {"key": "B", "text": "Room pricing discounts"},
            {"key": "C", "text": "Catering menus"},
            {"key": "D", "text": "Airport transportation"}
        ],
        "correctAnswer": "A",
        "explanation": "<b>Đáp án đúng: (A) Internet access in guest rooms.</b><br><br><i>Transcript:</i> Man: \"And I'd also like to look at the guest rooms. All the rooms have a high-speed Internet connection, right?\"<br><br><b>Dịch nghĩa:</b> Người đàn ông hỏi về kết nối Internet tốc độ cao trong các phòng nghỉ của khách."
    }
]

with open("test3_p3_partB.json", "w", encoding="utf-8") as f:
    json.dump(test3_p3, f, ensure_ascii=False, indent=2)
print("Part B written successfully, count:", len(test3_p3))
