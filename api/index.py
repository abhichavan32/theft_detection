import os
import sys
import django
from pathlib import Path

# Add the project directory to the path
sys.path.insert(0, '/var/task')

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electricity_theft_detection.settings')

# Setup Django
django.setup()

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()

app = get_wsgi_application()
