"""
Configuration settings for the Vaimo Event Recommendation System
Supports environment variables for containerized deployments
"""

import os

# Data file paths - can be overridden with environment variables
EVENTS_CSV_PATH = os.getenv("EVENTS_CSV_PATH", "data/events.csv")
USERS_CSV_PATH = os.getenv("USERS_CSV_PATH", "data/users.csv")

# API Configuration - Docker-friendly defaults
API_TITLE = os.getenv("API_TITLE", "Vaimo Event Recommendation System")
API_DESCRIPTION = os.getenv("API_DESCRIPTION", "A content-based recommendation system for user-event matching")
API_VERSION = os.getenv("API_VERSION", "1.0.0")
API_HOST = os.getenv("API_HOST", "0.0.0.0")  # 0.0.0.0 for Docker
API_PORT = int(os.getenv("API_PORT", "8000"))

# CORS Configuration - can be restricted in production
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") != "*" else ["*"]
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Recommendation settings
DEFAULT_RECOMMENDATION_LIMIT = int(os.getenv("DEFAULT_RECOMMENDATION_LIMIT", "10"))

# Environment info
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true" 