#task1
def find_and_print(messages, current_station):
    main_line_stations = ["Songshan", "Nanjing Sanmin", "Taipei Arena", "Nanjing Fuxing", "Songjiang Nanjing",
                          "Zhongshan", "Beimen", "Ximen", "Xiaonanmen", "Chiang Kai-Shek Memorial Hall",
                          "Guting", "Taipower Building", "Gongguan", "Wanlong", "Jingmei", "Dapinglin",
                          "Qizhang", "Xindian City Hall", "Xindian"]

    # 另外計算“Xiaobitan”與“Qizhang”之間的距離
    xiaobitan_to_qizhang_distance = 1

    if current_station == "Xiaobitan":
       current_station = "Qizhang"
    current_index = main_line_stations.index(current_station)

   # 初始化一個基準點
    min_distance = float('inf') #無窮大
    nearest_friend = None

    for friend, message in messages.items():
        friend_station = None   # 初始化 friend_station 為 None，
        for station in main_line_stations + ["Xiaobitan"]: 
            if station.replace(" ", "") in message.replace(" ", ""): # 使用 replace(" ", "") 方法移除字符串中的空格
                friend_station = station
                break
        
        if friend_station: 
            if friend_station == "Xiaobitan":
                friend_station = "Qizhang"
                extra_distance = xiaobitan_to_qizhang_distance 
            else:
                extra_distance = 0
       
            friend_index = main_line_stations.index(friend_station)

            distance = abs(current_index - friend_index) + extra_distance

            if distance < min_distance:
                min_distance = distance
                nearest_friend = friend

    print(nearest_friend)

messages = {
    "Leslie": "I'm at home near Xiaobitan station.",
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Vivian": "I'm at Xindian station waiting for you."
}

find_and_print(messages, "Wanlong")  # print Mary
find_and_print(messages, "Songshan")  # print Copper
find_and_print(messages, "Qizhang")  # print Leslie 
find_and_print(messages, "Ximen")  # print Bob
find_and_print(messages, "Xindian City Hall")  # print Vivian


#-------------------------------------

#task2
def book(consultants, hour, duration, criteria):
    available_consultants = [c for c in consultants if is_available(c, hour, duration)]

  　# 依篩選標準
    if criteria == "price":
        chosen_consultant = min(available_consultants, key=lambda x: x['price'], default=None)
    elif criteria == "rate":
        chosen_consultant = max(available_consultants, key=lambda x: x['rate'], default=None)

    if chosen_consultant:
        print(chosen_consultant['name'])
        update_booking(chosen_consultant, hour, duration)
    else:
        print("No Service")

def is_available(consultant, start_hour, duration):
    end_hour = start_hour + duration
    return all(start_hour >= booking['end'] or end_hour <= booking['start'] for booking in consultant.get('bookings', []))

def update_booking(consultant, start_hour, duration):
    if 'bookings' not in consultant:
        consultant['bookings'] = []
    consultant['bookings'].append({'start': start_hour, 'end': start_hour + duration})

consultants=[
    {"name":"John", "rate":4.5, "price":1000},
    {"name":"Bob", "rate":3, "price":1200},
    {"name":"Jenny", "rate":3.8, "price":800}
]

book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John


#-------------------------------------

#task3
def func(*data):
    name_freq = {}
    for name in data:
        if len(name) in [2, 3]:
            middle_name = name[1]
        else:
            middle_name = name[2]
        if middle_name not in name_freq:
            name_freq[middle_name] = [name]
        else:
            name_freq[middle_name].append(name)
    
    unique_names_printed = False
    for middle_name, full_names in name_freq.items():
        if len(full_names) == 1:  
            print(full_names[0])
            unique_names_printed = True
    
    if not unique_names_printed:
        print("沒有")

func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安

#-------------------------------------

#task4
def get_number(index):
    cycles = (index) // 3
    total_increase = cycles * 7

    position_in_cycle = (index) % 3

    if position_in_cycle == 0:  # 第一個位置
        pass
    elif position_in_cycle == 1:  # 第二個位置
        total_increase += 4
    else:  # 第三個位置
        total_increase += 8

    print(total_increase)
    return total_increase
    
get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70
