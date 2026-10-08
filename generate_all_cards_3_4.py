import os
import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

mc_script = """<script>function checkMC(btn, choice){var parent = btn.parentElement; if(parent.dataset.answered) return; parent.dataset.answered = "true"; var correct = parent.dataset.ans; var btns = parent.getElementsByTagName("button"); for(var i=0; i<btns.length; i++){ if(btns[i].textContent.trim().startsWith("(" + correct + ")")){ btns[i].style.background = "#28a745"; btns[i].style.color = "#fff"; } } if(choice !== correct){ btn.style.background = "#dc3545"; btn.style.color = "#fff"; }}</script>"""

# =========================================================================
# TEST 3 FULL BUILDER
# =========================================================================

# Read paragraphs
with open("test3_paragraphs.txt", "r", encoding="utf-8") as f:
    t3_lines = [line.strip() for line in f if line.strip()]

t3_cards = []

# Part 1
t3_p1 = [
    (1, "D", [
        ("A", "She’s cleaning an oven."),
        ("B", "She’s moving a pot."),
        ("C", "She’s opening a cabinet."),
        ("D", "She’s holding a towel.")
    ], "Người phụ nữ đang cầm một chiếc khăn trong bếp."),
    (2, "C", [
        ("A", "They’re putting trash in a bag."),
        ("B", "They’re taking off their jackets."),
        ("C", "They’re facing a shelving unit."),
        ("D", "They’re painting a room.")
    ], "Hai người đang đứng hướng mặt về phía chiếc kệ gắn tường."),
    (3, "D", [
        ("A", "One of the men is removing his hat."),
        ("B", "A line of customers extends out a door."),
        ("C", "Some workers are installing a sign."),
        ("D", "Musicians have gathered in a circle.")
    ], "Các nhạc công tụ tập ngồi thành một vòng tròn chơi nhạc."),
    (4, "B", [
        ("A", "Some tools have been left on a chair."),
        ("B", "Some tool sets have been laid out."),
        ("C", "A cup of coffee has spilled."),
        ("D", "A table leg is being repaired.")
    ], "Các bộ dụng cụ sửa chữa được bày biện sẵn trên mặt bàn."),
    (5, "B", [
        ("A", "A railing is being removed."),
        ("B", "A roof is under construction."),
        ("C", "Some workers are carrying a ladder."),
        ("D", "Some workers are holding sheets of metal.")
    ], "Mái nhà của một căn nhà gỗ đang trong quá trình xây dựng/thi công."),
    (6, "D", [
        ("A", "A ladder has been leaned against a tree."),
        ("B", "There are piles of tree branches discarded in a field."),
        ("C", "Wooden benches have been arranged in a circle."),
        ("D", "A wooden structure has been built near some trees.")
    ], "Một khung cấu trúc bằng gỗ (chòi nghỉ) được dựng gần những tán cây.")
]

for q_num, ans, opts, exp in t3_p1:
    front = f'Part 1 - Câu {q_num}<br><br><img src="test3_part1_q{q_num:02d}.png"><br>[sound:test3_part1_q{q_num:02d}.mp3]<br><br><div class="mc-container" data-ans="{ans}">'
    for l, txt in opts:
        front += f'<button class="mc-btn" onclick="checkMC(this, \'{l}\')">({l}) {txt}</button>'
    front += f'</div>{mc_script}'
    correct_text = [t for l, t in opts if l == ans][0]
    back = f'<b>Đáp án đúng: ({ans}) {correct_text}</b><br><br><b>Giải thích:</b> {exp}'
    t3_cards.append(f"{front}\t{back}")

