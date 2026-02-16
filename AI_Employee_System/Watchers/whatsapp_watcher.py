"""
WhatsApp Watcher - Playwright-based WhatsApp Web Automation
Monitors WhatsApp messages and saves them to Vault

⚠️  DISCLAIMER: This uses WhatsApp Web automation.
Please ensure compliance with WhatsApp's Terms of Service.
WhatsApp may rate-limit or block accounts using automation.
Use at your own risk.

Requirements:
- pip install playwright anthropic
- playwright install chromium
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WhatsAppWatcher:
    """
    Monitor WhatsApp messages using Playwright automation.
    
    Workflow:
    1. Launch browser with WhatsApp Web
    2. User scans QR code (first run)
    3. Monitor for new messages
    4. Save to Vault/Inbox/
    5. Mark as processed
    """
    
    def __init__(self, vault_path: str = "../vault"):
        self.vault_path = Path(vault_path)
        self.browser = None
        self.page = None
        self.processed_messages = set()
        self._load_processed_messages()
        
    def _load_processed_messages(self):
        """Load previously processed message IDs to avoid duplicates"""
        try:
            processed_file = self.vault_path / ".whatsapp_processed"
            if processed_file.exists():
                with open(processed_file, 'r') as f:
                    self.processed_messages = set(json.load(f))
                logger.info(f"Loaded {len(self.processed_messages)} processed messages")
        except Exception as e:
            logger.error(f"Error loading processed messages: {e}")
            self.processed_messages = set()
    
    def _save_processed_messages(self):
        """Save processed message IDs"""
        try:
            processed_file = self.vault_path / ".whatsapp_processed"
            with open(processed_file, 'w') as f:
                json.dump(list(self.processed_messages), f)
        except Exception as e:
            logger.error(f"Error saving processed messages: {e}")
    
    async def launch_browser(self) -> bool:
        """
        Launch Playwright browser with WhatsApp Web
        Returns True if successful
        """
        try:
            from playwright.async_api import async_playwright
            
            logger.info("Launching Playwright browser...")
            self.playwright = await async_playwright().start()
            
            # Launch browser with visible window so user can scan QR
            self.browser = await self.playwright.chromium.launch(headless=False)
            self.page = await self.browser.new_page()
            
            logger.info("Loading WhatsApp Web...")
            await self.page.goto("https://web.whatsapp.com", timeout=30000)
            
            # Wait for user to scan QR code (30 seconds timeout)
            logger.info("⏳ Please scan the QR code on your phone...")
            logger.info("Waiting for authentication...")
            
            try:
                await self.page.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
                logger.info("✅ Successfully logged into WhatsApp!")
                return True
            except Exception as e:
                logger.error(f"QR code scan timeout or failed: {e}")
                logger.info("Please ensure you scanned the QR code correctly")
                return False
                
        except ImportError:
            logger.error("Playwright not installed. Run: pip install playwright")
            logger.error("Then: playwright install chromium")
            return False
        except Exception as e:
            logger.error(f"Error launching browser: {e}")
            return False
    
    async def monitor_messages(self, poll_interval: int = 5) -> None:
        """
        Monitor WhatsApp for new messages
        
        Args:
            poll_interval: Seconds between checks
        """
        if not self.page:
            logger.error("Browser not initialized. Call launch_browser() first")
            return
        
        logger.info(f"Starting message monitor (checking every {poll_interval}s)...")
        
        try:
            while True:
                await asyncio.sleep(poll_interval)
                await self._check_new_messages()
        except KeyboardInterrupt:
            logger.info("Message monitoring stopped")
        finally:
            await self.close_browser()
    
    async def _check_new_messages(self) -> None:
        """Check for new messages in WhatsApp"""
        try:
            # Get all chat bubbles (messages)
            messages = await self.page.query_selector_all(
                '[data-testid="msg-container"]'
            )
            
            if not messages:
                return
            
            for msg_element in messages:
                try:
                    # Get message details
                    msg_id = await msg_element.get_attribute('data-id')
                    if msg_id in self.processed_messages:
                        continue
                    
                    # Extract message content
                    msg_content = await msg_element.text_content()
                    sender_element = await msg_element.evaluate('''
                        (el) => {
                            const span = el.querySelector('span[dir="auto"]');
                            return span ? span.textContent : null;
                        }
                    ''')
                    
                    # Get timestamp
                    time_element = await msg_element.evaluate('''
                        (el) => {
                            const timeEl = el.querySelector('span[class*="time"]');
                            return timeEl ? timeEl.textContent : null;
                        }
                    ''')
                    
                    if msg_content and msg_content.strip():
                        await self._save_message(
                            content=msg_content.strip(),
                            sender=sender_element or "Unknown",
                            timestamp=time_element or datetime.now().isoformat(),
                            msg_id=msg_id
                        )
                        self.processed_messages.add(msg_id)
                        self._save_processed_messages()
                        
                except Exception as e:
                    logger.debug(f"Error processing message element: {e}")
                    continue
                    
        except Exception as e:
            logger.debug(f"Error checking messages: {e}")
    
    async def _save_message(
        self,
        content: str,
        sender: str,
        timestamp: str,
        msg_id: str
    ) -> bool:
        """
        Save WhatsApp message to Vault
        
        Creates file: Vault/Inbox/WHATSAPP_<sender>_<timestamp>.md
        """
        try:
            # Create filename
            ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            safe_sender = sender.replace(' ', '_')[:20]
            filename = f"WHATSAPP_{safe_sender}_{ts}.md"
            
            filepath = self.vault_path / "Inbox" / filename
            
            # Create message content
            message_content = f"""# WhatsApp Message

