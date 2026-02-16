"""
FILE SYSTEM WATCHER
═══════════════════════════════════════════════════════════════════════════

Monitors a local directory for dropped files and processes them into the vault.

Features:
- Watch any local directory for file drops
- Process multiple file types (documents, images, text, etc.)
- Extract metadata and content
- Auto-categorize based on file type
- Integrate with orchestrator for AI analysis
- Deduplicate files (track processed files)
- Real-time monitoring with configurable polling

Use Case: Drop files from emails, documents, screenshots, PDFs directly
into a folder and AI Employee will automatically process them.
"""

import os
import time
import logging
import json
import mimetypes
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set
import hashlib
import shutil

# Optional: pip install watchdog (for better performance)
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("⚠️  watchdog not installed. Using polling mode (slower).")
    print("   Install: pip install watchdog")


class FileWatcher:
    """Monitors a directory for dropped files and processes them."""
    
    def __init__(self, watch_dir: Path, vault_dir: Path, processed_file: Optional[Path] = None):
        """
        Initialize file watcher.
        
        Args:
            watch_dir: Directory to monitor for file drops
            vault_dir: Vault directory for saving processed files
            processed_file: File to track processed file hashes
        """
        self.watch_dir = Path(watch_dir)
        self.vault_dir = Path(vault_dir)
        self.inbox_dir = vault_dir / "Inbox"
        
        # Create directories if not exist
        self.watch_dir.mkdir(parents=True, exist_ok=True)
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        
        # Processed file tracking
        self.processed_file = processed_file or self.watch_dir / ".processed_files.json"
        self.processed_hashes: Set[str] = self._load_processed_files()
        
        # Logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - FILE_WATCHER - %(levelname)s - %(message)s'
        )
        
        # File type handlers
        self.handlers = {
            'text': self._process_text_file,
            'code': self._process_code_file,
            'document': self._process_document,
            'image': self._process_image,
            'spreadsheet': self._process_spreadsheet,
            'pdf': self._process_pdf,
            'archive': self._process_archive,
            'other': self._process_generic,
        }
        
        # Watchdog observer (if available)
        self.observer = None
        if WATCHDOG_AVAILABLE:
            self.observer = Observer()
        
        self.running = False
    
    def _load_processed_files(self) -> Set[str]:
        """Load set of processed file hashes from cache."""
        if self.processed_file.exists():
            try:
                with open(self.processed_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('processed_hashes', []))
            except Exception as e:
                self.logger.warning(f"Could not load processed files: {e}")
        return set()
    
    def _save_processed_files(self):
        """Save processed file hashes to cache."""
        try:
            with open(self.processed_file, 'w') as f:
                json.dump({
                    'processed_hashes': list(self.processed_hashes),
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            self.logger.error(f"Could not save processed files: {e}")
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file for deduplication."""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            self.logger.error(f"Could not hash file {file_path}: {e}")
            return ""
    
    def _get_file_type(self, file_path: Path) -> str:
        """Determine file type category."""
        ext = file_path.suffix.lower()
        name = file_path.name.lower()
        
        # Text files
        text_exts = {'.txt', '.md', '.rst', '.json', '.yaml', '.yml', '.xml', '.csv', '.log'}
        if ext in text_exts:
            return 'text'
        
        # Code files
        code_exts = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.rb', '.php', '.sql', '.html', '.css', '.scss'}
        if ext in code_exts:
            return 'code'
        
        # Documents
        doc_exts = {'.pdf', '.doc', '.docx', '.odt', '.pages', '.wpd'}
        if ext == '.pdf':
            return 'pdf'
        if ext in doc_exts:
            return 'document'
        
        # Spreadsheets
        sheet_exts = {'.xls', '.xlsx', '.csv', '.ods', '.numbers', '.ics'}
        if ext in sheet_exts:
            return 'spreadsheet'
        
        # Images
        image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'}
        if ext in image_exts:
            return 'image'
        
        # Archives
        archive_exts = {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'}
        if ext in archive_exts:
            return 'archive'
        
        return 'other'
    
    def _process_text_file(self, file_path: Path) -> Dict:
        """Process text file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return {
                'type': 'text',
                'content': content[:2000],  # First 2000 chars
                'size_bytes': file_path.stat().st_size,
                'total_lines': len(content.split('\n')),
            }
        except Exception as e:
            self.logger.error(f"Could not process text file {file_path}: {e}")
            return {'type': 'text', 'error': str(e)}
    
    def _process_code_file(self, file_path: Path) -> Dict:
        """Process code file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            return {
                'type': 'code',
                'language': file_path.suffix[1:],
                'content_preview': '\n'.join(lines[:20]),  # First 20 lines
                'total_lines': len(lines),
                'size_bytes': file_path.stat().st_size,
            }
        except Exception as e:
            self.logger.error(f"Could not process code file {file_path}: {e}")
            return {'type': 'code', 'error': str(e)}
    
    def _process_document(self, file_path: Path) -> Dict:
        """Process document file (Word, etc)."""
        return {
            'type': 'document',
            'format': file_path.suffix[1:],
            'size_bytes': file_path.stat().st_size,
            'note': 'Document saved to vault. Use external parser for full content extraction.',
        }
    
    def _process_image(self, file_path: Path) -> Dict:
        """Process image file."""
        try:
            from PIL import Image
            img = Image.open(file_path)
            return {
                'type': 'image',
                'format': img.format,
                'dimensions': f"{img.width}x{img.height}",
                'size_bytes': file_path.stat().st_size,
            }
        except ImportError:
            return {
                'type': 'image',
                'size_bytes': file_path.stat().st_size,
                'note': 'Install Pillow for image metadata: pip install Pillow',
            }
        except Exception as e:
            return {'type': 'image', 'error': str(e)}
    
    def _process_spreadsheet(self, file_path: Path) -> Dict:
        """Process spreadsheet file."""
        return {
            'type': 'spreadsheet',
            'format': file_path.suffix[1:],
            'size_bytes': file_path.stat().st_size,
            'note': 'Spreadsheet saved to vault. Use pandas for data processing.',
        }
    
    def _process_pdf(self, file_path: Path) -> Dict:
        """Process PDF file."""
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            pages = len(reader.pages)
            return {
                'type': 'pdf',
                'pages': pages,
                'size_bytes': file_path.stat().st_size,
            }
        except ImportError:
            return {
                'type': 'pdf',
                'size_bytes': file_path.stat().st_size,
                'note': 'Install PyPDF2 for page count: pip install PyPDF2',
            }
        except Exception as e:
            return {'type': 'pdf', 'error': str(e)}
    
    def _process_archive(self, file_path: Path) -> Dict:
        """Process archive file."""
        try:
            import zipfile
            if file_path.suffix.lower() == '.zip':
                with zipfile.ZipFile(file_path, 'r') as zf:
                    file_list = zf.namelist()
                    return {
                        'type': 'archive',
                        'format': 'zip',
                        'files_count': len(file_list),
                        'size_bytes': file_path.stat().st_size,
                        'files': file_list[:10],  # First 10 files
                    }
        except Exception as e:
            self.logger.error(f"Could not process archive {file_path}: {e}")
        
        return {
            'type': 'archive',
            'format': file_path.suffix[1:],
            'size_bytes': file_path.stat().st_size,
        }
    
    def _process_generic(self, file_path: Path) -> Dict:
        """Process unknown file type."""
        return {
            'type': 'other',
            'format': file_path.suffix[1:] or 'unknown',
            'size_bytes': file_path.stat().st_size,
        }
    
    def _process_file(self, file_path: Path) -> bool:
        """
        Process a single file.
        
        Returns:
            True if processed successfully, False if skipped or error
        """
        try:
            # Skip hidden files and system files
            if file_path.name.startswith('.') or file_path.name.startswith('~'):
                return False
            
            # Skip if file is still being written
            mtime = file_path.stat().st_mtime
            if time.time() - mtime < 2:  # File modified in last 2 seconds
                return False
            
            # Calculate file hash
            file_hash = self._get_file_hash(file_path)
            if not file_hash:
                return False
            
            # Check if already processed
            if file_hash in self.processed_hashes:
                self.logger.info(f"⏭️  Skipping duplicate: {file_path.name}")
                return False
            
            # Create vault entry
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            vault_filename = f"FILE_DROP_{file_path.stem}_{timestamp}.md"
            vault_path = self.inbox_dir / vault_filename
            
            # Get file type and process
            file_type = self._get_file_type(file_path)
            handler = self.handlers.get(file_type, self.handlers['other'])
            metadata = handler(file_path)
            
            # Create markdown entry
            markdown_content = f"""# File Drop: {file_path.name}

**Received:** {datetime.now().isoformat()}
**File Size:** {file_path.stat().st_size} bytes
**File Hash:** {file_hash[:16]}...
**File Type:** {file_type}
**Original Path:** {file_path}

## Metadata
```json
{json.dumps(metadata, indent=2)}
```

## Status
- [ ] Review
- [ ] Action
- [ ] Archive

## Action Items
- What should AI Employee do with this file?
- Auto-route to specific person or process
- Extract specific information

## Notes
Add notes here for AI Employee processing.
"""
            
            # Save to vault
            with open(vault_path, 'w') as f:
                f.write(markdown_content)
            
            # Also copy original file to vault for reference
            file_copy_path = self.inbox_dir / f"FILE_{file_path.stem}_{timestamp}{file_path.suffix}"
            try:
                shutil.copy2(file_path, file_copy_path)
            except Exception as e:
                self.logger.warning(f"Could not copy file to vault: {e}")
            
            # Mark as processed
            self.processed_hashes.add(file_hash)
            self._save_processed_files()
            
            self.logger.info(f"✅ Processed: {file_path.name} → {vault_filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {e}")
            return False
    
    def _get_all_files(self) -> List[Path]:
        """Get all unprocessed files in watch directory."""
        try:
            files = [f for f in self.watch_dir.iterdir() 
                    if f.is_file() and not f.name.startswith('.')]
            return sorted(files, key=lambda f: f.stat().st_mtime)
        except Exception as e:
            self.logger.error(f"Error listing files: {e}")
            return []
    
    def run_once(self) -> int:
        """
        Scan watch directory once and process new files.
        
        Returns:
            Number of files processed
        """
        files = self._get_all_files()
        if not files:
            return 0
        
        count = 0
        for file_path in files:
            if self._process_file(file_path):
                count += 1
        
        if count > 0:
            self.logger.info(f"📊 Scan complete: {count} file(s) processed")
        
        return count
    
    def run_continuous(self, poll_interval: int = 5, max_duration: Optional[int] = None):
        """
        Continuously monitor directory for new files.
        
        Args:
            poll_interval: Seconds between scans (default: 5)
            max_duration: Maximum run time in seconds (None = infinite)
        """
        self.running = True
        start_time = time.time()
        
        self.logger.info(f"🔍 File Watcher started - monitoring: {self.watch_dir}")
        self.logger.info(f"📁 Vault inbox: {self.inbox_dir}")
        self.logger.info(f"⏱️  Polling interval: {poll_interval} seconds")
        
        try:
            scan_count = 0
            while self.running:
                try:
                    # Check if max duration exceeded
                    if max_duration and (time.time() - start_time) > max_duration:
                        self.logger.info(f"⏸️  Max duration ({max_duration}s) reached")
                        break
                    
                    # Scan once
                    count = self.run_once()
                    scan_count += 1
                    
                    if count > 0:
                        self.logger.info(f"📈 Total processed this session: {count}")
                    
                    # Wait for next scan
                    time.sleep(poll_interval)
                    
                except KeyboardInterrupt:
                    self.logger.info("⏹️  Keyboard interrupt received")
                    break
                except Exception as e:
                    self.logger.error(f"Error in monitoring loop: {e}")
                    time.sleep(poll_interval)
        
        finally:
            self.running = False
            self.logger.info(f"✅ File Watcher stopped - {scan_count} scans completed")
    
    def stop(self):
        """Stop the file watcher."""
        self.running = False
        if self.observer:
            self.observer.stop()
            self.observer.join()


class FileWatcherEventHandler(FileSystemEventHandler):
    """Watchdog event handler for file drops (optional, better performance)."""
    
    def __init__(self, watcher: FileWatcher):
        self.watcher = watcher
    
    def on_created(self, event):
        if event.is_directory:
            return
        file_path = Path(event.src_path)
        time.sleep(1)  # Wait for file to fully write
        self.watcher._process_file(file_path)


# Demo / Testing
if __name__ == "__main__":
    import sys
    
    # Example: Monitor current directory
    watch_directory = Path("./drops")
    vault_directory = Path("./Vault")
    
    watcher = FileWatcher(watch_directory, vault_directory)
    
    # Create test drops directory
    watch_directory.mkdir(exist_ok=True)
    
    print("\n" + "="*70)
    print("FILE SYSTEM WATCHER - Demo")
    print("="*70)
    print(f"\n📁 Watching: {watch_directory.absolute()}")
    print(f"💾 Vault Inbox: {watcher.inbox_dir.absolute()}")
    print("\nTry these commands in another terminal:")
    print(f'  echo "test content" > {watch_directory}/test.txt')
    print(f'  copy some.pdf {watch_directory}/')
    print("\nPress Ctrl+C to stop watcher...")
    print("-"*70 + "\n")
    
    # Run continuous monitoring
    watcher.run_continuous(poll_interval=2)
