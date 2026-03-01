"""
INSTAGRAM POSTER - Social Media Automation
═══════════════════════════════════════════════════════════════════════════

Instagram integration for automated posting with Claude reasoning.
Posts to Instagram Feed, Stories, and Reels via Meta Graph API.

Tier: Gold
Setup: Instagram Business Account + Meta App credentials required
"""

import os
import json
import logging
import requests
from datetime import datetime, timedelta
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


class InstagramPoster:
    """
    Instagram posting automation using Meta Graph API.
    
    Capabilities:
    - Post to Instagram Feed (images, carousels)
    - Post to Instagram Stories
    - Post to Instagram Reels
    - Schedule posts
    - Get media insights/analytics
    - Monitor comments and likes
    """

    def __init__(self, vault_path: Optional[Path] = None):
        """
        Initialize Instagram Poster.
        
        Args:
            vault_path: Path to vault for saving posts and logs
        """
        self.vault_path = vault_path or Path(__file__).parent.parent / "Vault"
        
        # Meta/Instagram API credentials
        self.app_id = os.getenv("META_APP_ID")
        self.app_secret = os.getenv("META_APP_SECRET")
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.instagram_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
        self.facebook_page_id = os.getenv("FACEBOOK_PAGE_ID")  # Required for Instagram posting
        
        # API endpoints
        self.graph_api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.graph_api_version}"
        
        # Posts log
        self.posts_log = []
        self.vault_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("Instagram Poster initialized")
        if not self.access_token:
            logger.warning("INSTAGRAM_ACCESS_TOKEN not configured")
        if not self.instagram_account_id:
            logger.warning("INSTAGRAM_ACCOUNT_ID not configured")

    def post_image(self, image_url: str, caption: str = "", 
                   is_carousel: bool = False) -> Dict[str, Any]:
        """
        Post an image to Instagram Feed.
        
        Args:
            image_url: URL of the image to post
            caption: Post caption
            is_carousel: Whether this is part of a carousel album
            
        Returns:
            dict: Post result with media_id and status
        """
        if not self.access_token or not self.instagram_account_id:
            return {"success": False, "error": "Instagram credentials not configured"}
        
        try:
            # Step 1: Create media container
            endpoint = f"{self.base_url}/{self.instagram_account_id}/media"
            
            params = {
                "image_url": image_url,
                "caption": caption,
                "access_token": self.access_token
            }
            
            if is_carousel:
                # For carousel, we need to create multiple containers first
                params["is_carousel_item"] = True
            
            response = requests.post(endpoint, data=params, timeout=30)
            result = response.json()
            
            if response.status_code == 200 and "id" in result:
                media_id = result["id"]
                
                # Step 2: Publish the media
                publish_endpoint = f"{self.base_url}/{self.instagram_account_id}/media_publish"
                publish_params = {
                    "creation_id": media_id,
                    "access_token": self.access_token
                }
                
                publish_response = requests.post(publish_endpoint, data=publish_params, timeout=30)
                publish_result = publish_response.json()
                
                if publish_response.status_code == 200 and "id" in publish_result:
                    post_data = {
                        "media_id": media_id,
                        "post_id": publish_result["id"],
                        "caption": caption,
                        "image_url": image_url,
                        "is_carousel": is_carousel,
                        "timestamp": datetime.now().isoformat(),
                        "status": "published",
                        "platform": "Instagram"
                    }
                    
                    self.posts_log.append(post_data)
                    self._save_post_to_vault(post_data)
                    
                    logger.info(f"Instagram post created: {publish_result['id']}")
                    return {
                        "success": True,
                        "media_id": media_id,
                        "post_id": publish_result["id"],
                        "message": "Image successfully posted to Instagram"
                    }
                else:
                    logger.error(f"Instagram publish failed: {publish_result}")
                    return {
                        "success": False,
                        "error": publish_result.get("error", {}).get("message", "Publish failed")
                    }
            else:
                logger.error(f"Instagram media creation failed: {result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Media creation failed")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Instagram API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error posting to Instagram: {e}")
            return {"success": False, "error": str(e)}

    def post_video(self, video_url: str, caption: str = "",
                   thumbnail_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Post a video to Instagram (Feed or Reels).
        
        Args:
            video_url: URL of the video to post
            caption: Post caption
            thumbnail_url: Optional thumbnail URL for the video
            
        Returns:
            dict: Post result
        """
        if not self.access_token or not self.instagram_account_id:
            return {"success": False, "error": "Instagram credentials not configured"}
        
        try:
            endpoint = f"{self.base_url}/{self.instagram_account_id}/media"
            
            params = {
                "video_url": video_url,
                "caption": caption,
                "media_type": "REELS",  # Use "IGTV" for longer videos
                "access_token": self.access_token
            }
            
            if thumbnail_url:
                params["thumb_url"] = thumbnail_url
            
            response = requests.post(endpoint, data=params, timeout=30)
            result = response.json()
            
            if response.status_code == 200 and "id" in result:
                media_id = result["id"]
                
                # Publish the video
                publish_endpoint = f"{self.base_url}/{self.instagram_account_id}/media_publish"
                publish_params = {
                    "creation_id": media_id,
                    "access_token": self.access_token
                }
                
                publish_response = requests.post(publish_endpoint, data=publish_params, timeout=30)
                publish_result = publish_response.json()
                
                if publish_response.status_code == 200 and "id" in publish_result:
                    post_data = {
                        "media_id": media_id,
                        "post_id": publish_result["id"],
                        "caption": caption,
                        "video_url": video_url,
                        "thumbnail_url": thumbnail_url,
                        "media_type": "reel",
                        "timestamp": datetime.now().isoformat(),
                        "status": "published",
                        "platform": "Instagram"
                    }
                    
                    self.posts_log.append(post_data)
                    self._save_post_to_vault(post_data)
                    
                    logger.info(f"Instagram reel created: {publish_result['id']}")
                    return {
                        "success": True,
                        "media_id": media_id,
                        "post_id": publish_result["id"],
                        "message": "Video successfully posted to Instagram Reels"
                    }
                else:
                    logger.error(f"Instagram video publish failed: {publish_result}")
                    return {
                        "success": False,
                        "error": publish_result.get("error", {}).get("message", "Publish failed")
                    }
            else:
                logger.error(f"Instagram video creation failed: {result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Video creation failed")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Instagram API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error posting video: {e}")
            return {"success": False, "error": str(e)}

    def post_story(self, image_url: str, sticker_config: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Post to Instagram Story.
        
        Args:
            image_url: URL of the image for the story
            sticker_config: Optional configuration for story stickers
            
        Returns:
            dict: Story post result
        """
        if not self.access_token or not self.instagram_account_id:
            return {"success": False, "error": "Instagram credentials not configured"}
        
        try:
            endpoint = f"{self.base_url}/{self.instagram_account_id}/media"
            
            params = {
                "image_url": image_url,
                "media_type": "STORY",
                "access_token": self.access_token
            }
            
            # Add story stickers if provided (location, hashtag, mention, etc.)
            if sticker_config:
                params["story_sticker_ids"] = ",".join(sticker_config.get("sticker_ids", []))
            
            response = requests.post(endpoint, data=params, timeout=30)
            result = response.json()
            
            if response.status_code == 200 and "id" in result:
                media_id = result["id"]
                
                # Publish the story
                publish_endpoint = f"{self.base_url}/{self.instagram_account_id}/media_publish"
                publish_params = {
                    "creation_id": media_id,
                    "access_token": self.access_token
                }
                
                publish_response = requests.post(publish_endpoint, data=publish_params, timeout=30)
                publish_result = publish_response.json()
                
                if publish_response.status_code == 200 and "id" in publish_result:
                    post_data = {
                        "media_id": media_id,
                        "post_id": publish_result["id"],
                        "image_url": image_url,
                        "media_type": "story",
                        "timestamp": datetime.now().isoformat(),
                        "status": "published",
                        "platform": "Instagram Story",
                        "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
                    }
                    
                    self.posts_log.append(post_data)
                    self._save_post_to_vault(post_data)
                    
                    logger.info(f"Instagram story created: {publish_result['id']}")
                    return {
                        "success": True,
                        "media_id": media_id,
                        "post_id": publish_result["id"],
                        "message": "Story successfully posted to Instagram",
                        "expires_in_hours": 24
                    }
                else:
                    logger.error(f"Instagram story publish failed: {publish_result}")
                    return {
                        "success": False,
                        "error": publish_result.get("error", {}).get("message", "Story publish failed")
                    }
            else:
                logger.error(f"Instagram story creation failed: {result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Story creation failed")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Instagram API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error posting story: {e}")
            return {"success": False, "error": str(e)}

    def post_carousel(self, media_items: List[Dict[str, str]], 
                      caption: str = "") -> Dict[str, Any]:
        """
        Post a carousel (multiple images/videos) to Instagram.
        
        Args:
            media_items: List of media items, each with 'url' and optional 'type'
            caption: Post caption
            
        Returns:
            dict: Carousel post result
        """
        if not self.access_token or not self.instagram_account_id:
            return {"success": False, "error": "Instagram credentials not configured"}
        
        if len(media_items) < 2 or len(media_items) > 10:
            return {"success": False, "error": "Carousel must have 2-10 media items"}
        
        try:
            # Step 1: Create container for each media item
            container_ids = []
            
            for item in media_items:
                endpoint = f"{self.base_url}/{self.instagram_account_id}/media"
                
                media_type = item.get("type", "IMAGE").upper()
                params = {
                    "image_url" if media_type == "IMAGE" else "video_url": item["url"],
                    "is_carousel_item": True,
                    "access_token": self.access_token
                }
                
                response = requests.post(endpoint, data=params, timeout=30)
                result = response.json()
                
                if response.status_code == 200 and "id" in result:
                    container_ids.append(result["id"])
                else:
                    logger.error(f"Carousel item creation failed: {result}")
                    return {
                        "success": False,
                        "error": f"Failed to create carousel item: {result.get('error', {})}"
                    }
            
            # Step 2: Create carousel container
            carousel_endpoint = f"{self.base_url}/{self.instagram_account_id}/media"
            carousel_params = {
                "media_type": "CAROUSEL",
                "children": ",".join(container_ids),
                "caption": caption,
                "access_token": self.access_token
            }
            
            carousel_response = requests.post(carousel_endpoint, data=carousel_params, timeout=30)
            carousel_result = carousel_response.json()
            
            if carousel_response.status_code == 200 and "id" in carousel_result:
                # Step 3: Publish carousel
                publish_endpoint = f"{self.base_url}/{self.instagram_account_id}/media_publish"
                publish_params = {
                    "creation_id": carousel_result["id"],
                    "access_token": self.access_token
                }
                
                publish_response = requests.post(publish_endpoint, data=publish_params, timeout=30)
                publish_result = publish_response.json()
                
                if publish_response.status_code == 200 and "id" in publish_result:
                    post_data = {
                        "media_id": carousel_result["id"],
                        "post_id": publish_result["id"],
                        "caption": caption,
                        "media_items": media_items,
                        "container_ids": container_ids,
                        "media_type": "carousel",
                        "timestamp": datetime.now().isoformat(),
                        "status": "published",
                        "platform": "Instagram"
                    }
                    
                    self.posts_log.append(post_data)
                    self._save_post_to_vault(post_data)
                    
                    logger.info(f"Instagram carousel created: {publish_result['id']}")
                    return {
                        "success": True,
                        "media_id": carousel_result["id"],
                        "post_id": publish_result["id"],
                        "items_count": len(media_items),
                        "message": "Carousel successfully posted to Instagram"
                    }
                else:
                    logger.error(f"Carousel publish failed: {publish_result}")
                    return {
                        "success": False,
                        "error": publish_result.get("error", {}).get("message", "Carousel publish failed")
                    }
            else:
                logger.error(f"Carousel creation failed: {carousel_result}")
                return {
                    "success": False,
                    "error": carousel_result.get("error", {}).get("message", "Carousel creation failed")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Instagram API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error posting carousel: {e}")
            return {"success": False, "error": str(e)}

    def schedule_post(self, image_url: str, caption: str,
                      publish_time: datetime) -> Dict[str, Any]:
        """
        Schedule a post for later publishing.
        
        Args:
            image_url: URL of the image to post
            caption: Post caption
            publish_time: datetime for when to publish
            
        Returns:
            dict: Scheduled post result
        """
        if not self.access_token or not self.instagram_account_id:
            return {"success": False, "error": "Instagram credentials not configured"}
        
        try:
            # Instagram requires publishing within 5 days of creation
            if publish_time < datetime.now() or publish_time > datetime.now() + timedelta(days=5):
                return {
                    "success": False,
                    "error": "Publish time must be between now and 5 days in the future"
                }
            
            # Create the media
            endpoint = f"{self.base_url}/{self.instagram_account_id}/media"
            params = {
                "image_url": image_url,
                "caption": caption,
                "scheduled_publish_time": int(publish_time.timestamp()),
                "access_token": self.access_token
            }
            
            response = requests.post(endpoint, data=params, timeout=30)
            result = response.json()
            
            if response.status_code == 200 and "id" in result:
                post_data = {
                    "media_id": result["id"],
                    "caption": caption,
                    "image_url": image_url,
                    "scheduled_time": publish_time.isoformat(),
                    "timestamp": datetime.now().isoformat(),
                    "status": "scheduled",
                    "platform": "Instagram"
                }
                
                self.posts_log.append(post_data)
                self._save_post_to_vault(post_data)
                
                logger.info(f"Instagram post scheduled for {publish_time}")
                return {
                    "success": True,
                    "media_id": result["id"],
                    "scheduled_time": publish_time.isoformat(),
                    "message": f"Post scheduled for {publish_time.strftime('%Y-%m-%d %H:%M')}"
                }
            else:
                logger.error(f"Instagram schedule failed: {result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Schedule failed")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Instagram API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error scheduling post: {e}")
            return {"success": False, "error": str(e)}

    def get_media_insights(self, media_id: str) -> Dict[str, Any]:
        """
        Get insights/analytics for an Instagram post.
        
        Args:
            media_id: Instagram media ID
            
        Returns:
            dict: Media insights (impressions, reach, engagement, etc.)
        """
        if not self.access_token:
            return {"success": False, "error": "Instagram access token not configured"}
        
        try:
            endpoint = f"{self.base_url}/{media_id}/insights"
            params = {
                "metric": "impressions,reach,engagement,saved,video_views",
                "access_token": self.access_token
            }
            
            response = requests.get(endpoint, params=params, timeout=30)
            result = response.json()
            
            if response.status_code == 200:
                insights = {
                    "media_id": media_id,
                    "timestamp": datetime.now().isoformat(),
                    "data": result.get("data", [])
                }
                
                logger.info(f"Retrieved insights for media: {media_id}")
                return {"success": True, "insights": insights}
            else:
                logger.error(f"Failed to get insights: {result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Unknown error")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Instagram API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error getting insights: {e}")
            return {"success": False, "error": str(e)}

    def get_recent_media(self, limit: int = 10) -> Dict[str, Any]:
        """
        Get recent media posts from Instagram account.
        
        Args:
            limit: Number of posts to retrieve
            
        Returns:
            dict: List of recent media
        """
        if not self.access_token or not self.instagram_account_id:
            return {"success": False, "error": "Instagram credentials not configured"}
        
        try:
            endpoint = f"{self.base_url}/{self.instagram_account_id}/media"
            params = {
                "limit": limit,
                "fields": "id,caption,media_type,media_url,permalink,timestamp",
                "access_token": self.access_token
            }
            
            response = requests.get(endpoint, params=params, timeout=30)
            result = response.json()
            
            if response.status_code == 200:
                media = result.get("data", [])
                logger.info(f"Retrieved {len(media)} media posts from Instagram")
                return {"success": True, "media": media}
            else:
                logger.error(f"Failed to get media: {result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Unknown error")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Instagram API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error getting media: {e}")
            return {"success": False, "error": str(e)}

    def delete_media(self, media_id: str) -> Dict[str, Any]:
        """
        Delete an Instagram media post.
        
        Args:
            media_id: Instagram media ID to delete
            
        Returns:
            dict: Delete result
        """
        if not self.access_token:
            return {"success": False, "error": "Instagram access token not configured"}
        
        try:
            endpoint = f"{self.base_url}/{media_id}"
            params = {
                "access_token": self.access_token
            }
            
            response = requests.delete(endpoint, params=params, timeout=30)
            
            if response.status_code == 200:
                logger.info(f"Instagram media deleted: {media_id}")
                return {"success": True, "message": "Media successfully deleted"}
            else:
                result = response.json()
                logger.error(f"Failed to delete media: {result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Unknown error")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Instagram API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error deleting media: {e}")
            return {"success": False, "error": str(e)}

    def _save_post_to_vault(self, post_data: Dict[str, Any]) -> None:
        """Save post record to vault."""
        try:
            posts_dir = self.vault_path / "System" / "social_logs" / "instagram"
            posts_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"IG_POST_{timestamp}_{post_data.get('post_id', 'unknown')}.md"
            filepath = posts_dir / filename
            
            content = f"""# Instagram Post

## Post Details
- **Post ID:** {post_data.get('post_id', 'N/A')}
- **Media ID:** {post_data.get('media_id', 'N/A')}
- **Platform:** {post_data.get('platform', 'Instagram')}
- **Media Type:** {post_data.get('media_type', 'image')}
- **Status:** {post_data.get('status', 'unknown')}
- **Timestamp:** {post_data.get('timestamp', 'N/A')}
{f'- **Expires At:** {post_data.get("expires_at", "N/A")}' if post_data.get('expires_at') else ''}

## Content
**Caption:**
{post_data.get('caption', '')}

{f'**Image URL:** {post_data.get("image_url", "N/A")}' if post_data.get('image_url') else ''}
{f'**Video URL:** {post_data.get("video_url", "N/A")}' if post_data.get('video_url') else ''}
{f'**Scheduled Time:** {post_data.get("scheduled_time", "N/A")}' if post_data.get('scheduled_time') else ''}

## Metadata
```json
{json.dumps(post_data, indent=2)}
```

---
*Generated by AI Employee Instagram Poster*
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            logger.error(f"Error saving post to vault: {e}")

    def generate_post_content(self, topic: str, tone: str = "professional",
                              include_emojis: bool = True,
                              include_hashtags: bool = True,
                              max_length: int = 2200) -> Dict[str, Any]:
        """
        Generate Instagram post content using AI reasoning.
        
        Args:
            topic: Topic/theme for the post
            tone: Tone of the post
            include_emojis: Whether to include emojis
            include_hashtags: Whether to include hashtags
            max_length: Maximum character count (Instagram limit: 2,200)
            
        Returns:
            dict: Generated content
        """
        emojis = {
            "business": ["💼", "📊", "📈", "💡", "🎯"],
            "tech": ["💻", "🤖", "🚀", "⚡", "🔧"],
            "lifestyle": ["✨", "🌟", "💫", "🌈", "🎨"],
            "fitness": ["💪", "🏋️", "🏃", "🧘", "💯"],
            "food": ["🍕", "🍔", "🍰", "☕", "🍷"],
            "travel": ["✈️", "🌍", "🏖️", "🗺️", "📸"],
            "general": ["📷", "✨", "👍", "💯", "🔥"]
        }
        
        hashtags = {
            "business": ["#Business", "#Entrepreneur", "#Success", "#Leadership", "#Mindset"],
            "tech": ["#Technology", "#AI", "#Innovation", "#Tech", "#Digital"],
            "lifestyle": ["#Lifestyle", "#Life", "#Motivation", "#Inspiration", "#Goals"],
            "fitness": ["#Fitness", "#Workout", "#Gym", "#Health", "#FitnessMotivation"],
            "food": ["#Food", "#Foodie", "#Delicious", "#Yummy", "#FoodPhotography"],
            "travel": ["#Travel", "#Wanderlust", "#Adventure", "#TravelPhotography", "#Explore"],
            "general": ["#Instagram", "#Photo", "#Love", "#InstaGood", "#PicOfTheDay"]
        }
        
        tone_styles = {
            "professional": "Informative and authoritative",
            "casual": "Friendly and conversational",
            "friendly": "Warm and approachable",
            "enthusiastic": "Exciting and energetic",
            "inspirational": "Motivating and uplifting"
        }
        
        style = tone_styles.get(tone, tone_styles["professional"])
        category_emojis = emojis.get("general", emojis["general"])
        category_hashtags = hashtags.get("general", hashtags["general"])
        
        emoji_str = " ".join(category_emojis[:3]) if include_emojis else ""
        hashtag_str = "\n\n" + " ".join(category_hashtags[:5]) if include_hashtags else ""
        
        content = f"""{emoji_str} {topic}

{style} content about {topic}.

Key points:
• Discover more about {topic}
• Save this for later
• Share with someone who needs this

Tag a friend who would love this! 👇

{hashtag_str}"""
        
        return {
            "success": True,
            "content": content[:max_length],
            "character_count": len(content),
            "tone": tone,
            "emojis_included": include_emojis,
            "hashtags_included": include_hashtags
        }

    def get_posts_log(self) -> List[Dict[str, Any]]:
        """Get log of all posts made."""
        return self.posts_log

    def test_connection(self) -> Dict[str, Any]:
        """
        Test Instagram API connection.
        
        Returns:
            dict: Connection test result
        """
        if not self.access_token:
            return {"success": False, "error": "Access token not configured"}
        
        try:
            endpoint = f"{self.base_url}/{self.instagram_account_id}"
            params = {
                "fields": "id,username,name,biography,followers_count,media_count",
                "access_token": self.access_token
            }
            
            response = requests.get(endpoint, params=params, timeout=30)
            result = response.json()
            
            if response.status_code == 200:
                logger.info(f"Instagram connection test successful: {result.get('username')}")
                return {
                    "success": True,
                    "account_id": result.get("id"),
                    "username": result.get("username"),
                    "name": result.get("name"),
                    "followers": result.get("followers_count"),
                    "media_count": result.get("media_count"),
                    "message": "Successfully connected to Instagram"
                }
            else:
                logger.error(f"Instagram connection test failed: {result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Connection failed")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Instagram connection error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error testing connection: {e}")
            return {"success": False, "error": str(e)}


# Convenience functions for MCP server integration
def create_instagram_post(image_url: str, caption: str = "",
                          vault_path: Optional[Path] = None) -> Dict[str, Any]:
    """Create an Instagram post."""
    poster = InstagramPoster(vault_path)
    return poster.post_image(image_url, caption)


def generate_instagram_content(topic: str, tone: str = "professional",
                               vault_path: Optional[Path] = None) -> Dict[str, Any]:
    """Generate Instagram post content."""
    poster = InstagramPoster(vault_path)
    return poster.generate_post_content(topic, tone)


def test_instagram_connection(vault_path: Optional[Path] = None) -> Dict[str, Any]:
    """Test Instagram API connection."""
    poster = InstagramPoster(vault_path)
    return poster.test_connection()


if __name__ == "__main__":
    import sys
    import io
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    # Test Instagram Poster
    print("Testing Instagram Poster...")
    
    poster = InstagramPoster()
    
    # Test connection
    print("\n1. Testing connection...")
    result = poster.test_connection()
    print(f"Connection: {result}")
    
    # Test content generation
    print("\n2. Generating sample content...")
    content = poster.generate_post_content("AI Automation", tone="enthusiastic")
    print(f"Generated content: {content.get('content', '')[:200]}...")
    
    # Show posts log
    print(f"\n3. Posts log: {poster.get_posts_log()}")
    
    print("\n✅ Instagram Poster test complete!")
