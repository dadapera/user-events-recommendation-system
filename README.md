# Vaimo Event Recommendation System

A content-based recommendation system built with FastAPI for matching users with relevant events based on their preferences and interests.

## Features

- **Content-Based Filtering**: Recommends events based on simple category matching between user preferences and events
- **Simple Scoring**: Events matching user's preferred categories get a score of 1.0, others get 0.0
- **RESTful API**: Clean FastAPI endpoints for user management, event creation, and getting recommendations
- **Explainable Recommendations**: Each recommendation comes with a human-readable explanation

## Architecture

```
vaimo_recom_sys/
├── main.py                    # FastAPI application and API endpoints
├── models.py                  # Pydantic data models
├── recommendation_engine.py   # Content-based recommendation logic
├── sample_data.py            # Sample data for testing
├── test_recommendations.py   # Test script with examples
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Models

### User
- Basic user information (ID, name, email, age, location)

### Event
- Event details (title, description, category, tags, location, date, price, organizer, capacity, rating)

### UserPreferences
- Simple user preferences:
  - User ID (automatically set)
  - Categories (list of interested event categories)

### RecommendationResponse
- Event recommendation with score and explanation

## Recommendation Algorithm

The content-based recommendation engine uses simple category matching:

1. **Category Matching**: Checks if the event's category matches any of the user's preferred categories
2. **Scoring**: Events with matching categories get a score of 1.0, others get 0.0
3. **Ranking**: Events are sorted by score (matching categories first)

## Installation

1. **Clone/Navigate to the project directory**:
   ```bash
   cd vaimo_recom_sys
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the API Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

### API Endpoints

- **POST** `/users/` - Create a new user
- **POST** `/users/{user_id}/preferences/` - Set user preferences
- **POST** `/events/` - Create a new event
- **GET** `/events/` - Get all events
- **GET** `/users/{user_id}/recommendations/` - Get personalized recommendations

### Testing

Run the test script to see the system in action:

```bash
python test_recommendations.py
```

This will:
1. Load sample users, events, and preferences
2. Test the API endpoints
3. Generate recommendations for each user
4. Display results with explanations

## Example Usage

### 1. Create a User

```python
import requests

user_data = {
    "user_id": "alice123",
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 28,
    "location": "San Francisco"
}

response = requests.post("http://localhost:8000/users/", json=user_data)
```

### 2. Set User Preferences

```python
preferences = {
    "categories": ["Technology", "Business"]
}

response = requests.post(
    "http://localhost:8000/users/alice123/preferences/", 
    json=preferences
)
```

### 3. Get Recommendations

```python
response = requests.get(
    "http://localhost:8000/users/alice123/recommendations/?limit=5"
)
recommendations = response.json()

for rec in recommendations:
    print(f"Event: {rec['event']['title']}")
    print(f"Score: {rec['score']:.3f}")
    print(f"Reason: {rec['reason']}")
    print("---")
```

## Sample Data

The system includes sample data with:
- 3 sample users with different category preferences
- 8 diverse events across categories (Technology, Music, Art, Business, Food)
- Simple user preferences focused on categories

## Extending the System

### Adding New Recommendation Factors

1. Add the factor calculation method to `ContentBasedRecommendationEngine`
2. Include it in the `calculate_composite_score` method
3. Add the weight to the `UserPreferences` model
4. Update the explanation generation logic

### Adding Collaborative Filtering

The current system uses only content-based filtering. You can extend it by:
1. Adding user-item interaction data (ratings, views, bookings)
2. Implementing collaborative filtering algorithms
3. Creating a hybrid system that combines both approaches

### Database Integration

Replace the in-memory storage with a proper database:
1. Add SQLAlchemy models
2. Set up database connections
3. Implement proper CRUD operations

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for FastAPI

## Future Enhancements

- [ ] User feedback collection and model improvement
- [ ] Real-time recommendations with WebSocket support
- [ ] A/B testing framework for recommendation algorithms
- [ ] Event popularity and trending factors
- [ ] Geolocation-based recommendations
- [ ] Social features (friend recommendations)
- [ ] Machine learning model training pipeline
- [ ] Caching layer for improved performance
- [ ] Database persistence
- [ ] User authentication and authorization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License. 