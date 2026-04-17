# DO MOVIE — Frontend Redesign Design Spec
Date: 2026-04-17

## Overview

Redesign all frontend pages of the DO MOVIE website. The entry point changes from `pages/index.html` to `pages/main.html`. All pages keep the existing color palette but get improved layout, typography, and consistent navigation.

---

## Color Palette (Unchanged)

| Token | Value | Usage |
|-------|-------|-------|
| `--dark` | `#2B1F14` | Navbar, dark sections, footer |
| `--dark-card` | `#3A2A1A` | Cards, panels |
| `--cream` | `#F5EFE6` | Light section backgrounds |
| `--gold` | `#F2C94C` | Accent, CTAs, active nav |
| `--white-warm` | `#FFF8E7` | Body text on dark bg |
| `--red-soft` | `#ff6b6b` | Errors, logout |
| `--orange` | `#F2994A` | Prices |

## Typography

- **Logo / Section titles**: `Cinzel` (Google Fonts) — cinematic feel
- **Thai body text**: `Sarabun` (Google Fonts) — readable Thai
- **Fallback**: `serif` / `sans-serif`

---

## Entry Point Change

**Problem**: Currently `pages/index.html` is the home page but the user wants `pages/main.html` to be the first page seen.

**Solution**:
1. Create `index.html` at the project root with an immediate redirect to `pages/main.html`
2. Update `pages/index.html` to redirect to `pages/main.html` (backward compatibility)
3. All "หน้าหลัก" nav links point to `main.html`

---

## Navigation (All Pages — Identical)

```
DO MOVIE | หน้าหลัก | หมวดหมู่▾ | DVD | ของที่ระลึก | กระดานรีวิว | ผู้กำกับ | [เข้าสู่ระบบ / username(ออก)]
```

- **หมวดหมู่** has a dropdown with: Sci-Fi → `Scifi_movie.html`, Horror → `Horor_movie.html`
- When logged in: show `username (ออก)` instead of `เข้าสู่ระบบ`; if `is_staff=true`, also show `Admin Panel`
- Active page link highlighted in `#F2C94C`

---

## Pages

### 1. `pages/main.html` — Homepage (NEW)

**Layout**: Editorial/Magazine style on dark background

**Sections (top → bottom)**:
1. **Navbar** (standard)
2. **Featured Movie Hero** — large horizontal card: poster left, title + genre badge + synopsis + CTA button right. Data from `GET /api/movies/` first result
3. **แนวหนัง** — 2 genre cards side by side: Sci-Fi (blue gradient) and Horror (red gradient), each with icon + description + "ดูทั้งหมด" button
4. **สำรวจเพิ่มเติม** — 3 shortcut cards: 💿 DVD / 🛍️ ของที่ระลึก / 📝 กระดานรีวิว
5. **Footer** (standard: ข่าวหนัง + เกี่ยวกับเรา + ติดตามเรา)

### 2. `pages/Scifi_movie.html` — Sci-Fi Movies

**Layout**:
1. Navbar
2. Hero banner — dark blue gradient, "🚀 หนัง Sci-Fi" title + subtitle
3. Movie card grid — poster (2:3 ratio) + title + year + director name. Click → `movie-detail.html?id=`
4. Empty state if no movies

### 3. `pages/Horor_movie.html` — Horror Movies

Same structure as Scifi but with dark red gradient banner.

### 4. `pages/movie-detail.html` — Movie Detail

**Sections**:
1. Navbar
2. **Detail Hero** — cream bg: poster left + title, genre badge, year badge, synopsis, director name right
3. **Director Bio** — dark bg: circular photo left + name, nationality/birth year, bio, link to director-detail
4. **More by Director** — cream bg: horizontal scroll/grid of other movies by same director (hidden if none)
5. Footer (simple copyright line)

### 5. `pages/DVD_INCEPTION.html` — DVD Catalog

**Layout**:
1. Navbar
2. Section header "รายการแผ่นหนัง (DVD)" + "คำสั่งซื้อ →" link
3. DVD grid — poster + title + synopsis excerpt + year + "ดูรายละเอียด" button. Data from `GET /api/movies/`
4. Footer (standard)

### 6. `pages/Item_forsale.html` — Merchandise Store

