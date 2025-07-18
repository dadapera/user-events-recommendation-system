#!/usr/bin/env python3
"""
Events Recommendation System - Startup Script
Run this script to start the FastAPI server
"""

import uvicorn

if __name__ == "__main__":
    # Run the FastAPI app from the app module
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 