"""
EMAIL SYSTEM INTEGRATION
═══════════════════════════════════════════════════════════════════════════

Integrates email processing with Gmail watcher and system orchestrator.
Provides unified email handling across the AI Employee system.

Features:
- Gmail watcher integration
- Automatic email categorization
- Response generation
- Approval workflow integration
- Complete audit logging
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EmailIntegrationConfig:
    """Configuration for email integration."""
    vault_path: Path
    auto_respond: bool = False
    auto_categorize: bool = True
    require_approval_for_responses: bool = True
    archive_after_days: int = 30
    log_all_interactions: bool = True


class EmailIntegrationBridge:
    """
    Bridges email processing with system orchestrator.
    
    Coordinates:
    - Gmail watcher input
    - Email processor logic
    - HITL approval for responses
    - Audit logging
    - Integration with orchestrator
    """
    
    def __init__(
        self,
        config: EmailIntegrationConfig,
        email_processor=None,
        hitl_framework=None,
        system_orchestrator=None
    ):
        self.config = config
        self.email_processor = email_processor
        self.hitl_framework = hitl_framework
        self.orchestrator = system_orchestrator
        
        # Initialize logger
        self.logger = logging.getLogger('EmailIntegration')
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging."""
        log_dir = self.config.vault_path / "System" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        handler = logging.FileHandler(log_dir / "email_integration.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def handle_gmail_message(
        self,
        message_id: str,
        sender: str,
        recipient: str,
        subject: str,
        body: str,
        is_important: bool = False
    ) -> Dict:
        """
        Handle incoming Gmail message from watcher.
        
        Args:
            message_id: Gmail message ID
            sender: From address
            recipient: To address
            subject: Email subject
            body: Email body
            is_important: Whether marked as important/starred
        
        Returns:
            Processing result
        """
        
        try:
            self.logger.info(f"Handling Gmail message {message_id} from {sender}")
            
            # Determine if action required
            requires_action = self._should_require_action(subject, body, is_important)
            requires_approval = self._should_require_approval(subject, body)
            
            # Process email
            if self.email_processor:
                result = self.email_processor.process_email(
                    email_id=message_id,
                    from_address=sender,
                    to_address=recipient,
                    subject=subject,
                    body=body,
                    requires_action=requires_action,
                    requires_approval=requires_approval
                )
            else:
                result = {
                    "success": False,
                    "error": "Email processor not initialized"
                }
            
            # If response needed and approved, generate response
            if result["success"] and self._should_respond(subject, body):
                response_result = self._generate_and_send_response(
                    message_id,
                    sender,
                    subject
                )
                result["response"] = response_result
            
            return result
        
        except Exception as e:
            self.logger.error(f"Error handling Gmail message {message_id}: {e}")
            
            if self.orchestrator:
                self.orchestrator.handle_component_error(
                    "email_integration",
                    e,
                    {"message_id": message_id},
                    "ERROR"
                )
            
            return {
                "success": False,
                "error": str(e)
            }
    
    def _should_require_action(self, subject: str, body: str, is_important: bool) -> bool:
        """Determine if email requires action."""
        keywords = ["action", "urgent", "asap", "need", "please", "required", "approval"]
        text = f"{subject} {body}".lower()
        
        return is_important or any(kw in text for kw in keywords)
    
    def _should_require_approval(self, subject: str, body: str) -> bool:
        """Determine if response requires approval."""
        keywords = ["financial", "payment", "contract", "agreement", "sensitive"]
        text = f"{subject} {body}".lower()
        
        return any(kw in text for kw in keywords)
    
    def _should_respond(self, subject: str, body: str) -> bool:
        """Determine if automatic response should be sent."""
        no_response_keywords = ["confirm", "delivered", "read", "auto-reply"]
        text = f"{subject} {body}".lower()
        
        return not any(kw in text for kw in no_response_keywords) and self.config.auto_respond
    
    def _generate_and_send_response(
        self,
        message_id: str,
        to_address: str,
        original_subject: str
    ) -> Dict:
        """Generate and send email response."""
        
        try:
            # Generate response
            response_subject = f"Re: {original_subject}"
            response_body = self._generate_response_text(original_subject)
            
            # Request approval if needed
            if self.config.require_approval_for_responses and self.hitl_framework:
                approval_result = self.hitl_framework.request_approval(
                    title=f"Email Response Approval: {original_subject}",
                    description=response_body,
                    risk_level="medium",
                    action="send_email_response"
                )
                
                if not approval_result.get("approved"):
                    self.logger.info(f"Email response pending approval: {message_id}")
                    return {
                        "status": "pending_approval",
                        "message_id": message_id
                    }
            
            # Send response
            if self.email_processor:
                self.email_processor.send_response(
                    message_id,
                    to_address,
                    response_subject,
                    response_body
                )
            
            self.logger.info(f"Response sent to {to_address}")
            
            return {
                "status": "sent",
                "to": to_address,
                "subject": response_subject
            }
        
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _generate_response_text(self, subject: str) -> str:
        """Generate automatic response text."""
        
        responses = {
            "inquiry": "Thank you for your inquiry. We'll review and get back to you shortly.",
            "support": "Thank you for contacting support. Your request has been received and prioritized.",
            "follow": "Thank you for following up. We appreciate your interest.",
            "default": "Thank you for your email. We have received it and will respond shortly."
        }
        
        subject_lower = subject.lower()
        
        for keyword, response in responses.items():
            if keyword in subject_lower:
                return response
        
        return responses["default"]
    
    def get_email_dashboard(self) -> Dict:
        """Get email system dashboard data."""
        
        dashboard = {
            "timestamp": datetime.now().isoformat(),
            "status": "active",
            "stats": {}
        }
        
        if self.email_processor:
            dashboard["stats"] = self.email_processor.get_stats()
        
        return dashboard
    
    def save_email_logs(self) -> Path:
        """Save email processing logs."""
        
        logs_file = self.config.vault_path / "System" / "email_logs" / "summary.json"
        logs_file.parent.mkdir(parents=True, exist_ok=True)
        
        dashboard = self.get_email_dashboard()
        logs_file.write_text(json.dumps(dashboard, indent=2))
        
        self.logger.info(f"Email logs saved to {logs_file}")
        return logs_file


