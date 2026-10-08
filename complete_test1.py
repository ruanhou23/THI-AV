import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Let's check if TOEIC_Listening_Test1_Audio_Interactive.txt has 34 or 70
with open("TOEIC_Listening_Test1_Audio_Interactive.txt", "r", encoding="utf-8") as f:
    t1_content = f.read()

# Let's complete Q35-70 for Test 1 if needed
p3_extra_t1 = [
    # Q35-37
    (35, 37, 35, "What department do the speakers most likely work in?", "B", [
        ("A", "Human Resources"), ("B", "Accounting / Finance"), ("C", "Marketing"), ("D", "Legal")
    ], "Accounting / Finance (Phòng Kế toán / Tài chính)", 'Woman: "Calculating company\'s expense reports, reviewing travel reimbursement forms..."'),
    (35, 37, 36, "What problem does the woman mention?", "A", [
        ("A", "A hotel accommodation is not on the approved list"), ("B", "A receipt was lost"), ("C", "A deadline was missed"), ("D", "A budget limit was exceeded")
    ], "A hotel accommodation is not on the approved list (Khách sạn không nằm trong danh mục duyệt chi)", 'Woman: "...our policy is for employees to stay at a hotel that\'s on our list of approved accommodations. This one isn\'t on the list."'),
    (35, 37, 37, "What does the man say he will do?", "C", [
        ("A", "Call the hotel manager"), ("B", "Reject the reimbursement"), ("C", "Approve an expense this one time"), ("D", "Consult with human resources")
    ], "Approve an expense this one time (Phê duyệt chi phí lần này)", 'Man: "As a supervisor, I can approve the expense this one time."'),

    # Q38-40
    (38, 40, 38, "What industry do the speakers most likely work in?", "D", [
        ("A", "Aviation"), ("B", "Rail transport"), ("C", "Road freight"), ("D", "Shipping / Maritime transport")
    ], "Shipping / Maritime transport (Vận tải biển / Hàng hải)", 'Man: "...up here on deck? ...our cargo ship still hasn\'t moved yet."'),
    (38, 40, 39, "What is the reason for a delay?", "A", [
        ("A", "Bad weather / Fog"), ("B", "Mechanical breakdown"), ("C", "Customs clearance"), ("D", "Dock worker strike")
    ], "Bad weather / Fog (Thời tiết xấu, sương mù dày đặc)", 'Woman: "I hope the fog over the harbor lifts soon... The ship won\'t be able to leave until the weather improves."'),
    (38, 40, 40, "What does the man say he will do?", "B", [
        ("A", "Inspect cargo containers"), ("B", "Contact the port authority"), ("C", "Chart a new course"), ("D", "Order more fuel")
    ], "Contact the port authority (Gọi điện cho cảng vụ)", 'Man: "I\'ll be sure to call the port authority soon for an update on when we\'ll be cleared to leave."'),

    # Q41-43
    (41, 43, 41, "Why is the woman at the restaurant?", "B", [
        ("A", "To apply for a chef job"), ("B", "To meet with clients for lunch"), ("C", "To organize a birthday party"), ("D", "To pick up takeout food")
    ], "To meet with clients for lunch (Gặp đối tác ăn trưa)", 'Woman: "Hi, I\'ve made a reservation to meet with some clients for lunch today."'),
    (41, 43, 42, "What does the woman mean when she says, 'It\'s very hot today'?", "C", [
        ("A", "She wants an iced beverage"), ("B", "The air conditioner should be turned on"), ("C", "She prefers to sit inside"), ("D", "The kitchen is too warm")
    ], "She prefers to sit inside (Cô ấy muốn ngồi trong nhà thay vì ngoài trời)", 'Woman: "I know I asked to be seated on your beautiful terrace, but it\'s very hot today."'),
    (41, 43, 43, "What does the man say about a parking garage?", "A", [
        ("A", "Customers can park there for free with a validated ticket"), ("B", "It is closed for repaving"), ("C", "It is only open after 5:00 PM"), ("D", "It requires valet parking")
    ], "Customers can park there for free with a validated ticket (Đỗ xe miễn phí bên kia đường khi được đóng dấu vé)", 'Man: "Our customers can park for free in the garage across the street. Our cashier will stamp their parking tickets."'),

    # Q44-46
    (44, 46, 44, "Where does the woman most likely work?", "A", [
        ("A", "An electronics retail store"), ("B", "A library"), ("C", "A software company"), ("D", "An internet provider")
    ], "An electronics retail store (Cửa hàng bán đồ điện tử)", 'Woman: "...the store will be busy because we\'re having a big sale on laptop computers and tablets."'),
    (44, 46, 45, "What does Murat ask about?", "B", [
        ("A", "Product warranty policies"), ("B", "The location to put a demonstration table"), ("C", "Store opening hours"), ("D", "Cash register operations")
    ], "The location to put a demonstration table (Vị trí đặt bàn chạy thử sản phẩm)", 'Murat: "Yes, where can I put our demonstration table?"'),
    (44, 46, 46, "What does the woman suggest doing?", "C", [
        ("A", "Offering a discount coupon"), ("B", "Giving out free pens"), ("C", "Displaying brochures for customers"), ("D", "Demonstrating accessories")
    ], "Displaying brochures for customers (Bày tờ rơi giới thiệu cho khách lấy)", 'Woman: "...if you brought any brochures with you, it\'ll be helpful to put those out for people to take."'),

    # Q47-49
    (47, 49, 47, "What type of industry do the speakers most likely work in?", "A", [
        ("A", "Food / Bakery manufacturing"), ("B", "Cosmetics"), ("C", "Pharmaceuticals"), ("D", "Clothing retail")
    ], "Food / Bakery manufacturing (Ngành thực phẩm / làm bánh)", 'Man: "...sales of our brands of cakes, pies, and cookies this past holiday season."'),
    (47, 49, 48, "What business challenge are the speakers discussing?", "C", [
        ("A", "Supply chain disruptions"), ("B", "Package labeling laws"), ("C", "Reducing sugar content while keeping good taste"), ("D", "Rising flour prices")
    ], "Reducing sugar content while keeping good taste (Giảm hàm lượng đường mà vẫn giữ vị ngon)", 'Woman: "The biggest trend right now is the reduction of sugar. The public wants healthier products, but the same great taste."'),
    (47, 49, 49, "What does the man say he will do?", "B", [
        ("A", "Review sales figures"), ("B", "Investigate supplier sweeteners tomorrow"), ("C", "Conduct customer focus groups"), ("D", "Contact marketing consultants")
    ], "Do research / investigation on suppliers\' sweeteners (Tìm hiểu, nghiên cứu thêm về chất tạo ngọt)", 'Hector: "I\'d have to do some investigation to find out more about that. I have some time available tomorrow afternoon."'),

    # Q50-52
    (50, 52, 50, "Why is the man calling?", "B", [
        ("A", "To reschedule a meeting"), ("B", "To offer project work to the woman"), ("C", "To ask for references"), ("D", "To submit an invoice")
    ], "To offer project work / request assistance on a marketing project (Mời làm việc cho một dự án tiếp thị)", 'Man: "I\'m calling to see if you\'d have time to work on a project for my marketing firm."'),
    (50, 52, 51, "What does the man say a client is interested in doing?", "C", [
        ("A", "Expanding retail stores"), ("B", "Redesigning a company logo"), ("C", "Creating a marketing campaign for social media"), ("D", "Launching a television commercial")
    ], "Creating a marketing campaign for social media (Tạo chiến dịch tiếp thị trên mạng xã hội)", 'Man: "...a new client in Brazil who\'s interested in creating a marketing campaign for social media sites."'),
    (50, 52, 52, "What does the woman ask the man to send?", "A", [
        ("A", "A detailed description of the job"), ("B", "A contract draft"), ("C", "A payment schedule"), ("D", "A portfolio sample")
    ], "A detailed description of the job (Bản mô tả công việc chi tiết)", 'Woman: "Why don\'t you send me a detailed description of the work?"'),

    # Q53-55
    (53, 55, 53, "What problem does the woman mention?", "A", [
        ("A", "A vehicle has a flat tire"), ("B", "Food spoiled in coolers"), ("C", "An event was postponed"), ("D", "Utensils are missing")
    ], "A vehicle has a flat tire (Một xe van chở hàng bị thủng lốp)", 'Woman: "...van number 5 for the music festival when we noticed it\'s got a flat tire."'),
    (53, 55, 54, "Where do the speakers most likely work?", "D", [
        ("A", "An auto repair shop"), ("B", "A music festival venue"), ("C", "A grocery store"), ("D", "A catering company")
    ], "A catering company (Công ty phục vụ ăn uống / tiệc lưu động)", 'Woman: "We\'ve got a lot of catering jobs today... The food\'s already in coolers, but everything\'s in the kitchen with the serving utensils..."'),
    (53, 55, 55, "What does the man say he will do next?", "B", [
        ("A", "Change the vehicle tire"), ("B", "Help carry food and utensils to the parking area"), ("C", "Cook more food"), ("D", "Call the festival coordinator")
    ], "Help load items into the van (Giúp khuân đồ/đồ ăn ra xe)", 'Man: "All right, I can help with that."'),

    # Q56-58
    (56, 58, 56, "Why is the man calling the woman?", "B", [
        ("A", "To apply for an editing vacancy"), ("B", "To learn about a career in journalism"), ("C", "To subscribe to a university paper"), ("D", "To pitch a news article")
    ], "To learn about a career in journalism (Để tìm hiểu về ngành nghề/báo chí)", 'Man: "I\'m interested in working in your field, but I\'m talking to some professionals first so I can find out more about it."'),
    (56, 58, 57, "Who most likely is the woman?", "C", [
        ("A", "A university professor"), ("B", "A graphic designer"), ("C", "A newspaper editor / journalist"), ("D", "A publishing sales agent")
    ], "A journalist / newspaper editor (Nhà báo / biên tập viên tòa soạn báo)", 'Woman: "...I joined the newspaper and eventually worked my way up to being an editor."'),
    (56, 58, 58, "What will the woman most likely do next?", "A", [
        ("A", "Describe her work hours and schedule"), ("B", "Review the man\'s resume"), ("C", "Introduce him to a colleague"), ("D", "Give him an office tour")
    ], "Describe her work hours/schedule (Mô tả lịch trình, giờ làm việc của mình)", 'Man: "Is it true that people in the news business work very long hours? So what\'s your schedule like?"'),

    # Q59-61
    (59, 61, 59, "What are the speakers mainly discussing?", "A", [
        ("A", "A company merger"), ("B", "A new office lease"), ("C", "An employee pension plan"), ("D", "A software transition")
    ], "A company merger (Vụ sáp nhập công ty)", 'Man: "...the proposed merger with QZ Corporation. It looks like we\'re going ahead with it."'),
    (59, 61, 60, "Why does the woman say, 'They also talked about it last year'?", "B", [
        ("A", "To praise executive efficiency"), ("B", "To express doubt about finalizing"), ("C", "To suggest waiting until next year"), ("D", "To confirm employee support")
    ], "To express doubt or note that previous talks did not finalize (Lưu ý rằng thương vụ từng được thảo luận nhưng chưa chốt)", 'Woman: "There would be a lot of advantages to merging operations, although they also talked about it last year."'),
    (59, 61, 61, "What does the woman want to avoid?", "C", [
        ("A", "Learning a new system"), ("B", "Managing extra staff"), ("C", "Relocating to another city"), ("D", "Working longer shifts")
    ], "Relocating / Moving to another city (Việc phải chuyển văn phòng / chuyển chỗ ở)", 'Woman: "Well, I really don\'t want to move, so that\'s a relief."'),

    # Q62-64
    (62, 64, 62, "Who is a gift for?", "B", [
        ("A", "Basketball tournament winners"), ("B", "All company employees"), ("C", "Key corporate clients"), ("D", "Visiting vendors")
    ], "Company employees (Nhân viên trong công ty)", 'Woman: "My company wants to give every employee a gift."'),
    (62, 64, 63, "Look at the graphic. What is the price of the item the man recommends?", "A", [
        ("A", "Giá tương ứng với 'Metal bottle with wide-mouthed lid'"), ("B", "Model A price"), ("C", "Model C price"), ("D", "Model D price")
    ], "Căn cứ vào bảng giá tương ứng với 'Metal bottle with wide-mouthed lid'", 'Man: "I recommend the metal bottle with the wide-mouthed lid. It\'s easier to clean than the one with the straw."'),
    (62, 64, 64, "What is the woman going to send to the man?", "C", [
        ("A", "A payment receipt"), ("B", "Employee delivery addresses"), ("C", "A company logo graphics file"), ("D", "A color chart")
    ], "A graphics file / logo file (Tập tin thiết kế logo công ty)", 'Man: "Yes, you\'ll just need to send me the graphics file. - Woman: I can do that."'),

    # Q65-67
    (65, 67, 65, "What type of art will be displayed in an exhibit?", "B", [
        ("A", "Oil landscapes"), ("B", "Pencil drawings"), ("C", "Bronze sculptures"), ("D", "Color photographs")
    ], "Pencil drawings (Tranh vẽ bằng bút chì)", 'Man: "Yoon, I just finished recording the audio guide for the pencil drawings..."'),
    (65, 67, 66, "Look at the graphic. Which piece of artwork will no longer be included?", "D", [
        ("A", "Piece by Andrea Kim"), ("B", "Piece by David Ortiz"), ("C", "Piece by Sarah Lee"), ("D", "The drawing by Claudia Hoffman")
    ], "Tác phẩm tương ứng của tác giả 'Claudia Hoffman'", 'Woman: "The drawing by Claudia Hoffman will no longer be in the exhibit."'),
    (65, 67, 67, "What does the woman say she will do right away?", "A", [
        ("A", "Update the audio guide recording"), ("B", "Print replacement brochures"), ("C", "Contact Claudia Hoffman"), ("D", "Hang a new artwork")
    ], "Update / modify the audio guide recording (Chỉnh sửa lại bản ghi âm hướng dẫn)", 'Woman: "Okay, then I\'ll make that change to the audio guide recording. I\'ll do that right away."'),

    # Q68-70
    (68, 70, 68, "Who most likely are the speakers?", "C", [
        ("A", "Construction managers"), ("B", "City council members"), ("C", "Reporters / Journalists"), ("D", "Wind turbine technicians")
    ], "Reporters / Journalists (Phóng viên, nhà báo đưa tin)", 'Man: "I counted seven other major media networks there in addition to ours... Let\'s compare our facts before we start writing."'),
    (68, 70, 69, "Look at the graphic. Which site has already been completed?", "B", [
        ("A", "Avondale"), ("B", "Winsten"), ("C", "Oakridge"), ("D", "Brookfield")
    ], "Winsten", 'Woman: "So the largest cluster of wind turbines, off the coast of Winsten, is already built."'),
    (68, 70, 70, "What does the man suggest focusing on?", "A", [
        ("A", "Job creation in turbine assembly and maintenance"), ("B", "Environmental impact on fish"), ("C", "Government subsidies"), ("D", "Electricity rate changes")
    ], "Job creation / new job opportunities (Số lượng việc làm mới được tạo ra)", 'Man: "...it\'s crucial for us to focus on how many new jobs related to assembling and maintaining the turbines are opening up in the area..."')
]

extra_cards = []
for s, e, q_num, q_txt, ans, opts, ans_lbl, trans in p3_extra_t1:
    front = f'Part 3 - Câu {q_num}<br><br>[sound:part3_c{s}_{e}.mp3]<br><b>Question {q_num}: {q_txt}</b><br><br><div class="mc-container" data-ans="{ans}">'
    for l, txt in opts:
        front += f'<button class="mc-btn" onclick="checkMC(this, \'{l}\')">({l}) {txt}</button>'
    front += f'</div>'
    correct_text = [t for l, t in opts if l == ans][0]
    back = f'<b>Đáp án đúng: ({ans}) {correct_text}</b><br><br><i>Transcript trích đoạn:</i> {trans}'
    extra_cards.append(f"{front}\t{back}")

# Update Test 1 file
new_t1_content = t1_content.strip() + "\n" + "\n".join(extra_cards) + "\n"
with open("TOEIC_Listening_Test1_Audio_Interactive.txt", "w", encoding="utf-8") as f:
    f.write(new_t1_content)

print(f"[+] ĐÃ HOÀN TẤT BỔ SUNG TEST 1: Hiện đã đủ 70 câu!")
