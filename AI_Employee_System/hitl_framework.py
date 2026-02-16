"""
HUMAN-IN-THE-LOOP (HITL) FRAMEWORK
═══════════════════════════════════════════════════════════════════════════

Advanced pattern for human control over AI actions.

Provides multiple intervention points where Claude must pause and ask 
for human confirmation before proceeding.

Types of Human Intervention:
1. APPROVAL     - Yes/No decision on specific action
2. CONFIRMATION - "Did you really mean this?"
3. REVIEW       - Detailed review of output before execution
4. GUIDANCE     - Ask human for additional info/direction
5. ESCALATION   - Route to specific person for decision
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime


class InterventionType(Enum):
    """Types of human intervention points."""
    APPROVAL = "approval"           # Yes/No decision
    CONFIRMATION = "confirmation"  # "Are you sure?"
    REVIEW = "review"              # Detailed review
    GUIDANCE = "guidance"          # Need human input
    ESCALATION = "escalation"      # Route to specific person


class InterventionLevel(Enum):
    """Risk level affecting intervention"""
    LOW = "low"              # Automatic, minimal review
    MEDIUM = "medium"        # Review required
    HIGH = "high"            # Explicit approval needed
    CRITICAL = "critical"    # Must escalate


class RiskAssessment(Enum):
    """How risky is this action?"""
    SAFE = "safe"                    # No risk (read-only)
    LOW_RISK = "low_risk"            # Minor impact
    MEDIUM_RISK = "medium_risk"      # Significant impact
    HIGH_RISK = "high_risk"          # Major impact (payment, delete)
    CRITICAL_RISK = "critical_risk"  # Company-threatening


@dataclass
class InterventionPoint:
    """Represents a point where human is needed."""
    intervention_id: str
    intervention_type: InterventionType
    level: InterventionLevel
    risk_assessment: RiskAssessment
    title: str
    description: str
    action_details: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # Resolution fields
    status: str = "pending"  # pending, approved, rejected, escalated
    resolved_by: Optional[str] = None
    resolution_time: Optional[str] = None
    resolution_notes: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'intervention_id': self.intervention_id,
            'intervention_type': self.intervention_type.value,
            'level': self.level.value,
            'risk_assessment': self.risk_assessment.value,
            'title': self.title,
            'description': self.description,
            'action_details': self.action_details,
            'timestamp': self.timestamp,
            'status': self.status,
            'resolved_by': self.resolved_by,
            'resolution_time': self.resolution_time,
            'resolution_notes': self.resolution_notes,
        }


@dataclass
class HITLConfig:
    """Configuration for HITL behavior."""
    # Which operations require what level of review
    require_review_on_send_email: bool = True
    require_review_on_payment: bool = True
    require_review_on_delete: bool = True
    require_review_on_form_submit: bool = True
    
    # Risk thresholds
    auto_approve_below_risk: RiskAssessment = RiskAssessment.LOW_RISK
    escalate_above_risk: RiskAssessment = RiskAssessment.HIGH_RISK
    
    # Escalation rules
    escalate_large_payments_to: str = "finance_manager"
    escalate_critical_to: str = "ceo"
    
    # Timing
    approval_timeout_minutes: int = 60
    reminder_interval_minutes: int = 15
    
    # Logging
    log_all_interventions: bool = True
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'require_review_on_send_email': self.require_review_on_send_email,
            'require_review_on_payment': self.require_review_on_payment,
            'require_review_on_delete': self.require_review_on_delete,
            'require_review_on_form_submit': self.require_review_on_form_submit,
            'auto_approve_below_risk': self.auto_approve_below_risk.value,
            'escalate_above_risk': self.escalate_above_risk.value,
            'escalate_large_payments_to': self.escalate_large_payments_to,
            'escalate_critical_to': self.escalate_critical_to,
            'approval_timeout_minutes': self.approval_timeout_minutes,
            'reminder_interval_minutes': self.reminder_interval_minutes,
            'log_all_interventions': self.log_all_interventions,
        }


class HITLFramework:
    """Human-in-the-Loop framework for controlling AI actions."""
    
    def __init__(self, vault_path: Path, config: Optional[HITLConfig] = None):
        """Initialize HITL framework."""
        self.vault_path = Path(vault_path)
        self.config = config or HITLConfig()
        
        self.logger = logging.getLogger("HITL")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Storage
        self.interventions_dir = vault_path / "System" / "interventions"
        self.interventions_dir.mkdir(parents=True, exist_ok=True)
        
        # Track current interventions
        self.pending_interventions: Dict[str, InterventionPoint] = {}
    
    def assess_risk(self, action_type: str, params: Dict[str, Any]) -> RiskAssessment:
        """
        Assess the risk level of an action.
        
        Args:
            action_type: Type of action (send_email, process_payment, etc.)
            params: Action parameters
        
        Returns:
            Risk assessment level
        """
        # Read-only = safe
        read_only_actions = {
            'read_file', 'list_directory', 'get_event', 'search_emails',
            'get_page_content', 'check_approval_status'
        }
        
        if action_type in read_only_actions:
            return RiskAssessment.SAFE
        
        # Email = medium risk
        if action_type == 'send_email':
            return RiskAssessment.MEDIUM_RISK
        
        # Payment = high risk (scale by amount)
        if action_type == 'process_payment':
            amount = params.get('amount', 0)
            if amount > 10000:  # > $10k = critical
                return RiskAssessment.CRITICAL_RISK
            elif amount > 1000:  # > $1k = high risk
                return RiskAssessment.HIGH_RISK
            else:
                return RiskAssessment.MEDIUM_RISK
        
        # Delete = high risk
        if action_type in ['delete_file', 'delete_event', 'delete_calendar']:
            return RiskAssessment.HIGH_RISK
        
        # Form submission = medium-high risk
        if action_type == 'fill_and_submit_form':
            return RiskAssessment.HIGH_RISK
        
        # Default to medium
        return RiskAssessment.MEDIUM_RISK
    
    def determine_intervention_level(self, risk: RiskAssessment) -> InterventionLevel:
        """Determine intervention level based on risk."""
        mapping = {
            RiskAssessment.SAFE: InterventionLevel.LOW,
            RiskAssessment.LOW_RISK: InterventionLevel.MEDIUM,
            RiskAssessment.MEDIUM_RISK: InterventionLevel.HIGH,
            RiskAssessment.HIGH_RISK: InterventionLevel.CRITICAL,
            RiskAssessment.CRITICAL_RISK: InterventionLevel.CRITICAL,
        }
        return mapping.get(risk, InterventionLevel.MEDIUM)
    
    def request_intervention(
        self,
        action_type: str,
        title: str,
        description: str,
        action_details: Dict[str, Any],
        intervention_type: InterventionType = InterventionType.APPROVAL
    ) -> InterventionPoint:
        """
        Request human intervention for an action.
        
        Args:
            action_type: Type of action
            title: Human-readable title
            description: What the action will do
            action_details: Details of the action
            intervention_type: Type of intervention needed
        
        Returns:
            InterventionPoint object
        """
        # Assess risk
        risk = self.assess_risk(action_type, action_details)
        level = self.determine_intervention_level(risk)
        
        # Create intervention point
        intervention_id = f"HITL_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        intervention = InterventionPoint(
            intervention_id=intervention_id,
            intervention_type=intervention_type,
            level=level,
            risk_assessment=risk,
            title=title,
            description=description,
            action_details=action_details,
        )
        
        # Determine if auto-approval is possible
        if risk.value <= self.config.auto_approve_below_risk.value:
            intervention.status = "auto_approved"
            self.logger.info(f"✅ Auto-approved (low risk): {intervention_id}")
            return intervention
        
        # Determine if escalation is needed
        if risk.value >= self.config.escalate_above_risk.value:
            intervention.level = InterventionLevel.CRITICAL
            self.logger.warning(f"⚠️  Escalation needed: {intervention_id}")
        
        # Save intervention
        self._save_intervention(intervention)
        self.pending_interventions[intervention_id] = intervention
        
        self.logger.info(f"📋 Intervention requested: {intervention_id}")
        return intervention
    
    def _save_intervention(self, intervention: InterventionPoint):
        """Save intervention to vault."""
        try:
            file_path = self.interventions_dir / f"{intervention.intervention_id}.json"
            
            with open(file_path, 'w') as f:
                json.dump(intervention.to_dict(), f, indent=2)
            
            # Also create markdown for human review
            self._create_intervention_markdown(intervention)
            
        except Exception as e:
            self.logger.error(f"Could not save intervention: {e}")
    
    def _create_intervention_markdown(self, intervention: InterventionPoint):
        """Create markdown file for human review."""
        try:
            md_path = self.vault_path / "Pending_Review" / f"{intervention.intervention_id}.md"
            md_path.parent.mkdir(parents=True, exist_ok=True)
            
            content = f"""# {intervention.intervention_type.value.upper()}: {intervention.title}

