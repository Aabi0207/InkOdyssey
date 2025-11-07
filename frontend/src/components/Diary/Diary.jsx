import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import './Diary.css';

const API_BASE_URL = 'http://localhost:8000/api/diary';

const Diary = () => {
  const { accessToken, logout } = useAuth();
  const [entries, setEntries] = useState([]);
  const [selectedEntry, setSelectedEntry] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [selectedDate, setSelectedDate] = useState('');
  const [view, setView] = useState('list'); // 'list', 'detail', 'create', 'edit'
  
  // Form state
  const [formData, setFormData] = useState({
    title: '',
    content_blocks: []
  });

  // Fetch all entries
  const fetchEntries = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/entries/`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setEntries(data.results || data);
      } else if (response.status === 401) {
        logout();
      }
    } catch (error) {
      console.error('Error fetching entries:', error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch entry by ID
  const fetchEntryById = async (id) => {
    try {
      const response = await fetch(`${API_BASE_URL}/entries/${id}/`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setSelectedEntry(data);
        setView('detail');
      }
    } catch (error) {
      console.error('Error fetching entry:', error);
    }
  };

  // Fetch statistics
  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/stats/`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  // Create new entry
  const createEntry = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/entries/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        const data = await response.json();
        setEntries([data, ...entries]);
        resetForm();
        setView('list');
        fetchStats();
      }
    } catch (error) {
      console.error('Error creating entry:', error);
    }
  };

  // Update entry
  const updateEntry = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/entries/${selectedEntry.id}/`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        const data = await response.json();
        setEntries(entries.map(entry => entry.id === data.id ? data : entry));
        setSelectedEntry(data);
        setIsEditing(false);
        setView('detail');
      }
    } catch (error) {
      console.error('Error updating entry:', error);
    }
  };

  // Delete entry
  const deleteEntry = async (id) => {
    if (!window.confirm('Are you sure you want to delete this entry?')) return;
    
    try {
      const response = await fetch(`${API_BASE_URL}/entries/${id}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      
      if (response.ok) {
        setEntries(entries.filter(entry => entry.id !== id));
        setSelectedEntry(null);
        setView('list');
        fetchStats();
      }
    } catch (error) {
      console.error('Error deleting entry:', error);
    }
  };

  // Fetch entries by date
  const fetchEntriesByDate = async (date) => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/entries/by-date/?date=${date}`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setEntries(data);
      }
    } catch (error) {
      console.error('Error fetching entries by date:', error);
    } finally {
      setLoading(false);
    }
  };

  // Handle date filter
  const handleDateFilter = (e) => {
    const date = e.target.value;
    setSelectedDate(date);
    if (date) {
      fetchEntriesByDate(date);
    } else {
      fetchEntries();
    }
  };

  // Add content block
  const addContentBlock = (type) => {
    const newBlock = {
      block_type: type,
      order: formData.content_blocks.length,
      text_content: type === 'text' ? '' : null,
      media_url: type !== 'text' ? '' : null,
      caption: ''
    };
    setFormData({
      ...formData,
      content_blocks: [...formData.content_blocks, newBlock]
    });
  };

  // Update content block
  const updateContentBlock = (index, field, value) => {
    const updatedBlocks = [...formData.content_blocks];
    updatedBlocks[index][field] = value;
    setFormData({
      ...formData,
      content_blocks: updatedBlocks
    });
  };

  // Remove content block
  const removeContentBlock = (index) => {
    const updatedBlocks = formData.content_blocks.filter((_, i) => i !== index);
    // Reorder remaining blocks
    updatedBlocks.forEach((block, i) => {
      block.order = i;
    });
    setFormData({
      ...formData,
      content_blocks: updatedBlocks
    });
  };

  // Move content block
  const moveContentBlock = (index, direction) => {
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    if (newIndex < 0 || newIndex >= formData.content_blocks.length) return;
    
    const updatedBlocks = [...formData.content_blocks];
    [updatedBlocks[index], updatedBlocks[newIndex]] = [updatedBlocks[newIndex], updatedBlocks[index]];
    
    // Update order values
    updatedBlocks.forEach((block, i) => {
      block.order = i;
    });
    
    setFormData({
      ...formData,
      content_blocks: updatedBlocks
    });
  };

  // Reset form
  const resetForm = () => {
    setFormData({
      title: '',
      content_blocks: []
    });
    setIsCreating(false);
    setIsEditing(false);
    setSelectedEntry(null);
  };

  // Start editing
  const startEditing = (entry) => {
    setFormData({
      title: entry.title,
      content_blocks: entry.content_blocks.map(block => ({
        block_type: block.block_type,
        order: block.order,
        text_content: block.text_content || '',
        media_url: block.media_url || '',
        caption: block.caption || ''
      }))
    });
    setSelectedEntry(entry);
    setIsEditing(true);
    setView('edit');
  };

  // Format date
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  useEffect(() => {
    fetchEntries();
    fetchStats();
  }, []);

  if (loading && entries.length === 0) {
    return (
      <div className="diary-container">
        <div className="loading">Loading your diary...</div>
      </div>
    );
  }

  return (
    <div className="diary-container">
      {/* Header */}
      <header className="diary-header">
        <div className="header-content">
          <h1>📖 My Diary</h1>
          <button onClick={logout} className="btn btn-secondary">Logout</button>
        </div>
      </header>

      {/* Statistics Dashboard */}
      {stats && view === 'list' && (
        <div className="stats-dashboard">
          <div className="stat-card">
            <div className="stat-value">{stats.total_entries}</div>
            <div className="stat-label">Total Entries</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.entries_this_week}</div>
            <div className="stat-label">This Week</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.entries_this_month}</div>
            <div className="stat-label">This Month</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.total_blocks}</div>
            <div className="stat-label">Content Blocks</div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="diary-main">
        {/* List View */}
        {view === 'list' && (
          <>
            <div className="diary-actions">
              <button 
                onClick={() => {
                  resetForm();
                  setView('create');
                }} 
                className="btn btn-primary"
              >
                ✏️ New Entry
              </button>
              <div className="date-filter">
                <label htmlFor="date-filter">Filter by date:</label>
                <input
                  id="date-filter"
                  type="date"
                  value={selectedDate}
                  onChange={handleDateFilter}
                  className="date-input"
                />
                {selectedDate && (
                  <button 
                    onClick={() => {
                      setSelectedDate('');
                      fetchEntries();
                    }}
                    className="btn btn-secondary btn-sm"
                  >
                    Clear
                  </button>
                )}
              </div>
            </div>

            <div className="entries-list">
              {entries.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-icon">📝</div>
                  <h3>No entries yet</h3>
                  <p>Start writing your first diary entry!</p>
                  <button 
                    onClick={() => {
                      resetForm();
                      setView('create');
                    }} 
                    className="btn btn-primary"
                  >
                    Create Entry
                  </button>
                </div>
              ) : (
                entries.map(entry => (
                  <div 
                    key={entry.id} 
                    className="entry-card"
                    onClick={() => fetchEntryById(entry.id)}
                  >
                    <div className="entry-header">
                      <h3>{entry.title}</h3>
                      <span className="entry-date">{formatDate(entry.created_at)}</span>
                    </div>
                    <div className="entry-meta">
                      <span className="block-count">
                        {entry.content_blocks_count || 0} blocks
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </>
        )}

        {/* Detail View */}
        {view === 'detail' && selectedEntry && (
          <div className="entry-detail">
            <button 
              onClick={() => setView('list')} 
              className="btn btn-secondary btn-back"
            >
              ← Back
            </button>
            
            <div className="entry-detail-header">
              <h2>{selectedEntry.title}</h2>
              <div className="entry-actions">
                <button 
                  onClick={() => startEditing(selectedEntry)} 
                  className="btn btn-primary"
                >
                  ✏️ Edit
                </button>
                <button 
                  onClick={() => deleteEntry(selectedEntry.id)} 
                  className="btn btn-danger"
                >
                  🗑️ Delete
                </button>
              </div>
            </div>
            
            <div className="entry-metadata">
              <span>Created: {formatDate(selectedEntry.created_at)}</span>
              {selectedEntry.updated_at !== selectedEntry.created_at && (
                <span>Updated: {formatDate(selectedEntry.updated_at)}</span>
              )}
            </div>

            <div className="content-blocks">
              {selectedEntry.content_blocks && selectedEntry.content_blocks.length > 0 ? (
                selectedEntry.content_blocks.map((block, index) => (
                  <div key={index} className={`content-block block-${block.block_type}`}>
                    {block.block_type === 'text' && (
                      <p className="block-text">{block.text_content}</p>
                    )}
                    {block.block_type === 'image' && (
                      <div className="block-media">
                        {block.media_url && (
                          <img src={block.media_url} alt={block.caption || 'Image'} />
                        )}
                        {block.caption && <p className="block-caption">{block.caption}</p>}
                      </div>
                    )}
                    {block.block_type === 'video' && (
                      <div className="block-media">
                        {block.media_url && (
                          <video controls>
                            <source src={block.media_url} />
                            Your browser does not support the video tag.
                          </video>
                        )}
                        {block.caption && <p className="block-caption">{block.caption}</p>}
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <p className="no-content">No content blocks</p>
              )}
            </div>
          </div>
        )}

        {/* Create/Edit Form */}
        {(view === 'create' || view === 'edit') && (
          <div className="entry-form">
            <button 
              onClick={() => {
                resetForm();
                setView('list');
              }} 
              className="btn btn-secondary btn-back"
            >
              ← Cancel
            </button>

            <h2>{view === 'create' ? 'Create New Entry' : 'Edit Entry'}</h2>

            <form onSubmit={view === 'create' ? createEntry : updateEntry}>
              <div className="form-group">
                <label htmlFor="title">Entry Title</label>
                <input
                  id="title"
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="Give your entry a title..."
                  required
                  className="form-control"
                />
              </div>

              <div className="content-blocks-section">
                <div className="section-header">
                  <h3>Content Blocks</h3>
                  <div className="block-buttons">
                    <button 
                      type="button" 
                      onClick={() => addContentBlock('text')}
                      className="btn btn-sm btn-outline"
                    >
                      📝 Text
                    </button>
                    <button 
                      type="button" 
                      onClick={() => addContentBlock('image')}
                      className="btn btn-sm btn-outline"
                    >
                      🖼️ Image
                    </button>
                    <button 
                      type="button" 
                      onClick={() => addContentBlock('video')}
                      className="btn btn-sm btn-outline"
                    >
                      🎥 Video
                    </button>
                  </div>
                </div>

                {formData.content_blocks.length === 0 ? (
                  <p className="no-blocks-message">
                    Add content blocks to your entry using the buttons above.
                  </p>
                ) : (
                  <div className="blocks-editor">
                    {formData.content_blocks.map((block, index) => (
                      <div key={index} className="block-editor">
                        <div className="block-editor-header">
                          <span className="block-type-badge">{block.block_type}</span>
                          <div className="block-controls">
                            <button
                              type="button"
                              onClick={() => moveContentBlock(index, 'up')}
                              disabled={index === 0}
                              className="btn btn-icon"
                              title="Move up"
                            >
                              ▲
                            </button>
                            <button
                              type="button"
                              onClick={() => moveContentBlock(index, 'down')}
                              disabled={index === formData.content_blocks.length - 1}
                              className="btn btn-icon"
                              title="Move down"
                            >
                              ▼
                            </button>
                            <button
                              type="button"
                              onClick={() => removeContentBlock(index)}
                              className="btn btn-icon btn-remove"
                              title="Remove block"
                            >
                              ✕
                            </button>
                          </div>
                        </div>

                        {block.block_type === 'text' && (
                          <textarea
                            value={block.text_content}
                            onChange={(e) => updateContentBlock(index, 'text_content', e.target.value)}
                            placeholder="Write your thoughts here..."
                            rows="4"
                            className="form-control"
                            required
                          />
                        )}

                        {(block.block_type === 'image' || block.block_type === 'video') && (
                          <>
                            <input
                              type="url"
                              value={block.media_url}
                              onChange={(e) => updateContentBlock(index, 'media_url', e.target.value)}
                              placeholder={`Enter ${block.block_type} URL...`}
                              className="form-control"
                              required
                            />
                            <input
                              type="text"
                              value={block.caption}
                              onChange={(e) => updateContentBlock(index, 'caption', e.target.value)}
                              placeholder="Add a caption (optional)..."
                              className="form-control"
                            />
                          </>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="form-actions">
                <button type="submit" className="btn btn-primary btn-lg">
                  {view === 'create' ? '📝 Create Entry' : '💾 Save Changes'}
                </button>
                <button 
                  type="button" 
                  onClick={() => {
                    resetForm();
                    setView('list');
                  }}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default Diary;
