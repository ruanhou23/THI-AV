import os
import sys
import shutil

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Paths
SPLIT_BASE = "Listening practice test 2/audio_split"
LOCAL_MEDIA_DIR = "test2_media"
os.makedirs(LOCAL_MEDIA_DIR, exist_ok=True)

appdata = os.environ.get('APPDATA', '')
ANKI_MEDIA_DIR = os.path.join(appdata, "Anki2", "Người dùng 1", "collection.media")

mc_script = """<script>function checkMC(btn, choice){var parent = btn.parentElement; if(parent.dataset.answered) return; parent.dataset.answered = "true"; var correct = parent.dataset.ans; var btns = parent.getElementsByTagName("button"); for(var i=0; i<btns.length; i++){ if(btns[i].textContent.trim().startsWith("(" + correct + ")")){ btns[i].style.background = "#28a745"; btns[i].style.color = "#fff"; } } if(choice !== correct){ btn.style.background = "#dc3545"; btn.style.color = "#fff"; }}</script>"""

cards = []

# ==================== PART 1 ====================
p1_data = [
    (1, "A", [
        ("A", "She’s inserting a cord into an outlet."),
        ("B", "She’s pressing a button on a machine."),
        ("C", "She’s gripping the handle of a drawer."),
        ("D", "She’s tacking a notice onto the wall.")
    ], "Người phụ nữ đang cắm dây điện vào ổ cắm trên tường."),
    (2, "B", [
        ("A", "Some window shutters are being replaced."),
        ("B", "A pillow is being arranged on a seat."),
        ("C", "An outdoor table is being cleared off."),
        ("D", "Some wooden boards are being painted.")
    ], "Người phụ nữ đang sắp xếp lại gối trên chiếc ghế dài ngoài hiên."),
    (3, "C", [
        ("A", "Some utensils have been discarded in a bin."),
        ("B", "Some bottles are being emptied into a sink."),
        ("C", "A rolling chair has been placed next to a counter."),
        ("D", "Some drawers have been left open.")
    ], "Một chiếc ghế xoay có bánh xe được đặt cạnh quầy tủ."),
    (4, "D", [
        ("A", "A man is chopping some wood into pieces."),
        ("B", "Leaves are scattered across the grass."),
        ("C", "A man is closing a window."),
        ("D", "Wood is piled near a fence.")
    ], "Gỗ được chất thành đống ở gần hàng rào phía sau sân."),
    (5, "C", [
        ("A", "People are standing in line in a lobby."),
        ("B", "Items are being loaded into shopping bags."),
        ("C", "Tents have been set up in a parking area."),
        ("D", "A worker is putting up a canopy.")
    ], "Những chiếc lều bạt được dựng trong khu vực bãi đỗ xe."),
    (6, "D", [
        ("A", "Some luggage is stacked next to an escalator."),
        ("B", "A suitcase is being lifted onto a shuttle bus."),
        ("C", "Some suitcases are displayed in a shop window."),
        ("D", "A luggage rack has two levels.")
    ], "Giá để hành lý có hai tầng (tầng trên và tầng dưới đều để va li).")
]

for q_num, ans, opts, exp in p1_data:
    front = f'Part 1 - Câu {q_num}<br><br><img src="test2_part1_q{q_num:02d}.png"><br>[sound:test2_part1_q{q_num:02d}.mp3]<br><br><div class="mc-container" data-ans="{ans}">'
    for l, txt in opts:
        front += f'<button class="mc-btn" onclick="checkMC(this, \'{l}\')">({l}) {txt}</button>'
    front += f'</div>{mc_script}'
    
    correct_text = [t for l, t in opts if l == ans][0]
    back = f'<b>Đáp án đúng: ({ans}) {correct_text}</b><br><br><b>Giải thích:</b> {exp}'
    cards.append(f"{front}\t{back}")

