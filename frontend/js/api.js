// กำหนด URL หลักของ API โดยตรวจสอบว่ากำลังรันบน localhost หรือ production
const API_BASE = (() => { // ตายตัว: IIFE (ฟังก์ชันที่เรียกตัวเองทันที) เพื่อเลือก URL ที่เหมาะสม
    const host = window.location.hostname; // ดึงชื่อ hostname ของหน้าปัจจุบัน เช่น "localhost" หรือ "domovie.onrender.com"
    if (host === 'localhost' || host === '127.0.0.1') { // ตรวจว่าเปิดในเครื่องตัวเองหรือไม่
        return 'http://localhost:8000/api'; // ถ้าใช่ → ใช้ Django dev server
    }
    return 'https://domovie.onrender.com/api'; // ถ้าไม่ใช่ → ใช้ URL production บน Render
})(); // ตายตัว: เรียกใช้ฟังก์ชันทันที

// ฟังก์ชันแสดง toast notification ที่มุมล่างขวา
function showToast(message, type) { // รับข้อความและ type ('success', 'error', หรือ undefined)
    var container = document.querySelector('.toast-container'); // หา toast container ที่มีอยู่แล้วในหน้า
    if (!container) { // ถ้ายังไม่มี container
        container = document.createElement('div'); // สร้าง div ใหม่
        container.className = 'toast-container'; // ใส่ class สำหรับ CSS positioning
        document.body.appendChild(container); // แนบ container ที่ท้าย body
    }
    var toast = document.createElement('div'); // สร้าง element toast ใหม่
    toast.className = 'toast' + (type ? ' toast-' + type : ''); // ใส่ class พื้นฐาน + class type ถ้ามี เช่น 'toast toast-success'
    toast.textContent = message; // ใส่ข้อความลงใน toast
    container.appendChild(toast); // เพิ่ม toast เข้า container
    setTimeout(function () { // รอ 3 วินาทีแล้วเริ่ม animation ออก
        toast.style.animation = 'toast-out 0.25s var(--ease) forwards'; // เล่น animation slide ออก
        setTimeout(function () { toast.remove(); }, 260); // ลบ element ออกจาก DOM หลัง animation จบ (260ms)
    }, 3000); // รอ 3000ms = 3 วินาทีก่อนเริ่มออก
}

// ฟังก์ชัน async สำหรับเรียก API ทุก endpoint พร้อม authentication header อัตโนมัติ
async function apiFetch(endpoint, options = {}) { // รับ path ของ endpoint และ options เพิ่มเติม (method, body ฯลฯ)
    const token = localStorage.getItem('access_token'); // ดึง JWT access token จาก localStorage
    const headers = { // สร้าง headers object สำหรับ request
        'Content-Type': 'application/json', // บอก server ว่าส่งข้อมูลแบบ JSON
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}), // ถ้ามี token → ใส่ Authorization header; ถ้าไม่มี → ไม่ใส่
        ...options.headers, // merge กับ headers เพิ่มเติมที่ส่งมา
    };

    try { // ตายตัว: เริ่ม try-catch สำหรับ network error
        const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers }); // ตายตัว: เรียก fetch จริง โดย merge options กับ headers ที่สร้าง

        if (response.status === 401) { // ถ้าได้รับ HTTP 401 (Unauthorized = token หมดอายุหรือไม่ถูกต้อง)
            localStorage.removeItem('access_token'); // ลบ token ที่ไม่ถูกต้องออก
            localStorage.removeItem('user'); // ลบข้อมูล user ออก
            window.location.href = '/login.html'; // redirect ไปหน้า login ทันที
            return null; // คืน null เพื่อหยุดการทำงานต่อ
        }

        return response; // คืน response object กลับไปให้ผู้เรียกใช้
    } catch (err) { // ถ้าเกิด network error เช่น ไม่มีอินเทอร์เน็ต
        console.error('Network error:', err); // log error ลง console
        throw err; // โยน error ต่อไปให้ผู้เรียกใช้จัดการ
    }
}
