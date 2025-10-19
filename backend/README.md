# InkOdyssey Backend - Authentication API

A comprehensive Django REST Framework backend with JWT authentication and social login (Google & Facebook).

## Features

✅ **Custom User Model** - Email-based authentication with first name and last name
✅ **JWT Authentication** - Secure token-based authentication with refresh tokens
✅ **Social Login** - Google OAuth2 and Facebook OAuth2 integration
✅ **User Registration** - Sign up with email, password, first name, and last name
✅ **User Login** - Email and password authentication
✅ **Token Refresh** - Automatic token refresh for seamless sessions
✅ **Password Change** - Secure password update for authenticated users
✅ **User Profile** - Get and update user details
✅ **CORS Enabled** - Ready for frontend integration

## Tech Stack

- **Django 4.2** - Python web framework
- **Django REST Framework** - API toolkit
- **djangorestframework-simplejwt** - JWT authentication
- **django-allauth** - Social authentication
- **dj-rest-auth** - REST API endpoints for auth
- **django-cors-headers** - CORS handling
- **python-decouple** - Configuration management

## Project Structure

```
backend/
├── backend/              # Main project settings
│   ├── settings.py       # Django configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI configuration
├── users/               # Users app
│   ├── models.py        # Custom User model
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API views
│   ├── urls.py          # Auth URL patterns
│   └── admin.py         # Admin configuration
├── manage.py            # Django management script
├── .env.example         # Environment variables template
└── db.sqlite3          # SQLite database
```

## Setup Instructions

### 1. Environment Setup

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Update `.env` with your credentials:
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FACEBOOK_CLIENT_ID=your-facebook-app-id
FACEBOOK_CLIENT_SECRET=your-facebook-app-secret
```

### 2. Database Setup

Migrations have already been applied. If you need to reset:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication

#### Register a New User
```http
POST /api/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securepassword123",
  "password2": "securepassword123"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "date_joined": "2025-10-15T12:00:00Z",
    "provider": null
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "User registered successfully"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "Login successful"
}
```

#### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Logout
```http
POST /api/auth/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### User Management

#### Get User Profile
```http
GET /api/auth/user/
Authorization: Bearer <access_token>
```

#### Update User Profile
```http
PUT /api/auth/user/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith"
}
```

#### Change Password
```http
POST /api/auth/change-password/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "oldpassword123",
  "new_password": "newpassword456",
  "new_password2": "newpassword456"
}
```

### Social Authentication

#### Google Login
```http
GET /api/auth/social/google/
```

#### Facebook Login
```http
GET /api/auth/social/facebook/
```

## Setting Up Social Authentication

### Google OAuth2

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:8000/api/auth/social/google/callback/`
   - `http://localhost:3000` (your frontend URL)
6. Copy Client ID and Client Secret to `.env`

### Facebook OAuth2

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add Facebook Login product
4. Configure OAuth redirect URIs:
   - `http://localhost:8000/api/auth/social/facebook/callback/`
5. Copy App ID and App Secret to `.env`

## Testing with cURL

### Register
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "testpass123",
    "password2": "testpass123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### Get User (with token)
```bash
curl -X GET http://localhost:8000/api/auth/user/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Security Notes

- ✅ Passwords are hashed using Django's default hasher (PBKDF2)
- ✅ JWT tokens are signed and verified
- ✅ CORS is configured for specific origins
- ✅ Token blacklisting enabled for logout
- ✅ Email validation on registration
- ✅ Password validation (minimum length, common passwords, etc.)

## Development Tips

### Access Admin Panel
Visit `http://localhost:8000/admin/` and login with superuser credentials.

### Check Installed Packages
```bash
pip list
```

### Run Tests
```bash
python manage.py test users
```

### Create New Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Troubleshooting

### Issue: Import errors or missing modules
**Solution:** Ensure all packages are installed in your virtual environment:
```bash
pip install -r requirements.txt
```

### Issue: CORS errors from frontend
**Solution:** Update `CORS_ALLOWED_ORIGINS` in `.env` with your frontend URL

### Issue: Social login not working
**Solution:** 
1. Verify OAuth credentials in `.env`
2. Check redirect URIs match in provider console
3. Ensure provider apps are enabled in Django admin

## Next Steps

- [ ] Create `requirements.txt` with all dependencies
- [ ] Add email verification for registration
- [ ] Implement password reset functionality
- [ ] Add rate limiting to prevent abuse
- [ ] Set up production database (PostgreSQL)
- [ ] Configure static/media files for production
- [ ] Add comprehensive test coverage
- [ ] Set up CI/CD pipeline

## License

This project is part of the InkOdyssey application.
