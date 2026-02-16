"""
INSTAGRAM POSTER
Simple poster module that simulates posting to Instagram (Meta Business placeholder).
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

logger = logging.getLogger("InstagramPoster")


class InstagramPoster:
    """Simulated Instagram poster.

    For production, replace with Meta Business API calls and proper media handling.
    """

    def __init__(self, access_token: Optional[str] = None, business_account_id: Optional[str] = None):
        self.access_token = access_token
        self.account_id = business_account_id
        self.vault = config.VAULT_PATH
        self.log_dir = self.vault / "System" / "social_logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.posts_file = self.log_dir / "instagram_posts.json"

        if not self.posts_file.exists():
            self.posts_file.write_text("[]", encoding="utf-8")

        logger.info("✅ InstagramPoster initialized")

    def generate_caption(self, theme: str, text: str) -> str:
        template = f"{text}\n\n#automation #AI #business"
        return template

    def create_post(self, caption: str, image_path: Optional[str] = None) -> Dict[str, Any]:
        post_id = f"IG_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        post = {
            "post_id": post_id,
            "caption": caption,
            "image": image_path,
            "status": "draft",
            "created_at": datetime.now().isoformat(),
            "published_at": None,
        }

        try:
            arr = json.loads(self.posts_file.read_text(encoding="utf-8"))
            arr.append(post)
            self.posts_file.write_text(json.dumps(arr, indent=2), encoding="utf-8")
            logger.info(f"✅ Instagram post created: {post_id}")
            return post
        except Exception as e:
            logger.error(f"❌ Error creating Instagram post: {e}")
            return {"error": str(e)}

    def publish_post(self, post_id: str) -> Dict[str, Any]:
        try:
            arr = json.loads(self.posts_file.read_text(encoding="utf-8"))
            for p in arr:
                if p.get("post_id") == post_id:
                    p["status"] = "published"
                    p["published_at"] = datetime.now().isoformat()
                    # In production, call Meta Business API here.
                    self.posts_file.write_text(json.dumps(arr, indent=2), encoding="utf-8")
                    logger.info(f"📤 Instagram post published: {post_id}")
                    return {"status": "success", "post_id": post_id}

            return {"status": "error", "message": "Post not found"}
        except Exception as e:
            logger.error(f"❌ Error publishing Instagram post: {e}")
            return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    poster = InstagramPoster()
    caption = poster.generate_caption("automation", "Automating business tasks with AI is a game-changer.")
    post = poster.create_post(caption, image_path=None)
    result = poster.publish_post(post.get("post_id"))

    print("Instagram smoke test:")
    print(post)
    print(result)
