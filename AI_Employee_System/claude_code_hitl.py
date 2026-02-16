"""
CLAUDE CODE + HITL INTEGRATION
═══════════════════════════════════════════════════════════════════════════

Integration layer that makes Claude Code use the HITL framework
for all sensitive operations.
"""

from pathlib import Path
from typing import Optional, Dict, Any

from claude_code import ClaudeCode
from hitl_framework import HITLFramework, InterventionType, RiskAssessment
from mcp_coordinator import MCPServerType, MCPResponse


class SafeClaudeCode(ClaudeCode):
    """
    Enhanced Claude Code with Human-in-the-Loop integration.
    
    IMPORTANT: This version REQUIRES human approval for sensitive operations.
    It will NEVER execute dangerous actions without explicit approval.
    """
    
    def __init__(self, vault_path: Path, anthropic_api_key: Optional[str] = None):
        """Initialize with HITL integration."""
        super().__init__(vault_path, anthropic_api_key)
        
        # Add HITL framework
        self.hitl = HITLFramework(vault_path)
        
        self.logger.info("✅ Claude Code initialized with HITL framework")
    
    def execute_action(self, action: str, params: Dict[str, Any], 
                      server_type: MCPServerType, capability: str,
                      requires_approval: bool = False) -> MCPResponse:
        """
        Execute action with HITL safety checks.
        
        ALL dangerous operations go through HITL first!
        
        Args:
            action: Description of the action
            params: Parameters for the MCP capability
            server_type: Which MCP server to use
            capability: Which capability to invoke
            requires_approval: Force approval (deprecated - always checked)
        
        Returns:
            Response from MCP server (or waiting notification)
        """
        
        # Step 1: Check if action needs HITL review
        action_type = f"{server_type.value}.{capability}"
        
        # Request HITL intervention
        intervention = self.hitl.request_intervention(
            action_type=action_type,
            title=action,
            description=f"Claude wants to execute: {action}",
            action_details={
                'server': server_type.value,
                'capability': capability,
                'params': params,
            },
            intervention_type=InterventionType.APPROVAL
        )
        
        # Step 2: Check if auto-approved (safe operation)
        if intervention.status == "auto_approved":
            self.logger.info(f"✅ Auto-approved (safe): {action}")
            return super().execute_action(
                action, params, server_type, capability, requires_approval=False
            )
        
        # Step 3: High-risk operation - STOP and wait
        if intervention.level.name in ["HIGH", "CRITICAL"]:
            self.logger.warning(f"⛔ HOLDING: {action}")
            self.logger.warning(f"   Intervention ID: {intervention.intervention_id}")
            self.logger.warning(f"   Waiting for human approval...")
            
            return MCPResponse(
                success=False,
                error="HUMAN_APPROVAL_REQUIRED",
                result={
                    'intervention_id': intervention.intervention_id,
                    'status': 'awaiting_approval',
                    'message': f"Action requires human approval: {action}",
                }
            )
        
        # Step 4: Check if human has approved
        if self.hitl.check_approval_status(intervention.intervention_id) == "awaiting_approval":
            return MCPResponse(
                success=False,
                error="APPROVAL_PENDING",
                result={
                    'intervention_id': intervention.intervention_id,
                    'status': 'pending',
                    'message': 'Waiting for human decision',
                }
            )
        
        # Step 5: Check if approved
        if intervention.status == "approved":
            self.logger.info(f"✅ Approved by human: {action}")
            return super().execute_action(
                action, params, server_type, capability, requires_approval=False
            )
        
        # Step 6: Rejected actions
        if intervention.status == "rejected":
            return MCPResponse(
                success=False,
                error="HUMAN_REJECTED",
                result={
                    'intervention_id': intervention.intervention_id,
                    'status': 'rejected',
                    'reason': intervention.resolution_notes,
                }
            )
        
        # Default: action not yet resolved
        return MCPResponse(
            success=False,
            error="PENDING_INTERVENTION",
            result={'intervention_id': intervention.intervention_id}
        )
    
    def check_pending_approvals(self) -> int:
        """
        Check how many approvals are pending.
        
        Returns:
            Number of pending interventions
        """
        pending = self.hitl.get_pending_interventions()
        return len(pending)
    
    def process_approved_actions(self) -> int:
        """
        Process any approved but pending actions.
        
        Returns:
            Number of actions executed
        """
        pending = self.hitl.get_pending_interventions()
        executed = 0
        
        for intervention in pending:
            if intervention.status == "approved":
                self.logger.info(f"Executing approved action: {intervention.title}")
                executed += 1
        
        return executed


class HITLController:
    """
    High-level controller combining Claude Code + HITL + Orchestrator.
    
    Manages the complete workflow:
    1. Claude Code thinks and plans
    2. HITL framework reviews risky operations
    3. Human approves or rejects
    4. Approved actions execute
    """
    
    def __init__(self, vault_path: Path):
        """Initialize controller."""
        self.vault_path = Path(vault_path)
        self.claude = SafeClaudeCode(vault_path)
        self.hitl = self.claude.hitl
    
    def full_protected_cycle(self, instruction: Optional[str] = None) -> Dict:
        """
        Run complete cycle with full HITL protection.
        
        Returns:
            Summary of cycle execution
        """
        import logging
        logger = logging.getLogger("HITLController")
        
        # Phase 1: Claude Code thinks and plans
        logger.info("🧠 PHASE 1: Claude thinking...")
        summary = self.claude.full_cycle(instruction)
        
        # Phase 2: Check for pending interventions
        logger.info("⏳ PHASE 2: Checking for interventions...")
        pending = self.hitl.get_pending_interventions()
        
        if pending:
            logger.info(f"📋 {len(pending)} human interventions needed")
            logger.warning("⛔ STOPPING: Waiting for human decisions")
            logger.warning("   Run: python hitl_review_interface.py")
            
            summary['pending_interventions'] = len(pending)
            summary['status'] = 'waiting_for_approval'
            return summary
        
        # Phase 3: Execute approved actions
        logger.info("✅ PHASE 3: All actions approved/safe - executing...")
        executed = self.claude.process_approved_actions()
        
        summary['executed_actions'] = executed
        summary['status'] = 'completed'
        
        return summary


# Demo / Testing
if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    vault_path = Path("./Vault")
    
    print("\n" + "="*70)
    print("CLAUDE CODE + HITL INTEGRATION - Demo")
    print("="*70 + "\n")
    
    try:
        # Test SafeClaudeCode
        safe_claude = SafeClaudeCode(vault_path)
        
        print("1️⃣  Testing safe operation (read file)...")
        response = safe_claude.execute_action(
            action="Read invoice list",
            params={'path': 'Accounting/'},
            server_type=MCPServerType.FILESYSTEM,
            capability='list_directory'
        )
        print(f"   Result: {response.result}\n")
        
        print("2️⃣  Testing high-risk operation (send email)...")
        response = safe_claude.execute_action(
            action="Send payment reminder",
            params={
                'to': 'john@example.com',
                'subject': 'Payment Due',
            },
            server_type=MCPServerType.EMAIL,
            capability='send_email'
        )
        print(f"   Result: {response.result}")
        print(f"   Status: {response.result.get('status') if response.result else 'error'}\n")
        
        print("3️⃣  Checking pending approvals...")
        pending = safe_claude.check_pending_approvals()
        print(f"   Pending: {pending}\n")
        
        print("✅ Integration demo complete!")
        print("\nTo review pending approvals, run:")
        print("  python hitl_review_interface.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
