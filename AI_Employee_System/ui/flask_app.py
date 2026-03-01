"""
Complete Flask UI for Personal AI Employee
Serves all dashboards and social media features
"""

from flask import Flask, request, jsonify, send_file, redirect, url_for, send_from_directory
from pathlib import Path
import sys
import os

# Get project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import watchers correctly
from AI_Employee_System.Watchers.facebook_poster import FacebookPoster
from AI_Employee_System.Watchers.instagram_poster import InstagramPoster

# Try to import config, use fallback if not available
try:
    import config
    VAULT_PATH = config.VAULT_PATH
except:
    VAULT_PATH = Path(__file__).resolve().parent.parent.parent / "Vault"


def create_app():
    app = Flask(__name__)
    
    fb = FacebookPoster()
    ig = InstagramPoster()
    
    # HTML files location - Personal AI Employee root folder
    HTML_DIR = r"D:\DocuBook-Chatbot folder\Personal AI Employee"
    
    print(f"HTML_DIR: {HTML_DIR}")

    # Main Social Poster UI
    @app.route('/')
    def index():
        html = """
        <!doctype html>
        <html>
          <head><title>Personal AI Employee - Social Poster</title></head>
          <body style="font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px;">
            <h1>🤖 Personal AI Employee - Social Poster</h1>
            <div style="margin: 20px 0;">
              <h2>📘 Facebook</h2>
              <button onclick="createFacebook()">Create FB Post</button>
              <button onclick="publishFacebook()">Publish FB Post</button>
            </div>
            <div style="margin: 20px 0;">
              <h2>📷 Instagram</h2>
              <button onclick="createInstagram()">Create IG Post</button>
              <button onclick="publishInstagram()">Publish IG Post</button>
            </div>
            <pre id="out" style="background: #f5f5f5; padding: 15px; border-radius: 5px;"></pre>
            <hr>
            <h3>📊 Other Dashboards:</h3>
            <ul>
              <li><a href="/tiers">All Tiers Dashboard</a></li>
              <li><a href="/tier/platinum">Platinum Dashboard</a></li>
              <li><a href="/dashboard">Complete Dashboard</a></li>
            </ul>
            <script>
            async function createFacebook(){
              const res = await fetch('/facebook/create', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({topic:'sales'})});
              const j = await res.json(); document.getElementById('out').innerText = JSON.stringify(j, null, 2);
            }
            async function publishFacebook(){
              const res = await fetch('/facebook/publish', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({message:'Test post'})});
              const j = await res.json(); document.getElementById('out').innerText = JSON.stringify(j, null, 2);
            }
            async function createInstagram(){
              const res = await fetch('/instagram/create', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({topic:'AI'})});
              const j = await res.json(); document.getElementById('out').innerText = JSON.stringify(j, null, 2);
            }
            async function publishInstagram(){
              const res = await fetch('/instagram/publish', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({caption:'Test'})});
              const j = await res.json(); document.getElementById('out').innerText = JSON.stringify(j, null, 2);
            }
            </script>
          </body>
        </html>
        """
        return html

    # Facebook endpoints
    @app.route('/facebook/create', methods=['POST'])
    def facebook_create():
        body = request.json or {}
        topic = body.get('topic', 'AI Automation')
        content_result = fb.generate_post_content(topic, tone='professional')
        return jsonify(content_result)

    @app.route('/facebook/publish', methods=['POST'])
    def facebook_publish():
        body = request.json or {}
        message = body.get('message', 'Test post from AI Employee')
        result = fb.post_to_page(message)
        return jsonify(result)

    # Instagram endpoints
    @app.route('/instagram/create', methods=['POST'])
    def instagram_create():
        body = request.json or {}
        topic = body.get('topic', 'AI Automation')
        content_result = ig.generate_post_content(topic, tone='casual')
        return jsonify(content_result)

    @app.route('/instagram/publish', methods=['POST'])
    def instagram_publish():
        body = request.json or {}
        caption = body.get('caption', 'Test post from AI Employee')
        return jsonify({'success': True, 'message': 'Would post to Instagram', 'caption': caption})

    @app.route('/social/logs', methods=['GET'])
    def social_logs():
        try:
            log_dir = VAULT_PATH / 'System' / 'social_logs'
            out = {}
            for f in sorted(log_dir.glob('*.json')):
                out[f.name] = __import__('json').loads(f.read_text(encoding='utf-8'))
            return jsonify(out)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Dashboard Routes
    @app.route('/tiers')
    def all_tiers():
        try:
            return send_file(os.path.join(HTML_DIR, 'tiers_dashboard.html'))
        except Exception as e:
            return jsonify({'error': str(e)}), 404

    @app.route('/tier/platinum')
    def tier_platinum():
        try:
            return send_file(os.path.join(HTML_DIR, 'platinum_dashboard.html'))
        except Exception as e:
            return jsonify({'error': str(e)}), 404

    @app.route('/dashboard')
    def dashboard():
        try:
            return send_file(os.path.join(HTML_DIR, 'complete_dashboard.html'))
        except Exception as e:
            return jsonify({'error': str(e)}), 404

    # Watcher Run Routes
    @app.route('/run/gmail')
    def run_gmail():
        try:
            import subprocess
            result = subprocess.run(
                ['python', 'Watchers/gmail_watcher.py'],
                cwd=str(PROJECT_ROOT / 'AI_Employee_System'),
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout + result.stderr
            return jsonify({'success': True, 'output': output})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/run/whatsapp')
    def run_whatsapp():
        try:
            import subprocess
            result = subprocess.run(
                ['python', 'Watchers/whatsapp_watcher.py'],
                cwd=str(PROJECT_ROOT / 'AI_Employee_System'),
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout + result.stderr
            return jsonify({'success': True, 'output': output})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/run/linkedin')
    def run_linkedin():
        try:
            import subprocess
            result = subprocess.run(
                ['python', 'Watchers/linkedin_poster.py'],
                cwd=str(PROJECT_ROOT / 'AI_Employee_System'),
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout + result.stderr
            return jsonify({'success': True, 'output': output})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/run/hitl')
    def run_hitl():
        try:
            import subprocess
            result = subprocess.run(
                ['python', 'hitl_framework.py'],
                cwd=str(PROJECT_ROOT / 'AI_Employee_System'),
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout + result.stderr
            return jsonify({'success': True, 'output': output})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    @app.route('/tier/bronze')
    def tier_bronze():
        return redirect(url_for('index'))
    
    @app.route('/tier/silver')
    def tier_silver():
        return redirect(url_for('index'))
    
    @app.route('/tier/gold')
    def tier_gold():
        return redirect(url_for('index'))

    return app


if __name__ == '__main__':
    import sys
    # Set UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 70)
    print("PERSONAL AI EMPLOYEE - FLASK UI SERVER")
    print("=" * 70)
    print("Starting server on: http://localhost:5001")
    print("")
    print("Available Dashboards:")
    print("  - http://localhost:5001/           - Social Poster")
    print("  - http://localhost:5001/tiers      - All Tiers")
    print("  - http://localhost:5001/tier/platinum - Platinum")
    print("  - http://localhost:5001/dashboard  - Complete Dashboard")
    print("")
    print("Press Ctrl+C to stop the server")
    print("=" * 70)

    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=False)
