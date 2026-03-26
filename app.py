"""
Personal AI Employee - Vercel Deployment
Flask App Entrypoint for Vercel Serverless
"""

import sys
import os
import traceback

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment for Vercel
os.environ['VERCEL'] = '1'
os.environ['VAULT_PATH'] = '/tmp/vault'

# Disable heavy imports for Vercel
os.environ['VERCEL_SERVERLESS'] = '1'

try:
    # Import Flask app from api_routes
    from api_routes import app as flask_app, init_db

    # Initialize database
    init_db()

    # Vercel expects 'app' variable
    app = flask_app

    # For Vercel serverless
    def handler(request):
        """Vercel serverless handler"""
        try:
            return flask_app(request.environ, lambda *args: None)
        except Exception as e:
            print(f"Request error: {str(e)}")
            print(traceback.format_exc())
            raise

except Exception as e:
    print(f"Import error: {str(e)}")
    print(traceback.format_exc())

    # Fallback app for errors
    from flask import Flask, jsonify
    app = Flask(__name__)

    @app.route('/')
    def error_page():
        return jsonify({
            'error': 'Failed to load app',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

    def handler(request):
        return app(request.environ, lambda *args: None)

if __name__ == "__main__":
    # Local development
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(debug=True, host="0.0.0.0", port=port)
