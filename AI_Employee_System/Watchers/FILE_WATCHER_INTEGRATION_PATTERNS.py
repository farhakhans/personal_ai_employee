"""
FILE WATCHER INTEGRATION GUIDE
═══════════════════════════════════════════════════════════════════════════

Examples and patterns for integrating File System Watcher with the 
AI Employee orchestrator for complete automation.
"""


# PATTERN 1: Direct integration with orchestrator
# ═══════════════════════════════════════════════════════════════════════════
"""
Process file drops using the main orchestrator
"""

PATTERN_1 = """
from pathlib import Path
from Watchers.file_watcher import FileWatcher
from orchestrator import AIEmployeeOrchestrator

# Step 1: Create file watcher
watcher = FileWatcher(
    watch_dir=Path("./Vault/Inbox/Drops"),
    vault_dir=Path("./Vault")
)

# Step 2: Create orchestrator
orchestrator = AIEmployeeOrchestrator(vault_dir=Path("./Vault"))

# Step 3: Process files in a loop
while True:
    # Scan for new files
    count = watcher.run_once()
    
    if count > 0:
        print(f"✅ Processed {count} new files")
        
        # Let orchestrator analyze the new FILE_DROP_*.md entries
        orchestrator.process_inbox()
        
        # AI will decide what to do with each file
    
    # Wait before next scan
    time.sleep(30)
"""


# PATTERN 2: Scheduled file processing
# ═══════════════════════════════════════════════════════════════════════════
"""
Run file watcher on a schedule (e.g., every 1 hour)
"""

PATTERN_2 = """
import schedule
import time
from pathlib import Path
from Watchers.file_watcher import FileWatcher

watcher = FileWatcher(
    watch_dir=Path("./Vault/Inbox/Drops"),
    vault_dir=Path("./Vault")
)

# Check for dropped files every hour
schedule.every(1).hours.do(watcher.run_once)

# Check every 5 minutes during business hours
schedule.every(5).minutes.do(watcher.run_once, job_name="business_hours")

while True:
    schedule.run_pending()
    time.sleep(1)
"""


# PATTERN 3: Multiple watchers for different file types
# ═══════════════════════════════════════════════════════════════════════════
"""
Monitor separate folders for different types of files
"""

PATTERN_3 = """
from pathlib import Path
from Watchers.file_watcher import FileWatcher
from concurrent.futures import ThreadPoolExecutor

# Create separate watchers
documents_watcher = FileWatcher(
    watch_dir=Path("./Vault/Inbox/Drops/Documents"),
    vault_dir=Path("./Vault")
)

images_watcher = FileWatcher(
    watch_dir=Path("./Vault/Inbox/Drops/Images"),
    vault_dir=Path("./Vault")
)

spreadsheets_watcher = FileWatcher(
    watch_dir=Path("./Vault/Inbox/Drops/Data"),
    vault_dir=Path("./Vault")
)

# Run all in parallel
with ThreadPoolExecutor(max_workers=3) as executor:
    executor.submit(documents_watcher.run_continuous, poll_interval=5)
    executor.submit(images_watcher.run_continuous, poll_interval=5)
    executor.submit(spreadsheets_watcher.run_continuous, poll_interval=5)
"""


# PATTERN 4: Download email attachments and process
# ═══════════════════════════════════════════════════════════════════════════
"""
Extract attachments from emails and process with file watcher
"""

PATTERN_4 = """
from pathlib import Path
from Watchers.file_watcher import FileWatcher
from gmail_watcher import GmailWatcher

# Create directories
attachment_temp = Path("./temp_attachments")
attachment_temp.mkdir(exist_ok=True)

watcher = FileWatcher(
    watch_dir=attachment_temp,
    vault_dir=Path("./Vault")
)

# Setup Gmail (not shown - requires credentials)
gmail = GmailWatcher()

# In your processing loop:
# 1. Get emails
# 2. Download attachments to temp_attachments/
attachments = gmail.get_attachment()  # Your implementation
for att in attachments:
    att.save(attachment_temp / att.filename)

# 3. File watcher processes them
watcher.run_once()

# 4. Cleanup temp files
import shutil
shutil.rmtree(attachment_temp)
"""


# PATTERN 5: Auto-categorize files based on content
# ═══════════════════════════════════════════════════════════════════════════
"""
Extend FileWatcher to auto-categorize and route files
"""

