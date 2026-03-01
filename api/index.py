from flask import Flask, jsonify, send_file, request
import os

app = Flask(__name__)

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.route('/')
def index():
    return send_file(os.path.join(BASE_DIR, 'dashboard.html'))

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "personal-ai-employee",
        "platform": "vercel"
    })

@app.route('/dashboard')
def dashboard():
    return send_file(os.path.join(BASE_DIR, 'dashboard.html'))

@app.route('/whatsapp-manager')
def whatsapp_manager():
    return send_file(os.path.join(BASE_DIR, 'whatsapp_manager.html'))

@app.route('/whatsapp_analysis.html')
def whatsapp_analysis():
    return send_file(os.path.join(BASE_DIR, 'whatsapp_analysis.html'))

@app.route('/banking_system.html')
def banking_system():
    return send_file(os.path.join(BASE_DIR, 'banking_system.html'))

@app.route('/analytics.html')
def analytics():
    return send_file(os.path.join(BASE_DIR, 'analytics.html'))

@app.route('/bronze_dashboard.html')
def bronze_dashboard():
    return send_file(os.path.join(BASE_DIR, 'bronze_dashboard.html'))

@app.route('/silver_dashboard.html')
def silver_dashboard():
    return send_file(os.path.join(BASE_DIR, 'silver_dashboard.html'))

@app.route('/gold_dashboard.html')
def gold_dashboard():
    return send_file(os.path.join(BASE_DIR, 'gold_dashboard.html'))

@app.route('/platinum_dashboard.html')
def platinum_dashboard():
    return send_file(os.path.join(BASE_DIR, 'platinum_dashboard.html'))

@app.route('/complete_dashboard.html')
def complete_dashboard():
    return send_file(os.path.join(BASE_DIR, 'complete_dashboard.html'))

@app.route('/agent-skills')
def agent_skills():
    return jsonify({
        "status": "ok",
        "message": "Agent Skills endpoint"
    })

@app.route('/api/mcp/servers')
def mcp_servers():
    return jsonify({
        "servers": ["approval", "email"],
        "status": "ok"
    })

# Catch-all for other HTML files
@app.route('/<path:filename>')
def serve_html(filename):
    if filename.endswith('.html'):
        filepath = os.path.join(BASE_DIR, filename)
        if os.path.exists(filepath):
            return send_file(filepath)
    
    return jsonify({
        "error": "Not found",
        "path": filename
    }), 404

if __name__ == '__main__':
    app.run(debug=True)
