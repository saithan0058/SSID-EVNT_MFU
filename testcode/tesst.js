function scheduleUserFunctions(scheduleData, callback) {
  scheduleData.forEach((item) => {
    const { username, datetime, gou} = item;
    // แปลงสตริงวันที่และเวลาเป็นรูปแบบที่ Date สามารถเข้าใจได้
    const targetDateTime = datetime.replace(" ", "T");
    const targetDateThailand = new Date(`${targetDateTime}+07:00`); // YYYY-MM-DDTHH:MM:SS+07:00

    // คำนวณเวลาที่เหลือจนถึงเวลาที่กำหนด
    const now = new Date();
    const timeUntilTarget = targetDateThailand - now;

    if (timeUntilTarget > 0) {
      setTimeout(function () {
        callback(username, targetDateThailand, gou);
      }, timeUntilTarget);
    } else {
      console.log(`เวลาที่กำหนดสำหรับ ${username} (${targetDateThailand}) ${gou} ผ่านไปแล้ว;;`);
    }
  });
}

// ตัวอย่างการใช้งานฟังก์ชัน
const scheduleData = [
  { username: "user1", gou: "g1", datetime: "2024-07-16 00:00:00" },
  { username: "user2", gou: "g1", datetime: "2024-07-16 00:39:00" },
  { username: "user3", gou: "g1", datetime: "2024-07-16 00:40:00" },
  { username: "user4", gou: "g1", datetime: "2024-07-16 00:45:00" },
  { username: "user5", gou: "g1", datetime: "2024-07-16 01:06:00" },
];

scheduleUserFunctions(scheduleData, function (username, scheduledTime,gou) {
  console.log(`ฟังก์ชันรันแล้วสำหรับ ${username}! เวลา: ${scheduledTime} ${gou}`);
});
