# Self-Reflection API Documentation

## Overview
The Self-Reflection API allows users to track their daily reflections by answering customizable questions. Questions can be of three types:
- **Range**: Numeric response (1-10)
- **Multiple Choice**: Select from predefined options
- **Text**: Free-form text response

## Authentication
All endpoints require JWT authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

## Base URL
```
/api/self-reflection/
```

---

## Endpoints

### 1. Reflection Questions

#### List All Questions
```http
GET /api/self-reflection/questions/
```

**Query Parameters:**
- `is_active` (optional): Filter by active status (`true` or `false`)
- `category` (optional): Filter by category name

**Response:**
```json
[
  {
    "id": 1,
    "question_text": "Rate your day out of 10",
    "question_type": "range",
    "min_value": 1,
    "max_value": 10,
    "choices": null,
    "is_active": true,
    "order": 1,
    "category": "Daily",
    "created_at": "2025-12-01T10:00:00Z",
    "updated_at": "2025-12-01T10:00:00Z"
  },
  {
    "id": 2,
    "question_text": "Mood of the day",
    "question_type": "choice",
    "min_value": 1,
    "max_value": 10,
    "choices": ["Happy", "Sad", "Neutral", "Excited", "Anxious"],
    "is_active": true,
    "order": 2,
    "category": "Wellness",
    "created_at": "2025-12-01T10:00:00Z",
    "updated_at": "2025-12-01T10:00:00Z"
  }
]
```

#### Get Active Questions Only
```http
GET /api/self-reflection/questions/active/
```

**Response:** Same as list, but only active questions ordered by display order.

#### Get Question Categories
```http
GET /api/self-reflection/questions/categories/
```

**Response:**
```json
{
  "categories": ["Daily", "Wellness", "Productivity"]
}
```

#### Create Question
```http
POST /api/self-reflection/questions/
```

**Request Body:**
```json
{
  "question_text": "How many glasses of water did you have?",
  "question_type": "range",
  "min_value": 0,
  "max_value": 10,
  "is_active": true,
  "order": 5,
  "category": "Health"
}
```

**For Multiple Choice:**
```json
{
  "question_text": "Energy level",
  "question_type": "choice",
  "choices": ["Very Low", "Low", "Medium", "High", "Very High"],
  "is_active": true,
  "order": 3,
  "category": "Wellness"
}
```

**For Text:**
```json
{
  "question_text": "What are you grateful for today?",
  "question_type": "text",
  "is_active": true,
  "order": 10,
  "category": "Gratitude"
}
```

#### Update Question
```http
PUT /api/self-reflection/questions/{id}/
PATCH /api/self-reflection/questions/{id}/
```

**Request Body:** Same as create (partial for PATCH)

#### Delete Question
```http
DELETE /api/self-reflection/questions/{id}/
```

---

### 2. Daily Reflections

#### List User's Reflections
```http
GET /api/self-reflection/reflections/
```

**Response:**
```json
[
  {
    "id": 1,
    "user_email": "user@example.com",
    "date": "2025-12-02",
    "notes": "Had a great day overall!",
    "responses": [
      {
        "id": 1,
        "question_id": 1,
        "question_text": "Rate your day out of 10",
        "question_type": "range",
        "range_response": 8,
        "choice_response": null,
        "text_response": null,
        "created_at": "2025-12-02T18:00:00Z",
        "updated_at": "2025-12-02T18:00:00Z"
      },
      {
        "id": 2,
        "question_id": 2,
        "question_text": "Mood of the day",
        "question_type": "choice",
        "range_response": null,
        "choice_response": "Happy",
        "text_response": null,
        "created_at": "2025-12-02T18:00:00Z",
        "updated_at": "2025-12-02T18:00:00Z"
      }
    ],
    "created_at": "2025-12-02T18:00:00Z",
    "updated_at": "2025-12-02T18:00:00Z"
  }
]
```