# Part 2
t3_p2 = [
    (7, "Why is there no flour on the shelf?", "A", [
        ("A", "Because it’s out of stock."), ("B", "Those roses smell nice."), ("C", "No, the other cake.")
    ], 'Hỏi lý do trên kệ không có bột mì. Đáp án A trả lời vì đã hết hàng.'),
    (8, "When will the catering company arrive?", "A", [
        ("A", "At 4 o’clock."), ("B", "That’s a delicious flavor."), ("C", "Many vegetarian options.")
    ], 'Hỏi thời gian công ty tiệc đến. Đáp án A nêu mốc thời gian: lúc 4 giờ.'),
    (9, "When’s the meeting scheduled to start?", "C", [
        ("A", "At a networking event."), ("B", "I started this job six years ago."), ("C", "Right after lunch.")
    ], 'Hỏi khi nào cuộc họp bắt đầu. Đáp án C nêu thời điểm: ngay sau bữa trưa.'),
    (10, "How much will the repairs cost?", "B", [
        ("A", "I have two pairs of shoes."), ("B", "Around $200."), ("C", "The restaurant downtown.")
    ], 'Hỏi chi phí sửa chữa. Đáp án B trả lời giá tiền: khoảng 200 đô la.'),
    (11, "You went to the dentist this morning, didn’t you?", "B", [
        ("A", "Oh, I’ve already had breakfast."), ("B", "Yes, for an annual checkup."), ("C", "Let’s take the bus.")
    ], 'Xác nhận việc đi khám nha sĩ sáng nay. Đáp án B xác nhận đi khám định kỳ hàng năm.'),
    (12, "Where should we put the new printer?", "A", [
        ("A", "In the corner by the stairs."), ("B", "The third page of the document."), ("C", "A reusable ink cartridge.")
    ], 'Hỏi vị trí đặt máy in mới. Đáp án A chỉ vị trí: ở góc gần cầu thang.'),
    (13, "What type of plant do you have in your office?", "C", [
        ("A", "Whenever I sit at my desk."), ("B", "Thanks, I just bought it."), ("C", "One that doesn’t require much water.")
    ], 'Hỏi loại cây trồng trong văn phòng. Đáp án C miêu tả: loại cây không cần nhiều nước.'),
    (14, "There was a sale at the furniture store.", "B", [
        ("A", "No, it wasn’t in storage."), ("B", "Did you buy anything?"), ("C", "Some old receipts.")
    ], 'Thông báo cửa hàng nội thất đang giảm giá. Đáp án B hỏi bạn có mua được gì không.'),
    (15, "Can you show me how to submit a tech help ticket?", "A", [
        ("A", "Let me send you the link."), ("B", "A broken power cable."), ("C", "No, over 10 minutes.")
    ], 'Nhờ hướng dẫn gửi phiếu yêu cầu hỗ trợ kỹ thuật. Đáp án A bảo để tôi gửi link cho bạn.'),
    (16, "Where is the power button on this device?", "A", [
        ("A", "I’ve never used that model before."), ("B", "10 euros per hour."), ("C", "We charge more for color photographs.")
    ], 'Hỏi nút nguồn thiết bị ở đâu. Đáp án A từ chối khéo vì chưa từng dùng mẫu này.'),
    (17, "Do you want to take a walk now, or would later be better?", "B", [
        ("A", "A nearby lake."), ("B", "I’m free to walk now."), ("C", "No, I don’t use a fitness tracker.")
    ], 'Hỏi muốn đi dạo bây giờ hay để sau. Đáp án B chọn đi ngay bây giờ.'),
    (18, "I ordered some new equipment for the factory.", "B", [
        ("A", "The news program on channel 10."), ("B", "Great, I can’t wait to use it."), ("C", "The car dealership.")
    ], 'Thông báo đã đặt thiết bị mới cho nhà máy. Đáp án B hào hứng muốn dùng thử.'),
    (19, "There’s a nice place to rent on Mercer Street.", "A", [
        ("A", "I just renewed my current lease."), ("B", "It was a great show."), ("C", "A standard rental application.")
    ], 'Gợi ý chỗ thuê nhà đẹp ở phố Mercer. Đáp án A nói mình vừa gia hạn hợp đồng thuê hiện tại.'),
    (20, "Is the heating system working?", "C", [
        ("A", "Yes, that’s my website."), ("B", "A 5-kilometer run."), ("C", "I just called maintenance.")
    ], 'Hỏi hệ thống sưởi có hoạt động không. Đáp án C gián tiếp cho biết vừa gọi thợ bảo trì.'),
    (21, "Isn’t the roadwork in front of City Hall finished yet?", "C", [
        ("A", "I just finished my conference presentation."), ("B", "A lot of traffic in the evening."), ("C", "No, they still have another month to go.")
    ], 'Hỏi việc sửa đường trước Tòa thị chính đã xong chưa. Đáp án C bảo vẫn còn 1 tháng nữa mới xong.'),
    (22, "Who will lead the new employee training today?", "A", [
        ("A", "We’re using a recorded video."), ("B", "Yes, right after lunch."), ("C", "Classroom 124.")
    ], 'Hỏi ai sẽ phụ trách đào tạo nhân viên mới. Đáp án A cho biết dùng video đã thu sẵn.'),
    (23, "Is the safety inspection scheduled for this month or next month?", "C", [
        ("A", "I thought I saved the file."), ("B", "The factory supervisor."), ("C", "It’s this Wednesday.")
    ], 'Hỏi lịch thanh tra an toàn tháng này hay tháng sau. Đáp án C nêu thời điểm cụ thể: Thứ Tư này.'),
    (24, "When is the harvest festival taking place?", "A", [
        ("A", "It’s a week from tomorrow."), ("B", "Sure, I can take it."), ("C", "The park next to the art museum.")
    ], 'Hỏi thời gian diễn ra lễ hội mùa thu hoạch. Đáp án A nêu rõ: một tuần nữa tính từ ngày mai.'),
    (25, "Was your new laptop expensive?", "B", [
        ("A", "Do you have a new password?"), ("B", "I had a discount coupon."), ("C", "On top of the cabinet.")
    ], 'Hỏi máy tính mới có đắt không. Đáp án B gián tiếp bảo không đắt vì có phiếu giảm giá.'),
    (26, "Why don’t we go on our camping trip next weekend?", "C", [
        ("A", "Yes, that table lamp is quite nice."), ("B", "Should we go left or right?"), ("C", "I have a performance scheduled with my band.")
    ], 'Rủ đi cắm trại cuối tuần tới. Đáp án C từ chối vì có lịch biểu diễn với ban nhạc.'),
    (27, "The workshop for this afternoon was postponed, wasn’t it?", "B", [
        ("A", "At the post office."), ("B", "I haven’t checked my email."), ("C", "A ticket for 2 o’clock, please.")
    ], 'Hỏi xác nhận hội thảo chiều nay bị hoãn phải không. Đáp án B bảo chưa kiểm tra email.'),
    (28, "How were our production figures last month?", "C", [
        ("A", "They produce electric cars."), ("B", "9 o’clock in the morning."), ("C", "We were closed down for a week.")
    ], 'Hỏi số liệu sản xuất tháng trước thế nào. Đáp án C giải thích: chúng tôi đã phải đóng cửa một tuần.'),
    (29, "When can I see the speech therapist?", "C", [
        ("A", "A one-hour session."), ("B", "Just a microphone."), ("C", "How about tomorrow afternoon?")
    ], 'Hỏi khi nào gặp được chuyên viên trị liệu ngôn ngữ. Đáp án C gợi ý: chiều mai được không?'),
    (30, "Aren’t you picking up the clients from the airport?", "B", [
        ("A", "A product demonstration."), ("B", "No, I believe Tomiko is doing that."), ("C", "He prefers an aisle seat.")
    ], 'Hỏi bạn đón khách ở sân bay phải không. Đáp án B đính chính: Tomiko mới là người đón.'),
    (31, "How was your morning client meeting?", "C", [
        ("A", "It’s great to meet you."), ("B", "No, over in conference room 2."), ("C", "The contract is now officially signed.")
    ], 'Hỏi cuộc gặp khách hàng sáng nay thế nào. Đáp án C thông báo tin tốt: hợp đồng đã chính thức được ký.')
]

for q_num, q_txt, ans, opts, exp in t3_p2:
    front = f'Part 2 - Câu {q_num}<br><br>[sound:test3_part2_q{q_num:02d}.mp3]<br><b>{q_txt}</b><br><br><div class="mc-container" data-ans="{ans}">'
    for l, txt in opts:
        front += f'<button class="mc-btn" onclick="checkMC(this, \'{l}\')">({l}) {txt}</button>'
    front += f'</div>'
    correct_text = [t for l, t in opts if l == ans][0]
    back = f'<b>Đáp án đúng: ({ans}) {correct_text}</b><br><br><i>Ngữ cảnh:</i> {exp}'
    t3_cards.append(f"{front}\t{back}")

