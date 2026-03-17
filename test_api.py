import urllib.request
import json
import sqlite3

# Extract user token directly from sqlite DB if possible, or bypass with Django test client
from django.test import Client
from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

User = get_user_model()
user = User.objects.first()
if user:
    from rest_framework.test import APIClient
    client = APIClient()
    client.force_authenticate(user=user)
    res = client.get('/api/diary/entries/')
    print(json.dumps(res.data, indent=2)[:500])
else:
    print("no user")