**Intervention ID:** {intervention.intervention_id}
**Level:** {intervention.level.value.upper()}
**Risk:** {intervention.risk_assessment.value.upper()}
**Timestamp:** {intervention.timestamp}

## Description

{intervention.description}

## Action Details

```json
{json.dumps(intervention.action_details, indent=2)}
```

## Type

{intervention.intervention_type.value}

## Your Decision

- [ ] Approve
- [ ] Reject
- [ ] Request Changes

## Notes

Add your notes or required changes here.
"""
            
            md_path.write_text(content)
            self.logger.info(f"📝 Intervention markdown saved: {md_path}")
            
        except Exception as e:
            self.logger.error(f"Could not create intervention markdown: {e}")
    
    def approve_intervention(self, intervention_id: str, notes: str = "") -> bool:
        """
        Approve an intervention.
        
        Args:
            intervention_id: ID of the intervention
            notes: Optional approval notes
        
        Returns:
            True if approved successfully
        """
        intervention = self.pending_interventions.get(intervention_id)
        
        if not intervention:
            self.logger.warning(f"Intervention not found: {intervention_id}")
            return False
        
        intervention.status = "approved"
        intervention.resolved_by = "human_user"
        intervention.resolution_time = datetime.now().isoformat()
        intervention.resolution_notes = notes
        
        self._save_intervention(intervention)
        
        # Move markdown to Approved folder
        self._move_intervention_file(intervention_id, "Approved")
        
        self.logger.info(f"✅ Approved: {intervention_id}")
        return True
    
    def reject_intervention(self, intervention_id: str, reason: str = "") -> bool:
        """
        Reject an intervention.
        
        Args:
            intervention_id: ID of the intervention
            reason: Reason for rejection
        
        Returns:
            True if rejected successfully
        """
        intervention = self.pending_interventions.get(intervention_id)
        
        if not intervention:
            self.logger.warning(f"Intervention not found: {intervention_id}")
            return False
        
        intervention.status = "rejected"
        intervention.resolved_by = "human_user"
        intervention.resolution_time = datetime.now().isoformat()
        intervention.resolution_notes = f"Rejected: {reason}"
        
        self._save_intervention(intervention)
        
        # Move markdown to Rejected folder
        self._move_intervention_file(intervention_id, "Rejected")
        
        self.logger.info(f"❌ Rejected: {intervention_id}")
        return True
    
    def request_guidance(self, intervention_id: str, guidance: str) -> bool:
        """
        Request guidance or modification for an intervention.
        
        Args:
            intervention_id: ID of the intervention
            guidance: Guidance or modification request
        
        Returns:
            True if guidance saved
        """
        intervention = self.pending_interventions.get(intervention_id)
        
        if not intervention:
            return False
        
        intervention.status = "awaiting_changes"
        intervention.resolution_notes = guidance
        
        self._save_intervention(intervention)
        self.logger.info(f"📝 Guidance added: {intervention_id}")
        
        return True
    
    def _move_intervention_file(self, intervention_id: str, folder: str):
        """Move intervention markdown to decision folder."""
        try:
            source = self.vault_path / "Pending_Review" / f"{intervention_id}.md"
            dest = self.vault_path / folder / f"{intervention_id}.md"
            
            if source.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                source.rename(dest)
        except Exception as e:
            self.logger.error(f"Could not move intervention file: {e}")
    
    def get_pending_interventions(self) -> List[InterventionPoint]:
        """Get all pending interventions."""
        pending = []
        
        try:
            pending_review_dir = self.vault_path / "Pending_Review"
            
            if pending_review_dir.exists():
                for json_file in pending_review_dir.glob("HITL_*.json"):
                    try:
                        with open(json_file, 'r') as f:
                            data = json.load(f)
                            intervention = InterventionPoint(**data)
                            pending.append(intervention)
                    except Exception as e:
                        self.logger.error(f"Could not load intervention: {e}")
        
        except Exception as e:
            self.logger.error(f"Could not get pending: {e}")
        
        return sorted(pending, key=lambda x: x.timestamp)
    
    def get_intervention_status(self, intervention_id: str) -> Optional[str]:
        """Get the status of an intervention."""
        intervention = self.pending_interventions.get(intervention_id)
        
        if not intervention:
            # Try to load from disk
            json_file = self.interventions_dir / f"{intervention_id}.json"
            
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    return data.get('status')
            except Exception:
                return None
        
        return intervention.status
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get HITL statistics."""
        try:
            all_interventions = []
            
            # Load from all folders
            for folder in ['Pending_Review', 'Approved', 'Rejected']:
                folder_path = self.vault_path / folder
                if folder_path.exists():
                    for md_file in folder_path.glob("HITL_*.md"):
                        # Count by status
                        all_interventions.append(md_file.stem)
            
            pending = self.get_pending_interventions()
            
            return {
                'total_interventions': len(all_interventions),
                'pending': len(pending),
                'approved': len(list((self.vault_path / "Approved").glob("HITL_*.md"))) if (self.vault_path / "Approved").exists() else 0,
                'rejected': len(list((self.vault_path / "Rejected").glob("HITL_*.md"))) if (self.vault_path / "Rejected").exists() else 0,
            }
        except Exception as e:
            self.logger.error(f"Could not get statistics: {e}")
            return {}
    
    def batch_approve(self, approval_ids: List[str], notes: str = "") -> int:
        """
        Approve multiple interventions at once.
        
        Args:
            approval_ids: List of intervention IDs
            notes: Notes for all approvals
        
        Returns:
            Number of successful approvals
        """
        count = 0
        for approval_id in approval_ids:
            if self.approve_intervention(approval_id, notes):
                count += 1
        
        return count
    
    def load_config(self, config_file: Path) -> HITLConfig:
        """Load HITL config from file."""
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
                
                # Convert string enums back to enums
                if 'auto_approve_below_risk' in data:
                    data['auto_approve_below_risk'] = RiskAssessment(data['auto_approve_below_risk'])
                if 'escalate_above_risk' in data:
                    data['escalate_above_risk'] = RiskAssessment(data['escalate_above_risk'])
                
                self.config = HITLConfig(**data)
                self.logger.info(f"✅ Loaded config: {config_file}")
                return self.config
        except Exception as e:
            self.logger.error(f"Could not load config: {e}")
            return self.config
    
    def save_config(self, config_file: Path):
        """Save HITL config to file."""
        try:
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_file, 'w') as f:
                json.dump(self.config.to_dict(), f, indent=2)
            
            self.logger.info(f"✅ Saved config: {config_file}")
        except Exception as e:
            self.logger.error(f"Could not save config: {e}")


