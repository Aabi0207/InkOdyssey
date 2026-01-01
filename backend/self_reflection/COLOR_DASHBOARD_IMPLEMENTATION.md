# Self-Reflection Color Mapping & Dashboard Implementation Summary

## Overview
Implemented automatic color assignment for self-reflection questions and comprehensive dashboard statistics API endpoints for data visualization.

## Changes Made

### 1. Database Schema Updates

#### New Field: `color_mapping` (JSONField)
Added to `ReflectionQuestion` model to store color assignments:
- **Choice Questions**: Maps each option to a unique color
- **Range Questions**: Maps each value to a heatmap-appropriate gradient color

#### Migration
- Created: `self_reflection/migrations/0002_reflectionquestion_color_mapping.py`
- Applied successfully

### 2. Color System

#### Color Palette (20 Colors)
```python
COLOR_PALETTE = [
    '#3291B6', '#BB8ED0', '#E0A8A8', '#9CC6DB', '#FCF6D9',
    '#CF4B00', '#DDBA7D', '#452829', '#57595B', '#E8D1C5',
    '#778873', '#A1BC98', '#9BB4C0', '#A72703', '#471396',
    '#EB5B00', '#6B3F69', '#86B0BD', '#932F67', '#015551'
]
```
- Used for choice/multiple-choice questions
- No color repetition within a single question
- Automatically cycles if more than 20 options

#### Heatmap Colors (Range Questions)
```python
HEATMAP_COLORS = {
    'low': '#FCF6D9',         # Very light - for low values
    'medium_low': '#E8D1C5',
    'medium': '#DDBA7D',
    'medium_high': '#CF4B00',
    'high': '#A72703'         # Dark - for high values
}
```
- Creates proper gradient for calendar heatmaps
- Values mapped based on position in range (0-100%)

### 3. Model Changes

#### `ReflectionQuestion` Model
**New Methods:**
1. `generate_color_mapping()`: Auto-generates color assignments
2. `save()`: Override to auto-assign colors on creation

**Logic:**
- Choice questions: Each option gets unique color from palette
- Range questions: Values get gradient colors for heatmap visualization
- Automatic assignment on save if `color_mapping` is empty

### 4. New API Endpoints

#### Dashboard Statistics
**Endpoint:** `GET /api/self-reflection/reflections/dashboard_stats/`

**Features:**
- Time-series data for line charts
- Calendar heatmap data
- Distribution statistics
- Supports filtering by days and question_id

**Data Provided:**
- **Range Questions:**
  - Line chart data with daily values
  - Heatmap data with color and intensity
  - Value distribution with percentages
  - Statistics (avg, min, max, count)

- **Choice Questions:**
  - Multi-dataset line chart data
  - Choice distribution with percentages
  - Color-coded datasets

**Query Parameters:**
- `days` (default: 30): Number of days to analyze
- `question_id` (optional): Filter to specific question

#### Enhanced Endpoints
- All question endpoints now include `color_mapping` in responses
- Serializers updated to expose color data

### 5. Management Commands

#### `update_question_colors`
**Usage:** `python manage.py update_question_colors`

**Purpose:**
- Updates existing questions with color mappings
- Useful for migrating old data
- Run after deployment

**Output:**
```
Updated colors for question: Rate your overall day...
Updated colors for question: Productivity of your day...
Successfully updated 4 question(s) with color mappings!
```

### 6. Helper Methods in Views

**Private Methods Added:**
1. `_get_range_line_chart_data()`: Time series for range questions
2. `_get_range_heatmap_data()`: Calendar heatmap data
3. `_get_range_distribution()`: Value distribution statistics
4. `_get_choice_line_chart_data()`: Choice selection over time
5. `_get_choice_distribution()`: Choice occurrence statistics

### 7. Documentation

Created comprehensive documentation:
- **DASHBOARD_API.md**: Complete API reference with examples
- Includes frontend integration examples
- Chart.js usage examples
- Color system explanation

## Files Modified

