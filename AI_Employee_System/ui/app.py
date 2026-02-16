"""
Simple Flask UI to trigger Facebook and Instagram poster actions and view logs.
Run: `python AI_Employee_System/ui/test_ui.py` to run automated smoke tests.
"""

from flask import Flask, request, jsonify, render_template_string
from pathlib import Path
import sys

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
        topic = body.get('topic', 'default')
        details = body.get('details', {})
        content = fb.generate_post(topic, details)
        post = fb.create_post(content)
        return jsonify(post)

    @app.route('/facebook/publish', methods=['POST'])
    def facebook_publish():
        # publish the last draft
        try:
            arr = fb.posts_file.read_text(encoding='utf-8')
            posts = __import__('json').loads(arr)
            if not posts:
                return jsonify({'status':'error','message':'no posts'}), 400
            last = posts[-1]['post_id']
            res = fb.publish_post(last)
            return jsonify(res)
        except Exception as e:
            return jsonify({'status':'error','message': str(e)}), 500

    # Instagram endpoints
    @app.route('/instagram/create', methods=['POST'])
    def instagram_create():
        body = request.json or {}
        text = body.get('text', 'Automated post')
        caption = ig.generate_caption('automation', text)
        post = ig.create_post(caption)
        return jsonify(post)

    @app.route('/instagram/publish', methods=['POST'])
    def instagram_publish():
        try:
            arr = ig.posts_file.read_text(encoding='utf-8')
            posts = __import__('json').loads(arr)
            if not posts:
                return jsonify({'status':'error','message':'no posts'}), 400
            last = posts[-1]['post_id']
            res = ig.publish_post(last)
            return jsonify(res)
        except Exception as e:
            return jsonify({'status':'error','message': str(e)}), 500

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

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5001, debug=False)
