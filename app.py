"""
Personal AI Employee - Vercel Deployment
Flask App Entrypoint for Vercel Serverless
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Flask app from api_routes
from api_routes import app as flask_app

# Vercel expects 'app' variable
app = flask_app

# For Vercel serverless
def handler(request):
    """Vercel serverless handler"""
    return flask_app(request.environ, lambda *args: None)

if __name__ == "__main__":
    flask_app.run(debug=True, host="0.0.0.0", port=8080)
