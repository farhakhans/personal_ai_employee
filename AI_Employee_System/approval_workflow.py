"""
APPROVAL WORKFLOW MANAGER
═══════════════════════════════════════════════════════════════════════════

Human-in-the-Loop approval system for Claude Code actions.

When Claude wants to:
- Send an email
- Process a payment
- Fill a form
- Post on social media
- Any sensitive operation

It requests approval first. You review and approve/reject each request.
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class ApprovalStatus(Enum):
    """Status of an approval request."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ApprovalRequest:
    """Represents an approval request."""
    
    def __init__(self, approval_id: str, action: str, description: str, 
                 params: Dict, timestamp: str):
        self.approval_id = approval_id
        self.action = action
        self.description = description
        self.params = params
        self.timestamp = timestamp
        self.status = ApprovalStatus.PENDING
    
    @classmethod
    def from_file(cls, file_path: Path) -> Optional['ApprovalRequest']:
        """Load approval request from vault file."""
        try:
            content = file_path.read_text()
            
            # Parse markdown file
            if "Approval ID:" not in content:
                return None
            
            # Extract fields
            lines = content.split('\n')
            approval_id = ""
            action = ""
            timestamp = ""
            
            for line in lines:
                if "Approval ID:" in line:
                    approval_id = line.split(":", 1)[1].strip()
                elif "Action Details" in line:
                    idx = lines.index(line)
                    if idx + 1 < len(lines):
                        action = lines[idx + 1].strip()
                elif "Timestamp:" in line:
                    timestamp = line.split(":", 1)[1].strip()
            
            # Get description from first heading
            description = file_path.stem.replace("APPROVAL_", "")
            
            request = cls(
                approval_id=approval_id,
                action=action,
                description=description,
                params={},
                timestamp=timestamp
            )
            
            return request
        except Exception as e:
            print(f"Error loading approval: {e}")
            return None


class ApprovalWorkflow:
    """Manages approval requests and workflow."""
    
    def __init__(self, vault_path: Path):
        """Initialize approval workflow."""
        self.vault_path = Path(vault_path)
        self.pending_dir = vault_path / "Pending_Approval"
        self.approved_dir = vault_path / "Approved"
        self.rejected_dir = vault_path / "Rejected"
        
        # Create directories
        self.pending_dir.mkdir(parents=True, exist_ok=True)
        self.approved_dir.mkdir(parents=True, exist_ok=True)
        self.rejected_dir.mkdir(parents=True, exist_ok=True)
    
    def get_pending_approvals(self) -> List[Path]:
        """Get all pending approval requests."""
        return sorted(
            self.pending_dir.glob("APPROVAL_*.md"),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )
    
    def get_approval_details(self, file_path: Path) -> Optional[Dict]:
        """Get detailed approval information."""
        try:
            content = file_path.read_text()
            
            return {
                'filename': file_path.name,
                'path': str(file_path),
                'content': content,
                'size': len(content),
                'created': datetime.fromtimestamp(
                    file_path.stat().st_mtime
                ).strftime('%Y-%m-%d %H:%M:%S'),
            }
        except Exception as e:
            return None
    
    def approve(self, file_path: Path) -> bool:
        """Approve a request (move to Approved folder)."""
        try:
            new_path = self.approved_dir / file_path.name
            file_path.rename(new_path)
            return True
        except Exception as e:
            print(f"Error approving: {e}")
            return False
    
    def reject(self, file_path: Path, reason: str = "") -> bool:
        """Reject a request (move to Rejected folder)."""
        try:
            # Add rejection reason to file
            content = file_path.read_text()
            content += f"\n\n## Rejection Reason\n{reason}\n"
            
            new_path = self.rejected_dir / file_path.name
            new_path.write_text(content)
            
            file_path.unlink()
            return True
        except Exception as e:
            print(f"Error rejecting: {e}")
            return False
    
    def display_approval(self, file_path: Path) -> None:
        """Display approval request in terminal."""
        details = self.get_approval_details(file_path)
        
        if not details:
            print(f"❌ Could not load approval: {file_path}")
            return
        
        # Pretty print
        print("\n" + "="*70)
        print("APPROVAL REQUEST".center(70))
        print("="*70)
        print(f"\n📄 {details['filename']}")
        print(f"🕐 Created: {details['created']}")
        print(f"\n{'-'*70}\n")
        print(details['content'])
        print("-"*70)


