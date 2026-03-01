from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "success",
        "message": "Personal AI Employee API is running!",
        "timestamp": "2026-03-01"
    })

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "service": "personal-ai-employee"})

@app.route('/dashboard')
def dashboard():
    return jsonify({"page": "dashboard", "status": "ok"})