1. **backend/self_reflection/models.py**
   - Added color constants (COLOR_PALETTE, HEATMAP_COLORS)
   - Added `color_mapping` field
   - Added `generate_color_mapping()` method
   - Override `save()` method

2. **backend/self_reflection/views.py**
   - Added `dashboard_stats` action
   - Added 5 helper methods for data generation
   - Fixed model name bugs (DailyReflection → SelfReflection)

3. **backend/self_reflection/serializers.py**
   - Added `color_mapping` to fields
   - Set as read-only field

4. **backend/self_reflection/migrations/**
   - Created `0002_reflectionquestion_color_mapping.py`

## Files Created

1. **backend/self_reflection/management/commands/update_question_colors.py**
   - Management command for updating colors

2. **backend/self_reflection/DASHBOARD_API.md**
   - Complete API documentation

3. **backend/test_dashboard_api.py**
   - Test script for API endpoints

## Testing

### Manual Testing Completed
✅ Migration created and applied successfully
✅ Management command executed successfully
✅ 4 existing questions updated with colors
✅ No syntax errors in Python files

### To Test (Requires Running Server)
- [ ] Test dashboard_stats endpoint with Postman/curl
- [ ] Verify color assignments in responses
- [ ] Test with different date ranges
- [ ] Test with specific question filtering

## Frontend Integration

### Required Charts/Visualizations

1. **Line Charts** (for both range and choice questions)
   - Use Chart.js, Recharts, or similar
   - Color-coded data points from `color_mapping`

2. **Calendar Heatmap** (for range questions)
   - Use react-calendar-heatmap or similar
   - Colors and intensity provided in API response

3. **Distribution Charts** (pie/bar charts)
   - Show percentage distribution
   - Use colors from `color_mapping`

### Example Frontend Code
```javascript
// Fetch dashboard data
const response = await fetch(
  `${API_URL}/reflections/dashboard_stats/?days=30`,
  {
    headers: { 'Authorization': `Bearer ${token}` }
  }
);
const data = await response.json();

// Use the data
data.questions.forEach(question => {
  if (question.question_type === 'range') {
    renderLineChart(question.line_chart);
    renderHeatmap(question.heatmap);
    renderDistribution(question.distribution);
  } else {
    renderChoiceChart(question.line_chart);
    renderPieChart(question.distribution);
  }
});
```

## API Response Example

```json
{
  "overview": {
    "total_reflections": 25,
    "days_analyzed": 30,
    "current_streak": 5,
    "start_date": "2024-11-03",
    "end_date": "2024-12-03"
  },
  "questions": [
    {
      "question_id": 1,
      "question_text": "Rate your overall day",
      "question_type": "range",
      "category": "Daily",
      "color_mapping": {
        "1": "#FCF6D9",
        "5": "#DDBA7D",
        "10": "#A72703"
      },
      "line_chart": {
        "data": [
          {
            "date": "2024-11-03",
            "value": 7,
            "color": "#CF4B00"
          }
        ],
        "statistics": {
          "average": 7.5,
          "min": 5,
          "max": 10,
          "count": 25
        }
      },
      "heatmap": [...],
      "distribution": {...}
    }
  ]
}
```

## Next Steps

### Backend
1. Start Django server: `python manage.py runserver`
2. Test API endpoints with provided test script
3. Verify data structure matches documentation

### Frontend
1. Create Dashboard component/page
2. Install charting library (Chart.js, Recharts, etc.)
3. Install calendar heatmap library
4. Fetch data from `/dashboard_stats/` endpoint
5. Render visualizations using color mappings

### Recommended Libraries
- **Chart.js**: For line, bar, and pie charts
- **react-calendar-heatmap**: For calendar heatmap
- **recharts**: Alternative modern charting library
- **react-chartjs-2**: React wrapper for Chart.js

## Notes

- Colors are assigned automatically on question creation
- Existing questions can be updated with management command
- Colors persist in database for consistency
- No duplicate colors within same question
- Range questions use gradient colors suitable for heatmaps
- All endpoints include proper authentication checks
- Data includes null values for days without reflections
