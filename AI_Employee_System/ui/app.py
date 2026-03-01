"""
Simple Flask UI to trigger Facebook and Instagram poster actions and view logs.
Run: `python AI_Employee_System/ui/test_ui.py` to run automated smoke tests.
"""

from flask import Flask, request, jsonify, render_template_string, send_file, redirect, url_for
from pathlib import Path
import sys
import os

# Ensure project root importable
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from AI_Employee_System.Watchers.facebook_poster import FacebookPoster
from AI_Employee_System.Watchers.instagram_poster import InstagramPoster
import config


def create_app():
    app = Flask(__name__)

    fb = FacebookPoster()
    ig = InstagramPoster()
    
    # Get the parent directory for HTML files (Personal AI Employee folder)
    HTML_ROOT = Path(__file__).resolve().parents[3]
    
    print(f"HTML_ROOT: {HTML_ROOT}")  # Debug print

    HTML = """
    <!doctype html>
    <html>
      <head><title>Social Poster UI</title></head>
      <body>
        <h1>Social Poster UI</h1>
        <div>
          <h2>Facebook</h2>
          <button onclick="createFacebook()">Create FB Post</button>
          <button onclick="publishFacebook()">Publish Last FB Post</button>
        </div>
        <div>
          <h2>Instagram</h2>
          <button onclick="createInstagram()">Create IG Post</button>
          <button onclick="publishInstagram()">Publish Last IG Post</button>
        </div>
        <pre id="out"></pre>

        <script>
        async function createFacebook(){
          const res = await fetch('/facebook/create', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({topic:'sales', details:{action:'helped a client', text:'Saved 30% costs'}})});
          const j = await res.json(); document.getElementById('out').innerText = JSON.stringify(j, null, 2);
        }
        async function publishFacebook(){
          const res = await fetch('/facebook/publish', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({})});
          const j = await res.json(); document.getElementById('out').innerText = JSON.stringify(j, null, 2);
        }
        async function createInstagram(){
          const res = await fetch('/instagram/create', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({text:'Automating business tasks with AI.'})});
          const j = await res.json(); document.getElementById('out').innerText = JSON.stringify(j, null, 2);
        }
        async function publishInstagram(){
          const res = await fetch('/instagram/publish', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({})});
          const j = await res.json(); document.getElementById('out').innerText = JSON.stringify(j, null, 2);
        }
        </script>
      </body>
    </html>
    """

    @app.route('/')
    def index():
        return render_template_string(HTML)

    # Facebook endpoints
    @app.route('/facebook/create', methods=['POST'])
    def facebook_create():
        body = request.json or {}
        topic = body.get('topic', 'AI Automation')
        details = body.get('details', {})
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
        text = body.get('text', 'Automated post')
        content_result = ig.generate_post_content(topic, tone='casual')
        return jsonify(content_result)

    @app.route('/instagram/publish', methods=['POST'])
    def instagram_publish():
        body = request.json or {}
        caption = body.get('caption', 'Test post from AI Employee')
        # For demo, just return success (actual post would need image URL)
        return jsonify({'success': True, 'message': 'Would post to Instagram', 'caption': caption})

    @app.route('/social/logs', methods=['GET'])
    def social_logs():
        try:
            log_dir = config.VAULT_PATH / 'System' / 'social_logs'
            out = {}
            for f in sorted(log_dir.glob('*.json')):
                out[f.name] = __import__('json').loads(f.read_text(encoding='utf-8'))
            return jsonify(out)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Tier Dashboard Routes
    @app.route('/tier/bronze')
    def tier_bronze():
        return redirect(url_for('index'))
    
    @app.route('/tier/silver')
    def tier_silver():
        return redirect(url_for('index'))
    
    @app.route('/tier/gold')
    def tier_gold():
        return redirect(url_for('index'))
    
    @app.route('/tier/platinum')
    def tier_platinum():
        try:
            html_path = r"D:\DocuBook-Chatbot folder\Personal AI Employee\platinum_dashboard.html"
            return send_file(html_path)
        except Exception as e:
            return jsonify({'error': str(e)}), 404
    
    @app.route('/tiers')
    def all_tiers():
        try:
            html_path = r"D:\DocuBook-Chatbot folder\Personal AI Employee\tiers_dashboard.html"
            return send_file(html_path)
        except Exception as e:
            return jsonify({'error': str(e)}), 404
    
    @app.route('/dashboard')
    def dashboard():
        try:
            html_path = r"D:\DocuBook-Chatbot folder\Personal AI Employee\complete_dashboard.html"
            return send_file(html_path)
        except Exception as e:
            return jsonify({'error': str(e)}), 404

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5001, debug=False)