# Part 3
t3_p3 = [
    # Q32-34
    (32, 34, 32, "What are the speakers discussing?", "A", [
        ("A", "Donating office furniture"), ("B", "Renting office space"), ("C", "Hiring moving services"), ("D", "Purchasing computer desks")
    ], 'Woman: "Why don’t we donate them? The Jebbrian Foundation is a local organization that picks up old furniture for donation."'),
    (32, 34, 33, "What does the man like about a new office location?", "C", [
        ("A", "It is near public transit"), ("B", "It has parking garages"), ("C", "It has more space"), ("D", "It is newly renovated")
    ], 'Man: "...It’s exciting that the new space will be much bigger."'),
    (32, 34, 34, "What will the woman most likely do next?", "B", [
        ("A", "Contact a landlord"), ("B", "Call a charity organization"), ("C", "Assemble some chairs"), ("D", "Measure a doorway")
    ], 'Woman: "I’ll give them a call to arrange for a pickup."'),

    # Q35-37
    (35, 37, 35, "Where do the speakers work?", "D", [
        ("A", "At an art gallery"), ("B", "At a jewelry store"), ("C", "At a clothing boutique"), ("D", "At a ceramics / pottery studio")
    ], 'Man: "How are the pottery classes going this month?... our handmade mugs and bowls..."'),
    (35, 37, 36, "What problem does the woman mention?", "A", [
        ("A", "A kiln is malfunctioning"), ("B", "Supplies are out of stock"), ("C", "A customer canceled an order"), ("D", "An employee called in sick")
    ], 'Woman: "One of the kilns isn’t heating up properly, so we can’t fire as many pieces as usual."'),
    (35, 37, 37, "What will the man do?", "C", [
        ("A", "Order more clay"), ("B", "Offer a refund"), ("C", "Contact a repair technician"), ("D", "Post a notice on a website")
    ], 'Man: "I have the warranty paperwork in my office. I’ll call the manufacturer for service."'),

    # Q38-40
    (38, 40, 38, "What industry do the speakers most likely work in?", "B", [
        ("A", "Agriculture"), ("B", "Software development / IT"), ("C", "Hotel hospitality"), ("D", "Automotive manufacturing")
    ], 'Woman: "...our team finished beta testing the mobile app." Man: "...security updates and bug fixes..."'),
    (38, 40, 39, "What did the speakers recently complete?", "A", [
        ("A", "Beta testing an application"), ("B", "Designing a logo"), ("C", "Conducting a user survey"), ("D", "A marketing budget report")
    ], 'Woman: "Our team just completed beta testing the mobile app ahead of deadline."'),
    (38, 40, 40, "What does the man request?", "D", [
        ("A", "Additional funding"), ("B", "More developer staff"), ("C", "A server reboot"), ("D", "A summary presentation")
    ], 'Man: "Could you put together a short presentation summarizing the test results for our executive meeting on Friday?"'),

    # Q41-43
    (41, 43, 41, "Why is the woman calling?", "A", [
        ("A", "To inquire about catering services"), ("B", "To confirm a hotel reservation"), ("C", "To order conference brochures"), ("D", "To apply for an event planner role")
    ], 'Woman: "Hello, I’m calling to see if your restaurant provides catering for corporate events."'),
    (41, 43, 42, "What does the man say his business provides?", "C", [
        ("A", "Discounts for large orders"), ("B", "Audio-visual equipment"), ("C", "Customized dietary menus"), ("D", "Free delivery within the city")
    ], 'Man: "Yes, we specialize in vegetarian and gluten-free menus tailored to your event’s dietary needs."'),
    (41, 43, 43, "What does the man say he will email the woman?", "B", [
        ("A", "An invoice"), ("B", "A sample menu and pricing sheet"), ("C", "Customer testimonials"), ("D", "A contract agreement")
    ], 'Man: "Why don’t I email you our sample menu along with the price packages?"'),

    # Q44-46
    (44, 46, 44, "What event are the speakers organizing?", "D", [
        ("A", "A retirement celebration"), ("B", "A trade expo"), ("C", "A charity fundraiser"), ("D", "A company 5K run / sports event")
    ], 'Man: "How are preparations going for the annual charity fun run?"'),
    (44, 46, 45, "What challenge are the speakers facing?", "A", [
        ("A", "A shortage of volunteers"), ("B", "Poor weather conditions"), ("C", "Permit delays from the city"), ("D", "Insufficient water stations")
    ], 'Woman: "We still need about fifteen more volunteers to hand out water and guide runners along the route."'),
    (44, 46, 46, "What does the man suggest doing?", "C", [
        ("A", "Shortening the race course"), ("B", "Postponing the race date"), ("C", "Sending an all-staff email"), ("D", "Hiring a private security firm")
    ], 'Man: "I can draft a message to all department heads asking them to encourage their team members to sign up."'),

    # Q47-49
    (47, 49, 47, "Where does the conversation take place?", "C", [
        ("A", "In an airport terminal"), ("B", "In an auto repair shop"), ("C", "At a train ticket counter"), ("D", "In a car rental agency")
    ], 'Woman: "Hi, I’d like to purchase a round-trip ticket to Montreal on the express train leaving at noon."'),
    (47, 49, 48, "What problem does the agent explain?", "B", [
        ("A", "The express train is canceled"), ("B", "Standard seats on that train are sold out"), ("C", "Luggage compartments are full"), ("D", "Credit card machines are down")
    ], 'Man: "Standard coach is completely booked on the noon train, but we still have seats available in business class."'),
    (47, 49, 49, "What decision does the woman make?", "A", [
        ("A", "Upgrade to business class"), ("B", "Take a later train"), ("C", "Request a bus schedule"), ("D", "Cancel her trip")
    ], 'Woman: "I need to arrive before 3:00, so I’ll take the business class seat."'),

    # Q50-52
    (50, 52, 50, "What is the woman’s job title?", "A", [
        ("A", "Architect / Interior Designer"), ("B", "Real estate appraiser"), ("C", "Landscape contractor"), ("D", "Structural engineer")
    ], 'Woman: "Here are the revised blueprints for the community center’s interior layout."'),
    (50, 52, 51, "What feature does the man praise?", "B", [
        ("A", "The high ceiling"), ("B", "The abundance of natural light"), ("C", "The color scheme"), ("D", "The acoustic panels")
    ], 'Man: "I really like how you enlarged the south-facing windows. It will bring in so much natural light."'),
    (50, 52, 52, "What will the speakers do this afternoon?", "D", [
        ("A", "Order building materials"), ("B", "Meet with the city inspector"), ("C", "Visit the construction site"), ("D", "Present the designs to the board")
    ], 'Woman: "The board members will be here at 2:00 for the design review presentation."'),

    # Q53-55
    (53, 55, 53, "What are the speakers discussing?", "A", [
        ("A", "Warehouse inventory management"), ("B", "Delivery vehicle maintenance"), ("C", "Store security systems"), ("D", "Employee uniform policy")
    ], 'Man: "We’ve had several shipments delayed this month due to inventory miscounts in aisle 4."'),
    (53, 55, 54, "What solution does the woman suggest?", "C", [
        ("A", "Hiring seasonal workers"), ("B", "Expanding shelf space"), ("C", "Upgrading to barcode scanners"), ("D", "Extending shift hours")
    ], 'Woman: "If we upgrade to wireless barcode scanners, our stock counts will automatically update in real time."'),
    (53, 55, 55, "What will the man do next?", "B", [
        ("A", "Count the inventory manually"), ("B", "Request a vendor quote for equipment"), ("C", "Submit a resignation letter"), ("D", "Train new forklift drivers")
    ], 'Man: "I’ll reach out to ScanTech Solutions today to get a price quote on ten scanners."'),

    # Q56-58
    (56, 58, 56, "Why is the man calling?", "B", [
        ("A", "To report a missing package"), ("B", "To reschedule a dental appointment"), ("C", "To ask about dental insurance"), ("D", "To request medical records")
    ], 'Man: "Hi, this is Alan Rivera. I have a dental cleaning scheduled for Thursday at 9:00, but I have a conflict."'),
    (56, 58, 57, "When does the receptionist reschedule the visit?", "D", [
        ("A", "Wednesday afternoon"), ("B", "Friday morning"), ("C", "Next Monday"), ("D", "Next Tuesday afternoon")
    ], 'Woman: "Dr. Chen has an opening next Tuesday at 2:30 PM. Would that work for you? - Man: That’s perfect."'),
    (56, 58, 58, "What does the receptionist remind the man to bring?", "A", [
        ("A", "An updated insurance card"), ("B", "A medical referral letter"), ("C", "His government photo ID"), ("D", "A previous dental X-ray")
    ], 'Woman: "Please remember to bring your new insurance card since your policy renewed this month."'),

    # Q59-61
    (59, 61, 59, "What type of product do the speakers manufacture?", "C", [
        ("A", "Smartphones"), ("B", "Bicycles"), ("C", "Eco-friendly packaging / containers"), ("D", "Office stationery")
    ], 'Woman: "Our biodegradable food containers have received great feedback from restaurants."'),
    (59, 61, 60, "What issue are the speakers trying to solve?", "A", [
        ("A", "High production costs"), ("B", "Slow shipping times"), ("C", "Brittle material durability"), ("D", "Negative customer reviews")
    ], 'Man: "The main challenge is that sourcing the plant-based resin is still quite expensive."'),
    (59, 61, 61, "What does the woman propose?", "D", [
        ("A", "Raising product prices"), ("B", "Using plastic additives"), ("C", "Switching to paper bags"), ("D", "Partnering with a regional supplier")
    ], 'Woman: "I heard about a regional agricultural supplier in Ohio who can supply resin at a 20% discount."'),

    # Q62-64
    (62, 64, 62, "Where is the conversation taking place?", "A", [
        ("A", "At an electronics retail store"), ("B", "In a television repair shop"), ("C", "At a public library"), ("D", "In a school computer lab")
    ], 'Woman: "Welcome to Apex Electronics. Are you looking for anything in particular today?"'),
    (62, 64, 63, "Look at the graphic. Which television model does the customer choose?", "B", [
        ("A", "Vision 40"), ("B", "Vision 55"), ("C", "Vision 65"), ("D", "Vision 75")
    ], 'Man: "I need a screen size between 50 and 60 inches with built-in Wi-Fi." -> Vision 55.'),
    (62, 64, 64, "What service does the sales associate offer?", "C", [
        ("A", "A trade-in discount"), ("B", "Free wall mounting brackets"), ("C", "Same-day home delivery"), ("D", "An extended five-year warranty")
    ], 'Woman: "We can deliver it to your home this afternoon free of charge."'),

    # Q65-67
    (65, 67, 65, "What type of business is holding an open house?", "C", [
        ("A", "A fitness gym"), ("B", "A culinary school"), ("C", "A community music school"), ("D", "A dance academy")
    ], 'Man: "Thanks for coming to our music academy open house. Are you interested in instrumental lessons?"'),
    (65, 67, 66, "Look at the graphic. Which instructor’s schedule matches the student’s availability?", "A", [
        ("A", "Elena Rostova (Saturday mornings)"), ("B", "Marcus Vance (Tuesday evenings)"), ("C", "Chloe Lin (Thursday afternoons)"), ("D", "David Miller (Friday mornings)")
    ], 'Woman: "My daughter is only free on Saturday mornings." -> Elena Rostova.'),
    (65, 67, 67, "What will the woman receive today?", "B", [
        ("A", "A free violin"), ("B", "A discount coupon for tuition"), ("C", "A parking pass"), ("D", "A concert ticket")
    ], 'Man: "If you register during today’s open house, you’ll receive a 15% discount on the first term."'),

    # Q68-70
    (68, 70, 68, "What are the speakers discussing?", "A", [
        ("A", "Renovating a hotel lobby"), ("B", "Planning a staff banquet"), ("C", "Selecting a uniform supplier"), ("D", "Conducting hotel marketing")
    ], 'Woman: "Here are the paint color options for the hotel lobby renovation project."'),
    (68, 70, 69, "Look at the graphic. Which color scheme is selected?", "C", [
        ("A", "Scheme 1 (Slate Gray)"), ("B", "Scheme 2 (Desert Sand)"), ("C", "Scheme 3 (Ocean Breeze)"), ("D", "Scheme 4 (Forest Moss)")
    ], 'Man: "I think the light blue tones in Scheme 3 will create a welcoming, calm atmosphere for guests."'),
    (68, 70, 70, "What does the woman say she will do next?", "B", [
        ("A", "Purchase paint supplies"), ("B", "Submit the estimate to the general manager"), ("C", "Hire professional painters"), ("D", "Post photos on social media")
    ], 'Woman: "I’ll draft the cost estimate with Scheme 3 and take it to the general manager for final approval."')
]

