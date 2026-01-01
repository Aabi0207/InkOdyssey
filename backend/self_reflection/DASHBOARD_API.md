# Self-Reflection Dashboard API Documentation

## Overview
This document describes the dashboard statistics endpoints that provide data for visualizations including line charts, calendar heatmaps, and distribution charts.

## Color System

### Color Palette (20 Colors for Choice Options)
The system automatically assigns colors to question options from this palette:
```
#3291B6, #BB8ED0, #E0A8A8, #9CC6DB, #FCF6D9,
#CF4B00, #DDBA7D, #452829, #57595B, #E8D1C5,
#778873, #A1BC98, #9BB4C0, #A72703, #471396,
#EB5B00, #6B3F69, #86B0BD, #932F67, #015551
```

### Heatmap Colors (Range Questions)
For range questions, colors are assigned based on value intensity:
- **Low values** (0-20% of range): `#FCF6D9` (Very Light)
- **Medium-Low** (20-40%): `#E8D1C5`
- **Medium** (40-60%): `#DDBA7D`
- **Medium-High** (60-80%): `#CF4B00`
- **High values** (80-100%): `#A72703` (Dark)

## Endpoints

### 1. Get Dashboard Statistics

**Endpoint:** `GET /api/self-reflection/reflections/dashboard_stats/`

**Description:** Get comprehensive statistics for dashboard visualizations including line charts, heatmaps, and distribution data.

**Query Parameters:**
- `days` (optional, default: 30): Number of days to analyze
- `question_id` (optional): Specific question ID to analyze. If not provided, returns data for all active questions.

**Authentication:** Required (Bearer Token)

**Example Request:**
```bash
# Get all questions data for last 30 days
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/self-reflection/reflections/dashboard_stats/

# Get specific question for last 90 days
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/self-reflection/reflections/dashboard_stats/?days=90&question_id=1
```

