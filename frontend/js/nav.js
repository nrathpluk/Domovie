// ฟังก์ชันสร้างและ render navigation bar
function renderNav() {
    const nav = document.getElementById('main-nav'); // หา element nav ที่มี id="main-nav"
    if (!nav) return; // ถ้าไม่มี element นี้ → หยุดทำงาน (ป้องกัน error)

    const loggedIn = isLoggedIn(); // ตรวจสอบว่า user login อยู่หรือไม่
    const user = getCurrentUser(); // ดึงข้อมูล user ปัจจุบัน (หรือ null ถ้ายังไม่ login)
    const path = window.location.pathname; // ดึง path ของ URL ปัจจุบัน เช่น "/movies.html"

    // ฟังก์ชันช่วยตรวจว่าลิงก์นี้เป็นหน้าที่กำลังอยู่หรือไม่
    function activeClass(href) {
        return path.endsWith(href) || (href === '/index.html' && path === '/') ? ' class="active"' : ''; // ถ้าตรง → คืน class="active"; ถ้าไม่ตรง → คืน string ว่าง
    }

    // inject HTML ของ nav bar เข้า element
    nav.innerHTML = `
        <a href="/index.html" class="brand">DOMOVIE<span class="brand-dot"></span></a>
        <button class="nav-hamburger" id="nav-hamburger" aria-label="Toggle navigation" aria-expanded="false">
            <span></span><span></span><span></span>
        </button>
        <div class="nav-links" id="nav-links">
            <a href="/movies.html"${activeClass('/movies.html')}>Movies</a>
            <span class="nav-sep"></span>
            <a href="/directors.html"${activeClass('/directors.html')}>Directors</a>
            <span class="nav-sep"></span>
            <a href="/dvds.html"${activeClass('/dvds.html')}>DVDs</a>
            ${loggedIn ? `
                <span class="nav-sep"></span>
                <a href="/cart.html"${activeClass('/cart.html')}>Cart</a>
                <a href="/orders.html"${activeClass('/orders.html')}>Orders</a>
                <span class="nav-sep"></span>
                <span class="nav-username">${user.username}</span>
                <button class="nav-out" onclick="logout()">Logout</button>
            ` : `
                <span class="nav-sep"></span>
                <a href="/login.html"${activeClass('/login.html')}>Login</a>
                <a href="/register.html" class="nav-link-register${path.endsWith('/register.html') ? ' active' : ''}">Register</a>
            `}
        </div>
    `; // สร้าง HTML ของ nav ทั้งหมด — ถ้า login แล้ว: แสดง Cart/Orders/username/Logout; ถ้ายังไม่ login: แสดง Login/Register

    const hamburger = document.getElementById('nav-hamburger'); // หาปุ่ม hamburger ที่เพิ่งสร้าง
    const links = document.getElementById('nav-links'); // หา container ของลิงก์ nav
    hamburger.addEventListener('click', function () { // ดักจับ click บนปุ่ม hamburger
        const open = links.classList.toggle('open'); // toggle class 'open' บน nav-links (เปิด/ปิด menu)
        hamburger.classList.toggle('open', open); // sync class 'open' บน hamburger (เพื่อ animate เป็น X)
        hamburger.setAttribute('aria-expanded', open); // อัปเดต aria-expanded สำหรับ accessibility
    });

    links.querySelectorAll('a').forEach(function (a) { // วน loop ทุกลิงก์ใน nav
        a.addEventListener('click', function () { // ดักจับ click บนแต่ละลิงก์
            links.classList.remove('open'); // ปิด mobile menu
            hamburger.classList.remove('open'); // reset hamburger icon กลับเป็นสาม เส้น
            hamburger.setAttribute('aria-expanded', 'false'); // อัปเดต aria-expanded เป็น false
        });
    });
}

document.addEventListener('DOMContentLoaded', renderNav); // ตายตัว: รัน renderNav หลัง DOM โหลดเสร็จ
