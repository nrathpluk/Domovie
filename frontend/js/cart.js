// ฟังก์ชันดึงข้อมูลตะกร้าจาก localStorage
function getCart() {
    const raw = localStorage.getItem('cart'); // อ่านข้อมูล cart ที่เก็บเป็น JSON string
    return raw ? JSON.parse(raw) : []; // ถ้ามีข้อมูล → แปลงเป็น array; ถ้าไม่มี → คืน array ว่าง
}

// ฟังก์ชันบันทึก cart ลง localStorage
function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart)); // แปลง array เป็น JSON string แล้วบันทึก
}

// ฟังก์ชันเพิ่ม DVD ลงตะกร้า
function addToCart(dvdId, quantity) {
    if (quantity === undefined) quantity = 1; // ถ้าไม่ระบุ quantity → ใช้ค่าเริ่มต้น 1
    const cart = getCart(); // โหลด cart ปัจจุบัน
    const existing = cart.find(function(item) { return item.dvd === dvdId; }); // หาว่า DVD นี้มีในตะกร้าแล้วหรือยัง
    if (existing) { // ถ้ามีอยู่แล้ว
        existing.quantity += quantity; // เพิ่ม quantity เข้าไป
    } else { // ถ้ายังไม่มี
        cart.push({ dvd: dvdId, quantity: quantity }); // เพิ่ม item ใหม่เข้า array
    }
    saveCart(cart); // บันทึก cart ที่อัปเดตแล้ว
}

// ฟังก์ชันลบ DVD ออกจากตะกร้า
function removeFromCart(dvdId) {
    saveCart(getCart().filter(function(item) { return item.dvd !== dvdId; })); // กรองเอา DVD ที่ต้องการออก แล้วบันทึก
}

// ฟังก์ชันอัปเดตจำนวนของ DVD ในตะกร้า
function updateCartQuantity(dvdId, quantity) {
    if (quantity <= 0) { // ถ้าจำนวนน้อยกว่าหรือเท่ากับ 0
        removeFromCart(dvdId); // ลบออกจากตะกร้าแทน
        return; // หยุดทำงาน
    }
    const cart = getCart(); // โหลด cart ปัจจุบัน
    const item = cart.find(function(i) { return i.dvd === dvdId; }); // หา item ที่ตรงกับ dvdId
    if (item) { // ถ้าเจอ item
        item.quantity = quantity; // อัปเดต quantity
        saveCart(cart); // บันทึก
    }
}

// ฟังก์ชันล้างตะกร้าทั้งหมด
function clearCart() {
    localStorage.removeItem('cart'); // ลบข้อมูล cart ออกจาก localStorage ทั้งหมด
}

// ฟังก์ชันนับจำนวน DVD รวมทั้งหมดในตะกร้า
function getCartCount() {
    return getCart().reduce(function(total, item) { return total + item.quantity; }, 0); // รวม quantity ทุก item เริ่มจาก 0
}
