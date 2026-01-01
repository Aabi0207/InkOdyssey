"""
Test script for dashboard statistics API
Run this after starting the Django server
"""
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000/api/self-reflection"

# You'll need to replace this with a valid token
# Get it by logging in through your frontend or using Django admin
TOKEN = "YOUR_ACCESS_TOKEN_HERE"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def test_dashboard_stats():
    """Test the dashboard statistics endpoint"""
    print("\n" + "="*60)
    print("Testing Dashboard Statistics API")
    print("="*60)
    
    # Test 1: Get all questions for last 30 days
    print("\n1. Getting dashboard stats for last 30 days...")
    response = requests.get(
        f"{BASE_URL}/reflections/dashboard_stats/",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success! Status: {response.status_code}")
        print(f"\nOverview:")
        print(f"  - Total Reflections: {data['overview']['total_reflections']}")
        print(f"  - Current Streak: {data['overview']['current_streak']}")
        print(f"  - Days Analyzed: {data['overview']['days_analyzed']}")
        print(f"  - Date Range: {data['overview']['start_date']} to {data['overview']['end_date']}")
        
        print(f"\nQuestions Found: {len(data['questions'])}")
        for q in data['questions']:
            print(f"\n  Question: {q['question_text']}")
            print(f"  Type: {q['question_type']}")
            print(f"  Category: {q['category']}")
            print(f"  Color Mapping: {json.dumps(q['color_mapping'], indent=4)}")
            
            if q['question_type'] == 'range':
                stats = q['line_chart']['statistics']
                print(f"  Statistics:")
                print(f"    - Average: {stats['average']}")
                print(f"    - Min: {stats['min']}, Max: {stats['max']}")
                print(f"    - Total Responses: {stats['count']}")
                print(f"  Heatmap Data Points: {len(q['heatmap'])}")
            elif q['question_type'] == 'choice':
                print(f"  Total Responses: {q['line_chart']['total_responses']}")
                print(f"  Datasets: {len(q['line_chart']['datasets'])}")
    else:
        print(f"✗ Failed! Status: {response.status_code}")
        print(f"Response: {response.text}")
    
    # Test 2: Get specific question for last 90 days
    print("\n\n2. Getting dashboard stats for specific question (90 days)...")
    response = requests.get(
        f"{BASE_URL}/reflections/dashboard_stats/?days=90&question_id=1",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success! Status: {response.status_code}")
        print(f"Questions returned: {len(data['questions'])}")
    else:
        print(f"✗ Failed! Status: {response.status_code}")


def test_questions_api():
    """Test that questions now include color_mapping"""
    print("\n" + "="*60)
    print("Testing Questions API (Color Mapping)")
    print("="*60)
    
    response = requests.get(
        f"{BASE_URL}/questions/",
        headers=headers
    )
    
    if response.status_code == 200:
        questions = response.json()
        print(f"✓ Success! Found {len(questions)} questions")
        
        for q in questions:
            print(f"\n  Question ID {q['id']}: {q['question_text']}")
            print(f"  Type: {q['question_type']}")
            if q['color_mapping']:
                print(f"  Colors assigned: {len(q['color_mapping'])} options")
                print(f"  Sample colors: {json.dumps(list(q['color_mapping'].items())[:3], indent=4)}")
            else:
                print(f"  ⚠ No color mapping! Run: python manage.py update_question_colors")
    else:
        print(f"✗ Failed! Status: {response.status_code}")


def test_streak():
    """Test the streak endpoint"""
    print("\n" + "="*60)
    print("Testing Streak API")
    print("="*60)
    
    response = requests.get(
        f"{BASE_URL}/reflections/streak/",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success! Current Streak: {data['current_streak']} days")
    else:
        print(f"✗ Failed! Status: {response.status_code}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Self-Reflection Dashboard API Test Suite")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if TOKEN == "YOUR_ACCESS_TOKEN_HERE":
        print("\n⚠ WARNING: Please update the TOKEN variable with a valid access token!")
        print("You can get a token by:")
        print("  1. Logging in through your frontend")
        print("  2. Using the /api/users/login/ endpoint")
        print("  3. Creating a token in Django admin")
    else:
        test_questions_api()
        test_streak()
        test_dashboard_stats()
    
    print("\n" + "="*60)
    print("Tests Complete!")
    print("="*60 + "\n")
