from flask import Flask, jsonify, request, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "success",
        "message": "Personal AI Employee API is running on Vercel!",
        "version": "1.0.0"
    })

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "personal-ai-employee",
        "platform": "vercel"
    })

@app.route('/dashboard')
def dashboard():
    return jsonify({
        "page": "dashboard",
        "status": "ok",
        "message": "Dashboard endpoint working"
    })

@app.route('/whatsapp-manager')
def whatsapp_manager():
    return jsonify({
        "page": "whatsapp-manager",
        "status": "ok"
    })

@app.route('/api/mcp/servers')
def mcp_servers():
    return jsonify({
        "servers": ["approval", "email"],
        "status": "ok"
    })

# Catch-all for static files
@app.route('/<path:path>')
def static_files(path):
    return jsonify({
        "path": path,
        "message": "Route exists"
    })

if __name__ == '__main__':
    app.run(debug=True)
