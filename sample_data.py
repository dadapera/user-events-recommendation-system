from datetime import datetime, timedelta
from models import User, Event, UserPreferences

def create_sample_users():
    """Create sample users for testing"""
    users = [
        User(
            user_id="user_1",
            name="Alice Johnson",
            email="alice@example.com",
            age=28,
            location="New York"
        ),
        User(
            user_id="user_2",
            name="Bob Smith",
            email="bob@example.com",
            age=35,
            location="San Francisco"
        ),
        User(
            user_id="user_3",
            name="Carol Davis",
            email="carol@example.com",
            age=42,
            location="Los Angeles"
        )
    ]
    return users

def create_sample_events():
    """Create sample events for testing"""
    base_date = datetime.now() + timedelta(days=7)
    
    events = [
        Event(
            event_id="event_1",
            title="Tech Conference 2024",
            description="A comprehensive technology conference featuring AI, machine learning, and web development talks",
            category="Technology",
            tags=["AI", "machine learning", "web development", "networking", "innovation"],
            location="San Francisco, CA",
            date=base_date,
            price=299.99,
            organizer="Tech Events Inc",
            capacity=500,
            rating=4.7
        ),
        Event(
            event_id="event_2",
            title="Jazz Night at Blue Note",
            description="An intimate evening of smooth jazz featuring local and international artists",
            category="Music",
            tags=["jazz", "live music", "evening", "intimate", "artists"],
            location="New York, NY",
            date=base_date + timedelta(days=2),
            price=45.00,
            organizer="Blue Note Club",
            capacity=150,
            rating=4.5
        ),
        Event(
            event_id="event_3",
            title="Startup Pitch Competition",
            description="Watch innovative startups pitch their ideas to investors and industry experts",
            category="Business",
            tags=["startup", "entrepreneurship", "pitch", "investors", "innovation"],
            location="Los Angeles, CA",
            date=base_date + timedelta(days=5),
            price=0.0,
            organizer="Startup Hub",
            capacity=200,
            rating=4.2
        ),
        Event(
            event_id="event_4",
            title="Modern Art Gallery Opening",
            description="Discover contemporary art from emerging and established artists in this exclusive gallery opening",
            category="Art",
            tags=["modern art", "gallery", "contemporary", "exhibition", "culture"],
            location="New York, NY",
            date=base_date + timedelta(days=3),
            price=25.00,
            organizer="Metropolitan Gallery",
            capacity=100,
            rating=4.1
        ),
        Event(
            event_id="event_5",
            title="Python Developer Meetup",
            description="Monthly meetup for Python developers featuring talks on frameworks, best practices, and career development",
            category="Technology",
            tags=["python", "programming", "meetup", "networking", "career"],
            location="San Francisco, CA",
            date=base_date + timedelta(days=10),
            price=0.0,
            organizer="Python Community",
            capacity=80,
            rating=4.6
        ),
        Event(
            event_id="event_6",
            title="Cooking Masterclass: Italian Cuisine",
            description="Learn to prepare authentic Italian dishes from a professional chef",
            category="Food",
            tags=["cooking", "italian", "masterclass", "chef", "hands-on"],
            location="Los Angeles, CA",
            date=base_date + timedelta(days=8),
            price=89.99,
            organizer="Culinary Institute",
            capacity=25,
            rating=4.8
        ),
        Event(
            event_id="event_7",
            title="Classical Music Concert",
            description="Experience the beauty of classical music performed by the city orchestra",
            category="Music",
            tags=["classical", "orchestra", "concert", "symphony", "cultural"],
            location="New York, NY",
            date=base_date + timedelta(days=12),
            price=65.00,
            organizer="City Orchestra",
            capacity=800,
            rating=4.4
        ),
        Event(
            event_id="event_8",
            title="Digital Marketing Workshop",
            description="Learn the latest digital marketing strategies and tools for business growth",
            category="Business",
            tags=["digital marketing", "workshop", "business", "growth", "online"],
            location="San Francisco, CA",
            date=base_date + timedelta(days=6),
            price=149.99,
            organizer="Marketing Pro Academy",
            capacity=50,
            rating=4.3
        )
    ]
    return events

def create_sample_preferences():
    """Create sample user preferences for testing"""
    preferences = [
        UserPreferences(
            user_id="user_1",
            categories=["Technology", "Business"]
        ),
        UserPreferences(
            user_id="user_2",
            categories=["Music", "Art"]
        ),
        UserPreferences(
            user_id="user_3",
            categories=["Food", "Art", "Business"]
        )
    ]
    return preferences 