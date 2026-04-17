# DOMOVIE — Frontend Integration Guide

## Base URL

Local dev:
```
http://localhost:8000/api
```

Production (Render):
```
https://your-app.onrender.com/api
```

ตั้งค่า API_BASE ใน JS แต่ละไฟล์:
```js
const API_BASE = 'http://localhost:8000/api';
```

---

## Authentication — JWT Token

### Login

```js
// POST /api/auth/login/
const res = await fetch(`${API_BASE}/auth/login/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'admin', password: 'admin1234' }),
});
const data = await res.json();
// data = { access, refresh, username, is_staff }

localStorage.setItem('access_token', data.access);
localStorage.setItem('refresh_token', data.refresh);
localStorage.setItem('username', data.username);
localStorage.setItem('is_staff', data.is_staff);
```

### ส่ง Token ใน Header (ทุก request ที่ต้องการ auth)

```js
const token = localStorage.getItem('access_token');

const res = await fetch(`${API_BASE}/movies/`, {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
});
```

### Logout

```js
// POST /api/auth/logout/
await fetch(`${API_BASE}/auth/logout/`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ refresh: localStorage.getItem('refresh_token') }),
});
localStorage.clear();
window.location.href = 'login.html';
```

### ดึงข้อมูล User ปัจจุบัน

```js
// GET /api/auth/me/
const res = await fetch(`${API_BASE}/auth/me/`, {
  headers: { 'Authorization': `Bearer ${token}` },
});
const user = await res.json();
// user = { id, username, email, is_staff }
```

### Register

```js
// POST /api/auth/register/
const res = await fetch(`${API_BASE}/auth/register/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, email, password }),
});
```

---

## Movies API

### ดึงรายการหนังทั้งหมด

```js
// GET /api/movies/
const res = await fetch(`${API_BASE}/movies/`);
const movies = await res.json();
// movies = [{ id, title, synopsis, release_year, genre, poster_image, director, director_name, created_at }, ...]
```

### ดึงหนังรายชิ้น

```js
// GET /api/movies/<id>/
const res = await fetch(`${API_BASE}/movies/1/`);
const movie = await res.json();
```

### เพิ่มหนัง (Admin only)

```js
// POST /api/movies/  — ใช้ FormData เพราะมีรูป
const formData = new FormData();
formData.append('title', 'Inception');
formData.append('synopsis', 'ความฝันซ้อนความฝัน...');
formData.append('release_year', 2010);
formData.append('genre', 'scifi');           // 'scifi' หรือ 'horror'
formData.append('director', 1);              // director id
formData.append('poster_image', fileInput.files[0]);  // optional

const res = await fetch(`${API_BASE}/movies/`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData,
});
```

### แก้ไขหนัง (Admin only)

```js
// PUT /api/movies/<id>/
const formData = new FormData();
formData.append('title', 'Inception Updated');
// ... ใส่ field ที่ต้องการแก้

const res = await fetch(`${API_BASE}/movies/1/`, {
  method: 'PUT',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData,
});
```

### ลบหนัง (Admin only)

```js
// DELETE /api/movies/<id>/
await fetch(`${API_BASE}/movies/1/`, {
  method: 'DELETE',
  headers: { 'Authorization': `Bearer ${token}` },
});
```

---

## Directors API

รูปแบบเดียวกับ Movies ทุกอย่าง เปลี่ยน endpoint เป็น `/api/directors/`

```js
// Fields: name, bio, nationality, birth_year, profile_image
const res = await fetch(`${API_BASE}/directors/`);
const directors = await res.json();
```

---

## Products API

```js
// GET /api/products/
const res = await fetch(`${API_BASE}/products/`);
const products = await res.json();
// products = [{ id, name, description, price, image, stock, created_at }, ...]
```

เพิ่มสินค้า (Admin only) — ใช้ FormData เหมือน movies:
```js
// POST /api/products/
const formData = new FormData();
formData.append('name', 'Inception Blu-ray');
formData.append('description', '...');
formData.append('price', '300.00');
formData.append('stock', 10);
formData.append('image', fileInput.files[0]);  // optional

const res = await fetch(`${API_BASE}/products/`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData,
});
```

---

## Reviews API

### ดึงรีวิวทั้งหมด (Public)

```js
// GET /api/reviews/
const res = await fetch(`${API_BASE}/reviews/`);
const reviews = await res.json();
// reviews = [{ id, movie_title, content, author, author_username, created_at }, ...]
```

### โพสต์รีวิว (ต้อง login)

```js
// POST /api/reviews/
const res = await fetch(`${API_BASE}/reviews/`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    movie_title: 'Inception',
    content: 'หนังดีมากๆ...',
  }),
});
```

---

## Cloudinary Image URLs

เมื่อ backend ใช้ Cloudinary (ตั้งค่า `CLOUDINARY_URL` ใน env) ค่า `poster_image`, `profile_image`, `image` ใน response จะเป็น Cloudinary URL เต็ม เช่น:

```
https://res.cloudinary.com/your-cloud/image/upload/v123/movies/inception.jpg
```

ใช้ใน HTML ได้เลย:
```js
img.src = movie.poster_image;  // Cloudinary URL โดยตรง
```

สำหรับ local dev จะเป็น:
```
http://localhost:8000/media/movies/inception.jpg
```

---

## ตัวอย่างแบบ Complete — หน้า Movie List

```html
<div id="movie-grid"></div>

<script>
const API_BASE = 'http://localhost:8000/api';

async function loadMovies(genre = null) {
  let url = `${API_BASE}/movies/`;
  const res = await fetch(url);
  const movies = await res.json();

  const filtered = genre ? movies.filter(m => m.genre === genre) : movies;

  document.getElementById('movie-grid').innerHTML = filtered.map(m => `
    <div class="movie-card">
      <img src="${m.poster_image || 'placeholder.jpg'}" alt="${m.title}">
      <h3>${m.title}</h3>
      <p>${m.synopsis}</p>
      <span>${m.release_year} · ${m.director_name}</span>
    </div>
  `).join('');
}

loadMovies('scifi');  // หรือ 'horror'
</script>
```

---

## Permission Summary

| Endpoint | GET | POST | PUT/DELETE |
|----------|-----|------|-----------|
| /api/movies/ | ✅ ทุกคน | 🔒 Admin | 🔒 Admin |
| /api/directors/ | ✅ ทุกคน | 🔒 Admin | 🔒 Admin |
| /api/products/ | ✅ ทุกคน | 🔒 Admin | 🔒 Admin |
| /api/reviews/ | ✅ ทุกคน | 🔑 Login | — |
| /api/auth/me/ | 🔑 Login | — | — |
| /api/auth/logout/ | — | 🔑 Login | — |
