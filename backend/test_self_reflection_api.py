"""
Test script for Self-Reflection API

This script demonstrates how to use the Self-Reflection API endpoints.
Run the Django server before executing this script.

Usage:
    python test_self_reflection_api.py
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

# Test user credentials (update these as needed)
TEST_USER = {
    "email": "test@example.com",
    "password": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
}


class SelfReflectionAPITester:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.session = requests.Session()
    
    def print_response(self, title, response):
        """Print formatted API response"""
        print(f"\n{'='*60}")
        print(f"{title}")
        print(f"{'='*60}")
        print(f"Status Code: {response.status_code}")
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response: {response.text}")
    
    def register_user(self):
        """Register a new test user"""
        print("\n\n[1] REGISTERING TEST USER")
        url = f"{API_BASE}/auth/register/"
        response = self.session.post(url, json=TEST_USER)
        self.print_response("User Registration", response)
        return response.status_code in [200, 201]
    
    def login_user(self):
        """Login and get JWT tokens"""
        print("\n\n[2] LOGGING IN")
        url = f"{API_BASE}/auth/login/"
        response = self.session.post(url, json={
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        })
        self.print_response("User Login", response)
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get('access')
            self.refresh_token = data.get('refresh')
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })
            return True
        return False
    
    def create_sample_questions(self):
        """Create sample reflection questions"""
        print("\n\n[3] CREATING SAMPLE QUESTIONS")
        url = f"{API_BASE}/self-reflection/questions/"
        
        questions = [
            {
                "question_text": "Rate your day out of 10",
                "question_type": "range",
                "min_value": 1,
                "max_value": 10,
                "order": 1,
                "category": "Daily",
                "is_active": True
            },
            {
                "question_text": "What was your productivity level?",
                "question_type": "range",
                "min_value": 1,
                "max_value": 10,
                "order": 2,
                "category": "Productivity",
                "is_active": True
            },
            {
                "question_text": "Mood of the day",
                "question_type": "choice",
                "choices": ["Happy", "Sad", "Neutral", "Excited", "Anxious", "Calm"],
                "order": 3,
                "category": "Wellness",
                "is_active": True
            },
            {
                "question_text": "How many glasses of water did you have?",
                "question_type": "range",
                "min_value": 0,
                "max_value": 15,
                "order": 4,
                "category": "Health",
                "is_active": True
            },
            {
                "question_text": "Energy level",
                "question_type": "choice",
                "choices": ["Very Low", "Low", "Medium", "High", "Very High"],
                "order": 5,
                "category": "Wellness",
                "is_active": True
            },
            {
                "question_text": "What are you grateful for today?",
                "question_type": "text",
                "order": 6,
                "category": "Gratitude",
                "is_active": True
            }
        ]
        
        created_questions = []
        for q in questions:
            response = self.session.post(url, json=q)
            self.print_response(f"Creating Question: {q['question_text']}", response)
            if response.status_code in [200, 201]:
                created_questions.append(response.json())
        
        return created_questions
    
    def get_active_questions(self):
        """Get all active questions"""
        print("\n\n[4] GETTING ACTIVE QUESTIONS")
        url = f"{API_BASE}/self-reflection/questions/active/"
        response = self.session.get(url)
        self.print_response("Active Questions", response)
        return response.json() if response.status_code == 200 else []
    
    def create_reflection_for_today(self, questions):
        """Create a reflection for today"""
        print("\n\n[5] CREATING TODAY'S REFLECTION")
        url = f"{API_BASE}/self-reflection/reflections/"
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Build responses based on question types
        responses = []
        for q in questions:
            response_data = {"question_id": q['id']}
            
            if q['question_type'] == 'range':
                if 'water' in q['question_text'].lower():
                    response_data['range_response'] = 8
                elif 'productivity' in q['question_text'].lower():
                    response_data['range_response'] = 7
                else:
                    response_data['range_response'] = 9
            
            elif q['question_type'] == 'choice':
                if 'mood' in q['question_text'].lower():
                    response_data['choice_response'] = 'Happy'
                elif 'energy' in q['question_text'].lower():
                    response_data['choice_response'] = 'High'
                else:
                    response_data['choice_response'] = q['choices'][0]
            
            elif q['question_type'] == 'text':
                response_data['text_response'] = 'I am grateful for my health, family, and the opportunity to learn new things.'
            
            responses.append(response_data)
        
        reflection_data = {
            "date": today,
            "notes": "Today was a productive day! Completed all my tasks and felt energized.",
            "responses": responses
        }
        
        response = self.session.post(url, json=reflection_data)
        self.print_response("Today's Reflection", response)
        return response.json() if response.status_code in [200, 201] else None
    
    def create_past_reflections(self, questions):
        """Create reflections for the past few days"""
        print("\n\n[6] CREATING PAST REFLECTIONS")
        url = f"{API_BASE}/self-reflection/reflections/"
        
        for days_ago in range(1, 8):  # Last 7 days
            date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            
            responses = []
            for q in questions:
                response_data = {"question_id": q['id']}
                
                if q['question_type'] == 'range':
                    # Varying values for different days
                    import random
                    if 'water' in q['question_text'].lower():
                        response_data['range_response'] = random.randint(6, 10)
                    else:
                        response_data['range_response'] = random.randint(5, 10)
                
                elif q['question_type'] == 'choice':
                    response_data['choice_response'] = q['choices'][days_ago % len(q['choices'])]
                
                elif q['question_type'] == 'text':
                    response_data['text_response'] = f'Reflection for {date}'
                
                responses.append(response_data)
            
            reflection_data = {
                "date": date,
                "notes": f"Reflection notes for {date}",
                "responses": responses
            }
            
            response = self.session.post(url, json=reflection_data)
            print(f"Created reflection for {date}: Status {response.status_code}")
    
    def get_todays_reflection(self):
        """Get today's reflection"""
        print("\n\n[7] GETTING TODAY'S REFLECTION")
        url = f"{API_BASE}/self-reflection/reflections/today/"
        response = self.session.get(url)
        self.print_response("Today's Reflection", response)
    
    def get_reflection_by_date(self):
        """Get reflection for a specific date"""
        print("\n\n[8] GETTING REFLECTION BY DATE")
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        url = f"{API_BASE}/self-reflection/reflections/by_date/?date={yesterday}"
        response = self.session.get(url)
        self.print_response(f"Reflection for {yesterday}", response)
    
    def get_all_reflections(self):
        """Get all user reflections"""
        print("\n\n[9] GETTING ALL REFLECTIONS")
        url = f"{API_BASE}/self-reflection/reflections/"
        response = self.session.get(url)
        self.print_response("All Reflections", response)
    
    def get_statistics(self):
        """Get reflection statistics"""
        print("\n\n[10] GETTING STATISTICS")
        url = f"{API_BASE}/self-reflection/reflections/stats/?days=30"
        response = self.session.get(url)
        self.print_response("Statistics (Last 30 Days)", response)
    
    def get_streak(self):
        """Get current reflection streak"""
        print("\n\n[11] GETTING CURRENT STREAK")
        url = f"{API_BASE}/self-reflection/reflections/streak/"
        response = self.session.get(url)
        self.print_response("Current Streak", response)
    
    def get_date_range(self):
        """Get reflections for a date range"""
        print("\n\n[12] GETTING DATE RANGE REFLECTIONS")
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        url = f"{API_BASE}/self-reflection/reflections/date_range/?start_date={start_date}&end_date={end_date}"
        response = self.session.get(url)
        self.print_response(f"Reflections from {start_date} to {end_date}", response)
    
    def run_all_tests(self):
        """Run all API tests"""
        print("="*60)
        print("SELF-REFLECTION API TEST SUITE")
        print("="*60)
        
        # Register or login
        if not self.register_user():
            print("\nUser already exists, attempting login...")
        
        if not self.login_user():
            print("\n❌ Login failed! Cannot proceed with tests.")
            return
        
        print("\n✅ Successfully authenticated!")
        
        # Create questions
        questions = self.create_sample_questions()
        
        if not questions:
            # Try to get existing questions
            questions = self.get_active_questions()
        
        if not questions:
            print("\n❌ No questions available! Cannot create reflections.")
            return
        
        # Create reflections
        self.create_reflection_for_today(questions)
        self.create_past_reflections(questions)
        
        # Query reflections
        self.get_todays_reflection()
        self.get_reflection_by_date()
        self.get_all_reflections()
        self.get_date_range()
        
        # Get statistics
        self.get_statistics()
        self.get_streak()
        
        print("\n\n" + "="*60)
        print("✅ ALL TESTS COMPLETED!")
        print("="*60)


if __name__ == "__main__":
    tester = SelfReflectionAPITester()
    tester.run_all_tests()
