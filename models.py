from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class User(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    name: str = Field(..., description="User's name")
    email: str = Field(..., description="User's email address")
    age: Optional[int] = Field(None, description="User's age")
    location: Optional[str] = Field(None, description="User's location")
    created_at: datetime = Field(default_factory=datetime.now)

class Event(BaseModel):
    event_id: str = Field(..., description="Unique identifier for the event")
    title: str = Field(..., description="Event title")
    description: str = Field(..., description="Event description")
    category: str = Field(..., description="Main category of the event")
    tags: List[str] = Field(..., description="List of tags associated with the event")
    location: str = Field(..., description="Event location")
    date: datetime = Field(..., description="Event date and time")
    price: float = Field(0.0, description="Event price (0 for free events)")
    organizer: str = Field(..., description="Event organizer")
    capacity: Optional[int] = Field(None, description="Maximum number of attendees")
    rating: Optional[float] = Field(None, description="Average rating of the event", ge=0, le=5)

class UserPreferences(BaseModel):
    user_id: Optional[str] = Field(None, description="User ID (set automatically)")
    categories: List[str] = Field(..., description="Categories the user is interested in")

class RecommendationResponse(BaseModel):
    event: Event = Field(..., description="The recommended event")
    score: float = Field(..., description="Recommendation score (0-1)")
    reason: str = Field(..., description="Explanation for why this event was recommended")

class EventRating(BaseModel):
    user_id: str = Field(..., description="User who rated the event")
    event_id: str = Field(..., description="Event that was rated")
    rating: float = Field(..., description="Rating value", ge=1, le=5)
    review: Optional[str] = Field(None, description="Optional review text")
    created_at: datetime = Field(default_factory=datetime.now) 