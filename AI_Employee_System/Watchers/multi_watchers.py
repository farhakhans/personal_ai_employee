"""
WHATSAPP WATCHER (Silver Tier)
Monitors WhatsApp Business API for incoming messages
Processes and stores them in vault
"""

import os
import logging
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# import other watcher classes to allow multi-user orchestration
from AI_Employee_System.Watchers.gmail_watcher import GmailWatcher
from AI_Employee_System.Watchers.whatsapp_watcher import WhatsAppWatcher

logger = logging.getLogger("WhatsAppWatcher")


class WhatsAppWatcher:
    """Monitors WhatsApp Business API"""
    
    def __init__(self, phone_number_id: str, access_token: str, vault_path: str):
        """
        phone_number_id: WhatsApp Business Phone Number ID
        access_token: Meta API access token
        vault_path: Path to vault
        """
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.vault_path = Path(vault_path)
        self.processed_messages = set()
        logger.info("✅ WhatsApp Watcher initialized (Silver Tier)")
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """Fetch recent messages from WhatsApp"""
        # Phase 2: Implement Meta WhatsApp Business API
        logger.info("📱 Connecting to WhatsApp API (Meta)...")
        
        # Mock response for now
        return [
            {
                "message_id": "wamid.001",
                "from": {"phone_number": "+1234567890", "name": "John Client"},
                "text": "Hi, interested in your services",
                "timestamp": datetime.now().isoformat()
            }
        ]
    
    def process_message(self, message: Dict[str, Any]) -> bool:
        """Process a WhatsApp message"""
        try:
            msg_id = message.get("message_id")
            
            if msg_id in self.processed_messages:
                return False
            
            from_number = message.get("from", {}).get("phone_number", "Unknown")
            text = message.get("text", "")
            timestamp = message.get("timestamp", datetime.now().isoformat())
            
            # Save to vault
            inbox_path = self.vault_path / "Inbox" / f"WHATSAPP_{msg_id}.md"
            
            content = f"""# WhatsApp Message
**From:** {from_number}  
**Date:** {timestamp}  
**Status:** 📲 Received

## Message
{text}

## Actions
- [ ] Reply
- [ ] Escalate
- [ ] Archive

---
*Captured by WhatsApp Watcher*
"""
            
            inbox_path.write_text(content, encoding='utf-8')
            self.processed_messages.add(msg_id)
            logger.info(f"✅ WhatsApp message saved: {msg_id}")
            
            return True
        except Exception as e:
            logger.error(f"❌ Error processing WhatsApp message: {e}")
            return False


