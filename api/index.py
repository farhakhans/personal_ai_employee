"""
Vercel Serverless Function for Personal AI Employee
Flask App Entrypoint
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Flask app from api_routes
from api_routes import app

# Vercel expects 'app' variable as entrypoint
app = app

if __name__ == "__main__":
    app.run(debug=True)
