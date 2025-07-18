from typing import List
from .models import Event, UserPreferences, RecommendationResponse

class ContentBasedRecommendationEngine:
    """
    Simple content-based recommendation engine that matches users with events
    based on category matching only.
    """
    
    def calculate_category_score(self, event: Event, preferences: UserPreferences) -> float:
        """Calculate score based on category matching"""
        # Check if event category matches any of user's preferred categories
        event_category_lower = event.category.lower()
        user_categories_lower = [cat.lower() for cat in preferences.categories]
        
        if event_category_lower in user_categories_lower:
            return 1.0
        return 0.0
    
    def generate_explanation(self, event: Event, preferences: UserPreferences, score: float) -> str:
        """Generate human-readable explanation for the recommendation"""
        if score > 0:
            return f"This event matches your interest in {event.category}."
        else:
            return "This event is in a different category from your preferences."
    
    def get_recommendations(self, preferences: UserPreferences, events: List[Event], 
                          limit: int = 10) -> List[RecommendationResponse]:
        """
        Generate personalized event recommendations for a user based on category matching
        """
        if not events:
            return []
        
        scored_events = []
        
        for event in events:
            score = self.calculate_category_score(event, preferences)
            explanation = self.generate_explanation(event, preferences, score)
            
            recommendation = RecommendationResponse(
                event=event,
                score=score,
                reason=explanation
            )
            
            scored_events.append(recommendation)
        
        # Sort by score (descending) and return top recommendations
        # Events with matching categories will have score=1.0, others will have score=0.0
        scored_events.sort(key=lambda x: x.score, reverse=True)
        
        return scored_events[:limit] 