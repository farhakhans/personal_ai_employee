"""
CLAUDE CODE - AI Reasoning & Planning Engine
═══════════════════════════════════════════════════════════════════════════

Claude Code is the thinking brain of your AI Employee.

Process:
1. WATCH (Watcher detects change)
   └─ Email arrives, file dropped, message sent

2. READ (Claude reads vault)
   └─ "Check /Needs_Action and /Accounting"

3. THINK (Claude reasons about situation)
   └─ "I see a WhatsApp from client asking for invoice
      AND a bank transaction showing late payment fee"

4. PLAN (Claude creates plan in vault)
   └─ Creates PLAN_ClientA_Invoice.md with checkboxes

5. ACT (Claude uses MCP servers as "hands")
   └─ MCP Invoice: Calculate overdue amount
   └─ MCP Email: Draft reminder email (needs approval)
   └─ MCP Approval: Request human approval before sending

This file implements the Claude Code engine with full MCP integration.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field

from anthropic import Anthropic
from mcp_coordinator import MCPCoordinator, MCPRequest, MCPServerType, MCPResponse


@dataclass
class ClaudeCodeSession:
    """Represents one Claude Code thinking session."""
    session_id: str
    timestamp: str
    input_files: List[str] = field(default_factory=list)
    thoughts: List[str] = field(default_factory=list)
    plans: List[str] = field(default_factory=list)
    actions_taken: List[Dict] = field(default_factory=list)
    approvals_requested: List[str] = field(default_factory=list)


class ClaudeCode:
    """Claude Code - The thinking brain of AI Employee."""
    
    def __init__(self, vault_path: Path, anthropic_api_key: Optional[str] = None):
        """
        Initialize Claude Code.
        
        Args:
            vault_path: Path to Obsidian vault
            anthropic_api_key: Anthropic API key (or env var ANTHROPIC_API_KEY)
        """
        self.vault_path = Path(vault_path)
        self.api_key = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment or parameters")
        
        # Initialize Anthropic client
        self.client = Anthropic(api_key=self.api_key)
        
        # Initialize MCP coordinator for actions
        self.mcp = MCPCoordinator(vault_path)
        
        # Logging
        self.logger = logging.getLogger("ClaudeCode")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Track sessions
        self.current_session: Optional[ClaudeCodeSession] = None
    
    def start_session(self) -> str:
        """Start a new Claude Code session."""
        session_id = f"SESSION_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.current_session = ClaudeCodeSession(
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )
        
        self.logger.info(f"🧠 Claude Code session started: {session_id}")
        return session_id
    
    def read_vault(self, folders: Optional[List[str]] = None) -> Dict[str, str]:
        """
        READ PHASE: Read files from vault.
        
        Args:
            folders: Folders to read from (default: Needs_Action, Pending_Approval, Accounting)
        
        Returns:
            Dictionary of folder -> contents
        """
        if folders is None:
            folders = ['Needs_Action', 'Pending_Approval', 'Accounting']
        
        contents = {}
        
        for folder in folders:
            folder_path = self.vault_path / folder
            
            if not folder_path.exists():
                continue
            
            files = list(folder_path.glob("*.md"))
            folder_content = []
            
            for file in files[:5]:  # Limit to 5 most recent
                try:
                    content = file.read_text()
                    folder_content.append({
                        'filename': file.name,
                        'content': content[:1000],  # First 1000 chars
                    })
                except Exception as e:
                    self.logger.error(f"Could not read {file}: {e}")
            
            if folder_content:
                contents[folder] = folder_content
        
        self.logger.info(f"📖 Read {sum(len(v) for v in contents.values())} files from vault")
        
        if self.current_session:
            self.current_session.input_files.extend(
                [f['filename'] for files in contents.values() for f in files]
            )
        
        return contents
    
    def think(self, vault_contents: Dict[str, str], custom_instruction: Optional[str] = None) -> str:
        """
        THINK PHASE: Claude reasons about the situation.
        
        Args:
            vault_contents: Contents read from vault
            custom_instruction: Custom instruction for Claude
        
        Returns:
            Claude's analysis and thinking
        """
        # Build prompt with vault contents
        prompt = f"""You are Claude Code, the thinking brain of an AI Employee system.

