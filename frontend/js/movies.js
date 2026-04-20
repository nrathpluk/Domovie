var currentPage = 1; // ตัวแปร global เก็บหน้าปัจจุบันที่กำลังแสดงอยู่
var currentSearch = ''; // ตัวแปร global เก็บคำค้นหาปัจจุบัน (ว่างเปล่า = ไม่ได้ค้นหา)


// ฟังก์ชัน async โหลดและแสดงรายการหนัง
async function loadMovies(page, search) {
    var grid = document.getElementById('movies-grid'); // หา element grid สำหรับแสดง movie cards
    var pager = document.getElementById('pagination'); // หา element สำหรับแสดง pagination buttons
    grid.innerHTML = '<div class="loading">Loading movies…</div>'; // แสดง loading indicator ก่อนดึงข้อมูล

    var url = '/movies/?page=' + page; // สร้าง URL พื้นฐานสำหรับเรียก API หน้าที่ต้องการ
    if (search) url += '&search=' + encodeURIComponent(search); // ถ้ามีคำค้นหา → เพิ่ม query string (encode เพื่อความปลอดภัย)

    var res = await apiFetch(url); // เรียก API ดึงรายการหนัง
    if (!res) return; // ถ้าได้รับ null (กรณี 401) → หยุดทำงาน
    var data = await res.json(); // แปลง response เป็น JavaScript object

    if (!data.results || !data.results.length) { // ถ้าไม่มีผลลัพธ์
        grid.innerHTML = '<div class="empty-state"><p>No movies found.</p></div>'; // แสดง empty state
        pager.innerHTML = ''; // ล้าง pagination
        return; // หยุดทำงาน
    }

    grid.innerHTML = data.results.map(function(m, i) { // วน loop สร้าง HTML card แต่ละหนัง
        var idx = String(i + 1).padStart(2, '0'); // สร้างเลข index เช่น "01", "02" สำหรับ card-frame
        var year = m.release_date ? m.release_date.slice(0, 4) : ''; // ดึงปี 4 หลักจาก release_date หรือ string ว่าง
        var meta = [m.director_name || 'Unknown', year].filter(Boolean).join(' \u2022 '); // รวมชื่อผู้กำกับและปีด้วย bullet (•), filter ออกค่าว่าง
        return '<a class="card" href="movie-detail.html?id=' + m.id + '" data-id="' + m.id + '">' + // เปิด card เป็น link ไปหน้า detail
            '<span class="card-frame">' + idx + '</span>' + // ป้ายเลข frame มุมบนซ้ายของ card
            (m.poster_url // ตรวจว่ามี poster URL หรือไม่
                ? '<img src="' + m.poster_url + '" alt="' + m.title + '" loading="lazy">' // มี → แสดงรูปพร้อม lazy loading
                : '<div class="card-img-placeholder">NO FILM</div>') + // ไม่มี → แสดง placeholder
            '<div class="card-body">' + // เปิด panel ข้อมูลด้านล่าง card (ซ่อนจนกว่าจะ hover)
            '<div class="card-title">' + m.title + '</div>' + // ชื่อหนัง
            '<div class="card-meta">' + meta + '</div>' + // ชื่อผู้กำกับ + ปี
            '</div></a>'; // ปิด card-body และ card link
    }).join(''); // รวม HTML ทุก card เป็น string เดียว

    renderPagination(data.count, page, pager); // สร้าง pagination โดยส่งจำนวนทั้งหมด, หน้าปัจจุบัน, container
}

// ฟังก์ชันสร้าง pagination buttons
function renderPagination(total, page, container) {
    var pages = Math.ceil(total / 10); // คำนวณจำนวนหน้าทั้งหมด (10 items ต่อหน้า, ปัดขึ้น)
    if (pages <= 1) { container.innerHTML = ''; return; } // ถ้ามีหน้าเดียว → ซ่อน pagination และหยุดทำงาน

    var btns = []; // array สำหรับเก็บ HTML ของ pagination buttons
    if (page > 1) btns.push('<button onclick="go(' + (page - 1) + ')">‹ Prev</button>'); // ถ้าไม่ใช่หน้าแรก → เพิ่มปุ่ม Prev
    for (var i = 1; i <= pages; i++) { // วน loop ทุกหน้า
        btns.push('<button class="' + (i === page ? 'active' : '') + '" onclick="go(' + i + ')">' + i + '</button>'); // สร้างปุ่มตัวเลข — หน้าปัจจุบัน ใส่ class active
    }
    if (page < pages) btns.push('<button onclick="go(' + (page + 1) + ')">Next ›</button>'); // ถ้าไม่ใช่หน้าสุดท้าย → เพิ่มปุ่ม Next
    container.innerHTML = btns.join(''); // render buttons ลง DOM
}

// ฟังก์ชันเปลี่ยนหน้า
function go(page) {
    currentPage = page; // อัปเดตหน้าปัจจุบัน
    loadMovies(page, currentSearch); // โหลดหนังหน้าใหม่พร้อมคำค้นหาที่มีอยู่
    window.scrollTo(0, 0); // เลื่อน scroll กลับขึ้นบนสุดของหน้า
}

document.addEventListener('DOMContentLoaded', function() { // ตายตัว: รันเมื่อ DOM โหลดเสร็จ
    loadMovies(1, ''); // โหลดหนังหน้าแรกโดยไม่มีคำค้นหา

    document.getElementById('search-btn').addEventListener('click', function() { // ดักจับ click ปุ่ม Search
        currentSearch = document.getElementById('search-input').value.trim(); // อ่านคำค้นหาจาก input (ตัด space ก่อน-หลัง)
        currentPage = 1; // reset กลับหน้า 1
        loadMovies(1, currentSearch); // โหลดหนังใหม่ด้วยคำค้นหา
    });

    document.getElementById('search-input').addEventListener('keydown', function(e) { // ดักจับ keydown ใน input
        if (e.key === 'Enter') document.getElementById('search-btn').click(); // ถ้ากด Enter → trigger click ปุ่ม Search
    });
});
