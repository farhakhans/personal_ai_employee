"""
HITL QUICK START & EXAMPLES
═══════════════════════════════════════════════════════════════════════════

practical examples and quick start guide for HITL system.
"""


QUICKSTART = """

╔═══════════════════════════════════════════════════════════════════════════╗
║              HUMAN-IN-THE-LOOP QUICK START                              ║
╚═══════════════════════════════════════════════════════════════════════════╝


⚡ 30-SECOND SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Make sure ANTHROPIC_API_KEY is set:
   $ echo $ANTHROPIC_API_KEY

2. Use SafeClaudeCode instead of ClaudeCode:
   $ python -c "
   from claude_code_hitl import SafeClaudeCode
   from pathlib import Path
   
   safe_claude = SafeClaudeCode(Path('./Vault'))
   safe_claude.full_cycle()
   "

3. Review pending approvals:
   $ python hitl_review_interface.py


🎯 AFTER EACH HITL RUN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Check pending:
  python -c "
  from claude_code_hitl import SafeClaudeCode
  print(f'Pending: {SafeClaudeCode(Path(\"./Vault\")).check_pending_approvals()}')
  "

Review & approve:
  python hitl_review_interface.py

Check status:
  python -c "
  from hitl_framework import HITLFramework
  h = HITLFramework(Path('./Vault'))
  s = h.get_statistics()
  print(f'Approved: {s[\"approved\"]}, Rejected: {s[\"rejected\"]}')
  "


📝 COMMON APPROVAL SCENARIOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. EMAIL APPROVAL
   Shows: To, Subject, Body preview
   Review: Recipient, content, formatting
   Decision: Approve/Reject/Request changes
   → Approve if correct
   → Reject if wrong recipient
   → Request changes if content needs edits

2. PAYMENT APPROVAL
   Shows: Vendor, Amount, Invoice ID
   Review: Vendor correct? Amount right? Invoice valid?
   Decision: Approve/Reject/Request changes
   → Approve if verified
   → Reject if amount seems wrong
   → Request changes if vendor account different

3. DELETE APPROVAL
   Shows: Files to delete
   Review: These files really should be deleted?
   Decision: Confirm/Reject
   → Approve only if absolutely sure
   → Reject if in doubt

4. FORM SUBMISSION APPROVAL
   Shows: Form fields filled in
   Review: All fields correct? Validated?
   Decision: Approve/Reject/Request changes
   → Approve if all fields correct
   → Reject if validation issues
   → Request changes for specific fields


💡 THREE APPROVAL STRATEGIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STRATEGY 1: HANDS-ON (Best for important decisions)
────────────────────────────────────────────────

Process:
  1. Claude runs: python claude_code_hitl.py
  2. Check pending: python hitl_review_interface.py
  3. Review each intervention individually
  4. Approve each one with notes
  5. Claude executes approved actions

When to use:
  • Large payments
  • Critical emails
  • Deleting important files
  • First-time vendor payments


STRATEGY 2: BATCH APPROVAL (For routine operations)
──────────────────────────────────────────────────

Process:
  1. Claude runs daily (scheduled)
  2. Review pending once per day
  3. Group similar approvals
  4. Batch approve with notes
  5. Batch approve all ✓

When to use:
  • Routine emails
  • Regular payments
  • Draft emails (safe)
  • Scheduled tasks


STRATEGY 3: RISK-BASED (Hybrid approach)
────────────────────────────────────────

Process:
  1. Safe operations auto-execute (read, draft)
  2. Medium risk requires approval
  3. High risk requires escalation
  4. Critical ops go to CEO

Config:
  auto_approve_below_risk: low_risk
  escalate_above_risk: high_risk
  escalate_critical_to: ceo

When to use:
  • Everything (recommended)


🛡️  SAFETY CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Before deploying to production:

□ Using SafeClaudeCode (not regular ClaudeCode)
□ HITL framework initialized
□ Review interface tested
□ HITL config saved to Vault/System/
□ Approval folders created
□ Risk assessment tested
□ Escalation routing configured
□ Logging enabled
□ First test run completed


📊 MONITORING YOUR APPROVALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

View statistics:
  python -c "
  from hitl_framework import HITLFramework
  from pathlib import Path
  
  h = HITLFramework(Path('./Vault'))
  stats = h.get_statistics()
  
  for key, value in stats.items():
    print(f'{key}: {value}')
  "

View pending by risk level:
  python -c "
  from hitl_framework import HITLFramework
  from pathlib import Path
  
  h = HITLFramework(Path('./Vault'))
  pending = h.get_pending_interventions()
  
  for intervention in pending:
    print(f'{intervention.risk_assessment.value}: {intervention.title}')
  "

View approval history:
  ls -la Vault/Approved/ | head -20
  # or
  ls -la Vault/Rejected/ | head -20


===== COMPLETE WORKFLOW EXAMPLE =====

Time: 10:00 AM
Action: Run Claude Code
Command: python -c "from claude_code_hitl import SafeClaudeCode; SafeClaudeCode(Path('./Vault')).full_cycle()"

Output:
  - Claude reads Vault/Needs_Action/
  - Claude finds email from client
  - Claude thinks: need to send invoice
  - Claude creates draft
  - Claude requests approval (HITL intercepts)
  - Creates: Vault/Pending_Review/HITL_Send_Invoice_ClientA.md

Time: 11:00 AM
Action: Review approvals
Command: python hitl_review_interface.py

Display:
  📋 Pending Approvals: 1
  
  Intervention 1
  📧 Send Invoice to Client A
  
  Type: approval
  Level: MEDIUM
  Risk: medium_risk
  
  Description: Claude wants to send invoice to client
  
  To: john@example.com
  Subject: Invoice #INV-2026-001
  Amount: $5,000
  
Your decision: a) Approve, r) Reject, g) Add guidance, s) Skip, x) Exit

You choose: a (Approve)
Notes: Looks correct

Result: ✅ Approved: HITL_Send_Invoice_ClientA

Time: 11:05 AM
Action: File moves to Approved/
Command: ls Vault/Approved/
Result: HITL_Send_Invoice_ClientA.md

Time: 11:10 AM
Action: Claude checks approval status
Process: Claude sees file in Approved/
Result: Sends email ✅

Summary: Email sent successfully!


🚀 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Test HITL now:
   python hitl_framework.py

2. Run with SafeClaudeCode:
   python claude_code_hitl.py

3. Review interface:
   python hitl_review_interface.py

4. Read full guide:
   python HITL_SETUP_GUIDE.py

5. Configure custom rules:
   Edit Vault/System/hitl_config.json


═══════════════════════════════════════════════════════════════════════════
HITL enabled: Your AI is now safe! 🛡️
═══════════════════════════════════════════════════════════════════════════
"""


