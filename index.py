"""
Personal AI Employee - Vercel Production Build
Minimal Flask App for Testing
"""

from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Personal AI Employee</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>✅ Personal AI Employee is Running on Vercel!</h1>
        <p>Production deployment successful!</p>
        <h2>Available Endpoints:</h2>
        <ul>
            <li><a href="/api/health">/api/health</a></li>
            <li><a href="/dashboard">/dashboard</a></li>
            <li><a href="/whatsapp-manager">/whatsapp-manager</a></li>
        </ul>
    </body>
    </html>
    '''

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "personal-ai-employee",
        "platform": "vercel",
        "version": "1.0.0"
    })

@app.route('/dashboard')
def dashboard():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Dashboard Page</h1>
        <p>Dashboard is working!</p>
        <a href="/">← Back to Home</a>
    </body>
    </html>
    '''

@app.route('/whatsapp-manager')
def whatsapp():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>WhatsApp Manager</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>WhatsApp Manager</h1>
        <p>WhatsApp Manager is working!</p>
        <a href="/">← Back to Home</a>
    </body>
    </html>
    '''

@app.route('/api/debug/info')
def debug():
    return jsonify({
        "message": "Debug endpoint working",
        "routes": ["/", "/api/health", "/dashboard", "/whatsapp-manager"]
    })

if __name__ == '__main__':
    app.run(debug=False)
