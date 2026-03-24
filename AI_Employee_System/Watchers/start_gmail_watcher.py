"""
Quick Launcher: Gmail Watcher
Run Gmail Watcher with one command
Sends email notifications when new emails arrive
"""

import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from gmail_watcher import GmailWatcher


def print_header():
    """Print beautiful header"""
    print("\n" + "="*70)
    print("  Gmail Watcher - Launcher".center(70))
    print("="*70 + "\n")


def main():
    """Main launcher"""
    print_header()

    # Check for credentials
    email_addr = os.getenv('GMAIL_ADDRESS')
    app_password = os.getenv('GMAIL_APP_PASSWORD')
    notification_email = os.getenv('NOTIFICATION_EMAIL')  # Optional

    if not email_addr or not app_password:
        print("[WARN] Gmail credentials not found!")
        print("\nSetup Instructions:")
        print("1. Create .env file in project root")
        print("2. Add your Gmail credentials:")
        print("   GMAIL_ADDRESS=your.email@gmail.com")
        print("   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx")
        print("   NOTIFICATION_EMAIL=your.email@gmail.com (optional)")
        print("\nGet App Password:")
        print("1. Go to: https://myaccount.google.com/")
        print("2. Security -> 2-Step Verification -> App passwords")
        print("3. Generate new app password for 'Mail'")
        print("4. Copy to .env file")
        return

    print("[OK] Gmail credentials found")
    print(f"  Email: {email_addr}")
    print(f"  Notification Email: {notification_email or email_addr}")
    print(f"  Poll Interval: 300 seconds (5 minutes)")
    
    # Check for demo mode
    if app_password.lower() in ['demo', 'test', 'demo_password']:
        print("\n⚠️  DEMO MODE - Running without real Gmail connection")
        print("   To receive real emails, set up Gmail App Password")
        print("   Guide: https://myaccount.google.com/security")

    # Initialize watcher
    vault_path = Path(__file__).parent.parent / "vault"
    watcher = GmailWatcher(
        email_addr=email_addr,
        app_password=app_password,
        vault_path=str(vault_path),
        poll_interval=300,
        notification_email=notification_email
    )

    # Start monitoring
    print("\nStarting Gmail Watcher...")
    print("-" * 70)
    print(f"[OK] Connected to vault: {vault_path}")
    print(f"\nEmails will save to:")
    print(f"  -> {vault_path}/Inbox/EMAIL_*.md\n")
    print("Email notifications will be sent to:")
    print(f"  -> {notification_email or email_addr}\n")
    print("Watching for new emails every 5 minutes...")
    print("Press Ctrl+C to stop\n")
    print("-" * 70)

    try:
        watcher.run_continuous()
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("[OK] Gmail Watcher stopped")
        print("=" * 70)
        print(f"\nEmails saved to: {vault_path}/Inbox/")
        print(f"Notifications sent to: {notification_email or email_addr}")
        print("\nWhat to do next:")
        print("1. Check emails in Vault/Inbox/")
        print("2. Check your Gmail for notifications")
        print("3. Move important ones to Vault/Needs_Action/")
        print("4. Archive processed emails to Vault/Approved/")
        print("\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        print("\nRun setup guide:")
        print("  1. Create .env file")
        print("  2. Add GMAIL_ADDRESS and GMAIL_APP_PASSWORD")
        print("  3. (Optional) Add NOTIFICATION_EMAIL for alerts")
