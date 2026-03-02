"""
WSGI config for electricity_theft_detection project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electricity_theft_detection.settings')

application = get_wsgi_application()
