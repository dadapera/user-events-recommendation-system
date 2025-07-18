from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
import csv
import os
from datetime import datetime

from .models import User, Event, UserPreferences, RecommendationResponse
from .recommendation_engine import ContentBasedRecommendationEngine
from .config import (
    API_TITLE, API_DESCRIPTION, API_VERSION,
    EVENTS_CSV_PATH, USERS_CSV_PATH,
    CORS_ORIGINS, CORS_ALLOW_CREDENTIALS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS,
    DEFAULT_RECOMMENDATION_LIMIT
)

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# Initialize recommendation engine
recommendation_engine = ContentBasedRecommendationEngine()

def read_events_from_csv():
    """Read events from CSV file on-demand"""
    csv_file = EVENTS_CSV_PATH
    if not os.path.exists(csv_file):
        raise HTTPException(status_code=500, detail=f"Events data file {csv_file} not found")
    
    events = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Parse tags (semicolon separated)
            tags = row['tags'].split(';') if row['tags'] else []
            
            # Create Event object
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
    
    return events

def read_user_from_csv(user_id: str):
    """Read a specific user and their preferences from CSV file on-demand"""
    csv_file = USERS_CSV_PATH
    if not os.path.exists(csv_file):
        raise HTTPException(status_code=500, detail=f"Users data file {csv_file} not found")
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['user_id'] == user_id:
                # Create User object
                user = User(
                    user_id=row['user_id'],
                    name=row['name'],
                    email=row['email'],
                    age=int(row['age']) if row['age'] else None,
                    location=row['location'],
                    created_at=datetime.fromisoformat(row['created_at'])
                )
                
                # Create UserPreferences object
                categories = row['categories'].split(';') if row['categories'] else []
                preferences = UserPreferences(
                    user_id=user.user_id,
                    categories=categories
                )
                
                return user, preferences
    
    # User not found
    return None, None

@app.get("/")
async def root():
    return {"message": "Vaimo Event Recommendation System"}

@app.get("/events/", response_model=List[Event])
async def get_events():
    """Get all events by reading from CSV file"""
    events = read_events_from_csv()
    return events

@app.get("/users/{user_id}/recommendations/", response_model=List[RecommendationResponse])
async def get_recommendations(user_id: str, limit: int = DEFAULT_RECOMMENDATION_LIMIT):
    """Get personalized event recommendations for a user by reading from CSV files"""
    # Read user and preferences from CSV
    user, user_preferences = read_user_from_csv(user_id)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_preferences is None:
        raise HTTPException(status_code=400, detail="User preferences not found")
    
    # Read events from CSV
    events = read_events_from_csv()
    
    if not events:
        return []
    
    recommendations = recommendation_engine.get_recommendations(
        user_preferences, events, limit
    )
    
    return recommendations 