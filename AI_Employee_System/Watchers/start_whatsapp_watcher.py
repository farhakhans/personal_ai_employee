"""
Quick Launcher: WhatsApp Watcher
Run WhatsApp Watcher with one command
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from whatsapp_watcher import WhatsAppWatcher


def print_header():
    """Print beautiful header"""
    print("\n" + "="*70)
    print("  WhatsApp Watcher - Launcher".center(70))
    print("="*70 + "\n")


async def main():
    """Main launcher"""
    print_header()

    print("[INFO] Starting WhatsApp Watcher...\n")

    # Initialize watcher
    vault_path = Path(__file__).parent.parent / "vault"
    watcher = WhatsAppWatcher(vault_path=str(vault_path))

    # Step 1: Launch browser
    print("Step 1: Launching browser...")
    print("-" * 70)
    success = await watcher.launch_browser()

    if not success:
        print("\n[ERROR] Failed to connect to WhatsApp")
        print("\nTroubleshooting:")
        print("1. Is Playwright installed? -> pip install playwright")
        print("2. Is Chromium installed? -> playwright install chromium")
        print("3. Did you scan the QR code? -> Open https://web.whatsapp.com")
        return

    # Step 2: Show recent chats
    print("\n\nStep 2: Recent Chats")
    print("-" * 70)
    chats = await watcher.get_recent_chats(limit=5)

    if chats:
        for chat in chats:
            print(f"{chat['index']}. {chat['name']}")
            if chat['preview']:
                print(f"   '{chat['preview'][:50]}...'")
    else:
        print("No chats found. Start a conversation on WhatsApp!")

    # Step 3: Start monitoring
    print("\n\nStep 3: Monitoring Messages")
    print("-" * 70)
    print(f"[OK] Connected to vault: {vault_path}")
    print("\nMessages will save to:")
    print(f"  -> {vault_path}/Inbox/WHATSAPP_*.md\n")
    print("Watching for new messages every 5 seconds...")
    print("Press Ctrl+C to stop\n")
    print("-" * 70)

    try:
        await watcher.monitor_messages(poll_interval=5)
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("[OK] WhatsApp Watcher stopped")
        print("=" * 70)
        print(f"\nMessages saved to: {vault_path}/Inbox/")
        print("\nWhat to do next:")
        print("1. Check messages in Vault/Inbox/")
        print("2. Move important ones to Vault/Needs_Action/")
        print("3. Archive processed messages to Vault/Approved/")
        print("4. Add automation rules in orchestrator.py")
        print("\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        print("\nRun setup guide:")
        print("  python WHATSAPP_SETUP.py")
