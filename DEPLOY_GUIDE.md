# DOMOVIE — Deploy Guide (Render + Cloudflare Pages)

> ทำตามลำดับ อย่าข้าม Step

---

## สิ่งที่ต้องเตรียม

| Service | Status |
|---------|--------|
| GitHub repo (push โค้ดขึ้นก่อน) | ต้องทำก่อน |
| Render account | ✅ มีแล้ว |
| Neon PostgreSQL | ✅ มีแล้ว |
| Cloudinary account | ✅ มีแล้ว (ต้องหา api_key และ api_secret) |
| Cloudflare Pages | ต้องสมัคร / มีแล้ว |

---

## STEP 1 — Push โค้ดขึ้น GitHub

```bash
cd C:\Users\JAY\Desktop\Domovie

git add .
git commit -m "feat: add gunicorn, prepare for deploy"
git push origin main
```

> **สำคัญ:** ต้องมี repo บน GitHub ก่อน — ถ้ายังไม่มีให้สร้างที่ github.com แล้ว push ขึ้นไป

---

## STEP 2 — หา Cloudinary Credentials

1. ไปที่ [cloudinary.com](https://cloudinary.com) → Login
2. ไปที่ **Dashboard** (หน้าแรกหลัง login)
3. หาหัวข้อ **API Keys** หรือ **Product Environment Credentials**
4. copy:
   - `API Key` (ตัวเลข)
   - `API Secret` (ตัวอักษรยาวๆ)
   - `Cloud name` = `dmqgbv9kx`

แล้ว CLOUDINARY_URL จะเป็น:
```
cloudinary://YOUR_API_KEY:YOUR_API_SECRET@dmqgbv9kx
```

---

## STEP 3 — Deploy Backend บน Render

### 3.1 สร้าง Web Service

1. ไปที่ [render.com](https://render.com) → **New** → **Web Service**
2. เชื่อมกับ GitHub repo `Domovie`
3. ตั้งค่าดังนี้:

| Setting | Value |
|---------|-------|
| **Name** | `domovie-backend` (หรือชื่ออะไรก็ได้) |
| **Region** | Singapore (ใกล้ที่สุด) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| **Start Command** | `gunicorn domovie.wsgi:application` |

### 3.2 ตั้งค่า Environment Variables

คลิก **Environment** แล้วเพิ่มตัวแปรเหล่านี้ทีละตัว:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | (กด Generate หรือใช้ค่าด้านล่าง) |
| `DEBUG` | `False` |
| `DATABASE_URL` | `postgresql://neondb_owner:npg_vD5IPWjRkut3@ep-damp-unit-a1ywiavl-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require` |
| `CLOUDINARY_URL` | `cloudinary://YOUR_API_KEY:YOUR_API_SECRET@dmqgbv9kx` |
| `ALLOWED_HOSTS` | (ใส่หลัง deploy เสร็จ — จะได้ URL จาก Render) |
| `CORS_ALLOWED_ORIGINS` | (ใส่หลัง deploy Cloudflare Pages เสร็จ) |

**วิธี Generate SECRET_KEY** — รันใน terminal:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3.3 Deploy

กด **Create Web Service** → รอ build (ประมาณ 3-5 นาที)

เมื่อ deploy เสร็จ จะได้ URL เช่น:
```
https://domovie-backend.onrender.com
```

---

## STEP 4 — อัปเดต ALLOWED_HOSTS บน Render

หลังได้ URL จาก Render แล้ว:

1. กลับไปที่ Render Dashboard → Environment
2. อัปเดต `ALLOWED_HOSTS`:
   ```
   domovie-backend.onrender.com
   ```
3. กด **Save Changes** → Render จะ redeploy อัตโนมัติ

---

## STEP 5 — Seed ข้อมูลบน Render (ถ้าต้องการ)

ใน Render Dashboard → **Shell** tab:
```bash
python manage.py seed_data
```

สร้าง: admin/admin1234, user/user1234, 5 directors, 10 movies, 4 products

---

## STEP 6 — แก้ Frontend config.js

แก้ไฟล์ `js/config.js` เปลี่ยน API_BASE:

```js
// เปลี่ยนจาก:
const API_BASE = 'http://localhost:8000/api';

// เป็น:
const API_BASE = 'https://domovie-backend.onrender.com/api';
```

> แทน `domovie-backend.onrender.com` ด้วย URL จริงที่ได้จาก Render

---

## STEP 7 — Deploy Frontend บน Cloudflare Pages

1. ไปที่ [pages.cloudflare.com](https://pages.cloudflare.com) → **Create a project**
2. เชื่อมกับ GitHub repo `Domovie`
3. ตั้งค่า:

| Setting | Value |
|---------|-------|
| **Project name** | `domovie` |
| **Production branch** | `main` |
| **Framework preset** | `None` |
| **Build command** | (ว่างไว้) |
| **Build output directory** | `/` |

4. กด **Save and Deploy** → รอประมาณ 1 นาที

ได้ URL เช่น:
```
https://domovie.pages.dev
```

---

## STEP 8 — อัปเดต CORS บน Render

กลับไปที่ Render → Environment → อัปเดต:

| Key | Value |
|-----|-------|
| `CORS_ALLOWED_ORIGINS` | `https://domovie.pages.dev` |

กด Save → รอ redeploy

---

## STEP 9 — Commit และ Push การแก้ไขทั้งหมด

```bash
git add js/config.js
git commit -m "feat: update API_BASE to production Render URL"
git push origin main
```

Cloudflare Pages จะ redeploy อัตโนมัติ

---

## Checklist สรุป

- [ ] Push โค้ดขึ้น GitHub
- [ ] หา Cloudinary api_key + api_secret
- [ ] Deploy backend บน Render + ใส่ env vars
- [ ] ได้ Render URL แล้ว → อัปเดต ALLOWED_HOSTS
- [ ] Seed ข้อมูลผ่าน Render Shell
- [ ] แก้ `js/config.js` → API_BASE ใช้ Render URL จริง
- [ ] Deploy frontend บน Cloudflare Pages
- [ ] ได้ Pages URL → อัปเดต CORS_ALLOWED_ORIGINS บน Render
- [ ] Push config.js ที่แก้แล้ว → Pages redeploy

---

## ปัญหาที่พบบ่อย

| ปัญหา | วิธีแก้ |
|-------|--------|
| Build fail — `collectstatic` error | เช็ค `CLOUDINARY_URL` ว่าถูกต้อง |
| `ALLOWED_HOSTS` error | เพิ่ม Render domain ใน env var |
| CORS error บน browser | เพิ่ม Cloudflare Pages domain ใน `CORS_ALLOWED_ORIGINS` |
| รูปภาพไม่ขึ้น | เช็ค Cloudinary credentials |
| DB connection error | เช็ค `DATABASE_URL` ว่า copy ครบ |
