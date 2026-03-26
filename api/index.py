"""
Personal AI Employee - Vercel Deployment
Flask App for Vercel Serverless Functions
"""

from flask import Flask, jsonify, make_response
import os

# Create Flask app - Vercel needs this 'app' variable
app = Flask(__name__)

# Get base directory (Vercel deployment root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cache HTML content
HTML_CACHE = {}

def read_html_file(filename):
    try:
        filepath = os.path.join(BASE_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

def get_html(filename):
    if filename not in HTML_CACHE:
        HTML_CACHE[filename] = read_html_file(filename)
    return HTML_CACHE[filename]


@app.route('/')
def index():
    html = get_html('dashboard.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    return jsonify({"error": "dashboard.html not found"}), 404


@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "personal-ai-employee",
        "platform": "vercel"
    })


@app.route('/dashboard')
def dashboard():
    html = get_html('dashboard.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    return jsonify({"error": "dashboard.html not found"}), 404


@app.route('/whatsapp-manager')
def whatsapp_manager():
    html = get_html('whatsapp_manager.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    return jsonify({"error": "whatsapp_manager.html not found"}), 404


@app.route('/whatsapp_analysis.html')
def whatsapp_analysis():
    html = get_html('whatsapp_analysis.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    return jsonify({"error": "File not found"}), 404


@app.route('/banking_system.html')
def banking_system():
    html = get_html('banking_system.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    return jsonify({"error": "File not found"}), 404


@app.route('/analytics.html')
def analytics():
    html = get_html('analytics.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    return jsonify({"error": "File not found"}), 404


@app.route('/bronze_dashboard.html')
def bronze_dashboard():
    html = get_html('bronze_dashboard.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    return jsonify({"error": "File not found"}), 404


@app.route('/silver_dashboard.html')
def silver_dashboard():
    html = get_html('silver_dashboard.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    return jsonify({"error": "File not found"}), 404


@app.route('/gold_dashboard.html')
def gold_dashboard():
    html = get_html('gold_dashboard.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    return jsonify({"error": "File not found"}), 404


@app.route('/platinum_dashboard.html')
def platinum_dashboard():
    html = get_html('platinum_dashboard.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    return jsonify({"error": "File not found"}), 404


@app.route('/complete_dashboard.html')
def complete_dashboard():
    html = get_html('complete_dashboard.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    return jsonify({"error": "File not found"}), 404


@app.route('/agent-skills')
def agent_skills():
    return jsonify({"status": "ok", "message": "Agent Skills endpoint"})


@app.route('/api/mcp/servers')
def mcp_servers():
    return jsonify({"servers": ["approval", "email"], "status": "ok"})


@app.route('/api/debug/files')
def debug_files():
    try:
        files = os.listdir(BASE_DIR)
        html_files = [f for f in files if f.endswith('.html')]
        return jsonify({
            "base_dir": BASE_DIR,
            "html_files": html_files[:30],
            "total_html": len(html_files)
        })
    except Exception as e:
        return jsonify({"error": str(e), "base_dir": BASE_DIR})


# Catch-all for other HTML files
@app.route('/<path:filename>')
def serve_html(filename):
    if filename.endswith('.html'):
        html = get_html(filename)
        if html:
            response = make_response(html)
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            return response
    
    return jsonify({
        "error": "Not found",
        "path": filename
    }), 404


# Vercel expects this for serverless
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

# Vercel serverless handler
def handler(request):
    """Vercel serverless handler"""
    return app(request.environ, lambda *args: None)
