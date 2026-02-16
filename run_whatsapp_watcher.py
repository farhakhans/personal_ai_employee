"""
Run WhatsApp Watcher - Standalone Script
Run this directly to start WhatsApp monitoring
"""

import sys
import asyncio
from pathlib import Path

# Add the Watchers directory to path
watchers_path = Path(__file__).parent / "AI_Employee_System" / "Watchers"
sys.path.insert(0, str(watchers_path))

from whatsapp_watcher import WhatsAppWatcher


async def run():
    """Run WhatsApp Watcher"""
    print("\n" + "="*70)
    print("  📱 WhatsApp Watcher - Running".center(70))
    print("="*70 + "\n")
    
    # Initialize
    vault_path = Path(__file__).parent / "vault"
    watcher = WhatsAppWatcher(vault_path=str(vault_path))
    
    print("🔹 Step 1: Launching Browser")
    print("-" * 70)
    success = await watcher.launch_browser()
    
    if not success:
        print("\n❌ Failed to launch WhatsApp")
        print("\nRun these commands first:")
        print("  pip install playwright")
        print("  playwright install chromium")
        print("  python AI_Employee_System/Watchers/WHATSAPP_SETUP.py")
        return
    
    print("\n✅ Connected to WhatsApp Web!")
    
    print("\n🔹 Step 2: Getting Recent Chats")
    print("-" * 70)
    chats = await watcher.get_recent_chats(limit=10)
    
    if chats:
        print(f"\nFound {len(chats)} recent chats:\n")
        for i, chat in enumerate(chats, 1):
            print(f"  {i}. {chat['name']}")
            if chat.get('preview'):
                preview = chat['preview'][:40] + "..." if len(chat['preview']) > 40 else chat['preview']
                print(f"     \"{preview}\"")
    else:
        print("No chats found")
    
    print("\n🔹 Step 3: Monitoring Messages")
    print("-" * 70)
    print(f"\n💾 Saving to: {vault_path}/Inbox/WHATSAPP_*.md")
    print("\n⏵  Monitoring every 5 seconds...")
    print("   Press Ctrl+C to stop\n")
    
    try:
        await watcher.monitor_messages(poll_interval=5)
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("✅ Stopped WhatsApp Watcher")
        print("="*70)
        print(f"\n📁 Check your messages: {vault_path}/Inbox/")
        print("\nNext steps:")
        print("  1. Review messages in Vault/Inbox/")
        print("  2. Move important ones to Vault/Needs_Action/")
        print("  3. Process and archive")


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Install dependencies: pip install playwright anthropic")
        print("  2. Install browser: playwright install chromium")
        print("  3. Run setup: python AI_Employee_System/Watchers/WHATSAPP_SETUP.py")