Your task is to analyze the current vault state and decide what actions to take.

CURRENT VAULT STATE:
{json.dumps(vault_contents, indent=2)}

AVAILABLE MCP SERVERS (Your "Hands"):
{self.mcp.describe_servers()}

INSTRUCTIONS:
1. Analyze the current situation
2. Identify patterns and issues
3. Plan specific actions to take
4. For each action, specify which MCP server to use
5. Always request approval for sensitive operations

Remember:
- Read-only operations don't need approval
- Any action that modifies state (send email, process payment, etc.) needs approval
- Be specific about parameters for each action

"""
        
        if custom_instruction:
            prompt += f"\nADDITIONAL INSTRUCTION:\n{custom_instruction}\n"
        
        # Call Claude with system prompt
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system="""You are Claude Code, the thinking engine of an AI Employee system.
You have access to MCP servers that can interact with external systems.
Always be clear about:
1. What you observe in the vault
2. What problems need solving
3. What specific actions to take (with MCP server names)
4. Which actions need human approval""",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        thoughts = response.content[0].text
        self.logger.info(f"🧠 Claude analyzed situation")
        
        if self.current_session:
            self.current_session.thoughts.append(thoughts)
        
        return thoughts
    
    def plan(self, thoughts: str) -> str:
        """
        PLAN PHASE: Claude creates an action plan.
        
        Args:
            thoughts: Claude's analysis from think phase
        
        Returns:
            Action plan with steps
        """
        prompt = f"""Based on your analysis:

{thoughts}

Now create a detailed action plan:

1. List each action you need to take
2. For each action:
   - Specify the MCP server (filesystem, email, browser, calendar, approval)
   - List the exact parameters needed
   - Note if approval is required (yes/no)
3. Specify the order of operations
4. Include checkboxes for tracking