PATTERN_5 = """
from pathlib import Path
from Watchers.file_watcher import FileWatcher
import json

class SmartFileWatcher(FileWatcher):
    '''Enhanced file watcher with auto-categorization'''
    
    def _process_file(self, file_path):
        # Process normally first
        result = super()._process_file(file_path)
        
        if result:
            # Now categorize the file
            category = self._categorize_file(file_path)
            
            # Move to category-specific folder
            category_folder = self.vault_dir / "Inbox" / f"Category_{category}"
            category_folder.mkdir(exist_ok=True)
            
            # Move the markdown entry
            md_file = (self.inbox_dir / f"FILE_DROP_{file_path.stem}*").glob("*")[0]
            new_path = category_folder / md_file.name
            md_file.rename(new_path)
    
    def _categorize_file(self, file_path):
        '''Determine file category'''
        file_type = self._get_file_type(file_path)
        
        categories = {
            'pdf': 'Documents',
            'document': 'Documents',
            'image': 'Media',
            'code': 'Code',
            'spreadsheet': 'Data',
            'archive': 'Archives',
            'text': 'Notes',
        }
        
        return categories.get(file_type, 'Other')

# Use it
watcher = SmartFileWatcher(
    watch_dir=Path("./Vault/Inbox/Drops"),
    vault_dir=Path("./Vault")
)
watcher.run_once()
"""


# PATTERN 6: Process files with Claude AI
# ═══════════════════════════════════════════════════════════════════════════
"""
Use Claude to analyze file contents and suggest actions
"""

PATTERN_6 = """
from pathlib import Path
from Watchers.file_watcher import FileWatcher
from anthropic import Anthropic

client = Anthropic()
watcher = FileWatcher(
    watch_dir=Path("./Vault/Inbox/Drops"),
    vault_dir=Path("./Vault")
)

# After processing files
watcher.run_once()

# Find new FILE_DROP entries
inbox = Path("./Vault/Inbox")
new_files = list(inbox.glob("FILE_DROP_*.md"))

for file_entry in new_files:
    content = file_entry.read_text()
    
    # Ask Claude what to do with it
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f'''This file was just dropped into our system:

{content}

What action should we take?
- Route to specific person/department
- Extract key information
- Archive or delete
- Process further

Be brief and specific.'''
        }]
    )
    
    # Save Claude's recommendation
    recommendation = response.content[0].text
    
    # Update the file with recommendation
    updated_content = content + f"""

## AI Recommendation

{recommendation}
"""
    
    file_entry.write_text(updated_content)
"""


# PATTERN 7: Watch Downloads folder (real example)
# ═══════════════════════════════════════════════════════════════════════════
"""
Monitor your Downloads folder for new files with extension filtering
"""

PATTERN_7 = """
from pathlib import Path
from Watchers.file_watcher import FileWatcher

# Use your actual Downloads folder
downloads = Path.home() / "Downloads"
vault = Path("./Vault")

watcher = FileWatcher(
    watch_dir=downloads,
    vault_dir=vault
)

# Only process specific file types
import fnmatch

def filter_important_files(file_path):
    '''Only process business files'''
    name = file_path.name.lower()
    important_patterns = [
        '*.pdf',      # Documents
        '*.xlsx',     # Spreadsheets
        '*.docx',     # Word docs
        '*.pptx',     # Presentations
        '*invoice*',  # Important files
        '*contract*',
        '*report*',
    ]
    
    return any(fnmatch.fnmatch(name, pattern) for pattern in important_patterns)

# Run with filtering
files = [f for f in downloads.iterdir() if filter_important_files(f)]
for file in files:
    watcher._process_file(file)
"""


# PATTERN 8: Real-time with watchdog (if installed)
# ═══════════════════════════════════════════════════════════════════════════
"""
Use watchdog for true real-time file system events (faster)
"""

PATTERN_8 = """
# First: pip install watchdog

from pathlib import Path
from Watchers.file_watcher import FileWatcher, FileWatcherEventHandler
from watchdog.observers import Observer

watch_dir = Path("./Vault/Inbox/Drops")
vault_dir = Path("./Vault")

watcher = FileWatcher(watch_dir, vault_dir)

# Create event handler
event_handler = FileWatcherEventHandler(watcher)

# Create observer
observer = Observer()
observer.schedule(event_handler, str(watch_dir), recursive=False)

# Start watching
observer.start()

print(f"🔍 Real-time watcher started for {watch_dir}")
print("Press Ctrl+C to stop")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
"""


