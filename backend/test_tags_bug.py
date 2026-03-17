import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import json

User = get_user_model()
user = User.objects.first()
if not user:
    user = User.objects.create_user(username='test_bugs', email='test@bug.com', password='test')

client = APIClient()
client.force_authenticate(user=user)

# 1. Create a tag
client.post('/api/diary/tags/', {'name': 'Holiday'}, format='json')

# 2. Create entry with a tag
res = client.post('/api/diary/entries/', {
    'title': 'Test Entry',
    'tags': ['Holiday', 'NewTag']
}, format='json')

print("Create Entry Status:", res.status_code)
print("Create Entry Data:", json.dumps(res.data))

# 3. Retrieve entries
res2 = client.get('/api/diary/entries/')
print("List Entries tags:")
for entry in res2.data:
    print(json.dumps(entry.get('tags'), indent=2))

