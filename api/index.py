from flask import Flask, jsonify, send_file, request, make_response
import os
import mimetypes

app = Flask(__name__)

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set proper MIME types
mimetypes.add_type('text/html', '.html')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

@app.route('/')
def index():
    response = make_response(send_file(os.path.join(BASE_DIR, 'dashboard.html')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "personal-ai-employee",
        "platform": "vercel"
    })

@app.route('/dashboard')
def dashboard():
    response = make_response(send_file(os.path.join(BASE_DIR, 'dashboard.html')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/whatsapp-manager')
def whatsapp_manager():
    response = make_response(send_file(os.path.join(BASE_DIR, 'whatsapp_manager.html')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/whatsapp_analysis.html')
def whatsapp_analysis():
    response = make_response(send_file(os.path.join(BASE_DIR, 'whatsapp_analysis.html')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/banking_system.html')
def banking_system():
    response = make_response(send_file(os.path.join(BASE_DIR, 'banking_system.html')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/analytics.html')
def analytics():
    response = make_response(send_file(os.path.join(BASE_DIR, 'analytics.html')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/bronze_dashboard.html')
def bronze_dashboard():
    response = make_response(send_file(os.path.join(BASE_DIR, 'bronze_dashboard.html')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/silver_dashboard.html')
def silver_dashboard():
    response = make_response(send_file(os.path.join(BASE_DIR, 'silver_dashboard.html')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/gold_dashboard.html')
def gold_dashboard():
    response = make_response(send_file(os.path.join(BASE_DIR, 'gold_dashboard.html')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/platinum_dashboard.html')
def platinum_dashboard():
    response = make_response(send_file(os.path.join(BASE_DIR, 'platinum_dashboard.html')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/complete_dashboard.html')
def complete_dashboard():
    response = make_response(send_file(os.path.join(BASE_DIR, 'complete_dashboard.html')))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

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
            response = make_response(send_file(filepath))
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            return response
    
    return jsonify({
        "error": "Not found",
        "path": filename
    }), 404

if __name__ == '__main__':
    app.run(debug=True)
