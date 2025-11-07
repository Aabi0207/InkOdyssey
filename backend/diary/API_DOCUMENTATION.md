# Diary API Documentation

This document describes all the available API endpoints for the Diary application.

## Base URL
All diary endpoints are prefixed with: `/api/diary/`

## Authentication
All diary endpoints require authentication using JWT tokens. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Diary Entry Endpoints

### 1. List All Diary Entries
**GET** `/api/diary/entries/`

Returns a list of all diary entries for the authenticated user.

**Response:**
```json
[
  {
    "id": 1,
    "title": "My First Entry",
    "author_email": "user@example.com",
    "author_name": "John Doe",
    "content_blocks_count": 3,
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z"
  }
]
```

---

### 2. Create a New Diary Entry
**POST** `/api/diary/entries/`

Create a new diary entry with optional content blocks.

**Request Body:**
```json
{
  "title": "My Day at the Beach",
  "content_blocks": [
    {
      "block_type": "text",
      "order": 0,
      "text_content": "Today was an amazing day at the beach!"
    },
    {
      "block_type": "image",
      "order": 1,
      "media_url": "https://example.com/beach.jpg",
      "caption": "Beautiful sunset"
    },
    {
      "block_type": "text",
      "order": 2,
      "text_content": "Can't wait to go back!"
    }
  ]
}
```

**Response:** (201 Created)
```json
{
  "id": 2,
  "title": "My Day at the Beach",
  "content_blocks": [
    {
      "id": 1,
      "block_type": "text",
      "order": 0,
      "text_content": "Today was an amazing day at the beach!",
      "media_file": null,
      "media_url": null,
      "caption": "",
      "created_at": "2025-01-15T14:30:00Z"
    }
  ],
  "created_at": "2025-01-15T14:30:00Z",
  "updated_at": "2025-01-15T14:30:00Z"
}
```

---

### 3. Get a Specific Diary Entry
**GET** `/api/diary/entries/<id>/`

Retrieve detailed information about a specific diary entry including all content blocks.

**Response:**
```json
{
  "id": 1,
  "title": "My First Entry",
  "author": 1,
  "author_email": "user@example.com",
  "author_name": "John Doe",
  "content_blocks": [
    {
      "id": 1,
      "block_type": "text",
      "order": 0,
      "text_content": "This is my first diary entry!",
      "media_file": null,
      "media_url": null,
      "caption": "",
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

---

### 4. Update a Diary Entry
**PUT/PATCH** `/api/diary/entries/<id>/`

Update an existing diary entry. Using PUT will replace all content blocks, while PATCH can partially update.

**Request Body:**
```json
{
  "title": "Updated Title",
  "content_blocks": [
    {
      "block_type": "text",
      "order": 0,
      "text_content": "Updated content"
    }
  ]
}
```

**Response:** (200 OK)
```json
{
  "id": 1,
  "title": "Updated Title",
  "content_blocks": [...],
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T15:45:00Z"
}
```

---

### 5. Delete a Diary Entry
**DELETE** `/api/diary/entries/<id>/`

Delete a diary entry and all associated content blocks.

**Response:** (204 No Content)

---

### 6. Get Diary Entries by Date
**GET** `/api/diary/entries/by-date/?date=YYYY-MM-DD`

Retrieve all diary entries created on a specific date.

**Query Parameters:**
- `date` (required): Date in YYYY-MM-DD format (e.g., 2025-01-15)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Morning Entry",
    "author": 1,
    "author_email": "user@example.com",
    "author_name": "John Doe",
    "content_blocks": [...],
    "created_at": "2025-01-15T08:30:00Z",
    "updated_at": "2025-01-15T08:30:00Z"
  },
  {
    "id": 2,
    "title": "Evening Entry",
    "author": 1,
    "author_email": "user@example.com",
    "author_name": "John Doe",
    "content_blocks": [...],
    "created_at": "2025-01-15T20:00:00Z",
    "updated_at": "2025-01-15T20:00:00Z"
  }
]
```

---

## Content Block Endpoints

### 7. List Content Blocks for an Entry
**GET** `/api/diary/entries/<entry_id>/blocks/`

