"""
Integration workflow engine for Personal AI Employee
Handles event-driven operations across multiple external services (Gmail, WhatsApp,
LinkedIn, Facebook) with tier-based gating.

The watchers/posters already collect and store credentials; this module reads user
settings, checks the tier, and drives high-level actions such as auto-posting,
notifications, and cross-channel automation.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

from auth_db import db
from AI_Employee_System.Watchers.gmail_watcher import GmailWatcher
from AI_Employee_System.Watchers.whatsapp_watcher import WhatsAppWatcher
from AI_Employee_System.Watchers.linkedin_poster import LinkedInPoster
from AI_Employee_System.Watchers.facebook_poster import FacebookPoster


class IntegrationWorkflow:
    """Primary workflow class.  Instantiate with a user id.

    Use :py:meth:`run` to perform regularly scheduled processing (e.g. from
    system_orchestrator) or call individual handlers in response to an event.
    """

    def __init__(self, user_id: int):
        self.user = db.get_user_by_id(user_id)
        if not self.user:
            raise ValueError(f"No user with id {user_id}")
        self.tier = self.user['tier'] or 'bronze'
        self.integrations = db.get_user_integrations(user_id)

        # instantiate clients according to tier and configuration
        self.gmail = None
        if 'gmail' in self.integrations and self.tier in ['bronze','silver','gold','platinum']:
            cfg = self.integrations['gmail']
            self.gmail = GmailWatcher(
                email_addr=cfg.get('email',''),
                app_password=cfg.get('app_password',''),
                vault_path=os.path.join(os.getcwd(), 'vault'),
                user_tier=self.tier
            )

        self.whatsapp = None
        if 'whatsapp' in self.integrations and self.tier in ['bronze','silver','gold','platinum']:
            self.whatsapp = WhatsAppWatcher(vault_path=os.path.join(os.getcwd(), 'vault'), user_tier=self.tier)

        self.linkedin = None
        if 'linkedin' in self.integrations and self.tier in ['silver','gold','platinum']:
            cfg = self.integrations['linkedin']
            self.linkedin = LinkedInPoster(access_token=cfg.get('token',''),
                                           business_profile_id=cfg.get('profile_id',''),
                                           user_tier=self.tier)

        self.facebook = None
        if 'facebook' in self.integrations and self.tier in ['gold','platinum']:
            cfg = self.integrations['facebook']
            self.facebook = FacebookPoster(vault_path=os.path.join(os.getcwd(), 'vault'),
                                           user_tier=self.tier)

    def run(self):
        """Periodic scan that can be invoked from a scheduler.

        - check new email messages and route them
        - look for vault items flagged for social posting
        - send WhatsApp notifications for payments or security alerts
        """
        if self.gmail:
            # the watcher already writes to vault; this example also could trigger
            # a LinkedIn summary once per day, for silver+ users.
            self.gmail.check_new_emails()

        if self.linkedin:
            # placeholder: generate a daily update based on vault stats
            stats = self._gather_vault_stats()
            if stats:
                content = self.linkedin.generate_daily_update(stats)
                post = self.linkedin.create_post(content)
                self.linkedin.publish_post(post['post_id'])

        # extend with more workflows as needed

    def _gather_vault_stats(self) -> Dict[str, Any]:
        """Scan the vault for simple counts (needs more sophisticated parsing)."""
        try:
            vault_dir = Path('vault')
            needs = len(list(vault_dir.glob('Inbox/*.md')))
            return {'emails_processed': needs}
        except Exception:
            return {}

    # convenience hooks which can be called externally by watchers/orchestrator
    def on_email_received(self, email_data: Dict[str, Any]):
        """Process an individual email event."""
        # for gold/platinum we might send a WhatsApp alert
        if self.whatsapp:
            # code to send notification using another helper module
            pass

    def on_payment_received(self, payment_info: Dict[str, Any]):
        """Workflow when a payment is received."""
        if self.whatsapp:
            # send immediate WhatsApp payment alert
            pass