EXAMPLES = """

╔═══════════════════════════════════════════════════════════════════════════╗
║                    HITL CODE EXAMPLES                                    ║
╚═══════════════════════════════════════════════════════════════════════════╝


EXAMPLE 1: Basic SafeClaudeCode with HITL
──────────────────────────────────────────

from claude_code_hitl import SafeClaudeCode
from pathlib import Path

# Initialize
claude = SafeClaudeCode(Path('./Vault'))

# Run cycle - sensitive operations now require approval
summary = claude.full_cycle(
    instruction="Process pending invoices"
)

# Check for pending approvals
pending = claude.check_pending_approvals()
print(f"Pending approvals: {pending}")

# Summary
print(f"Status: {summary['status']}")


EXAMPLE 2: Manual Risk Assessment
──────────────────────────────────

from hitl_framework import HITLFramework, RiskAssessment
from pathlib import Path

hitl = HITLFramework(Path('./Vault'))

# Test risk assessment
actions = [
    ('read_file', {}),
    ('send_email', {}),
    ('process_payment', {'amount': 500}),
    ('process_payment', {'amount': 50000}),
    ('delete_file', {}),
]

for action_type, params in actions:
    risk = hitl.assess_risk(action_type, params)
    level = hitl.determine_intervention_level(risk)
    print(f"{action_type}: {risk.value} → {level.value}")


EXAMPLE 3: Request Intervention & Wait for Approval
───────────────────────────────────────────────────

from hitl_framework import HITLFramework
from pathlib import Path
import time

hitl = HITLFramework(Path('./Vault'))

# Request approval
intervention = hitl.request_intervention(
    action_type='send_email',
    title='Send Payment Reminder',
    description='Send payment reminder to Client A for overdue invoice',
    action_details={
        'client': 'Client A',
        'amount': 5000,
        'days_overdue': 30,
    }
)

print(f"Created: {intervention.intervention_id}")
print(f"Status: {intervention.status}")

# Wait for approval (example)
print("Waiting for human approval...")
max_wait = 300  # 5 minutes

for i in range(max_wait):
    status = hitl.get_intervention_status(intervention.intervention_id)
    
    if status == 'approved':
        print("✅ APPROVED! Executing action...")
        # Execute action here
        break
    elif status == 'rejected':
        print("❌ REJECTED! Operation cancelled.")
        break
    
    if (i + 1) % 30 == 0:
        print(f"Still waiting... ({i+1}s)")
    
    time.sleep(1)


EXAMPLE 4: Approve/Reject in Code
─────────────────────────────────

from hitl_framework import HITLFramework
from pathlib import Path

hitl = HITLFramework(Path('./Vault'))

# Get all pending
pending = hitl.get_pending_interventions()

for intervention in pending:
    print(f"\\n{intervention.title}")
    print(f"Risk: {intervention.risk_assessment.value}")
    
    if "payment" in intervention.title.lower():
        if intervention.action_details.get('amount', 0) < 1000:
            # Auto-approve small payments
            hitl.approve_intervention(
                intervention.intervention_id,
                notes="Auto-approved (below threshold)"
            )
        else:
            # Request guidance for large payments
            hitl.request_guidance(
                intervention.intervention_id,
                guidance="Please specify budget code for this payment"
            )


EXAMPLE 5: Batch Approval with Notes
────────────────────────────────────

from hitl_framework import HITLFramework
from pathlib import Path

hitl = HITLFramework(Path('./Vault'))

# Get pending
pending = hitl.get_pending_interventions()

# Filter to only emails
email_approvals = [
    i.intervention_id for i in pending 
    if 'email' in i.action_details.get('type', '').lower()
]

if email_approvals:
    # Batch approve with notes
    count = hitl.batch_approve(
        email_approvals,
        notes="Batch approved on 2026-02-13 by John"
    )
    print(f"Approved {count} emails")


EXAMPLE 6: Custom Risk Assessment
──────────────────────────────────

from hitl_framework import HITLFramework, RiskAssessment
from pathlib import Path

class CustomHITL(HITLFramework):
    def assess_risk(self, action_type, params):
        # Custom rules
        
        # Invoices > $10k with new vendors = critical
        if action_type == 'send_invoice':
            amount = params.get('amount', 0)
            is_new_vendor = params.get('new_vendor', False)
            
            if amount > 10000 and is_new_vendor:
                return RiskAssessment.CRITICAL_RISK
        
        # Use default assessment
        return super().assess_risk(action_type, params)

# Use it
custom = CustomHITL(Path('./Vault'))


EXAMPLE 7: Monitor HITL in Real-time
────────────────────────────────────

from hitl_framework import HITLFramework
from pathlib import Path
import time

hitl = HITLFramework(Path('./Vault'))

print("Monitoring HITL (press Ctrl+C to stop)\\n")

try:
    while True:
        stats = hitl.get_statistics()
        pending = stats.get('pending', 0)
        approved = stats.get('approved', 0)
        
        print(f"[{time.strftime('%H:%M:%S')}] Pending: {pending}, Approved: {approved}")
        
        time.sleep(10)

except KeyboardInterrupt:
    print("\\nMonitoring stopped")


EXAMPLE 8: CLaudé Code + Orchestrator + HITL
─────────────────────────────────────────────

from claude_code_hitl import HITLController
from pathlib import Path

# Full protected cycle
controller = HITLController(Path('./Vault'))

# This runs everything safely:
# 1. Claude thinks & plans
# 2. HITL reviews risky actions
# 3. Waits for human approval
# 4. Executes approved actions
summary = controller.full_protected_cycle(
    instruction="Process new client requests"
)

if summary.get('status') == 'waiting_for_approval':
    print(f"⏳ {summary['pending_interventions']} approvals needed")
    print("Review with: python hitl_review_interface.py")
else:
    print(f"✅ Completed {summary.get('executed_actions', 0)} actions")
"""


def main():
    """Display quick start & examples."""
    print(QUICKSTART)
    print("\\n" + "="*79)
    print(EXAMPLES)


if __name__ == "__main__":
    main()
