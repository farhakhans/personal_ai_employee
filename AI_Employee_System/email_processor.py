"""
EMAIL PROCESSING SYSTEM & LOGGING
═══════════════════════════════════════════════════════════════════════════

Manages email ingestion, processing, and logging for the autonomous AI Employee.
Integrates with Gmail watcher and provides complete email audit trail.

Features:
- Email inbox management
- Email processing logs
- Automated responses
- Email categorization
- Error tracking
- Complete audit trail
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum


class EmailStatus(Enum):
    """Status of email in processing pipeline."""
    RECEIVED = "received"
    READING = "reading"
    PROCESSING = "processing"
    RESPONDING = "responding"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


class EmailCategory(Enum):
    """Email categorization."""
    INBOX = "inbox"
    APPROVAL = "approval"
    NOTIFICATION = "notification"
    REPORT = "report"
    SPAM = "spam"
    ARCHIVED = "archived"


@dataclass
class EmailRecord:
    """Individual email record."""
    email_id: str
    from_address: str
    to_address: str
    subject: str
    body: str
    timestamp: str
    status: str = EmailStatus.RECEIVED.value
    category: str = EmailCategory.INBOX.value
    processing_notes: str = ""
    response_sent: bool = False
    response_content: Optional[str] = None
    error_message: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    requires_approval: bool = False
    approved: bool = False
    approval_by: Optional[str] = None


class EmailLogger:
    """Logging system for all email operations."""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.logs_dir = vault_path / "System" / "email_logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self.inbox_dir = vault_path / "Inbox"
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger('EmailProcessor')
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging handler."""
        log_file = self.logs_dir / "email_processing.log"
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_received(self, email_record: EmailRecord) -> None:
        """Log received email."""
        self.logger.info(f"Email received: {email_record.email_id} from {email_record.from_address}")
        self._save_email_record(email_record)
    
    def log_processing(self, email_id: str, status: str, notes: str = "") -> None:
        """Log processing status."""
        self.logger.info(f"Email {email_id} status: {status}")
        if notes:
            self.logger.debug(f"  Notes: {notes}")
    
    def log_error(self, email_id: str, error: Exception) -> None:
        """Log processing error."""
        self.logger.error(f"Error processing email {email_id}: {error}")
    
    def log_response(self, email_id: str, response_content: str) -> None:
        """Log response sent."""
        self.logger.info(f"Response sent to email {email_id}")
        self.logger.debug(f"  Content: {response_content[:100]}...")
    
    def _save_email_record(self, record: EmailRecord) -> None:
        """Save email record to JSON."""
        record_file = self.logs_dir / f"{record.email_id}.json"
        record_file.write_text(json.dumps(asdict(record), indent=2))


class EmailInbox:
    """Manages email inbox structure and processing."""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.inbox_dir = vault_path / "Inbox"
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.subdirs = {
            "unread": self.inbox_dir / "Unread",
            "needs_action": self.inbox_dir / "Needs_Action",
            "approvals": self.inbox_dir / "Approvals_Needed",
            "processed": self.inbox_dir / "Processed",
            "archived": self.inbox_dir / "Archived"
        }
        
        for subdir in self.subdirs.values():
            subdir.mkdir(parents=True, exist_ok=True)
    
    def add_to_inbox(
        self,
        email_id: str,
        subject: str,
        from_address: str,
        body_preview: str,
        requires_action: bool = False,
        requires_approval: bool = False
    ) -> Path:
        """Add email to appropriate inbox folder."""
        
        # Determine destination
        if requires_approval:
            dest_dir = self.subdirs["approvals"]
        elif requires_action:
            dest_dir = self.subdirs["needs_action"]
        else:
            dest_dir = self.subdirs["unread"]
        
        # Create email file
        email_file = dest_dir / f"{email_id}_{subject[:30].replace(' ', '_')}.md"
        
        content = f"""# Email from {from_address}

**Date:** {datetime.now().isoformat()}  
**Subject:** {subject}  
**Email ID:** {email_id}  
**Status:** Unread

## Preview
{body_preview}

## Actions
- Review full email in Gmail
- Archive
- Mark as processed
- Assign to team member

## Notes
_Add notes here_
"""
        
        email_file.write_text(content)
        return email_file
    
    def mark_processed(self, email_id: str) -> None:
        """Move email to processed folder."""
        # Find and move the file
        for subdir in [self.subdirs["unread"], self.subdirs["needs_action"], self.subdirs["approvals"]]:
            for file in subdir.glob(f"{email_id}_*"):
                file.rename(self.subdirs["processed"] / file.name)
    
    def archive_email(self, email_id: str) -> None:
        """Move email to archived folder."""
        for subdir in self.subdirs.values():
            for file in subdir.glob(f"{email_id}_*"):
                file.rename(self.subdirs["archived"] / file.name)
    
    def get_inbox_summary(self) -> Dict:
        """Get summary of inbox contents."""
        summary = {}
        for name, subdir in self.subdirs.items():
            count = len(list(subdir.glob("*.md")))
            summary[name] = count
        return summary