#### Get Today's Reflection
```http
GET /api/self-reflection/reflections/today/
```

**Success Response:** Same as individual reflection object

**Not Found Response (404):**
```json
{
  "detail": "No reflection found for today.",
  "date": "2025-12-02",
  "has_reflection": false
}
```

#### Get Reflection by Date
```http
GET /api/self-reflection/reflections/by_date/?date=2025-12-01
```

**Query Parameters:**
- `date` (required): Date in YYYY-MM-DD format

**Response:** Same as individual reflection

#### Get Reflections for Date Range
```http
GET /api/self-reflection/reflections/date_range/?start_date=2025-11-01&end_date=2025-11-30
```

**Query Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format

**Response:** Array of reflections

#### Create/Update Daily Reflection
```http
POST /api/self-reflection/reflections/
```

**Request Body:**
```json
{
  "date": "2025-12-02",
  "notes": "Today was productive!",
  "responses": [
    {
      "question_id": 1,
      "range_response": 8
    },
    {
      "question_id": 2,
      "choice_response": "Happy"
    },
    {
      "question_id": 3,
      "text_response": "I'm grateful for my family and friends."
    },
    {
      "question_id": 4,
      "range_response": 7
    }
  ]
}
```

**Notes:**
- If a reflection for the date already exists, it will be updated
- Only provide the response field that matches the question type:
  - Range questions: `range_response`
  - Choice questions: `choice_response`
  - Text questions: `text_response`

**Response:** Complete reflection object with all responses

#### Update Reflection
```http
PUT /api/self-reflection/reflections/{id}/
PATCH /api/self-reflection/reflections/{id}/
```

**Request Body:** Same as create

#### Get Statistics
```http
GET /api/self-reflection/reflections/stats/?days=30
```

**Query Parameters:**
- `days` (optional, default: 30): Number of days to analyze

**Response:**
```json
{
  "total_reflections": 25,
  "days_analyzed": 30,
  "current_streak": 7,
  "question_averages": [
    {
      "question_id": 1,
      "question_text": "Rate your day out of 10",
      "average": 7.5,
      "count": 25
    },
    {
      "question_id": 4,
      "question_text": "Productivity level",
      "average": 6.8,
      "count": 25
    }
  ]
}
```

#### Get Current Streak
```http
GET /api/self-reflection/reflections/streak/
```

**Response:**
```json
{
  "current_streak": 7
}
```

**Note:** Streak is calculated as consecutive days from today backwards where the user has submitted a reflection.

#### Bulk Create Reflections
```http
POST /api/self-reflection/reflections/bulk_create/
```

**Request Body:**
```json
[
  {
    "date": "2025-12-01",
    "notes": "Good day",
    "responses": [
      {"question_id": 1, "range_response": 8},
      {"question_id": 2, "choice_response": "Happy"}
    ]
  },
  {
    "date": "2025-12-02",
    "notes": "Great day",
    "responses": [
      {"question_id": 1, "range_response": 9},
      {"question_id": 2, "choice_response": "Excited"}
    ]
  }
]
```

**Response:** Array of created/updated reflections

#### Delete Reflection
```http
DELETE /api/self-reflection/reflections/{id}/
```

---

## Data Models

### ReflectionQuestion
- `id`: Integer (auto-generated)
- `question_text`: String (max 500 chars)
- `question_type`: String (`range`, `choice`, or `text`)
- `min_value`: Integer (for range questions, default: 1)
- `max_value`: Integer (for range questions, default: 10)
- `choices`: Array (for choice questions)
- `is_active`: Boolean (default: true)
- `order`: Integer (display order, default: 0)
- `category`: String (optional, max 100 chars)
- `created_at`: DateTime
- `updated_at`: DateTime

### DailyReflection
- `id`: Integer (auto-generated)
- `user`: Foreign Key to User
- `date`: Date
- `notes`: Text (optional)
- `created_at`: DateTime
- `updated_at`: DateTime

