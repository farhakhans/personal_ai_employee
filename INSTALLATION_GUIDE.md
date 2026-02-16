# 📚 Complete Installation & Usage Guide

## System Overview

You now have a complete **Personal AI Employee System** with full automation capabilities:

✅ Automatic task detection and processing  
✅ Real-time dashboard with monitoring  
✅ Approval workflow management  
✅ Automatic plan generation  
✅ Smart notifications  
✅ Complete audit trail  
✅ Interactive menu system  

---

## What We Created

### Core System Files (7 files)
1. **app.py** - Main application with interactive menu
2. **config.py** - All system configuration
3. **task_manager.py** - Task tracking and processing
4. **approval_system.py** - Approval workflow engine
5. **plan_generator.py** - Auto-generates action plans
6. **dashboard.py** - Real-time monitoring dashboard
7. **notification_system.py** - Alert and notification system

### Support Files (4 files)
1. **quick_status.py** - Single-command status check
2. **run.bat** - Windows launcher
3. **run.sh** - Linux/Mac launcher
4. **status.bat** - Windows quick status

### Documentation (3 files)
1. **README.md** - Complete documentation
2. **QUICKSTART.md** - Quick start guide
3. **INSTALLATION_GUIDE.md** - This file

### Configuration (3 files)
1. **Business_Goals.md.md** - Business objectives
2. **Company_Handbook.md.md** - Rules and procedures
3. **Dashboard.md.md** - Dashboard guide

### Example Tasks (2 files)
1. **vault/Needs_Action/EMAIL_ClientA_2026-02-15.md.md** - Payment task
2. **vault/Needs_Action/TASK_ClientB_Proposal_2026-02-15.md.md** - Process task

### Folder Structure
```
vault/
├── Needs_Action/      ← Your tasks go here
├── Pending_Approval/  ← Auto-moved here
├── Approved/          ← After approval
├── Done/              ← After completion
└── Plans/             ← Auto-generated plans
```

---

## Installation (Already Done!)

The system is fully installed and ready to use. No additional setup needed!

**Python Requirements:**
- Python 3.8 or higher (already verified)
- Standard library only (pathlib, json, datetime)

---

## Getting Started (3 Steps)

### Step 1: Understand the System (2 min)
Read this section carefully to understand what you're working with.

### Step 2: Create Your First Task (2 min)
Copy this into `vault/Needs_Action/` as a new file:

**Filename:** `TASK_MyFirstTask_2026-02-15.md.md`

**Content:**
```markdown
# My First Task

## Objective
Demonstrate the Personal AI Employee system

## Description
This is a test task to show how the system works.

## Priority
MEDIUM

## Type
PROCESS
```

### Step 3: Run the System (1 min)
Open terminal and run:
```bash
python quick_status.py
```

You should see:
- Your task appears in dashboard
- System shows it's PENDING
- Total tasks: 1

---

## System Usage

### Quick Status (Fastest)
```bash
python quick_status.py
```
**What it does:** Shows dashboard and exits  
**Best for:** Quick checks  
**Time:** < 1 second

### Interactive Mode (Full Control)
```bash
python app.py
```
**What it does:** Opens main menu  
**Menu options:**
1. Refresh Dashboard
2. View Pending Tasks
3. View Pending Approvals
4. Approve/Reject Tasks
5. View Completed Tasks
6. View System Status
7. Save Dashboard State
8. Run Continuous Monitor
0. Exit

### Monitoring Mode (Continuous)
```bash
python app.py monitor
```
**What it does:** Checks every 5 minutes  
**Best for:** Leaving running in background  
**Stop with:** Ctrl+C

### Command Line Mode (Scripting)
```bash
python app.py bootstrap    # Initialize and show status
python app.py monitor      # Continuous monitoring
python app.py status       # Show status and exit
```

---

## Task Management

### Creating Tasks

**Location:** `vault/Needs_Action/` folder

**File Format:** `[TYPE]_[NAME]_[DATE].md.md`

