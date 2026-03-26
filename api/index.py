"""
Personal AI Employee - Vercel Deployment
Flask App for Vercel Serverless Functions
"""

from flask import Flask, jsonify, make_response
import os

# Create Flask app - Vercel needs this 'app' variable
app = Flask(__name__)

# Get base directory - try multiple paths for Vercel compatibility
def get_base_dir():
    """Get the base directory where HTML files are located"""
    # Current file location
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try parent directory first (api/ is subfolder)
    parent_dir = os.path.dirname(current_dir)
    
    # Check if login_custom.html exists in parent
    if os.path.exists(os.path.join(parent_dir, 'login_custom.html')):
        return parent_dir
    
    # Try current directory
    if os.path.exists(os.path.join(current_dir, 'login_custom.html')):
        return current_dir
    
    # Try /vercel/path0 (Vercel deployment path)
    vercel_path = '/vercel/path0'
    if os.path.exists(vercel_path) and os.path.exists(os.path.join(vercel_path, 'login_custom.html')):
        return vercel_path
    
    # Default to parent
    return parent_dir

BASE_DIR = get_base_dir()

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
    # Try login_custom.html first (main login page)
    html = get_html('login_custom.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    
    # Fallback to complete_dashboard.html
    html = get_html('complete_dashboard.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    
    # Last fallback - dashboard.html
    html = get_html('dashboard.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    
    return jsonify({"error": "No HTML files found", "base_dir": BASE_DIR}), 404


@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "personal-ai-employee",
        "platform": "vercel"
    })


@app.route('/api/debug/files')
def debug_files():
    """Debug endpoint to see available files"""
    try:
        files = os.listdir(BASE_DIR)
        html_files = [f for f in files if f.endswith('.html')]
        return jsonify({
            "base_dir": BASE_DIR,
            "html_files": html_files[:50],
            "total_html": len(html_files),
            "all_files": files[:20]
        })
    except Exception as e:
        return jsonify({"error": str(e), "base_dir": BASE_DIR})


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


@app.route('/login_custom.html')
def login_custom():
    html = get_html('login_custom.html')
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
