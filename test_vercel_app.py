"""
Vercel Deployment Test
Simple Flask app for testing
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        "status": "success",
        "message": "Personal AI Employee is running on Vercel!",
        "endpoints": [
            "/",
            "/dashboard",
            "/whatsapp-manager",
            "/api/mcp/servers"
        ]
    })

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "service": "personal-ai-employee"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