class EmailProcessor:
    """Main email processing orchestrator."""
    
    def __init__(self, vault_path: Path, error_recovery=None):
        self.vault_path = vault_path
        self.logger = EmailLogger(vault_path)
        self.inbox = EmailInbox(vault_path)
        self.error_recovery = error_recovery
        self.processed_count = 0
        self.error_count = 0
    
    def process_email(
        self,
        email_id: str,
        from_address: str,
        to_address: str,
        subject: str,
        body: str,
        requires_action: bool = False,
        requires_approval: bool = False
    ) -> Dict:
        """Process incoming email."""
        
        try:
            # Create email record
            record = EmailRecord(
                email_id=email_id,
                from_address=from_address,
                to_address=to_address,
                subject=subject,
                body=body,
                timestamp=datetime.now().isoformat(),
                requires_approval=requires_approval
            )
            
            # Log receipt
            self.logger.log_received(record)
            
            # Add to inbox
            self.inbox.add_to_inbox(
                email_id,
                subject,
                from_address,
                body[:200],  # Preview
                requires_action,
                requires_approval
            )
            
            self.processed_count += 1
            
            return {
                "success": True,
                "email_id": email_id,
                "status": "processing",
                "action": "added_to_inbox"
            }
        
        except Exception as e:
            self.logger.log_error(email_id, e)
            self.error_count += 1
            
            if self.error_recovery:
                self.error_recovery.capture_error(
                    "email_processor",
                    e,
                    {"email_id": email_id},
                    "ERROR"
                )
            
            return {
                "success": False,
                "email_id": email_id,
                "error": str(e)
            }
    
    def send_response(
        self,
        email_id: str,
        to_address: str,
        response_subject: str,
        response_body: str
    ) -> Dict:
        """Send email response."""
        
        try:
            self.logger.log_response(email_id, response_body)
            
            # Log response in system
            response_log = self.vault_path / "System" / "email_logs" / f"{email_id}_response.txt"
            response_log.write_text(f"""
To: {to_address}
Subject: {response_subject}
Timestamp: {datetime.now().isoformat()}

{response_body}
""")
            
            return {
                "success": True,
                "to_address": to_address,
                "subject": response_subject
            }
        
        except Exception as e:
            self.logger.log_error(email_id, e)
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_stats(self) -> Dict:
        """Get email processing statistics."""
        inbox_summary = self.inbox.get_inbox_summary()
        
        return {
            "total_processed": self.processed_count,
            "errors": self.error_count,
            "inbox": inbox_summary,
            "timestamp": datetime.now().isoformat()
        }


# Example usage
if __name__ == "__main__":
    vault_path = Path("./Vault")
    
    # Initialize
    email_processor = EmailProcessor(vault_path)
    
    # Example: Process incoming email
    result = email_processor.process_email(
        email_id="gmail_msg_001",
        from_address="client@example.com",
        to_address="info@company.com",
        subject="Project Inquiry",
        body="Hi, I'm interested in your services. Can we schedule a call?",
        requires_action=True
    )
    
    print(f"Email processing result: {result}")
    print(f"Inbox summary: {email_processor.get_stats()}")
    
    # Save stats
    stats_file = vault_path / "System" / "email_stats.json"
    stats_file.write_text(json.dumps(email_processor.get_stats(), indent=2))
    print(f"✓ Email stats saved to {stats_file}")
