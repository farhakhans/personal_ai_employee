"""
DEMO EMAIL SERVICE - Test Email Flow Without Real Credentials
═══════════════════════════════════════════════════════════════════════════

Simulates real email sending and receiving for testing.
Creates local email files without connecting to SMTP/IMAP servers.

Usage:
    python demo_email_service.py send --to user@example.com --subject "Test" --body "Hello"
    python demo_email_service.py receive
    python demo_email_service.py inbox
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import hashlib


class DemoEmailService:
    """Demo email service for testing without real credentials."""
    
    def __init__(self, vault_path: str = None):
        # Use absolute path based on script location
        if vault_path is None:
            vault_path = Path(__file__).parent / "Vault"
        else:
            vault_path = Path(vault_path)
        
        self.vault_path = vault_path
        self.inbox_dir = self.vault_path / "Inbox" / "EMAIL"
        self.sent_dir = self.vault_path / "Sent" / "EMAIL"
        self.demo_dir = self.vault_path / "Demo" / "EMAIL"
        
        # Create directories
        for dir_path in [self.inbox_dir, self.sent_dir, self.demo_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.demo_email = "demo@ai-employee.local"
        print(f"📧 Demo Email Service initialized")
        print(f"   Email: {self.demo_email}")
        print(f"   Inbox: {self.inbox_dir}")
        print(f"   Sent: {self.sent_dir}")
        print()
    
    def send_email(self, to: str, subject: str, body: str,
                   html: bool = False, cc: Optional[str] = None,
                   attachments: Optional[List[str]] = None) -> Dict[str, any]:
        """Simulate sending an email."""
        timestamp = datetime.now()
        
        # Create email record
        email_data = {
            'from': self.demo_email,
            'to': to,
            'cc': cc,
            'subject': subject,
            'body': body,
            'html': html,
            'timestamp': timestamp.isoformat(),
            'status': 'sent',
            'attachments': attachments or []
        }
        
        # Save to sent folder
        self._save_email(self.sent_dir, email_data)
        
        # Simulate delivery - create in inbox too
        inbox_data = email_data.copy()
        inbox_data['from'] = to  # Simulate reply
        inbox_data['subject'] = f"Re: {subject}"
        inbox_data['body'] = f"This is an automated demo response to:\n\n{body}"
        inbox_data['status'] = 'received'
        
        self._save_email(self.inbox_dir, inbox_data)
        
        print(f"✅ Email sent (DEMO MODE)")
        print(f"   To: {to}")
        print(f"   Subject: {subject}")
        print(f"   Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Location: {self.sent_dir}")
        print()
        
        return {
            'status': 'success',
            'message': f'Email sent to {to} (demo mode)',
            'subject': subject,
            'timestamp': timestamp.isoformat()
        }
    
    def receive_emails(self, limit: int = 10) -> List[Dict[str, any]]:
        """Load emails from inbox."""
        emails = []
        
        if self.inbox_dir.exists():
            email_files = list(self.inbox_dir.glob("*.md"))
            email_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            for file_path in email_files[:limit]:
                email_data = self._load_email(file_path)
                if email_data:
                    emails.append(email_data)
        
        print(f"📬 Found {len(emails)} email(s) in inbox")
        print()
        
        return emails
    
    def _save_email(self, directory: Path, email_data: Dict):
        """Save email to markdown file."""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        # Clean subject - remove colons and limit length
        subject_safe = email_data['subject'].replace(' ', '_').replace('/', '_').replace(':', '')[:20]
        
        if email_data['status'] == 'sent':
            filename = f"SENT_{email_data['to'].replace('@', '_')}_{subject_safe}_{timestamp}.md"
        else:
            filename = f"EMAIL_{email_data['from'].replace('@', '_')}_{subject_safe}_{timestamp}.md"
        
        content = f"""# Email - {email_data['status'].upper()}

## Header
- **Subject:** {email_data['subject']}
- **From:** {email_data['from']}
- **To:** {email_data['to']}
{f"- **CC:** {email_data['cc']}" if email_data.get('cc') else ""}
- **Date:** {email_data['timestamp']}
- **Status:** {email_data['status']}

## Content

{email_data['body']}

## Metadata
- **Format:** {'HTML' if email_data.get('html') else 'Plain Text'}
- **Attachments:** {', '.join(email_data.get('attachments', [])) if email_data.get('attachments') else 'None'}

## Status
- [ ] Read
- [ ] Processed
- [ ] Archived