**Response Structure:**

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
        "2": "#FCF6D9",
        "3": "#E8D1C5",
        "4": "#E8D1C5",
        "5": "#DDBA7D",
        "6": "#DDBA7D",
        "7": "#CF4B00",
        "8": "#CF4B00",
        "9": "#A72703",
        "10": "#A72703"
      },
      "line_chart": {
        "data": [
          {
            "date": "2024-11-03",
            "value": 7,
            "color": "#CF4B00"
          },
          {
            "date": "2024-11-04",
            "value": null,
            "color": null
          }
        ],
        "statistics": {
          "average": 7.5,
          "min": 5,
          "max": 10,
          "count": 25
        }
      },
      "heatmap": [
        {
          "date": "2024-11-03",
          "value": 7,
          "color": "#CF4B00",
          "intensity": 0.67
        }
      ],
      "distribution": {
        "1": {
          "count": 0,
          "percentage": 0,
          "color": "#FCF6D9"
        },
        "2": {
          "count": 1,
          "percentage": 4.0,
          "color": "#FCF6D9"
        }
      }
    },
    {
      "question_id": 2,
      "question_text": "What was your overall mood",
      "question_type": "choice",
      "category": "Wellness",
      "color_mapping": {
        "Happy": "#3291B6",
        "Sad": "#BB8ED0",
        "Neutral": "#E0A8A8",
        "Excited": "#9CC6DB"
      },
      "line_chart": {
        "datasets": [
          {
            "label": "Happy",
            "color": "#3291B6",
            "data": [
              {
                "date": "2024-11-03",
                "selected": true,
                "value": 1
              },
              {
                "date": "2024-11-04",
                "selected": false,
                "value": 0
              }
            ]
          },
          {
            "label": "Sad",
            "color": "#BB8ED0",
            "data": [...]
          }
        ],
        "total_responses": 25
      },
      "distribution": {
        "Happy": {
          "count": 12,
          "percentage": 48.0,
          "color": "#3291B6"
        },
        "Sad": {
          "count": 5,
          "percentage": 20.0,
          "color": "#BB8ED0"
        }
      }
    }
  ]
}
```

### 2. Get Reflection Streak

**Endpoint:** `GET /api/self-reflection/reflections/streak/`

**Description:** Get the user's current streak of consecutive days with reflections.

**Example Response:**
```json
{
  "current_streak": 7
}
```

### 3. Get Basic Stats

**Endpoint:** `GET /api/self-reflection/reflections/stats/`

**Description:** Get basic statistics about user's reflections.

**Query Parameters:**
- `days` (optional, default: 30): Number of days to analyze

**Example Response:**
```json
{
  "total_reflections": 25,
  "days_analyzed": 30,
  "current_streak": 7,
  "question_averages": [
    {
      "question_id": 1,
      "question_text": "Rate your overall day",
      "average": 7.5,
      "count": 25
    }
  ]
}
```

## Data Visualization Usage

### Line Charts (Range Questions)

For range questions, use the `line_chart.data` array to plot values over time:

```javascript
// Example with Chart.js
const lineData = {
  labels: chartData.data.map(d => d.date),
  datasets: [{
    label: question.question_text,
    data: chartData.data.map(d => d.value),
    borderColor: '#3291B6',
    backgroundColor: 'rgba(50, 145, 182, 0.1)',
    pointBackgroundColor: chartData.data.map(d => d.color || '#3291B6')
  }]
};
```

### Line Charts (Choice Questions)

For choice questions, create multiple datasets for each choice:

```javascript
// Example with Chart.js
const lineData = {
  labels: datasets[0].data.map(d => d.date),
  datasets: datasets.map(dataset => ({
    label: dataset.label,
    data: dataset.data.map(d => d.value),
    borderColor: dataset.color,
    backgroundColor: dataset.color + '20'
  }))
};
```

### Calendar Heatmap

Use the `heatmap` array to create a calendar visualization:

```javascript
// Example with a heatmap library
const heatmapData = question.heatmap.map(item => ({
  date: item.date,
  value: item.value,
  color: item.color,
  intensity: item.intensity // 0-1 for opacity/shade variations
}));
```

### Distribution Charts (Pie/Bar Charts)

Use the `distribution` object for pie or bar charts:

```javascript
// Example data transformation
const pieData = {
  labels: Object.keys(distribution),
  datasets: [{
    data: Object.values(distribution).map(d => d.count),
    backgroundColor: Object.values(distribution).map(d => d.color),
    label: 'Responses'
  }]
};
```

## Color Mapping Features

### Automatic Color Assignment

When creating or updating questions:

1. **Choice Questions**: Each choice automatically gets a unique color from the palette
2. **Range Questions**: Each value gets a heatmap-appropriate color based on its position

Example:
```json
POST /api/self-reflection/questions/
{
  "question_text": "How do you feel?",
  "question_type": "choice",
  "choices": ["Happy", "Sad", "Excited"]
}

// Response includes:
{
  "color_mapping": {
    "Happy": "#3291B6",
    "Sad": "#BB8ED0",
    "Excited": "#E0A8A8"
  }
}
```

### Updating Existing Questions

If you need to regenerate color mappings for existing questions:

```bash
python manage.py update_question_colors
```

## Important Notes

1. **No Color Repetition**: Within a single question, colors are never repeated
2. **Consistent Colors**: Once assigned, colors remain consistent for the question
3. **Null Values**: Line chart data includes null values for days without responses
4. **Time Series**: All date-based data is sorted chronologically
5. **Percentages**: Distribution percentages are rounded to 1 decimal place
6. **Intensity**: Heatmap intensity is normalized between 0 and 1

## Frontend Integration Example

```javascript
// Fetch dashboard data
const fetchDashboardData = async (days = 30) => {
  const response = await fetch(
    `${API_URL}/reflections/dashboard_stats/?days=${days}`,
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    }
  );
  return await response.json();
};

// Use the data
const data = await fetchDashboardData(30);

data.questions.forEach(question => {
  if (question.question_type === 'range') {
    // Render line chart and heatmap
    renderLineChart(question.line_chart);
    renderHeatmap(question.heatmap);
    renderDistributionChart(question.distribution);
  } else if (question.question_type === 'choice') {
    // Render multi-line chart or stacked area chart
    renderChoiceLineChart(question.line_chart);
    renderPieChart(question.distribution);
  }
});
```
