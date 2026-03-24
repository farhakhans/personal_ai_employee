"""
REAL EMAIL SERVICE - SMTP/IMAP Email Flow
═══════════════════════════════════════════════════════════════════════════

Real email sending and receiving using SMTP and IMAP protocols.
Works with Gmail, Outlook, Yahoo, and custom SMTP servers.

Features:
- Send real emails via SMTP
- Receive real emails via IMAP
- Compose emails with attachments
- HTML and plain text support
- CLI commands for all operations

Usage:
    python real_email_service.py send --to recipient@example.com --subject "Hello" --body "Message"
    python real_email_service.py receive
    python real_email_service.py inbox
    python real_email_service.py compose
"""

import os
import sys
import json
import logging
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import decode_header
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - EMAIL_SERVICE - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RealEmailService:
    """
    Real email service using SMTP for sending and IMAP for receiving.
    
    Supports:
    - Gmail (smtp.gmail.com, imap.gmail.com)
    - Outlook (smtp-mail.outlook.com, outlook.office365.com)
    - Yahoo (smtp.mail.yahoo.com, imap.mail.yahoo.com)
    - Custom SMTP/IMAP servers
    """
    
    # Provider configurations
    PROVIDERS = {
        'gmail': {
            'smtp': 'smtp.gmail.com',
            'smtp_port': 587,
            'imap': 'imap.gmail.com',
            'imap_port': 993,
            'name': 'Gmail'
        },
        'outlook': {
            'smtp': 'smtp-mail.outlook.com',
            'smtp_port': 587,
            'imap': 'outlook.office365.com',
            'imap_port': 993,
            'name': 'Outlook'
        },
        'yahoo': {
            'smtp': 'smtp.mail.yahoo.com',
            'smtp_port': 465,
            'imap': 'imap.mail.yahoo.com',
            'imap_port': 993,
            'name': 'Yahoo'
        }
    }
    
    def __init__(self, email_addr: str, password: str, provider: str = 'gmail'):
        """
        Initialize email service.
        
        Args:
            email_addr: Your email address
            password: Email password or app password (spaces will be removed)
            provider: Email provider (gmail, outlook, yahoo, custom)
        """
        self.email_addr = email_addr
        # Remove spaces from password (Gmail app passwords have spaces)
        self.password = password.replace(' ', '') if password else password
        self.provider = provider.lower()
        self.vault_path = Path(os.getenv('VAULT_PATH', '../Vault'))
        
        # Get server settings
        if provider in self.PROVIDERS:
            config = self.PROVIDERS[provider]
            self.smtp_server = config['smtp']
            self.smtp_port = config['smtp_port']
            self.imap_server = config['imap']
            self.imap_port = config['imap_port']
        else:
            # Custom provider
            self.smtp_server = os.getenv('CUSTOM_SMTP_SERVER', 'smtp.gmail.com')
            self.smtp_port = int(os.getenv('CUSTOM_SMTP_PORT', '587'))
            self.imap_server = os.getenv('CUSTOM_IMAP_SERVER', 'imap.gmail.com')
            self.imap_port = int(os.getenv('CUSTOM_IMAP_PORT', '993'))
        
        # Create vault directories
        self.inbox_dir = self.vault_path / "Inbox" / "EMAIL"
        self.sent_dir = self.vault_path / "Sent" / "EMAIL"
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        self.sent_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"✅ Email Service initialized for {email_addr} ({provider})")
    
    def send_email(self, to: str, subject: str, body: str, 
                   html: bool = False, cc: Optional[str] = None,
                   bcc: Optional[str] = None, 
                   attachments: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Send a real email via SMTP.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
            html: If True, send as HTML email
            cc: CC recipients (comma-separated)
            bcc: BCC recipients (comma-separated)
            attachments: List of file paths to attach
            
        Returns:
            dict: Status and message details
        """
        try:
            logger.info(f"📧 Sending email to {to}...")
            
            # Create message
            msg = MIMEMultipart("alternative")
            msg['Subject'] = subject
            msg['From'] = self.email_addr
            msg['To'] = to
            
            if cc:
                msg['Cc'] = cc
            
            # Add body
            if html:
                msg.attach(MIMEText(body, 'html', 'utf-8'))
            else:
                msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        self._attach_file(msg, file_path)
                        logger.info(f"📎 Attached: {file_path}")
            
            # Get all recipients
            all_recipients = [to]
            if cc:
                all_recipients.extend(cc.split(','))
            if bcc:
                all_recipients.extend(bcc.split(','))
            
            # Connect and send
            logger.info(f"🔌 Connecting to SMTP server {self.smtp_server}:{self.smtp_port}")
            
            if self.smtp_port == 465:
                # SSL connection
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                # TLS connection
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
            
            server.login(self.email_addr, self.password)
            server.sendmail(self.email_addr, all_recipients, msg.as_string())
            server.quit()
            
            logger.info(f"✅ Email sent successfully to {to}!")
            
            # Save to sent folder
            self._save_email('sent', {
                'to': to,
                'cc': cc,
                'subject': subject,
                'body': body,
                'html': html,
                'timestamp': datetime.now().isoformat()
            })
            
            return {
                'status': 'success',
                'message': f'Email sent to {to}',
                'subject': subject,
                'timestamp': datetime.now().isoformat()
            }
            
        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"❌ SMTP Authentication failed: {str(e)}"
            logger.error(error_msg)
            return {
                'status': 'error',
                'message': 'Authentication failed. Please check:\n1. Gmail address is correct\n2. App Password (not regular password) is used\n3. 2FA is enabled on Google Account\n4. Get App Password from: https://myaccount.google.com/apppasswords',
                'error_code': 'SMTP_AUTH_FAILED'
            }
        except smtplib.SMTPException as e:
            error_msg = f"❌ SMTP error: {str(e)}"
            logger.error(error_msg)
            return {'status': 'error', 'message': str(e)}
        except Exception as e:
            error_msg = f"❌ Failed to send email: {str(e)}"
            logger.error(error_msg)
            return {'status': 'error', 'message': str(e)}
    
    def receive_emails(self, limit: int = 10, unread_only: bool = True) -> List[Dict[str, Any]]:
        """
        Receive emails from IMAP server.
        
        Args:
            limit: Maximum number of emails to fetch
            unread_only: Only fetch unread emails
            
        Returns:
            list: List of email dictionaries
        """
        emails_list = []
        
        try:
            logger.info(f"📥 Connecting to IMAP server {self.imap_server}:{self.imap_port}")
            
            # Connect to IMAP
            if self.imap_port == 993:
                mail = imaplib.IMAP4_SSL(self.imap_server)
            else:
                mail = imaplib.IMAP4(self.imap_server)
            
            mail.login(self.email_addr, self.password)
            mail.select('inbox')
            
            # Search for emails
            if unread_only:
                status, messages = mail.search(None, 'UNSEEN')
            else:
                status, messages = mail.search(None, 'ALL')
            
            if status != 'OK':
                logger.warning("No messages found!")
                return emails_list
            
            # Get email IDs
            email_ids = messages[0].split()
            
            if not email_ids:
                logger.info("✅ No new emails!")
                return emails_list
            
            # Fetch latest emails (up to limit)
            email_ids = email_ids[-limit:]
            logger.info(f"Found {len(email_ids)} emails to process")
            
            for email_id in email_ids:
                email_data = self._fetch_email(mail, email_id)
                if email_data:
                    emails_list.append(email_data)
                    # Save to vault
                    self._save_email('inbox', email_data)
                    # Mark as read
                    mail.store(email_id, '+FLAGS', '\\Seen')
            
            mail.close()
            mail.logout()
            
            logger.info(f"✅ Received {len(emails_list)} emails")
            
        except imaplib.IMAP4.error as e:
            logger.error(f"❌ IMAP error: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Failed to receive emails: {str(e)}")
        
        return emails_list
    
    def _fetch_email(self, mail: imaplib.IMAP4_SSL, email_id: bytes) -> Optional[Dict[str, Any]]:
        """Fetch and parse a single email."""
        try:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            
            if status != 'OK':
                return None
            
            # Parse email
            raw_email = email.message_from_bytes(msg_data[0][1])
            
            # Get headers
            subject = self._decode_header(raw_email.get('Subject', ''))
            from_addr = self._decode_header(raw_email.get('From', ''))
            to_addr = self._decode_header(raw_email.get('To', ''))
            date_str = raw_email.get('Date', '')
            
            # Get body
            body = ""
            html_body = ""
            attachments = []
            
            for part in raw_email.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get_content_disposition())
                
                # Check for attachments
                if 'attachment' in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        attachments.append(filename)
                
                # Get text content
                if content_type == 'text/plain' and not body:
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        body = part.get_payload(decode=True).decode('latin-1', errors='ignore')
                
                # Get HTML content
                if content_type == 'text/html' and not html_body:
                    try:
                        html_body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        html_body = part.get_payload(decode=True).decode('latin-1', errors='ignore')
            
            # Use HTML if no plain text
            if not body and html_body:
                body = html_body
            
            return {
                'from': from_addr,
                'to': to_addr,
                'subject': subject,
                'body': body[:5000] if body else '',  # Limit body length
                'html': bool(html_body),
                'date': date_str,
                'timestamp': datetime.now().isoformat(),
                'attachments': attachments,
                'has_attachments': len(attachments) > 0
            }
            
        except Exception as e:
            logger.error(f"Error fetching email: {e}")
            return None
    
    def _decode_header(self, header: str) -> str:
        """Decode email header with encoding."""
        try:
            decoded = decode_header(header)
            result = ""
            for content, encoding in decoded:
                if isinstance(content, bytes):
                    result += content.decode(encoding or 'utf-8', errors='ignore')
                else:
                    result += content
            return result.strip()
        except:
            return header
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str):
        """Attach a file to email."""
        try:
            with open(file_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{os.path.basename(file_path)}"'
            )
            msg.attach(part)
        except Exception as e:
            logger.error(f"Error attaching file {file_path}: {e}")
    
    def _save_email(self, folder: str, email_data: Dict[str, Any]):
        """Save email to vault."""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        subject_safe = email_data['subject'].replace(' ', '_').replace('/', '_')[:50]
        
        if folder == 'inbox':
            filename = f"EMAIL_{email_data['from'].replace('@', '_')}_{subject_safe}_{timestamp}.md"
            save_dir = self.inbox_dir
        else:
            filename = f"EMAIL_SENT_{email_data['to'].replace('@', '_')}_{subject_safe}_{timestamp}.md"
            save_dir = self.sent_dir
        
        content = f"""# Email - {folder.upper()}

## Header
- **Subject:** {email_data['subject']}
- **From:** {email_data['from'] if 'from' in email_data else self.email_addr}
- **To:** {email_data.get('to', 'N/A')}
- **Date:** {email_data.get('date', email_data['timestamp'])}
- **Timestamp:** {email_data['timestamp']}

## Content

{email_data['body']}

## Metadata
- **Has Attachments:** {email_data.get('has_attachments', False)}
- **Attachments:** {', '.join(email_data.get('attachments', []))}
- **Format:** {'HTML' if email_data.get('html') else 'Plain Text'}

## Status
- [ ] Read
- [ ] Processed
- [ ] Archived

---
*Saved by Real Email Service*
"""
        
        try:
            with open(save_dir / filename, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.debug(f"Saved email to {save_dir / filename}")
        except Exception as e:
            logger.error(f"Error saving email: {e}")
    
    def test_connection(self) -> Dict[str, bool]:
        """Test SMTP and IMAP connections."""
        results = {
            'smtp': False,
            'imap': False
        }
        
        # Test SMTP
        try:
            if self.smtp_port == 465:
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
            server.login(self.email_addr, self.password)
            server.quit()
            results['smtp'] = True
            logger.info("✅ SMTP connection successful")
        except Exception as e:
            logger.error(f"❌ SMTP connection failed: {e}")
        
        # Test IMAP
        try:
            if self.imap_port == 993:
                mail = imaplib.IMAP4_SSL(self.imap_server)
            else:
                mail = imaplib.IMAP4(self.imap_server)
            mail.login(self.email_addr, self.password)
            mail.logout()
            results['imap'] = True
            logger.info("✅ IMAP connection successful")
        except Exception as e:
            logger.error(f"❌ IMAP connection failed: {e}")
        
        return results


# CLI Commands
def cmd_send(args):
    """Send email from CLI."""
    email_service = RealEmailService(
        os.getenv('GMAIL_ADDRESS', ''),
        os.getenv('GMAIL_APP_PASSWORD', ''),
        os.getenv('EMAIL_PROVIDER', 'gmail')
    )
    
    if not email_service.email_addr:
        print("❌ Error: Email address not configured. Set GMAIL_ADDRESS in .env")
        sys.exit(1)
    
    if not email_service.password:
        print("❌ Error: Email password not configured. Set GMAIL_APP_PASSWORD in .env")
        sys.exit(1)
    
    result = email_service.send_email(
        to=args.to,
        subject=args.subject,
        body=args.body,
        html=args.html,
        cc=args.cc,
        attachments=args.attachments
    )
    
    if result['status'] == 'success':
        print(f"✅ {result['message']}")
        print(f"   Subject: {result['subject']}")
        print(f"   Time: {result['timestamp']}")
    else:
        print(f"❌ {result['message']}")
        sys.exit(1)


def cmd_receive(args):
    """Receive emails from CLI."""
    email_service = RealEmailService(
        os.getenv('GMAIL_ADDRESS', ''),
        os.getenv('GMAIL_APP_PASSWORD', ''),
        os.getenv('EMAIL_PROVIDER', 'gmail')
    )
    
    if not email_service.email_addr:
        print("❌ Error: Email address not configured. Set GMAIL_ADDRESS in .env")
        sys.exit(1)
    
    print(f"📥 Checking emails for {email_service.email_addr}...")
    print()
    
    emails = email_service.receive_emails(
        limit=args.limit if hasattr(args, 'limit') else 10,
        unread_only=not (args.all if hasattr(args, 'all') else False)
    )
    
    if not emails:
        print("✅ No new emails!")
        return
    
    print(f"📬 Received {len(emails)} email(s):\n")
    
    for i, email_data in enumerate(emails, 1):
        print(f"{'='*60}")
        print(f"📧 Email #{i}")
        print(f"   From: {email_data['from']}")
        print(f"   Subject: {email_data['subject']}")
        print(f"   Date: {email_data['date']}")
        if email_data['has_attachments']:
            print(f"   Attachments: {', '.join(email_data['attachments'])}")
        print(f"\n   Preview:")
        print(f"   {'-'*50}")
        preview = email_data['body'][:300]
        print(f"   {preview}...")
        print(f"   {'-'*50}")
        print()
    
    print(f"✅ Emails saved to: {email_service.inbox_dir}")


def cmd_inbox(args):
    """Show inbox summary."""
    email_service = RealEmailService(
        os.getenv('GMAIL_ADDRESS', ''),
        os.getenv('GMAIL_APP_PASSWORD', ''),
        os.getenv('EMAIL_PROVIDER', 'gmail')
    )
    
    print(f"📬 Inbox for {email_service.email_addr}")
    print(f"   Location: {email_service.inbox_dir}")
    print()
    
    if email_service.inbox_dir.exists():
        emails = list(email_service.inbox_dir.glob("*.md"))
        emails.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if emails:
            print(f"Found {len(emails)} email(s):\n")
            for i, email_file in enumerate(emails[:20], 1):
                print(f"  {i}. {email_file.name}")
        else:
            print("📭 Inbox is empty")
    else:
        print("📭 Inbox directory does not exist yet")


def cmd_compose(args):
    """Interactive email compose."""
    email_service = RealEmailService(
        os.getenv('GMAIL_ADDRESS', ''),
        os.getenv('GMAIL_APP_PASSWORD', ''),
        os.getenv('EMAIL_PROVIDER', 'gmail')
    )
    
    if not email_service.email_addr:
        print("❌ Error: Email address not configured. Set GMAIL_ADDRESS in .env")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("📝 COMPOSE NEW EMAIL")
    print("="*60 + "\n")
    
    # Get recipient
    to = input("To: ").strip()
    if not to:
        print("❌ Recipient email is required")
        sys.exit(1)
    
    # Get CC (optional)
    cc = input("CC (optional): ").strip() or None
    
    # Get subject
    subject = input("Subject: ").strip()
    if not subject:
        print("❌ Subject is required")
        sys.exit(1)
    
    # Get body
    print("\nBody (end with empty line or type 'SEND' on a new line):")
    print("-" * 60)
    body_lines = []
    while True:
        line = input()
        if line.strip().upper() == 'SEND' or (not line and body_lines):
            break
        body_lines.append(line)
    
    body = '\n'.join(body_lines)
    
    # Confirm send
    print("\n" + "="*60)
    print("📧 EMAIL PREVIEW")
    print("="*60)
    print(f"To: {to}")
    if cc:
        print(f"CC: {cc}")
    print(f"Subject: {subject}")
    print(f"\nBody:\n{body[:500]}{'...' if len(body) > 500 else ''}")
    print("="*60)
    
    confirm = input("\nSend this email? (yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y']:
        result = email_service.send_email(
            to=to,
            subject=subject,
            body=body,
            cc=cc
        )
        
        if result['status'] == 'success':
            print(f"\n✅ Email sent successfully!")
        else:
            print(f"\n❌ Failed to send: {result['message']}")
            sys.exit(1)
    else:
        print("\n❌ Email cancelled")


def cmd_test(args):
    """Test email connection."""
    email_service = RealEmailService(
        os.getenv('GMAIL_ADDRESS', ''),
        os.getenv('GMAIL_APP_PASSWORD', ''),
        os.getenv('EMAIL_PROVIDER', 'gmail')
    )
    
    print("\n🔧 Testing Email Connection")
    print("="*60)
    print(f"Email: {email_service.email_addr}")
    print(f"Provider: {email_service.provider}")
    print(f"SMTP: {email_service.smtp_server}:{email_service.smtp_port}")
    print(f"IMAP: {email_service.imap_server}:{email_service.imap_port}")
    print("="*60 + "\n")
    
    results = email_service.test_connection()
    
    print("\n" + "="*60)
    print("RESULTS:")
    print(f"  SMTP (Send): {'✅ Connected' if results['smtp'] else '❌ Failed'}")
    print(f"  IMAP (Receive): {'✅ Connected' if results['imap'] else '❌ Failed'}")
    print("="*60)
    
    if results['smtp'] and results['imap']:
        print("\n✅ All connections successful!")
    else:
        print("\n⚠️  Some connections failed. Check your credentials.")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Real Email Service CLI")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Send command
    send_parser = subparsers.add_parser('send', help='Send an email')
    send_parser.add_argument('--to', required=True, help='Recipient email')
    send_parser.add_argument('--subject', required=True, help='Email subject')
    send_parser.add_argument('--body', required=True, help='Email body')
    send_parser.add_argument('--html', action='store_true', help='Send as HTML')
    send_parser.add_argument('--cc', help='CC recipients')
    send_parser.add_argument('--attachments', nargs='*', help='Attachments')
    send_parser.set_defaults(func=cmd_send)
    
    # Receive command
    recv_parser = subparsers.add_parser('receive', help='Receive emails')
    recv_parser.add_argument('--limit', type=int, default=10, help='Max emails')
    recv_parser.add_argument('--all', action='store_true', help='Include read')
    recv_parser.set_defaults(func=cmd_receive)
    
    # Inbox command
    inbox_parser = subparsers.add_parser('inbox', help='Show inbox')
    inbox_parser.set_defaults(func=cmd_inbox)
    
    # Compose command
    compose_parser = subparsers.add_parser('compose', help='Compose email')
    compose_parser.set_defaults(func=cmd_compose)
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test connection')
    test_parser.set_defaults(func=cmd_test)
    
    args = parser.parse_args()
    
    if args.command:
        args.func(args)
    else:
        parser.print_help()
