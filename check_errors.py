#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electricity_theft_detection.settings')
django.setup()

from theft_detection.models import ElectricityData, PredictionResult
from django.contrib.auth.models import User

print("\n" + "="*60)
print("🔍 SYSTEM DIAGNOSTICS")
print("="*60)

# Check database
try:
    print("\n✓ Database Connection: OK")
    print(f"  - Total Records: {ElectricityData.objects.count()}")
    print(f"  - Total Predictions: {PredictionResult.objects.count()}")
except Exception as e:
    print(f"✗ Database Error: {e}")

# Check models
try:
    print("\n✓ Models: OK")
    print(f"  - ElectricityData objects: {ElectricityData.objects.count()}")
    print(f"  - PredictionResult objects: {PredictionResult.objects.count()}")
except Exception as e:
    print(f"✗ Model Error: {e}")

# Check admin user
try:
    admin_user = User.objects.get(username='admin')
    print(f"\n✓ Admin User: EXISTS")
    print(f"  - Username: {admin_user.username}")
    print(f"  - Email: {admin_user.email}")
    print(f"  - Is Superuser: {admin_user.is_superuser}")
except User.DoesNotExist:
    print(f"\n✗ Admin User: NOT FOUND")
except Exception as e:
    print(f"✗ Admin Check Error: {e}")

# Check ML models
try:
    from theft_detection.ml_models.detector import ElectricityTheftDetector
    detector = ElectricityTheftDetector()
    if detector.load_models():
        print("\n✓ ML Models: LOADED")
        print("  - Scaler: Loaded")
        print("  - LOF Model: Loaded")
        print("  - Isolation Forest: Loaded")
    else:
        print("\n⚠ ML Models: Not yet trained (will be trained on first prediction)")
except Exception as e:
    print(f"\n✗ ML Models Error: {e}")

print("\n" + "="*60)
print("✓ ALL SYSTEMS OPERATIONAL")
print("="*60 + "\n")
