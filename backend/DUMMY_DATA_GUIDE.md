# Dummy Data Population Guide

## Quick Start

### 1. Find Your Username
First, you need to know which user account to populate data for. You can:
- Use your login username
- Check Django admin to see user list
- Create a new test user if needed

### 2. Run the Script

**Basic Usage (90 days of data for 'testuser'):**
```bash
cd backend
python populate_dummy_data.py --username YOUR_USERNAME
```

**Custom number of days:**
```bash
python populate_dummy_data.py --username YOUR_USERNAME --days 180
```

**Clear existing data first:**
```bash
python populate_dummy_data.py --username YOUR_USERNAME --clear
```

### 3. View Results
- Navigate to Dashboard in your app
- You should see beautiful charts with varied data
- Try different time ranges (7/30/90 days, All Time)

## Examples

### Populate 90 days for user "john"
```bash
python populate_dummy_data.py --username john --days 90
```

### Populate 30 days for user "admin"
```bash
python populate_dummy_data.py --username admin --days 30
```

### Clear and repopulate 60 days
```bash
python populate_dummy_data.py --username john --days 60 --clear
```

## What the Script Does

### Data Generation Patterns

**Range Questions (1-10 ratings):**
- **Day/Overall ratings**: Weighted towards higher values (6-9)
- **Productivity**: More centered distribution (4-7)
- **Other questions**: Bell curve favoring middle-high values

**Choice Questions:**
- **Mood questions**: Favors positive moods with occasional negative
- **Other choices**: Random but realistic distribution

### Realistic Features
- ✅ Randomly skips 20% of days (more realistic)
- ✅ Varied response patterns based on question type
- ✅ Skips days that already have reflections
- ✅ Only creates responses for active questions
- ✅ Ignores text questions (as requested)

## Output Example

```
============================================================
Populating Dummy Reflection Data
============================================================

✓ Found user: john
✓ Found 4 active questions:
  - Rate your overall day (range)
  - Productivity of your day (range)
  - What was your mood (choice)
  - Best thing today (text)

============================================================
Generating reflections for last 90 days...
============================================================

  ✓ 2024-12-03: Created with 3 responses
  ⊙ 2024-12-02: Randomly skipped
  ✓ 2024-12-01: Created with 3 responses
  ✓ 2024-11-30: Created with 3 responses
  ...

============================================================
Summary
============================================================
✓ Created 72 new reflections
⊙ Skipped 18 days (existing or randomly omitted)
📊 Total responses: 216

✓ Done! Your dashboard should now have plenty of data to visualize.
```

## Troubleshooting

### "User not found"
- Make sure you're using the correct username
- Check in Django admin or create the user first

### "No active questions found"
- Create some reflection questions first
- Make sure questions are marked as "active"

### "Already exists, skipping"
- The script won't overwrite existing data
- Use `--clear` flag to delete existing data first

### Script errors
- Make sure you're in the backend directory
- Ensure virtual environment is activated
- Check that Django is properly configured

## Tips

1. **Start small**: Try 30 days first to see results quickly
2. **Use different patterns**: The script creates realistic varied data
3. **Test dashboard**: After running, check all time ranges on dashboard
4. **Multiple users**: You can run for different users to compare
5. **Re-run safely**: Script won't duplicate - safe to run multiple times

## Data Patterns

The script creates intelligent patterns:

### Week Patterns
- Some "bad days" scattered throughout
- Generally positive trends
- Realistic variations

### Month Patterns
- Productivity varies mid-range
- Mood favors positive but includes some downs
- Day ratings generally good with exceptions

### Year Patterns (90+ days)
- Long-term trends visible
- Seasonal variations
- Enough data for meaningful heatmaps

## Next Steps

After running the script:
1. ✅ Refresh your dashboard page
2. ✅ Try different time ranges (7/30/90/All Time)
3. ✅ Check the heatmap year selector
4. ✅ Hover over charts to see details
5. ✅ Verify distribution statistics look good
