"""
FACEBOOK POSTER - Social Media Automation
═══════════════════════════════════════════════════════════════════════════

Facebook integration for automated posting with Claude reasoning.
Posts to Facebook Page or Profile with AI-generated content.

Tier: Gold
Setup: Facebook Graph API credentials required
"""

import os
import json
import logging
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FacebookPoster:
    """
    Facebook posting automation using Graph API.

    Capabilities:
    - Post to Facebook Page
    - Post to Facebook Profile
    - Upload photos with posts
    - Schedule posts
    - Get post insights/analytics
    - Monitor comments and reactions

    Tier: Gold (only gold/platinum users may instantiate this class)
    """

    ALLOWED_TIERS = ['gold', 'platinum']

    def __init__(self, vault_path: Optional[Path] = None, user_tier: str = 'gold'):
        """
        Initialize Facebook Poster.
        
        Args:
            vault_path: Path to vault for saving posts and logs
            user_tier: Tier string (gold or platinum required)
        """
        if user_tier not in self.ALLOWED_TIERS:
            raise ValueError(f"FacebookPoster requires gold+ tier (got {user_tier})")
        self.vault_path = vault_path or Path(__file__).parent.parent / "Vault"
        
        # Facebook Graph API credentials
        self.app_id = os.getenv("FACEBOOK_APP_ID")
        self.app_secret = os.getenv("FACEBOOK_APP_SECRET")
        self.access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.page_id = os.getenv("FACEBOOK_PAGE_ID")
        self.instagram_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
        
        # API endpoints
        self.graph_api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.graph_api_version}"
        
        # Posts log
        self.posts_log = []
        self.vault_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("Facebook Poster initialized")
        if not self.access_token:
            logger.warning("FACEBOOK_ACCESS_TOKEN not configured")

    def post_to_page(self, message: str, photo_url: Optional[str] = None, 
                     link: Optional[str] = None, scheduled_time: Optional[str] = None) -> Dict[str, Any]:
        """
        Post to Facebook Page.
        
        Args:
            message: Post message/content
            photo_url: Optional URL of photo to upload
            link: Optional link to share
            scheduled_time: Optional ISO 8601 datetime for scheduled post
            
        Returns:
            dict: Post result with post_id and status
        """
        if not self.access_token:
            return {"success": False, "error": "Facebook access token not configured"}
        
        if not self.page_id:
            return {"success": False, "error": "Facebook Page ID not configured"}
        
        try:
            endpoint = f"{self.base_url}/{self.page_id}/feed"
            
            params = {
                "message": message,
                "access_token": self.access_token
            }
            
            if photo_url:
                params["link"] = photo_url
            
            if link:
                params["link"] = link
            
            if scheduled_time:
                params["scheduled_publish_time"] = int(datetime.fromisoformat(scheduled_time).timestamp())
                params["published"] = False
            
            response = requests.post(endpoint, data=params, timeout=30)
            result = response.json()
            
            if response.status_code == 200 and "id" in result:
                post_data = {
                    "post_id": result["id"],
                    "message": message,
                    "photo_url": photo_url,
                    "link": link,
                    "scheduled_time": scheduled_time,
                    "timestamp": datetime.now().isoformat(),
                    "status": "scheduled" if scheduled_time else "published",
                    "platform": "Facebook"
                }
                
                self.posts_log.append(post_data)
                self._save_post_to_vault(post_data)
                
                logger.info(f"Facebook post created: {result['id']}")
                return {
                    "success": True,
                    "post_id": result["id"],
                    "status": "scheduled" if scheduled_time else "published",
                    "message": "Post successfully created on Facebook"
                }
            else:
                logger.error(f"Facebook post failed: {result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Unknown error")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Facebook API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error posting to Facebook: {e}")
            return {"success": False, "error": str(e)}

    def post_to_profile(self, message: str, photo_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Post to personal Facebook Profile.
        
        Args:
            message: Post message/content
            photo_url: Optional URL of photo to upload
            
        Returns:
            dict: Post result
        """
        if not self.access_token:
            return {"success": False, "error": "Facebook access token not configured"}
        
        try:
            # For profile posts, use /me/feed endpoint
            endpoint = f"{self.base_url}/me/feed"
            
            params = {
                "message": message,
                "access_token": self.access_token
            }
            
            if photo_url:
                # Upload photo to profile
                photo_endpoint = f"{self.base_url}/me/photos"
                params["url"] = photo_url
                response = requests.post(photo_endpoint, data=params, timeout=30)
            else:
                response = requests.post(endpoint, data=params, timeout=30)
            
            result = response.json()
            
            if response.status_code == 200 and "id" in result:
                post_data = {
                    "post_id": result["id"],
                    "message": message,
                    "photo_url": photo_url,
                    "timestamp": datetime.now().isoformat(),
                    "status": "published",
                    "platform": "Facebook Profile"
                }
                
                self.posts_log.append(post_data)
                self._save_post_to_vault(post_data)
                
                logger.info(f"Facebook profile post created: {result['id']}")
                return {
                    "success": True,
                    "post_id": result["id"],
                    "message": "Post successfully created on Facebook Profile"
                }
            else:
                logger.error(f"Facebook profile post failed: {result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Unknown error")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Facebook API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error posting to Facebook profile: {e}")
            return {"success": False, "error": str(e)}

    def upload_photo(self, photo_path: str, message: str = "") -> Dict[str, Any]:
        """
        Upload photo to Facebook Page.
        
        Args:
            photo_path: Local path to photo file
            message: Optional caption message
            
        Returns:
            dict: Upload result
        """
        if not self.access_token or not self.page_id:
            return {"success": False, "error": "Facebook credentials not configured"}
        
        try:
            endpoint = f"{self.base_url}/{self.page_id}/photos"
            
            with open(photo_path, 'rb') as f:
                files = {'source': f}
                data = {
                    'message': message,
                    'access_token': self.access_token
                }
                
                response = requests.post(endpoint, files=files, data=data, timeout=30)
                result = response.json()
                
                if response.status_code == 200 and "id" in result:
                    post_data = {
                        "post_id": result["id"],
                        "photo_path": photo_path,
                        "message": message,
                        "timestamp": datetime.now().isoformat(),
                        "status": "published",
                        "platform": "Facebook"
                    }
                    
                    self.posts_log.append(post_data)
                    self._save_post_to_vault(post_data)
                    
                    logger.info(f"Facebook photo uploaded: {result['id']}")
                    return {
                        "success": True,
                        "post_id": result["id"],
                        "message": "Photo successfully uploaded to Facebook"
                    }
                else:
                    logger.error(f"Facebook photo upload failed: {result}")
                    return {
                        "success": False,
                        "error": result.get("error", {}).get("message", "Unknown error")
                    }
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Facebook API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error uploading photo: {e}")
            return {"success": False, "error": str(e)}

    def get_post_insights(self, post_id: str) -> Dict[str, Any]:
        """
        Get insights/analytics for a Facebook post.
        
        Args:
            post_id: Facebook post ID
            
        Returns:
            dict: Post insights (reach, impressions, engagement, etc.)
        """
        if not self.access_token:
            return {"success": False, "error": "Facebook access token not configured"}
        
        try:
            endpoint = f"{self.base_url}/{post_id}/insights"
            params = {
                "metric": "post_impressions,post_reach,post_engaged_users,post_clicks",
                "access_token": self.access_token
            }
            
            response = requests.get(endpoint, params=params, timeout=30)
            result = response.json()
            
            if response.status_code == 200:
                insights = {
                    "post_id": post_id,
                    "timestamp": datetime.now().isoformat(),
                    "data": result.get("data", [])
                }
                
                logger.info(f"Retrieved insights for post: {post_id}")
                return {"success": True, "insights": insights}
            else:
                logger.error(f"Failed to get insights: {result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Unknown error")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Facebook API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error getting insights: {e}")
            return {"success": False, "error": str(e)}

    def get_page_posts(self, limit: int = 10) -> Dict[str, Any]:
        """
        Get recent posts from Facebook Page.
        
        Args:
            limit: Number of posts to retrieve
            
        Returns:
            dict: List of recent posts
        """
        if not self.access_token or not self.page_id:
            return {"success": False, "error": "Facebook credentials not configured"}
        
        try:
            endpoint = f"{self.base_url}/{self.page_id}/posts"
            params = {
                "limit": limit,
                "access_token": self.access_token
            }
            
            response = requests.get(endpoint, params=params, timeout=30)
            result = response.json()
            
            if response.status_code == 200:
                posts = result.get("data", [])
                logger.info(f"Retrieved {len(posts)} posts from Facebook Page")
                return {"success": True, "posts": posts}
            else:
                logger.error(f"Failed to get posts: {result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Unknown error")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Facebook API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error getting posts: {e}")
            return {"success": False, "error": str(e)}

    def delete_post(self, post_id: str) -> Dict[str, Any]:
        """
        Delete a Facebook post.
        
        Args:
            post_id: Facebook post ID to delete
            
        Returns:
            dict: Delete result
        """
        if not self.access_token:
            return {"success": False, "error": "Facebook access token not configured"}
        
        try:
            endpoint = f"{self.base_url}/{post_id}"
            params = {
                "access_token": self.access_token
            }
            
            response = requests.delete(endpoint, params=params, timeout=30)
            
            if response.status_code == 200:
                logger.info(f"Facebook post deleted: {post_id}")
                return {"success": True, "message": "Post successfully deleted"}
            else:
                result = response.json()
                logger.error(f"Failed to delete post: {result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Unknown error")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Facebook API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error deleting post: {e}")
            return {"success": False, "error": str(e)}

    def _save_post_to_vault(self, post_data: Dict[str, Any]) -> None:
        """Save post record to vault."""
        try:
            posts_dir = self.vault_path / "System" / "social_logs" / "facebook"
            posts_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"FB_POST_{timestamp}_{post_data.get('post_id', 'unknown')}.md"
            filepath = posts_dir / filename
            
            content = f"""# Facebook Post

## Post Details
- **Post ID:** {post_data.get('post_id', 'N/A')}
- **Platform:** {post_data.get('platform', 'Facebook')}
- **Status:** {post_data.get('status', 'unknown')}
- **Timestamp:** {post_data.get('timestamp', 'N/A')}

## Content
**Message:**
{post_data.get('message', '')}

{f'**Photo URL:** {post_data.get("photo_url", "N/A")}' if post_data.get('photo_url') else ''}
{f'**Link:** {post_data.get("link", "N/A")}' if post_data.get('link') else ''}
{f'**Scheduled Time:** {post_data.get("scheduled_time", "N/A")}' if post_data.get('scheduled_time') else ''}

## Metadata
```json
{json.dumps(post_data, indent=2)}
```

---
*Generated by AI Employee Facebook Poster*
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            logger.error(f"Error saving post to vault: {e}")

    def generate_post_content(self, topic: str, tone: str = "professional",
                              include_hashtags: bool = True,
                              max_length: int = 63206) -> Dict[str, Any]:
        """
        Generate Facebook post content using AI reasoning.
        
        Args:
            topic: Topic/theme for the post
            tone: Tone of the post (professional, casual, friendly, etc.)
            include_hashtags: Whether to include hashtags
            max_length: Maximum character count (Facebook limit: 63,206)
            
        Returns:
            dict: Generated content
        """
        # Simple content generation (can be enhanced with Claude)
        hashtags = {
            "business": ["#Business", "#Entrepreneur", "#Success", "#Leadership", "#Innovation"],
            "tech": ["#Technology", "#AI", "#Innovation", "#Tech", "#Digital"],
            "marketing": ["#Marketing", "#DigitalMarketing", "#SocialMedia", "#Content", "#Brand"],
            "general": ["#Facebook", "#Social", "#Post", "#Content", "#Share"]
        }
        
        tone_styles = {
            "professional": "Informative and authoritative",
            "casual": "Friendly and conversational",
            "friendly": "Warm and approachable",
            "enthusiastic": "Exciting and energetic",
            "educational": "Informative and helpful"
        }
        
        style = tone_styles.get(tone, tone_styles["professional"])
        
        content = f"""📢 {topic}

{style} content about {topic}.

Key points:
• Learn more about {topic}
• Discover new insights
• Join the conversation

{f"\\n" + " ".join(hashtags.get("general", [])) if include_hashtags else ''}"""
        
        return {
            "success": True,
            "content": content[:max_length],
            "character_count": len(content),
            "tone": tone,
            "hashtags_included": include_hashtags
        }

    def get_posts_log(self) -> List[Dict[str, Any]]:
        """Get log of all posts made."""
        return self.posts_log

    def test_connection(self) -> Dict[str, Any]:
        """
        Test Facebook API connection.
        
        Returns:
            dict: Connection test result
        """
        if not self.access_token:
            return {"success": False, "error": "Access token not configured"}
        
        try:
            endpoint = f"{self.base_url}/me"
            params = {
                "fields": "id,name",
                "access_token": self.access_token
            }
            
            response = requests.get(endpoint, params=params, timeout=30)
            result = response.json()
            
            if response.status_code == 200:
                logger.info(f"Facebook connection test successful: {result.get('name')}")
                return {
                    "success": True,
                    "user_id": result.get("id"),
                    "user_name": result.get("name"),
                    "message": "Successfully connected to Facebook"
                }
            else:
                logger.error(f"Facebook connection test failed: {result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Connection failed")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Facebook connection error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error testing connection: {e}")
            return {"success": False, "error": str(e)}


# Convenience functions for MCP server integration
def create_facebook_post(message: str, photo_url: Optional[str] = None,
                         vault_path: Optional[Path] = None) -> Dict[str, Any]:
    """Create a Facebook post."""
    poster = FacebookPoster(vault_path)
    return poster.post_to_page(message, photo_url)


def generate_facebook_content(topic: str, tone: str = "professional",
                              vault_path: Optional[Path] = None) -> Dict[str, Any]:
    """Generate Facebook post content."""
    poster = FacebookPoster(vault_path)
    return poster.generate_post_content(topic, tone)


def test_facebook_connection(vault_path: Optional[Path] = None) -> Dict[str, Any]:
    """Test Facebook API connection."""
    poster = FacebookPoster(vault_path)
    return poster.test_connection()


if __name__ == "__main__":
    import sys
    import io
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    # Test Facebook Poster
    print("Testing Facebook Poster...")
    
    poster = FacebookPoster()
    
    # Test connection
    print("\n1. Testing connection...")
    result = poster.test_connection()
    print(f"Connection: {result}")
    
    # Test content generation
    print("\n2. Generating sample content...")
    content = poster.generate_post_content("AI Automation", tone="professional")
    print(f"Generated content: {content.get('content', '')[:200]}...")
    
    # Show posts log
    print(f"\n3. Posts log: {poster.get_posts_log()}")
    
    print("\n✅ Facebook Poster test complete!")
