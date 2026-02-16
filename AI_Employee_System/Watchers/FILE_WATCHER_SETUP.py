"""
FILE SYSTEM WATCHER SETUP GUIDE
═══════════════════════════════════════════════════════════════════════════

Complete setup and configuration guide for File System Watcher.
Monitor local directories and automatically process dropped files.
"""

import os
import sys


SETUP_GUIDE = """

╔═══════════════════════════════════════════════════════════════════════════╗
║                 FILE SYSTEM WATCHER - SETUP GUIDE                        ║
╚═══════════════════════════════════════════════════════════════════════════╝


📋 WHAT IS FILE SYSTEM WATCHER?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File System Watcher monitors a local directory for new files and 
automatically processes them into your AI Employee vault.

✅ Use Cases:
  • Auto-process documents from downloads folder
  • Monitor shared folders for new client files
  • Process screenshots and images automatically
  • Handle attached files from email downloads
  • Trigger workflows on file drops


⚡ QUICK INSTALL (2 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Install optional dependency (watchdog for better performance)
   $ pip install watchdog

   Note: Works without it, but uses polling instead of file events

Step 2: Start the watcher
   $ python Watchers/start_file_watcher.py

Step 3: Drop files into the watch directory
   Default location: Vault/Inbox/Drops/

Your AI Employee will:
  ✓ Detect new files automatically
  ✓ Extract metadata and content
  ✓ Create vault entries with file information
  ✓ Copy files for reference and processing
  ✓ Track processed files (no duplicates)


📁 DIRECTORY STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Vault/
├── Inbox/
│   ├── Drops/              ← Drop files here
│   ├── FILE_DROP_*.md      ← Auto-generated entries
│   └── FILE_*.pdf, .docx   ← Copied files for reference
│
├── Needs_Action/           ← AI marks for processing
├── In_Progress/            ← Currently handling
├── Plans/                  ← Generated action plans
├── Done/                   ← Completed items
├── Approved/               ← Approved items
└── Updates/                ← System updates


🎯 WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  File Dropped
   You place a file in Vault/Inbox/Drops/

2️⃣  Detection (every 5 seconds)
   Watcher detects the new file

3️⃣  Processing
   • Calculate file hash (deduplication)
   • Extract metadata and content
   • Type-specific analysis
   • Create markdown summary

4️⃣  Storage
   • Save FILE_DROP_<name>_<timestamp>.md to Vault/Inbox/
   • Copy original file to vault
   • Track processed file hash

5️⃣  AI Analysis (Optional)
   Run orchestrator to analyze and act on dropped files:
   
   $ python orchestrator.py
   
   AI Employee will:
   • Read new FILE_DROP_*.md entries
   • Analyze file content and purpose
   • Create action plans
   • Request approvals if needed


🔧 CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CUSTOM WATCH DIRECTORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Create a Python script:

    from pathlib import Path
    from Watchers.file_watcher import FileWatcher
    
    # Monitor custom directory
    watcher = FileWatcher(
        watch_dir=Path("D:/Downloads"),      # Your directory
        vault_dir=Path("./Vault")             # Your vault
    )
    watcher.run_continuous(poll_interval=5)


POLLING INTERVAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Control how often the watcher scans:

    watcher.run_continuous(poll_interval=10)  # Check every 10 seconds
    watcher.run_continuous(poll_interval=2)   # Check every 2 seconds (more CPU)
    watcher.run_continuous(poll_interval=30)  # Check every 30 seconds (less CPU)


RUN ONCE vs CONTINUOUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

One-time scan:
    count = watcher.run_once()
    print(f"Processed {count} files")

Continuous monitoring:
    watcher.run_continuous(poll_interval=5)


📊 SUPPORTED FILE TYPES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TEXT FILES          CODE FILES          DOCUMENTS
├─ .txt             ├─ .py              ├─ .pdf
├─ .md              ├─ .js              ├─ .doc
├─ .json            ├─ .ts              ├─ .docx
├─ .yaml            ├─ .java            ├─ .odt
├─ .xml             ├─ .cpp             └─ .pages
├─ .csv             ├─ .go
└─ .log             ├─ .rs              IMAGES
                    ├─ .ruby            ├─ .jpg
SPREADSHEETS        ├─ .php             ├─ .png
├─ .xlsx            ├─ .sql             ├─ .gif
├─ .xls             ├─ .html            ├─ .svg
├─ .ods             └─ .css             ├─ .webp
└─ .numbers                             └─ .ico

ARCHIVES            OTHER
├─ .zip             └─ Any file
├─ .rar              (saves with size info)
├─ .7z
├─ .tar
└─ .gz


📦 ENHANCED PROCESSING (via optional packages)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Image Metadata (dimensions, format):
   $ pip install Pillow
   
   Extracts: size, format, dimensions

PDF Page Count:
   $ pip install PyPDF2
   
   Extracts: page count

Code Analysis:
   $ pip install ast-comments
   
   Can analyze code structure, functions, classes


🔐 SECURITY & BEST PRACTICES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ DO's:
   • Use dedicated directories for file drops
   • Monitor only trusted source folders
   • Review auto-processed files in Vault/Inbox/
   • Set up approval workflows for sensitive files
   • Regularly archive processed files

❌ DON'Ts:
   • Don't point watcher at system directories
   • Don't disable deduplication
   • Don't process files from untrusted sources without review
   • Don't use very fast polling (< 2 seconds) for large directories
   • Don't mix file drops with manual files


⚠️  TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Files not detected?
   • Check watch directory exists: Vault/Inbox/Drops/
   • Ensure files are fully written before scan
   • Try smaller polling interval: watcher.run_continuous(poll_interval=2)

2. "watchdog not installed" warning?
   • Install it: pip install watchdog
   • System works without it (slower, uses polling)

3. Permission denied errors?
   • Check folder permissions
   • Run with appropriate user privileges
   • Vault directory must be writable

4. Duplicate processing?
   • File hashes cached in .processed_files.json
   • Clear cache: rm Vault/Inbox/Drops/.processed_files.json
   • Will re-process deleted files

5. Image dimensions showing 0x0?
   • Install Pillow: pip install Pillow
   • Formats not recognized need manual processing

6. Large files slow down watcher?
   • Increase polling interval: poll_interval=30
   • Process in smaller batches
   • Use dedicated high-performance directory


🔗 INTEGRATION WITH ORCHESTRATOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Once files are dropped and processed:

1. Run orchestrator to analyze:
   $ python orchestrator.py

2. Orchestrator will:
   • Read FILE_DROP_*.md entries
   • Analyze content with Claude
   • Decide on action (route, store, process)
   • Create action plans

3. Monitor processing:
   • Check Vault/Needs_Action/ for pending items
   • Review Vault/In_Progress/ for current work
   • Archive completed in Vault/Done/


📚 ADVANCED USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MULTIPLE WATCHERS
━━━━━━━━━━━━━━━━━━

Monitor multiple directories:

    from concurrent.futures import ThreadPoolExecutor
    from Watchers.file_watcher import FileWatcher
    
    # Create watchers for different sources
    documents_watcher = FileWatcher(
        Path("D:/Documents/Drops"),
        Path("./Vault")
    )
    
    downloads_watcher = FileWatcher(
        Path("D:/Downloads/Inbox"),
        Path("./Vault")
    )
    
    # Run in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(documents_watcher.run_continuous, 5)
        executor.submit(downloads_watcher.run_continuous, 5)


CUSTOM FILE PROCESSORS
━━━━━━━━━━━━━━━━━━━━━━━━━

Extend FileWatcher with custom logic:

    class CustomFilesWatcher(FileWatcher):
        def _process_image(self, file_path):
            # Custom image processing
            metadata = super()._process_image(file_path)
            # Add custom AI vision analysis
            return metadata


AUTO-CLEANUP
━━━━━━━━━━━━

Automatically move processed files:

    watcher = FileWatcher(watch_dir, vault_dir)
    for file_path in watch_dir.iterdir():
        if watcher._process_file(file_path):
            file_path.unlink()  # Delete after processing


TIME-LIMITED MONITORING
━━━━━━━━━━━━━━━━━━━━━━━━

Run watcher for specific duration:

    # Monitor for 1 hour
    watcher.run_continuous(
        poll_interval=5,
        max_duration=3600  # seconds
    )


🎓 EXAMPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXAMPLE 1: Monitor Downloads folder
──────────────────────────────────

    from pathlib import Path
    from Watchers.file_watcher import FileWatcher
    
    downloads = Path.home() / "Downloads" / "Inbox"
    watcher = FileWatcher(downloads, Path("./Vault"))
    watcher.run_continuous()  # Monitor until Ctrl+C


EXAMPLE 2: Process specific file types
──────────────────────────────────────

    watcher = FileWatcher(watch_dir, vault_dir)
    
    # Only process PDF files
    for file in watch_dir.glob("*.pdf"):
        watcher._process_file(file)


EXAMPLE 3: Integrate with task scheduler
─────────────────────────────────────────

    import schedule
    from Watchers.file_watcher import FileWatcher
    
    watcher = FileWatcher(watch_dir, vault_dir)
    
    # Scan 4 times per day
    schedule.every(6).hours.do(watcher.run_once)
    
    while True:
        schedule.run_pending()
        time.sleep(1)


EXAMPLE 4: Email attachments processing
───────────────────────────────────────

Download email attachments and process:

    from gmail_watcher import GmailWatcher
    from file_watcher import FileWatcher
    
    # Download attachments
    gmail = GmailWatcher()
    attachment_dir = Path("./temp_attachments")
    # ... save attachments to attachment_dir
    
    # Process them
    file_watcher = FileWatcher(attachment_dir, Path("./Vault"))
    file_watcher.run_once()


📞 SUPPORT & HELP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Check logs in:
  • Terminal output (for current session)
  • Vault/Inbox/Drops/.processed_files.json (processed file tracking)

Common commands:
  $ python Watchers/start_file_watcher.py    # Start watcher
  $ ls Vault/Inbox/FILE_DROP_*.md            # View processed entries
  $ rm Vault/Inbox/Drops/.processed_files.json # Reset tracking


🎉 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Start file watcher:
   $ python Watchers/start_file_watcher.py

2. Drop test files into Vault/Inbox/Drops/

3. Watch them get processed in real-time

4. Run orchestrator to analyze dropped files:
   $ python orchestrator.py

5. Watch AI Employee take action!


═══════════════════════════════════════════════════════════════════════════
File System Watcher Ready! Start monitoring: python Watchers/start_file_watcher.py
═══════════════════════════════════════════════════════════════════════════
"""


def main():
    """Display setup guide."""
    print(SETUP_GUIDE)
    
    # Offer to start watcher
    print("\n" + "="*79)
    response = input("\n▶️  Start file watcher now? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        print("\n🚀 Launching File System Watcher...\n")
        os.system("python Watchers/start_file_watcher.py")
    else:
        print("\n✅ Setup guide displayed.")
        print("\nTo start later, run:")
        print("  python Watchers/start_file_watcher.py")
        print("\nFor more help:")
        print("  python Watchers/FILE_WATCHER_SETUP.py")


if __name__ == "__main__":
    main()
