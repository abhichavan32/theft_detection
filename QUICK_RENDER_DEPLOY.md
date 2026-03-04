# ⚡ QUICK RENDER DEPLOYMENT (5 Minutes)

## Copy-Paste Quick Start

### 1️⃣ Push to GitHub
```bash
cd c:\Users\acer\OneDrive\Desktop\timepass\electricity_theft_detection

git add -A
git commit -m "Ready for deployment"
git remote add origin https://github.com/YOUR_USERNAME/theft_detection.git
git push -u origin main
```

### 2️⃣ Go to Render
- Visit https://render.com
- Sign up / Log in
- Click "New Web Service"

### 3️⃣ Connect GitHub
- Choose "GitHub" as source
- Authorize Render
- Select your `theft_detection` repository
- Click "Connect"

### 4️⃣ Configure (Copy These Exactly)

**Name:** electricity-theft-detection
**Environment:** Python 3.11
**Region:** Ohio
**Branch:** main

**Build Command:**
```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

**Start Command:**
```
gunicorn electricity_theft_detection.wsgi:application
```

**Environment Variables:**
```
DEBUG=False
```

### 5️⃣ Deploy
- Click "Create Web Service"
- Wait 2-5 minutes for deployment
- Visit your live URL: `https://your-service-name.onrender.com`

---

## Done! 🎉

Your app is now live on the internet!

**What's deployed:**
- ✅ Django backend
- ✅ Database (SQLite)
- ✅ Static files (CSS, images)
- ✅ Admin panel

**Get your URL from:**
Render Dashboard → Your Service → "Live"

---

## If Something Goes Wrong 🔧

1. **Check logs:** Click "Logs" tab in Render
2. **Common fixes:**
   - Missing file → Check files are committed to GitHub
   - Module error → Add to requirements.txt
   - Static files broken → They're collected during build

3. **Redeploy:**
   - Make changes locally
   - `git push origin main`
   - Render auto-deploys!

---

**Need more help?** See `RENDER_DEPLOYMENT_GUIDE.md` for detailed instructions!
