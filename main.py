from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn

from models import User, Event, UserPreferences, RecommendationResponse
from recommendation_engine import ContentBasedRecommendationEngine

app = FastAPI(
    title="Vaimo Event Recommendation System",
    description="A content-based recommendation system for user-event matching",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommendation engine
recommendation_engine = ContentBasedRecommendationEngine()

# In-memory storage (in production, use a proper database)
users_db = {}
events_db = {}
user_preferences_db = {}

@app.get("/")
async def root():
    return {"message": "Vaimo Event Recommendation System"}

@app.post("/users/", response_model=User)
async def create_user(user: User):
    """Register a new user"""
    if user.user_id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    users_db[user.user_id] = user
    return user

@app.post("/users/{user_id}/preferences/", response_model=UserPreferences)
async def set_user_preferences(user_id: str, preferences: UserPreferences):
    """Set user preferences for recommendation"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    preferences.user_id = user_id
    user_preferences_db[user_id] = preferences
    return preferences

@app.post("/events/", response_model=Event)
async def create_event(event: Event):
    """Create a new event"""
    if event.event_id in events_db:
        raise HTTPException(status_code=400, detail="Event already exists")
    
    events_db[event.event_id] = event
    return event

@app.get("/events/", response_model=List[Event])
async def get_events():
    """Get all events"""
    return list(events_db.values())

@app.get("/users/{user_id}/recommendations/", response_model=List[RecommendationResponse])
async def get_recommendations(user_id: str, limit: int = 10):
    """Get personalized event recommendations for a user"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_id not in user_preferences_db:
        raise HTTPException(status_code=400, detail="User preferences not set")
    
    user_preferences = user_preferences_db[user_id]
    events = list(events_db.values())
    
    if not events:
        return []
    
    recommendations = recommendation_engine.get_recommendations(
        user_preferences, events, limit
    )
    
    return recommendations

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 