# ==================== PART 2 ====================
p2_data = [
    (7, "Have the machines on the factory floor been cleaned?", "A", [
        ("A", "No, not yet."),
        ("B", "It’s in the shipping container."),
        ("C", "I just put it in the trash bin.")
    ], 'Hỏi máy móc trên sàn nhà máy đã được dọn sạch chưa. Đáp án A xác nhận chưa làm.'),
    (8, "How much will the budget increase next year?", "A", [
        ("A", "About 10%."),
        ("B", "3 hours, I think."),
        ("C", "At the bank’s main branch.")
    ], 'Hỏi ngân sách năm tới sẽ tăng bao nhiêu. Đáp án A trả lời về tỷ lệ phần trăm (khoảng 10%).'),
    (9, "You’re going to water the plants before you leave, aren’t you?", "B", [
        ("A", "I walked the whole way."),
        ("B", "Yes, right after lunch."),
        ("C", "In the break room.")
    ], 'Hỏi xác nhận hành động tưới cây trước khi rời đi. Đáp án B đồng ý và nêu rõ thời điểm (ngay sau bữa trưa).'),
    (10, "Aren’t you going to schedule an eye doctor appointment?", "B", [
        ("A", "Those glasses look nice on you."),
        ("B", "I already scheduled one."),
        ("C", "The seminar is three days long.")
    ], 'Hỏi về việc đặt lịch khám mắt. Đáp án B trả lời mình đã đặt lịch rồi.'),
    (11, "I’m going to try to fix this printer.", "C", [
        ("A", "You’re right, it doesn’t fit."),
        ("B", "Double-sided copies."),
        ("C", "Are you sure it can be repaired?")
    ], 'Thông báo ý định sửa máy in. Đáp án C hỏi lại thể hiện sự nghi ngờ về khả năng sửa được.'),
    (12, "What should we do with these brochures?", "C", [
        ("A", "A trip to the seashore."),
        ("B", "Yes, I found it already."),
        ("C", "I’ll leave them at the front desk.")
    ], 'Hỏi nên làm gì với các tờ rơi. Đáp án C đề xuất để ở bàn lễ tân.'),
    (13, "Has the policy meeting been rescheduled?", "B", [
        ("A", "We have lots of desk calendar designs."),
        ("B", "Yes, it’s happening tomorrow instead."),
        ("C", "This soup I ordered is delicious.")
    ], 'Hỏi cuộc họp chính sách đã dời lịch chưa. Đáp án B xác nhận dời sang ngày mai.'),
    (14, "Why don’t we stop by the office cafeteria on our way to the workshop?", "A", [
        ("A", "Sure, we have time for that."),
        ("B", "A full-service buffet."),
        ("C", "The topic is professional networking.")
    ], 'Đề nghị ghé căng tin trên đường đến buổi hội thảo. Đáp án A đồng ý vì đủ thời gian.'),
    (15, "Have you tried our famous pasta dish?", "B", [
        ("A", "We need a table for five."),
        ("B", "Yes, it was delicious."),
        ("C", "I’ll try to make it on time.")
    ], 'Hỏi đã thử món mì Ý nổi tiếng chưa. Đáp án B khen món ăn ngon.'),
    (16, "Who’s the opening act at tonight’s concert?", "B", [
        ("A", "Could you turn up the volume?"),
        ("B", "A jazz singer from France."),
        ("C", "The position has been filled.")
    ], 'Hỏi ai là nghệ sĩ mở màn buổi biểu diễn. Đáp án B nêu ca sĩ jazz đến từ Pháp.'),
    (17, "When do the product demonstrations start?", "A", [
        ("A", "The schedule was emailed last Friday."),
        ("B", "Some innovative features."),
        ("C", "In room 202, I think.")
    ], 'Hỏi khi nào bắt đầu chạy thử sản phẩm. Đáp án A nhắc lịch đã gửi qua email.'),
    (18, "I tried updating the website, but it didn’t work.", "C", [
        ("A", "That date works for me."),
        ("B", "Usually our online reviews."),
        ("C", "Just send me the changes you want.")
    ], 'Nêu vấn đề cập nhật web không thành công. Đáp án C đề nghị gửi thông tin cần đổi.'),
    (19, "Did you hire a new welding specialist?", "B", [
        ("A", "The part's back-ordered."),
        ("B", "Yes, he starts tomorrow."),
        ("C", "No, it should be higher.")
    ], 'Hỏi đã tuyển chuyên gia hàn chưa. Đáp án B xác nhận anh ấy bắt đầu làm ngày mai.'),
    (20, "How was the color palette for the lobby chosen?", "C", [
        ("A", "Blue and orange."),
        ("B", "It was fine, thanks."),
        ("C", "I wasn’t involved.")
    ], 'Hỏi cách chọn bảng màu cho sảnh. Đáp án C nói mình không tham gia.'),
    (21, "When are we ordering more supplies for the office?", "B", [
        ("A", "In the storage closet."),
        ("B", "Next week on Monday."),
        ("C", "The new desk looks great.")
    ], 'Hỏi khi nào đặt thêm đồ dùng văn phòng. Đáp án B trả lời Thứ Hai tuần tới.'),
    (22, "The battery for the water pump is going to be solar powered, right?", "A", [
        ("A", "We’re still in the planning stages."),
        ("B", "$140 per year."),
        ("C", "Yes, I’d love a glass of water.")
    ], 'Xác nhận pin chạy bằng năng lượng mặt trời. Đáp án A cho biết vẫn đang lên kế hoạch.'),
    (23, "Where can I buy a charger for this laptop?", "B", [
        ("A", "Around 3 o’clock."),
        ("B", "I can order one for you."),
        ("C", "A limited return policy.")
    ], 'Hỏi nơi mua sạc máy tính. Đáp án B đề nghị đặt mua giúp.'),
    (24, "Do I need to reserve a meeting room?", "A", [
        ("A", "Yes, let me show you how."),
        ("B", "The service is good."),
        ("C", "My slide presentation.")
    ], 'Hỏi có cần đặt trước phòng họp không. Đáp án A bảo có và hướng dẫn cách làm.'),
    (25, "When’s the new department director supposed to start?", "B", [
        ("A", "It’s an hour long."),
        ("B", "Ms. Pavlova isn’t retiring for several weeks."),
        ("C", "No, that department’s upstairs.")
    ], 'Hỏi khi nào giám đốc mới nhậm chức. Đáp án B cho biết vài tuần nữa giám đốc cũ mới nghỉ hưu.'),
    (26, "Should I deliver these pizzas, or will you?", "C", [
        ("A", "No thanks, I’m not hungry."),
        ("B", "$10 for two."),
        ("C", "They’re being picked up.")
    ], 'Hỏi ai sẽ đi giao pizza. Đáp án C phủ định vì khách sẽ tự đến lấy.'),
    (27, "This month’s shipment schedule has been revised.", "B", [
        ("A", "I couldn’t find them either."),
        ("B", "Which dates have been changed?"),
        ("C", "$2 per pound.")
    ], 'Thông báo lịch giao hàng thay đổi. Đáp án B hỏi ngày nào bị đổi.'),
    (28, "How much will the repairs cost?", "A", [
        ("A", "The work is covered under the warranty plan."),
        ("B", "Yes, it’s also available in red."),
        ("C", "In about two weeks.")
    ], 'Hỏi chi phí sửa chữa. Đáp án A cho biết sửa chữa được bảo hành chi trả.'),
    (29, "Why don’t we provide more samples of the wallpaper patterns?", "C", [
        ("A", "The newspaper is delivered daily."),
        ("B", "An interior design course."),
        ("C", "There are plenty in the binders.")
    ], 'Đề xuất thêm mẫu giấy dán tường. Đáp án C cho biết đã có nhiều mẫu trong bìa hồ sơ.'),
    (30, "Can you give me a tour of the property this afternoon?", "A", [
        ("A", "Sorry, I won’t have time until tomorrow."),
        ("B", "It has a very modern design."),
        ("C", "A house on Maple Street.")
    ], 'Nhờ dẫn đi xem nhà chiều nay. Đáp án A từ chối khéo vì bận đến mai.'),
    (31, "Who’s scheduled to test the product today?", "A", [
        ("A", "We’re waiting for confirmation."),
        ("B", "It’s a great album, right?"),
        ("C", "About 6 weeks ago.")
    ], 'Hỏi ai kiểm thử sản phẩm hôm nay. Đáp án A cho biết đang đợi xác nhận.')
]