class LinkedInWatcher:
    """Monitors LinkedIn for mentions and engagement (Silver Tier)"""

    def __init__(self, access_token: str, vault_path: str):
        self.access_token = access_token
        self.vault_path = Path(vault_path)
        self.person_urn = os.getenv("LINKEDIN_PERSON_URN")
        self.base_url = "https://api.linkedin.com/v2"
        logger.info("✅ LinkedIn Watcher initialized (Silver Tier)")

    def get_mentions(self) -> List[Dict[str, Any]]:
        """Get LinkedIn mentions and comments"""
        logger.info("🔗 Checking LinkedIn mentions...")
        
        if not self.access_token:
            logger.warning("⚠️ LinkedIn access token not configured")
            return []
        
        try:
            # Get notifications (includes mentions)
            endpoint = f"{self.base_url}/notifications"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            params = {
                "count": 50,
                "projection": "(elements*(id,activity,actionType,created))"
            }
            
            response = requests.get(
                endpoint,
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                elements = data.get("elements", [])
                
                mentions = []
                for element in elements:
                    action_type = element.get("actionType", "")
                    
                    # Filter for mentions, comments, and likes
                    if action_type in ["MENTION", "COMMENT", "LIKE"]:
                        mention_data = {
                            "id": element.get("id"),
                            "type": action_type.lower(),
                            "activity": element.get("activity"),
                            "created_at": element.get("created"),
                            "actor": element.get("activity", {}).get("actor", {}),
                            "text": element.get("activity", {}).get("text", "")
                        }
                        mentions.append(mention_data)
                
                logger.info(f"✅ Found {len(mentions)} LinkedIn mentions/interactions")
                return mentions
            else:
                logger.error(f"❌ Failed to fetch LinkedIn mentions: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error fetching LinkedIn mentions: {e}")
            return []

    def get_profile_visits(self) -> int:
        """Get recent profile visits"""
        logger.info("👀 Checking profile visits...")
        
        if not self.access_token:
            return 0
        
        try:
            # LinkedIn API doesn't directly expose profile visits
            # Return 0 or implement via LinkedIn Analytics API
            return 0
        except Exception as e:
            logger.error(f"❌ Error fetching profile visits: {e}")
            return 0

    def get_recent_activity(self) -> Dict[str, Any]:
        """Get recent LinkedIn activity including posts and engagement"""
        logger.info("📊 Fetching recent LinkedIn activity...")
        
        if not self.access_token or not self.person_urn:
            return {"success": False, "error": "Credentials not configured"}
        
        try:
            # Get posts
            posts_endpoint = f"{self.base_url}/shares"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            posts_params = {
                "q": "owners",
                "owners": self.person_urn,
                "count": 10
            }
            
            posts_response = requests.get(
                posts_endpoint,
                headers=headers,
                params=posts_params,
                timeout=30
            )
            
            posts = []
            if posts_response.status_code == 200:
                posts_data = posts_response.json()
                posts = posts_data.get("elements", [])
            
            # Get notifications
            notifications_endpoint = f"{self.base_url}/notifications"
            
            notifications_params = {
                "count": 20
            }
            
            notifications_response = requests.get(
                notifications_endpoint,
                headers=headers,
                params=notifications_params,
                timeout=30
            )
            
            notifications = []
            if notifications_response.status_code == 200:
                notifications_data = notifications_response.json()
                notifications = notifications_data.get("elements", [])
            
            result = {
                "success": True,
                "posts": posts,
                "notifications": notifications,
                "posts_count": len(posts),
                "notifications_count": len(notifications)
            }
            
            logger.info(f"✅ Fetched {len(posts)} posts and {len(notifications)} notifications")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error fetching LinkedIn activity: {e}")
            return {"success": False, "error": str(e)}


class TwitterWatcher:
    """Monitors Twitter/X for mentions (Silver Tier+)"""
    
    def __init__(self, api_key: str, api_secret: str, vault_path: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.vault_path = Path(vault_path)
        logger.info("✅ Twitter Watcher initialized (Silver Tier+)")
    
    def get_mentions(self) -> List[Dict[str, Any]]:
        """Get Tweet mentions"""
        logger.info("🐦 Checking Twitter mentions...")
        return []


class MultiWatcherOrchestrator:
    """Silver Tier: Manages multiple watchers

    This orchestrator reads the user database and creates per-user watchers
    according to their configured integrations.  It uses the same watcher
    classes defined in this module but passes credentials from the database.
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.watchers = {}  # key: user_{id}_{integration}

        # load users and their integrations
        try:
            from auth_db import db
            users = db.get_all_users(limit=1000)
            for u in users:
                if not u['is_active']:
                    continue
                user_id = u['id']
                integr = db.get_user_integrations(user_id)
                tier = u.get('tier', 'bronze')
                # Gmail
                if 'gmail' in integr and tier in ['bronze','silver','gold','platinum']:
                    cfg = integr['gmail']
                    try:
                        watcher = GmailWatcher(cfg.get('email',''), cfg.get('app_password',''), vault_path, user_tier=tier)
                        self.register_watcher(f"user_{user_id}_gmail", watcher)
                    except Exception as e:
                        logger.warning(f"Skipping gmail watcher for user {user_id}: {e}")
                # WhatsApp (playwright)
                if 'whatsapp' in integr and tier in ['bronze','silver','gold','platinum']:
                    try:
                        watcher = WhatsAppWatcher(vault_path, user_tier=tier)
                        self.register_watcher(f"user_{user_id}_whatsapp", watcher)
                    except Exception as e:
                        logger.warning(f"Skipping whatsapp watcher for user {user_id}: {e}")
                # LinkedIn
                if 'linkedin' in integr and tier in ['silver','gold','platinum']:
                    cfg = integr['linkedin']
                    try:
                        watcher = LinkedInWatcher(cfg.get('token',''), vault_path)
                        self.register_watcher(f"user_{user_id}_linkedin", watcher)
                    except Exception as e:
                        logger.warning(f"Skipping linkedin watcher for user {user_id}: {e}")
                # Facebook and others would have their own watchers if defined
        except Exception as e:
            logger.error(f"Error initializing MultiWatcherOrchestrator: {e}")

        logger.info("✅ Multi-Watcher Orchestrator initialized (Silver Tier)")
    
    def register_watcher(self, name: str, watcher: Any):
        """Register a watcher"""
        self.watchers[name] = watcher
        logger.info(f"✅ Registered watcher: {name}")
    
    def run_all_watchers(self) -> Dict[str, int]:
        """Run all registered watchers"""
        results = {}
        
        for name, watcher in self.watchers.items():
            logger.info(f"🔄 Running watcher: {name}")
            results[name] = 0  # Message count
        
        return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Multi-Watcher System (Silver Tier)")
    print("Watchers: Gmail, WhatsApp, LinkedIn, Twitter")
