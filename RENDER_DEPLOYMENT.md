# Render.com Deployment Guide (Recommended for ML Projects)

## Why Render Instead of Vercel?

✅ **Render is perfect for ML/Django apps**
- Handles large Python packages (scikit-learn, pandas, numpy)
- Better for long-running processes
- PostgreSQL support built-in  
- More generous free tier for learning
- Proper Django support

❌ **Vercel is for lightweight APIs only**
- Limited runtime
- No GPU/ML support
- Complex Python deps cause issues

---

## Deployment Steps

### 1. Delete Vercel Config
```bash
rm vercel.json
git add .
git commit -m "Switch to Render deployment"
git push origin main
```

### 2. Connect GitHub to Render

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select your GitHub repo
5. Fill in:
   - **Name:** `electricity-theft-detection`
   - **Runtime:** `Python 3.11`
   - **Build Command:** 
     ```
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command:**
     ```
     gunicorn electricity_theft_detection.wsgi:application --bind 0.0.0.0:10000
     ```

### 3. Set Environment Variables

In Render Dashboard → Environment:

```
DEBUG=False
SECRET_KEY=your-50-char-random-key
ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
LOG_LEVEL=INFO
PYTHONUNBUFFERED=1
```

**For PostgreSQL** (recommended for production):
```
DB_ENGINE=django.db.backends.postgresql
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### 4. Deploy

Click "Create Web Service" and Render will auto-deploy! 🚀

---

## Monitoring

- Logs: View in Render Dashboard → Logs
- Performance: Built-in metrics
- Auto-redeploy: On every git push

---

## Upgrading from Free

If you need:
- Always-on server
- PostgreSQL database  
- More resources

Render paid plans start at $7/month (very reasonable for ML projects).

---

## Local Testing

Test locally before deploying:

```bash
# Install gunicorn
pip install gunicorn

# Run like Render does
gunicorn electricity_theft_detection.wsgi:application --bind 0.0.0.0:8000

# Visit: http://localhost:8000
```
