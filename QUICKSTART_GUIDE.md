# 🚀 Quick Start Guide - InkOdyssey Diary App

## Overview
InkOdyssey is a personal diary application with a beautiful, modern interface. This guide will help you get started quickly.

## Prerequisites
- Python 3.11+ installed
- Node.js 16+ and npm installed
- Git (optional)

## Setup Instructions

### 1. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
# On Windows (Git Bash):
source ../env/Scripts/activate
# On Windows (CMD):
..\env\Scripts\activate.bat
# On Mac/Linux:
source ../env/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run migrations (if not already done)
python manage.py migrate

# Create a superuser (optional, for admin access)
python manage.py createsuperuser

# Start the Django development server
python manage.py runserver
```

The backend will run on: `http://localhost:8000`

### 2. Frontend Setup (React + Vite)

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install

# Start the development server
npm run dev
```

The frontend will run on: `http://localhost:5173`

## Using the Application

### First Time Setup

1. **Register an Account**
   - Open browser to `http://localhost:5173`
   - Click "Register" or navigate to `/register`
   - Fill in:
     - Email
     - First Name
     - Last Name
     - Password
     - Confirm Password
   - Click "Register"

2. **Login**
   - You'll be automatically logged in after registration
   - Or navigate to `/login`
   - Enter email and password
   - Click "Login"

3. **Access Diary**
   - After login, you'll be redirected to `/diary`
   - Or manually navigate to `http://localhost:5173/diary`

### Creating Your First Entry

1. Click the **"✏️ New Entry"** button
2. Enter a title (e.g., "My First Day")
3. Add content blocks:
   - **Text Block**: Click "📝 Text" to add paragraphs
   - **Image Block**: Click "🖼️ Image" to add images (provide URL)
   - **Video Block**: Click "🎥 Video" to add videos (provide URL)
4. Fill in your content
5. Use ▲ ▼ buttons to reorder blocks
6. Click **"📝 Create Entry"**

### Managing Entries

#### View Entry
- Click any entry card from the list
- See full details including all content blocks

#### Edit Entry
1. Open an entry
2. Click **"✏️ Edit"**
3. Modify title or content blocks
4. Click **"💾 Save Changes"**

#### Delete Entry
1. Open an entry
2. Click **"🗑️ Delete"**
3. Confirm deletion

#### Filter by Date
1. Use the date picker in the toolbar
2. Select a date
3. View all entries from that day
4. Click "Clear" to reset

## Features Overview

### Dashboard Statistics
At the top of the diary page, you'll see:
- **Total Entries**: All your diary entries
- **This Week**: Entries created this week
- **This Month**: Entries created this month
- **Content Blocks**: Total blocks across all entries

### Content Block Types

1. **Text Blocks**
   - Write your thoughts, stories, or notes
   - Supports multi-line text
   - Auto-saves formatting

2. **Image Blocks**
   - Add images via URL
   - Include optional captions
   - Images display at full width

3. **Video Blocks**
   - Embed videos via URL
   - Include optional captions
   - Videos are playable inline

### Navigation

- **Main List View**: Shows all your entries
- **Detail View**: Shows full entry with all content
- **Create View**: Form to create new entry
- **Edit View**: Form to edit existing entry

## API Endpoints

The frontend communicates with these backend endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/diary/entries/` | List all entries |
| POST | `/api/diary/entries/` | Create new entry |
| GET | `/api/diary/entries/{id}/` | Get specific entry |
| PATCH | `/api/diary/entries/{id}/` | Update entry |
| DELETE | `/api/diary/entries/{id}/` | Delete entry |
| GET | `/api/diary/entries/by-date/?date=YYYY-MM-DD` | Filter by date |
| GET | `/api/diary/stats/` | Get statistics |

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'django'`
```bash
# Solution: Activate virtual environment
cd backend
source ../env/Scripts/activate  # Windows Git Bash
# or
..\env\Scripts\activate.bat     # Windows CMD
```

**Problem**: `django.db.utils.OperationalError: no such table`
```bash
# Solution: Run migrations
python manage.py migrate
```

**Problem**: `Port 8000 already in use`
```bash
# Solution: Kill the process or use different port
python manage.py runserver 8001
# Update API_BASE_URL in frontend Diary.jsx accordingly
```

### Frontend Issues

**Problem**: `Cannot GET /diary`
- Ensure frontend dev server is running (`npm run dev`)
- Check that you're using `http://localhost:5173` not `8000`

