# DOMOVIE

เว็บแอปดูหนังแนว Sci-Fi และ Horror พร้อมระบบ admin จัดการเนื้อหา

- **Frontend:** HTML/CSS/JS static — deploy บน Cloudflare Pages
- **Backend:** Django + DRF — deploy บน Render
- **Database:** PostgreSQL (Neon)
- **Storage:** Cloudinary (รูปภาพ)
- **Auth:** JWT (djangorestframework-simplejwt)

---

## โครงสร้างโปรเจกต์

```
Domovie/
├── backend/              # Django project
│   ├── domovie/          # settings, urls
│   ├── movies/           # Movie + Director + Review models + API
│   ├── store/            # Product model + API
│   ├── accounts/         # Auth (session + JWT API)
│   ├── templates/        # Django HTML templates
│   ├── media/            # Local dev image uploads (gitignored)
│   ├── requirements.txt
│   ├── .env.example
│   └── manage.py
├── pages/                # Frontend static HTML
├── css/                  # Frontend CSS
├── js/                   # Frontend JS
├── images/               # Frontend images
├── FRONTEND_INTEGRATION.md
└── README.md
```

---

## Local Dev Setup

### 1. เข้าโฟลเดอร์ backend

```bash
cd backend
```

### 2. สร้าง virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. ติดตั้ง dependencies

```bash
pip install -r requirements.txt
```

### 4. ตั้งค่า environment variables

```bash
cp .env.example .env
# แก้ไข .env ตามต้องการ (local dev ใช้ค่า default ได้เลย)
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Seed ข้อมูลตัวอย่าง

```bash
python manage.py seed_data
```

สร้าง:
- **admin** / admin1234 (is_staff=True)
- **user** / user1234 (is_staff=False)
- 5 directors, 10 movies, 4 products

### 7. Run server

```bash
python manage.py runserver
```

เปิดที่ `http://localhost:8000`

---

## URL หลัก

| URL | หน้า |
|-----|------|
| `/` | หน้าหลัก |
| `/genres/` | หมวดหมู่หนัง |
| `/genres/scifi/` | หนัง Sci-Fi |
| `/genres/horror/` | หนัง Horror |
| `/movies/<id>/` | รายละเอียดหนัง |
| `/reviews/` | กระดานรีวิว |
| `/dvd/` | รายการ DVD |
| `/login/` | เข้าสู่ระบบ (session) |
| `/admin-panel/` | Admin Dashboard |
| `/admin-panel/login/` | Admin Login |
| `/admin-panel/movies/` | จัดการหนัง |
| `/admin-panel/directors/` | จัดการผู้กำกับ |
| `/admin-panel/products/` | จัดการสินค้า |
| `/api/movies/` | Movies API |
| `/api/directors/` | Directors API |
| `/api/products/` | Products API |
| `/api/reviews/` | Reviews API |
| `/api/auth/login/` | JWT Login |
| `/api/auth/me/` | Current User |

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Production | insecure default | Django secret key |
| `DEBUG` | No | `True` | Debug mode |
| `ALLOWED_HOSTS` | Production | `localhost,127.0.0.1` | Comma-separated hosts |
| `DATABASE_URL` | Production | SQLite | Neon PostgreSQL URL |
| `CLOUDINARY_URL` | Production | local media/ | Cloudinary connection URL |
| `CORS_ALLOWED_ORIGINS` | Production | localhost | Comma-separated origins |

---

## Deploy บน Render

### 1. สร้าง Web Service เชื่อมกับ GitHub repo

### 2. ตั้งค่า Build & Deploy

| Setting | Value |
|---------|-------|
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| Start Command | `gunicorn domovie.wsgi:application` |

เพิ่ม `gunicorn` ใน requirements.txt ก่อน deploy

### 3. Environment Variables ใน Render Dashboard

```
SECRET_KEY             = <generate a strong random key>
DEBUG                  = False
DATABASE_URL           = <Neon connection string>
CLOUDINARY_URL         = <Cloudinary URL>
CORS_ALLOWED_ORIGINS   = https://your-app.pages.dev
ALLOWED_HOSTS          = your-app.onrender.com
```

---

## เชื่อมต่อ Neon PostgreSQL

1. สมัคร [neon.tech](https://neon.tech) (free tier)
2. สร้าง project → copy **Connection string**
3. ใส่ใน `DATABASE_URL`:
   ```
   postgresql://user:password@ep-xxx.neon.tech/dbname?sslmode=require
   ```

---

## เชื่อมต่อ Cloudinary

1. สมัคร [cloudinary.com](https://cloudinary.com) (free tier)
2. Dashboard → Copy **API Environment variable**
3. ใส่ใน `CLOUDINARY_URL`:
   ```
   cloudinary://api_key:api_secret@cloud_name
   ```

---

## Deploy Frontend บน Cloudflare Pages

1. เชื่อม GitHub repo กับ Cloudflare Pages
2. ตั้งค่า Root directory: `/`, Build command: ว่าง
3. แก้ `API_BASE` ในไฟล์ JS ให้ชี้ไป Render URL:
   ```js
   const API_BASE = 'https://your-app.onrender.com/api';
   ```
