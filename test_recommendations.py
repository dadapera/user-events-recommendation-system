#!/usr/bin/env python3
"""
Test script for the Vaimo Event Recommendation System
"""

import asyncio
import requests
import json
from datetime import datetime
from sample_data import create_sample_users, create_sample_events, create_sample_preferences

BASE_URL = "http://localhost:8000"

def serialize_for_json(model):
    """Convert Pydantic model to JSON-serializable dict with datetime handling"""
    data = model.model_dump()
    # Convert any datetime objects to ISO format strings
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    return data

async def test_api():
    """Test the recommendation API with sample data"""
    
    print("🚀 Testing Vaimo Event Recommendation System")
    print("=" * 50)
    
    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ API Status: {response.json()['message']}")
    except requests.exceptions.ConnectionError:
        print("❌ API is not running. Start the server with: python main.py")
        return
    
    # Create sample data
    users = create_sample_users()
    events = create_sample_events()
    preferences = create_sample_preferences()
    
    print(f"\n📊 Loading sample data:")
    print(f"  • {len(users)} users")
    print(f"  • {len(events)} events")
    print(f"  • {len(preferences)} user preferences")
    
    # Create users
    print("\n👥 Creating users...")
    for user in users:
        response = requests.post(
            f"{BASE_URL}/users/",
            json=serialize_for_json(user)
        )
        if response.status_code == 200:
            print(f"  ✅ Created user: {user.name}")
        else:
            print(f"  ❌ Failed to create user: {user.name}")
    
    # Create events
    print("\n🎉 Creating events...")
    for event in events:
        response = requests.post(
            f"{BASE_URL}/events/",
            json=serialize_for_json(event)
        )
        if response.status_code == 200:
            print(f"  ✅ Created event: {event.title}")
        else:
            print(f"  ❌ Failed to create event: {event.title}")
    
    # Set user preferences
    print("\n⚙️ Setting user preferences...")
    for pref in preferences:
        response = requests.post(
            f"{BASE_URL}/users/{pref.user_id}/preferences/",
            json=serialize_for_json(pref)
        )
        if response.status_code == 200:
            print(f"  ✅ Set preferences for user: {pref.user_id}")
        else:
            print(f"  ❌ Failed to set preferences for user: {pref.user_id}")
    
    # Get recommendations for each user
    print("\n🎯 Getting recommendations...")
    print("=" * 50)
    
    for user in users:
        print(f"\n🔍 Recommendations for {user.name} ({user.user_id}):")
        print("-" * 40)
        
        response = requests.get(
            f"{BASE_URL}/users/{user.user_id}/recommendations/?limit=5"
        )
        
        if response.status_code == 200:
            recommendations = response.json()
            
            if not recommendations:
                print("  No recommendations found.")
                continue
            
            for i, rec in enumerate(recommendations, 1):
                event = rec['event']
                score = rec['score']
                reason = rec['reason']
                
                print(f"\n  {i}. {event['title']}")
                print(f"     📊 Score: {score:.3f}")
                print(f"     📝 Reason: {reason}")
                print(f"     📍 Location: {event['location']}")
                print(f"     💰 Price: ${event['price']}")
                print(f"     🏷️ Category: {event['category']}")
                print(f"     🔖 Tags: {', '.join(event['tags'][:3])}...")
        else:
            print(f"  ❌ Failed to get recommendations: {response.text}")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")
    print("\nTo explore the API further:")
    print("1. Visit http://localhost:8000/docs for interactive API documentation")
    print("2. Use the endpoints to create your own users, events, and preferences")
    print("3. Experiment with different preference weights to see how recommendations change")

def test_local_engine():
    """Test the recommendation engine locally without API"""
    
    print("🧪 Testing recommendation engine locally...")
    print("=" * 50)
    
    from recommendation_engine import ContentBasedRecommendationEngine
    
    # Create sample data
    users = create_sample_users()
    events = create_sample_events()
    preferences = create_sample_preferences()
    
    # Initialize engine
    engine = ContentBasedRecommendationEngine()
    
    # Test recommendations for first user
    user_pref = preferences[0]  # Alice's preferences
    
    print(f"\n🎯 Testing recommendations for {user_pref.user_id}")
    print(f"Interested categories: {', '.join(user_pref.categories)}")
    
    recommendations = engine.get_recommendations(user_pref, events, limit=3)
    
    print(f"\n📋 Top 3 recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.event.title}")
        print(f"   Score: {rec.score:.3f}")
        print(f"   Reason: {rec.reason}")
        print(f"   Category: {rec.event.category}")
        print(f"   Tags: {', '.join(rec.event.tags)}")

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Test API (requires server running)")
    print("2. Test local engine only")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        asyncio.run(test_api())
    elif choice == "2":
        test_local_engine()
    else:
        print("Invalid choice. Running local test...")
        test_local_engine() 