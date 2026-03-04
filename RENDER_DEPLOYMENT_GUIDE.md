# Render Deployment Guide - Electricity Theft Detection

## Step-by-Step Deployment Instructions

### **STEP 1: Prerequisites**
- ✅ GitHub account with your repository
- ✅ Render account (create at https://render.com)
- ✅ Project pushed to GitHub

### **STEP 2: Push Project to GitHub**

If you haven't already pushed your code:

```bash
cd c:\Users\acer\OneDrive\Desktop\timepass\electricity_theft_detection

# Add and commit changes
git add -A
git commit -m "Electricity theft detection - ready for deployment"

# Add your GitHub remote (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/theft_detection.git

# Push to GitHub
git push -u origin main
```

> ⚠️ Make sure you create the repository on GitHub first before pushing!

---

### **STEP 3: Connect GitHub to Render**

1. Go to **https://render.com** and sign in/sign up
2. Click **"New Web Service"** or **"New +"** button
3. Select **"Web Service"**
4. Choose **"GitHub"** as the source
5. Click **"Connect GitHub"** and authorize Render to access your repositories
6. Select your **`theft_detection`** repository
7. Click **"Connect"**

---

### **STEP 4: Configure Render Deployment Settings**

#### **Basic Settings:**
- **Name:** `electricity-theft-detection` (or your preferred name)
- **Environment:** Select **Python 3.11** from dropdown
- **Region:** Select **Ohio** (or closest to you)
- **Branch:** `main`

#### **Build & Start Commands:**

**Build Command:**
```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

**Start Command:**
```
gunicorn electricity_theft_detection.wsgi:application
```

#### **Environment Variables:**

Click **"Add Environment Variable"** and add the following:

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `(leave empty - uses defaults)` |
| `PYTHON_VERSION` | `3.11` |

**For SECRET_KEY:** Render will auto-generate this. Leave blank or let Render manage it.

---

### **STEP 5: Select Plan**

- **Plan:** Select **Free** tier (suitable for development)
  - Or upgrade to **Starter ($7/month)** for always-on service
- **Auto-Deploy:** Enable **Yes** (auto-deploys on GitHub push)

---

### **STEP 6: Create Web Service**

1. Review all settings
2. Click **"Create Web Service"** button
3. Render will start building and deploying

**This may take 2-5 minutes.** You'll see build logs in real-time.

---

### **STEP 7: Monitor Deployment**

During deployment, you'll see:
```
Building Docker image...
Installing dependencies...
Running collectstatic...
Running migrations...
Starting server...
```

**Success indicator:**
```
✓ Service live at: https://your-service-name.onrender.com
```

---

### **STEP 8: Access Your Application**

Once deployed:
- **Visit:** `https://your-service-name.onrender.com`
- **Admin Panel:** `https://your-service-name.onrender.com/admin`
- **API Endpoints:** `https://your-service-name.onrender.com/api/*`

---

### **STEP 9: Troubleshooting**

#### **If the build fails:**

1. **Check logs:** Click "Logs" in Render dashboard
2. **Common errors:**
   - Missing dependencies → Update `requirements.txt`
   - Static files issue → Run `python manage.py collectstatic --noinput` locally
   - Database migration failed → Check `migrations/` folder

#### **If the service won't start:**

1. Check environment variables are set correctly
2. Verify `gunicorn` is in `requirements.txt`
3. Check ALLOWED_HOSTS setting

#### **If pages load but styles are missing:**

1. Try rebuilding: Click "Clear build cache" in settings
2. Re-deploy: Push a new commit to GitHub
3. Manually trigger: Click "Manual Deploy" > "Latest"

---

### **STEP 10: Accessing Admin (Optional)**

1. Create a superuser (run this in Render's shell or locally, then migrate):

**Local:**
```bash
python manage.py createsuperuser
```

Follow prompts for username, email, and password.

2. Push to GitHub
3. Render will auto-deploy
4. Visit: `https://your-service-name.onrender.com/admin`
5. Login with username and password

---

### **STEP 11: Deploy Updates**

**To deploy changes:**

```bash
# Make changes to your code
git add -A
git commit -m "Your changes"
git push origin main
```

Render will **automatically deploy** if "Auto-Deploy" is enabled.

**Or manually redeploy:**
1. Go to Render dashboard
2. Click your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

### **Important Configuration Files**

Your project includes:

| File | Purpose |
|------|---------|
| `render.yaml` | Render deployment configuration |
| `requirements.txt` | Python dependencies |
| `electricity_theft_detection/settings.py` | Django settings |
| `Procfile` | (Optional) Alternative to render.yaml |

---

### **Production Important Notes**

⚠️ **Before fully deploying to production:**

1. **Update SECRET_KEY** in Render environment
2. **Change DEBUG to False** (already set in render.yaml)
3. **Set ALLOWED_HOSTS** to your Render domain
4. **Enable HTTPS** (Render does this automatically)
5. **Configure CSRF_TRUSTED_ORIGINS** if accessing from different domains
6. **Set up database** (SQLite works for free tier, or use Render PostgreSQL add-on)

---

### **Optional: Add PostgreSQL Database**

1. In Render dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Name it: `electricity-theft-detection-db`
4. Copy the **Internal Database URL**
5. In your web service, add environment variable:
   - Key: `DATABASE_URL`
   - Value: `(paste the URL)`
6. Re-deploy

---

### **Useful Render CLI Commands**

If you install Render CLI:

```bash
# Login
render login

# Deploy
render deploy --name electricity-theft-detection

# View logs
render logs --name electricity-theft-detection

# Check status
render status --name electricity-theft-detection
```

---

### **Getting Help**

- 📖 [Render Django Docs](https://render.com/docs/deploy-django)
- 🆘 [Render Support](https://render.com/support)
- 💬 [Django Deployment Docs](https://docs.djangoproject.com/en/6.0/howto/deployment/)

---

## Summary

✅ Your app is ready for Render deployment!

**Next steps:**
1. Push code to GitHub
2. Create Render account
3. Connect GitHub repository
4. Configure settings (build/start commands, env vars)
5. Click "Create Web Service"
6. Monitor build logs
7. Access your deployed app!

**Estimated deployment time:** 2-5 minutes

Good luck! 🚀