**Examples:**
- `PAYMENT_Invoice_2026-02-15.md.md`
- `EMAIL_ClientA_2026-02-15.md.md`
- `TASK_Project_Review_2026-02-15.md.md`

### Task Template

```markdown
# Task Title

## Objective
What needs to be accomplished

## Description
Details about the task

## Priority
CRITICAL | HIGH | MEDIUM | LOW

## Type
PAYMENT | EMAIL | PROCESS | REPORT | OTHER

## Amount
[Only for PAYMENT type - e.g., 500]

## Additional Notes
Any extra information
```

### Task Fields

| Field       | Required | Options                         | Notes                      |
| ----------- | -------- | ------------------------------- | -------------------------- |
| Objective   | Yes      | Any                             | Main goal                  |
| Priority    | Yes      | CRITICAL, HIGH, MEDIUM, LOW     | Auto-detected from content |
| Type        | Yes      | PAYMENT, EMAIL, PROCESS, REPORT | Auto-processed differently |
| Amount      | No       | Number                          | Only for PAYMENT type      |
| Description | No       | Any                             | Additional details         |

### What Happens Automatically

When you add a task file:

1. **Detection** (Instant)
   - System finds file in Needs_Action
   - Reads file content
   - Extracts metadata

2. **Analysis** (1 second)
   - Determines priority
   - Identifies task type
   - Extracts amount (if payment)

3. **Planning** (2 seconds)
   - Auto-generates action plan
   - Saves to vault/Plans/
   - Creates step-by-step instructions

4. **Approval Check** (1 second)
   - Checks if approval needed
   - If < $50 payment: Auto-approves
   - If > $50: Creates approval request

5. **Notification** (Instant)
   - Sends alert to dashboard
   - Displays in system logs
   - Listed in pending tasks

6. **Status Tracking**
   - Task moved to appropriate folder
   - Status updated in database
   - History maintained

---

## Approval Workflow

### How Approvals Work

**For Payments:**
- < $50 → Auto-approve ✓
- $50-1000 → Require approval
- > $1000 → Require senior approval

**For Tasks:**
- CRITICAL → Always flag
- HIGH → Often needs approval
- MEDIUM → Sometimes needs review
- LOW → Usually auto-process

### Approving a Task

1. Run the system:
```bash
python app.py
```

2. Select option **4: Approve/Reject Tasks**

3. Review approval details:
   - Task name
   - Type (PAYMENT, etc.)
   - Amount (if applicable)
   - Creation date

4. Choose action:
   - **a** = Approve
   - **r** = Reject

5. Task automatically:
   - Moves to Approved folder
   - Status updated
   - Notification sent
   - Logged for audit

### Approval Status

**Pending:** Awaiting action  
**Approved:** Accepted  
**Rejected:** Declined  
**Auto-approved:** System auto-approved (< $50)

---

## Dashboard & Monitoring

### Dashboard Contents

**System Status**
- HEALTHY, ATTENTION NEEDED, or CRITICAL ALERT
- Last update timestamp

**Task Summary**
- Total tasks
- Pending count
- Awaiting approval count
- Completed count

**Approvals**
- Pending count
- Total approved
- Total rejected

**Health Metrics**
- Completion rate %
- Backlog size
- Recommendations

**Recent Activity**
- Last 10 activities
- Timestamps
- Status changes

### Dashboard Files

**Real-time View:**
```bash
python quick_status.py
```

**Saved State:**
- File: `dashboard_state.json`
- Auto-saved after each run
- Contains all metrics

**View Saved State:**
```bash
cat dashboard_state.json
```

---

## File Management

### Task Folders

