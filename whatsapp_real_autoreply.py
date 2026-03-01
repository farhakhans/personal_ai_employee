"""
WhatsApp Real Auto-Reply System
Integrates with WhatsApp Business API for real message handling
"""

import json
import requests
import time
from datetime import datetime
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent
CONFIG_FILE = PROJECT_ROOT / "whatsapp_config.json"
MESSAGES_FILE = PROJECT_ROOT / "whatsapp_messages.json"

class WhatsAppAutoReply:
    def __init__(self):
        self.config = self.load_config()
        self.messages = self.load_messages()
        self.auto_reply_enabled = True
        self.keywords = self.load_keywords()
        
    def load_config(self):
        """Load WhatsApp configuration"""
        default_config = {
            'phone_number': '+92 300 1234567',
            'access_token': '',  # WhatsApp Business API Token
            'phone_id': '',  # WhatsApp Phone ID
            'webhook_verify_token': 'my_verify_token_123',
            'greeting_message': 'Assalam-o-Alaikum! Thank you for contacting AI Employee System. How can we help you today?',
            'business_hours_message': 'We are currently away but will respond within 24 hours.',
            'auto_reply_enabled': True
        }
        
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
                default_config.update(saved_config)
        
        return default_config
    
    def load_keywords(self):
        """Load keyword triggers"""
        default_keywords = [
            {'keyword': 'price', 'response': 'Our pricing starts at $99/month. Would you like to schedule a demo?'},
            {'keyword': 'payment', 'response': 'You can make payment via bank transfer. Account: 1234567890'},
            {'keyword': 'order', 'response': 'To place an order, please provide: 1) Product name 2) Quantity 3) Delivery address'},
            {'keyword': 'hello', 'response': 'Walaikum Assalam! How can I help you today?'},
            {'keyword': 'hi', 'response': 'Hello! Thanks for contacting us. How can we help?'}
        ]
        
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if 'keywords' in config:
                    return config['keywords']
        
        return default_keywords
    
    def load_messages(self):
        """Load message history"""
        if MESSAGES_FILE.exists():
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'messages': []}
    
    def save_messages(self):
        """Save message history"""
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, indent=2)
    
    def save_config(self):
        """Save configuration"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)
    
    def send_whatsapp_message(self, to_number, message):
        """Send real WhatsApp message via WhatsApp Business API"""
        
        # If no access token, simulate sending
        if not self.config.get('access_token'):
            print(f"📱 [SIMULATED] Sending to {to_number}: {message}")
            self.messages['messages'].append({
                'type': 'sent',
                'to': to_number,
                'message': message,
                'timestamp': datetime.now().isoformat(),
                'status': 'sent',
                'auto_reply': True
            })
            self.save_messages()
            return True
        
        # Real WhatsApp Business API
        url = f"https://graph.facebook.com/v17.0/{self.config['phone_id']}/messages"
        
        headers = {
            'Authorization': f'Bearer {self.config["access_token"]}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messaging_product': 'whatsapp',
            'to': to_number.replace('+', '').replace(' ', ''),
            'type': 'text',
            'text': {
                'body': message
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            result = response.json()
            
            if response.status_code == 200:
                print(f"✅ Message sent to {to_number}")
                self.messages['messages'].append({
                    'type': 'sent',
                    'to': to_number,
                    'message': message,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'delivered',
                    'message_id': result.get('messages', [{}])[0].get('id'),
                    'auto_reply': True
                })
                self.save_messages()
                return True
            else:
                print(f"❌ Failed to send message: {result}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending message: {str(e)}")
            return False
    
    def process_incoming_message(self, from_number, message_text, sender_name=''):
        """Process incoming WhatsApp message and send auto-reply"""
        
        print(f"\n📨 New message from {sender_name or from_number}: {message_text}")
        
        if not self.auto_reply_enabled:
            print("⚠️ Auto-reply is disabled")
            return
        
        # Save incoming message
        self.messages['messages'].append({
            'type': 'received',
            'from': from_number,
            'from_name': sender_name,
            'message': message_text,
            'timestamp': datetime.now().isoformat(),
            'status': 'received',
            'auto_replied': False
        })
        
        # Find matching keyword
        response = None
        matched_keyword = None
        message_lower = message_text.lower()
        
        for kw in self.keywords:
            if kw['keyword'].lower() in message_lower:
                response = kw['response']
                matched_keyword = kw['keyword']
                break
        
        # Use greeting if no keyword match
        if not response:
            response = self.config.get('greeting_message', 
                'Thank you for your message. We will respond shortly.')
        
        # Add keyword info to response
        if matched_keyword:
            response += f"\n\n(Auto-reply for: {matched_keyword})"
        
        # Send auto-reply
        time.sleep(1)  # Small delay for natural feel
        success = self.send_whatsapp_message(from_number, response)
        
        if success:
            # Mark as auto-replied
            for msg in reversed(self.messages['messages']):
                if msg['from'] == from_number and msg['message'] == message_text:
                    msg['auto_replied'] = True
                    break
            self.save_messages()
            print(f"🤖 Auto-reply sent!")
    
    def setup_webhook(self):
        """Setup WhatsApp webhook for receiving messages"""
        print("=" * 60)
        print("WhatsApp Webhook Setup")
        print("=" * 60)
        print("\nTo receive real WhatsApp messages:")
        print("\n1. Go to: https://developers.facebook.com/apps/")
        print("2. Select your app")
        print("3. Go to WhatsApp → Configuration")
        print("4. Set Webhook URL to: https://your-domain.com/webhook")
        print("5. Set Verify Token to: my_verify_token_123")
        print("\nFor local testing, use ngrok:")
        print("   ngrok http 5000")
        print("   Then use the ngrok URL as webhook")
        print("=" * 60)
    
    def handle_webhook(self, request_data):
        """Handle incoming webhook from WhatsApp"""
        try:
            # Parse webhook data
            if 'object' not in request_data or request_data['object'] != 'whatsapp_business_account':
                return {'status': 'ignored'}
            
            for entry in request_data.get('entry', []):
                for change in entry.get('changes', []):
                    if change.get('field') == 'messages':
                        value = change.get('value', {})
                        for message in value.get('contacts', []):
                            # Get message text
                            if 'messages' in value:
                                for msg in value['messages']:
                                    if msg.get('type') == 'text':
                                        from_number = message.get('wa_id', '')
                                        sender_name = message.get('profile', {}).get('name', '')
                                        message_text = msg.get('text', {}).get('body', '')
                                        
                                        # Process message
                                        self.process_incoming_message(
                                            from_number, 
                                            message_text, 
                                            sender_name
                                        )
            
            return {'status': 'ok'}
            
        except Exception as e:
            print(f"❌ Webhook error: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def test_auto_reply(self):
        """Test auto-reply with sample messages"""
        print("\n🧪 Testing Auto-Reply System...")
        print("=" * 60)
        
        test_messages = [
            ('+92 300 1234567', 'Hi, what is the price?', 'Test Customer 1'),
            ('+92 321 7654321', 'I want to make a payment', 'Test Customer 2'),
            ('+92 333 9876543', 'Hello, how are you?', 'Test Customer 3'),
            ('+92 345 1122334', 'Can I place an order?', 'Test Customer 4')
        ]
        
        for number, message, name in test_messages:
            print(f"\n--- Testing: {name} ---")
            self.process_incoming_message(number, message, name)
            time.sleep(2)
        
        print("\n" + "=" * 60)
        print("✅ Test complete! Check whatsapp_messages.json for results")
        print("=" * 60)


# Create instance
whatsapp_bot = WhatsAppAutoReply()

# For testing
if __name__ == '__main__':
    whatsapp_bot.test_auto_reply()
