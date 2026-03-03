# Vercel Deployment Guide

## Quick Start (5 minutes)

### 1. Install Vercel CLI
```bash
npm i -g vercel
```

### 2. Push to GitHub
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### 3. Deploy to Vercel
```bash
vercel --prod
```

Or connect your GitHub repo directly at [vercel.com](https://vercel.com):
1. Click "Add New..." → "Project"
2. Import your GitHub repo
3. Click "Deploy"

---

## Configuration (Important!)

### Set Environment Variables on Vercel

Go to your project on Vercel Dashboard → Settings → Environment Variables

Add these variables:

```env
DEBUG=False
SECRET_KEY=<generate-a-strong-random-secret-key-50-chars-minimum>
ALLOWED_HOSTS=your-project-name.vercel.app,your-domain.com
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
LOG_LEVEL=WARNING
```

**For Production Database (PostgreSQL recommended):**
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_db_name
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=your-db-host.com
DB_PORT=5432
```

---

## Troubleshooting

### Error: `externally-managed-environment`
**Cause:** Vercel uses `uv` (a fast Python package manager)
**Solution:** Already handled by `vercel.json` configuration

### Error: `ModuleNotFoundError`
**Solution:** Make sure all packages in `requirements.txt` are correct:
```bash
pip list
```

### Database Issues
- Vercel doesn't persist SQLite across deployments
- **Upgrade to PostgreSQL** before production
- Use PostgreSQL credentials from your hosting provider (Render, Heroku Postgres, AWS RDS, etc.)

### Static Files Not Loading
Already configured in `settings.py` to use `STATIC_ROOT` and `STATIC_URL`

---

## Advanced: Custom Domain

1. Go to Vercel Dashboard → Project Settings → Domains
2. Add your custom domain (e.g., `yourdomain.com`)
3. Follow DNS configuration instructions from your domain registrar

---

## Monitoring & Logs

View logs in Vercel:
```bash
vercel logs <project-name>
```

Or through the Vercel Dashboard → Deployments → Logs

---

## Redeployment

After pushing code changes:
```bash
git push origin main
```

Vercel will automatically redeploy! (if auto-deploy is enabled)

Or manually:
```bash
vercel --prod
```
