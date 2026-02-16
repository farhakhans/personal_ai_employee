"""
HUMAN-IN-THE-LOOP SETUP GUIDE
═══════════════════════════════════════════════════════════════════════════

Complete guide for implementing Human-in-the-Loop (HITL) patterns.
"""


HITL_SETUP_GUIDE = """

╔═══════════════════════════════════════════════════════════════════════════╗
║           HUMAN-IN-THE-LOOP (HITL) COMPLETE SETUP GUIDE                 ║
╚═══════════════════════════════════════════════════════════════════════════╝


📌 WHAT IS HUMAN-IN-THE-LOOP (HITL)?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HITL is a safety pattern where:
- Claude Code performs intelligent reasoning
- BUT requires explicit human approval for risky operations
- Human can see exactly what Claude plans to do
- Human can approve, reject, or request changes
- Only approved actions execute

This prevents:
  ❌ Accidental emails sent
  ❌ Random payments processed
  ❌ Important files deleted
  ❌ Forms submitted incorrectly


🎯 THE THREE INTERVENTION TYPES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  APPROVAL
   Simple Yes/No decision
   "Should Claude send this email?"
   
   Used for: Most sensitive actions

2️⃣  CONFIRMATION
   "Are you really sure?"
   Prevents accidental decisions
   
   Used for: High-risk operations

3️⃣  REVIEW
   Detailed human review of output
   "Is this invoice calculation correct?"
   
   Used for: Complex decisions


📊 RISK LEVELS (Automatic Classification)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 SAFE (Auto-approved)
   └─ Read file, list directory, search emails
   └─ Action: Execute immediately

🔵 LOW RISK (Standard review)
   └─ Draft email, get event details
   └─ Action: Requires approval

🟡 MEDIUM RISK (Higher review)
   └─ Send email, create event
   └─ Action: Requires explicit approval

🔴 HIGH RISK (Critical review)
   └─ Delete files, payments < $10k
   └─ Action: Requires escalation

⛔ CRITICAL RISK (Must escalate)
   └─ Large payments > $10k
   └─ Action: Route to finance/CEO


⚡ QUICK SETUP (3 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Test HITL Framework
   $ python hitl_framework.py
   
   Outputs risk assessments for different actions

Step 2: Start Claude Code WITH HITL
   $ python -c "
   from claude_code_hitl import SafeClaudeCode
   from pathlib import Path
   
   claude = SafeClaudeCode(Path('./Vault'))
   summary = claude.full_cycle()
   print(f'Pending approvals: {claude.check_pending_approvals()}')
   "

Step 3: Review Pending Approvals
   $ python hitl_review_interface.py
   
   Interactive menu for approving/rejecting decisions


🔧 CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Create: Vault/System/hitl_config.json

{
  "require_review_on_send_email": true,      // ✓ Always review emails
  "require_review_on_payment": true,         // ✓ Always review payments
  "require_review_on_delete": true,          // ✓ Always review deletes
  "require_review_on_form_submit": true,     // ✓ Always review submissions
  
  "auto_approve_below_risk": "low_risk",     // Auto-approve safe ops
  "escalate_above_risk": "high_risk",        // Escalate risky ops
  
  "escalate_large_payments_to": "finance_manager",  // Who gets escalations
  "escalate_critical_to": "ceo",             // Who gets critical escalations
  
  "approval_timeout_minutes": 60,            // Action expires if not approved
  "reminder_interval_minutes": 15,           // Remind user TODO approvals
  
  "log_all_interventions": true              // Keep detailed audit trail
}

Load in code:
  from hitl_framework import HITLFramework
  
  hitl = HITLFramework(Path('./Vault'))
  hitl.load_config(Path('./Vault/System/hitl_config.json'))


📋 WORKFLOW EXAMPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WORKFLOW 1: Send Email (Medium Risk)
─────────────────────────────────────

Timeline:

  10:00 - Claude Code runs (reads Needs_Action folder)
  10:01 - Finds: "Client asking for invoice"
  10:02 - Claude thinks: "Should draft and send response"
  10:03 - HITL intercepts: "Send email is medium risk"
  10:04 - Creates: Vault/Pending_Review/HITL_Send_Email_ClientA.md
  
  10:15 - You run: python hitl_review_interface.py
  10:15 - Shows draft email
  10:15 - You review and click: APPROVE
  10:16 - File moves: Vault/Approved/HITL_Send_Email_ClientA.md
  
  10:20 - Claude checks: "Is this approved?"
  10:21 - Claude sees: File in Approved/
  10:22 - Claude sends email ✅


WORKFLOW 2: Process Payment (High Risk)
───────────────────────────────────────

Timeline:

  10:00 - Bank notification arrives: "Payment due: $5,000"
  10:01 - File watcher processes: Vault/Inbox/FILE_DROP_payment.md
  10:02 - Claude Code runs
  10:03 - Claude reads accounting data
  10:04 - Claude decides: "Process vendor payment"
  10:05 - HITL intercepts: "Payment is HIGH RISK"
  10:06 - Creates: Vault/Pending_Review/HITL_Payment_Vendor.md
  10:07 - Marks: Level: HIGH, Risk: high_risk
  
  10:30 - You review in: python hitl_review_interface.py
  10:30 - Shows: vendor, amount, invoice
  10:30 - You request guidance: "Which vendor account?"
  10:31 - File moves: Vault/Pending_Review/ (status: awaiting_changes)
  
  10:45 - Claude reads guidance
  10:46 - Claude updates details: vendor account specified
  10:47 - Creates new intervention with updated details
  
  11:00 - You review again
  11:00 - You click: APPROVE
  11:01 - Payment processes ✅


WORKFLOW 3: Critical Payment (Escalation)
──────────────────────────────────────────

Timeline:

  10:00 - Invoice arrives: $50,000 contract payment
  10:01 - Claude Code processes
  10:02 - HITL detects: $50k > $10k threshold
  10:03 - HITL marks: Level: CRITICAL, Risk: critical_risk
  10:04 - HITL escalates to: CEO (from config)
  10:05 - Creates: Vault/Pending_Review/HITL_Payment_Contract_50k.md
  
  11:00 - CEO notified (you could add email alerts)
  11:30 - CEO reviews in: python hitl_review_interface.py
  11:30 - CEO sees: $50,000 to Acme Corp for Contract 2026
  11:30 - CEO clicks: APPROVE
  11:31 - Payment processes ✅


✅ INTERVENTION STATUSES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

pending
  └─ Waiting for human decision
  └─ File: Vault/Pending_Review/HITL_*.md
  └─ Action: User needs to review

approved
  └─ Human said YES
  └─ File: Vault/Approved/HITL_*.md
  └─ Action: Claude can execute

rejected
  └─ Human said NO
  └─ File: Vault/Rejected/HITL_*.md
  └─ Action: Claude won't execute

awaiting_changes
  └─ Human requested modifications
  └─ File: Vault/Pending_Review/HITL_*.md
  └─ Action: Claude updates details and resubmits

auto_approved
  └─ Automatically approved (safe operation)
  └─ File: Not created (internal only)
  └─ Action: Claude executes immediately


🎯 DECISION TYPES & MEANINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APPROVE
  ✅ "Yes, do it"
  └─ Action executes immediately
  └─ Can execute now or later

REJECT
  ❌ "No, don't do it"
  └─ Action is cancelled
  └─ Claude won't retry
  └─ Operation is logged as rejected

GUIDANCE
  📝 "Do it, but change X"
  └─ Action doesn't execute yet
  └─ Claude reads guidance
  └─ Claude updates parameters
  └─ Claude resubmits for review


💻 CODE EXAMPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXAMPLE 1: Basic SafeClaudeCode
───────────────────────────────

from claude_code_hitl import SafeClaudeCode
from pathlib import Path

# Initialize with HITL protection
claude = SafeClaudeCode(Path('./Vault'))

# This will now require approval for sensitive operations
summary = claude.full_cycle(
    custom_instruction="Process pending invoices"
)

# Check how many are waiting
pending = claude.check_pending_approvals()
print(f"Pending approvals: {pending}")

# If pending > 0, human needs to review:
# $ python hitl_review_interface.py


EXAMPLE 2: Manual HITL Request
───────────────────────────────

from hitl_framework import HITLFramework, InterventionType
from pathlib import Path

hitl = HITLFramework(Path('./Vault'))

# Request approval for something
intervention = hitl.request_intervention(
    action_type='send_email',
    title='Send Invoice to Client',
    description='Send $5000 invoice for completed project',
    action_details={
        'client': 'John Smith',
        'amount': 5000,
        'invoice_id': 'INV-2026-001',
    },
    intervention_type=InterventionType.APPROVAL
)

print(f"Intervention ID: {intervention.intervention_id}")
print(f"Status: {intervention.status}")
print(f"Risk: {intervention.risk_assessment.value}")


EXAMPLE 3: Review in Code
─────────────────────────

from hitl_framework import HITLFramework
from pathlib import Path

hitl = HITLFramework(Path('./Vault'))

# Get all pending
pending = hitl.get_pending_interventions()

if pending:
    for intervention in pending:
        print(f"\\n{intervention.title}")
        print(f"Risk: {intervention.risk_assessment.value}")
        
        # Approve it
        hitl.approve_intervention(
            intervention.intervention_id,
            notes="Looks good, approved"
        )


⚡ QUICK COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run Claude Code with HITL:
  $ python -c "
  from claude_code_hitl import SafeClaudeCode
  from pathlib import Path
  SafeClaudeCode(Path('./Vault')).full_cycle()
  "

Review pending:
  $ python hitl_review_interface.py

Check HITL status:
  $ python -c "
  from hitl_framework import HITLFramework
  from pathlib import Path
  h = HITLFramework(Path('./Vault'))
  print(h.get_statistics())
  "

View logs:
  $ tail -f Vault/System/interventions/*.json


🔐 SAFETY GUARANTEES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

With HITL enabled (SafeClaudeCode):

✅ GUARANTEED SAFE:
   • Claude CANNOT send email without approval
   • Claude CANNOT delete files without approval
   • Claude CANNOT process payments without approval
   • Claude CANNOT submit forms without approval
   
✅ ALWAYS LOGGED:
   • Every intervention is recorded
   • Every decision is timestamped
   • Who approved/rejected is logged
   • Modification requests are preserved

✅ HUMAN IN CONTROL:
   • You see exactly what Claude plans
   • You can reject any action
   • You can request modifications
   • You can escalate to others


⚠️  IMPORTANT RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Rules for Safe Operation:

1. Always use SafeClaudeCode (never direct ClaudeCode)
   ❌ Bad:  from claude_code import ClaudeCode
   ✅ Good: from claude_code_hitl import SafeClaudeCode

2. Review pending approvals regularly
   ❌ Bad:  Let approvals pile up for days
   ✅ Good: Review multiple times per day

3. Don't batch approve blindly
   ❌ Bad:  "Approve all 20 pending"
   ✅ Good: Review each one individually

4. Add notes when rejecting
   ❌ Bad:  Reject with no explanation
   ✅ Good: "This amount is too high - needs CEO review"

5. Use guidance for modifications
   ❌ Bad:  Reject, then hope Claude guesses right
   ✅ Good: "Change recipient to john@newcompany.com"


📚 TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ No pending interventions showing
   → Run: python hitl_framework.py (demo mode)
   → Manually request intervention in Python
   → Check: Vault/Pending_Review/ folder exists

❌ Approval interface shows 0 pending
   → Some actions auto-approve (safe operations)
   → Check MCP being used (read vs write)
   → Try requesting approval for: send_email, delete_file

❌ Can't find intervention markdown
   → They're created in: Vault/Pending_Review/
   → Also saved as JSON: Vault/System/interventions/
   → Check folder permissions

❌ Claude executing without approval
   → You're using regular ClaudeCode (not SafeClaudeCode)
   → Action is read-only (auto-approved)
   → Check HITL config - might be overriding


🎓 LEARNING PATH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Day 1: Understand the concept
  □ Read this guide
  □ Run: python hitl_framework.py
  □ Understand risk levels

Day 2: Start using it
  □ Use SafeClaudeCode instead of ClaudeCode
  □ Run your first cycle with HITL
  □ Review pending approvals

Day 3: Master it
  □ Customize HITL config
  □ Add custom risk assessment
  □ Set up escalation routing


═══════════════════════════════════════════════════════════════════════════
You now have Human-in-the-Loop safety for your AI Employee! 🛡️
═══════════════════════════════════════════════════════════════════════════
"""


def main():
    """Display HITL setup guide."""
    print(HITL_SETUP_GUIDE)


if __name__ == "__main__":
    main()