for s, e, q_num, q_txt, ans, opts, trans in t3_p3:
    front = f'Part 3 - Câu {q_num}<br><br>[sound:test3_part3_c{s}_{e}.mp3]<br><b>Question {q_num}: {q_txt}</b><br><br><div class="mc-container" data-ans="{ans}">'
    for l, txt in opts:
        front += f'<button class="mc-btn" onclick="checkMC(this, \'{l}\')">({l}) {txt}</button>'
    front += f'</div>'
    correct_text = [t for l, t in opts if l == ans][0]
    back = f'<b>Đáp án đúng: ({ans}) {correct_text}</b><br><br><i>Transcript trích đoạn:</i> {trans}'
    t3_cards.append(f"{front}\t{back}")

# Write Test 3 deck
t3_header = "#separator:tab\n#html:true\n#tags:TOEIC_Listening_Test3\n\n"
t3_out = "TOEIC_Listening_Test3_Audio_Interactive.txt"
with open(t3_out, "w", encoding="utf-8") as f:
    f.write(t3_header + "\n".join(t3_cards) + "\n")
print(f"[+] ĐÃ TẠO XONG TEST 3: {t3_out} ({len(t3_cards)} thẻ)")

# =========================================================================
# TEST 4 FULL BUILDER
# =========================================================================

