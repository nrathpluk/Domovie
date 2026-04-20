var currentPage = 1; // ตัวแปร global เก็บหน้าปัจจุบันที่กำลังแสดงอยู่
var currentSearch = ''; // ตัวแปร global เก็บคำค้นหาปัจจุบัน

// ฟังก์ชัน async โหลดและแสดงรายการ DVDs
async function loadDVDs(page, search) {
    var grid = document.getElementById('dvds-grid'); // หา element grid สำหรับแสดง DVD cards
    var pager = document.getElementById('pagination'); // หา element สำหรับ pagination buttons
    grid.innerHTML = '<div class="loading">Loading DVDs…</div>'; // แสดง loading indicator ก่อนดึงข้อมูล

    var url = '/dvds/?page=' + page; // สร้าง URL พื้นฐานสำหรับเรียก API
    if (search) url += '&search=' + encodeURIComponent(search); // ถ้ามีคำค้นหา → เพิ่ม query string

    var res = await apiFetch(url); // เรียก API GET /dvds/
    if (!res) return; // ถ้าได้รับ null (กรณี 401) → หยุดทำงาน
    var data = await res.json(); // แปลง response เป็น JavaScript object

    if (!data.results || !data.results.length) { // ถ้าไม่มีผลลัพธ์
        grid.innerHTML = '<div class="empty-state"><p>No DVDs found.</p></div>'; // แสดง empty state
        pager.innerHTML = ''; // ล้าง pagination
        return; // หยุดทำงาน
    }

    grid.innerHTML = data.results.map(function(dvd, i) { // วน loop สร้าง HTML card แต่ละ DVD
        var idx = String(i + 1).padStart(2, '0'); // สร้างเลข index เช่น "01", "02" สำหรับ card-frame
        var oos = dvd.stock === 0 ? '<div class="card-oos">OUT OF STOCK</div>' : ''; // ถ้า stock = 0 → เตรียม overlay "OUT OF STOCK"
        var addBtn = dvd.stock > 0 // ตรวจว่ามี stock หรือไม่
            ? '<button class="btn btn-primary btn-sm" onclick="handleAddToCart(' + dvd.id + ')">Add to Cart</button>' // มี stock → สร้างปุ่ม Add to Cart
            : ''; // ไม่มี stock → ไม่แสดงปุ่ม

        return '<div class="card">' + // เปิด card (ใช้ div ไม่ใช่ a เพราะ DVD ไม่มีหน้า detail)
            oos + // ใส่ overlay OUT OF STOCK ถ้ามี
            '<span class="card-frame">' + idx + '</span>' + // ป้ายเลข frame มุมบนซ้าย
            (dvd.cover_image // ตรวจว่ามีรูปปกหรือไม่
                ? '<img src="' + dvd.cover_image + '" alt="' + dvd.movie_title + '" loading="lazy">' // มี → แสดงรูปพร้อม lazy loading
                : '<div class="card-img-placeholder">DISC</div>') + // ไม่มี → แสดง placeholder "DISC"
            '<div class="card-body">' + // เปิด panel ข้อมูลด้านล่าง card
            '<div class="card-title">' + dvd.movie_title + '</div>' + // ชื่อหนังที่ DVD เป็นของ
            '<div class="card-price">$' + parseFloat(dvd.price).toFixed(2) + '</div>' + // ราคา DVD แสดง 2 ทศนิยม
            '<div class="card-meta">Stock: ' + dvd.stock + '</div>' + // จำนวน stock ที่เหลือ
            (addBtn ? '<div style="margin-top:0.5rem">' + addBtn + '</div>' : '') + // ถ้ามีปุ่ม → ใส่ wrapper div เพิ่ม spacing
            '</div></div>'; // ปิด card-body และ card
    }).join(''); // รวม HTML ทุก card เป็น string เดียว

    renderPagination(data.count, page, pager); // สร้าง pagination
}

// ฟังก์ชันจัดการ click ปุ่ม Add to Cart
function handleAddToCart(dvdId) {
    if (!isLoggedIn()) { // ตรวจว่า login หรือยัง
        window.location.href = '/login.html'; // ถ้ายังไม่ login → redirect ไปหน้า login ก่อน
        return; // หยุดทำงาน
    }
    addToCart(dvdId); // เพิ่ม DVD ลงตะกร้า (ใช้ฟังก์ชันจาก cart.js)
    var alertEl = document.getElementById('alert'); // หา element alert บนหน้า
    alertEl.textContent = 'Added to cart!'; // ใส่ข้อความแจ้งเตือน
    alertEl.className = 'alert alert-success'; // ตั้ง class สำหรับสไตล์สีเขียว
    alertEl.style.display = 'block'; // แสดง alert
    setTimeout(function() { alertEl.style.display = 'none'; }, 2500); // ซ่อน alert อัตโนมัติหลัง 2.5 วินาที
}

// ฟังก์ชันสร้าง pagination buttons (เหมือนใน movies.js)
function renderPagination(total, page, container) {
    var pages = Math.ceil(total / 10); // คำนวณจำนวนหน้าทั้งหมด
    if (pages <= 1) { container.innerHTML = ''; return; } // ถ้ามีหน้าเดียว → ซ่อน pagination

    var btns = []; // array สำหรับเก็บ HTML ของปุ่ม
    if (page > 1) btns.push('<button onclick="go(' + (page - 1) + ')">‹ Prev</button>'); // ปุ่ม Prev ถ้าไม่ใช่หน้าแรก
    for (var i = 1; i <= pages; i++) { // วน loop ทุกหน้า
        btns.push('<button class="' + (i === page ? 'active' : '') + '" onclick="go(' + i + ')">' + i + '</button>'); // ปุ่มตัวเลขแต่ละหน้า
    }
    if (page < pages) btns.push('<button onclick="go(' + (page + 1) + ')">Next ›</button>'); // ปุ่ม Next ถ้าไม่ใช่หน้าสุดท้าย
    container.innerHTML = btns.join(''); // render buttons ลง DOM
}

// ฟังก์ชันเปลี่ยนหน้า
function go(page) {
    currentPage = page; // อัปเดตหน้าปัจจุบัน
    loadDVDs(page, currentSearch); // โหลด DVDs หน้าใหม่
    window.scrollTo(0, 0); // เลื่อน scroll กลับขึ้นบน
}

document.addEventListener('DOMContentLoaded', function() { // ตายตัว: รันเมื่อ DOM โหลดเสร็จ
    loadDVDs(1, ''); // โหลด DVDs หน้าแรกโดยไม่มีคำค้นหา

    document.getElementById('search-btn').addEventListener('click', function() { // ดักจับ click ปุ่ม Search
        currentSearch = document.getElementById('search-input').value.trim(); // อ่านคำค้นหาจาก input
        currentPage = 1; // reset หน้ากลับเป็น 1
        loadDVDs(1, currentSearch); // โหลด DVDs ใหม่ด้วยคำค้นหา
    });

    document.getElementById('search-input').addEventListener('keydown', function(e) { // ดักจับ keydown ใน input
        if (e.key === 'Enter') document.getElementById('search-btn').click(); // กด Enter → trigger ปุ่ม Search
    });
});
