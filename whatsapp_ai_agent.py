"""
WhatsApp AI Agent - Intelligent Auto-Reply
Uses AI Employee System for smart responses
"""

import json
import requests
from datetime import datetime
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

class WhatsAppAIAgent:
    def __init__(self):
        self.config_file = PROJECT_ROOT / "whatsapp_ai_config.json"
        self.messages_file = PROJECT_ROOT / "whatsapp_ai_messages.json"
        self.config = self.load_config()
        self.messages = self.load_messages()
        
        # AI Agent settings
        self.ai_enabled = True
        self.learning_mode = True  # Learn from conversations
        self.response_delay = 2  # Seconds before replying
        
    def load_config(self):
        """Load AI Agent configuration"""
        default_config = {
            'business_name': 'AI Employee System',
            'greeting': 'Assalam-o-Alaikum! 👋 Welcome to AI Employee System. I\'m your AI assistant. How can I help you today?',
            'fallback_message': 'Thank you for your message. Let me connect you with a human agent who will respond shortly.',
            'working_hours': {
                'enabled': False,
                'start': '09:00',
                'end': '18:00',
                'timezone': 'PKT'
            },
            'ai_settings': {
                'use_anthropic': False,  # Set to True if you have Anthropic API key
                'anthropic_key': '',
                'model': 'claude-3-haiku-20240307',
                'temperature': 0.7,
                'max_tokens': 500
            },
            'auto_topics': {
                'pricing': 'Our AI Employee System has 4 tiers:\n\n🥉 Bronze: Basic automation\n🥈 Silver: WhatsApp + Social Media\n🥇 Gold: All platforms + MCP\n💎 Platinum: Full production ready\n\nWhich tier interests you?',
                'demo': 'Great! I\'d love to show you our AI Employee System. You can start a free trial at: http://localhost:5000\n\nWould you like me to schedule a personalized demo?',
                'features': '✨ AI Employee Features:\n\n📧 Gmail Auto-Reply\n📱 WhatsApp Business Bot\n📊 Social Media Management\n💰 Payment Tracking\n👥 Customer Management\n📈 Analytics Dashboard\n\nWhat would you like to know more about?',
                'contact': 'You can reach us at:\n📧 Email: support@aiemployee.ai\n📱 Phone: +92 300 1234567\n🌐 Website: www.aiemployee.ai',
                'support': 'For technical support:\n1. Check documentation: /docs\n2. View status: /status\n3. Email support: support@aiemployee.ai\n\nHow can I assist you further?'
            }
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
                default_config.update(saved_config)
        
        return default_config
    
    def load_messages(self):
        """Load message history"""
        if self.messages_file.exists():
            with open(self.messages_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'conversations': []}
    
    def save_messages(self):
        """Save message history"""
        with open(self.messages_file, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, indent=2, ensure_ascii=False)
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def detect_intent(self, message):
        """Detect user intent from message"""
        message_lower = message.lower()
        
        # Intent patterns
        intents = {
            'greeting': ['hello', 'hi', 'hey', 'assalam', 'salam', 'good morning', 'good evening'],
            'pricing': ['price', 'cost', 'tier', 'plan', 'package', 'subscription', 'buy', 'purchase'],
            'demo': ['demo', 'trial', 'test', 'try', 'show', 'example', 'sample'],
            'features': ['feature', 'function', 'capability', 'what can', 'what do', 'offer'],
            'support': ['help', 'support', 'issue', 'problem', 'error', 'bug', 'stuck'],
            'contact': ['contact', 'email', 'phone', 'address', 'location', 'reach'],
            'thanks': ['thank', 'thanks', 'shukriya', 'grateful'],
            'bye': ['bye', 'goodbye', 'see you', 'later', 'end', 'stop']
        }
        
        # Check each intent
        for intent, keywords in intents.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return intent
        
        return 'general'  # Default intent
    
    def get_ai_response(self, message, sender_name='', conversation_history=[]):
        """Generate AI response"""
        intent = self.detect_intent(message)
        
        # Check for auto-topic responses
        if intent in ['pricing', 'demo', 'features', 'support', 'contact']:
            topic_key = intent
            if topic_key in self.config['auto_topics']:
                return self.config['auto_topics'][topic_key]
        
        # Handle greetings
        if intent == 'greeting':
            greeting = self.config['greeting']
            if sender_name:
                greeting = f"Assalam-o-Alaikum {sender_name}! 👋\n\n{greeting}"
            return greeting
        
        # Handle thanks
        if intent == 'thanks':
            return "You\'re welcome! 😊 Is there anything else I can help you with?"
        
        # Handle goodbye
        if intent == 'bye':
            return "Thank you for contacting us! Have a great day. Feel free to message us anytime. 👋"
        
        # Try AI response if Anthropic is configured
        ai_settings = self.config['ai_settings']
        if ai_settings.get('use_anthropic') and ai_settings.get('anthropic_key'):
            try:
                response = self.call_anthropic_ai(message, conversation_history)
                if response:
                    return response
            except Exception as e:
                print(f"AI response failed: {e}")
        
        # Fallback response
        return self.config['fallback_message']
    
    def call_anthropic_ai(self, message, conversation_history=[]):
        """Call Anthropic Claude API for intelligent response"""
        try:
            from anthropic import Anthropic
            
            client = Anthropic(api_key=self.config['ai_settings']['anthropic_key'])
            
            # Build conversation context
            system_prompt = """You are a helpful AI assistant for AI Employee System.
            Be friendly, professional, and concise.
            Use emojis appropriately.
            If you don\'t know something, offer to connect with human support.
            Keep responses under 200 words."""
            
            # Build message history
            messages = []
            for msg in conversation_history[-5:]:  # Last 5 messages
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Call API
            response = client.messages.create(
                model=self.config['ai_settings']['model'],
                max_tokens=self.config['ai_settings']['max_tokens'],
                system=system_prompt,
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return None
    
    def process_message(self, from_number, message_text, sender_name=''):
        """Process incoming message and generate AI response"""
        timestamp = datetime.now().isoformat()
        
        print(f"\n📨 [{timestamp}] From {sender_name or from_number}: {message_text}")
        
        # Get conversation history for this user
        user_history = [
            msg for msg in self.messages['conversations']
            if msg.get('from') == from_number
        ][-10:]  # Last 10 messages
        
        # Generate AI response
        response = self.get_ai_response(message_text, sender_name, user_history)
        
        # Save conversation
        self.messages['conversations'].append({
            'timestamp': timestamp,
            'from': from_number,
            'from_name': sender_name,
            'message': message_text,
            'response': response,
            'intent': self.detect_intent(message_text),
            'ai_generated': True
        })
        
        # Limit conversation history
        if len(self.messages['conversations']) > 1000:
            self.messages['conversations'] = self.messages['conversations'][-500:]
        
        self.save_messages()
        
        print(f"🤖 AI Response: {response}")
        
        return response
    
    def send_message(self, to_number, message):
        """Send WhatsApp message (placeholder - integrate with your WhatsApp API)"""
        print(f"📱 Sending to {to_number}: {message}")
        
        # TODO: Integrate with your WhatsApp Business API
        # You can use the existing send_whatsapp_message from whatsapp_real_autoreply.py
        
        return True
    
    def handle_incoming(self, from_number, message, sender_name=''):
        """Handle incoming message - main entry point"""
        response = self.process_message(from_number, message, sender_name)
        self.send_message(from_number, response)
        return response
    
    def get_stats(self):
        """Get conversation statistics"""
        total = len(self.messages['conversations'])
        intents = {}
        
        for msg in self.messages['conversations']:
            intent = msg.get('intent', 'unknown')
            intents[intent] = intents.get(intent, 0) + 1
        
        return {
            'total_conversations': total,
            'intents': intents,
            'ai_enabled': self.ai_enabled
        }


# Create global instance
whatsapp_ai = WhatsAppAIAgent()

# Test function
def test_ai_agent():
    """Test the AI Agent"""
    print("=" * 60)
    print("WhatsApp AI Agent Test")
    print("=" * 60)
    
    test_messages = [
        ('+92 300 1234567', 'Hello', 'Ahmed'),
        ('+92 321 7654321', 'What is the price?', 'Fatima'),
        ('+92 333 9876543', 'Can I get a demo?', 'Hassan'),
        ('+92 345 1122334', 'What features do you offer?', 'Ayesha'),
        ('+92 300 9999999', 'Thank you!', 'Test User')
    ]
    
    for number, message, name in test_messages:
        print(f"\n--- {name} ---")
        whatsapp_ai.handle_incoming(number, message, name)
    
    print("\n" + "=" * 60)
    print("Stats:", whatsapp_ai.get_stats())
    print("=" * 60)


if __name__ == '__main__':
    test_ai_agent()