Get all content blocks for a specific diary entry.

**Response:**
```json
[
  {
    "id": 1,
    "block_type": "text",
    "order": 0,
    "text_content": "First paragraph",
    "media_file": null,
    "media_url": null,
    "caption": "",
    "created_at": "2025-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "block_type": "image",
    "order": 1,
    "text_content": null,
    "media_file": "/media/diary_media/2025/01/15/photo.jpg",
    "media_url": null,
    "caption": "A beautiful moment",
    "created_at": "2025-01-15T10:31:00Z"
  }
]
```

---

### 8. Add a Content Block to an Entry
**POST** `/api/diary/entries/<entry_id>/blocks/`

Add a new content block to an existing diary entry.

**Request Body (Text Block):**
```json
{
  "block_type": "text",
  "order": 3,
  "text_content": "Additional thoughts..."
}
```

**Request Body (Image/Video Block):**
```json
{
  "block_type": "image",
  "order": 4,
  "media_url": "https://example.com/image.jpg",
  "caption": "Optional caption"
}
```

**Note:** For file uploads, use `multipart/form-data` and include the file in the `media_file` field.

**Response:** (201 Created)
```json
{
  "id": 3,
  "block_type": "text",
  "order": 3,
  "text_content": "Additional thoughts...",
  "media_file": null,
  "media_url": null,
  "caption": "",
  "created_at": "2025-01-15T16:00:00Z"
}
```

---

### 9. Get a Specific Content Block
**GET** `/api/diary/entries/<entry_id>/blocks/<id>/`

Retrieve details of a specific content block.

**Response:**
```json
{
  "id": 1,
  "block_type": "text",
  "order": 0,
  "text_content": "Content text",
  "media_file": null,
  "media_url": null,
  "caption": "",
  "created_at": "2025-01-15T10:30:00Z"
}
```

---

### 10. Update a Content Block
**PUT/PATCH** `/api/diary/entries/<entry_id>/blocks/<id>/`

Update an existing content block.

**Request Body:**
```json
{
  "text_content": "Updated text content",
  "order": 1
}
```

**Response:** (200 OK)

---

### 11. Delete a Content Block
**DELETE** `/api/diary/entries/<entry_id>/blocks/<id>/`

Delete a specific content block.

**Response:** (204 No Content)

---

## Statistics Endpoint

### 12. Get Diary Statistics
**GET** `/api/diary/stats/`

Get statistics about the user's diary entries.

**Response:**
```json
{
  "total_entries": 25,
  "entries_this_month": 8,
  "entries_this_week": 3,
  "total_blocks": 87,
  "block_distribution": [
    {
      "block_type": "text",
      "count": 45
    },
    {
      "block_type": "image",
      "count": 32
    },
    {
      "block_type": "video",
      "count": 10
    }
  ]
}
```

---

## Content Block Types

### Text Block
```json
{
  "block_type": "text",
  "order": 0,
  "text_content": "Your text content here"
}
```

### Image Block
```json
{
  "block_type": "image",
  "order": 1,
  "media_file": "file object (for upload)",
  "media_url": "https://example.com/image.jpg (for external URL)",
  "caption": "Optional image caption"
}
```

### Video Block
```json
{
  "block_type": "video",
  "order": 2,
  "media_file": "file object (for upload)",
  "media_url": "https://example.com/video.mp4 (for external URL)",
  "caption": "Optional video caption"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Date parameter is required (format: YYYY-MM-DD)"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Notes

1. **Authentication Required**: All endpoints require a valid JWT access token.
2. **User Isolation**: Users can only access their own diary entries and content blocks.
3. **Multiple Entries Per Day**: Users can create multiple diary entries on the same day.
4. **Content Block Order**: The `order` field determines the display sequence of blocks within an entry.
5. **Media Files**: 
   - Upload files using `multipart/form-data`
   - Alternatively, provide external URLs using the `media_url` field
   - Supported for images and videos only
6. **Timestamps**: All timestamps are in ISO 8601 format with timezone information.
7. **Pagination**: List endpoints may include pagination (configured at 10 items per page).
