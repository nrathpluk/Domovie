# DoMovie — Deployment Steps

Stack: Django backend → Render | PostgreSQL → Render DB | Frontend → Cloudflare Pages

---

## Prerequisites

- GitHub repo pushed (done)
- Render account: https://render.com
- Cloudflare account: https://pages.cloudflare.com

---

## STEP 1 — Deploy Backend + Database on Render

1. Go to **render.com** → **New** → **Blueprint**
2. Connect your GitHub repo
3. Render reads `render.yaml` from root automatically
4. Click **Apply** — Render will create:
   - Web service: `domovie-backend`
   - PostgreSQL database: `domovie-db`

**What happens automatically (from `render.yaml`):**
```
buildCommand: pip install -r ../requirements.txt
              && python manage.py migrate
              && python manage.py collectstatic --noinput

startCommand: gunicorn domovie.wsgi:application --bind 0.0.0.0:$PORT
```

**Auto-injected env vars:**
| Key | Source |
|-----|--------|
| `SECRET_KEY` | Render generates randomly |
| `DATABASE_URL` | Render injects from `domovie-db` |
| `DEBUG` | `"False"` |
| `CORS_ALLOWED_ORIGINS` | `"https://domovie.pages.dev"` ← update after Step 2 |

---

## STEP 2 — Deploy Frontend on Cloudflare Pages

1. Go to **pages.cloudflare.com** → **Create a project** → **Connect to Git**
2. Select your GitHub repo
3. Configure build settings:

| Setting | Value |
|---------|-------|
| Framework preset | `None` |
| Build command | *(leave empty)* |
| Build output directory | `frontend` |
| Root directory | *(leave empty)* |

4. Click **Save and Deploy**
5. Note your Cloudflare URL, e.g. `https://domovie.pages.dev`

---

## STEP 3 — Update CORS with Real Cloudflare URL

After Cloudflare gives you the actual URL:

1. Go to **Render Dashboard** → `domovie-backend` → **Environment**
2. Update `CORS_ALLOWED_ORIGINS` value to your real URL:
   ```
   https://YOUR-PROJECT.pages.dev
   ```
3. Click **Save** — Render redeploys automatically

---

## STEP 4 — Update api.js with Real Render URL

If your Render service URL differs from `domovie-backend.onrender.com`:

Edit `frontend/js/api.js`:
```javascript
return 'https://YOUR-SERVICE-NAME.onrender.com/api';
```

Then:
```bash
git add frontend/js/api.js
git commit -m "fix(api): update production backend URL"
git push origin main
```

Cloudflare Pages auto-redeploys on push.

---

## STEP 5 — Create Admin User

After backend is live, go to **Render Dashboard** → `domovie-backend` → **Shell**:

```bash
python manage.py createsuperuser
```

Then manage data at: `https://domovie-backend.onrender.com/admin/`

---

## STEP 6 — Verify End-to-End

Open `https://YOUR-PROJECT.pages.dev` and test:

- [ ] Home page loads featured movies
- [ ] Click movie card → navigates to detail page
- [ ] Register new account
- [ ] Login → token stored in localStorage
- [ ] DVDs page loads
- [ ] Add to cart → cart persists on refresh
- [ ] Place order → appears in Orders page
- [ ] Directors page loads and links to director detail

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `CORS error` in browser console | `CORS_ALLOWED_ORIGINS` missing frontend URL | Update env var in Render Dashboard |
| `500` on all API calls | `SECRET_KEY` or `DATABASE_URL` not set | Check Environment tab in Render |
| Static files 404 | `collectstatic` failed | Check Render build logs |
| `relation does not exist` | Migrations didn't run | Run `python manage.py migrate` in Render Shell |
| API calls go to `localhost:8000` | `api.js` not updated | Edit `frontend/js/api.js` production URL |
| First API call takes ~30s | Render free tier spins down after 15min idle | Expected — upgrade to paid plan to avoid |
| `Module not found` on build | Missing package in `requirements.txt` | Add package, push, Render rebuilds |

---

## File Reference

| File | Purpose |
|------|---------|
| `render.yaml` | Render service + database config |
| `requirements.txt` | Python dependencies |
| `backend/domovie/settings.py` | Django config — reads all secrets from env vars |
| `frontend/js/api.js` | API base URL (localhost vs production) |
| `.gitignore` | Excludes `.env`, `venv/`, `staticfiles/` |

---

## System Flow After Deployment

```
User Browser
    │
    ├── HTML/CSS/JS ──► Cloudflare Pages (CDN, static)
    │
    └── API calls ─────► Render (Django + Gunicorn)
                              │
                              └── PostgreSQL (Render DB)
```

1. Browser loads static files from Cloudflare CDN
2. JS calls `https://domovie-backend.onrender.com/api/...`
3. Django validates JWT, queries PostgreSQL, returns JSON
4. Browser renders data