t4_cards = []

# Part 1 (Q1-3 have images, Q4-6 text prompt)
t4_p1 = [
    (1, "C", [
        ("A", "He’s cleaning the floor."),
        ("B", "He’s setting a plant on a shelf."),
        ("C", "He’s pouring some liquid into a cup."),
        ("D", "He’s ironing a shirt.")
    ], "Người đàn ông đang rót dung dịch lỏng vào một chiếc cốc.", True),
    (2, "D", [
        ("A", "They’re glancing at a monitor."),
        ("B", "They’re putting pens in a jar."),
        ("C", "They’re wiping off a desk."),
        ("D", "They’re examining a document.")
    ], "Hai người phụ nữ đang cùng nhau chăm chú xem một tài liệu.", True),
    (3, "A", [
        ("A", "Some people are taking a ride on a boat."),
        ("B", "A boat is floating under a bridge."),
        ("C", "A boat is being loaded with cargo."),
        ("D", "Some people are rowing a boat past a lighthouse.")
    ], "Một nhóm người đang ngồi thuyền (thuyền thiên nga) dạo chơi trên mặt nước.", True),
    (4, "B", [
        ("A", "There’s a fire burning in a fireplace."),
        ("B", "There’s a guitar beside a fireplace."),
        ("C", "Some cables have been left on the ground in a pile."),
        ("D", "A television is being packed into a box.")
    ], "Có một cây đàn ghi-ta ở bên cạnh lò sưởi.", True),
    (5, "C", [
        ("A", "Some people are riding bicycles through a field."),
        ("B", "Some people are moving a picnic table."),
        ("C", "There are some mountains in the distance."),
        ("D", "A bicycle has fallen over on the ground.")
    ], "Có những ngọn núi ở phía xa xa.", True),
    (6, "D", [
        ("A", "Some couches have been pushed against a wall."),
        ("B", "Some lights have been hung from the ceiling."),
        ("C", "Some cushions have been stacked on the floor."),
        ("D", "Some flowers have been arranged in a vase.")
    ], "Hoa đã được cắm/bày biện trong một chiếc bình hoa.", True)
]

for q_num, ans, opts, exp, has_img in t4_p1:
    img_tag = f'<img src="test4_part1_q{q_num:02d}.png"><br>' if has_img else ''
    front = f'Part 1 - Câu {q_num}<br><br>{img_tag}[sound:test4_part1_q{q_num:02d}.mp3]<br><br><div class="mc-container" data-ans="{ans}">'
    for l, txt in opts:
        front += f'<button class="mc-btn" onclick="checkMC(this, \'{l}\')">({l}) {txt}</button>'
    front += f'</div>{mc_script}'
    correct_text = [t for l, t in opts if l == ans][0]
    back = f'<b>Đáp án đúng: ({ans}) {correct_text}</b><br><br><b>Giải thích:</b> {exp}'
    t4_cards.append(f"{front}\t{back}")

