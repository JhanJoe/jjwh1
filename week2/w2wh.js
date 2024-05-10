//task1
function findAndPrint(messages, currentStation) {
    const mainLineStations = ["Songshan", "Nanjing Sanmin", "Taipei Arena", "Nanjing Fuxing", "Songjiang Nanjing",
                              "Zhongshan", "Beimen", "Ximen", "Xiaonanmen", "Chiang Kai-Shek Memorial Hall",
                              "Guting", "Taipower Building", "Gongguan", "Wanlong", "Jingmei", "Dapinglin",
                              "Qizhang", "Xindian City Hall", "Xindian"];
    
    // 另外處理“Xiaobitan”與“Qizhang”之間的距離
    const xiaobitanToQizhangDistance = 1; 

    if (currentStation === "Xiaobitan") {
        currentStation = "Qizhang";
    }
    const currentIndex = mainLineStations.indexOf(currentStation);

    let minDistance = Infinity; // 初始化最小距離為無窮大
    let nearestFriend = null; // 初始化最近的朋友為 null

    for (const [friend, message] of Object.entries(messages)) {
        let friendStation = null;
        
        for (const station of mainLineStations.concat("Xiaobitan")) {
            if (message.replace(/\s/g, "").includes(station.replace(/\s/g, ""))) {
                friendStation = station;
                break;
            }
        }

        if (friendStation) { 
            let extraDistance = 0;
            if (friendStation === "Xiaobitan") {
                friendStation = "Qizhang";
                extraDistance = xiaobitanToQizhangDistance;
            }
            
            const friendIndex = mainLineStations.indexOf(friendStation); 
            const distance = Math.abs(currentIndex - friendIndex) + extraDistance;

            if (distance < minDistance) { 
                minDistance = distance;
                nearestFriend = friend;
            }
        }
    }

    console.log(nearestFriend); 
}

const messages = {
    "Leslie": "I'm at home near Xiaobitan station.",
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Vivian": "I'm at Xindian station waiting for you."
};

findAndPrint(messages, "Wanlong");  // print Mary
findAndPrint(messages, "Songshan");  // print Copper
findAndPrint(messages, "Qizhang");  // print Leslie
findAndPrint(messages, "Ximen");  // print Bob
findAndPrint(messages, "Xindian City Hall");  // Vivian



//task2
function book(consultants, hour, duration, criteria) {
    // 初始化可用顧問列表
    const availableConsultants = consultants.filter(consultant => isAvailable(consultant, hour, duration));

    let chosenConsultant = null; // 預設選中的顧問為 null

    if (criteria === "price") {
        chosenConsultant = availableConsultants.reduce((min, current) => 
            (min === null || current.price < min.price) ? current : min, null);
    } else if (criteria === "rate") {
        chosenConsultant = availableConsultants.reduce((max, current) => 
            (max === null || current.rate > max.rate) ? current : max, null);
    }
  
    if (chosenConsultant !== null) {
        console.log(chosenConsultant.name);  
        updateBooking(chosenConsultant, hour, duration);  
    } else {
        console.log("No Service");  
    }
}

function isAvailable(consultant, startHour, duration) {
    const endHour = startHour + duration;
    return (consultant.bookings || []).every(booking =>
        startHour >= booking.end || endHour <= booking.start);
}

function updateBooking(consultant, startHour, duration) {
    if (!consultant.bookings) {
        consultant.bookings = []; 
    }
    consultant.bookings.push({start: startHour, end: startHour + duration});  
}

const consultants = [
    {"name": "John", "rate": 4.5, "price": 1000, "bookings": []},
    {"name": "Bob", "rate": 3, "price": 1200, "bookings": []},
    {"name": "Jenny", "rate": 3.8, "price": 800, "bookings": []}
];

book(consultants, 15, 1, "price"); // Jenny
book(consultants, 11, 2, "price"); // Jenny
book(consultants, 10, 2, "price"); // John
book(consultants, 20, 2, "rate"); // John
book(consultants, 11, 1, "rate"); // Bob
book(consultants, 11, 2, "rate"); // No Service
book(consultants, 14, 3, "price"); // John


//task 3
function func(...data) {
    const nameFreq = {};
  
    data.forEach(name => {
        let middleName;

          if (name.length === 2 || name.length === 3) {
            middleName = name[1];  
        } else {
            middleName = name[2];  
        }

        // 統計中間名出現次數
        if (!nameFreq[middleName]) {
            nameFreq[middleName] = [name]; 
        } else {
            nameFreq[middleName].push(name); 
        }
    });

    let uniqueNamesPrinted = false;
    Object.entries(nameFreq).forEach(([middleName, fullNames]) => {
        if (fullNames.length === 1) {
            console.log(fullNames[0]);  
            uniqueNamesPrinted = true;  
        }
    });
  
    if (!uniqueNamesPrinted) {
        console.log("沒有");
    }
}

func("彭大牆", "陳王明雅", "吳明"); // print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); // print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆"); // print 夏曼藍波安


//task 4
function getNumber(index) {
    const cycles = Math.floor(index / 3);  
    let totalIncrease = cycles * 7;        

    const positionInCycle = index % 3;    

    if (positionInCycle === 1) {           
        totalIncrease += 4;
    } else if (positionInCycle === 2) {    
        totalIncrease += 8;
    } 

    console.log(totalIncrease);           
    return totalIncrease;
}

getNumber(1);  // print 4
getNumber(5);  // print 15
getNumber(10); // print 25
getNumber(30); // print 70
