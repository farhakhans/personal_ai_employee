"""
Personal AI Employee - Vercel Serverless Entry Point
Simplified for Vercel deployment
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment for Vercel
os.environ['VERCEL'] = '1'
os.environ['VAULT_PATH'] = '/tmp/vault'

# Import Flask app
from api_routes import app

# Vercel serverless handler
def handler(request):
    """Vercel serverless handler for Python"""
    return app(request.environ, lambda *args: None)

# For local testing
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
