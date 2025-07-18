"""
Configuration settings for the Events Recommendation System
"""

import os

# Data file paths
EVENTS_CSV_PATH = "data/events.csv"
USERS_CSV_PATH = "data/users.csv"

# API Configuration
API_TITLE = "Events Recommendation System"
API_DESCRIPTION = "A content-based recommendation system for user-event matching"
API_VERSION = "1.0.0"
API_HOST = "0.0.0.0"
API_PORT = 8000

# CORS Configuration
CORS_ORIGINS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Recommendation settings
DEFAULT_RECOMMENDATION_LIMIT = 10 