# PATTERN 9: Database logging
# ═══════════════════════════════════════════════════════════════════════════
"""
Keep a log of all processed files in a database
"""

PATTERN_9 = """
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from Watchers.file_watcher import FileWatcher

class DatabaseLoggingWatcher(FileWatcher):
    def __init__(self, watch_dir, vault_dir, db_path="./file_watcher.db"):
        super().__init__(watch_dir, vault_dir)
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS processed_files (
                    id INTEGER PRIMARY KEY,
                    filename TEXT NOT NULL,
                    file_hash TEXT UNIQUE,
                    file_type TEXT,
                    size_bytes INTEGER,
                    processed_at TIMESTAMP,
                    metadata JSON
                )
            ''')
            conn.commit()
    
    def _process_file(self, file_path):
        result = super()._process_file(file_path)
        
        if result:
            file_hash = self._get_file_hash(file_path)
            file_type = self._get_file_type(file_path)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR IGNORE INTO processed_files
                    (filename, file_hash, file_type, size_bytes, processed_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    file_path.name,
                    file_hash,
                    file_type,
                    file_path.stat().st_size,
                    datetime.now().isoformat()
                ))
                conn.commit()
        
        return result

# Use it
watcher = DatabaseLoggingWatcher(
    watch_dir=Path("./Vault/Inbox/Drops"),
    vault_dir=Path("./Vault")
)
watcher.run_once()

# Query history
with sqlite3.connect("./file_watcher.db") as conn:
    cursor = conn.execute("SELECT * FROM processed_files ORDER BY processed_at DESC")
    for row in cursor:
        print(row)
"""


# PATTERN 10: Compress old files
# ═══════════════════════════════════════════════════════════════════════════
"""
Archive processed files after a certain period
"""

PATTERN_10 = """
import zipfile
from pathlib import Path
from datetime import datetime, timedelta

def archive_old_files(vault_dir, days_old=7):
    '''Compress files older than N days'''
    
    inbox = vault_dir / "Inbox"
    archive_dir = vault_dir / "Archives"
    archive_dir.mkdir(exist_ok=True)
    
    # Find old FILE_DROP files
    for file in inbox.glob("FILE_DROP_*.md"):
        mtime = datetime.fromtimestamp(file.stat().st_mtime)
        age = datetime.now() - mtime
        
        if age > timedelta(days=days_old):
            # Create archive
            archive_name = f"files_{mtime.strftime('%Y-%m-%d')}.zip"
            archive_path = archive_dir / archive_name
            
            with zipfile.ZipFile(archive_path, 'a') as zf:
                zf.write(file, arcname=file.name)
            
            # Remove original
            file.unlink()
            print(f"Archived: {file.name}")

# Run daily
archive_old_files(Path("./Vault"), days_old=30)
"""


def print_all_patterns():
    """Display all integration patterns."""
    patterns = [
        ("PATTERN 1", "Direct orchestrator integration", PATTERN_1),
        ("PATTERN 2", "Scheduled file processing", PATTERN_2),
        ("PATTERN 3", "Multiple watchers for different types", PATTERN_3),
        ("PATTERN 4", "Download email attachments", PATTERN_4),
        ("PATTERN 5", "Auto-categorize files based on content", PATTERN_5),
        ("PATTERN 6", "Process files with Claude AI", PATTERN_6),
        ("PATTERN 7", "Watch Downloads folder (real example)", PATTERN_7),
        ("PATTERN 8", "Real-time with watchdog", PATTERN_8),
        ("PATTERN 9", "Database logging", PATTERN_9),
        ("PATTERN 10", "Compress old files", PATTERN_10),
    ]
    
    print("\n" + "="*79)
    print("FILE WATCHER INTEGRATION PATTERNS".center(79))
    print("="*79 + "\n")
    
    for pattern_num, title, code in patterns:
        print(f"\n{pattern_num}: {title}")
        print("-" * 79)
        print(code)
        print()
    
    print("="*79)
    print("Choose the pattern that fits your workflow!".center(79))
    print("="*79 + "\n")


if __name__ == "__main__":
    print_all_patterns()
