# Complete Deployment Guide: Frontend on Vercel + Backend on Render

## Project Structure

```
electricity-theft-detection/
├── frontend/                    ← React app (Deploy to Vercel)
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vercel.json
│   └── .env
│
├── backend/                     ← Django API (Deploy to Render)
│   ├── manage.py
│   ├── requirements.txt
│   ├── electricity_theft_detection/
│   ├── theft_detection/
│   ├── render.yaml
│   └── .env
```

---

## Step 1: Prepare Git Repository

```bash
# Clean up old files
rm vercel.json                  # Remove Vercel config from root
rm -rf api/                     # Remove old API folder

# Commit changes
git add .
git commit -m "Setup frontend-backend separation"
git push origin main
```

---

## Step 2: Deploy Backend to Render

### 2.1 Connect GitHub to Render

1. Go to [render.com](https://render.com)
2. Sign up/login with GitHub
3. Click **"New +"** → **"Web Service"**
4. Select your GitHub repository
5. Fill in the form:
   - **Name:** `electricity-theft-backend`
   - **Environment:** `Python 3.11`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command:**
     ```bash
     gunicorn electricity_theft_detection.wsgi:application --bind 0.0.0.0:10000
     ```
   - **Root Directory:** `.` (current directory)

### 2.2 Set Environment Variables

In Render Dashboard → **Environment** tab:

```
DEBUG=False
SECRET_KEY=<generate-a-strong-50-character-random-key>
ALLOWED_HOSTS=your-backend-name.onrender.com,localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
LOG_LEVEL=INFO
PYTHON_VERSION=3.11.0
PYTHONUNBUFFERED=1
```

**Example with real values:**
```
DEBUG=False
SECRET_KEY=kq8rjwp9sdfh23498sdhf23498hf234982hf982h3f98h23f
ALLOWED_HOSTS=electricity-theft-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://electricity-theft-frontend.vercel.app
```

### 2.3 Deploy

Click **"Create Web Service"** and wait for deployment (~3-5 minutes)

**Backend URL:** `https://electricity-theft-backend.onrender.com` (copy this!)

---

## Step 3: Deploy Frontend to Vercel

### 3.1 Create Production Environment File

In `frontend/.env.production`:

```env
REACT_APP_API_URL=https://electricity-theft-backend.onrender.com
REACT_APP_API_BASE_URL=https://electricity-theft-backend.onrender.com/api
```

Commit and push:
```bash
git add frontend/.env.production
git commit -m "Add production API endpoint"
git push origin main
```

### 3.2 Connect GitHub to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Sign up/login with GitHub
3. Click **"Add New +"** → **"Project"**
4. Select your repository
5. Click **"Import"**
6. Configure project:
   - **Framework Preset:** React
   - **Root Directory:** `./frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `build`
   - **Install Command:** `npm install`

### 3.3 Set Environment Variables

In Vercel Dashboard → **Settings** → **Environment Variables**:

```
REACT_APP_API_URL=https://electricity-theft-backend.onrender.com
REACT_APP_API_BASE_URL=https://electricity-theft-backend.onrender.com/api
```

### 3.4 Deploy

Click **"Deploy"** and wait for deployment (~2-3 minutes)

**Frontend URL:** `https://your-project-name.vercel.app` (this is your public site!)

---

## Step 4: Verify Setup

### Test Backend API

```bash
curl https://electricity-theft-backend.onrender.com/api/electricity-data/stats/
```

Should return JSON with statistics.

### Test Frontend Connection

Open `https://your-project-name.vercel.app` in browser:
- Dashboard should load
- Should show statistics from backend
- Prediction page should work

---

## Environment Variables Reference

### Backend (.env on Render)

| Variable | Value | Example |
|----------|-------|---------|
| `DEBUG` | `False` | For production |
| `SECRET_KEY` | 50+ random chars | `kq8rjwp9sdf...` |
| `ALLOWED_HOSTS` | Domain list | `electricity-theft-backend.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | Frontend URL | `https://your-frontend.vercel.app` |
| `DB_ENGINE` | `django.db.backends.sqlite3` | SQLite |
| `LOG_LEVEL` | `INFO` or `WARNING` | Production: `WARNING` |

### Frontend (.env in Vercel)

| Variable | Value | Example |
|----------|-------|---------|
| `REACT_APP_API_URL` | Backend base URL | `https://your-backend.onrender.com` |
| `REACT_APP_API_BASE_URL` | API endpoint | `https://your-backend.onrender.com/api` |

---

## Troubleshooting

### Frontend can't connect to backend
- ✅ Check `CORS_ALLOWED_ORIGINS` includes your Vercel frontend URL
- ✅ Check `REACT_APP_API_URL` matches backend domain
- ✅ Backend must have HTTPS enabled

### 404 errors on Vercel
- ✅ Make sure `Root Directory` is set to `./frontend`
- ✅ Clear Vercel cache: Settings → Git → Disconnect and reconnect

### Backend not starting
- ✅ Check logs on Render Dashboard
- ✅ Verify `gunicorn` is in requirements.txt
- ✅ Check Django migrations ran successfully

### Models not loading
- ✅ Backend needs to run `python manage.py generate_data` first
- ✅ SSH into Render or trigger operation via dashboard

---

## Monitoring

### Render Backend Logs
- Render Dashboard → Services → Select service → Logs

### Vercel Frontend Logs
- Vercel Dashboard → Select project → Deployments → Select deployment → Logs

---

## Updates & Redeployment

### Update Backend
```bash
git add .
git commit -m "Update backend"
git push origin main
# Render auto-redeploys on push
```

### Update Frontend
```bash
cd frontend
git add .
git commit -m "Update frontend"
git push origin main
# Vercel auto-redeploys on push
```

---

## Production Checklist

- [ ] Backend `DEBUG=False`
- [ ] Strong `SECRET_KEY` (50+ chars, random)
- [ ] `ALLOWED_HOSTS` configured on backend
- [ ] `CORS_ALLOWED_ORIGINS` includes frontend URL
- [ ] Frontend `.env` has correct backend API URL
- [ ] Database migrations completed
- [ ] ML models trained (`python manage.py generate_data`)
- [ ] Both frontend and backend using HTTPS
- [ ] Tested prediction functionality end-to-end

---

## Cost Estimate

- **Render Free Tier:** Backend runs free (15 min auto-stop on inactivity)
- **Vercel Free Tier:** Frontend runs free
- **Total:** $0/month for learning/demo!

You can upgrade to paid tiers when going to production.
