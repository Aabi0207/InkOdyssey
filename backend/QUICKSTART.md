# 🚀 Quick Start Guide

## Get Started in 3 Minutes

### 1️⃣ Create Environment File
```bash
cd backend
cp .env.example .env
```

### 2️⃣ Create Superuser (Optional)
```bash
python manage.py createsuperuser
```
Follow prompts to enter email, first name, last name, and password.

### 3️⃣ Start the Server
```bash
python manage.py runserver
```

Server will start at: **http://localhost:8000**

---

## 🧪 Test Your API

### Method 1: Use the Test Script
```bash
python test_api.py
```

### Method 2: Manual Testing

#### Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "first_name": "Demo",
    "last_name": "User",
    "password": "DemoPass123!",
    "password2": "DemoPass123!"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "DemoPass123!"
  }'
```

Copy the `access` token from the response.

#### Get User Profile
```bash
curl -X GET http://localhost:8000/api/auth/user/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

---

## 📱 Available Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/auth/register/` | POST | No | Register new user |
| `/api/auth/login/` | POST | No | Login user |
| `/api/auth/logout/` | POST | Yes | Logout user |
| `/api/auth/user/` | GET/PUT/PATCH | Yes | Get/update profile |
| `/api/auth/change-password/` | POST | Yes | Change password |
| `/api/auth/token/refresh/` | POST | No | Refresh JWT token |
| `/api/auth/social/google/` | GET | No | Google OAuth login |
| `/api/auth/social/facebook/` | GET | No | Facebook OAuth login |
| `/admin/` | GET | Yes | Django Admin Panel |

---

## 🔐 Setup Social Login (Optional)

### Google OAuth
1. Get credentials from [Google Cloud Console](https://console.cloud.google.com/)
2. Add to `.env`:
   ```
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

### Facebook OAuth
1. Get credentials from [Facebook Developers](https://developers.facebook.com/)
2. Add to `.env`:
   ```
   FACEBOOK_CLIENT_ID=your-app-id
   FACEBOOK_CLIENT_SECRET=your-app-secret
   ```

---

## 🐛 Troubleshooting

### Server won't start?
```bash
# Check if port 8000 is in use
python manage.py runserver 8080
```

### Database errors?
```bash
# Recreate database
rm db.sqlite3
python manage.py migrate
```

### Import errors?
```bash
# Reinstall packages
pip install -r requirements.txt
```

---

## 📚 Documentation

- Full API docs: `README.md`
- Implementation details: `IMPLEMENTATION_SUMMARY.md`
- Environment setup: `.env.example`

---

## ✅ What's Included

- ✨ Email-based authentication
- 🔑 JWT token authentication
- 🔄 Token refresh mechanism
- 🌐 Google & Facebook OAuth
- 👤 User profile management
- 🔒 Password change
- 🛡️ Secure password hashing
- 📊 Django admin panel
- 🔧 Environment configuration
- 📝 Complete API documentation

---

**Need help?** Check `README.md` for detailed documentation!
