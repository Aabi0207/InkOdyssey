import React, { useState, useEffect } from 'react';
import { Plus, Trash2, TrendingUp, Calendar, Heart, Smile } from 'lucide-react';
import './Dashboard.css';

const API_BASE_URL = 'http://localhost:8000/api/tracker';

const Dashboard = () => {
  const [habits, setHabits] = useState([]);
  const [todayLogs, setTodayLogs] = useState([]);
  const [todayReflection, setTodayReflection] = useState(null);
  const [showAddHabit, setShowAddHabit] = useState(false);
  const [showReflection, setShowReflection] = useState(false);
  const [loading, setLoading] = useState(true);

  // New habit form
  const [newHabit, setNewHabit] = useState({
    name: '',
    description: '',
    frequency: 'daily',
    tracking_type: 'boolean',
    target_value: 1,
    color: '#2980B9',
    icon: ''
  });

  // Reflection form
  const [reflection, setReflection] = useState({
    day_rating: 5,
    mood: 'okay',
    mood_intensity: 5,
    notes: '',
    gratitude: ''
  });

  const moodOptions = [
    { value: 'terrible', label: 'Terrible', emoji: '😞' },
    { value: 'bad', label: 'Bad', emoji: '😕' },
    { value: 'okay', label: 'Okay', emoji: '😐' },
    { value: 'good', label: 'Good', emoji: '🙂' },
    { value: 'excellent', label: 'Excellent', emoji: '😊' },
    { value: 'peak', label: 'Peak', emoji: '🤩' }
  ];

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      await Promise.all([
        fetchHabits(),
        fetchTodayLogs(),
        fetchTodayReflection()
      ]);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchHabits = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/habits/active/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const data = await response.json();
        setHabits(data);
      }
    } catch (error) {
      console.error('Error fetching habits:', error);
    }
  };

  const fetchTodayLogs = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/logs/today/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const data = await response.json();
        setTodayLogs(data);
      }
    } catch (error) {
      console.error('Error fetching today logs:', error);
    }
  };

  const fetchTodayReflection = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/reflections/today/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const data = await response.json();
        setTodayReflection(data);
        setReflection({
          day_rating: data.day_rating,
          mood: data.mood,
          mood_intensity: data.mood_intensity,
          notes: data.notes,
          gratitude: data.gratitude
        });
      }
    } catch (error) {
      // No reflection for today yet
      setTodayReflection(null);
    }
  };

  const handleAddHabit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/habits/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newHabit)
      });
      
      if (response.ok) {
        setNewHabit({
          name: '',
          description: '',
          frequency: 'daily',
          tracking_type: 'boolean',
          target_value: 1,
          color: '#2980B9',
          icon: ''
        });
        setShowAddHabit(false);
        fetchHabits();
      } else {
        alert('Failed to add habit');
      }
    } catch (error) {
      console.error('Error adding habit:', error);
      alert('Failed to add habit');
    }
  };

  const handleDeleteHabit = async (habitId) => {
    if (!confirm('Are you sure you want to delete this habit?')) return;
    
    try {
      const response = await fetch(`${API_BASE_URL}/habits/${habitId}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        fetchHabits();
        fetchTodayLogs();
      } else {
        alert('Failed to delete habit');
      }
    } catch (error) {
      console.error('Error deleting habit:', error);
      alert('Failed to delete habit');
    }
  };

  const handleLogHabit = async (habitId, value = 1) => {
    try {
      const response = await fetch(`${API_BASE_URL}/logs/log_habit/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          habit_id: habitId,
          value: value
        })
      });
      
      if (response.ok) {
        fetchTodayLogs();
      } else {
        alert('Failed to log habit');
      }
    } catch (error) {
      console.error('Error logging habit:', error);
      alert('Failed to log habit');
    }
  };

  const handleSaveReflection = async (e) => {
    e.preventDefault();
    try {
      const today = new Date().toISOString().split('T')[0];
      const payload = todayReflection 
        ? reflection 
        : { ...reflection, date: today };
      
      const url = todayReflection 
        ? `${API_BASE_URL}/reflections/${todayReflection.id}/`
        : `${API_BASE_URL}/reflections/`;
      
      const method = todayReflection ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method: method,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });
      
      if (response.ok) {
        setShowReflection(false);
        fetchTodayReflection();
      } else {
        alert('Failed to save reflection');
      }
    } catch (error) {
      console.error('Error saving reflection:', error);
      alert('Failed to save reflection');
    }
  };

  const getHabitLog = (habitId) => {
    return todayLogs.find(log => log.habit === habitId);
  };

  const getCompletionPercentage = (habit) => {
    const log = getHabitLog(habit.id);
    if (!log) return 0;
    if (habit.tracking_type === 'boolean') {
      return log.completed ? 100 : 0;
    }
    return Math.min((log.value / habit.target_value) * 100, 100);
  };

  if (loading) {
    return <div className="dashboard-loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-container">
        <header className="dashboard-header">
          <h1>Dashboard</h1>
          <p className="dashboard-date">{new Date().toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          })}</p>
        </header>

        {/* Daily Reflection Section */}
        <section className="reflection-section">
          <div className="section-header">
            <h2><Heart size={20} /> Daily Reflection</h2>
            <button 
              className="btn-primary"
              onClick={() => setShowReflection(!showReflection)}
            >
              {todayReflection ? 'Edit Reflection' : 'Add Reflection'}
            </button>
          </div>

          {todayReflection && !showReflection && (
            <div className="reflection-summary">
              <div className="reflection-item">
                <span className="reflection-label">Day Rating:</span>
                <span className="reflection-value">{todayReflection.day_rating}/10</span>
              </div>
              <div className="reflection-item">
                <span className="reflection-label">Mood:</span>
                <span className="reflection-value">
                  {moodOptions.find(m => m.value === todayReflection.mood)?.emoji} {todayReflection.mood}
                  <span className="mood-intensity"> (Intensity: {todayReflection.mood_intensity}/10)</span>
                </span>
              </div>
              {todayReflection.gratitude && (
                <div className="reflection-item">
                  <span className="reflection-label">Grateful for:</span>
                  <span className="reflection-value">{todayReflection.gratitude}</span>
                </div>
              )}
            </div>
          )}

          {showReflection && (
            <form className="reflection-form" onSubmit={handleSaveReflection}>
              <div className="form-group">
                <label>How was your day? (1-10)</label>
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={reflection.day_rating}
                  onChange={(e) => setReflection({...reflection, day_rating: parseInt(e.target.value)})}
                  required
                />
                <span className="range-value">{reflection.day_rating}</span>
              </div>

              <div className="form-group">
                <label>Overall Mood</label>
                <div className="mood-selector">
                  {moodOptions.map(mood => (
                    <button
                      key={mood.value}
                      type="button"
                      className={`mood-option ${reflection.mood === mood.value ? 'selected' : ''}`}
                      onClick={() => setReflection({...reflection, mood: mood.value})}
                    >
                      <span className="mood-emoji">{mood.emoji}</span>
                      <span className="mood-label">{mood.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              <div className="form-group">
                <label>Mood Intensity (1-10)</label>
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={reflection.mood_intensity}
                  onChange={(e) => setReflection({...reflection, mood_intensity: parseInt(e.target.value)})}
                  required
                />
                <span className="range-value">{reflection.mood_intensity}</span>
              </div>

              <div className="form-group">
                <label>What are you grateful for today?</label>
                <textarea
                  value={reflection.gratitude}
                  onChange={(e) => setReflection({...reflection, gratitude: e.target.value})}
                  placeholder="Write something you're grateful for..."
                  rows="3"
                />
              </div>

              <div className="form-group">
                <label>Additional Notes (Optional)</label>
                <textarea
                  value={reflection.notes}
                  onChange={(e) => setReflection({...reflection, notes: e.target.value})}
                  placeholder="Any additional thoughts..."
                  rows="3"
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-primary">Save Reflection</button>
                <button 
                  type="button" 
                  className="btn-secondary"
                  onClick={() => setShowReflection(false)}
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
        </section>

        {/* Habits Section */}
        <section className="habits-section">
          <div className="section-header">
            <h2><TrendingUp size={20} /> Habit Tracker</h2>
            <button 
              className="btn-primary"
              onClick={() => setShowAddHabit(!showAddHabit)}
            >
              <Plus size={18} /> Add Habit
            </button>
          </div>

          {showAddHabit && (
            <form className="add-habit-form" onSubmit={handleAddHabit}>
              <div className="form-row">
                <div className="form-group">
                  <label>Habit Name*</label>
                  <input
                    type="text"
                    value={newHabit.name}
                    onChange={(e) => setNewHabit({...newHabit, name: e.target.value})}
                    placeholder="e.g., Drink water"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Tracking Type</label>
                  <select
                    value={newHabit.tracking_type}
                    onChange={(e) => setNewHabit({
                      ...newHabit, 
                      tracking_type: e.target.value,
                      target_value: e.target.value === 'boolean' ? 1 : newHabit.target_value
                    })}
                  >
                    <option value="boolean">Yes/No (One-time)</option>
                    <option value="counter">Counter (Multiple times)</option>
                  </select>
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Frequency</label>
                  <select
                    value={newHabit.frequency}
                    onChange={(e) => setNewHabit({...newHabit, frequency: e.target.value})}
                  >
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="custom">Custom</option>
                  </select>
                </div>

                {newHabit.tracking_type === 'counter' && (
                  <div className="form-group">
                    <label>Target Value</label>
                    <input
                      type="number"
                      min="1"
                      value={newHabit.target_value}
                      onChange={(e) => setNewHabit({...newHabit, target_value: parseInt(e.target.value)})}
                      placeholder="e.g., 8 glasses"
                      required
                    />
                  </div>
                )}

                <div className="form-group">
                  <label>Color</label>
                  <input
                    type="color"
                    value={newHabit.color}
                    onChange={(e) => setNewHabit({...newHabit, color: e.target.value})}
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Description (Optional)</label>
                <textarea
                  value={newHabit.description}
                  onChange={(e) => setNewHabit({...newHabit, description: e.target.value})}
                  placeholder="Add a description..."
                  rows="2"
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-primary">Add Habit</button>
                <button 
                  type="button" 
                  className="btn-secondary"
                  onClick={() => setShowAddHabit(false)}
                >
                  Cancel
                </button>
              </div>
            </form>
          )}

          {habits.length === 0 ? (
            <div className="empty-state">
              <p>No habits yet. Start by adding your first habit!</p>
            </div>
          ) : (
            <div className="habits-grid">
              {habits.map(habit => {
                const log = getHabitLog(habit.id);
                const percentage = getCompletionPercentage(habit);
                
                return (
                  <div key={habit.id} className="habit-card">
                    <div className="habit-header">
                      <div className="habit-info">
                        <div 
                          className="habit-color" 
                          style={{ backgroundColor: habit.color }}
                        />
                        <div>
                          <h3>{habit.name}</h3>
                          {habit.description && (
                            <p className="habit-description">{habit.description}</p>
                          )}
                        </div>
                      </div>
                      <button
                        className="btn-icon"
                        onClick={() => handleDeleteHabit(habit.id)}
                        title="Delete habit"
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>

                    <div className="habit-progress">
                      <div className="progress-bar">
                        <div 
                          className="progress-fill" 
                          style={{ 
                            width: `${percentage}%`,
                            backgroundColor: habit.color
                          }}
                        />
                      </div>
                      <span className="progress-text">
                        {habit.tracking_type === 'counter' 
                          ? `${log?.value || 0} / ${habit.target_value}`
                          : log?.completed ? '✓ Completed' : 'Not done'
                        }
                      </span>
                    </div>

                    <div className="habit-actions">
                      {habit.tracking_type === 'boolean' ? (
                        <button
                          className={`btn-log ${log?.completed ? 'completed' : ''}`}
                          onClick={() => handleLogHabit(habit.id, 1)}
                          disabled={log?.completed}
                        >
                          {log?.completed ? 'Done Today' : 'Mark as Done'}
                        </button>
                      ) : (
                        <div className="counter-controls">
                          <button
                            className="btn-counter"
                            onClick={() => handleLogHabit(habit.id, 1)}
                          >
                            +1
                          </button>
                          <button
                            className="btn-counter"
                            onClick={() => handleLogHabit(habit.id, -1)}
                          >
                            -1
                          </button>
                        </div>
                      )}
                    </div>

                    {habit.current_streak > 0 && (
                      <div className="habit-streak">
                        🔥 {habit.current_streak} day streak
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
