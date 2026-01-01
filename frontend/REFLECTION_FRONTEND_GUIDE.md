# Self-Reflection Frontend Implementation

## Overview
Complete React frontend for the Self-Reflection system with question management, daily reflections, and statistics tracking.

## Files Created

### 1. SelfReflection.jsx
**Location**: `frontend/src/components/SelfReflection/SelfReflection.jsx`

**Features**:
- **Three-View Interface**:
  - Daily Reflection: Form to answer questions and submit reflections
  - Manage Questions: CRUD interface for reflection questions
  - Statistics: Dashboard showing streak, averages, and progress

- **Dynamic Question Rendering**:
  - Range questions: Slider input (1-10 or custom range)
  - Choice questions: Multiple choice buttons
  - Text questions: Textarea input

- **Unsplash Integration**: Random landscape/nature background images

- **State Management**:
  - Questions, responses, notes, stats, and streak tracking
  - Pre-fills existing reflection data for the current day

### 2. SelfReflection.css
**Location**: `frontend/src/components/SelfReflection/SelfReflection.css`

**Design System**:
- **Colors**: 
  - Background: #ECF0F1
  - Primary: #2C3E50
  - Accent: #2980B9
- **Fonts**: Poppins (body), Playfair Display (headings)
- **Class Prefix**: All classes use `reflection-` prefix
- **Responsive**: Mobile-optimized with breakpoints at 768px

### 3. ReflectionPage.jsx
**Location**: `frontend/src/pages/ReflectionPage.jsx`

Simple page wrapper following the existing pattern.

### 4. App.jsx Updates
Added route: `/reflection` → `<ReflectionPage />` (protected route)

## Key Features

### Daily Reflection View
- Displays all active questions in order
- Shows current streak with flame icon
- Dynamic form based on question types
- Optional notes field
- Pre-fills existing reflection data
- Submit/Update button

### Question Management View
- List all questions with type, category, and order badges
- Create new questions with modal form
- Edit existing questions
- Delete questions (with confirmation)
- Support for all three question types
- Choice management (add/remove choices)
- Order and active status control

### Statistics View
- Gradient stat cards:
  - Current streak (flame gradient)
  - Total reflections count
  - Questions tracked
- Question averages section:
  - Progress bars for each range question
  - Average scores out of 10
  - Response counts

## API Integration

**Base URL**: `http://127.0.0.1:8000/api/self-reflection/`

**Endpoints Used**:
- `GET /questions/active/` - Fetch active questions
- `POST /questions/` - Create question
- `PUT /questions/{id}/` - Update question
- `DELETE /questions/{id}/` - Delete question
- `GET /reflections/today/` - Get today's reflection
- `POST /reflections/` - Submit/update reflection
- `GET /reflections/stats/?days=30` - Get statistics
- `GET /reflections/streak/` - Get current streak

**Authentication**: Bearer token from AuthContext

## Usage

### Access the Reflection Page
Navigate to: `http://localhost:5173/reflection`

### Create Questions (First Time Setup)
1. Go to "Manage Questions" tab
2. Click "Add Question"
3. Fill in:
   - Question text
   - Type (range/choice/text)
   - Category (optional)
   - Choices (for choice type)
   - Display order
4. Save question

### Daily Reflection
1. Go to "Daily Reflection" tab
2. Answer all questions
3. Add optional notes
4. Click "Save Reflection"

### View Statistics
1. Go to "Statistics" tab
2. View streak, total reflections, and averages
3. See progress bars for range questions

## Environment Variables

Ensure `.env` file contains:
```
VITE_UNSPLASH_ACCESS_KEY=bWSoyldoD6HT4IVADFKyFkV0EDYWfKVUdWZOy7cDp5A
```

## Responsive Design

- **Desktop**: Full three-column layout for stats
- **Tablet**: Two-column layout
- **Mobile**: Single-column stacked layout
- Tabs switch to vertical on mobile
- Question cards optimize padding/spacing

## Class Naming Convention

All CSS classes use `reflection-` prefix to avoid conflicts:
- `.reflection-container`
- `.reflection-tabs`
- `.reflection-question-card`
- `.reflection-range-slider`
- `.reflection-choice-btn`
- And 100+ more...

## Notes

- Background image loads on component mount
- Reflection data auto-fetches for current date
- Form pre-fills if reflection exists for today
- Statistics show last 30 days by default
- All modals use overlay pattern for consistency
- Edit question pre-fills form with existing data
- Delete confirmation prevents accidental removal