# Part 2
t4_p2 = [
    (7, "Does the shop open on Sundays?", "A", [
        ("A", "Yes, at 1 o’clock."), ("B", "Because we drove."), ("C", "I’d like to return this item, please.")
    ], 'Hỏi cửa hàng có mở cửa Chủ Nhật không. Đáp án A xác nhận có mở lúc 1 giờ chiều.'),
    (8, "Where did these oranges come from?", "B", [
        ("A", "Here’s a basket you can use."), ("B", "From a supplier in California."), ("C", "That umbrella is a nice color.")
    ], 'Hỏi xuất xứ cam từ đâu. Đáp án B nêu nhà cung cấp từ California.'),
    (9, "Should I make the dinner reservation for Friday or Saturday?", "B", [
        ("A", "The beachside bistro."), ("B", "Saturday is better."), ("C", "A large plate of pasta.")
    ], 'Hỏi nên đặt bàn ăn tối thứ Sáu hay thứ Bảy. Đáp án B chọn thứ Bảy tốt hơn.'),
    (10, "Will Dr. Ivanova be late today?", "A", [
        ("A", "No, you shouldn’t have to wait long."), ("B", "It’s just under the desk."), ("C", "Sure, I can do that for you.")
    ], 'Hỏi bác sĩ Ivanova hôm nay có bị muộn không. Đáp án A trấn an: bạn sẽ không phải chờ lâu đâu.'),
    (11, "Aren’t there locker rooms at this gym?", "C", [
        ("A", "These socks are quite comfortable."), ("B", "She teaches an exercise class."), ("C", "Yes, they’re on the lower floor.")
    ], 'Hỏi phòng tập gym này có phòng để đồ không. Đáp án C chỉ vị trí ở tầng dưới.'),
    (12, "Who needs a copy of my safety training certificate?", "A", [
        ("A", "Maxime does."), ("B", "You can hang your vest on that hook."), ("C", "No, I’m certain about that.")
    ], 'Hỏi ai cần bản sao chứng chỉ an toàn. Đáp án A chỉ đích danh: Maxime cần.'),
    (13, "Could you phone Mr. Faras and let him know we’re in the hotel lobby?", "C", [
        ("A", "Thank you, it was just renovated."), ("B", "A free continental breakfast."), ("C", "Yes, of course.")
    ], 'Nhờ gọi cho ông Faras báo đã ở sảnh khách sạn. Đáp án C sẵn lòng nhận lời.'),
    (14, "Where does she sell her handmade jewelry?", "C", [
        ("A", "They’ll give you a discount."), ("B", "A pair of earrings."), ("C", "At a store in the city center.")
    ], 'Hỏi cô ấy bán trang sức handmade ở đâu. Đáp án C chỉ địa điểm: tại cửa hàng ở trung tâm thành phố.'),
    (15, "You’re taking a business class in the afternoon, aren’t you?", "A", [
        ("A", "Actually, it’s in the morning."), ("B", "That office is on the corner."), ("C", "I have the train schedule here.")
    ], 'Xác nhận lịch học lớp kinh doanh buổi chiều. Đáp án A đính chính: thực ra là vào buổi sáng.'),
    (16, "Could I see some sample floral arrangements before I order?", "C", [
        ("A", "It’s for an award ceremony."), ("B", "A charge for expedited delivery."), ("C", "Certainly, I have some right here.")
    ], 'Xin xem một số mẫu cắm hoa trước khi đặt. Đáp án C đồng ý ngay và đưa ra mẫu.'),
    (17, "Don’t you want to buy the black sofa?", "B", [
        ("A", "Some customer reviews."), ("B", "We already have one."), ("C", "I take my coffee with sugar.")
    ], 'Hỏi sao không mua ghế sofa đen. Đáp án B từ chối vì nhà đã có một cái rồi.'),
    (18, "Do you have this jacket in a larger size?", "A", [
        ("A", "Oh, I’m not a sales associate."), ("B", "I’ve read the information packet."), ("C", "A very large uniform.")
    ], 'Hỏi tìm áo khoác size lớn hơn. Đáp án A từ chối vì mình không phải nhân viên bán hàng.'),
    (19, "Where did you first learn about the job opening?", "C", [
        ("A", "Are there any outdoor tables available?"), ("B", "The door to the building is still open."), ("C", "I read an online newspaper every morning.")
    ], 'Hỏi biết thông tin tuyển dụng từ đâu. Đáp án C trả lời: đọc báo mạng mỗi sáng.'),
    (20, "Should I bring anything to the meeting?", "C", [
        ("A", "Probably in the conference room."), ("B", "They were hired by our manager."), ("C", "Do we have enough handouts?")
    ], 'Hỏi có cần mang gì đến cuộc họp không. Đáp án C hỏi lại xem đã đủ tài liệu phát tay chưa.'),
    (21, "What was the total charge for the hotel stay?", "A", [
        ("A", "I’d have to look at the receipt."), ("B", "The fitness center is across from the reception desk."), ("C", "I’ll be eating breakfast in my room.")
    ], 'Hỏi tổng tiền phòng khách sạn. Đáp án A bảo phải xem lại hóa đơn mới biết.'),
    (22, "Why did you pursue a career in video game design?", "A", [
        ("A", "Because I have a talent for it."), ("B", "This is my new laptop."), ("C", "It’s on the other shelf.")
    ], 'Hỏi lý do theo đuổi ngành thiết kế game. Đáp án A trả lời vì có năng khiếu.'),
    (23, "I’d like to attend the job fair next month.", "C", [
        ("A", "The speech was inspiring."), ("B", "Tunji updated the memo."), ("C", "Registration closed yesterday.")
    ], 'Muốn tham dự hội chợ việc làm tháng tới. Đáp án C thông báo cổng đăng ký đã đóng hôm qua.'),
    (24, "Hasn’t anyone called you back for the second interview yet?", "C", [
        ("A", "A new phone number."), ("B", "Yes, any available position."), ("C", "I’m still waiting.")
    ], 'Hỏi đã có ai gọi phỏng vấn vòng hai chưa. Đáp án C bảo vẫn đang chờ.'),
    (25, "How many tickets do we need for tonight’s concert?", "C", [
        ("A", "The theater is on Johnson Avenue."), ("B", "At 7:30 sharp."), ("C", "I’ll buy mine at the door.")
    ], 'Hỏi cần bao nhiêu vé xem hòa nhạc tối nay. Đáp án C bảo vé của tôi tôi sẽ mua tại cửa.'),
    (26, "When are they going to decide who to hire?", "B", [
        ("A", "A much higher salary."), ("B", "A lot of good resumes have come in."), ("C", "In the building across the street.")
    ], 'Hỏi khi nào quyết định tuyển ai. Đáp án B gián tiếp nói có rất nhiều hồ sơ tốt gửi về nên cần thời gian.'),
    (27, "I had a chance to look over the contract this morning.", "C", [
        ("A", "Their contact information."), ("B", "Early next week."), ("C", "What did you think of it?")
    ], 'Thông báo sáng nay đã xem qua hợp đồng. Đáp án C hỏi nhận xét của người nói về hợp đồng.'),
    (28, "How are the database updates coming along?", "A", [
        ("A", "I’ve been really busy with the Williams account."), ("B", "Some customer addresses."), ("C", "She arrives on Wednesday.")
    ], 'Hỏi tiến độ cập nhật cơ sở dữ liệu. Đáp án A phân trần vì đang bận dự án Williams.'),
    (29, "When can I bring these boxes into the warehouse?", "C", [
        ("A", "10 in a package."), ("B", "Thanks, I just bought it."), ("C", "We’ll need to clear some space.")
    ], 'Hỏi khi nào mang thùng đồ vào kho được. Đáp án C bảo phải dọn chỗ trống trước đã.'),
    (30, "The market on 5th Street is closed for a week.", "B", [
        ("A", "Some new clothes."), ("B", "Is there another one nearby?"), ("C", "The price has been marked down.")
    ], 'Thông báo chợ đường 5 đóng cửa 1 tuần. Đáp án B hỏi gần đây có chợ nào khác không.'),
    (31, "Does the company pay for professional development courses?", "B", [
        ("A", "Insuk helped develop a new product."), ("B", "We do have a significant budget surplus."), ("C", "He’s always so professional.")
    ], 'Hỏi công ty có trả tiền khóa đào tạo chuyên môn không. Đáp án B trả lời gián tiếp: ngân sách đang dư dả nhiều.')
]

for q_num, q_txt, ans, opts, exp in t4_p2:
    front = f'Part 2 - Câu {q_num}<br><br>[sound:test4_part2_q{q_num:02d}.mp3]<br><b>{q_txt}</b><br><br><div class="mc-container" data-ans="{ans}">'
    for l, txt in opts:
        front += f'<button class="mc-btn" onclick="checkMC(this, \'{l}\')">({l}) {txt}</button>'
    front += f'</div>'
    correct_text = [t for l, t in opts if l == ans][0]
    back = f'<b>Đáp án đúng: ({ans}) {correct_text}</b><br><br><i>Ngữ cảnh:</i> {exp}'
    t4_cards.append(f"{front}\t{back}")

