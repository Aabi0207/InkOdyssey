# Frontend Integration Quick Start

## Getting Started

This guide will help you integrate the Self-Reflection API into your React frontend.

## Prerequisites

- User must be authenticated (have JWT access token)
- Questions must be created (via Django admin or API)

## Step-by-Step Integration

### 1. Create API Service File

Create `src/services/selfReflectionApi.js`:

```javascript
const API_BASE = 'http://localhost:8000/api/self-reflection';

const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  };
};

export const selfReflectionApi = {
  // Get all active questions
  getActiveQuestions: async () => {
    const response = await fetch(`${API_BASE}/questions/active/`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch questions');
    return response.json();
  },

  // Get today's reflection
  getTodayReflection: async () => {
    const response = await fetch(`${API_BASE}/reflections/today/`, {
      headers: getAuthHeaders()
    });
    if (response.status === 404) return null; // No reflection yet
    if (!response.ok) throw new Error('Failed to fetch reflection');
    return response.json();
  },

  // Create/update reflection
  saveReflection: async (data) => {
    const response = await fetch(`${API_BASE}/reflections/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Failed to save reflection');
    return response.json();
  },

  // Get reflection by date
  getReflectionByDate: async (date) => {
    const response = await fetch(`${API_BASE}/reflections/by_date/?date=${date}`, {
      headers: getAuthHeaders()
    });
    if (response.status === 404) return null;
    if (!response.ok) throw new Error('Failed to fetch reflection');
    return response.json();
  },

  // Get statistics
  getStats: async (days = 30) => {
    const response = await fetch(`${API_BASE}/reflections/stats/?days=${days}`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  },

  // Get current streak
  getStreak: async () => {
    const response = await fetch(`${API_BASE}/reflections/streak/`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch streak');
    return response.json();
  }
};
```

### 2. Create Question Components

#### Range Input Component

```javascript
// src/components/SelfReflection/RangeInput.jsx
import React from 'react';

const RangeInput = ({ question, value, onChange }) => {
  return (
    <div className="range-input">
      <label>{question.question_text}</label>
      <div className="range-control">
        <input
          type="range"
          min={question.min_value}
          max={question.max_value}
          value={value || question.min_value}
          onChange={(e) => onChange(question.id, parseInt(e.target.value))}
        />
        <span className="range-value">{value || question.min_value}</span>
      </div>
    </div>
  );
};

export default RangeInput;
```

#### Choice Input Component

```javascript
// src/components/SelfReflection/ChoiceInput.jsx
import React from 'react';

const ChoiceInput = ({ question, value, onChange }) => {
  return (
    <div className="choice-input">
      <label>{question.question_text}</label>
      <select
        value={value || ''}
        onChange={(e) => onChange(question.id, e.target.value)}
      >
        <option value="">Select an option</option>
        {question.choices.map((choice) => (
          <option key={choice} value={choice}>
            {choice}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ChoiceInput;
```

#### Text Input Component

```javascript
// src/components/SelfReflection/TextInput.jsx
import React from 'react';

const TextInput = ({ question, value, onChange }) => {
  return (
    <div className="text-input">
      <label>{question.question_text}</label>
      <textarea
        value={value || ''}
        onChange={(e) => onChange(question.id, e.target.value)}
        rows="4"
        placeholder="Enter your thoughts..."
      />
    </div>
  );
};

export default TextInput;
```

### 3. Create Main Reflection Form

```javascript
// src/components/SelfReflection/ReflectionForm.jsx
import React, { useState, useEffect } from 'react';
import { selfReflectionApi } from '../../services/selfReflectionApi';
import RangeInput from './RangeInput';
import ChoiceInput from './ChoiceInput';
import TextInput from './TextInput';

const ReflectionForm = () => {
  const [questions, setQuestions] = useState([]);
  const [responses, setResponses] = useState({});
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [existingReflection, setExistingReflection] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      
      // Load questions
      const questionsData = await selfReflectionApi.getActiveQuestions();
      setQuestions(questionsData);
      
      // Try to load today's reflection
      const todayReflection = await selfReflectionApi.getTodayReflection();
      
      if (todayReflection) {
        setExistingReflection(todayReflection);
        setNotes(todayReflection.notes || '');
        
        // Pre-fill responses
        const existingResponses = {};
        todayReflection.responses.forEach(response => {
          const question = questionsData.find(q => q.id === response.question_id);
          if (question) {
            if (question.question_type === 'range') {
              existingResponses[response.question_id] = response.range_response;
            } else if (question.question_type === 'choice') {
              existingResponses[response.question_id] = response.choice_response;
            } else if (question.question_type === 'text') {
              existingResponses[response.question_id] = response.text_response;
            }
          }
        });
        setResponses(existingResponses);
      }
    } catch (error) {
      console.error('Error loading data:', error);
      alert('Failed to load reflection form');
    } finally {
      setLoading(false);
    }
  };

  const handleResponseChange = (questionId, value) => {
    setResponses(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setSaving(true);
      
      // Build responses array
      const responsesArray = questions.map(question => {
        const response = { question_id: question.id };
        const value = responses[question.id];
        
        if (question.question_type === 'range') {
          response.range_response = value || question.min_value;
        } else if (question.question_type === 'choice') {
          if (!value) {
            throw new Error(`Please answer: ${question.question_text}`);
          }
          response.choice_response = value;
        } else if (question.question_type === 'text') {
          response.text_response = value || '';
        }
        
        return response;
      });
      
      // Submit reflection
      const today = new Date().toISOString().split('T')[0];
      const data = {
        date: today,
        notes: notes,
        responses: responsesArray
      };
      
      await selfReflectionApi.saveReflection(data);
      
      alert('Reflection saved successfully!');
    } catch (error) {
      console.error('Error saving reflection:', error);
      alert(error.message || 'Failed to save reflection');
    } finally {
      setSaving(false);
    }
  };

  const renderQuestion = (question) => {
    const value = responses[question.id];
    
    if (question.question_type === 'range') {
      return (
        <RangeInput
          key={question.id}
          question={question}
          value={value}
          onChange={handleResponseChange}
        />
      );
    } else if (question.question_type === 'choice') {
      return (
        <ChoiceInput
          key={question.id}
          question={question}
          value={value}
          onChange={handleResponseChange}
        />
      );
    } else if (question.question_type === 'text') {
      return (
        <TextInput
          key={question.id}
          question={question}
          value={value}
          onChange={handleResponseChange}
        />
      );
    }
  };

  if (loading) {
    return <div className="loading">Loading reflection form...</div>;
  }

  return (
    <div className="reflection-form-container">
      <h2>
        {existingReflection ? "Today's Reflection" : "Daily Reflection"}
      </h2>
      
      <form onSubmit={handleSubmit} className="reflection-form">
        {questions.map(renderQuestion)}
        
        <div className="notes-section">
          <label>Additional Notes (Optional)</label>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            rows="4"
            placeholder="Any additional thoughts for today..."
          />
        </div>
        
        <button type="submit" disabled={saving}>
          {saving ? 'Saving...' : existingReflection ? 'Update Reflection' : 'Save Reflection'}
        </button>
      </form>
    </div>
  );
};

export default ReflectionForm;
```

### 4. Create Statistics Dashboard

```javascript
// src/components/SelfReflection/StatsDashboard.jsx
import React, { useState, useEffect } from 'react';
import { selfReflectionApi } from '../../services/selfReflectionApi';

const StatsDashboard = () => {
  const [stats, setStats] = useState(null);
  const [streak, setStreak] = useState(0);
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(30);

  useEffect(() => {
    loadStats();
  }, [days]);

  const loadStats = async () => {
    try {
      setLoading(true);
      const [statsData, streakData] = await Promise.all([
        selfReflectionApi.getStats(days),
        selfReflectionApi.getStreak()
      ]);
      setStats(statsData);
      setStreak(streakData.current_streak);
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading statistics...</div>;
  }

  return (
    <div className="stats-dashboard">
      <h2>Your Reflection Statistics</h2>
      
      <div className="stats-cards">
        <div className="stat-card">
          <h3>Current Streak</h3>
          <p className="stat-value">{streak} days</p>
        </div>
        
        <div className="stat-card">
          <h3>Total Reflections</h3>
          <p className="stat-value">{stats.total_reflections}</p>
          <p className="stat-subtitle">in last {stats.days_analyzed} days</p>
        </div>
      </div>
      
      <div className="averages-section">
        <h3>Question Averages</h3>
        {stats.question_averages.map(qa => (
          <div key={qa.question_id} className="average-item">
            <span className="question-text">{qa.question_text}</span>
            <span className="average-value">{qa.average} / 10</span>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${(qa.average / 10) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
      
      <div className="time-range-selector">
        <label>Time Range:</label>
        <select value={days} onChange={(e) => setDays(parseInt(e.target.value))}>
          <option value="7">Last 7 days</option>
          <option value="30">Last 30 days</option>
          <option value="90">Last 90 days</option>
        </select>
      </div>
    </div>
  );
};

export default StatsDashboard;
```

### 5. Create Reflection History View

```javascript
// src/components/SelfReflection/ReflectionHistory.jsx
import React, { useState, useEffect } from 'react';
import { selfReflectionApi } from '../../services/selfReflectionApi';

const ReflectionHistory = () => {
  const [selectedDate, setSelectedDate] = useState('');
  const [reflection, setReflection] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleDateChange = async (date) => {
    setSelectedDate(date);
    if (!date) {
      setReflection(null);
      return;
    }
    
    try {
      setLoading(true);
      const data = await selfReflectionApi.getReflectionByDate(date);
      setReflection(data);
    } catch (error) {
      console.error('Error loading reflection:', error);
      setReflection(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="reflection-history">
      <h2>Reflection History</h2>
      
      <div className="date-selector">
        <label>Select Date:</label>
        <input
          type="date"
          value={selectedDate}
          onChange={(e) => handleDateChange(e.target.value)}
          max={new Date().toISOString().split('T')[0]}
        />
      </div>
      
      {loading && <div className="loading">Loading...</div>}
      
      {reflection ? (
        <div className="reflection-display">
          <h3>{new Date(reflection.date).toLocaleDateString()}</h3>
          
          <div className="responses">
            {reflection.responses.map(response => (
              <div key={response.id} className="response-item">
                <h4>{response.question_text}</h4>
                <p>
                  {response.range_response && `${response.range_response}/10`}
                  {response.choice_response}
                  {response.text_response}
                </p>
              </div>
            ))}
          </div>
          
          {reflection.notes && (
            <div className="notes">
              <h4>Notes</h4>
              <p>{reflection.notes}</p>
            </div>
          )}
        </div>
      ) : selectedDate ? (
        <div className="no-reflection">
          No reflection found for {selectedDate}
        </div>
      ) : null}
    </div>
  );
};

export default ReflectionHistory;
```

### 6. Add Routes

```javascript
// In your main App.jsx or router configuration
import ReflectionForm from './components/SelfReflection/ReflectionForm';
import StatsDashboard from './components/SelfReflection/StatsDashboard';
import ReflectionHistory from './components/SelfReflection/ReflectionHistory';

// Add routes
<Route path="/reflection" element={<ReflectionForm />} />
<Route path="/reflection/stats" element={<StatsDashboard />} />
<Route path="/reflection/history" element={<ReflectionHistory />} />
```

## Basic Styling

Create `src/components/SelfReflection/SelfReflection.css`:

```css
.reflection-form-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.reflection-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.range-input, .choice-input, .text-input {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.range-control {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.range-control input[type="range"] {
  flex: 1;
}

.range-value {
  font-weight: bold;
  min-width: 30px;
}

.notes-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stats-dashboard {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.stat-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: #2980b9;
}

.averages-section {
  margin-top: 2rem;
}

.average-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #2980b9;
  transition: width 0.3s;
}
```

## Quick Test Checklist

1. ✅ Questions load correctly
2. ✅ Form renders all question types
3. ✅ Existing reflections pre-fill the form
4. ✅ Form submission works
5. ✅ Statistics display correctly
6. ✅ Streak calculation works
7. ✅ History view shows past reflections

## Common Issues & Solutions

### Issue: Questions not loading
**Solution:** Check that questions are created in Django admin and marked as active

### Issue: Authentication errors
**Solution:** Verify JWT token is stored and included in headers

### Issue: Date format errors
**Solution:** Use `YYYY-MM-DD` format for all date parameters

### Issue: Validation errors
**Solution:** Ensure all required responses are provided and match question types

## Next Steps

1. Add loading states and error handling
2. Implement better form validation
3. Add calendar view for history
4. Create charts for statistics
5. Add reminder notifications
6. Implement data export

## Resources

- Full API Documentation: `backend/self_reflection/API_DOCUMENTATION.md`
- Backend README: `backend/self_reflection/README.md`
- Test Script: `backend/test_self_reflection_api.py`

## Support

If you encounter issues:
1. Check browser console for errors
2. Verify API responses in Network tab
3. Check Django server logs
4. Review API documentation for correct request format