Format as a structured plan that can be saved to the vault."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            system="You are creating a detailed action plan with specific MCP server calls.",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        plan = response.content[0].text
        self.logger.info(f"📋 Created action plan")
        
        if self.current_session:
            self.current_session.plans.append(plan)
        
        return plan
    
    def save_plan(self, plan: str, plan_name: str = "PLAN") -> Path:
        """
        Save action plan to vault.
        
        Args:
            plan: Plan content
            plan_name: Name for plan file
        
        Returns:
            Path to saved plan
        """
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        plan_file = self.vault_path / "Plans" / f"{plan_name}_{timestamp}.md"
        plan_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Format as markdown with header
        full_content = f"""# Action Plan: {plan_name}

**Created:** {datetime.now().isoformat()}
**Session:** {self.current_session.session_id if self.current_session else 'N/A'}

## Plan Details

{plan}

## Status
- [ ] Execute Step 1
- [ ] Execute Step 2
- [ ] Execute Step 3
- [ ] Complete & Archive

## Notes
Add execution notes here as you complete each step.
"""
        
        plan_file.write_text(full_content)
        self.logger.info(f"📁 Plan saved: {plan_file}")
        
        return plan_file
    
    def execute_action(self, action: str, params: Dict[str, Any], 
                      server_type: MCPServerType, capability: str,
                      requires_approval: bool = False) -> MCPResponse:
        """
        ACT PHASE: Execute an action using MCP.
        
        Args:
            action: Description of the action
            params: Parameters for the MCP capability
            server_type: Which MCP server to use
            capability: Which capability to invoke
            requires_approval: Whether this needs human approval
        
        Returns:
            Response from MCP server
        """
        self.logger.info(f"🤖 Executing: {server_type.value}.{capability}")
        
        # Create MCP request
        request = MCPRequest(
            server_type=server_type,
            capability=capability,
            params=params,
            description=action
        )
        
        # Invoke MCP
        response = self.mcp.invoke(request)
        
        # Log action
        if self.current_session:
            self.current_session.actions_taken.append({
                'action': action,
                'server': server_type.value,
                'capability': capability,
                'success': response.success,
                'timestamp': response.timestamp,
            })
        
        return response
    
    def request_approval(self, action_type: str, description: str, 
                        params: Dict[str, Any]) -> str:
        """
        REQUEST APPROVAL PHASE: Create approval request.
        
        Sensitive operations (payment, email send, form submission)
        require human approval before execution.
        
        Args:
            action_type: Type of action (payment, email, form_submit, etc.)
            description: What the action will do
            params: Parameters for the action
        
        Returns:
            Approval ID
        """
        approval_response = self.execute_action(
            action=f"Request approval for {action_type}",
            params={
                'action': action_type,
                'description': description,
                'params': params,
            },
            server_type=MCPServerType.APPROVAL,
            capability='request_approval'
        )
        
        if approval_response.success and approval_response.result:
            approval_id = approval_response.result.get('approval_id')
            
            if self.current_session:
                self.current_session.approvals_requested.append(approval_id)
            
            self.logger.info(f"✋ Approval requested: {approval_id}")
            return approval_id
        
        return ""
    
    def check_approval(self, approval_id: str) -> bool:
        """
        Check if an approval has been granted.
        
        Args:
            approval_id: ID of approval to check
        
        Returns:
            True if approved, False otherwise
        """
        response = self.execute_action(
            action=f"Check approval status",
            params={'approval_id': approval_id},
            server_type=MCPServerType.APPROVAL,
            capability='check_approval_status'
        )
        
        if response.success:
            status = response.result.get('status')
            return status == 'approved'
        
        return False
    
    def end_session(self) -> Optional[Dict]:
        """End session and return summary."""
        if not self.current_session:
            return None
        
        summary = {
            'session_id': self.current_session.session_id,
            'timestamp': self.current_session.timestamp,
            'files_read': len(self.current_session.input_files),
            'thoughts_generated': len(self.current_session.thoughts),
            'plans_created': len(self.current_session.plans),
            'actions_taken': len(self.current_session.actions_taken),
            'approvals_requested': len(self.current_session.approvals_requested),
        }
        
        self.logger.info(f"✅ Session ended: {summary}")
        
        # Save session log
        self._save_session_log(summary)
        
        return summary
    
    def _save_session_log(self, summary: Dict):
        """Save session log to vault."""
        try:
            log_file = self.vault_path / "System" / "claude_code_sessions.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(log_file, 'a') as f:
                f.write(json.dumps(summary) + '\n')
        except Exception as e:
            self.logger.error(f"Could not save session log: {e}")
    
    def full_cycle(self, custom_instruction: Optional[str] = None) -> Dict:
        """
        Run complete WATCH->READ->THINK->PLAN->ACT cycle.
        
        Args:
            custom_instruction: Custom instruction for thinking phase
        
        Returns:
            Session summary
        """
        # Start session
        self.start_session()
        
        try:
            # READ
            vault_contents = self.read_vault()
            
            if not vault_contents:
                self.logger.info("No vault contents to process")
                return self.end_session()
            
            # THINK
            thoughts = self.think(vault_contents, custom_instruction)
            
            # PLAN
            plan = self.plan(thoughts)
            
            # Save plan to vault
            self.save_plan(plan)
            
            # Return summary
            return self.end_session()
        
        except Exception as e:
            self.logger.error(f"Error in cycle: {e}")
            raise


# Example Usage
if __name__ == "__main__":
    import sys
    
    # Initialize Claude Code
    vault_path = Path("./Vault")
    
    try:
        claude_code = ClaudeCode(vault_path)
        
        print("\n" + "="*70)
        print("CLAUDE CODE - Reasoning Engine Demo")
        print("="*70 + "\n")
        
        # Run full cycle
        print("🧠 Starting Claude Code reasoning cycle...\n")
        
        summary = claude_code.full_cycle(
            custom_instruction="Analyze vault and suggest 2-3 priority actions"
        )
        
        print("\n" + "="*70)
        print("Session Summary:")
        print("="*70)
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nMake sure ANTHROPIC_API_KEY is set:")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
