import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.first()
if user:
    from rest_framework.test import APIClient
    client = APIClient()
    client.force_authenticate(user=user)
    res = client.get('/api/diary/entries/')
    import json
    print("Entries type:", type(res.data))
    if hasattr(res.data, 'get'):
        print(json.dumps(res.data, default=str)[:1000])
    else:
        print(json.dumps(res.data, default=str)[:1000])
    
    print("\nTags info:")
    res_tags = client.get('/api/diary/tags/')
    print(json.dumps(res_tags.data, default=str)[:1000])
else:
    print("no user")
