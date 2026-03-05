"""
Personal AI Employee - Vercel Deployment
Flask App Entrypoint for Vercel Serverless
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment for Vercel
os.environ['VERCEL'] = '1'
os.environ['VAULT_PATH'] = '/tmp/vault'

# Import Flask app from api_routes
from api_routes import app as flask_app, init_db

# Initialize database
init_db()

# Vercel expects 'app' variable
app = flask_app

# For Vercel serverless
def handler(request):
    """Vercel serverless handler"""
    return flask_app(request.environ, lambda *args: None)

if __name__ == "__main__":
    # Local development
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(debug=True, host="0.0.0.0", port=port)
