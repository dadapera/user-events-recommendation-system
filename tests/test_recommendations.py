#!/usr/bin/env python3
"""
Test script for the Vaimo Event Recommendation System
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    """Test the recommendation API with the simplified endpoints"""
    print("🚀 Testing Vaimo Event Recommendation System")
    print("=" * 50)
    
    # Test API status
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print(f"✅ API Status: {response.json()['message']}")
        else:
            print(f"❌ API not responding properly")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running at http://localhost:8000")
        return
    
    print("\n" + "=" * 50)
    
    # Test GET /events/ endpoint
    print("📅 Testing GET /events/ endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/events/")
        if response.status_code == 200:
            events = response.json()
            print(f"✅ Successfully retrieved {len(events)} events")
            
            # Display first few events
            for i, event in enumerate(events[:3]):
                print(f"  📍 Event {i+1}: {event['title']}")
                print(f"     Category: {event['category']}")
                print(f"     Location: {event['location']}")
                print(f"     Price: ${event['price']}")
                print(f"     Date: {event['date']}")
                print()
        else:
            print(f"❌ Failed to get events: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing events endpoint: {e}")
    
    print("=" * 50)
    
    # Test GET /users/{user_id}/recommendations/ endpoint
    print("🎯 Testing GET /users/{user_id}/recommendations/ endpoint...")
    
    # Test with different users
    test_users = ["user_1", "user_2", "user_3"]
    
    for user_id in test_users:
        print(f"\n👤 Testing recommendations for {user_id}...")
        try:
            response = requests.get(f"{BASE_URL}/users/{user_id}/recommendations/")
            if response.status_code == 200:
                recommendations = response.json()
                print(f"✅ Got {len(recommendations)} recommendations for {user_id}")
                
                # Display top 3 recommendations
                for i, rec in enumerate(recommendations[:3]):
                    event = rec['event']
                    print(f"  🎯 Recommendation {i+1}: {event['title']}")
                    print(f"     Score: {rec['score']:.3f}")
                    print(f"     Reason: {rec['reason']}")
                    print(f"     Category: {event['category']}")
                    print()
            elif response.status_code == 404:
                print(f"❌ User {user_id} not found")
            elif response.status_code == 400:
                print(f"❌ User preferences not set for {user_id}")
            else:
                print(f"❌ Failed to get recommendations: {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing recommendations for {user_id}: {e}")
    
    print("=" * 50)
    print("🎉 API testing completed!")
    
    # Test with non-existent user
    print(f"\n🔍 Testing with non-existent user...")
    try:
        response = requests.get(f"{BASE_URL}/users/nonexistent/recommendations/")
        if response.status_code == 404:
            print("✅ Correctly returned 404 for non-existent user")
        else:
            print(f"❌ Expected 404, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing non-existent user: {e}")

def test_local_engine():
    """Test the recommendation engine locally without API"""
    print("🚀 Testing Local Recommendation Engine")
    print("=" * 50)
    
    try:
        # Import the app modules
        import sys
        import os
        import csv
        from datetime import datetime
        
        # Get the project root directory (parent of tests directory)
        project_root = os.path.dirname(os.path.dirname(__file__))
        sys.path.append(project_root)
        
        from app.recommendation_engine import ContentBasedRecommendationEngine
        from app.models import User, Event, UserPreferences
        from app.config import EVENTS_CSV_PATH, USERS_CSV_PATH
        
        # Read events from CSV
        events = []
        events_file = os.path.join(project_root, EVENTS_CSV_PATH)
        
        if not os.path.exists(events_file):
            print(f"❌ Events file not found: {events_file}")
            return
        
        print(f"📊 Loading events from {events_file}...")
        with open(events_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tags = row['tags'].split(';') if row['tags'] else []
                event = Event(
                    event_id=row['event_id'],
                    title=row['title'],
                    description=row['description'],
                    category=row['category'],
                    tags=tags,
                    location=row['location'],
                    date=datetime.fromisoformat(row['date']),
                    price=float(row['price']),
                    organizer=row['organizer'],
                    capacity=int(row['capacity']) if row['capacity'] else None,
                    rating=float(row['rating']) if row['rating'] else None
                )
                events.append(event)
        
        print(f"✅ Loaded {len(events)} events")
        
        # Read users and preferences from CSV
        users_file = os.path.join(project_root, USERS_CSV_PATH)
        
        if not os.path.exists(users_file):
            print(f"❌ Users file not found: {users_file}")
            return
        
        print(f"👥 Loading users from {users_file}...")
        users_with_preferences = []
        
        with open(users_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User(
                    user_id=row['user_id'],
                    name=row['name'],
                    email=row['email'],
                    age=int(row['age']) if row['age'] else None,
                    location=row['location'],
                    created_at=datetime.fromisoformat(row['created_at'])
                )
                
                categories = row['categories'].split(';') if row['categories'] else []
                preferences = UserPreferences(
                    user_id=user.user_id,
                    categories=categories
                )
                
                users_with_preferences.append((user, preferences))
        
        print(f"✅ Loaded {len(users_with_preferences)} users with preferences")
        
        # Initialize recommendation engine
        engine = ContentBasedRecommendationEngine()
        
        print("\n" + "=" * 60)
        print("🎯 TESTING RECOMMENDATIONS")
        print("=" * 60)
        
        # Test recommendations for each user
        for user, preferences in users_with_preferences:
            print(f"\n👤 Testing recommendations for {user.name} ({user.user_id})")
            print(f"📍 Location: {user.location}")
            print(f"🏷️  Interested in: {', '.join(preferences.categories)}")
            print("-" * 50)
            
            # Get recommendations
            recommendations = engine.get_recommendations(preferences, events, limit=5)
            
            if not recommendations:
                print("  ❌ No recommendations found")
                continue
            
            print(f"  🎯 Found {len(recommendations)} recommendations:")
            
            for i, rec in enumerate(recommendations, 1):
                event = rec.event
                score = rec.score
                reason = rec.reason
                
                print(f"\n  {i}. 🎪 {event.title}")
                print(f"     📊 Score: {score:.3f}")
                print(f"     📝 Reason: {reason}")
                print(f"     🏷️  Category: {event.category}")
                print(f"     📍 Location: {event.location}")
                print(f"     💰 Price: ${event.price}")
                print(f"     ⭐ Rating: {event.rating}/5.0")
                print(f"     🔖 Tags: {', '.join(event.tags[:3])}{'...' if len(event.tags) > 3 else ''}")
        
        print("\n" + "=" * 60)
        print("✅ Local engine testing completed successfully!")
        print("=" * 60)
        
        # Show some statistics
        categories = set()
        locations = set()
        for event in events:
            categories.add(event.category)
            locations.add(event.location)
        
        print(f"\n📈 Dataset Statistics:")
        print(f"  • {len(events)} total events")
        print(f"  • {len(categories)} categories: {', '.join(sorted(categories))}")
        print(f"  • {len(locations)} locations: {', '.join(sorted(locations))}")
        print(f"  • {len(users_with_preferences)} users with preferences")
        
    except Exception as e:
        print(f"❌ Error during local testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Test API (requires server running)")
    print("2. Test local engine only")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_api()
    elif choice == "2":
        test_local_engine()
    else:
        print("Invalid choice. Please enter 1 or 2.") 