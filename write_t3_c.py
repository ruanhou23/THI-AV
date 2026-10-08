import json

test3_p3 = [
    # Q56 - Q58 (Audio: media/test3_part3_c56_58.mp3)
    {
        "id": "t3_q56", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 56,
        "prompt": "Where does the conversation most likely take place?",
        "audio": "media/test3_part3_c56_58.mp3", "image": None,
        "options": [
            {"key": "A", "text": "At a supermarket / grocery store"},
            {"key": "B", "text": "At a restaurant kitchen"},
            {"key": "C", "text": "At a farm warehouse"},
            {"key": "D", "text": "At an appliance factory"}
        ],
        "correctAnswer": "A",
        "explanation": "<b>Đáp án đúng: (A) At a supermarket / grocery store.</b><br><br><i>Transcript:</i> Woman: \"Sales of pineapples have gone up a lot this month at our store... machine we installed in the fruit aisle.\"<br><br><b>Dịch nghĩa:</b> Cuộc hội thoại diễn ra tại một cửa hàng thực phẩm/siêu thị nơi có quầy trái cây."
    },
    {
        "id": "t3_q57", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 57,
        "prompt": "What does the man say is popular?",
        "audio": "media/test3_part3_c56_58.mp3", "image": None,
        "options": [
            {"key": "A", "text": "A coupon promotion"},
            {"key": "B", "text": "A fruit-peeling machine"},
            {"key": "C", "text": "An organic fruit brand"},
            {"key": "D", "text": "A store loyalty card"}
        ],
        "correctAnswer": "B",
        "explanation": "<b>Đáp án đúng: (B) A fruit-peeling machine.</b><br><br><i>Transcript:</i> Man: \"It must be the pineapple peeling machine we installed in the fruit aisle. Customers like watching it peel and slice their pineapple for them.\"<br><br><b>Dịch nghĩa:</b> Chiếc máy gọt và cắt dứa tự động được khách hàng rất yêu thích."
    },
    {
        "id": "t3_q58", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 58,
        "prompt": "What does the man suggest doing?",
        "audio": "media/test3_part3_c56_58.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Purchasing more machines immediately"},
            {"key": "B", "text": "Offering free food samples"},
            {"key": "C", "text": "Waiting to see future sales numbers"},
            {"key": "D", "text": "Lowering produce prices"}
        ],
        "correctAnswer": "C",
        "explanation": "<b>Đáp án đúng: (C) Waiting to see future sales numbers.</b><br><br><i>Transcript:</i> Man: \"Let's wait to see if sales numbers stay high before we invest in any more.\"<br><br><b>Dịch nghĩa:</b> Người đàn ông khuyên nên đợi xem doanh số bán có tiếp tục duy trì cao hay không trước khi quyết định đầu tư thêm máy."
    },

    # Q59 - Q61 (Audio: media/test3_part3_c59_61.mp3)
    {
        "id": "t3_q59", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 59,
        "prompt": "What are the speakers discussing?",
        "audio": "media/test3_part3_c59_61.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Opening hours for a clinic"},
            {"key": "B", "text": "Managing canceled dental appointments"},
            {"key": "C", "text": "Ordering new dental instruments"},
            {"key": "D", "text": "Billing procedures"}
        ],
        "correctAnswer": "B",
        "explanation": "<b>Đáp án đúng: (B) Managing canceled dental appointments.</b><br><br><i>Transcript:</i> Man: \"Ingrid, we've had three patients this week who had to cancel their dental appointments at the last minute.\"<br><br><b>Dịch nghĩa:</b> Hai người đang bàn về vấn đề các bệnh nhân hủy lịch khám răng vào phút chót."
    },
    {
        "id": "t3_q60", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 60,
        "prompt": "Why does the man say, \"You just have to check a box\"?",
        "audio": "media/test3_part3_c59_61.mp3", "image": None,
        "options": [
            {"key": "A", "text": "To emphasize that a feature is easy to use"},
            {"key": "B", "text": "To confirm that a form is complete"},
            {"key": "C", "text": "To ask for an explanation"},
            {"key": "D", "text": "To report a computer bug"}
        ],
        "correctAnswer": "A",
        "explanation": "<b>Đáp án đúng: (A) To emphasize that a feature is easy to use.</b><br><br><i>Transcript:</i> Man: \"...there was an option to receive a text message notification if an earlier slot became available. You just have to check a box.\"<br><br><b>Dịch nghĩa:</b> Anh ấy nhấn mạnh tính năng nhận tin nhắn báo lịch trống rất đơn giản, người dùng chỉ cần tích vào ô chọn."
    },
    {
        "id": "t3_q61", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 61,
        "prompt": "What does the woman offer to do this afternoon?",
        "audio": "media/test3_part3_c59_61.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Call some patients"},
            {"key": "B", "text": "Contact an insurance provider"},
            {"key": "C", "text": "Look into software options"},
            {"key": "D", "text": "Update a website"}
        ],
        "correctAnswer": "C",
        "explanation": "<b>Đáp án đúng: (C) Look into software options.</b><br><br><i>Transcript:</i> Woman: \"I have some time this afternoon. I'll look into software packages that include that feature.\"<br><br><b>Dịch nghĩa:</b> Người phụ nữ đề nghị chiều nay sẽ tìm hiểu các gói phần mềm có tích hợp tính năng này."
    },

    # Q62 - Q64 (Audio: media/test3_part3_c62_64.mp3)
    {
        "id": "t3_q62", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 62,
        "prompt": "Who will the man give some gifts to?",
        "audio": "media/test3_part3_c62_64.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Conference participants"},
            {"key": "B", "text": "Employees"},
            {"key": "C", "text": "Contest winners"},
            {"key": "D", "text": "Visitors"}
        ],
        "correctAnswer": "B",
        "explanation": "<b>Đáp án đúng: (B) Employees.</b><br><br><i>Transcript:</i> Man: \"Hi Raquel, have you had a chance to look for something I could buy the employees for the New Year?\"<br><br><b>Dịch nghĩa:</b> Người đàn ông muốn mua quà năm mới tặng cho các nhân viên của công ty."
    },
    {
        "id": "t3_q63", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 63,
        "prompt": "Look at the graphic. How much is the mug that the woman likes?",
        "audio": "media/test3_part3_c62_64.mp3", "image": None,
        "options": [
            {"key": "A", "text": "$15"},
            {"key": "B", "text": "$18"},
            {"key": "C", "text": "$23"},
            {"key": "D", "text": "$28"}
        ],
        "correctAnswer": "C",
        "explanation": "<b>Đáp án đúng: (C) $23.</b><br><br><i>Transcript:</i> Woman: \"I like the medium mug with the Desert Roaming design.\" Dựa theo bảng giá mẫu cốc Desert Roaming cỡ vừa (medium) có giá là $23."
    },
    {
        "id": "t3_q64", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 64,
        "prompt": "What does the man say he will do?",
        "audio": "media/test3_part3_c62_64.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Sign an order request"},
            {"key": "B", "text": "Contact a supplier directly"},
            {"key": "C", "text": "Distribute a catalog"},
            {"key": "D", "text": "Pay with cash"}
        ],
        "correctAnswer": "A",
        "explanation": "<b>Đáp án đúng: (A) Sign an order request.</b><br><br><i>Transcript:</i> Man: \"I'll sign off on that order request once you fill out the paperwork.\"<br><br><b>Dịch nghĩa:</b> Người đàn ông sẽ ký phê duyệt đơn đặt hàng sau khi người phụ nữ hoàn tất giấy tờ."
    },

    # Q65 - Q67 (Audio: media/test3_part3_c65_67.mp3)
    {
        "id": "t3_q65", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 65,
        "prompt": "What industry do the speakers most likely work in?",
        "audio": "media/test3_part3_c65_67.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Film production"},
            {"key": "B", "text": "City planning"},
            {"key": "C", "text": "Real estate"},
            {"key": "D", "text": "Law enforcement"}
        ],
        "correctAnswer": "A",
        "explanation": "<b>Đáp án đúng: (A) Film production.</b><br><br><i>Transcript:</i> Man: \"Here's the map that you requested for next week's shoot, for the driving scene... camera operators to follow the action...\"<br><br><b>Dịch nghĩa:</b> Hai người làm việc trong ngành sản xuất phim ảnh (buổi quay cảnh lái xe của diễn viên)."
    },
    {
        "id": "t3_q66", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 66,
        "prompt": "Why does the woman want to make a change?",
        "audio": "media/test3_part3_c65_67.mp3", "image": None,
        "options": [
            {"key": "A", "text": "To avoid a construction zone"},
            {"key": "B", "text": "To make filming easier"},
            {"key": "C", "text": "To stay within budget"},
            {"key": "D", "text": "To use better lighting"}
        ],
        "correctAnswer": "B",
        "explanation": "<b>Đáp án đúng: (B) To make filming easier.</b><br><br><i>Transcript:</i> Woman: \"We may need to alter the route so it'll be less difficult for our camera operators to follow the action.\"<br><br><b>Dịch nghĩa:</b> Cô muốn thay đổi lộ trình lái xe để người quay phim dễ dàng theo sát hành động hơn."
    },
    {
        "id": "t3_q67", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 67,
        "prompt": "Look at the graphic. Which road should be closed?",
        "audio": "media/test3_part3_c65_67.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Bangalore Avenue"},
            {"key": "B", "text": "Dublin Avenue"},
            {"key": "C", "text": "Polly Street"},
            {"key": "D", "text": "Elm Lane"}
        ],
        "correctAnswer": "C",
        "explanation": "<b>Đáp án đúng: (C) Polly Street.</b><br><br><i>Transcript:</i> Woman: \"Instead of turning left on Elm Lane, let's have them turn right and park in front of the hair salon. Man: Okay. I'll arrange for that road to be closed...\" Trên sơ đồ bản đồ, con đường rẽ phải có tiệm làm tóc (hair salon) là đường Polly Street."
    },

    # Q68 - Q70 (Audio: media/test3_part3_c68_70.mp3)
    {
        "id": "t3_q68", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 68,
        "prompt": "What are the speakers preparing for?",
        "audio": "media/test3_part3_c68_70.mp3", "image": None,
        "options": [
            {"key": "A", "text": "A job interview"},
            {"key": "B", "text": "A video game release"},
            {"key": "C", "text": "A marketing presentation"},
            {"key": "D", "text": "An awards ceremony"}
        ],
        "correctAnswer": "B",
        "explanation": "<b>Đáp án đúng: (B) A video game release.</b><br><br><i>Transcript:</i> Woman: \"Hi Pablo, I wanted to talk to you about the video game we designed—the one we're launching soon.\"<br><br><b>Dịch nghĩa:</b> Họ đang chuẩn bị cho việc phát hành tựa game điện tử sắp ra mắt."
    },
    {
        "id": "t3_q69", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 69,
        "prompt": "Look at the graphic. Which level is the woman concerned about?",
        "audio": "media/test3_part3_c68_70.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Level 1"},
            {"key": "B", "text": "Level 2"},
            {"key": "C", "text": "Level 3"},
            {"key": "D", "text": "Level 4"}
        ],
        "correctAnswer": "C",
        "explanation": "<b>Đáp án đúng: (C) Level 3.</b><br><br><i>Transcript:</i> Woman: \"...in the Underwater level, there's a problem with the part where the characters discover the lost city in the ocean. As I was going over the layout, I found a glitch in the gameplay.\" Theo sơ đồ thứ tự các màn chơi, màn Underwater (Dưới nước) là Level 3."
    },
    {
        "id": "t3_q70", "test": 3, "part": 3, "partName": "Part 3 - Conversations (Đoạn hội thoại)", "questionNum": 70,
        "prompt": "What does the woman suggest doing?",
        "audio": "media/test3_part3_c68_70.mp3", "image": None,
        "options": [
            {"key": "A", "text": "Working over the weekend"},
            {"key": "B", "text": "Postponing the launch date"},
            {"key": "C", "text": "Hiring another programmer"},
            {"key": "D", "text": "Surveying game testers"}
        ],
        "correctAnswer": "A",
        "explanation": "<b>Đáp án đúng: (A) Working over the weekend.</b><br><br><i>Transcript:</i> Woman: \"Yes. But we should work on it as soon as possible. I could put some extra time in over the weekend. How about you?\"<br><br><b>Dịch nghĩa:</b> Người phụ nữ đề xuất làm thêm giờ vào cuối tuần để khắc phục lỗi kịp thời."
    }
]

with open("test3_p3_partC.json", "w", encoding="utf-8") as f:
    json.dump(test3_p3, f, ensure_ascii=False, indent=2)
print("Part C written successfully, count:", len(test3_p3))