**Layout**:
1. Navbar
2. Section header "ของที่ระลึก" + subtitle
3. Product grid — image (2:3) + name + description + price + stock. Data from `GET /api/products/`
4. Footer (standard)

### 7. `pages/list_order.html` — Order List

**Layout**:
1. Navbar
2. "คำสั่งซื้อสินค้า" title
3. Styled table: No. / ชื่อสินค้า / ราคา / Stock / ปุ่มสั่งซื้อ
4. Cart summary panel: จำนวน + ราคารวม + ปุ่มชำระเงิน (10% discount if >3 items, +7% VAT)

### 8. `pages/data_board.html` — Review Board

**Layout**:
1. Navbar
2. Board header "กระดานรีวิวภาพยนตร์" + subtitle
3. **If logged in**: Review form (ชื่อหนัง + textarea + submit)
4. **If not logged in**: Login prompt banner
5. Reviews grid — card per review: movie title + date + content + author
6. No footer (page is self-contained)

### 9. `pages/directors.html` — Directors

**Layout**:
1. Navbar
2. Section header "ผู้กำกับ"
3. Director grid — circular photo + name + nationality + birth year. Click → `director-detail.html?id=`
4. Footer (simple copyright)

### 10. `pages/director-detail.html` — Director Detail

**Layout**:
1. Navbar
2. Profile hero — large circular photo + name + nationality + birth year + full bio
3. "ผลงานภาพยนตร์" — movie poster grid filtered by this director
4. Footer (simple copyright)

### 11. `pages/login.html` — Login

**Layout**: Full-page centered, dark bg with subtle grain texture
- Back arrow (→ main.html)
- Card: "เข้าสู่ระบบ" title + Username + Password + submit + link to register
- After login: redirect to `main.html` (not `index.html`)

### 12. `pages/regist.html` — Register

Same layout as login.
- Card: "สมัครสมาชิก" title + Username + Email + Password + Confirm + submit + link to login
- After success: redirect to `login.html`

---

## Shared Components

### Standard Footer
```
[ข่าวสารหนังใหม่]  [เกี่ยวกับเรา]  [ติดตามเรา]
© 2026 Web DoMovie. All rights reserved.
```
Used on: main.html, DVD_INCEPTION.html, Item_forsale.html

### Simple Footer (copyright only)
Used on: movie-detail.html, directors.html, director-detail.html

### Fade-in Animation
All content uses `.fade` / `.fade.show` pattern (IntersectionObserver or scroll listener via `main.js`)

---

## CSS Strategy

Each page keeps its own CSS file. Common patterns (nav, footer, fade, container) will be duplicated for simplicity — no shared CSS refactor in this pass.

New pages that currently use inline `<style>` blocks will have styles consolidated into the inline block (no new CSS files needed).

---

## JS Changes

- `login.html`: change `window.location.href = 'index.html'` → `'main.html'`
- All nav "หน้าหลัก" links → `../pages/main.html` (or `main.html` for same-dir files)

---

## File Changes Summary

| File | Action |
|------|--------|
| `index.html` (root) | **CREATE** — redirect to `pages/main.html` |
| `pages/index.html` | **UPDATE** — redirect to `main.html` |
| `pages/main.html` | **REWRITE** — full homepage |
| `pages/Scifi_movie.html` | **REDESIGN** |
| `pages/Horor_movie.html` | **REDESIGN** |
| `pages/movie-detail.html` | **REDESIGN** |
| `pages/DVD_INCEPTION.html` | **REDESIGN** |
| `pages/Item_forsale.html` | **REDESIGN** |
| `pages/list_order.html` | **REDESIGN** |
| `pages/data_board.html` | **REDESIGN** |
| `pages/directors.html` | **REDESIGN** |
| `pages/director-detail.html` | **REDESIGN** |
| `pages/login.html` | **REDESIGN** |
| `pages/regist.html` | **REDESIGN** |
| `css/main.css` | **UPDATE** — homepage styles |
| `css/index.css` | **UPDATE** — shared nav/footer styles |
| `css/Scifi_movie.css` | **UPDATE** |
| `css/Horro_movie.css` | **UPDATE** |
| `css/data_board.css` | **UPDATE** |
| `css/regist.css` | **UPDATE** — login + register shared |
