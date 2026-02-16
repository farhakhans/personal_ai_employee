"""
Configuration file for Personal AI Employee System
"""

from pathlib import Path
from datetime import datetime

# Project paths
PROJECT_ROOT = Path(__file__).parent
VAULT_PATH = PROJECT_ROOT / "vault"
SCRIPTS_PATH = PROJECT_ROOT / "Vault_Scripts"

# Vault folder paths
VAULT_SUBFOLDERS = {
    "needs_action": VAULT_PATH / "Needs_Action",
    "pending_approval": VAULT_PATH / "Pending_Approval",
    "approved": VAULT_PATH / "Approved",
    "done": VAULT_PATH / "Done",
    "plans": VAULT_PATH / "Plans"
}

# System configuration
SYSTEM_CONFIG = {
    "ai_name": "Personal AI Employee",
    "version": "1.0.0",
    "created_date": "2026-02-15",
    "timezone": "UTC",
    "check_interval_seconds": 300,  # Check every 5 minutes
}

# Business rules
BUSINESS_RULES = {
    "require_approval_for_payment": True,
    "min_approval_amount": 100,
    "max_daily_spending": 5000,
    "task_priority_levels": ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
    "default_task_priority": "MEDIUM"
}

# Approval rules
APPROVAL_RULES = {
    "payment_approval_required": True,
    "urgent_notification_threshold_hours": 2,
    "auto_approve_below_amount": 50
}

# Logging configuration
LOGGING_CONFIG = {
    "log_file": PROJECT_ROOT / "system_logs.txt",
    "log_level": "INFO",
    "max_log_size_mb": 10,
    "backup_logs": True
}

# Dashboard configuration
DASHBOARD_CONFIG = {
    "recent_activity_count": 10,
    "show_pending_approvals": True,
    "show_active_projects": True,
    "refresh_interval_seconds": 60
}
