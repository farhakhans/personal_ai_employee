"""
WhatsApp Real Auto-Reply Runner
Monitors WhatsApp Web and sends automatic replies

SETUP:
1. pip install playwright
2. playwright install chromium
3. python run_whatsapp_autoreply.py
"""

import asyncio
import sys
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from AI_Employee_System.Watchers.whatsapp_watcher import WhatsAppWatcher
from whatsapp_real_autoreply import WhatsAppAutoReply

# Configuration
VAULT_PATH = Path(__file__).parent / "vault"
AUTO_REPLY_KEYWORDS = {
    'hello': 'Walaikum Assalam! How can I help you today?',
    'hi': 'Hello! Thanks for contacting us. How can we help?',
    'price': 'Our pricing starts at $99/month. Would you like to schedule a demo?',
    'payment': 'You can make payment via bank transfer. Account: 1234567890',
    'order': 'To place an order, please provide: 1) Product name 2) Quantity 3) Delivery address',
    'thanks': 'You\'re welcome! Is there anything else I can help you with?',
    'thank you': 'You\'re welcome! Feel free to ask if you need anything else.'
}

class WhatsAppRealAutoReply:
    def __init__(self):
        self.watcher = WhatsAppWatcher(vault_path=str(VAULT_PATH))
        self.auto_reply = WhatsAppAutoReply()
        self.auto_reply.keywords = [
            {'keyword': kw, 'response': resp} 
            for kw, resp in AUTO_REPLY_KEYWORDS.items()
        ]
        self.last_message_time = {}
        
    async def start(self):
        """Start WhatsApp auto-reply system"""
        print("=" * 70)
        print("🚀 WhatsApp Real Auto-Reply System")
        print("=" * 70)
        print(f"\n💾 Messages will be saved to: {VAULT_PATH / 'Inbox'}")
        print(f"🤖 Auto-reply enabled for {len(self.auto_reply.keywords)} keywords")
        print("\nKeywords:", ', '.join(AUTO_REPLY_KEYWORDS.keys()))
        print("\n" + "=" * 70)
        
        # Launch browser
        print("\n📱 Launching WhatsApp Web...")
        print("⏳ Please scan the QR code with your phone...")
        
        success = await self.watcher.launch_browser()
        if not success:
            print("\n❌ Failed to connect to WhatsApp Web")
            print("Make sure you scanned the QR code correctly.")
            return
        
        print("\n✅ Connected to WhatsApp Web!")
        print("\n" + "=" * 70)
        print("🎯 Auto-Reply System ACTIVE")
        print("=" * 70)
        print("\nMonitoring messages... (Press Ctrl+C to stop)\n")
        
        # Start monitoring with custom handler
        await self.monitor_and_reply()
    
    async def monitor_and_reply(self, poll_interval=3):
        """Monitor messages and send auto-replies"""
        try:
            while True:
                await asyncio.sleep(poll_interval)
                await self._check_and_reply()
        except KeyboardInterrupt:
            print("\n\n⏹️  Stopping auto-reply system...")
        finally:
            await self.watcher.close_browser()
    
    async def _check_and_reply(self):
        """Check for new messages and send auto-replies"""
        try:
            # Get all message containers
            messages = await self.watcher.page.query_selector_all(
                '[data-testid="msg-container"]'
            )
            
            if not messages:
                return
            
            for msg_element in messages:
                try:
                    msg_id = await msg_element.get_attribute('data-id')
                    if msg_id in self.watcher.processed_messages:
                        continue
                    
                    # Check if it's an incoming message (not sent by us)
                    is_incoming = await msg_element.evaluate('''
                        (el) => {
                            return el.getAttribute('data-testid') === 'msg-container' && 
                                   !el.closest('[data-testid="message-out"]');
                        }
                    ''')
                    
                    if not is_incoming:
                        continue
                    
                    # Get message content
                    msg_content = await msg_element.text_content()
                    if not msg_content or not msg_content.strip():
                        continue
                    
                    # Get sender
                    sender_element = await msg_element.evaluate('''
                        (el) => {
                            const span = el.querySelector('span[dir="auto"]');
                            return span ? span.textContent : 'Unknown';
                        }
                    ''')
                    
                    # Process and auto-reply
                    await self._process_message(
                        content=msg_content.strip(),
                        sender=sender_element,
                        msg_id=msg_id
                    )
                    
                except Exception as e:
                    print(f"⚠️  Error processing message: {e}")
                    continue
                    
        except Exception as e:
            print(f"⚠️  Error checking messages: {e}")
    
    async def _process_message(self, content: str, sender: str, msg_id: str):
        """Process incoming message and send auto-reply"""
        print(f"\n{'='*70}")
        print(f"📨 New message from {sender}")
        print(f"💬 Content: {content[:100]}{'...' if len(content) > 100 else ''}")
        
        # Save to vault
        await self.watcher._save_message(
            content=content,
            sender=sender,
            timestamp=datetime.now().isoformat(),
            msg_id=msg_id
        )
        
        # Mark as processed
        self.watcher.processed_messages.add(msg_id)
        self.watcher._save_processed_messages()
        
        # Check for rate limiting (don't reply to same person within 60 seconds)
        now = datetime.now()
        if sender in self.last_message_time:
            time_diff = (now - self.last_message_time[sender]).total_seconds()
            if time_diff < 60:
                print(f"⏳ Skipping reply (too soon - {time_diff:.1f}s since last reply)")
                return
        
        self.last_message_time[sender] = now
        
        # Find matching keyword and send auto-reply
        response = None
        matched_keyword = None
        content_lower = content.lower()
        
        for kw in self.auto_reply.keywords:
            if kw['keyword'].lower() in content_lower:
                response = kw['response']
                matched_keyword = kw['keyword']
                break
        
        if response:
            print(f"🤖 Auto-replying (keyword: {matched_keyword})...")
            success = await self.watcher.send_message(sender, response)
            
            if success:
                print(f"✅ Auto-reply sent to {sender}")
            else:
                print(f"❌ Failed to send auto-reply")
        else:
            print(f"ℹ️  No matching keyword found (message saved to vault)")

async def main():
    """Main entry point"""
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    bot = WhatsAppRealAutoReply()
    await bot.start()

if __name__ == '__main__':
    import io
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  WhatsApp Auto-Reply stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Install Playwright: pip install playwright")
        print("2. Install Chromium: playwright install chromium")
        print("3. Make sure WhatsApp Web loads correctly")
        print("4. Check your internet connection")
