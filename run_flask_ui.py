"""
Run Flask UI Server for Personal AI Employee
"""

import sys
import os

# Set encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add UI directory to Python path (don't change directory)
ui_path = os.path.join(os.path.dirname(__file__), 'AI_Employee_System', 'ui')
sys.path.insert(0, ui_path)

# Import and run
from flask_app import create_app

print("=" * 60)
print("PERSONAL AI EMPLOYEE - FLASK UI SERVER")
print("=" * 60)
print("Starting server on: http://localhost:5001")
print("")
print("Available Dashboards:")
print("  - http://localhost:5001/            - Social Poster")
print("  - http://localhost:5001/tiers       - All Tiers")
print("  - http://localhost:5001/tier/platinum - Platinum")
print("  - http://localhost:5001/dashboard   - Complete Dashboard")
print("")
print("Press Ctrl+C to stop the server")
print("=" * 60)

app = create_app()
app.run(host='0.0.0.0', port=5001, debug=False)
