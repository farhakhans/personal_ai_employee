"""
WhatsApp Web Controller - Integrated with WhatsApp Manager
Opens WhatsApp Web in browser and monitors messages
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import threading
import json
from pathlib import Path
import asyncio

app = Flask(__name__)
CORS(app)

PROJECT_ROOT = Path(__file__).parent
whatsapp_receiver_process = None
is_running = False

def run_whatsapp_receiver():
    """Run WhatsApp receiver in background"""
    global whatsapp_receiver_process, is_running
    
    try:
        # Start the receiver
        whatsapp_receiver_process = subprocess.Popen(
            ['python', str(PROJECT_ROOT / 'run_whatsapp_receiver.py')],
            cwd=str(PROJECT_ROOT),
            creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0
        )
        is_running = True
        print("✅ WhatsApp Receiver started!")
    except Exception as e:
        print(f"❌ Error starting receiver: {e}")
        is_running = False

@app.route('/start-whatsapp', methods=['POST'])
def start_whatsapp():
    """Start WhatsApp receiver"""
    global is_running
    
    if is_running:
        return jsonify({
            'status': 'already_running',
            'message': 'WhatsApp receiver is already running'
        })
    
    # Start in background thread
    thread = threading.Thread(target=run_whatsapp_receiver, daemon=True)
    thread.start()
    
    return jsonify({
        'status': 'started',
        'message': 'WhatsApp receiver starting... Browser will open for QR scan'
    })

@app.route('/stop-whatsapp', methods=['POST'])
def stop_whatsapp():
    """Stop WhatsApp receiver"""
    global whatsapp_receiver_process, is_running
    
    if whatsapp_receiver_process:
        try:
            whatsapp_receiver_process.terminate()
            is_running = False
            return jsonify({
                'status': 'stopped',
                'message': 'WhatsApp receiver stopped'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    return jsonify({
        'status': 'not_running',
        'message': 'WhatsApp receiver is not running'
    })

@app.route('/whatsapp-status')
def whatsapp_status():
    """Get WhatsApp receiver status"""
    return jsonify({
        'is_running': is_running,
        'status': 'running' if is_running else 'stopped'
    })

@app.route('/whatsapp-web')
def whatsapp_web():
    """Open WhatsApp Web directly"""
    import webbrowser
    webbrowser.open('https://web.whatsapp.com')
    return jsonify({
        'status': 'opened',
        'message': 'WhatsApp Web opened in browser'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
