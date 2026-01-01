# Quick Reference: Dashboard Usage

## To Start Using the Dashboard

### 1. Start Backend Server
```bash
cd backend
python manage.py runserver
```

### 2. Start Frontend Server
```bash
cd frontend
npm run dev
```

### 3. Add Some Reflections First
- Go to "Reflection" page (http://localhost:5173/reflection)
- Answer the reflection questions for multiple days
- This will generate data for the dashboard

### 4. View Dashboard
- Navigate to Dashboard page
- You'll see beautiful charts based on your reflection data
- Use the day selector (7/30/90 days) to change the time window

## What You'll See

### If You Have Reflection Data:
✅ Overview stats (total reflections, streak, questions)
✅ Smooth line charts for range questions (with gradient fills)
✅ Calendar heatmaps for choice questions (with color legend)
✅ Distribution statistics for each question
✅ Grouped by category

### If You Don't Have Data Yet:
- Empty state with message: "No Reflection Data Yet"
- Message encouraging you to add reflections

## Chart Types

### Range Questions (1-10 ratings)
- **Visualization**: Smooth area chart
- **Shows**: Trend over time
- **Stats**: Average, min, max, count
- **Distribution**: How often you selected each value
- **Colors**: Gradient from light to dark based on value

### Choice Questions (Multiple options)
- **Visualization**: Calendar heatmap (GitHub-style)
- **Shows**: Which option selected on each day
- **Legend**: Color key showing option → color mapping
- **Distribution**: Percentage breakdown of choices
- **Colors**: Automatically assigned from backend

## Features

### Interactive Elements
- ✅ Hover over chart points to see exact values
- ✅ Hover over heatmap squares to see date + choice
- ✅ Click day range buttons to change time window
- ✅ Smooth animations and transitions

### Responsive Design
- ✅ Desktop: 2-column chart layout
- ✅ Tablet: 1-column chart layout
- ✅ Mobile: Optimized spacing and touch-friendly

### Loading States
- ✅ Spinner while fetching data
- ✅ Error message with retry button if fetch fails
- ✅ Empty state if no data exists

## API Endpoints Used

```javascript
// Main dashboard data
GET /api/self-reflection/reflections/dashboard_stats/?days=30

// Authentication
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Customization

### Change Colors
Edit `Dashboard.css`:
- Primary color: Search for `#2980B9`
- Background: Search for `#FEFBF6`
- Text colors: `#2C3E50`, `#7f8c8d`

### Change Chart Height
In `Dashboard.jsx`, find:
```javascript
<ResponsiveContainer width="100%" height={300}>
```
Change `300` to desired height.

### Change Default Days
In `Dashboard.jsx`, find:
```javascript
const [selectedDays, setSelectedDays] = useState(30);
```
Change `30` to `7` or `90`.

## Troubleshooting

### "Failed to load dashboard data"
- ✅ Check if backend server is running
- ✅ Check if you're logged in (valid access token)
- ✅ Check browser console for errors

### "No Reflection Data Yet"
- ✅ Add some reflections first
- ✅ Make sure questions are marked as "active"
- ✅ Check date range (may need more days)

### Charts not showing
- ✅ Check browser console for errors
- ✅ Ensure recharts is installed: `npm install recharts`
- ✅ Refresh the page

### Heatmap squares all gray
- ✅ Check if you have choice question responses
- ✅ Verify color_mapping exists in API response
- ✅ Check browser console for errors

## Tips

1. **Add variety**: Answer different questions to see diverse charts
2. **Be consistent**: Answer regularly to see meaningful trends
3. **Use categories**: Organize questions by category for better grouping
4. **Test ranges**: Try different day ranges (7/30/90) to see patterns
5. **Hover everywhere**: Charts have interactive tooltips with details

## Example Workflow

1. ✅ Create 3-4 questions (mix of range and choice types)
2. ✅ Add reflections for at least 7-10 days
3. ✅ Visit Dashboard to see your first charts
4. ✅ Change day range to see different time windows
5. ✅ Hover over charts to explore detailed data
6. ✅ Continue adding daily reflections to build trends

## Color Mapping (Automatic)

### Range Questions
- Low values (1-2): Light colors (#FCF6D9)
- Medium values (5-6): Medium colors (#DDBA7D)
- High values (9-10): Dark colors (#A72703)

### Choice Questions
- Each option gets a unique color from palette
- 20 colors available (no repetition within question)
- Colors assigned automatically by backend
- Consistent across all visualizations

## Performance

- Charts are optimized for smooth rendering
- Data cached in component state
- Only re-fetches when day range changes
- Responsive animations with CSS transitions