for q_num, q_txt, ans, opts, exp in p2_data:
    front = f'Part 2 - Câu {q_num}<br><br>[sound:test2_part2_q{q_num:02d}.mp3]<br><b>{q_txt}</b><br><br><div class="mc-container" data-ans="{ans}">'
    for l, txt in opts:
        front += f'<button class="mc-btn" onclick="checkMC(this, \'{l}\')">({l}) {txt}</button>'
    front += f'</div>'
    
    correct_text = [t for l, t in opts if l == ans][0]
    back = f'<b>Đáp án đúng: ({ans}) {correct_text}</b><br><br><i>Ngữ cảnh:</i> {exp}'
    cards.append(f"{front}\t{back}")

# ==================== PART 3 ====================
p3_data = [
    # Q32-34
    (32, 34, 32, "Where does the conversation most likely take place?", "C", [
        ("A", "At a train station"), ("B", "At a weather center"), ("C", "On a ship"), ("D", "In a repair shop")
    ], 'Man: "Good morning, Captain. We’ll be docking at the port in Kolkata this evening, right?"'),
    (32, 34, 33, "What caused a delay?", "B", [
        ("A", "Mechanical trouble"), ("B", "Bad weather"), ("C", "A customs inspection"), ("D", "A sick passenger")
    ], 'Woman: "Actually, we had to change course overnight to avoid a storm, so we’re running behind schedule."'),
    (32, 34, 34, "What will the man do next?", "D", [
        ("A", "Steer the vessel"), ("B", "Contact the port authority"), ("C", "Prepare some lunch"), ("D", "Check some equipment")
    ], 'Woman: "...checking the machinery in the engine room." - Man: "Of course, I’ll head there now."'),

    # Q35-37
    (35, 37, 35, "Where does the woman most likely work?", "A", [
        ("A", "At a fitness center"), ("B", "At a medical clinic"), ("C", "At a sporting goods store"), ("D", "At a community college")
    ], 'Man: "Hi, I’m here to schedule some personal training sessions." Woman: "...fitness goals?"'),
    (35, 37, 36, "What does the man ask about?", "C", [
        ("A", "Class schedules"), ("B", "Locker rentals"), ("C", "A special promotion"), ("D", "Parking availability")
    ], 'Man: "I saw online that you’re running a special for new members: 50% off the first month’s membership. Can I sign up for that?"'),
    (35, 37, 37, "What will the woman do next?", "B", [
        ("A", "Process a payment"), ("B", "Give a tour of a facility"), ("C", "Introduce an instructor"), ("D", "Demonstrate some equipment")
    ], 'Woman: "Absolutely. But before I get you signed up, let me show you around our facility."'),

    # Q38-40
    (38, 40, 38, "Who most likely are the speakers?", "C", [
        ("A", "Interior decorators"), ("B", "Real estate agents"), ("C", "Art conservators / Museum staff"), ("D", "Catering coordinators")
    ], 'Woman: "As you can see, this Renaissance landscape painting we acquired is in bad condition. We can’t display it yet."'),
    (38, 40, 39, "What does the woman say she will do?", "A", [
        ("A", "Research an artist\'s style"), ("B", "Frame an artwork"), ("C", "Consult with a donor"), ("D", "Order some canvas")
    ], 'Woman: "I’ll begin by investigating the artist’s color palette and style to see how we should repair the damaged areas."'),
    (38, 40, 40, "Why does the man suggest beginning a project quickly?", "D", [
        ("A", "A deadline was moved up"), ("B", "A sponsor made a special request"), ("C", "Supplies are running low"), ("D", "It should be ready for an upcoming event")
    ], 'Man: "...this would be a stunning piece to unveil at our anniversary dinner in June... we should get started right away."'),

    # Q41-43
    (41, 43, 41, "What is the woman preparing?", "B", [
        ("A", "A company budget"), ("B", "A marketing presentation"), ("C", "A contract agreement"), ("D", "An employee training session")
    ], 'Woman: "Hi Ozan, do you have time to review some slides I’m presenting at a meeting on Thursday?... our updated marketing plan..."'),
    (41, 43, 42, "What kind of business is Smith Incorporated?", "D", [
        ("A", "A grocery chain"), ("B", "An advertising agency"), ("C", "A law firm"), ("D", "A bookstore chain")
    ], 'Woman: "...for their chain of bookstores."'),
    (41, 43, 43, "What do the men agree about?", "A", [
        ("A", "An informal meeting style is preferable"), ("B", "A deadline should be extended"), ("C", "A client will decline an offer"), ("D", "Extra staff will be needed")
    ], 'Man 2: "Ozan is right. I think they’d prefer a meeting that was more of a conversation than a presentation."'),

    # Q44-46
    (44, 46, 44, "Why does the woman congratulate the man?", "A", [
        ("A", "A successful experiment"), ("B", "A promotion"), ("C", "An article publication"), ("D", "A new client contract")
    ], 'Woman: "I heard that the results of your experiment were better than you expected. Congratulations!"'),
    (44, 46, 45, "What does the man imply when he says, 'Ezra’s leaving the company next week'?", "B", [
        ("A", "A budget will be changed"), ("B", "He should not submit his report to Ezra"), ("C", "A position is being eliminated"), ("D", "An office will be remodeled")
    ], 'Woman: "You’ll have to write up your results and submit them to the research director. That’s Ezra, right?" - Man: "Oh, Ezra’s leaving the company next week."'),
    (44, 46, 46, "What does the man hope to do next quarter?", "C", [
        ("A", "Publish his research"), ("B", "Present at a seminar"), ("C", "Manage a research group"), ("D", "Transfer to another branch")
    ], 'Man: "I’ve never managed an entire research group. I hope to get some experience doing that next quarter."'),

    # Q47-49
    (47, 49, 47, "Where most likely are the speakers?", "A", [
        ("A", "At a broadcasting/news studio"), ("B", "At a sports arena"), ("C", "At a health club"), ("D", "In a college classroom")
    ], 'Woman: "...special segment of our news program... Thanks for coming into the studio today, Dhruv."'),
    (47, 49, 48, "What does the man say he recently did?", "B", [
        ("A", "Won an athletic competition"), ("B", "Opened a fitness center"), ("C", "Wrote a training manual"), ("D", "Purchased some equipment")
    ], 'Man: "...I’m excited to tell you about the gym I just opened last month."'),
    (47, 49, 49, "What does the woman ask the man to talk about?", "C", [
        ("A", "His training fees"), ("B", "His workout routine"), ("C", "How he began his career"), ("D", "His diet recommendations")
    ], 'Woman: "Sounds great! How did you get started in this line of work?"'),

    # Q50-52
    (50, 52, 50, "What has the woman been hired to do?", "B", [
        ("A", "Take photos of marine wildlife"), ("B", "Write content for a website"), ("C", "Plan fundraising galas"), ("D", "Lead research tours")
    ], 'Director: "We’re happy you’ll be producing content for our website." - Woman: "I’m looking forward to writing about Redmond’s initiatives..."'),
    (50, 52, 51, "According to the director, what is the organization’s goal?", "C", [
        ("A", "Promoting aquaculture businesses"), ("B", "Cleaning harbor waterways"), ("C", "Preserving aquatic ecosystems"), ("D", "Training wildlife biologists")
    ], 'Director: "Public awareness will help us get funding to meet our aim of preserving these ecosystems."'),
    (50, 52, 52, "What does Roberto say is exciting?", "A", [
        ("A", "Using drones for aerial photography"), ("B", "Receiving a research grant"), ("C", "Traveling to an overseas site"), ("D", "Finding a new mangrove species")
    ], 'Roberto: "And what’s exciting is that we’ve started using drones to photograph the area with the mangroves..."'),

    # Q53-55
    (53, 55, 53, "What does the man say about some contacts in China?", "B", [
        ("A", "They signed a revised agreement"), ("B", "They are on holiday"), ("C", "They visited Singapore"), ("D", "They postponed an experiment")
    ], 'Man: "...our research partners in China are off this week for a national holiday, so there’s no point in meeting."'),
    (53, 55, 54, "What does the woman imply when she says, 'We didn’t allocate funds for a project leader'?", "A", [
        ("A", "A budget meeting is necessary"), ("B", "An applicant was rejected"), ("C", "A project will be delayed"), ("D", "Extra staff must be recruited")
    ], 'Woman: "...we didn’t allocate funds for a project leader." - Man: "Uh-oh... You’re right. We need to discuss how to fix that."'),
    (53, 55, 55, "What does the woman say about some travel expenses?", "B", [
        ("A", "They were approved by a supervisor"), ("B", "They can be eliminated"), ("C", "They exceed previous estimates"), ("D", "They are partially reimbursed")
    ], 'Woman: "You know, we allocated money for a trip to Singapore to present our preliminary findings. We don’t really need to do that."'),

    # Q56-58
    (56, 58, 56, "Where is the woman calling from?", "B", [
        ("A", "A software development firm"), ("B", "A restaurant equipment company"), ("C", "A dining establishment"), ("D", "A cooking academy")
    ], 'Woman: "I’m calling from Reuben Restaurant Equipment. I recently purchased your software to keep track of my warehouse inventory..."'),
    (56, 58, 57, "What is some software being used for?", "A", [
        ("A", "Tracking warehouse inventory"), ("B", "Processing orders"), ("C", "Managing staff payroll"), ("D", "Scheduling deliveries")
    ], 'Woman: "...purchased your software to keep track of my warehouse inventory..."'),
    (56, 58, 58, "What does the man help the woman do?", "C", [
        ("A", "Update an account password"), ("B", "Request a replacement item"), ("C", "Adjust an alert setting"), ("D", "Download a user manual")
    ], 'Man: "...if you click on that product, you’ll see a link that says \'Set custom alert,\' and you can set it to any number from there."'),

    # Q59-61
    (59, 61, 59, "Where are the speakers most likely working?", "A", [
        ("A", "At a public garden / botanical park"), ("B", "At a floristry shop"), ("C", "At a fruit orchard"), ("D", "At a construction supply company")
    ], 'Man: "I just spoke to the garden director. He wants us to install an irrigation system in the rose garden as well as the magnolia grove."'),
    (59, 61, 60, "What have the speakers been asked to do?", "B", [
        ("A", "Prune magnolia trees"), ("B", "Install an irrigation system"), ("C", "Test soil quality"), ("D", "Harvest cherry fruit")
    ], 'Man: "He wants us to install an irrigation system in the rose garden as well as the magnolia grove."'),
    (59, 61, 61, "What does the man offer to do?", "A", [
        ("A", "Check leftover supplies"), ("B", "Order extra pipes"), ("C", "Take garden measurements"), ("D", "Contact the garden director")
    ], 'Man: "We have some extra parts left over from when we worked on the cherry trees. I’ll check what we have left..."'),

    # Q62-64
    (62, 64, 62, "Why does the man apologize?", "B", [
        ("A", "He lost a client contract"), ("B", "He arrived late for work"), ("C", "He damaged a car battery"), ("D", "He forgot an invoice")
    ], 'Man: "Good morning, Ms. Al-Johani. Sorry I’m a little late, traffic was terrible."'),
    (62, 64, 63, "According to the woman, why will the speakers be very busy today?", "A", [
        ("A", "Many convention attendees reserved rental cars"), ("B", "The rental fleet is undergoing inspection"), ("C", "A computer outage occurred"), ("D", "The office is understaffed")
    ], 'Woman: "...big education convention in town starting today, and a lot of attendees from out of town have reserved cars..."'),
    (62, 64, 64, "Look at the graphic. Where will the man go first?", "C", [
        ("A", "Gasoline vehicle parking"), ("B", "Car wash station"), ("C", "Electric cars section"), ("D", "Front customer counter")
    ], 'Woman: "I’d like you to start by checking the batteries in our electric cars."'),

    # Q65-67
    (65, 67, 65, "Where do the speakers most likely work?", "A", [
        ("A", "A city parks department"), ("B", "An art institute"), ("C", "A residential building developer"), ("D", "A municipal library")
    ], 'Woman: "Well, all our public programs and community events are on schedule." - Man: "...Janice Park project? We’re still planning on planting trees..."'),
    (65, 67, 66, "What does the woman say will take place next month?", "B", [
        ("A", "A tree-planting ceremony"), ("B", "A children’s poster competition"), ("C", "A mayoral election"), ("D", "A neighborhood parade")
    ], 'Woman: "There’ll be a children’s poster competition next month, which the city mayor will judge."'),
    (65, 67, 67, "Look at the graphic. What kind of seedlings will be given away?", "A", [
        ("A", "The tallest tree variety"), ("B", "The most fragrant variety"), ("C", "The fastest growing variety"), ("D", "The shade-providing variety")
    ], 'Woman: "We’ll be giving away the tallest of these four varieties, since it was the most popular in a survey of our residents."'),

    # Q68-70
    (68, 70, 68, "Where does the conversation most likely take place?", "A", [
        ("A", "At a cafe"), ("B", "At a supermarket bakery"), ("C", "In a corporate cafeteria"), ("D", "At a hotel lounge")
    ], 'Man: "Hi, I’d like a large black coffee and an egg and cheese croissant, please."'),
    (68, 70, 69, "Look at the graphic. How much will the man save on his purchase?", "B", [
        ("A", "5%"), ("B", "10% / Chiết khấu theo thẻ Easy Cash"), ("C", "15%"), ("D", "20%")
    ], 'Woman: "...Are you a Shelby’s preferred customer?" - Man: "Uh, no, I’m not, but I do have an Easy Cash card."'),
    (68, 70, 70, "What does the man say he will do later today?", "B", [
        ("A", "Pick up a pastry order"), ("B", "Call to place a breakfast order"), ("C", "Apply for a membership card"), ("D", "Meet with his team")
    ], 'Man: "No, I’ll call you later today when I know what everyone wants. Thanks for the information!"')
]

for s, e, q_num, q_txt, ans, opts, trans in p3_data:
    front = f'Part 3 - Câu {q_num}<br><br>[sound:test2_part3_c{s}_{e}.mp3]<br><b>Question {q_num}: {q_txt}</b><br><br><div class="mc-container" data-ans="{ans}">'
    for l, txt in opts:
        front += f'<button class="mc-btn" onclick="checkMC(this, \'{l}\')">({l}) {txt}</button>'
    front += f'</div>'
    
    correct_text = [t for l, t in opts if l == ans][0]
    back = f'<b>Đáp án đúng: ({ans}) {correct_text}</b><br><br><i>Transcript trích đoạn:</i> {trans}'
    cards.append(f"{front}\t{back}")

# Write complete deck
header = "#separator:tab\n#html:true\n#tags:TOEIC_Listening_Test2\n\n"
content = header + "\n".join(cards) + "\n"

out_filename = "TOEIC_Listening_Test2_Audio_Interactive.txt"
with open(out_filename, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\n[+] ĐÃ HOÀN THÀNH TẠO TOÀN BỘ 70 CÂU TEST 2: {out_filename}")
