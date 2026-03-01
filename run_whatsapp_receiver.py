"""
WhatsApp Real-Time Message Receiver & Auto-Reply
Uses Playwright to monitor WhatsApp Web and send real auto-replies

SETUP:
1. pip install playwright
2. playwright install chromium
3. python run_whatsapp_receiver.py
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed!")
    print("Run: pip install playwright")
    print("Then: playwright install chromium")
    sys.exit(1)

# Configuration
VAULT_PATH = Path(__file__).parent / "vault" / "Inbox"
CONFIG_FILE = Path(__file__).parent / "whatsapp_config.json"
MESSAGES_FILE = Path(__file__).parent / "whatsapp_messages.json"

# Auto-reply keywords
AUTO_REPLY_KEYWORDS = {
    'hello': 'Walaikum Assalam! How can I help you today?',
    'hi': 'Hello! Thanks for contacting us. How can we help?',
    'price': 'Our pricing starts at $99/month. Would you like to schedule a demo?',
    'payment': 'You can make payment via bank transfer. Account: 1234567890',
    'order': 'To place an order, please provide: 1) Product name 2) Quantity 3) Delivery address',
    'thanks': 'You\'re welcome! Is there anything else I can help you with?',
    'thank you': 'You\'re welcome! Feel free to ask if you need anything else.',
    'cost': 'Our pricing starts at $99/month. Contact us for a custom quote!',
    'buy': 'Great! To place an order, please provide: 1) Product name 2) Quantity 3) Delivery address',
    'help': 'How can I assist you today? We offer: 1) Products 2) Services 3) Support',
}

class WhatsAppRealReceiver:
    def __init__(self):
        self.browser = None
        self.page = None
        self.processed_messages = set()
        self.last_reply_time = {}
        self.config = self.load_config()
        self.messages = self.load_messages()
        VAULT_PATH.mkdir(parents=True, exist_ok=True)
        
    def load_config(self):
        """Load configuration"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'auto_reply_enabled': True}
    
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
            processed_file = Path(__file__).parent / ".whatsapp_processed"
            if processed_file.exists():
                with open(processed_file, 'r', encoding='utf-8') as f:
                    self.processed_messages = set(json.load(f))
                print(f"✅ Loaded {len(self.processed_messages)} processed messages")
        except Exception as e:
            print(f"⚠️  Error loading processed messages: {e}")
            self.processed_messages = set()
    
    def save_processed_messages(self):
        """Save processed message IDs"""
        try:
            processed_file = Path(__file__).parent / ".whatsapp_processed"
            with open(processed_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.processed_messages), f)
        except Exception as e:
            print(f"⚠️  Error saving processed messages: {e}")
    
    async def start(self):
        """Start WhatsApp Web monitoring"""
        print("\n" + "=" * 70)
        print("🚀 WhatsApp Real-Time Message Receiver")
        print("=" * 70)
        print(f"\n💾 Messages saved to: {VAULT_PATH}")
        print(f"🤖 Auto-reply: {'ENABLED' if self.config.get('auto_reply_enabled', True) else 'DISABLED'}")
        print(f"\n📋 Keywords: {', '.join(AUTO_REPLY_KEYWORDS.keys())}")
        print("\n" + "=" * 70)
        
        # Load processed messages
        self.load_processed_messages()
        
        # Launch browser
        print("\n📱 Starting WhatsApp Web...")
        print("⏳ Please scan QR code with your phone...\n")
        
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=False,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            self.page = await self.browser.new_page()
            
            await self.page.goto("https://web.whatsapp.com", timeout=60000)
            
            # Wait for WhatsApp to load
            print("⏳ Waiting for WhatsApp Web to load...")
            try:
                await self.page.wait_for_selector('[data-testid="chat-list"]', timeout=120000)
                print("\n✅ WhatsApp Web connected successfully!")
            except Exception as e:
                print(f"\n⚠️  QR Code timeout or error: {e}")
                print("\n💡 Troubleshooting:")
                print("   1. Make sure you scanned QR code")
                print("   2. Check internet connection")
                print("   3. Try refreshing WhatsApp Web manually")
                return
            
            print("\n" + "=" * 70)
            print("🎯 MONITORING ACTIVE - Waiting for messages...")
            print("=" * 70)
            print("\n(Press Ctrl+C to stop)\n")
            
            # Start monitoring
            await self.monitor_messages()
            
        except Exception as e:
            print(f"\n❌ Error starting: {e}")
            print("\n💡 Troubleshooting:")
            print("   1. Install Playwright: pip install playwright")
            print("   2. Install Chromium: playwright install chromium")
            print("   3. Check internet connection")
        finally:
            await self.stop()
    
    async def monitor_messages(self, poll_interval=3):
        """Monitor for new messages"""
        while True:
            try:
                await asyncio.sleep(poll_interval)
                await self.check_new_messages()
            except Exception as e:
                print(f"⚠️  Error monitoring: {e}")
                await asyncio.sleep(5)
    
    async def check_new_messages(self):
        """Check for new incoming messages"""
        try:
            # Find all message containers
            message_containers = await self.page.query_selector_all('[data-testid="msg-container"]')
            
            if not message_containers:
                return
            
            for container in message_containers:
                try:
                    # Get message ID
                    msg_id = await container.get_attribute('data-id')
                    if not msg_id or msg_id in self.processed_messages:
                        continue
                    
                    # Check if it's an incoming message (not sent by us)
                    is_incoming = await self.is_incoming_message(container)
                    if not is_incoming:
                        self.processed_messages.add(msg_id)
                        self.save_processed_messages()
                        continue
                    
                    # Extract message details
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
                    print(f"⚠️  Error processing message container: {e}")
                    continue
                    
        except Exception as e:
            print(f"⚠️  Error checking messages: {e}")
    
    async def is_incoming_message(self, container):
        """Check if message is incoming (received, not sent)"""
        try:
            # Check for message-in class or absence of message-out indicators
            class_name = await container.get_attribute('class')
            if 'message-in' in str(class_name):
                return True
            
            # Alternative: check if it's not in message-out container
            parent = await container.evaluate('(el) => el.closest(\'[data-testid="message-out"]\')')
            if parent is None:
                # Check for green tick (sent message indicator)
                sent_indicator = await container.query_selector('[data-testid="msg-tick"]')
                if sent_indicator is None:
                    return True
            
            return False
        except:
            return True  # Default to incoming if unsure
    
    async def get_sender(self, container):
        """Get sender name from message"""
        try:
            # Try to find sender name in message container
            sender_el = await container.query_selector('span[dir="auto"]')
            if sender_el:
                sender = await sender_el.text_content()
                if sender and sender.strip():
                    return sender.strip()
            
            # Fallback: get from chat header
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
        print(f"📨 NEW MESSAGE")
        print(f"👤 From: {sender}")
        print(f"💬 Message: {message_text[:100]}{'...' if len(message_text) > 100 else ''}")
        print(f"🕐 Time: {timestamp}")
        
        # Save to vault
        await self.save_to_vault(sender, message_text, timestamp, msg_id)
        
        # Save to messages JSON
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
        
        # Mark as processed
        self.processed_messages.add(msg_id)
        self.save_processed_messages()
        
        # Check if auto-reply is enabled
        if not self.config.get('auto_reply_enabled', True):
            print(f"⚠️  Auto-reply disabled")
            return
        
        # Check rate limiting (don't reply to same person within 60 seconds)
        now = datetime.now()
        if sender in self.last_reply_time:
            time_diff = (now - self.last_reply_time[sender]).total_seconds()
            if time_diff < 60:
                print(f"⏳ Skipping reply (too soon - {time_diff:.1f}s)")
                return
        
        # Find matching keyword
        response = self.find_auto_reply(message_text)
        
        if response:
            print(f"🤖 Sending auto-reply...")
            success = await self.send_reply(sender, response)
            
            if success:
                self.last_reply_time[sender] = now
                print(f"✅ Auto-reply sent!")
                
                # Update message record
                for msg in reversed(self.messages['messages']):
                    if msg['id'] == msg_id:
                        msg['auto_replied'] = True
                        msg['auto_reply_text'] = response
                        break
                self.save_messages()
            else:
                print(f"❌ Failed to send auto-reply")
        else:
            print(f"ℹ️  No matching keyword (message saved)")
    
    def find_auto_reply(self, message_text):
        """Find auto-reply based on keywords"""
        message_lower = message_text.lower()
        
        for keyword, response in AUTO_REPLY_KEYWORDS.items():
            if keyword.lower() in message_lower:
                return response
        
        # Default greeting if no keyword match
        if len(message_text.split()) < 5:  # Short message, likely greeting
            return self.config.get('greeting_message', 
                'Thank you for your message. How can we help you today?')
        
        return None
    
    async def send_reply(self, recipient, message):
        """Send reply message"""
        try:
            # Click on the chat to open it
            await self.click_on_chat(recipient)
            
            # Type and send message
            msg_input = await self.page.query_selector('[data-testid="msg-input"]')
            if msg_input:
                await msg_input.click()
                await msg_input.fill(message)
                
                # Send message (Enter key)
                await self.page.keyboard.press('Enter')
                
                await asyncio.sleep(1)
                
                # Go back to chat list
                back_button = await self.page.query_selector('[data-testid="back"]')
                if back_button:
                    await back_button.click()
                
                return True
            
            print("⚠️  Message input not found")
            return False
        except Exception as e:
            print(f"⚠️  Error sending reply: {e}")
            return False
    
    async def click_on_chat(self, chat_name):
        """Click on a chat by name"""
        try:
            # Search for chat
            search_box = await self.page.query_selector('[data-testid="search-input"]')
            if search_box:
                await search_box.click()
                await search_box.fill(chat_name)
                await asyncio.sleep(1)
                
                # Click first result
                first_result = await self.page.query_selector('[role="row"][tabindex="0"]')
                if first_result:
                    await first_result.click()
                    await asyncio.sleep(1)
                    
                    # Clear search
                    await search_box.fill('')
                    return True
            
            return False
        except Exception as e:
            print(f"⚠️  Error clicking chat: {e}")
            return False
    
    async def save_to_vault(self, sender, message_text, timestamp, msg_id):
        """Save message to vault"""
        try:
            ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            safe_sender = "".join(c for c in sender if c.isalnum() or c in (' ', '_', '-')).strip()[:30]
            filename = f"WHATSAPP_{safe_sender}_{ts}.md"
            filepath = VAULT_PATH / filename
            
            content = f"""# WhatsApp Message

**From:** {sender}
**Time:** {timestamp}
**Date Added:** {datetime.now().isoformat()}
**Source:** WhatsApp Web
**Message ID:** {msg_id}

## Content

{message_text}

## Status

- [ ] Read
- [ ] Process
- [ ] Archive

## Notes

"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"💾 Saved to vault: {filename}")
            return True
        except Exception as e:
            print(f"⚠️  Error saving to vault: {e}")
            return False
    
    async def stop(self):
        """Stop monitoring"""
        print("\n\n⏹️  Stopping WhatsApp receiver...")
        if self.browser:
            await self.browser.close()
        print("✅ Stopped")


async def main():
    receiver = WhatsAppRealReceiver()
    await receiver.start()

if __name__ == '__main__':
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1, errors='replace')
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nWhatsApp Receiver stopped by user")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("   1. Install Playwright: pip install playwright")
        print("   2. Install Chromium: playwright install chromium")
        print("   3. Check internet connection")
        input("\nPress Enter to exit...")
