# DOMOVIE — Progress Tracker

## Features Checklist

### Backend Setup
- [x] Django project scaffolded (`backend/domovie/`)
- [x] `movies` app created
- [x] `accounts` app created
- [x] `store` app created
- [x] `settings.py` configured (env vars: SECRET_KEY, DEBUG, DATABASE_URL, CLOUDINARY_URL, CORS)
- [x] `requirements.txt` updated (DRF, simplejwt, cloudinary, cors, dj-database-url, dotenv)

### Models
- [x] `Director` model (name, bio, nationality, birth_year, profile_image)
- [x] `Movie` model (title, synopsis, release_year, genre, poster_image, director FK, created_at)
- [x] `Review` model (movie_title, content, author FK, created_at)
- [x] `Product` model (name, description, price, image, stock, created_at)
- [x] Migrations run

### Static Files
- [x] CSS copied to `movies/static/movies/css/`
- [x] JS (main.js) copied to `movies/static/movies/js/`
- [x] Images copied to `movies/static/movies/images/`

### Templates (Django)
- [x] `base.html` with nav (auth-aware: login/logout/admin links)
- [x] `movies/index.html` — หน้าหลัก (featured movie + director from DB)
- [x] `movies/genre_list.html` — หมวดหมู่ (Netflix-zoom)
- [x] `movies/movie_list.html` — รายการหนังตาม genre
- [x] `movies/movie_detail.html` — รายละเอียดหนัง
- [x] `movies/data_board.html` — กระดานรีวิว (Django session auth)
- [x] `movies/dvd_list.html` — รายการ DVD (static UI)
- [x] `movies/list_order.html` — คำสั่งซื้อ (static UI)
- [x] `movies/items_forsale.html` — ของที่ระลึก (static UI)
- [x] `accounts/login.html`
- [x] `accounts/register.html`
- [x] `admin_panel/base_admin.html`
- [x] `admin_panel/movies_list.html`
- [x] `admin_panel/movies_form.html`
- [x] `admin_panel/movies_delete.html`
- [x] `admin_panel/directors_list.html`
- [x] `admin_panel/directors_form.html`
- [x] `admin_panel/directors_delete.html`
- [x] `admin_panel/login.html` — login form สำหรับ admin
- [x] `admin_panel/dashboard.html` — stats + recent movies/products
- [x] `admin_panel/products_list.html`
- [x] `admin_panel/products_form.html`
- [x] `admin_panel/products_delete.html`
- [x] `admin_panel/base_admin.html` — อัปเดต sidebar (Dashboard, Movies, Directors, Products, Logout)

### Views & URLs
- [x] `movies/urls.py` — public routes
- [x] `movies/admin_urls.py` — admin panel routes (login, dashboard, movies, directors, products)
- [x] `movies/admin_views.py` — เพิ่ม admin_login, dashboard, products CRUD
- [x] `store/forms.py` — ProductForm
- [x] `accounts/urls.py` — login/logout/register + api_urlpatterns
- [x] `domovie/urls.py` — root URL config

### Auth
- [x] Session-based login/logout
- [x] Register (UserCreationForm)
- [x] Admin = `is_staff=True`, protected by `@staff_member_required`

### Seed Data
- [x] `python manage.py seed_data`
- [x] 5 directors seeded
- [x] 10 movies seeded (with poster images)
- [x] admin / admin1234
- [x] user / user1234

### DRF API
- [x] `movies/serializers.py` — Director, Movie, Review
- [x] `movies/api_views.py` — ListCreate + RetrieveUpdateDestroy views
- [x] `movies/api_urls.py` — /api/movies/, /api/directors/, /api/reviews/
- [x] `store/serializers.py` — Product
- [x] `store/views.py` — Product API views
- [x] `store/urls.py` — /api/products/
- [x] `accounts/serializers.py` — Register, User
- [x] `accounts/views.py` — api_login, api_logout, api_me, api_register
- [x] `domovie/urls.py` — /api/ prefix routing ครบ
- [x] JWT token blacklist enabled

### Firebase Removal
- [x] Firebase JS removed (firebase-config.js, login.js, regist.js, data_board.js, index.js ลบออกแล้ว)
- [x] Review board ใช้ Django DB แทน Firestore
- [x] login.html เปลี่ยนเป็น JWT API call
- [x] regist.html เปลี่ยนเป็น API register call
- [x] data_board.html เปลี่ยนเป็น API fetch + localStorage token
- [x] index.html ลบ Firebase script ออก ใช้ข้อมูล static แทน

### Frontend API Wiring (Static Pages → Django API)
- [x] `js/config.js` สร้างใหม่: API_BASE + getImageUrl() helper
- [x] `pages/Scifi_movie.html` — fetch /api/movies/?genre=scifi → render cards แบบ dynamic
- [x] `pages/Horor_movie.html` — fetch /api/movies/?genre=horror → render cards แบบ dynamic
- [x] `pages/index.html` — fetch featured movie + director from API, auth navbar
- [x] `pages/DVD_INCEPTION.html` — fetch /api/movies/ → render dvd-grid dynamic
- [x] `pages/Item_forsale.html` — สร้างใหม่: fetch /api/products/ → store grid
- [x] `pages/list_order.html` — fetch /api/products/ → table rows + cart + checkout คำนวณ discount+VAT
- [x] `pages/movie-detail.html` — สร้างใหม่: movie info + director bio + more movies by director
- [x] `pages/directors.html` — สร้างใหม่: director grid จาก API
- [x] `pages/director-detail.html` — สร้างใหม่: director profile + filmography
- [x] Auth navbar (localStorage: username/is_staff) ทุกหน้า
- [x] `pages/main.html` — เพิ่ม config.js + auth navbar
- [x] Frontend Redesign ครบทุกหน้า (Cinzel+Sarabun, dropdown nav, homepage ใหม่, เปลี่ยน entry point เป็น main.html)

---

## Log การเปลี่ยนแปลง

| วันที่ | สิ่งที่ทำ |
|--------|----------|
| 2026-04-17 | Scaffold Django project (movies, accounts apps), models, templates, views, URLs, seed_data, ลบ Firebase |
| 2026-04-17 | เพิ่ม store app + Product model, อัปเดต settings.py (env vars, DRF, JWT, CORS), requirements.txt, ลบ Firebase JS ออกจาก frontend ทั้งหมด |
| 2026-04-17 | สร้าง DRF API ครบ: movies, directors, products, reviews, auth (login/logout/me/register) JWT-based, seed_data เพิ่ม 4 products |
| 2026-04-17 | อัปเดต Admin Panel: sidebar ใหม่, login page, dashboard stats, products CRUD ครบ |
| 2026-04-17 | สร้าง FRONTEND_INTEGRATION.md, README.md (deploy guide), backend/.env.example |
| 2026-04-17 | Wire frontend ทั้งหมดกับ Django API: config.js, Scifi/Horror pages, index, DVD, Item_forsale, list_order, movie-detail, directors, director-detail, auth navbar ทุกหน้า |
| 2026-04-17 | Frontend Redesign ครบทุกหน้า: เพิ่ม Google Fonts (Cinzel + Sarabun), dropdown nav ใหม่, entry point เปลี่ยนเป็น pages/main.html, homepage ใหม่ (hero + genre cards + explore), redesign ทุก 12 หน้า (main, scifi, horror, movie-detail, DVD, store, order, review board, directors, director-detail, login, regist), อัปเดต CSS ทุกไฟล์ |