# Demo / Testing
if __name__ == "__main__":
    import sys
    
    vault_path = Path("./Vault")
    hitl = HITLFramework(vault_path)
    
    print("\n" + "="*70)
    print("HUMAN-IN-THE-LOOP FRAMEWORK - Demo")
    print("="*70 + "\n")
    
    # Example 1: Low-risk action (auto-approved)
    print("Example 1: Read file (low risk - auto-approved)")
    intervention = hitl.request_intervention(
        action_type='read_file',
        title='Read Vault Contents',
        description='Read files from vault',
        action_details={'path': 'Inbox/'}
    )
    print(f"Status: {intervention.status}\n")
    
    # Example 2: Medium-risk action (needs review)
    print("Example 2: Send email (medium risk - needs approval)")
    intervention = hitl.request_intervention(
        action_type='send_email',
        title='Send Invoice to Client',
        description='Send invoice payment reminder to John Smith',
        action_details={
            'to': 'john@example.com',
            'subject': 'Invoice Payment Reminder',
            'body': 'Your invoice is due...'
        }
    )
    print(f"Status: {intervention.status}")
    print(f"Level: {intervention.level.value}")
    print(f"Intervention ID: {intervention.intervention_id}\n")
    
    # Example 3: High-risk action (needs escalation)
    print("Example 3: Large payment (critical risk - needs escalation)")
    intervention = hitl.request_intervention(
        action_type='process_payment',
        title='Process Payment to Vendor',
        description='Process payment of $15,000 to vendor',
        action_details={
            'vendor': 'Acme Corp',
            'amount': 15000,
            'invoice_id': 'INV-001'
        }
    )
    print(f"Status: {intervention.status}")
    print(f"Level: {intervention.level.value}")
    print(f"Risk: {intervention.risk_assessment.value}\n")
    
    # Stats
    stats = hitl.get_statistics()
    print("Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