class EmailWatcherIntegration:
    """
    Integration point for Gmail watcher.
    Use this to hook gmail_watcher into email processor.
    """
    
    def __init__(self, email_bridge: EmailIntegrationBridge):
        self.email_bridge = email_bridge
    
    def on_new_message(
        self,
        message_id: str,
        sender: str,
        recipient: str,
        subject: str,
        body: str,
        labels: List[str] = None
    ) -> Dict:
        """Called when Gmail watcher detects new message."""
        
        is_important = labels and "IMPORTANT" in labels
        
        return self.email_bridge.handle_gmail_message(
            message_id=message_id,
            sender=sender,
            recipient=recipient,
            subject=subject,
            body=body,
            is_important=is_important
        )


def create_email_integration(
    vault_path: Path,
    email_processor=None,
    hitl_framework=None,
    system_orchestrator=None
) -> EmailIntegrationBridge:
    """Factory function to create email integration."""
    
    config = EmailIntegrationConfig(
        vault_path=vault_path,
        auto_respond=True,
        auto_categorize=True,
        require_approval_for_responses=True
    )
    
    return EmailIntegrationBridge(
        config=config,
        email_processor=email_processor,
        hitl_framework=hitl_framework,
        system_orchestrator=system_orchestrator
    )


# Example setup
if __name__ == "__main__":
    from pathlib import Path
    from email_processor import EmailProcessor
    
    vault_path = Path("./Vault")
    
    # Initialize components
    email_processor = EmailProcessor(vault_path)
    
    # Create integration
    email_integration = create_email_integration(
        vault_path=vault_path,
        email_processor=email_processor
    )
    
    # Test: Simulate Gmail watcher input
    watcher_integration = EmailWatcherIntegration(email_integration)
    
    result = watcher_integration.on_new_message(
        message_id="gmail_msg_12345",
        sender="client@example.com",
        recipient="info@company.com",
        subject="Urgent: Need assistance with pricing",
        body="Hi, I need help with your pricing model. When can we discuss?",
        labels=["INBOX", "IMPORTANT"]
    )
    
    print(f"✓ Email handled: {result}")
    print(f"✓ Dashboard: {email_integration.get_email_dashboard()}")
    
    # Save logs
    email_integration.save_email_logs()
