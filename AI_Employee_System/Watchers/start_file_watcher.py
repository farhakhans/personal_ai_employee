"""
START FILE WATCHER - Quick Launcher
═══════════════════════════════════════════════════════════════════════════

One-command launcher for file system watcher.
Monitors a directory for dropped files and processes them into the vault.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Watchers.file_watcher import FileWatcher


def print_banner():
    """Print fancy banner."""
    print("\n" + "🟢" * 40)
    print("🟢" + " " * 38 + "🟢")
    print("🟢" + "  FILE SYSTEM WATCHER - STARTING...".center(38) + "🟢")
    print("🟢" + " " * 38 + "🟢")
    print("🟢" * 40 + "\n")


def print_status(watch_dir, vault_dir, inbox_dir):
    """Print status information."""
    print(f"📁 Watching Directory: {watch_dir}")
    print(f"💾 Vault Location:     {vault_dir}")
    print(f"📥 Inbox Folder:       {inbox_dir}")
    print(f"⏱️  Polling Interval:   5 seconds")
    print(f"🕐 Started:             {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "-" * 70 + "\n")


def print_instructions():
    """Print usage instructions."""
    print("📋 HOW IT WORKS:")
    print("  1. Drop files into the watch directory")
    print("  2. Watcher detects changes automatically")
    print("  3. Creates markdown entry in Vault/Inbox/")
    print("  4. Copies original file to vault for reference")
    print("\n")
    print("✅ SUPPORTED FILE TYPES:")
    print("  • Text:       .txt, .md, .json, .yaml, .csv, .log")
    print("  • Code:       .py, .js, .ts, .java, .go, .cpp, .sql, .html")
    print("  • Documents:  .pdf, .doc, .docx, .odt")
    print("  • Images:     .jpg, .png, .gif, .svg, .webp")
    print("  • Sheets:     .xlsx, .xls, .csv, .numbers")
    print("  • Archives:   .zip, .rar, .7z, .tar, .gz")
    print("\n")
    print("⚙️  FEATURES:")
    print("  ✓ Automatic deduplication (tracks file hashes)")
    print("  ✓ File metadata extraction")
    print("  ✓ Type-specific processing")
    print("  ✓ Real-time monitoring")
    print("  ✓ Integration with AI orchestrator")
    print("\n")


def run_file_watcher():
    """Run the file watcher."""
    
    # Determine paths
    current_dir = Path(__file__).parent.parent
    watch_dir = current_dir / "Vault" / "Inbox" / "Drops"
    vault_dir = current_dir / "Vault"
    
    # Create drop directory if needed
    watch_dir.mkdir(parents=True, exist_ok=True)
    
    print_banner()
    print_instructions()
    print_status(watch_dir, vault_dir, watch_dir.parent)
    
    print("🔍 File Watcher is running...\n")
    print("Press Ctrl+C to stop monitoring\n")
    print("=" * 70 + "\n")
    
    try:
        # Create and run watcher
        watcher = FileWatcher(watch_dir, vault_dir)
        
        # Show initial scan
        print("📊 Initial scan...\n")
        count = watcher.run_once()
        if count > 0:
            print(f"✅ Found {count} new file(s)\n")
        else:
            print("No new files found. Waiting for drops...\n")
        
        print("=" * 70 + "\n")
        
        # Run continuous monitoring
        watcher.run_continuous(poll_interval=5)
        
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("⏹️  File Watcher Stopped\n")
        print_summary(watcher)
        print("\nThank you for using File Watcher! 👋")
        print("=" * 70 + "\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def print_summary(watcher):
    """Print final summary."""
    processed_count = len(watcher.processed_hashes)
    print(f"📊 Files Processed: {processed_count}")
    print(f"📁 Vault Inbox: {watcher.inbox_dir}")
    print("\nAll processed files saved to Vault/Inbox/")
    print("Use orchestrator to analyze and act on dropped files.")


if __name__ == "__main__":
    run_file_watcher()
