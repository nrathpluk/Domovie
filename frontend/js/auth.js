// ฟังก์ชันดึงข้อมูล user ปัจจุบันจาก localStorage
function getCurrentUser() {
    const data = localStorage.getItem('user'); // อ่านข้อมูล user ที่เก็บไว้ใน localStorage
    return data ? JSON.parse(data) : null; // ถ้ามีข้อมูล → แปลง JSON string กลับเป็น object; ถ้าไม่มี → คืน null
}

// ฟังก์ชันตรวจสอบว่า user login อยู่หรือไม่
function isLoggedIn() {
    return !!localStorage.getItem('access_token'); // !! แปลงค่าเป็น boolean: มี token = true, ไม่มี = false
}

// ฟังก์ชันบันทึก token และข้อมูล user หลัง login สำเร็จ
function setAuth(data) {
    localStorage.setItem('access_token', data.access); // บันทึก JWT access token ลง localStorage
    localStorage.setItem('user', JSON.stringify(data.user)); // แปลง user object เป็น JSON string แล้วบันทึก
}

// ฟังก์ชัน logout ออกจากระบบ
function logout() {
    localStorage.removeItem('access_token'); // ลบ token ออกจาก localStorage
    localStorage.removeItem('user'); // ลบข้อมูล user ออกจาก localStorage
    window.location.href = '/login.html'; // redirect ไปหน้า login
}

// ฟังก์ชัน guard สำหรับหน้าที่ต้องการ authentication
function requireAuth() {
    if (!isLoggedIn()) { // ถ้ายังไม่ได้ login
        window.location.href = '/login.html'; // บังคับ redirect ไปหน้า login
    }
}
