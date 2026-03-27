"""
LinkedIn CLI Poster
Post to LinkedIn directly from command line

Usage:
    python post_linkedin_cli.py "Your post message here"
    python post_linkedin_cli.py --file post.txt
    python post_linkedin_cli.py --test
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from AI_Employee_System.Watchers.linkedin_poster import LinkedInPoster


def print_banner():
    """Print welcome banner"""
    print("=" * 70)
    print("  💼 LINKEDIN CLI POSTER - AI Employee System")
    print("=" * 70)
    print()


def check_credentials():
    """Check if LinkedIn credentials are configured"""
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    person_urn = os.getenv("LINKEDIN_PERSON_URN")
    
    if not access_token:
        print("❌ Error: LINKEDIN_ACCESS_TOKEN not configured in .env file")
        print("\n📝 Setup Instructions:")
        print("1. Run: python get_linkedin_token.py")
        print("2. Or manually add to .env file:")
        print("   LINKEDIN_ACCESS_TOKEN=your-token-here")
        print("   LINKEDIN_PERSON_URN=urn:li:person:YOUR_ID")
        return False
    
    if not person_urn:
        print("⚠️  Warning: LINKEDIN_PERSON_URN not configured")
        print("   Will try to fetch from API...")
    
    return True


def test_connection():
    """Test LinkedIn API connection"""
    print("🔗 Testing LinkedIn API connection...")
    
    try:
        poster = LinkedInPoster(user_tier='silver')
        result = poster.test_connection()
        
        if result.get('success'):
            print(f"✅ Connected successfully!")
            print(f"   User: {result.get('user_name', 'Unknown')}")
            print(f"   ID: {result.get('user_id', 'Unknown')}")
            return True
        else:
            print(f"❌ Connection failed: {result.get('error', 'Unknown error')}")
            if result.get('details'):
                print(f"   Details: {result.get('details')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def post_message(message, title=""):
    """Post a message to LinkedIn"""
    print(f"📝 Posting to LinkedIn...")
    print(f"   Title: {title if title else 'No title'}")
    print(f"   Message length: {len(message)} characters")
    print()
    
    try:
        poster = LinkedInPoster(user_tier='silver')
        result = poster.post_to_profile(message, title)
        
        if result.get('success'):
            print("✅ Post published successfully!")
            print(f"   Post ID: {result.get('post_id')}")
            print(f"   URL: {result.get('post_url')}")
            
            # Save to vault
            print(f"   Saved to vault: Yes")
            return True
        else:
            print(f"❌ Post failed: {result.get('error', 'Unknown error')}")
            if result.get('details'):
                print(f"   Details: {result.get('details')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def post_with_image(message, image_url, title=""):
    """Post a message with image to LinkedIn"""
    print(f"📝 Posting to LinkedIn with image...")
    print(f"   Image URL: {image_url}")
    print(f"   Message length: {len(message)} characters")
    print()
    
    try:
        poster = LinkedInPoster(user_tier='silver')
        result = poster.post_with_image(message, image_url)
        
        if result.get('success'):
            print("✅ Post with image published successfully!")
            print(f"   Post ID: {result.get('post_id')}")
            return True
        else:
            print(f"❌ Post failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def get_recent_posts(count=5):
    """Get recent posts from LinkedIn"""
    print(f"📊 Fetching recent posts...")
    
    try:
        poster = LinkedInPoster(user_tier='silver')
        result = poster.get_my_posts(count)
        
        if result.get('success'):
            posts = result.get('posts', [])
            print(f"✅ Found {len(posts)} posts")
            print()
            
            for i, post in enumerate(posts, 1):
                print(f"--- Post {i} ---")
                print(f"ID: {post.get('id')}")
                print(f"Text: {post.get('text', {}).get('text', '')[:200]}...")
                print(f"Created: {post.get('created')}")
                print()
            
            return True
        else:
            print(f"❌ Failed to fetch posts: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def get_notifications(count=10):
    """Get recent notifications from LinkedIn"""
    print(f"🔔 Fetching notifications...")
    
    try:
        poster = LinkedInPoster(user_tier='silver')
        result = poster.get_notifications(count)
        
        if result.get('success'):
            notifications = result.get('notifications', [])
            print(f"✅ Found {len(notifications)} notifications")
            print()
            
            for i, notif in enumerate(notifications[:5], 1):
                print(f"{i}. Type: {notif.get('type')}")
                print(f"   Activity: {notif.get('activity')}")
                print(f"   Time: {notif.get('created_at')}")
                print()
            
            if len(notifications) > 5:
                print(f"... and {len(notifications) - 5} more")
            
            return True
        else:
            print(f"❌ Failed to fetch notifications: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Post to LinkedIn from command line',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python post_linkedin_cli.py "Hello LinkedIn!"
  python post_linkedin_cli.py --file post.txt
  python post_linkedin_cli.py --test
  python post_linkedin_cli.py --posts
  python post_linkedin_cli.py --notifications
  python post_linkedin_cli.py --image "Check this out!" https://example.com/image.jpg
        """
    )
    
    parser.add_argument('message', nargs='?', help='Post message text')
    parser.add_argument('--file', '-f', help='Read message from file')
    parser.add_argument('--title', '-t', default='', help='Post title (optional)')
    parser.add_argument('--test', action='store_true', help='Test LinkedIn connection')
    parser.add_argument('--posts', action='store_true', help='Show recent posts')
    parser.add_argument('--notifications', action='store_true', help='Show recent notifications')
    parser.add_argument('--image', '-i', nargs=2, metavar=('MESSAGE', 'URL'), help='Post with image')
    parser.add_argument('--count', '-c', type=int, default=5, help='Number of posts/notifications to fetch')
    
    args = parser.parse_args()
    
    print_banner()
    
    # Check credentials
    if not check_credentials():
        sys.exit(1)
    
    # Test connection
    if args.test:
        success = test_connection()
        sys.exit(0 if success else 1)
    
    # Show recent posts
    if args.posts:
        success = get_recent_posts(args.count)
        sys.exit(0 if success else 1)
    
    # Show notifications
    if args.notifications:
        success = get_notifications(args.count)
        sys.exit(0 if success else 1)
    
    # Post with image
    if args.image:
        message, image_url = args.image
        success = post_with_image(message, image_url, args.title)
        sys.exit(0 if success else 1)
    
    # Get message from file
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ Error: File not found: {args.file}")
            sys.exit(1)
        
        message = file_path.read_text(encoding='utf-8').strip()
        print(f"📄 Read message from file: {args.file}")
    
    # Get message from argument
    elif args.message:
        message = args.message
    
    # No message provided
    else:
        print("❌ Error: No message provided")
        print("\nUsage:")
        print("  python post_linkedin_cli.py \"Your message here\"")
        print("  python post_linkedin_cli.py --file post.txt")
        print("\nRun 'python post_linkedin_cli.py --help' for more options")
        sys.exit(1)
    
    # Post to LinkedIn
    success = post_message(message, args.title)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