# Part 3
t4_p3 = [
    # Q32-34
    (32, 34, 32, "Why was the ferry service delayed?", "B", [
        ("A", "Engine maintenance"), ("B", "Rough water / severe weather"), ("C", "Crew shortage"), ("D", "Bridge repair")
    ], 'Man: "...port authority has suspended all marine traffic due to rough water."'),
    (32, 34, 33, "When are operations expected to resume?", "C", [
        ("A", "In 1 hour"), ("B", "In 2 hours"), ("C", "In about 3 hours"), ("D", "Tomorrow morning")
    ], 'Man: "This storm is expected to pass in about 3 hours, but operations should return to normal after that."'),
    (32, 34, 34, "What does the man remind the woman about her ticket?", "A", [
        ("A", "It is valid until midnight"), ("B", "It can be refunded online"), ("C", "It includes meal vouchers"), ("D", "It requires seat re-assignment")
    ], 'Man: "Your ticket will be good until midnight."'),

    # Q35-37
    (35, 37, 35, "What type of business do the speakers own?", "A", [
        ("A", "A bakery / pastry shop"), ("B", "A flower boutique"), ("C", "A coffee roasting plant"), ("D", "A bookstore cafe")
    ], 'Woman: "Our custom wedding cakes have been so popular this wedding season!"'),
    (35, 37, 36, "What equipment problem is discussed?", "C", [
        ("A", "A broken delivery van"), ("B", "A leaky refrigerator"), ("C", "A commercial mixer motor failed"), ("D", "A display glass cracked")
    ], 'Man: "The motor in our heavy-duty commercial mixer burned out yesterday afternoon."'),
    (35, 37, 37, "What does the woman suggest doing?", "B", [
        ("A", "Renting equipment"), ("B", "Borrowing a mixer from a nearby bakery"), ("C", "Canceling weekend orders"), ("D", "Buying a new mixer immediately")
    ], 'Woman: "Let’s ask Clara at Sweet Delights down the street. She has an extra mixer we might borrow."'),

    # Q38-40
    (38, 40, 38, "Where is the man traveling to?", "C", [
        ("A", "London"), ("B", "Tokyo"), ("C", "Chicago for a medical conference"), ("D", "Sydney for vacation")
    ], 'Man: "I’m heading to Chicago next Tuesday for the international medical conference."'),
    (38, 40, 39, "What travel arrangement does the woman help with?", "A", [
        ("A", "Booking a hotel near the convention center"), ("B", "Arranging a rental vehicle"), ("C", "Rescheduling a flight"), ("D", "Purchasing train passes")
    ], 'Woman: "I found a hotel just two blocks from the convention hall that has rooms within our per diem limit."'),
    (38, 40, 40, "What does the woman ask the man to provide?", "D", [
        ("A", "His passport number"), ("B", "A presentation copy"), ("C", "Emergency contacts"), ("D", "His frequent flyer number")
    ], 'Woman: "Could you email me your frequent flyer number so I can attach it to your flight booking?"'),

    # Q41-43
    (41, 43, 41, "What department do the speakers work in?", "B", [
        ("A", "Legal"), ("B", "Human Resources"), ("C", "Marketing"), ("D", "Accounting")
    ], 'Woman: "We need to finalize the orientation schedule for the ten new software engineers starting next month."'),
    (41, 43, 42, "What change to the schedule is proposed?", "A", [
        ("A", "Moving the IT setup session to morning"), ("B", "Extending the lunch break"), ("C", "Inviting the CEO for a speech"), ("D", "Postponing the benefits review")
    ], 'Man: "Why don’t we have the IT department issue their laptops and set up their logins first thing in the morning?"'),
    (41, 43, 43, "What will the woman do next?", "C", [
        ("A", "Send offer letters"), ("B", "Order catered lunches"), ("C", "Contact the IT manager"), ("D", "Reserve a training room")
    ], 'Woman: "I’ll check in with the IT manager today to make sure they can accommodate that timing."'),

    # Q44-46
    (44, 46, 44, "What are the speakers discussing?", "D", [
        ("A", "A restaurant expansion"), ("B", "A corporate restructuring"), ("C", "A new ad campaign"), ("D", "A new office security policy")
    ], 'Man: "Beginning next Monday, all employees must badge in at the front turnstiles."'),
    (44, 46, 45, "What concern does the woman express?", "A", [
        ("A", "Long wait times during morning arrival"), ("B", "Lost ID replacement costs"), ("C", "Visitors feeling unwelcome"), ("D", "Parking garage access")
    ], 'Woman: "I’m worried lines will back up out the front door between 8:30 and 9:00 AM."'),
    (44, 46, 46, "How will management address the issue?", "B", [
        ("A", "Installing facial scanners"), ("B", "Adding security staff to guide lines"), ("C", "Staggering work hours"), ("D", "Delaying implementation")
    ], 'Man: "Facilities is stationing two security guards at the turnstiles for the first two weeks to help assist people."'),

    # Q47-49
    (47, 49, 47, "Why is the woman calling the hotel?", "B", [
        ("A", "To cancel a suite"), ("B", "To ask about shuttle transportation to the airport"), ("C", "To complain about room service"), ("D", "To inquire about meeting rooms")
    ], 'Woman: "Does your hotel provide a complimentary shuttle to the international airport?"'),
    (47, 49, 48, "What does the front desk agent tell the woman?", "C", [
        ("A", "The shuttle is fully booked"), ("B", "There is a $20 service fee"), ("C", "The shuttle runs every thirty minutes on the hour"), ("D", "She must take a taxi")
    ], 'Man: "Yes, our airport shuttle departs from the front entrance every thirty minutes, 24 hours a day."'),
    (47, 49, 49, "What does the woman request?", "A", [
        ("A", "A wake-up call at 5:00 AM"), ("B", "An early checkout invoice"), ("C", "Breakfast in a bag"), ("D", "Extra pillows")
    ], 'Woman: "Great. Could you also schedule a wake-up call for my room at 5:00 AM tomorrow?"'),

    # Q50-52
    (50, 52, 50, "What type of product is being launched?", "A", [
        ("A", "An electric bicycle"), ("B", "A solar lawnmower"), ("C", "A fitness watch"), ("D", "A camping tent")
    ], 'Man: "Our new lightweight e-bike, the Urban Glide, is hitting retail stores in two weeks."'),
    (50, 52, 51, "What promotional strategy does the team agree on?", "C", [
        ("A", "Radio commercials"), ("B", "Billboards downtown"), ("C", "Partnering with social media influencers"), ("D", "Offering half-price coupons")
    ], 'Woman: "We’ve partnered with five popular cycling influencers on social media to post ride videos."'),
    (50, 52, 52, "What will the man check before Friday?", "B", [
        ("A", "The assembly plant speed"), ("B", "The warehouse inventory counts"), ("C", "Warranty terms"), ("D", "Competitor prices")
    ], 'Man: "I’ll make sure our regional warehouses have received enough initial stock units before Friday."'),

    # Q53-55
    (53, 55, 53, "What is the problem with the conference room?", "B", [
        ("A", "Air conditioning is broken"), ("B", "The video projector is not displaying color correctly"), ("C", "Chairs are missing"), ("D", "The Wi-Fi network is down")
    ], 'Woman: "The colors on the overhead projector in Room B are completely washed out and tinted yellow."'),
    (53, 55, 54, "Why is fixing it urgent?", "A", [
        ("A", "A client presentation starts in 30 minutes"), ("B", "The CEO is hosting an all-hands"), ("C", "A board meeting is tomorrow"), ("D", "A press conference is scheduled")
    ], 'Man: "Our international clients will be dialing in for our design review in thirty minutes!"'),
    (53, 55, 55, "What solution is chosen?", "C", [
        ("A", "Using paper printouts"), ("B", "Calling building maintenance"), ("C", "Moving the meeting to Conference Room D"), ("D", "Replacing the projector bulb")
    ], 'Woman: "Conference Room D next door is empty right now. Let’s just move the laptop and materials in there."'),

    # Q56-58
    (56, 58, 56, "Where do the speakers work?", "A", [
        ("A", "At a public library"), ("B", "In a university bookstore"), ("C", "At an art museum"), ("D", "In a local elementary school")
    ], 'Man: "Our summer children’s reading club at the library has reached over 200 participants!"'),
    (56, 58, 57, "What event is planned for the weekend?", "B", [
        ("A", "A book sale"), ("B", "A storytelling session by a local author"), ("C", "A poetry contest"), ("D", "A puppet show")
    ], 'Woman: "Local author Marcus Vance will be here this Saturday to read from his new illustrated book."'),
    (56, 58, 58, "What does the woman ask the man to do?", "D", [
        ("A", "Order more bookmarks"), ("B", "Design a banner"), ("C", "Set up extra chairs in the auditorium"), ("D", "Post an announcement on the library’s social media")
    ], 'Woman: "Could you create a promotional graphic and post it to our social media pages today?"'),

    # Q59-61
    (59, 61, 59, "What is the focus of the news report?", "B", [
        ("A", "A newly opened highway bypass"), ("B", "A city recycling and compost initiative"), ("C", "A public park expansion"), ("D", "A farmers market opening")
    ], 'Speaker 1: "The city council recently voted to expand weekly curbside composting to all residential neighborhoods."'),
    (59, 61, 60, "What benefit does the city official highlight?", "A", [
        ("A", "Diverting thousands of tons of organic waste from landfills"), ("B", "Lowering city property taxes"), ("C", "Creating public park jobs"), ("D", "Generating electric power")
    ], 'Speaker 2: "This program will divert more than thirty percent of our household waste away from regional landfills."'),
    (59, 61, 61, "How can residents get a free compost bin?", "C", [
        ("A", "Picking one up at City Hall"), ("B", "Buying one at local hardware stores"), ("C", "Signing up on the municipal department of sanitation website"), ("D", "Calling a hotline number")
    ], 'Speaker 1: "Residents can register online at the city sanitation portal to receive a free kitchen compost bin."'),

    # Q62-64
    (62, 64, 62, "Why is the woman contacting the courier company?", "A", [
        ("A", "To track an urgent medical shipment"), ("B", "To complain about damaged merchandise"), ("C", "To change a delivery address"), ("D", "To request an invoice copy")
    ], 'Woman: "I need to check the delivery status of a package containing sensitive laboratory samples."'),
    (62, 64, 63, "Look at the graphic. Where is the package currently located?", "C", [
        ("A", "Dispatched from origin hub"), ("B", "In transit on flight 302"), ("C", "At the regional sorting facility"), ("D", "Out for final delivery")
    ], 'Man: "According to tracking code MX-804, it arrived at our regional sorting facility at 6:30 this morning."'),
    (62, 64, 64, "When is the guaranteed delivery time?", "B", [
        ("A", "By 10:00 AM"), ("B", "By 1:00 PM today"), ("C", "By 5:00 PM today"), ("D", "Tomorrow morning")
    ], 'Man: "With Priority Express service, it is scheduled for delivery before 1:00 PM today."'),

    # Q65-67
    (65, 67, 65, "What type of business are the speakers visiting?", "B", [
        ("A", "A textile manufacturer"), ("B", "A commercial coffee roastery"), ("C", "A commercial bakery"), ("D", "A microbrewery")
    ], 'Man: "Welcome to Alpine Roasters. We roast specialty coffee beans from eleven countries."'),
    (65, 67, 66, "Look at the graphic. Which blend has the highest acidity profile?", "A", [
        ("A", "Ethiopian Yirgacheffe"), ("B", "Sumatra Mandheling"), ("C", "Colombian Supremo"), ("D", "Guatemala Antigua")
    ], 'Woman: "Our cafe customers love bright, fruity acidity. Which blend stands out for that?" -> Ethiopian Yirgacheffe.'),
    (65, 67, 67, "What offer does the roastery manager make?", "C", [
        ("A", "Free brewing equipment"), ("B", "A free tasting workshop for cafe staff"), ("C", "A 10% discount on standing wholesale subscriptions"), ("D", "Free branded ceramic cups")
    ], 'Man: "If you sign up for a monthly wholesale subscription today, we discount your first three orders by ten percent."'),

    # Q68-70
    (68, 70, 68, "What is the purpose of the meeting?", "A", [
        ("A", "Selecting architectural finishes for a hospital wing"), ("B", "Interviewing construction contractors"), ("C", "Reviewing a medical equipment budget"), ("D", "Planning an open house")
    ], 'Woman: "We need to choose the flooring material for the pediatric outpatient clinic."'),
    (68, 70, 69, "Look at the graphic. Which flooring option is chosen?", "B", [
        ("A", "Polished Terrazzo"), ("B", "Seamless Antimicrobial Vinyl"), ("C", "Ceramic Tile"), ("D", "Natural Hardwood")
    ], 'Man: "For ease of sanitation and slip resistance, the antimicrobial seamless vinyl is our top recommendation."'),
    (68, 70, 70, "What does the architect promise to send tomorrow?", "D", [
        ("A", "A 3D virtual model"), ("B", "Material cost sheets"), ("C", "Warranty certificates"), ("D", "Physical color samples for the vinyl")
    ], 'Woman: "I’ll have our supplier courier over physical color samples of the vinyl tomorrow morning."')
]

for s, e, q_num, q_txt, ans, opts, trans in t4_p3:
    front = f'Part 3 - Câu {q_num}<br><br>[sound:test4_part3_c{s}_{e}.mp3]<br><b>Question {q_num}: {q_txt}</b><br><br><div class="mc-container" data-ans="{ans}">'
    for l, txt in opts:
        front += f'<button class="mc-btn" onclick="checkMC(this, \'{l}\')">({l}) {txt}</button>'
    front += f'</div>'
    correct_text = [t for l, t in opts if l == ans][0]
    back = f'<b>Đáp án đúng: ({ans}) {correct_text}</b><br><br><i>Transcript trích đoạn:</i> {trans}'
    t4_cards.append(f"{front}\t{back}")

# Write Test 4 deck
t4_header = "#separator:tab\n#html:true\n#tags:TOEIC_Listening_Test4\n\n"
t4_out = "TOEIC_Listening_Test4_Audio_Interactive.txt"
with open(t4_out, "w", encoding="utf-8") as f:
    f.write(t4_header + "\n".join(t4_cards) + "\n")
print(f"[+] ĐÃ TẠO XONG TEST 4: {t4_out} ({len(t4_cards)} thẻ)")
