# Domovie — Project Context

## โปรเจกต์นี้คืออะไร
เว็บแอปดูหนัง มี แค่admin สามารถเพิ่มเนื้อหาได้ และ user auth
Tech: Django + DRF, PostgreSQL (Neon), Cloudinary, Cloudflare Pages

## โครงสร้างโฟลเดอร์
- backend/ → Django project
- frontend/ → HTML/CSS/JS static files

## กฎการทำงาน
- ใช้ภาษาไทยในการอธิบาย
- comment โค้ดเป็นภาษาอังกฤษ
- ทุกครั้งที่แก้ไขอะไร ให้บอกด้วยว่าทำไม
- ถ้าทำถึงไหนแล้ว ทำอะไรไปแล้วเขียนจำไว้ด้วย

## PROGRESS.md — กฎสำคัญ
ไฟล์ `PROGRESS.md` ที่ root ของโปรเจกต์คือ progress tracker หลัก
**ทุกครั้งที่ทำ feature ใหม่ แก้ bug สำคัญ หรือเปลี่ยนแปลงอะไรในโปรเจกต์ ต้องอัปเดตไฟล์นี้เสมอ โดย:**
1. ติ๊ก checkbox ใน section ที่เกี่ยวข้อง (ถ้ายังไม่มีให้เพิ่มเข้าไป)
2. เพิ่มแถวใหม่ในตาราง "Log การเปลี่ยนแปลง" พร้อมวันที่และสิ่งที่ทำ
3. ย้าย item จาก TODO ไปยัง checklist ที่ทำเสร็จแล้ว (ถ้ามี)