def interactive_approval_menu():
    """Interactive menu for managing approvals."""
    vault_path = Path("./Vault")
    workflow = ApprovalWorkflow(vault_path)
    
    print("\n" + "🟢"*35)
    print("🟢" + " "*68 + "🟢")
    print("🟢" + "  APPROVAL WORKFLOW MANAGER".center(68) + "🟢")
    print("🟢" + " "*68 + "🟢")
    print("🟢"*35 + "\n")
    
    while True:
        # Get pending approvals
        pending = workflow.get_pending_approvals()
        
        if not pending:
            print("\n✅ No pending approvals!")
            print("\nOptions:")
            print("  1. Check again")
            print("  2. Exit")
            
            choice = input("\nEnter choice (1-2): ").strip()
            
            if choice == "2":
                break
            
            continue
        
        print(f"\n📋 Pending Approvals: {len(pending)}\n")
        
        # Display summary
        for i, file_path in enumerate(pending[:5], 1):
            timestamp = datetime.fromtimestamp(
                file_path.stat().st_mtime
            ).strftime('%H:%M:%S')
            
            action = file_path.stem.replace("APPROVAL_", "")
            print(f"  {i}. [{timestamp}] {action}")
        
        if len(pending) > 5:
            print(f"  ... and {len(pending) - 5} more")
        
        print("\nOptions:")
        print(f"  1-{min(5, len(pending))}. Review approval")
        print("  a. Approve all (dangerous!)")
        print("  x. Exit")
        
        choice = input("\nEnter choice: ").strip().lower()
        
        if choice == "x":
            break
        elif choice == "a":
            confirm = input("⚠️  Approve ALL requests? This is dangerous! (yes/no): ").strip()
            if confirm.lower() == "yes":
                for file_path in pending:
                    workflow.approve(file_path)
                    print(f"✅ Approved: {file_path.name}")
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(pending):
                file_path = pending[idx]
                
                # Display detailed approval
                workflow.display_approval(file_path)
                
                # Get user decision
                print("\n\nYour decision:")
                print("  a) Approve")
                print("  r) Reject")
                print("  c) Cancel (review again later)")
                
                decision = input("\nEnter choice (a/r/c): ").strip().lower()
                
                if decision == "a":
                    if workflow.approve(file_path):
                        print(f"\n✅ Approved: {file_path.name}")
                    else:
                        print(f"\n❌ Error approving")
                
                elif decision == "r":
                    reason = input("\nReason for rejection: ").strip()
                    if workflow.reject(file_path, reason):
                        print(f"\n❌ Rejected: {file_path.name}")
                    else:
                        print(f"\n❌ Error rejecting")
                
                elif decision == "c":
                    print("\n⏭️  Skipping for now")
                else:
                    print("\n❌ Invalid choice")


# Demo / Testing
if __name__ == "__main__":
    # Check if running interactive menu
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_approval_menu()
    else:
        # Demo mode
        print("\n" + "="*70)
        print("APPROVAL WORKFLOW - Demo")
        print("="*70 + "\n")
        
        vault_path = Path("./Vault")
        workflow = ApprovalWorkflow(vault_path)
        
        # Check for pending approvals
        pending = workflow.get_pending_approvals()
        
        print(f"📋 Pending Approvals: {len(pending)}\n")
        
        if pending:
            for i, file_path in enumerate(pending[:3], 1):
                details = workflow.get_approval_details(file_path)
                if details:
                    print(f"{i}. {details['filename']}")
                    print(f"   Created: {details['created']}")
                    print(f"   Size: {details['size']} bytes\n")
        
        print("\nTo manage approvals interactively:")
        print("  python approval_workflow.py --interactive")
