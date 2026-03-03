# Deployment Guide

## Environment Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the `.env.example` file to `.env` and update with your deployment values:

```bash
cp .env.example .env
```

### 3. Update `.env` for Your Environment

**Development:**
```env
DEBUG=True
SECRET_KEY=your-development-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Production:**
```env
DEBUG=False
SECRET_KEY=your-production-secret-key-minimum-50-chars-random
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 4. Database Configuration

**SQLite (Default - Development):**
```env
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

**PostgreSQL (Recommended for Production):**
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=electricity_theft_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=your-db-host.com
DB_PORT=5432
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Generate Training Data & Train Models
```bash
python manage.py generate_data --normal 1000 --theft 200 --meters 10
```

### 7. Collect Static Files (Production)
```bash
python manage.py collectstatic --noinput
```

### 8. Run Development Server
```bash
python manage.py runserver
```

### 9. Run Production Server (Using Gunicorn)
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn electricity_theft_detection.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 10. Security Checklist
- [ ] Generate a strong `SECRET_KEY` for production
- [ ] Set `DEBUG=False` in production
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Set secure database credentials
- [ ] Configure CORS and CSRF settings
- [ ] Use HTTPS in production
- [ ] Keep `.env` file out of version control

## Important Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` (production) |
| `SECRET_KEY` | Django secret key | 50+ random characters |
| `ALLOWED_HOSTS` | Allowed domain names | `yourdomain.com,www.yourdomain.com` |
| `DB_ENGINE` | Database type | `django.db.backends.postgresql` |
| `DB_NAME` | Database name | `electricity_theft_db` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | `secure_password` |
| `DB_HOST` | Database host | `localhost` or IP |

## Deployment Platforms

### Heroku
1. Create `Procfile`:
```
web: gunicorn electricity_theft_detection.wsgi:application
release: python manage.py migrate
```

2. Create `runtime.txt`:
```
python-3.10.12
```

3. Deploy:
```bash
git push heroku main
```

### Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "electricity_theft_detection.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### AWS/Azure/GCP
- Use environment variable management tools (AWS Secrets Manager, Azure Key Vault)
- Load `.env` variables from those services
- Use auto-scaling groups for multiple instances
