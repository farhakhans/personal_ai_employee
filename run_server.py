"""
Run Main Flask API Server for Personal AI Employee
Includes authentication, dashboard pages, and WhatsApp API
"""

import sys
import os

# Set encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("PERSONAL AI EMPLOYEE - MAIN API SERVER")
print("=" * 60)
print("Starting server on: http://localhost:5000")
print("")
print("Available URLs:")
print("  - http://localhost:5000/              - Login Page")
print("  - http://localhost:5000/main-dashboard - Main Dashboard")
print("  - http://localhost:5000/whatsapp-manager - WhatsApp Manager")
print("  - http://localhost:5000/whatsapp_analysis.html - WhatsApp Analysis")
print("  - http://localhost:5000/bronze        - Bronze Tier")
print("  - http://localhost:5000/silver        - Silver Tier")
print("  - http://localhost:5000/gold          - Gold Tier")
print("  - http://localhost:5000/platinum      - Platinum Tier")
print("")
print("Press Ctrl+C to stop the server")
print("=" * 60)

# Import and run api_routes
from api_routes import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
