import json

test3_p3 = [
    {
        "id": "t3_q32", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 32,
        "prompt": "What change is a company making?",
        "audio": "media/test3_part3_c32_34.mp3", "image": None,
        "options": [
            {"key": "A", "text": "It is lowering some prices."},
            {"key": "B", "text": "It is hiring more staffers."},
            {"key": "C", "text": "It is moving to a new location."},
            {"key": "D", "text": "It is expanding a product line."}
        ],
        "correctAnswer": "C",
        "explanation": "<b>Đáp án đúng: (C) It is moving to a new location.</b><br><br><i>Transcript:</i> Man: \"The company's making a big change this year by moving offices. It's exciting that the new space will be much bigger.\"<br><br><b>Dịch nghĩa:</b> Người đàn ông nói công ty đang có sự thay đổi lớn năm nay là chuyển văn phòng sang địa điểm mới rộng rãi hơn."
    },
    {
        "id": "t3_q33", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 33,
        "prompt": "What suggestion does the woman make?",
        "audio": "media/test3_part3_c32_34.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Updating a handbook"},
            {"key": "B", "text": "Donating some furniture"},
            {"key": "C", "text": "Creating a schedule"},
            {"key": "D", "text": "Downloading a software program"}
        ],
        "correctAnswer": "B",
        "explanation": "<b>Đáp án đúng: (B) Donating some furniture.</b><br><br><i>Transcript:</i> Woman: \"Why don't we donate them? The Jebbrian Foundation is a local organization that picks up old furniture for donation.\"<br><br><b>Dịch nghĩa:</b> Người phụ nữ gợi ý quyên tặng bàn ghế cho một tổ chức từ thiện địa phương."
    },
    {
        "id": "t3_q34", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 34,
        "prompt": "What will the speakers most likely do next?",
        "audio": "media/test3_part3_c32_34.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Train a new employee"},
            {"key": "B", "text": "Review an application"},
            {"key": "C", "text": "Check a list"},
            {"key": "D", "text": "Talk to some directors"}
        ],
        "correctAnswer": "D",
        "explanation": "<b>Đáp án đúng: (D) Talk to some directors.</b><br><br><i>Transcript:</i> Man: \"That's a good idea. Let's talk to our directors to see what they think.\"<br><br><b>Dịch nghĩa:</b> Người đàn ông đề xuất trao đổi với các giám đốc để hỏi ý kiến của họ."
    },
    {
        "id": "t3_q35", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 35,
        "prompt": "Who most likely are the women?",
        "audio": "media/test3_part3_c35_37.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Company executives"},
            {"key": "B", "text": "Journalists"},
            {"key": "C", "text": "Health-care professionals"},
            {"key": "D", "text": "Safety inspectors"}
        ],
        "correctAnswer": "B",
        "explanation": "<b>Đáp án đúng: (B) Journalists.</b><br><br><i>Transcript:</i> Woman 1: \"Thanks for allowing us to cover the event for our newspaper. We really wanted to interview you as the organizer.\"<br><br><b>Dịch nghĩa:</b> Hai người phụ nữ là nhà báo/phóng viên đưa tin về hội chợ triển lãm y tế cho tòa soạn báo."
    },
    {
        "id": "t3_q36", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 36,
        "prompt": "What does the man say he is pleased about?",
        "audio": "media/test3_part3_c35_37.mp3", "image": None,
        "options": [
            {"key": "A", "text": "The number of event participants"},
            {"key": "B", "text": "The amount of money raised"},
            {"key": "C", "text": "The quality of vendors"},
            {"key": "D", "text": "The variety of presentations"}
        ],
        "correctAnswer": "A",
        "explanation": "<b>Đáp án đúng: (A) The number of event participants.</b><br><br><i>Transcript:</i> Man: \"I'm pleased to report that registration has increased this year. We have over 2,000 participants. It's our best turnout yet.\"<br><br><b>Dịch nghĩa:</b> Người đàn ông hài lòng vì số lượng người tham gia tăng lên hơn 2.000 người, đông nhất từ trước đến nay."
    },
    {
        "id": "t3_q37", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 37,
        "prompt": "What will the women do next?",
        "audio": "media/test3_part3_c35_37.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Watch a demonstration"},
            {"key": "B", "text": "Get some refreshments"},
            {"key": "C", "text": "Register for an event"},
            {"key": "D", "text": "Take a photograph"}
        ],
        "correctAnswer": "D",
        "explanation": "<b>Đáp án đúng: (D) Take a photograph.</b><br><br><i>Transcript:</i> Woman 1: \"can we get a photo of you in front of the poster for the show—the one on that wall? Man: Certainly.\"<br><br><b>Dịch nghĩa:</b> Người phụ nữ đề nghị chụp một bức ảnh người đàn ông đứng trước áp phích của sự kiện."
    },
    {
        "id": "t3_q38", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 38,
        "prompt": "What most likely is the woman's job?",
        "audio": "media/test3_part3_c38_40.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Professional chef"},
            {"key": "B", "text": "Bank executive"},
            {"key": "C", "text": "Administrative assistant"},
            {"key": "D", "text": "Web designer"}
        ],
        "correctAnswer": "D",
        "explanation": "<b>Đáp án đúng: (D) Web designer.</b><br><br><i>Transcript:</i> Woman: \"As you know, I've been redesigning Ace Bancorp's website to add new online banking functions.\"<br><br><b>Dịch nghĩa:</b> Người phụ nữ cho biết cô đang thiết kế lại trang web của ngân hàng để thêm các chức năng ngân hàng trực tuyến."
    },
    {
        "id": "t3_q39", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 39,
        "prompt": "What will the man most likely do?",
        "audio": "media/test3_part3_c38_40.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Buy some materials from the woman"},
            {"key": "B", "text": "Check the woman's work"},
            {"key": "C", "text": "List investment options"},
            {"key": "D", "text": "Update some client information"}
        ],
        "correctAnswer": "B",
        "explanation": "<b>Đáp án đúng: (B) Check the woman's work.</b><br><br><i>Transcript:</i> Woman: \"I wonder whether you could test out the redeveloped site for me. Man: I can do that... I'll make sure I check those.\"<br><br><b>Dịch nghĩa:</b> Người đàn ông đồng ý kiểm tra trang web vừa được tái phát triển cho người phụ nữ."
    },
    {
        "id": "t3_q40", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 40,
        "prompt": "What will the woman most likely send to the man?",
        "audio": "media/test3_part3_c38_40.mp3", "image": None,
        "options": [
            {"key": "A", "text": "A cost estimate"},
            {"key": "B", "text": "A revised schedule"},
            {"key": "C", "text": "A building plan"},
            {"key": "D", "text": "A list of changes"}
        ],
        "correctAnswer": "D",
        "explanation": "<b>Đáp án đúng: (D) A list of changes.</b><br><br><i>Transcript:</i> Man: \"Why don't you send me a list of the specific updates you made? I'll make sure I check those.\"<br><br><b>Dịch nghĩa:</b> Người đàn ông bảo người phụ nữ gửi danh sách những cập nhật/thay đổi cụ thể đã thực hiện trên trang web."
    }
]

with open("test3_p3_partA.json", "w", encoding="utf-8") as f:
    json.dump(test3_p3, f, ensure_ascii=False, indent=2)
print("Part A written successfully, count:", len(test3_p3))
