"""
WhatsApp Live Server - Real-time Auto-Reply with Web Interface
Integrates WhatsApp Web monitoring with Flask backend
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from threading import Thread
import socketio

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Installing Playwright...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    from playwright.async_api import async_playwright

# Configuration
PROJECT_ROOT = Path(__file__).parent
CONFIG_FILE = PROJECT_ROOT / "whatsapp_config.json"
MESSAGES_FILE = PROJECT_ROOT / "whatsapp_messages_live.json"

# Auto-reply keywords
AUTO_REPLY_KEYWORDS = {
    'hello': 'Walaikum Assalam! How can I help you today?',
    'hi': 'Hello! Thanks for contacting us. How can we help?',
    'hey': 'Hello! How can I assist you?',
    'price': 'Our pricing starts at $99/month. Would you like to schedule a demo?',
    'cost': 'Our pricing starts at $99/month. Contact us for a custom quote!',
    'payment': 'You can make payment via bank transfer. Account: 1234567890',
    'pay': 'Payment details: Bank Transfer - Account: 1234567890',
    'order': 'To place an order, please provide: 1) Product name 2) Quantity 3) Delivery address',
    'buy': 'Great! To order, please provide: 1) Product 2) Quantity 3) Address',
    'thanks': 'You\'re welcome! Is there anything else I can help you with?',
    'thank you': 'You\'re welcome! Feel free to ask if you need anything else.',
    'help': 'How can I assist you today? We offer: 1) Products 2) Services 3) Support',
    'support': 'Our support team is here to help! What do you need assistance with?',
    'contact': 'You can reach us at: +92 300 1234567 or info@example.com',
    'location': 'Visit us at: 123 Main Street, Karachi, Pakistan',
    'address': 'Our address: 123 Main Street, Karachi, Pakistan',
    'business hours': 'We are open Monday-Saturday, 9 AM to 6 PM',
    'timing': 'Our business hours are 9 AM to 6 PM, Monday to Saturday',
}

class WhatsAppLiveReceiver:
    def __init__(self):
        self.browser = None
        self.page = None
        self.processed_messages = set()
        self.last_reply_time = {}
        self.config = self.load_config()
        self.messages = self.load_messages()
        self.is_running = False
        self.sio = None
        self.new_messages_callback = None
        
        # Create vault folder
        vault_path = PROJECT_ROOT / "vault" / "Inbox"
        vault_path.mkdir(parents=True, exist_ok=True)
        
    def load_config(self):
        """Load configuration"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'auto_reply_enabled': True, 'phone_number': '+92 300 1234567'}
    
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
    
    def load_processed_messages(self):
        """Load processed message IDs"""
        try:
            processed_file = PROJECT_ROOT / ".whatsapp_processed"
            if processed_file.exists():
                with open(processed_file, 'r', encoding='utf-8') as f:
                    self.processed_messages = set(json.load(f))
                print(f"Loaded {len(self.processed_messages)} processed messages")
        except Exception as e:
            print(f"Error loading processed messages: {e}")
            self.processed_messages = set()
    
    def save_processed_messages(self):
        """Save processed message IDs"""
        try:
            processed_file = PROJECT_ROOT / ".whatsapp_processed"
            with open(processed_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.processed_messages), f)
        except Exception as e:
            print(f"Error saving processed messages: {e}")
    
    def set_new_message_callback(self, callback):
        """Set callback for new messages"""
        self.new_messages_callback = callback
    
    async def start(self):
        """Start WhatsApp Web monitoring"""
        print("\n" + "=" * 70)
        print("WhatsApp Live Receiver - Starting...")
        print("=" * 70)
        print(f"Messages saved to: {MESSAGES_FILE}")
        print(f"Auto-reply: {'ENABLED' if self.config.get('auto_reply_enabled', True) else 'DISABLED'}")
        print(f"Keywords: {', '.join(AUTO_REPLY_KEYWORDS.keys())}")
        print("=" * 70)
        
        self.is_running = True
        self.load_processed_messages()
        
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=False,
                args=['--no-sandbox', '--disable-setuid-sandbox', '--start-maximized']
            )
            self.page = await self.browser.new_page()
            
            print("\nOpening WhatsApp Web...")
            await self.page.goto("https://web.whatsapp.com", timeout=60000)
            
            print("\nWaiting for QR code scan...")
            print("Please scan the QR code with your phone:")
            print("  1. Open WhatsApp on phone")
            print("  2. Settings > Linked Devices > Link a Device")
            print("  3. Scan the QR code")
            
            try:
                await self.page.wait_for_selector('[data-testid="chat-list"]', timeout=120000)
                print("\nWhatsApp Web connected successfully!")
            except Exception as e:
                print(f"\nQR Code scan timeout: {e}")
                return
            
            print("\nMonitoring messages... (Press Ctrl+C to stop)")
            await self.monitor_messages()
            
        except Exception as e:
            print(f"\nError starting: {e}")
        finally:
            await self.stop()
    
    async def monitor_messages(self, poll_interval=2):
        """Monitor for new messages"""
        while self.is_running:
            try:
                await asyncio.sleep(poll_interval)
                await self.check_new_messages()
            except Exception as e:
                print(f"Error monitoring: {e}")
                await asyncio.sleep(5)
    
    async def check_new_messages(self):
        """Check for new incoming messages"""
        try:
            if not self.page:
                return
            
            # Find all message containers
            message_containers = await self.page.query_selector_all('[data-testid="msg-container"]')
            
            if not message_containers:
                return
            
            for container in message_containers:
                try:
                    msg_id = await container.get_attribute('data-id')
                    if not msg_id or msg_id in self.processed_messages:
                        continue
                    
                    # Check if incoming message
                    is_incoming = await self.is_incoming_message(container)
                    if not is_incoming:
                        self.processed_messages.add(msg_id)
                        self.save_processed_messages()
                        continue
                    
                    # Get message details
                    sender = await self.get_sender(container)
                    message_text = await self.get_message_text(container)
                    timestamp = datetime.now().isoformat()
                    
                    if not message_text or not message_text.strip():
                        self.processed_messages.add(msg_id)
                        self.save_processed_messages()
                        continue
                    
                    # Process the message
                    await self.process_message(sender, message_text, timestamp, msg_id)
                    
                except Exception as e:
                    print(f"Error processing message: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error checking messages: {e}")
    
    async def is_incoming_message(self, container):
        """Check if message is incoming"""
        try:
            class_name = await container.get_attribute('class')
            if 'message-in' in str(class_name):
                return True
            
            # Check for green tick (sent message)
            sent_indicator = await container.query_selector('[data-testid="msg-tick"]')
            if sent_indicator is None:
                return True
            
            return False
        except:
            return True
    
    async def get_sender(self, container):
        """Get sender name"""
        try:
            sender_el = await container.query_selector('span[dir="auto"]')
            if sender_el:
                sender = await sender_el.text_content()
                if sender and sender.strip():
                    return sender.strip()
            
            chat_header = await self.page.query_selector('[data-testid="conversation-info-header"]')
            if chat_header:
                name = await chat_header.text_content()
                if name and name.strip():
                    return name.strip()
            
            return "Unknown"
        except:
            return "Unknown"
    
    async def get_message_text(self, container):
        """Extract message text"""
        try:
            text_elements = await container.query_selector_all('span[dir="auto"]')
            texts = []
            for el in text_elements:
                text = await el.text_content()
                if text and text.strip():
                    texts.append(text.strip())
            
            return ' '.join(texts) if texts else ""
        except:
            return ""
    
    async def process_message(self, sender, message_text, timestamp, msg_id):
        """Process incoming message and send auto-reply"""
        print(f"\n{'='*70}")
        print(f"NEW MESSAGE")
        print(f"From: {sender}")
        print(f"Message: {message_text[:100]}")
        print(f"Time: {timestamp}")
        
        # Save to messages
        self.messages['messages'].append({
            'id': msg_id,
            'type': 'received',
            'from': sender,
            'message': message_text,
            'timestamp': timestamp,
            'status': 'received',
            'auto_replied': False
        })
        self.save_messages()
        
        # Notify callback (for web interface)
        if self.new_messages_callback:
            await self.new_messages_callback({
                'id': msg_id,
                'from': sender,
                'message': message_text,
                'timestamp': timestamp,
                'type': 'received'
            })
        
        # Mark as processed
        self.processed_messages.add(msg_id)
        self.save_processed_messages()
        
        # Check auto-reply
        if not self.config.get('auto_reply_enabled', True):
            print("Auto-reply disabled")
            return
        
        # Rate limiting
        now = datetime.now()
        if sender in self.last_reply_time:
            time_diff = (now - self.last_reply_time[sender]).total_seconds()
            if time_diff < 60:
                print(f"Skipping reply (too soon - {time_diff:.1f}s)")
                return
        
        # Find auto-reply
        response = self.find_auto_reply(message_text)
        
        if response:
            print(f"Sending auto-reply...")
            success = await self.send_reply(sender, response)
            
            if success:
                self.last_reply_time[sender] = now
                print(f"Auto-reply sent!")
                
                # Update message record
                for msg in reversed(self.messages['messages']):
                    if msg['id'] == msg_id:
                        msg['auto_replied'] = True
                        msg['auto_reply_text'] = response
                        break
                self.save_messages()
                
                # Notify callback
                if self.new_messages_callback:
                    await self.new_messages_callback({
                        'id': f'{msg_id}_reply',
                        'from': 'You',
                        'message': response,
                        'timestamp': datetime.now().isoformat(),
                        'type': 'sent',
                        'auto_reply': True
                    })
            else:
                print(f"Failed to send auto-reply")
        else:
            print(f"No matching keyword (message saved)")
    
    def find_auto_reply(self, message_text):
        """Find auto-reply based on keywords"""
        message_lower = message_text.lower()
        
        for keyword, response in AUTO_REPLY_KEYWORDS.items():
            if keyword.lower() in message_lower:
                return response
        
        # Default greeting for short messages
        if len(message_text.split()) < 5:
            return self.config.get('greeting_message', 
                'Thank you for your message. How can we help you today?')
        
        return None
    
    async def send_reply(self, recipient, message):
        """Send reply message"""
        try:
            await self.click_on_chat(recipient)
            
            msg_input = await self.page.query_selector('[data-testid="msg-input"]')
            if msg_input:
                await msg_input.click()
                await msg_input.fill(message)
                await self.page.keyboard.press('Enter')
                await asyncio.sleep(1)
                
                # Go back
                back_button = await self.page.query_selector('[data-testid="back"]')
                if back_button:
                    await back_button.click()
                
                return True
            
            print("Message input not found")
            return False
        except Exception as e:
            print(f"Error sending reply: {e}")
            return False
    
    async def click_on_chat(self, chat_name):
        """Click on a chat by name"""
        try:
            search_box = await self.page.query_selector('[data-testid="search-input"]')
            if search_box:
                await search_box.click()
                await search_box.fill(chat_name)
                await asyncio.sleep(1)
                
                first_result = await self.page.query_selector('[role="row"][tabindex="0"]')
                if first_result:
                    await first_result.click()
                    await asyncio.sleep(1)
                    await search_box.fill('')
                    return True
            
            return False
        except Exception as e:
            print(f"Error clicking chat: {e}")
            return False
    
    async def stop(self):
        """Stop monitoring"""
        print("\nStopping WhatsApp receiver...")
        self.is_running = False
        if self.browser:
            await self.browser.close()
        print("Stopped")


# Global instance
whatsapp_receiver = None

def start_receiver():
    """Start WhatsApp receiver in background thread"""
    global whatsapp_receiver
    whatsapp_receiver = WhatsAppLiveReceiver()
    
    def run_async():
        asyncio.run(whatsapp_receiver.start())
    
    thread = Thread(target=run_async, daemon=True)
    thread.start()
    return whatsapp_receiver

def get_receiver():
    """Get receiver instance"""
    return whatsapp_receiver

if __name__ == '__main__':
    if sys.platform == 'win32':
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1, errors='replace')
    
    receiver = WhatsAppLiveReceiver()
    asyncio.run(receiver.start())
