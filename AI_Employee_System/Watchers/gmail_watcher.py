"""
GMAIL WATCHER
Monitors Gmail inbox and processes new emails
Runs continuously, checking every 5 minutes
"""

import os
import json
import time
import logging
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
import imaplib
import email
from email.header import decode_header

logger = logging.getLogger("GmailWatcher")


class GmailWatcher:
    """Watches Gmail inbox for new emails

    This integration is available to all tiers (bronze+).  The constructor
    accepts an optional ``user_tier`` value and will refuse to initialize if
    the tier is not allowed.
    """

    ALLOWED_TIERS = ['bronze', 'silver', 'gold', 'platinum']

    def __init__(self, email_addr: str, app_password: str, vault_path: str,
                 poll_interval: int = 300, user_tier: str = 'bronze'):
        """
        email_addr: Gmail address
        app_password: Gmail app password (from 2FA settings)
        vault_path: Path to Obsidian vault
        poll_interval: Seconds between polls (default 5 min)
        user_tier: Tier of the user/organization (used for gating)
        """
        if user_tier not in self.ALLOWED_TIERS:
            raise ValueError(f"GmailWatcher is not permitted for tier {user_tier}")

        self.email_addr = email_addr
        self.app_password = app_password
        self.vault_path = vault_path
        self.poll_interval = poll_interval
        self.user_tier = user_tier
        self.processed_emails = set()
        self.load_processed_emails()
    
    def load_processed_emails(self):
        """Load list of already-processed email IDs"""
        inbox_dir = Path(self.vault_path) / "Inbox"
        if inbox_dir.exists():
            for file in inbox_dir.glob("*.md"):
                # Extract email ID from filename
                name = file.stem
                self.processed_emails.add(name)
    
    def connect_gmail(self):
        """Connect to Gmail via IMAP"""
        try:
            imap = imaplib.IMAP4_SSL("imap.gmail.com")
            imap.login(self.email_addr, self.app_password)
            imap.select("INBOX")
            logger.info(f"✅ Connected to Gmail: {self.email_addr}")
            return imap
        except Exception as e:
            logger.error(f"❌ Gmail connection failed: {e}")
            return None
    
    def decode_email_header(self, header_val):
        """Decode email header (handles encoding)"""
        if not header_val:
            return ""
        
        if not isinstance(header_val, str):
            return str(header_val)
        
        try:
            decoded_parts = decode_header(header_val)
            result = ""
            for part, encoding in decoded_parts:
                if isinstance(part, bytes):
                    result += part.decode(encoding or 'utf-8', errors='ignore')
                else:
                    result += part
            return result.strip()
        except:
            return header_val
    
    def get_email_body(self, msg):
        """Extract email body (text only)"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        body += part.get_payload()
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                body = msg.get_payload()
        
        return body[:2000]  # Limit body size
    
    def process_email(self, msg_id: str) -> Dict[str, Any]:
        """Process a single email"""
        try:
            imap = self.connect_gmail()
            if not imap:
                return None
            
            status, msg_data = imap.fetch(msg_id, "(RFC822)")
            if status != "OK":
                return None
            
            msg = email.message_from_bytes(msg_data[0][1])
            
            sender = self.decode_email_header(msg.get("From", "Unknown"))
            subject = self.decode_email_header(msg.get("Subject", "(No Subject)"))
            body = self.get_email_body(msg)
            date_str = msg.get("Date", "")
            
            email_id = f"EMAIL_{msg_id.decode().strip().replace(' ', '_')}"
            
            # Don't process duplicates
            if email_id in self.processed_emails:
                return None
            
            email_data = {
                "email_id": email_id,
                "from": sender,
                "subject": subject,
                "body": body,
                "date": date_str,
                "received_at": datetime.now().isoformat(),
                "status": "unprocessed"
            }
            
            imap.close()
            imap.logout()
            
            return email_data
        
        except Exception as e:
            logger.error(f"❌ Error processing email {msg_id}: {e}")
            return None
    
    def save_to_inbox(self, email_data: Dict[str, Any]) -> bool:
        """Save email to Vault/Inbox"""
        try:
            inbox_path = Path(self.vault_path) / "Inbox"
            inbox_path.mkdir(parents=True, exist_ok=True)
            
            email_id = email_data["email_id"]
            file_path = inbox_path / f"{email_id}.md"
            
            # Create markdown file
            content = f"""# Email: {email_data['subject']}
**From:** {email_data['from']}  
**Date:** {email_data['date']}  
**Received:** {email_data['received_at']}  
**Status:** 📥 Inbox

---

## Subject
{email_data['subject']}

## Body
{email_data['body']}

---

## Actions
- [ ] Triage (Assign category/priority)
- [ ] Draft Response
- [ ] Archive
- [ ] Mark as Done

## Analysis
Priority: TBD  
Category: TBD  
Suggested Action: TBD  

---
*Auto-captured by Gmail Watcher*
"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.processed_emails.add(email_id)
            logger.info(f"✅ Saved to Inbox: {email_id}")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Error saving email: {e}")
            return False
    
    def check_new_emails(self) -> int:
        """Check for new emails and process them"""
        try:
            imap = self.connect_gmail()
            if not imap:
                return 0
            
            # Get list of emails
            status, msg_ids = imap.search(None, "ALL")
            if status != "OK":
                logger.error("Failed to search emails")
                return 0
            
            msg_id_list = msg_ids[0].split()
            
            # Process only recent emails (last 50)
            new_count = 0
            for msg_id in msg_id_list[-50:]:
                msg_id_decoded = msg_id.decode()
                
                if msg_id_decoded not in self.processed_emails:
                    email_data = self.process_email(msg_id)
                    if email_data:
                        self.save_to_inbox(email_data)
                        new_count += 1
            
            imap.close()
            imap.logout()
            
            if new_count > 0:
                logger.info(f"📨 Found {new_count} new email(s)")
            
            return new_count
        
        except Exception as e:
            logger.error(f"❌ Error checking emails: {e}")
            return 0
    
    def run_once(self) -> bool:
        """Run one polling cycle"""
        logger.info("🔄 Polling Gmail...")
        new_emails = self.check_new_emails()
        logger.info(f"✅ Poll complete. New emails: {new_emails}")
        return True
    
    def run_continuous(self):
        """Run continuous polling"""
        logger.info(f"🚀 Gmail Watcher starting (polling every {self.poll_interval}s)")
        
        try:
            while True:
                self.run_once()
                logger.info(f"⏳ Next poll in {self.poll_interval}s")
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            logger.info("🛑 Gmail Watcher stopped")


def setup_watcher_from_env():
    """Create watcher from environment variables"""
    email = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")
    vault = os.getenv("VAULT_PATH", r"d:\DocuBook-Chatbot folder\Personal AI Employee\AI_Employee_System\Vault")
    
    if not email or not password:
        raise ValueError("GMAIL_ADDRESS and GMAIL_APP_PASSWORD required in .env")
    
    return GmailWatcher(email, password, vault)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
    )
    
    # For testing without real Gmail, create dummy mode
    print("Gmail Watcher")
    print("=" * 50)
    print("\nTo use this watcher:")
    print("1. Create .env file with:")
    print("   GMAIL_ADDRESS=your@gmail.com")
    print("   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx")
    print("\n2. Run: python gmail_watcher.py")
    print("\nThe watcher will check Gmail every 5 minutes")
    print("and save new emails to Vault/Inbox/")