**From:** {sender}
**Time:** {timestamp}
**Date Added:** {datetime.now().isoformat()}
**Source:** WhatsApp Web
**Message ID:** {msg_id}

## Content

{content}

## Status

- [ ] Read
- [ ] Process
- [ ] Archive

## Notes

"""
            
            # Ensure directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Save file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(message_content)
            
            logger.info(f"✅ Saved: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            return False
    
    async def get_recent_chats(self, limit: int = 5) -> List[Dict]:
        """
        Get list of recent chats
        
        Returns:
            List of dicts with chat info
        """
        if not self.page:
            logger.error("Browser not initialized")
            return []
        
        try:
            recent_chats = []
            
            # Get all chat items
            chat_items = await self.page.query_selector_all(
                '[data-testid="chat-list-item"]'
            )
            
            for i, chat in enumerate(chat_items[:limit]):
                try:
                    # Get chat name
                    name_element = await chat.query_selector('[data-testid="conversationlist-item-header"]')
                    name = await name_element.text_content() if name_element else "Unknown"
                    
                    # Get last message preview
                    msg_element = await chat.query_selector('[class*="message-preview"]')
                    preview = await msg_element.text_content() if msg_element else ""
                    
                    recent_chats.append({
                        "index": i + 1,
                        "name": name.strip(),
                        "preview": preview.strip()[:100]
                    })
                except Exception as e:
                    logger.debug(f"Error reading chat {i}: {e}")
                    continue
            
            return recent_chats
            
        except Exception as e:
            logger.error(f"Error getting recent chats: {e}")
            return []
    
    async def send_message(self, chat_name: str, message: str) -> bool:
        """
        Send a message to a specific chat
        
        Args:
            chat_name: Name of person/group
            message: Message to send
            
        Returns:
            True if successful
        """
        if not self.page:
            logger.error("Browser not initialized")
            return False
        
        try:
            logger.info(f"Sending message to {chat_name}...")
            
            # Search for chat
            search_box = await self.page.query_selector('[data-testid="search-input"]')
            if search_box:
                await search_box.click()
                await search_box.fill(chat_name)
                await asyncio.sleep(1)  # Wait for results
                
                # Click first result
                first_result = await self.page.query_selector('[data-testid="chat-list-item"]')
                if first_result:
                    await first_result.click()
                    await asyncio.sleep(1)
            
            # Type and send message
            msg_input = await self.page.query_selector('[data-testid="msg-input"]')
            if msg_input:
                await msg_input.click()
                await msg_input.fill(message)
                
                # Send (Ctrl+Enter)
                await self.page.keyboard.press('Control+Enter')
                logger.info(f"✅ Message sent to {chat_name}")
                return True
            
            logger.error("Message input not found")
            return False
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    async def close_browser(self) -> None:
        """Close browser and cleanup"""
        try:
            if self.page:
                await self.page.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            logger.info("Browser closed")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")


# ============================================================================
# QUICK START
# ============================================================================

async def main():
    """
    Quick start: Launch WhatsApp Watcher
    """
    print("\n" + "="*60)
    print("WhatsApp Watcher - Playwright Edition")
    print("="*60)
    print("\n⚠️  DISCLAIMER:")
    print("This uses WhatsApp Web automation.")
    print("Ensure compliance with WhatsApp's Terms of Service.")
    print("\n")
    
    watcher = WhatsAppWatcher(vault_path="./vault")
    
    # Launch browser
    success = await watcher.launch_browser()
    if not success:
        print("❌ Failed to connect to WhatsApp")
        return
    
    print("\n✅ Connected to WhatsApp!")
    
    # Show recent chats
    print("\nRecent Chats:")
    print("-" * 60)
    chats = await watcher.get_recent_chats(5)
    for chat in chats:
        print(f"{chat['index']}. {chat['name']}")
        if chat['preview']:
            print(f"   → {chat['preview']}")
    
    # Start monitoring
    print("\n" + "="*60)
    print("Starting message monitor...")
    print("Messages will be saved to: Vault/Inbox/")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    await watcher.monitor_messages(poll_interval=5)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ WhatsApp Watcher stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Install Playwright: pip install playwright")
        print("2. Install Chrome: playwright install chromium")
        print("3. Ensure selenium and/or browser automation tools are working")
        print("4. Check WhatsApp Web loads correctly at https://web.whatsapp.com")
