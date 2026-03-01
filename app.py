"""
Personal AI Employee - Vercel Deployment
Flask App Entrypoint for Vercel
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Flask app from api_routes
from api_routes import app

# Export app for Vercel
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
