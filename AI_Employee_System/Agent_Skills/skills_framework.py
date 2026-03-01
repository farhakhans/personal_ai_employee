"""
AGENT SKILLS FRAMEWORK
Base architecture for all Claude AI capabilities
Implements skills as modular, composable functions
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime
import json
import logging

logger = logging.getLogger("AgentSkills")


class AgentSkill(ABC):
    """Base class for all agent capabilities"""
    
    def __init__(self, name: str, description: str, requires_approval: bool = False):
        self.name = name
        self.description = description
        self.requires_approval = requires_approval
        self.last_executed = None
        self.execution_count = 0
        
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the skill
        Returns: {success, result, errors, timestamp}
        """
        pass
    
    def log_execution(self, success: bool, result: str = None):
        self.last_executed = datetime.now()
        self.execution_count += 1
        logger.info(f"[{self.name}] Executed: {success} | Result: {result}")
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "requires_approval": self.requires_approval,
            "last_executed": self.last_executed.isoformat() if self.last_executed else None,
            "execution_count": self.execution_count
        }


class VaultReadSkill(AgentSkill):
    """Read files from Obsidian vault"""

    def __init__(self, vault_path: str):
        super().__init__(
            name="VaultRead",
            description="Read markdown files from Obsidian vault",
            requires_approval=True  # Manual approval required
        )
        self.vault_path = vault_path

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        context: {file_path: str}
        """
        try:
            file_path = context.get("file_path")
            if not file_path:
                return {"success": False, "error": "file_path required"}

            full_path = f"{self.vault_path}/{file_path}"

            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            self.log_execution(True, f"Read {file_path}")
            return {
                "success": True,
                "content": content,
                "file_path": file_path,
                "size": len(content),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.log_execution(False, str(e))
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


class VaultWriteSkill(AgentSkill):
    """Write files to Obsidian vault"""

    def __init__(self, vault_path: str):
        super().__init__(
            name="VaultWrite",
            description="Write markdown files to Obsidian vault",
            requires_approval=True  # Manual approval required
        )
        self.vault_path = vault_path
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        context: {file_path: str, content: str, mode: 'w' or 'a'}
        """
        try:
            file_path = context.get("file_path")
            content = context.get("content")
            mode = context.get("mode", "w")
            
            if not file_path or content is None:
                return {"success": False, "error": "file_path and content required"}
            
            full_path = f"{self.vault_path}/{file_path}"
            
            with open(full_path, mode, encoding='utf-8') as f:
                f.write(content)
            
            self.log_execution(True, f"Wrote to {file_path}")
            return {
                "success": True,
                "file_path": file_path,
                "bytes_written": len(content),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.log_execution(False, str(e))
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


class EmailTriageSkill(AgentSkill):
    """Triage incoming emails"""
    
    def __init__(self):
        super().__init__(
            name="EmailTriage",
            description="Analyze emails and categorize by priority/action",
            requires_approval=True  # Manual approval required
        )
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        context: {email_id: str, sender: str, subject: str, body: str}
        """
        try:
            # Basic triage logic
            subject = context.get("subject", "").lower()
            sender = context.get("sender", "")
            body = context.get("body", "")
            
            # Determine priority and category
            priority = "normal"
            category = "general"
            action = "review"
            
            keywords_urgent = ["urgent", "asap", "emergency", "critical", "immediately"]
            keywords_sales = ["interested", "inquiry", "quote", "proposal", "purchase"]
            keywords_support = ["issue", "problem", "bug", "error", "help"]
            
            if any(kw in subject for kw in keywords_urgent):
                priority = "high"
            
            if any(kw in subject for kw in keywords_sales):
                category = "sales"
                action = "respond"
            elif any(kw in subject for kw in keywords_support):
                category = "support"
                action = "escalate"
            
            return {
                "success": True,
                "email_id": context.get("email_id"),
                "sender": sender,
                "subject": subject,
                "priority": priority,
                "category": category,
                "action": action,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


class DraftResponseSkill(AgentSkill):
    """Draft email responses"""
    
    def __init__(self):
        super().__init__(
            name="DraftResponse",
            description="Generate draft email responses for human review",
            requires_approval=True  # Manual approval required
        )
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        context: {sender: str, subject: str, email_body: str, tone: str}
        """
        try:
            sender = context.get("sender")
            subject = context.get("subject")
            tone = context.get("tone", "professional")
            
            # Simple template-based response (would use Claude in real system)
            draft = f"""Subject: Re: {subject}

Hi {sender},

Thank you for reaching out. We appreciate your interest in our services.

[DRAFT TEMPLATE - Human should customize this response]

Best regards,
Your AI Employee
"""
            
            return {
                "success": True,
                "draft": draft,
                "status": "pending_review",
                "requires_approval": True,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


class ApprovalSkill(AgentSkill):
    """Request human approval for sensitive actions"""
    
    def __init__(self):
        super().__init__(
            name="RequestApproval",
            description="Create approval request and wait for human decision",
            requires_approval=True
        )
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        context: {action: str, details: str, reference_id: str}
        """
        try:
            action = context.get("action")
            details = context.get("details")
            reference_id = context.get("reference_id")
            
            approval_file = f"Pending_Approval/APPROVAL_{reference_id}.md"
            
            approval_content = f"""# Approval Request
**Action:** {action}  
**Reference ID:** {reference_id}  
**Created:** {datetime.now().isoformat()}  
**Status:** ⏳ PENDING

## Details
{details}

## Decision
- [ ] APPROVE
- [ ] REJECT
- [ ] REQUEST CHANGES

**Decision By:** (human fills this in)  
**Timestamp:** (auto-filled)  

---
*System will process this approval when you make a selection.*
"""
            
            return {
                "success": True,
                "approval_file": approval_file,
                "reference_id": reference_id,
                "status": "pending",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


class CreatePlanSkill(AgentSkill):
    """Create action plans from analysis"""
    
    def __init__(self, vault_path: str):
        super().__init__(
            name="CreatePlan",
            description="Generate Plan.md files for multi-step tasks",
            requires_approval=True  # Manual approval required
        )
        self.vault_path = vault_path
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        context: {title: str, steps: list, priority: str}
        """
        try:
            title = context.get("title")
            steps = context.get("steps", [])
            priority = context.get("priority", "medium")
            
            plan_id = f"PLAN_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            plan_content = f"""# Plan: {title}
**Plan ID:** {plan_id}  
**Priority:** {priority}  
**Created:** {datetime.now().isoformat()}  
**Status:** 📋 DRAFT

## Steps
"""
            
            for i, step in enumerate(steps, 1):
                plan_content += f"{i}. [ ] {step}\n"
            
            plan_content += f"""

## Timeline
- Start: TBD
- Due: TBD

## Owner
- AI Employee (execute)
- Human (approve)

## Status
✅ Created | ⏳ In Progress | ✓ Completed

---
*Auto-generated by AI Employee - Review and approve before execution*
"""
            
            return {
                "success": True,
                "plan_id": plan_id,
                "file_path": f"Plans/PLAN_{plan_id}.md",
                "steps_count": len(steps),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


# ===== SKILL REGISTRY =====
class SkillRegistry:
    """Central registry of all available skills"""
    
    def __init__(self, vault_path: str):
        self.skills = {}
        self.vault_path = vault_path
        self._register_default_skills()
    
    def _register_default_skills(self):
        """Register Bronze tier skills"""
        self.register(VaultReadSkill(self.vault_path))
        self.register(VaultWriteSkill(self.vault_path))
        self.register(EmailTriageSkill())
        self.register(DraftResponseSkill())
        self.register(ApprovalSkill())
        self.register(CreatePlanSkill(self.vault_path))
    
    def register(self, skill: AgentSkill):
        self.skills[skill.name] = skill
        logger.info(f"Registered skill: {skill.name}")
    
    def execute_skill(self, skill_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a skill - requires manual approval for skills that need it"""
        if skill_name not in self.skills:
            return {"success": False, "error": f"Skill '{skill_name}' not found"}
        
        skill = self.skills[skill_name]
        
        # Check if skill requires manual approval
        if skill.requires_approval:
            # Create approval request instead of executing
            approval_request = {
                "success": True,
                "requires_approval": True,
                "status": "pending_approval",
                "skill_name": skill.name,
                "skill_description": skill.description,
                "context": context,
                "message": f"⚠️ Manual approval required for '{skill.name}'. Please review and approve before execution.",
                "timestamp": datetime.now().isoformat()
            }
            return approval_request
        
        # Only execute if no approval required
        return skill.execute(context)
    
    def approve_and_execute(self, skill_name: str, context: Dict[str, Any], approval_code: str = None) -> Dict[str, Any]:
        """Execute a skill after manual approval"""
        if skill_name not in self.skills:
            return {"success": False, "error": f"Skill '{skill_name}' not found"}
        
        skill = self.skills[skill_name]
        
        # Log the approval
        logger.info(f"[{skill.name}] Manual approval granted. Executing...")
        
        # Execute the skill
        result = skill.execute(context)
        result["manually_approved"] = True
        return result
    
    def list_skills(self) -> Dict[str, Any]:
        return {name: skill.to_dict() for name, skill in self.skills.items()}
    
    def get_skill_info(self, skill_name: str) -> Optional[Dict]:
        if skill_name not in self.skills:
            return None
        return self.skills[skill_name].to_dict()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    vault = r"d:\DocuBook-Chatbot folder\Personal AI Employee\AI_Employee_System\Vault"
    registry = SkillRegistry(vault)
    
    print("✅ Agent Skills Framework Initialized")
    print("\nAvailable Skills:")
    for name, info in registry.list_skills().items():
        print(f"  - {name}: {info['description']}")
