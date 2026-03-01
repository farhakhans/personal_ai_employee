"""
Personal AI Employee - Production Build
Flask App for Vercel Serverless Functions
Optimized for Production Deployment
"""

from flask import Flask, jsonify, make_response, send_from_directory
import os
import logging

# Configure logging for production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app - Vercel needs this 'app' variable
app = Flask(__name__)

# Production configuration
app.config['DEBUG'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Get base directory (Vercel deployment root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cache HTML content for production
HTML_CACHE = {}
CACHE_INITIALIZED = False

def initialize_cache():
    """Initialize HTML cache on first request"""
    global CACHE_INITIALIZED
    if CACHE_INITIALIZED:
        return
    
    logger.info(f"Initializing HTML cache from: {BASE_DIR}")
    try:
        files = os.listdir(BASE_DIR)
        html_files = [f for f in files if f.endswith('.html')]
        logger.info(f"Found {len(html_files)} HTML files")
        
        for filename in html_files:
            try:
                filepath = os.path.join(BASE_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    HTML_CACHE[filename] = f.read()
                logger.info(f"Cached: {filename}")
            except Exception as e:
                logger.error(f"Error caching {filename}: {e}")
        
        CACHE_INITIALIZED = True
        logger.info(f"Cache initialized with {len(HTML_CACHE)} files")
    except Exception as e:
        logger.error(f"Error initializing cache: {e}")


def get_html(filename):
    """Get HTML content from cache"""
    initialize_cache()
    return HTML_CACHE.get(filename)


@app.route('/')
def index():
    """Serve main dashboard"""
    html = get_html('dashboard.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        response.headers['Cache-Control'] = 'public, max-age=3600'
        return response
    
    logger.error("dashboard.html not found")
    return jsonify({
        "error": "dashboard.html not found",
        "base_dir": BASE_DIR
    }), 404


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "personal-ai-employee",
        "platform": "vercel",
        "version": "1.0.0",
        "cached_files": len(HTML_CACHE)
    })


@app.route('/dashboard')
def dashboard():
    """Serve dashboard"""
    html = get_html('dashboard.html')
    if html:
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        response.headers['Cache-Control'] = 'public, max-age=3600'
        return response
    return jsonify({"error": "dashboard.html not found"}), 404


@app.route('/whatsapp-manager')
def whatsapp_manager():
    """Serve WhatsApp Manager"""
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
    return jsonify({
        "servers": ["approval", "email"],
        "status": "ok",
        "tier": "bronze+"
    })


@app.route('/api/debug/files')
def debug_files():
    """Debug endpoint to check available files"""
    try:
        files = os.listdir(BASE_DIR)
        html_files = sorted([f for f in files if f.endswith('.html')])
        return jsonify({
            "base_dir": BASE_DIR,
            "html_files": html_files,
            "total_html": len(html_files),
            "cached": len(HTML_CACHE),
            "cache_initialized": CACHE_INITIALIZED
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
            response.headers['Cache-Control'] = 'public, max-age=3600'
            return response
    
    logger.warning(f"Not found: {filename}")
    return jsonify({
        "error": "Not found",
        "path": filename,
        "base_dir": BASE_DIR
    }), 404


# Initialize cache on module load
initialize_cache()

# Vercel serverless entrypoint
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
