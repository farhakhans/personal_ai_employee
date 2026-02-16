"""
HITL REVIEW INTERFACE
═══════════════════════════════════════════════════════════════════════════

Interactive interface for reviewing and approving human-in-the-loop interventions.
"""

import sys
from pathlib import Path
from typing import Optional
import json
from datetime import datetime

from hitl_framework import HITLFramework, InterventionPoint, InterventionLevel


class HITLReviewInterface:
    """Interactive UI for reviewing and approving interventions."""
    
    def __init__(self, vault_path: Path):
        """Initialize review interface."""
        self.vault_path = Path(vault_path)
        self.hitl = HITLFramework(vault_path)
        self.stats_updated = False
    
    def display_banner(self):
        """Display welcome banner."""
        print("\n" + "🟢"*35)
        print("🟢" + " "*68 + "🟢")
        print("🟢" + "  HUMAN-IN-THE-LOOP REVIEW INTERFACE".center(68) + "🟢")
        print("🟢" + " "*68 + "🟢")
        print("🟢"*35 + "\n")
    
    def display_intervention(self, intervention: InterventionPoint, index: int = 0):
        """Display a single intervention for review."""
        
        # Risk indicator
        risk_colors = {
            'safe': '🟢',
            'low_risk': '🔵',
            'medium_risk': '🟡',
            'high_risk': '🔴',
            'critical_risk': '⛔',
        }
        
        risk_icon = risk_colors.get(intervention.risk_assessment.value, '❓')
        
        print(f"\n{'-'*70}")
        if index > 0:
            print(f"Intervention {index}")
        
        print(f"{risk_icon} {intervention.title}")
        print(f"\n  Type: {intervention.intervention_type.value}")
        print(f"  Level: {intervention.level.value.upper()}")
        print(f"  Risk: {intervention.risk_assessment.value}")
        print(f"  ID: {intervention.intervention_id}")
        print(f"\n  Description:\n  {intervention.description}")
        
        # Show action details
        if intervention.action_details:
            print(f"\n  Action Details:")
            for key, value in intervention.action_details.items():
                if isinstance(value, (dict, list)):
                    print(f"    {key}: {json.dumps(value)}")
                else:
                    print(f"    {key}: {value}")
        
        print(f"\n  Time: {intervention.timestamp}")
    
    def show_main_menu(self):
        """Display main menu."""
        print("\n" + "="*70)
        print("MAIN MENU".center(70))
        print("="*70)
        
        stats = self.hitl.get_statistics()
        pending = stats.get('pending', 0)
        
        print(f"\n📊 STATUS:")
        print(f"  Pending Approvals: {pending}")
        print(f"  Approved: {stats.get('approved', 0)}")
        print(f"  Rejected: {stats.get('rejected', 0)}")
        print(f"  Total: {stats.get('total_interventions', 0)}")
        
        print(f"\nOPTIONS:")
        print(f"  1. Review pending approvals")
        print(f"  2. Batch approve all pending")
        print(f"  3. View statistics")
        print(f"  4. View approved interventions")
        print(f"  5. View rejected interventions")
        print(f"  x. Exit")
        
        choice = input("\nEnter choice (1-5, x): ").strip().lower()
        return choice
    
    def review_pending(self):
        """Review pending interventions one by one."""
        pending = self.hitl.get_pending_interventions()
        
        if not pending:
            print("\n✅ No pending approvals!")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n📋 {len(pending)} pending approval(s)\n")
        
        for i, intervention in enumerate(pending, 1):
            self.display_intervention(intervention, i)
            
            # Get decision
            print(f"\nYour decision:")
            print(f"  a) Approve")
            print(f"  r) Reject")
            print(f"  g) Add guidance (request changes)")
            print(f"  s) Skip for now")
            print(f"  x) Exit review")
            
            decision = input("\nEnter choice (a/r/g/s/x): ").strip().lower()
            
            if decision == "a":
                notes = input("Add notes (optional): ").strip()
                self.hitl.approve_intervention(intervention.intervention_id, notes)
                print(f"\n✅ Approved: {intervention.intervention_id}")
            
            elif decision == "r":
                reason = input("Reason for rejection: ").strip()
                self.hitl.reject_intervention(intervention.intervention_id, reason)
                print(f"\n❌ Rejected: {intervention.intervention_id}")
            
            elif decision == "g":
                guidance = input("What changes are needed?: ").strip()
                self.hitl.request_guidance(intervention.intervention_id, guidance)
                print(f"\n📝 Guidance added")
            
            elif decision == "s":
                print(f"\n⏭️  Skipping")
                continue
            
            elif decision == "x":
                print(f"\n👋 Exiting review")
                break
            
            else:
                print(f"\n❌ Invalid choice")
    
    def batch_approve_all(self):
        """Approve all pending interventions at once."""
        pending = self.hitl.get_pending_interventions()
        
        if not pending:
            print("\n✅ No pending approvals!")
            return
        
        print(f"\n⚠️  About to approve {len(pending)} intervention(s)")
        print("\nList of interventions:")
        
        for i, intervention in enumerate(pending, 1):
            print(f"  {i}. {intervention.title}")
        
        confirm = input("\n⚠️  Are you sure? (yes/no): ").strip().lower()
        
        if confirm == "yes":
            notes = input("Add notes for all approvals (optional): ").strip()
            
            ids = [i.intervention_id for i in pending]
            count = self.hitl.batch_approve(ids, notes)
            
            print(f"\n✅ Approved {count}/{len(pending)} interventions")
        else:
            print("\n👌 Cancelled")
    
    def view_statistics(self):
        """View HITL statistics."""
        stats = self.hitl.get_statistics()
        pending = self.hitl.get_pending_interventions()
        
        print("\n" + "="*70)
        print("HITL STATISTICS".center(70))
        print("="*70)
        
        print(f"\n📊 Overall:")
        print(f"  Total Interventions: {stats.get('total_interventions', 0)}")
        print(f"  Pending: {stats.get('pending', 0)}")
        print(f"  Approved: {stats.get('approved', 0)}")
        print(f"  Rejected: {stats.get('rejected', 0)}")
        
        if pending:
            print(f"\n⏳ Pending Interventions:")
            
            # Group by level
            by_level = {}
            for intervention in pending:
                level = intervention.level.value
                if level not in by_level:
                    by_level[level] = []
                by_level[level].append(intervention)
            
            for level in ['low', 'medium', 'high', 'critical']:
                count = len(by_level.get(level, []))
                if count > 0:
                    print(f"  {level.upper()}: {count}")
                    for i in by_level.get(level, [])[:2]:
                        print(f"    • {i.title}")
            
            # Show oldest pending
            oldest = min(pending, key=lambda x: x.timestamp)
            print(f"\n  Oldest pending: {oldest.title}")
            print(f"  Time: {oldest.timestamp}")
        
        input("\nPress Enter to continue...")
    
    def view_approved(self):
        """View approved interventions."""
        try:
            approved_dir = self.vault_path / "Approved"
            
            if not approved_dir.exists():
                print("\n✅ No approved interventions yet!")
                return
            
            approved_files = list(approved_dir.glob("HITL_*.md"))
            
            print(f"\n✅ Approved Interventions: {len(approved_files)}\n")
            
            for i, file in enumerate(sorted(approved_files, reverse=True)[:10], 1):
                print(f"  {i}. {file.stem}")
            
            if len(approved_files) > 10:
                print(f"  ... and {len(approved_files) - 10} more")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def view_rejected(self):
        """View rejected interventions."""
        try:
            rejected_dir = self.vault_path / "Rejected"
            
            if not rejected_dir.exists():
                print("\n No rejected interventions yet!")
                return
            
            rejected_files = list(rejected_dir.glob("HITL_*.md"))
            
            print(f"\n❌ Rejected Interventions: {len(rejected_files)}\n")
            
            for i, file in enumerate(sorted(rejected_files, reverse=True)[:10], 1):
                print(f"  {i}. {file.stem}")
            
            if len(rejected_files) > 10:
                print(f"  ... and {len(rejected_files) - 10} more")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the interactive review interface."""
        self.display_banner()
        
        while True:
            choice = self.show_main_menu()
            
            if choice == "1":
                self.review_pending()
            elif choice == "2":
                self.batch_approve_all()
            elif choice == "3":
                self.view_statistics()
            elif choice == "4":
                self.view_approved()
            elif choice == "5":
                self.view_rejected()
            elif choice == "x":
                print("\n👋 Goodbye!\n")
                break
            else:
                print("\n❌ Invalid choice")


def main():
    """Run HITL review interface."""
    vault_path = Path("./Vault")
    
    try:
        interface = HITLReviewInterface(vault_path)
        interface.run()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
