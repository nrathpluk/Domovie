// ฟังก์ชัน async โหลดและแสดง orders ของ user
async function loadOrders() {
    requireAuth(); // ตรวจสอบ authentication ก่อน — ถ้าไม่ได้ login จะ redirect ไปหน้า login ทันที
    var container = document.getElementById('orders-container'); // หา container สำหรับแสดง orders

    var res = await apiFetch('/orders/'); // เรียก API GET /orders/ เพื่อดึง orders ของ user ปัจจุบัน
    if (!res) return; // ถ้า apiFetch คืน null (กรณี 401) → หยุดทำงาน
    var data = await res.json(); // แปลง response เป็น JavaScript object
    var orders = data.results || data; // รองรับทั้ง paginated response (มี .results) และ plain array

    if (!orders.length) { // ถ้าไม่มี order เลย
        container.innerHTML = // แสดง empty state พร้อมปุ่มไปหน้า DVDs
            '<div class="empty-state">' +
            '<p>No orders yet.</p>' +
            '<a href="/dvds.html" class="btn btn-primary">Browse DVDs</a>' +
            '</div>';
        return; // หยุดทำงาน ไม่ต้อง render ตาราง
    }

    container.innerHTML = // สร้าง HTML ของตาราง orders
        '<table class="table">' + // ตายตัว: เปิด table
        '<thead><tr>' + // ตายตัว: เปิด header row
        '<th>Order</th><th>Total</th><th>Status</th><th>Date</th><th>Items</th>' + // คอลัมน์ header ของตาราง
        '</tr></thead>' + // ตายตัว: ปิด header row
        '<tbody>' + // ตายตัว: เปิด body ของตาราง
        orders.map(function(order) { // วน loop แต่ละ order
            var itemsText = order.items.map(function(i) { // วน loop items ภายใน order
                return 'DVD #' + i.dvd + ' \u00d7 ' + i.quantity + ' @ $' + parseFloat(i.price).toFixed(2); // สร้างข้อความ เช่น "DVD #3 × 2 @ $12.99" (\u00d7 = ×)
            }).join(', '); // รวมทุก item ด้วย comma

            return '<tr>' + // เปิด row
                '<td>#' + order.id + '</td>' + // แสดง order id
                '<td>$' + parseFloat(order.total_price).toFixed(2) + '</td>' + // แสดงราคารวม 2 ทศนิยม
                '<td><span class="badge badge-' + order.status + '">' + order.status + '</span></td>' + // แสดง badge สถานะ — class ขึ้นอยู่กับ status เช่น badge-pending
                '<td>' + new Date(order.created_at).toLocaleDateString() + '</td>' + // แปลง ISO date เป็นวันที่แบบ locale
                '<td class="order-items">' + itemsText + '</td>' + // แสดงรายการสินค้า
                '</tr>'; // ปิด row
        }).join('') + // รวมทุก row
        '</tbody></table>'; // ตายตัว: ปิด body และ table
}

document.addEventListener('DOMContentLoaded', loadOrders); // ตายตัว: รัน loadOrders หลัง DOM โหลดเสร็จ
