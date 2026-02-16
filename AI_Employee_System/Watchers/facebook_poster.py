"""
FACEBOOK POSTER
Simple poster module that simulates posting to Facebook (Graph API placeholder).
Creates local audit entries in the vault for traceability.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from pathlib import Path
import sys

# Ensure project root is on sys.path so `config` can be imported when running as script
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))
import config

logger = logging.getLogger("FacebookPoster")


class FacebookPoster:
    """Simulated Facebook poster.

    For production, replace internal methods with calls to the
    Facebook Graph API (with proper credentials and app review).
    """

    def __init__(self, access_token: Optional[str] = None, page_id: Optional[str] = None):
        self.access_token = access_token
        self.page_id = page_id
        self.vault = config.VAULT_PATH
        self.log_dir = self.vault / "System" / "social_logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.posts_file = self.log_dir / "facebook_posts.json"

        # ensure file exists
        if not self.posts_file.exists():
            self.posts_file.write_text("[]", encoding="utf-8")

        logger.info("✅ FacebookPoster initialized")

    def generate_post(self, topic: str, details: Dict[str, Any]) -> str:
        templates = {
            "sales": "🎯 Exciting news! We just {action}. {details}",
            "update": "📢 Update: {details}",
            "announcement": "📣 Announcing: {announcement}. {details}",
            "default": "📝 {details}",
        }

        template = templates.get(topic, templates["default"])
        post = template.format(
            action=details.get("action", "launched something new"),
            details=details.get("text", ""),
            announcement=details.get("announcement", ""),
        )
        return post

    def create_post(self, content: str, media: Optional[List[str]] = None) -> Dict[str, Any]:
        post_id = f"FB_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        post = {
            "post_id": post_id,
            "content": content,
            "media": media or [],
            "status": "draft",
            "created_at": datetime.now().isoformat(),
            "published_at": None,
        }

        # append to local JSON log
        try:
            arr = json.loads(self.posts_file.read_text(encoding="utf-8"))
            arr.append(post)
            self.posts_file.write_text(json.dumps(arr, indent=2), encoding="utf-8")
            logger.info(f"✅ Facebook post created: {post_id}")
            return post
        except Exception as e:
            logger.error(f"❌ Error creating Facebook post: {e}")
            return {"error": str(e)}

    def publish_post(self, post_id: str) -> Dict[str, Any]:
        try:
            arr = json.loads(self.posts_file.read_text(encoding="utf-8"))
            for p in arr:
                if p.get("post_id") == post_id:
                    p["status"] = "published"
                    p["published_at"] = datetime.now().isoformat()
                    # In production, call Facebook Graph API here.
                    self.posts_file.write_text(json.dumps(arr, indent=2), encoding="utf-8")
                    logger.info(f"📤 Facebook post published: {post_id}")
                    return {"status": "success", "post_id": post_id}

            return {"status": "error", "message": "Post not found"}
        except Exception as e:
            logger.error(f"❌ Error publishing Facebook post: {e}")
            return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    poster = FacebookPoster()
    content = poster.generate_post("sales", {"action": "closed a new client", "text": "We helped ClientA reduce costs by 30%"})
    post = poster.create_post(content)
    result = poster.publish_post(post.get("post_id"))

    print("Facebook smoke test:")
    print(post)
    print(result)