---
*Saved by Demo Email Service*
"""
        
        with open(directory / filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _load_email(self, file_path: Path) -> Optional[Dict]:
        """Load email from markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple parsing
            lines = content.split('\n')
            email_data = {'file': file_path.name}
            
            for line in lines:
                if line.startswith('- **Subject:**'):
                    email_data['subject'] = line.replace('- **Subject:**', '').strip()
                elif line.startswith('- **From:**'):
                    email_data['from'] = line.replace('- **From:**', '').strip()
                elif line.startswith('- **To:**'):
                    email_data['to'] = line.replace('- **To:**', '').strip()
                elif line.startswith('## Content'):
                    break
            
            email_data['body'] = content
            return email_data
            
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None
    
    def show_inbox(self):
        """Display inbox summary."""
        print(f"📬 Inbox for {self.demo_email}")
        print(f"   Location: {self.inbox_dir}")
        print()
        
        if self.inbox_dir.exists():
            emails = list(self.inbox_dir.glob("*.md"))
            emails.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            if emails:
                print(f"Found {len(emails)} email(s):\n")
                for i, email_file in enumerate(emails[:20], 1):
                    stat = email_file.stat()
                    modified = datetime.fromtimestamp(stat.st_mtime)
                    print(f"  {i}. {email_file.name}")
                    print(f"     Modified: {modified.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print("📭 Inbox is empty")
        else:
            print("📭 Inbox directory does not exist")
        
        print()


def cmd_send(args):
    """Send email from CLI."""
    email_service = DemoEmailService()
    email_service.send_email(
        to=args.to,
        subject=args.subject,
        body=args.body,
        html=args.html,
        cc=args.cc,
        attachments=args.attachments
    )


def cmd_receive(args):
    """Receive emails from CLI."""
    email_service = DemoEmailService()
    emails = email_service.receive_emails(limit=args.limit)
    
    if emails:
        for i, email_data in enumerate(emails, 1):
            print(f"{'='*60}")
            print(f"📧 Email #{i}")
            print(f"   File: {email_data.get('file', 'N/A')}")
            print(f"   From: {email_data.get('from', 'N/A')}")
            print(f"   Subject: {email_data.get('subject', 'N/A')}")
            print()


def cmd_inbox(args):
    """Show inbox."""
    email_service = DemoEmailService()
    email_service.show_inbox()


def cmd_compose(args):
    """Interactive compose."""
    email_service = DemoEmailService()
    
    print("\n" + "="*60)
    print("📝 COMPOSE NEW EMAIL (DEMO MODE)")
    print("="*60 + "\n")
    
    to = input("To: ").strip()
    if not to:
        print("❌ Recipient required")
        return
    
    subject = input("Subject: ").strip()
    if not subject:
        print("❌ Subject required")
        return
    
    print("\nBody (end with empty line):")
    body_lines = []
    while True:
        line = input()
        if not line and body_lines:
            break
        body_lines.append(line)
    
    body = '\n'.join(body_lines)
    
    print(f"\nSending to {to}...")
    email_service.send_email(to=to, subject=subject, body=body)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Demo Email Service CLI")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Send
    send_p = subparsers.add_parser('send', help='Send email')
    send_p.add_argument('--to', required=True)
    send_p.add_argument('--subject', required=True)
    send_p.add_argument('--body', required=True)
    send_p.add_argument('--html', action='store_true')
    send_p.add_argument('--cc')
    send_p.add_argument('--attachments', nargs='*')
    send_p.set_defaults(func=cmd_send)
    
    # Receive
    recv_p = subparsers.add_parser('receive', help='Receive emails')
    recv_p.add_argument('--limit', type=int, default=10)
    recv_p.set_defaults(func=cmd_receive)
    
    # Inbox
    inbox_p = subparsers.add_parser('inbox', help='Show inbox')
    inbox_p.set_defaults(func=cmd_inbox)
    
    # Compose
    compose_p = subparsers.add_parser('compose', help='Compose email')
    compose_p.set_defaults(func=cmd_compose)
    
    args = parser.parse_args()
    
    if args.command:
        args.func(args)
    else:
        print("Demo Email Service - Test without real credentials")
        print("\nCommands:")
        print("  send      - Send an email")
        print("  receive   - Receive emails")
        print("  inbox     - Show inbox")
        print("  compose   - Interactive compose")
        print("\nExamples:")
        print("  python demo_email_service.py send --to user@example.com --subject 'Hello' --body 'Test'")
        print("  python demo_email_service.py receive")
        print("  python demo_email_service.py inbox")
        print("  python demo_email_service.py compose")