**Problem**: `401 Unauthorized` errors
- Your session has expired
- Click "Logout" and login again
- Check that backend is running

**Problem**: `Network Error` or `Failed to fetch`
- Verify backend is running on `http://localhost:8000`
- Check CORS settings in backend `settings.py`
- Ensure `CORS_ALLOWED_ORIGINS` includes `http://localhost:5173`

**Problem**: Blank page or white screen
- Check browser console for errors (F12)
- Verify all imports are correct
- Clear browser cache and reload

## Testing the Application

### Manual Testing Checklist

- [ ] Register new account
- [ ] Login with credentials
- [ ] View empty state message
- [ ] Create entry with text blocks
- [ ] Create entry with image blocks
- [ ] Create entry with video blocks
- [ ] View entry details
- [ ] Edit entry
- [ ] Delete entry (with confirmation)
- [ ] Filter entries by date
- [ ] Clear date filter
- [ ] View statistics dashboard
- [ ] Logout
- [ ] Login again

### Sample Content

**Sample Image URLs:**
- `https://images.unsplash.com/photo-1506905925346-21bda4d32df4`
- `https://images.unsplash.com/photo-1469474968028-56623f02e42e`

**Sample Video URLs:**
- `https://www.w3schools.com/html/mov_bbb.mp4`
- `https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4`

## Advanced Usage

### Using Django Admin

1. Create superuser (if not done):
   ```bash
   python manage.py createsuperuser
   ```

2. Access admin panel:
   - Navigate to `http://localhost:8000/admin/`
   - Login with superuser credentials
   - View/manage entries directly

### API Testing with cURL

**Create Entry:**
```bash
curl -X POST http://localhost:8000/api/diary/entries/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Entry",
    "content_blocks": [
      {
        "block_type": "text",
        "order": 0,
        "text_content": "This is a test entry"
      }
    ]
  }'
```

**Get All Entries:**
```bash
curl http://localhost:8000/api/diary/entries/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Keyboard Shortcuts (Future Enhancement)

Currently not implemented, but planned:
- `Ctrl + N`: New entry
- `Ctrl + S`: Save entry
- `Ctrl + E`: Edit current entry
- `Esc`: Cancel/Go back

## Mobile Usage

The application is fully responsive:
- **Mobile**: Optimized for phones (< 768px)
- **Tablet**: Adapted layout (768px - 1024px)
- **Desktop**: Full features (> 1024px)

## Data Storage

- All data is stored in SQLite database (`backend/db.sqlite3`)
- Media files stored in `backend/media/diary_media/`
- User passwords are hashed (never stored in plain text)
- JWT tokens stored in browser localStorage

## Security Notes

- All API endpoints require authentication
- Users can only access their own entries
- Tokens expire after 1 hour (refresh token valid for 30 days)
- Always logout on shared computers

## Next Steps

After getting comfortable with basic features:

1. **Customize Styling**
   - Edit `frontend/src/components/Diary/Diary.css`
   - Change colors, fonts, layouts

2. **Add Features**
   - Implement tags/categories
   - Add search functionality
   - Create export to PDF feature

3. **Deploy Application**
   - Deploy backend (Heroku, Railway, AWS)
   - Deploy frontend (Vercel, Netlify)
   - Update API URLs for production

## Getting Help

- **Backend API Docs**: `backend/diary/API_DOCUMENTATION.md`
- **Frontend Docs**: `frontend/DIARY_COMPONENT_README.md`
- **Implementation Guide**: `backend/diary/IMPLEMENTATION_GUIDE.md`

## Tips for Best Experience

1. **Regular Writing**: Make it a daily habit
2. **Use Multiple Blocks**: Mix text with images/videos
3. **Descriptive Titles**: Make entries easy to find later
4. **Backup Data**: Periodically backup `db.sqlite3`
5. **Explore Features**: Try all content block types

## Common Workflows

### Daily Journal Entry
1. Open app
2. Click "New Entry"
3. Title: "November 7, 2025"
4. Add text blocks for morning, afternoon, evening
5. Add photos from the day
6. Save

### Travel Diary
1. Create entry for each day
2. Add location in title
3. Use image blocks for photos
4. Add video blocks for clips
5. Write descriptions in text blocks

### Project Documentation
1. Create entry per milestone
2. Use text blocks for notes
3. Add screenshots as images
4. Link to videos or demos
5. Update entries as project progresses

---

**Enjoy writing in your personal diary! 📖✨**
