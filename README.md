# Vaimo Event Recommendation System

A content-based recommendation system built with FastAPI for matching users with relevant events based on their preferences and interests. The system loads data from CSV files to simulate reading from a remote database.

## Features

- **Content-Based Filtering**: Recommends events based on simple category matching between user preferences and events
- **Simple Scoring**: Events matching user's preferred categories get a score of 1.0, others get 0.0
- **CSV Data Loading**: Loads events and users from CSV files on startup to simulate remote database access
- **RESTful API**: Clean FastAPI endpoints for retrieving events and getting recommendations
- **Explainable Recommendations**: Each recommendation comes with a human-readable explanation

## Architecture

```
vaimo_recom_sys/
├── app/                       # Main application package
│   ├── __init__.py           # Package init file
│   ├── main.py               # FastAPI application and API endpoints
│   ├── models.py             # Pydantic data models
│   ├── recommendation_engine.py # Content-based recommendation logic
│   └── config.py             # Configuration settings
├── data/                      # Data files
│   ├── events.csv            # Sample events data (simulates remote DB)
│   └── users.csv             # Sample users and preferences data
├── tests/                     # Test files
│   ├── __init__.py           # Test package init
│   └── test_recommendations.py # Test script with examples
├── docs/                      # Documentation (future use)
├── run.py                     # Application startup script
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Project Structure

### `/app/` - Main Application Package
- **`main.py`** - FastAPI application with API endpoints
- **`models.py`** - Pydantic data models for validation
- **`recommendation_engine.py`** - Content-based recommendation logic
- **`config.py`** - Centralized configuration settings
- **`__init__.py`** - Package initialization

### `/data/` - Data Files
- **`events.csv`** - Sample events data with columns: event_id, title, description, category, tags (semicolon-separated), location, date, price, organizer, capacity, rating
- **`users.csv`** - Sample users and preferences with columns: user_id, name, email, age, location, created_at, categories (semicolon-separated preferences)

### `/tests/` - Test Suite
- **`test_recommendations.py`** - API and functionality tests
- **`__init__.py`** - Test package initialization

### `/docs/` - Documentation
- Future documentation files

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
python run.py
```

Or run directly with uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000` and automatically load data from CSV files on each request.

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

### API Endpoints

- **GET** `/events/` - Get all events
- **GET** `/users/{user_id}/recommendations/` - Get personalized recommendations

### Testing

Run the test script to see the system in action:

```bash
python tests/test_recommendations.py
```

Or from the project root:
```bash
python -m pytest tests/
```

This will:
1. Test the API endpoints
2. Retrieve all events
3. Generate recommendations for each user based on their CSV-defined preferences
4. Display results with explanations

## Example Usage

### 1. Get All Events

```python
import requests

response = requests.get("http://localhost:8000/events/")
events = response.json()

for event in events:
    print(f"Event: {event['title']}")
    print(f"Category: {event['category']}")
    print(f"Location: {event['location']}")
    print(f"Price: ${event['price']}")
    print("---")
```

### 2. Get Recommendations for a User

```python
response = requests.get(
    "http://localhost:8000/users/user_1/recommendations/?limit=5"
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
- **3 sample users** with different category preferences:
  - Alice (user_1): Technology, Business
  - Bob (user_2): Music, Art  
  - Carol (user_3): Food, Art, Business
- **8 diverse events** across categories (Technology, Music, Art, Business, Food)
- Events located in New York, San Francisco, and Los Angeles

## Extending the System

### Adding New Data

1. **Add Events**: Edit `data/events.csv` to include new events
2. **Add Users**: Edit `data/users.csv` to include new users and their preferences
3. **No Restart Needed**: Data is loaded on-demand with each request

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

Replace the CSV loading with a proper database:
1. Add SQLAlchemy models
2. Set up database connections
3. Implement proper CRUD operations
4. Replace CSV loading functions with database queries

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for FastAPI
- **CSV**: Simple data storage format for demo purposes

## Configuration

The system uses a centralized configuration file (`app/config.py`) for easy customization:

- **Data paths**: CSV file locations
- **API settings**: Title, description, version, host, port
- **CORS settings**: Cross-origin resource sharing configuration
- **Recommendation settings**: Default limits and parameters

To modify settings, edit `app/config.py` and restart the server.

## Future Enhancements

- [ ] User feedback collection and model improvement
- [ ] Real-time recommendations with WebSocket support
- [ ] A/B testing framework for recommendation algorithms
- [ ] Event popularity and trending factors
- [ ] Geolocation-based recommendations
- [ ] Social features (friend recommendations)
- [ ] Machine learning model training pipeline
- [ ] Caching layer for improved performance
- [ ] Database persistence (replace CSV files)
- [ ] User authentication and authorization
- [ ] Admin endpoints for managing events and users

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License. 