**Constraints:**
- Unique combination of user + date (one reflection per user per day)

### ReflectionResponse
- `id`: Integer (auto-generated)
- `daily_reflection`: Foreign Key to DailyReflection
- `question`: Foreign Key to ReflectionQuestion
- `range_response`: Integer (1-10, for range questions)
- `choice_response`: String (for choice questions)
- `text_response`: Text (for text questions)
- `created_at`: DateTime
- `updated_at`: DateTime

**Constraints:**
- Unique combination of daily_reflection + question (one response per question per reflection)

---

## Example Workflow

### 1. Setup Questions (Admin/Backend)
```bash
# Create questions via API or Django admin
POST /api/self-reflection/questions/
{
  "question_text": "Rate your day out of 10",
  "question_type": "range",
  "min_value": 1,
  "max_value": 10,
  "order": 1,
  "category": "Daily"
}
```

### 2. Frontend Fetches Active Questions
```javascript
// Get all active questions for the reflection form
GET /api/self-reflection/questions/active/
```

### 3. User Submits Daily Reflection
```javascript
POST /api/self-reflection/reflections/
{
  "date": "2025-12-02",
  "notes": "Today was great!",
  "responses": [
    {"question_id": 1, "range_response": 8},
    {"question_id": 2, "choice_response": "Happy"},
    {"question_id": 3, "range_response": 7},
    {"question_id": 4, "range_response": 8}
  ]
}
```

### 4. View Past Reflections
```javascript
// Get all reflections
GET /api/self-reflection/reflections/

// Get specific date
GET /api/self-reflection/reflections/by_date/?date=2025-11-15

// Get date range
GET /api/self-reflection/reflections/date_range/?start_date=2025-11-01&end_date=2025-11-30
```

### 5. View Statistics
```javascript
// Get 30-day stats
GET /api/self-reflection/reflections/stats/?days=30

// Get current streak
GET /api/self-reflection/reflections/streak/
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid date format. Use YYYY-MM-DD"
}
```

### 404 Not Found
```json
{
  "detail": "No reflection found for today.",
  "date": "2025-12-02",
  "has_reflection": false
}
```

### Validation Errors
```json
{
  "responses": [
    {
      "range_response": ["Range response is required for this question."]
    }
  ]
}
```

---

## Frontend Integration Tips

### 1. Dynamic Form Generation
Fetch active questions and generate form inputs based on question type:
```javascript
const questions = await fetch('/api/self-reflection/questions/active/');

questions.forEach(q => {
  if (q.question_type === 'range') {
    // Render slider from min_value to max_value
  } else if (q.question_type === 'choice') {
    // Render dropdown/radio with choices
  } else if (q.question_type === 'text') {
    // Render textarea
  }
});
```

### 2. Check if Reflection Exists for Today
```javascript
try {
  const today = await fetch('/api/self-reflection/reflections/today/');
  // Pre-fill form with existing data
} catch (error) {
  // Show empty form for new reflection
}
```

### 3. Submit Reflection
```javascript
const responses = questions.map(q => {
  const response = { question_id: q.id };
  
  if (q.question_type === 'range') {
    response.range_response = formData[`q_${q.id}`];
  } else if (q.question_type === 'choice') {
    response.choice_response = formData[`q_${q.id}`];
  } else if (q.question_type === 'text') {
    response.text_response = formData[`q_${q.id}`];
  }
  
  return response;
});

await fetch('/api/self-reflection/reflections/', {
  method: 'POST',
  body: JSON.stringify({
    date: new Date().toISOString().split('T')[0],
    notes: formData.notes,
    responses
  })
});
```

### 4. Display Statistics
```javascript
const stats = await fetch('/api/self-reflection/reflections/stats/?days=30');

// Show average scores
stats.question_averages.forEach(qa => {
  console.log(`${qa.question_text}: ${qa.average}/10`);
});

// Show streak
console.log(`Current streak: ${stats.current_streak} days`);
```
