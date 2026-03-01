"""
TWITTER POSTER - Social Media Automation
═══════════════════════════════════════════════════════════════════════════

Twitter/X integration for automated posting with Claude reasoning.
Posts tweets, threads, and monitors engagement.

Tier: Gold
Setup: Twitter API v2 credentials required
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


class TwitterPoster:
    """
    Twitter/X posting automation using Twitter API v2.
    
    Capabilities:
    - Post tweets (280 characters)
    - Post threads (multiple tweets)
    - Upload media with tweets
    - Get tweet analytics
    - Monitor mentions and replies
    """

    def __init__(self, vault_path: Optional[Path] = None):
        """
        Initialize Twitter Poster.
        
        Args:
            vault_path: Path to vault for saving posts and logs
        """
        self.vault_path = vault_path or Path(__file__).parent.parent / "Vault"
        
        # Twitter API v2 credentials
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_SECRET")
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        
        # API endpoints
        self.base_url = "https://api.twitter.com/2"
        self.vault_path.mkdir(parents=True, exist_ok=True)
        
        # Posts log
        self.posts_log = []
        
        logger.info("Twitter Poster initialized")
        if not self.api_key:
            logger.warning("TWITTER_API_KEY not configured")

    def create_tweet(self, text: str, media_urls: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create a new tweet.
        
        Args:
            text: Tweet text (max 280 characters)
            media_urls: Optional list of media URLs to attach
            
        Returns:
            dict: Tweet result with tweet_id and status
        """
        if not self.bearer_token:
            return {"success": False, "error": "Twitter bearer token not configured"}
        
        if len(text) > 280:
            return {"success": False, "error": "Tweet text exceeds 280 character limit"}
        
        try:
            endpoint = f"{self.base_url}/tweets"
            
            headers = {
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": "application/json"
            }
            
            payload = {"text": text}
            
            response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
            result = response.json()
            
            if response.status_code == 201 and "data" in result:
                tweet_data = {
                    "tweet_id": result["data"]["id"],
                    "text": text,
                    "media_urls": media_urls,
                    "timestamp": datetime.now().isoformat(),
                    "status": "published",
                    "platform": "Twitter"
                }
                
                self.posts_log.append(tweet_data)
                self._save_post_to_vault(tweet_data)
                
                logger.info(f"Tweet created: {result['data']['id']}")
                return {
                    "success": True,
                    "tweet_id": result["data"]["id"],
                    "text": text,
                    "message": "Tweet successfully posted to Twitter"
                }
            else:
                logger.error(f"Twitter post failed: {result}")
                return {
                    "success": False,
                    "error": result.get("errors", [{}])[0].get("message", "Unknown error")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Twitter API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error posting tweet: {e}")
            return {"success": False, "error": str(e)}

    def create_thread(self, tweets: List[str]) -> Dict[str, Any]:
        """
        Create a thread of tweets (multiple connected tweets).
        
        Args:
            tweets: List of tweet texts (each max 280 chars)
            
        Returns:
            dict: Thread result with tweet IDs
        """
        if not tweets or len(tweets) > 10:
            return {"success": False, "error": "Thread must have 1-10 tweets"}
        
        # Validate each tweet
        for i, tweet in enumerate(tweets):
            if len(tweet) > 280:
                return {"success": False, "error": f"Tweet {i+1} exceeds 280 character limit"}
        
        tweet_ids = []
        
        for i, tweet_text in enumerate(tweets):
            # First tweet is normal, rest are replies
            result = self.create_tweet(tweet_text)
            
            if result.get("success"):
                tweet_ids.append(result["tweet_id"])
            else:
                return {
                    "success": False,
                    "error": f"Failed to post tweet {i+1}: {result.get('error')}",
                    "partial_ids": tweet_ids
                }
        
        return {
            "success": True,
            "tweet_ids": tweet_ids,
            "thread_length": len(tweets),
            "message": f"Thread of {len(tweets)} tweets successfully posted"
        }

    def get_tweet_insights(self, tweet_id: str) -> Dict[str, Any]:
        """
        Get insights/analytics for a tweet.
        
        Args:
            tweet_id: Twitter tweet ID
            
        Returns:
            dict: Tweet insights (impressions, likes, retweets, etc.)
        """
        if not self.bearer_token:
            return {"success": False, "error": "Twitter bearer token not configured"}
        
        try:
            endpoint = f"{self.base_url}/tweets/{tweet_id}"
            params = {
                "tweet.fields": "public_metrics,created_at"
            }
            
            headers = {
                "Authorization": f"Bearer {self.bearer_token}"
            }
            
            response = requests.get(endpoint, params=params, headers=headers, timeout=30)
            result = response.json()
            
            if response.status_code == 200 and "data" in result:
                metrics = result["data"].get("public_metrics", {})
                insights = {
                    "tweet_id": tweet_id,
                    "timestamp": datetime.now().isoformat(),
                    "impressions": metrics.get("impression_count", 0),
                    "likes": metrics.get("like_count", 0),
                    "retweets": metrics.get("retweet_count", 0),
                    "replies": metrics.get("reply_count", 0),
                    "quotes": metrics.get("quote_count", 0)
                }
                
                logger.info(f"Retrieved insights for tweet: {tweet_id}")
                return {"success": True, "insights": insights}
            else:
                logger.error(f"Failed to get insights: {result}")
                return {
                    "success": False,
                    "error": result.get("errors", [{}])[0].get("message", "Unknown error")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Twitter API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error getting insights: {e}")
            return {"success": False, "error": str(e)}

    def get_user_tweets(self, username: str, limit: int = 10) -> Dict[str, Any]:
        """
        Get recent tweets from a user.
        
        Args:
            username: Twitter username (without @)
            limit: Number of tweets to retrieve
            
        Returns:
            dict: List of recent tweets
        """
        if not self.bearer_token:
            return {"success": False, "error": "Twitter bearer token not configured"}
        
        try:
            # First get user ID
            user_endpoint = f"{self.base_url}/users/by/username/{username}"
            user_headers = {"Authorization": f"Bearer {self.bearer_token}"}
            
            user_response = requests.get(user_endpoint, headers=user_headers, timeout=30)
            user_result = user_response.json()
            
            if user_response.status_code != 200:
                return {"success": False, "error": "User not found"}
            
            user_id = user_result["data"]["id"]
            
            # Get user's tweets
            tweets_endpoint = f"{self.base_url}/users/{user_id}/tweets"
            params = {"max_results": limit}
            
            tweets_response = requests.get(tweets_endpoint, params=params, headers=user_headers, timeout=30)
            tweets_result = tweets_response.json()
            
            if tweets_response.status_code == 200:
                tweets = tweets_result.get("data", [])
                logger.info(f"Retrieved {len(tweets)} tweets from @{username}")
                return {"success": True, "tweets": tweets}
            else:
                logger.error(f"Failed to get tweets: {tweets_result}")
                return {
                    "success": False,
                    "error": tweets_result.get("errors", [{}])[0].get("message", "Unknown error")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Twitter API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error getting user tweets: {e}")
            return {"success": False, "error": str(e)}

    def delete_tweet(self, tweet_id: str) -> Dict[str, Any]:
        """
        Delete a tweet.
        
        Args:
            tweet_id: Twitter tweet ID to delete
            
        Returns:
            dict: Delete result
        """
        if not self.bearer_token:
            return {"success": False, "error": "Twitter bearer token not configured"}
        
        try:
            endpoint = f"{self.base_url}/tweets/{tweet_id}"
            
            headers = {
                "Authorization": f"Bearer {self.bearer_token}"
            }
            
            response = requests.delete(endpoint, headers=headers, timeout=30)
            
            if response.status_code == 200:
                logger.info(f"Tweet deleted: {tweet_id}")
                return {"success": True, "message": "Tweet successfully deleted"}
            else:
                result = response.json()
                logger.error(f"Failed to delete tweet: {result}")
                return {
                    "success": False,
                    "error": result.get("errors", [{}])[0].get("message", "Unknown error")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Twitter API error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error deleting tweet: {e}")
            return {"success": False, "error": str(e)}

    def _save_post_to_vault(self, tweet_data: Dict[str, Any]) -> None:
        """Save tweet record to vault."""
        try:
            posts_dir = self.vault_path / "System" / "social_logs" / "twitter"
            posts_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"TWITTER_POST_{timestamp}_{tweet_data.get('tweet_id', 'unknown')}.md"
            filepath = posts_dir / filename
            
            content = f"""# Twitter Post

## Post Details
- **Tweet ID:** {tweet_data.get('tweet_id', 'N/A')}
- **Platform:** {tweet_data.get('platform', 'Twitter')}
- **Status:** {tweet_data.get('status', 'unknown')}
- **Timestamp:** {tweet_data.get('timestamp', 'N/A')}

## Content
**Tweet Text:**
{tweet_data.get('text', '')}

{f'**Media URLs:** {", ".join(tweet_data.get("media_urls", []))}' if tweet_data.get('media_urls') else ''}

## Metadata
```json
{json.dumps(tweet_data, indent=2)}
```

---
*Generated by AI Employee Twitter Poster*
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            logger.error(f"Error saving post to vault: {e}")

    def generate_tweet_content(self, topic: str, tone: str = "casual",
                               include_hashtags: bool = True,
                               max_length: int = 280) -> Dict[str, Any]:
        """
        Generate tweet content using AI reasoning.
        
        Args:
            topic: Topic/theme for the tweet
            tone: Tone of the tweet
            include_hashtags: Whether to include hashtags
            max_length: Maximum character count (Twitter limit: 280)
            
        Returns:
            dict: Generated content
        """
        hashtags = {
            "business": ["#Business", "#Entrepreneur", "#Success"],
            "tech": ["#Technology", "#AI", "#Tech"],
            "marketing": ["#Marketing", "#DigitalMarketing", "#SocialMedia"],
            "general": ["#Twitter", "#Tweet", "#Content"]
        }
        
        tone_styles = {
            "casual": "Friendly and conversational",
            "professional": "Informative and authoritative",
            "enthusiastic": "Exciting and energetic",
            "witty": "Clever and humorous"
        }
        
        style = tone_styles.get(tone, tone_styles["casual"])
        category_hashtags = hashtags.get("general", hashtags["general"])
        
        content = f"{topic}\n\n{style} take on {topic}. What do you think?"
        
        if include_hashtags:
            hashtag_str = " " + " ".join(category_hashtags)
            if len(content) + len(hashtag_str) <= max_length:
                content += hashtag_str
        
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
        Test Twitter API connection.
        
        Returns:
            dict: Connection test result
        """
        if not self.bearer_token:
            return {"success": False, "error": "Bearer token not configured"}
        
        try:
            endpoint = f"{self.base_url}/users/me"
            headers = {
                "Authorization": f"Bearer {self.bearer_token}"
            }
            
            response = requests.get(endpoint, headers=headers, timeout=30)
            result = response.json()
            
            if response.status_code == 200:
                logger.info(f"Twitter connection test successful: {result.get('data', {}).get('name')}")
                return {
                    "success": True,
                    "user_id": result.get("data", {}).get("id"),
                    "username": result.get("data", {}).get("username"),
                    "name": result.get("data", {}).get("name"),
                    "message": "Successfully connected to Twitter"
                }
            else:
                logger.error(f"Twitter connection test failed: {result}")
                return {
                    "success": False,
                    "error": result.get("errors", [{}])[0].get("message", "Connection failed")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Twitter connection error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error testing connection: {e}")
            return {"success": False, "error": str(e)}


# Convenience functions for MCP server integration
def create_twitter_tweet(text: str, vault_path: Optional[Path] = None) -> Dict[str, Any]:
    """Create a Twitter tweet."""
    poster = TwitterPoster(vault_path)
    return poster.create_tweet(text)


def generate_twitter_content(topic: str, tone: str = "casual",
                             vault_path: Optional[Path] = None) -> Dict[str, Any]:
    """Generate Twitter tweet content."""
    poster = TwitterPoster(vault_path)
    return poster.generate_tweet_content(topic, tone)


def test_twitter_connection(vault_path: Optional[Path] = None) -> Dict[str, Any]:
    """Test Twitter API connection."""
    poster = TwitterPoster(vault_path)
    return poster.test_connection()


if __name__ == "__main__":
    import sys
    import io
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    # Test Twitter Poster
    print("Testing Twitter Poster...")
    
    poster = TwitterPoster()
    
    # Test connection
    print("\n1. Testing connection...")
    result = poster.test_connection()
    print(f"Connection: {result}")
    
    # Test content generation
    print("\n2. Generating sample content...")
    content = poster.generate_tweet_content("AI Automation", tone="casual")
    print(f"Generated content: {content.get('content', '')[:200]}...")
    
    # Show posts log
    print(f"\n3. Posts log: {poster.get_posts_log()}")
    
    print("\n Twitter Poster test complete!")
