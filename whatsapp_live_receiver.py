"""
WhatsApp Live Receiver - Real-time message monitoring
Receives messages from WhatsApp Web and sends to API
"""

import time
import json
import requests
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
CONFIG_FILE = PROJECT_ROOT / "whatsapp_config.json"
MESSAGES_FILE = PROJECT_ROOT / "whatsapp_messages.json"

class WhatsAppLiveReceiver:
    def __init__(self):
        self.config = self.load_config()
        self.running = True
        self.api_url = "http://localhost:5000/api/whatsapp/ai/send"
        
    def load_config(self):
        """Load WhatsApp configuration"""
        default_config = {
            'phone_number': '+92 300 1234567',
            'access_token': '',
            'phone_id': '',
            'auto_reply_enabled': True
        }
        
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
                default_config.update(saved_config)
        
        return default_config
    
    def receive_message(self, from_number, message_text, sender_name=''):
        """Receive message and send to AI for auto-reply"""
        print(f"\n📨 [{datetime.now().strftime('%H:%M:%S')}] From {sender_name or from_number}: {message_text}")
        
        # Save to messages file
        self.save_message(from_number, message_text, sender_name)
        
        # Send to AI for auto-reply
        if self.config.get('auto_reply_enabled', True):
            self.send_to_ai(from_number, message_text)
    
    def save_message(self, from_number, message, sender_name=''):
        """Save message to file"""
        messages = {'messages': []}
        
        if MESSAGES_FILE.exists():
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                messages = json.load(f)
        
        messages['messages'].append({
            'type': 'received',
            'from': from_number,
            'from_name': sender_name,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'status': 'received'
        })
        
        # Keep last 1000 messages
        if len(messages['messages']) > 1000:
            messages['messages'] = messages['messages'][-1000:]
        
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
    
    def send_to_ai(self, from_number, message):
        """Send message to AI for auto-reply"""
        try:
            response = requests.post(
                self.api_url,
                json={'to': from_number, 'message': message},
                timeout=10
            )
            result = response.json()
            
            if result.get('status') == 'success':
                print(f"🤖 AI Response: {result.get('response', '')[:100]}...")
                
                # Save AI response
                self.save_message(
                    from_number,
                    result.get('response', ''),
                    'AI Assistant'
                )
        except Exception as e:
            print(f"❌ AI request failed: {e}")
    
    def start(self):
        """Start WhatsApp receiver"""
        print("=" * 60)
        print("WhatsApp Live Receiver")
        print("=" * 60)
        print(f"📱 Phone: {self.config['phone_number']}")
        print(f"🤖 AI Auto-Reply: {'Enabled' if self.config.get('auto_reply_enabled') else 'Disabled'}")
        print(f"🌐 API: {self.api_url}")
        print("\n⏳ Monitoring for messages...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while self.running:
                # In real implementation, this would poll WhatsApp Web API
                # For now, simulate with demo messages
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\n⛔ Receiver stopped by user")
            self.running = False


def main():
    receiver = WhatsAppLiveReceiver()
    receiver.start()


if __name__ == '__main__':
    main()