**Needs_Action/** - WHERE YOU PUT NEW TASKS
- This is where the system monitors
- Add .md files here
- System processes automatically

**Plans/** - AUTO-GENERATED PLANS
- System creates detailed plans
- Named: `PLAN_[TaskName].md`
- Contains steps, checkpoints, approvals

**Pending_Approval/** - WAITING FOR APPROVAL
- Tasks needing human review
- Auto-moved here by system
- Approve via menu option 4

**Approved/** - APPROVED TASKS
- Approved by human
- Ready for execution
- Moved here automatically

**Done/** - COMPLETED TASKS
- Finished and archived
- Moved here when complete
- Kept for history

### Data Files

**approvals.json**
- All approval history
- Timestamps and decisions
- Audit trail
- Auto-saved

**dashboard_state.json**
- Latest dashboard snapshot
- All metrics and status
- Created after each run

**system_logs.txt**
- System activity log
- Errors and warnings
- Full history (auto-rotating)

---

## Configuration

### Default Settings

Edit `config.py` to customize:

**Check Interval (5 minutes)**
```python
SYSTEM_CONFIG["check_interval_seconds"] = 300
```

**Approval Threshold (Auto-approve < $50)**
```python
APPROVAL_RULES["auto_approve_below_amount"] = 50
```

**Spending Limits**
```python
BUSINESS_RULES = {
    "max_daily_spending": 5000,
    ...
}
```

**Log Settings**
```python
LOGGING_CONFIG = {
    "log_file": Path(...) / "system_logs.txt",
    "max_log_size_mb": 10
}
```

### Common Customizations

**Make approvals faster (shorter interval):**
```python
SYSTEM_CONFIG["check_interval_seconds"] = 60  # Every minute
```

**Lower auto-approval amount:**
```python
APPROVAL_RULES["auto_approve_below_amount"] = 25  # Auto-approve < $25
```

**Higher spending limit:**
```python
BUSINESS_RULES["max_daily_spending"] = 10000  # Allow $10K/day
```

---

## Troubleshooting

### Tasks Not Appearing?

1. Check file location: `vault/Needs_Action/`
2. Check filename: Must end with `.md.md`
3. Verify content format (markdown)
4. Run `python quick_status.py` to reload
5. Check for error messages

### Approvals Not Working?

1. Restart system: `python app.py`
2. Check amount format (must be number)
3. Verify approval_system.py exists
4. Check `config.py` approval settings
5. Look for error in console output

### System Not Starting?

1. Check Python version: `python --version` (need 3.8+)
2. Verify all .py files in root folder
3. Check folder permissions
4. Try running from different terminal
5. Restart Python/terminal

### Dashboard Not Updating?

1. Run `python quick_status.py` to refresh
2. Check system_logs.txt for errors
3. Verify vault folders exist
4. Check file permissions
5. Try restarting the system

### Payment Not Auto-Approving?

1. Check amount "Amount: 50" in task file
2. Verify < $50 for auto-approval
3. Check config.py threshold setting
4. Look in `approvals.json` to confirm
5. Run dashboard to see status

---

## Real-World Examples

### Example 1: Send Invoice

File: `vault/Needs_Action/PAYMENT_Invoice_2026-02-15.md.md`

```markdown
# Send Invoice to Client A

## Objective
Send invoice for Project Alpha work

## Description
Invoice for completed deliverables.
Client: ClientA
Email: client@example.com

## Priority
HIGH

## Type
PAYMENT

## Amount
1500
```

**What happens:**
1. ✓ Task detected
2. ✓ Plan generated
3. ✓ Approval requested ($1500 > $50)
4. ✓ Notification sent
5. ⏳ Waiting for approval via menu

### Example 2: Internal Process

File: `vault/Needs_Action/TASK_Monthly_Report_2026-02-15.md.md`

```markdown
# Generate Monthly Report

## Objective
Create monthly performance report

## Description
Compile metrics from all projects.
Include: revenue, completion rate, alerts.
Format: PDF and Excel

## Priority
MEDIUM

## Type
PROCESS
```

**What happens:**
1. ✓ Task detected
2. ✓ Plan generated
3. ✓ No approval needed (internal)
4. ✓ Listed in pending tasks
5. ✓ Tracked in dashboard

### Example 3: Critical Alert

File: `vault/Needs_Action/EMAIL_CRITICAL_2026-02-15.md.md`

```markdown
# CRITICAL: Server Outage

## Objective
Immediate server restoration

## Description
Main server down, clients affected.
Status: EMERGENCY

## Priority
CRITICAL

## Type
ALERT
```

**What happens:**
1. ✓ Task detected immediately
2. ✓ CRITICAL notification sent
3. ✓ Dashboard shows urgent alert
4. ✓ Priority handling
5. ⚠️ Requires immediate action

---

## Best Practices

### File Organization
✓ Use clear, descriptive names  
✓ Include dates in YYYY-MM-DD format  
✓ Separate words with underscores  
✓ Keep filenames < 50 characters  
✓ Always end with `.md.md`

### Task Creation
✓ Be specific in objectives  
✓ Set correct priority  
✓ Include relevant details  
✓ Add dollar amounts for payments  
✓ Use consistent formatting

### System Monitoring
✓ Check status daily: `python quick_status.py`  
✓ Review approvals weekly  
✓ Archive old tasks monthly  
✓ Update config seasonally  
✓ Check logs for errors

### Payment Safety
✓ Always verify amounts  
✓ Check approval trail  
✓ Use correct email addresses  
✓ Confirm before processing  
✓ Keep receipts

---

## Advanced Features

### Continuous Monitoring
Run in background with monitor mode:
```bash
python app.py monitor
```
- Checks every 5 minutes
- Auto-processes tasks
- Sends notifications
- Perfect for production

### Batch Processing
Add multiple tasks quickly:
```
vault/Needs_Action/TASK_1_2026-02-15.md.md
vault/Needs_Action/TASK_2_2026-02-15.md.md
vault/Needs_Action/TASK_3_2026-02-15.md.md
```
System processes all automatically.

### Status Snapshots
Save current state:
```bash
python app.py
# Option 7: Save Dashboard State
```
Creates `dashboard_state.json` for records.

### Approval Audit Trail
Check approval history:
```bash
cat approvals.json
```
See all approvals with timestamps and approver info.

---

## Support & Resources

### Documentation
- **README.md** - Complete system documentation
- **QUICKSTART.md** - Get started quickly
- **config.py** - Inline configuration comments
- **Business_Goals.md.md** - Goals and objectives
- **Company_Handbook.md.md** - Rules and procedures

### Key Commands
```bash
python app.py              # Interactive menu
python quick_status.py     # Quick status check
python app.py bootstrap    # Initialize
python app.py monitor      # Continuous monitoring
```

### Log Files
- Check `system_logs.txt` for system activity
- Review `approvals.json` for approval history
- See `dashboard_state.json` for latest status

### Error Handling
- Console shows all errors and warnings
- Check logs for detailed information
- System continues despite non-critical errors
- Critical errors require attention

---

## Next Steps

1. **Create Your First Task** (5 minutes)
   - Create a file in vault/Needs_Action/
   - Run `python quick_status.py`
   - See it appear in dashboard

2. **Handle an Approval** (3 minutes)
   - Create PAYMENT task ($100)
   - Run `python app.py`
   - Select option 4 to approve
   - Watch it move to Approved/ folder

3. **Monitor Continuously** (Setup once)
   - Run `python app.py monitor`
   - Let it run in background
   - Check status anytime with quick_status.py

4. **Customize Configuration** (Optional)
   - Edit config.py
   - Change approval thresholds
   - Adjust check intervals
   - Update business rules

5. **Scale Up**
   - Add more tasks
   - Create multiple projects
   - Build complex workflows
   - Automate your entire workflow

---

## Version Information

- **System:** Personal AI Employee
- **Version:** 1.0.0
- **Released:** February 15, 2026
- **Status:** Production Ready
- **Python:** 3.8+
- **License:** Personal Use

---

## Questions?

Check the detailed docs:
- **README.md** for complete reference
- **QUICKSTART.md** for quick start
- **config.py** for settings
- **Source code** for implementation details

Your Personal AI Employee is ready to work!

🚀 **Start now:** `python quick_status.py`