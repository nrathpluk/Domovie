from django.db import models  # นำเข้า base class สำหรับสร้าง model
from django.conf import settings  # นำเข้า settings เพื่ออ้างอิง AUTH_USER_MODEL แบบ flexible


class Director(models.Model):  # model ผู้กำกับภาพยนตร์
    name = models.CharField(max_length=200)  # ชื่อผู้กำกับ บังคับกรอก
    bio = models.TextField(blank=True)  # ประวัติผู้กำกับ ไม่บังคับ
    birth_date = models.DateField(null=True, blank=True)  # วันเกิด ไม่บังคับ (null ใน DB ได้)
    image_url = models.URLField(max_length=500, blank=True, null=True)  # URL รูปภาพผู้กำกับ ไม่บังคับ

    def __str__(self):  # string representation สำหรับ admin panel
        return self.name  # แสดงชื่อผู้กำกับ


class Anime(models.Model):  # model อนิเมะ
    title = models.CharField(max_length=200)  # ชื่ออนิเมะ บังคับ
    synopsis = models.TextField(blank=True)  # เนื้อเรื่องย่อ ไม่บังคับ
    release_date = models.DateField(null=True, blank=True)  # วันฉาย ไม่บังคับ
    director = models.ForeignKey(
        Director, on_delete=models.SET_NULL, null=True, blank=True, related_name='animes'
    )  # FK ไปหา Director — ถ้าลบ Director → set null (ไม่ลบอนิเมะตาม) / related_name='animes' ให้ query director.animes.all() ได้
    poster_url = models.URLField(max_length=500, blank=True)  # URL โปสเตอร์อนิเมะ ไม่บังคับ

    def __str__(self):  # string representation
        return self.title  # แสดงชื่ออนิเมะ


class Book(models.Model):  # model หนังสือ
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='books')  # FK ไปหา Anime — ถ้าลบ Anime → ลบหนังสือด้วย (CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # ราคาหนังสือ สูงสุด 8 หลัก ทศนิยม 2 ตำแหน่ง
    stock = models.PositiveIntegerField(default=0)  # จำนวน stock เริ่มต้น 0
    cover_image = models.URLField(max_length=500, blank=True)  # URL รูปปกหนังสือ ไม่บังคับ

    def __str__(self):  # string representation
        return f"{self.anime.title} Book"  # แสดงชื่ออนิเมะ + " Book"


class Order(models.Model):  # model คำสั่งซื้อ
    STATUS_CHOICES = [  # ตัวเลือกสถานะ order
        ('pending', 'Pending'),      # รอดำเนินการ
        ('completed', 'Completed'),  # สำเร็จแล้ว
        ('cancelled', 'Cancelled'),  # ยกเลิกแล้ว
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
    )  # FK ไปหา User — ถ้าลบ User → ลบ Order ด้วย / ใช้ settings.AUTH_USER_MODEL แทน hardcode เพื่อ flexible
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ราคารวมทั้ง order (หลังหักส่วนลดแล้ว)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # สถานะ order เริ่มต้นเป็น pending
    created_at = models.DateTimeField(auto_now_add=True)  # วันเวลาสร้าง — set อัตโนมัติ ไม่แก้ได้

    def __str__(self):  # string representation
        return f"Order #{self.id} by {self.user.username}"  # แสดง id และ username ของผู้สั่ง


class OrderItem(models.Model):  # model รายการสินค้าในแต่ละ order
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')  # FK ไปหา Order — ลบ Order → ลบ items ด้วย
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)  # FK ไปหา Book — ถ้าลบหนังสือ → set null (เก็บประวัติ order ไว้)
    quantity = models.PositiveIntegerField()  # จำนวนที่สั่ง
    price = models.DecimalField(max_digits=8, decimal_places=2)  # ราคา ณ วันสั่งซื้อ (snapshot ไม่เปลี่ยนตามหนังสือ)

    def __str__(self):  # string representation
        return f"{self.quantity}x {self.book}"  # แสดงจำนวน × ชื่อหนังสือ
