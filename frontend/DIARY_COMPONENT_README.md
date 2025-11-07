# Diary Component - Frontend Documentation

## Overview
A comprehensive, modern diary application component built with React. Features a beautiful gradient UI with full CRUD functionality for managing personal diary entries.

## Features

### 📊 Dashboard Statistics
- Total entries count
- Entries this week
- Entries this month
- Total content blocks

### 📝 Entry Management
- **Create**: Add new diary entries with multiple content blocks
- **Read**: View all entries in a beautiful card layout
- **Update**: Edit existing entries and their content
- **Delete**: Remove entries with confirmation

### 🎨 Content Blocks
Support for three types of content blocks:
1. **Text Blocks**: Rich text content for your thoughts
2. **Image Blocks**: Add images with captions via URL
3. **Video Blocks**: Embed videos with captions via URL

### 🔍 Filtering & Search
- Filter entries by specific date
- View all entries for a particular day
- Clear filters to see all entries

### ✨ User Experience
- Smooth animations and transitions
- Responsive design (mobile, tablet, desktop)
- Loading states
- Empty states with helpful prompts
- Confirmation dialogs for destructive actions

## Component Structure

```
components/Diary/
├── Diary.jsx       # Main component with all functionality
└── Diary.css       # Comprehensive styling
```

## Usage

### Route Configuration
The diary component is available at `/diary` route and is protected (requires authentication).

```jsx
<Route path="/diary" element={<ProtectedRoute><DiaryPage /></ProtectedRoute>} />
```

### Creating an Entry

1. Click "New Entry" button
2. Enter a title
3. Add content blocks:
   - Click "📝 Text" for text blocks
   - Click "🖼️ Image" for image blocks
   - Click "🎥 Video" for video blocks
4. Fill in the content for each block
5. Reorder blocks using ▲ ▼ buttons
6. Remove unwanted blocks with ✕ button
7. Click "Create Entry" to save

### Viewing Entries

- All entries are displayed as cards on the main page
- Click any entry card to view full details
- Entry cards show:
  - Title
  - Creation date/time
  - Number of content blocks

### Editing an Entry

1. Click on an entry to view details
2. Click "✏️ Edit" button
3. Modify title and content blocks
4. Add, remove, or reorder blocks
5. Click "Save Changes"

### Deleting an Entry

1. Click on an entry to view details
2. Click "🗑️ Delete" button
3. Confirm deletion in the popup

### Filtering by Date

1. Use the date picker in the top bar
2. Select a date to see all entries from that day
3. Click "Clear" to remove the filter

## API Integration

The component connects to the following backend endpoints:

- `GET /api/diary/entries/` - List all entries
- `POST /api/diary/entries/` - Create new entry
- `GET /api/diary/entries/{id}/` - Get specific entry
- `PATCH /api/diary/entries/{id}/` - Update entry
- `DELETE /api/diary/entries/{id}/` - Delete entry
- `GET /api/diary/entries/by-date/?date=YYYY-MM-DD` - Filter by date
- `GET /api/diary/stats/` - Get statistics

All requests include JWT authentication token in the Authorization header.

## Styling

### Color Scheme
- Primary: `#667eea` (Purple-blue)
- Secondary: `#764ba2` (Deep purple)
- Gradient background for modern look
- White cards with subtle shadows

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Key Features
- Smooth hover effects
- Card elevation on hover
- Fade-in animations
- Glass-morphism effects
- Modern button styles

## State Management

### Main States
```jsx
- entries: Array of diary entries
- selectedEntry: Currently viewed entry
- formData: Form state for create/edit
- stats: Dashboard statistics
- view: Current view ('list', 'detail', 'create', 'edit')
- loading: Loading state
- selectedDate: Date filter value
```

### Form Data Structure
```jsx
{
  title: string,
  content_blocks: [
    {
      block_type: 'text' | 'image' | 'video',
      order: number,
      text_content: string | null,
      media_url: string | null,
      caption: string
    }
  ]
}
```

## Key Functions

### CRUD Operations
- `fetchEntries()` - Get all entries
- `fetchEntryById(id)` - Get single entry
- `createEntry(e)` - Create new entry
- `updateEntry(e)` - Update existing entry
- `deleteEntry(id)` - Delete entry

### Content Block Management
- `addContentBlock(type)` - Add new block
- `updateContentBlock(index, field, value)` - Update block content
- `removeContentBlock(index)` - Remove block
- `moveContentBlock(index, direction)` - Reorder blocks

### Utilities
- `fetchStats()` - Get statistics
- `fetchEntriesByDate(date)` - Filter by date
- `formatDate(dateString)` - Format timestamps
- `resetForm()` - Clear form state

## Dependencies

Required npm packages:
- `react` - Core React library
- `react-router-dom` - Routing (already in project)
- Auth context (already implemented)

## Future Enhancements

Potential features to add:
- [ ] File upload for images/videos (currently uses URLs)
- [ ] Rich text editor for text blocks
- [ ] Search functionality
- [ ] Tags/categories
- [ ] Mood tracking
- [ ] Weather integration
- [ ] Export to PDF
- [ ] Dark mode
- [ ] Entry templates
- [ ] Reminders/notifications
- [ ] Draft entries
- [ ] Image galleries
- [ ] Calendar view

## Troubleshooting

### Authentication Issues
- Ensure JWT token is valid
- Check if token is expired (component will auto-logout)
- Verify CORS settings on backend

### API Connection Issues
- Confirm backend is running on `http://localhost:8000`
- Check browser console for error messages
- Verify API endpoints match backend URLs

### Display Issues
- Clear browser cache
- Check browser console for CSS/JS errors
- Verify all imports are correct

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance

- Lazy loading could be added for large entry lists
- Images are loaded on-demand
- Efficient re-rendering with React hooks
- Minimal API calls (only when needed)

## Security

- JWT authentication required for all operations
- User can only access their own entries
- XSS protection through React's built-in escaping
- CSRF protection via token-based auth

## Accessibility

Current features:
- Semantic HTML structure
- Form labels for screen readers
- Keyboard navigation support
- Focus states on interactive elements

Improvements needed:
- ARIA labels for better screen reader support
- Keyboard shortcuts
- High contrast mode
- Focus trap in modals

## Testing

To test the component:
1. Start backend: `cd backend && py manage.py runserver`
2. Start frontend: `cd frontend && npm run dev`
3. Register/Login at http://localhost:5173
4. Navigate to http://localhost:5173/diary
5. Test all CRUD operations

## Contributing

When making changes:
1. Follow existing code style
2. Test all features before committing
3. Update documentation if needed
4. Ensure responsive design is maintained
5. Add comments for complex logic

## Support

For issues or questions:
- Check backend API documentation
- Review browser console for errors
- Verify authentication state
- Check network tab for API responses
