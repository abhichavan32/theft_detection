# Quick Deployment Checklist

## Before Deployment

```bash
# Update frontend .env
echo "REACT_APP_API_URL=https://electricity-theft-backend.onrender.com" > frontend/.env.production
echo "REACT_APP_API_BASE_URL=https://electricity-theft-backend.onrender.com/api" >> frontend/.env.production

# Test locally
npm install            # in frontend folder
npm start             # should start on localhost:3000
python manage.py runserver  # in backend folder
```

## Deployment Steps (5 minutes)

### Backend on Render

1. Go to render.com → New Web Service
2. Select your GitHub repo
3. **Build Command:**
   ```
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
   ```
4. **Start Command:**
   ```
   gunicorn electricity_theft_detection.wsgi:application --bind 0.0.0.0:10000
   ```
5. Add Environment Variables (see FULL_DEPLOYMENT.md)
6. Deploy → Copy backend URL when ready

### Frontend on Vercel

1. Go to vercel.com → Add New Project
2. Select your GitHub repo
3. **Root Directory:** `./frontend`
4. Add Environment Variables:
   - `REACT_APP_API_URL` = your backend Render URL
   - `REACT_APP_API_BASE_URL` = your backend URL + `/api`
5. Deploy

## Test After Deployment

```bash
# Open frontend
https://your-frontend.vercel.app

# Test API
curl https://your-backend.onrender.com/api/electricity-data/stats/

# Should return:
# {"total_records": X, "theft_detected": Y, "normal_detected": Z}
```

## Environment Variables Needed

**Backend (Render):**
```
DEBUG=False
SECRET_KEY=<50-char-random>
ALLOWED_HOSTS=your-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

**Frontend (Vercel):**
```
REACT_APP_API_URL=https://your-backend.onrender.com
REACT_APP_API_BASE_URL=https://your-backend.onrender.com/api
```
