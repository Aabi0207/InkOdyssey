"""
Populate database with dummy self-reflection data for testing dashboard
Run this script from the backend directory:
    python populate_dummy_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from self_reflection.models import ReflectionQuestion, SelfReflection, ReflectionResponse
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


def create_dummy_data(user_email='aabi@gmail.com', days_back=90):
    """
    Create dummy reflection data for a user
    
    Args:
        user_email: User email to create reflections for
        days_back: Number of days back to create reflections
    """
    
    print(f"\n{'='*60}")
    print(f"Populating Dummy Reflection Data")
    print(f"{'='*60}\n")
    
    # Get or create user
    try:
        user = User.objects.get(email=user_email)
        print(f"✓ Found user: {user_email}")
    except User.DoesNotExist:
        print(f"✗ User '{user_email}' not found!")
        print(f"  Please provide an existing user email or create one first.")
        return
    
    # Get active questions
    questions = ReflectionQuestion.objects.filter(is_active=True)
    
    if not questions.exists():
        print(f"\n✗ No active questions found!")
        print(f"  Please create some reflection questions first.")
        return
    
    print(f"✓ Found {questions.count()} active questions:")
    
    range_questions = questions.filter(question_type='range')
    choice_questions = questions.filter(question_type='choice')
    
    for q in questions:
        print(f"  - {q.question_text} ({q.question_type})")
    
    print(f"\n{'='*60}")
    print(f"Generating reflections for last {days_back} days...")
    print(f"{'='*60}\n")
    
    created_count = 0
    skipped_count = 0
    
    # Create reflections for each day
    for i in range(days_back):
        date = (timezone.now() - timedelta(days=i)).date()
        
        # Randomly skip some days (20% chance) to make data more realistic
        if random.random() < 0.2:
            skipped_count += 1
            continue
        
        # Check if reflection already exists
        existing = SelfReflection.objects.filter(user=user, date=date).first()
        
        if existing:
            print(f"  ⊙ {date}: Already exists, skipping...")
            skipped_count += 1
            continue
        
        # Create reflection
        reflection = SelfReflection.objects.create(
            user=user,
            date=date,
            notes=f"Auto-generated reflection for {date}"
        )
        
        response_count = 0
        
        # Add responses for range questions
        for question in range_questions:
            # Create varied patterns based on question
            if 'day' in question.question_text.lower() or 'overall' in question.question_text.lower():
                # Day ratings: tend to be higher with some variation
                value = random.choices(
                    range(question.min_value, question.max_value + 1),
                    weights=[1, 1, 2, 3, 5, 8, 10, 8, 5, 3],  # Bell curve favoring higher values
                    k=1
                )[0]
            elif 'productivity' in question.question_text.lower():
                # Productivity: more varied, some low days
                value = random.choices(
                    range(question.min_value, question.max_value + 1),
                    weights=[2, 3, 4, 5, 6, 7, 6, 5, 4, 2],  # More centered distribution
                    k=1
                )[0]
            else:
                # Default: random but weighted towards middle-high
                value = random.choices(
                    range(question.min_value, question.max_value + 1),
                    weights=[1, 2, 3, 5, 7, 8, 7, 5, 3, 2],
                    k=1
                )[0]
            
            ReflectionResponse.objects.create(
                daily_reflection=reflection,
                question=question,
                range_response=value
            )
            response_count += 1
        
        # Add responses for choice questions
        for question in choice_questions:
            if not question.choices:
                continue
            
            # Create realistic patterns for mood questions
            if 'mood' in question.question_text.lower():
                # Mood: favor positive choices with occasional negative
                if len(question.choices) >= 4:
                    # Weight more positive moods
                    weights = [1, 2, 3, 5] + [4] * (len(question.choices) - 4)
                else:
                    weights = [1] * len(question.choices)
                choice = random.choices(question.choices, weights=weights, k=1)[0]
            else:
                # Other choice questions: random distribution
                choice = random.choice(question.choices)
            
            ReflectionResponse.objects.create(
                daily_reflection=reflection,
                question=question,
                choice_response=choice
            )
            response_count += 1
        
        print(f"  ✓ {date}: Created with {response_count} responses")
        created_count += 1
    
    print(f"\n{'='*60}")
    print(f"Summary")
    print(f"{'='*60}")
    print(f"✓ Created {created_count} new reflections")
    print(f"⊙ Skipped {skipped_count} days (existing or randomly omitted)")
    print(f"📊 Total responses: {created_count * (range_questions.count() + choice_questions.count())}")
    print(f"\n✓ Done! Your dashboard should now have plenty of data to visualize.\n")


def clear_existing_data(user_email='aabi@gmail.com'):
    """
    Clear all existing reflection data for a user
    WARNING: This will delete all reflections and responses!
    """
    try:
        user = User.objects.get(email=user_email)
        count = SelfReflection.objects.filter(user=user).count()
        
        if count == 0:
            print(f"\nNo existing reflections found for {user_email}")
            return
        
        confirm = input(f"\n⚠ WARNING: This will delete {count} reflections for {user_email}. Continue? (yes/no): ")
        
        if confirm.lower() == 'yes':
            SelfReflection.objects.filter(user=user).delete()
            print(f"✓ Deleted {count} reflections")
        else:
            print("✗ Cancelled")
    except User.DoesNotExist:
        print(f"✗ User '{user_email}' not found!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Populate database with dummy reflection data')
    parser.add_argument('--email', type=str, default='aabi@gmail.com', help='User email to create data for')
    parser.add_argument('--days', type=int, default=90, help='Number of days back to generate data')
    parser.add_argument('--clear', action='store_true', help='Clear existing data before populating')
    
    args = parser.parse_args()
    
    if args.clear:
        clear_existing_data(args.email)
    
    create_dummy_data(args.email, args.days)
