# 🚀 Quick Start Guide - Personal AI Employee

## 5-Minute Setup

### Step 1: Verify Installation ✓
The system is already installed and tested. Your Python environment is ready.

### Step 2: Create Your First Task (2 min)
Create a new task file in the `vault/Needs_Action/` folder:

**File:** `vault/Needs_Action/EMAIL_ClientA_2026-02-15.md.md`

**Content:**
```markdown
# Send Invoice to Client A

## Objective
Send updated invoice to ClientA for Project Alpha

## Description
Prepare and send invoice for completed work on Project Alpha.
Client email: clienta@example.com
Amount: $2500

## Priority
HIGH

## Type
PAYMENT

## Amount
2500
```

### Step 3: Run the System (1 min)
```bash
python app.py
```

This opens the interactive menu. Select:
- **Option 1:** View Dashboard (see your new task)
- **Option 2:** View Pending Tasks
- **Option 6:** View System Status

### Step 4: See It In Action (2 min)
- Dashboard shows your task
- Plan automatically generated in `vault/Plans/`
- Approval requested (shown in dashboard)
- All tracked in real-time

## Common Commands

### Quick Status (No Menu)
```bash
python quick_status.py
```
Shows dashboard and exits - perfect for checking status

### Interactive Management
```bash
python app.py
```
Full menu with all options

### Continuous Monitoring
```bash
python app.py monitor
```
Runs every 5 minutes, Ctrl+C to stop

## What Happens Automatically

When you add a task file to `vault/Needs_Action/`:

1. **✓ Auto-Detected** → System finds the task
2. **✓ Auto-Analyzed** → Reads and categorizes
3. **✓ Plan Generated** → Creates action plan in `vault/Plans/`
4. **✓ Approval Requested** → For payments/critical tasks
5. **✓ Notifications Sent** → Alerts appear in dashboard
6. **✓ Status Tracked** → All changes logged

## Task File Template

Create files like this in `vault/Needs_Action/`:

```markdown
# [TASK TITLE]

## Objective
[What needs to be done]

## Description
[Details about the task]

## Priority
CRITICAL | HIGH | MEDIUM | LOW

## Type
PAYMENT | PROCESS | EMAIL | OTHER

## Amount
[If payment, add amount like: 500]
```

## File Naming Convention
- Start with task type: `EMAIL_`, `TASK_`, `PLAN_`, `PAYMENT_`
- Add client/project: `ClientA`, `ProjectAlpha`
- Add date: `2026-02-15`
- Full example: `EMAIL_ClientA_2026-02-15.md.md`

## Directory Structure Explained

```
vault/
├── Needs_Action/      ← PUT NEW TASKS HERE
├── Plans/             ← Auto-generated plans
├── Pending_Approval/  ← Tasks waiting approval
├── Approved/          ← Approved tasks (auto-moved)
└── Done/              ← Completed tasks (auto-moved)
```

## Example Workflow

### Step-by-Step Example

**1. Create Task File**
```
NAME: vault/Needs_Action/PAYMENT_Invoice_2026-02-15.md.md

CONTENT:
# Send Invoice

Objective: Send invoice for $500

Priority: HIGH
Type: PAYMENT
Amount: 500
```

**2. Run System**
```bash
python quick_status.py
```

**3. System Automatically:**
- ✓ Loads task
- ✓ Creates plan: `vault/Plans/PLAN_PAYMENT_Invoice_2026-02-15.md`
- ✓ Creates approval request (< $50 auto-approves)
- ✓ Shows in dashboard
- ✓ Sends notifications

**4. View Details**
```bash
python app.py
# Select option 2: View Pending Tasks
# Select option 3: View Pending Approvals
# Select option 1: Refresh Dashboard
```

## Dashboard Sections

### Task Summary
- Total Tasks
- Pending
- Awaiting Approval
- Completed

### Approvals
- Pending (need action)
- Approved
- Rejected

### Health Status
- Completion Rate
- Backlog
- Recommendations

### Recent Activity
- Last task created
- Last approvals
- System alerts

## Approval Workflow

### Automatic Approval
- Amount < $50 → Auto-approve ✓
- No action needed!

### Needs Approval
- Amount $50-1000 → Requests approval
- Go to menu option 4
- Review and approve/reject

### Senior Approval
- Amount > $1000 → Needs senior review
- Still managed through menu system

## Customization

Edit `config.py` to change:
- Check intervals (default: 5 min)
- Approval thresholds (default: $50 auto-approve)
- Spending limits (daily/weekly/monthly)
- Log settings
- Priorities

Example:
```python
# config.py
APPROVAL_RULES = {
    "auto_approve_below_amount": 50,  # Change this
    "urgent_notification_threshold_hours": 2
}
```

## Troubleshooting

### No Tasks Showing?
1. Check task file in `vault/Needs_Action/`
2. Verify filename ends with `.md.md`
3. Run `python quick_status.py` again

### Approvals Not Working?
1. Check approval system loaded (app.py bootstrap)
2. Verify amount format in task file
3. Check `approvals.json` in root folder

### System Not Starting?
1. Verify Python 3.8+ installed: `python --version`
2. Ensure all .py files in root folder
3. Check folder permissions for vault/

## Key Files

### Core System
- `app.py` - Main application
- `config.py` - Settings
- `task_manager.py` - Task tracking
- `approval_system.py` - Approvals
- `plan_generator.py` - Plan creation
- `dashboard.py` - Status monitoring
-`notification_system.py` - Alerts

### Data Files
- `approvals.json` - Approval history
- `dashboard_state.json` - Latest status
- `Business_Goals.md.md` - Business objectives
- `Company_Handbook.md.md` - Rules
- `Dashboard.md.md` - Dashboard overview

### Scripts
- `run.bat` - Windows launcher
- `quick_status.py` - Quick check
- `status.bat` - Windows quick check

### Vault (Task Storage)
- `vault/Needs_Action/` - New tasks
- `vault/Plans/` - Generated plans
- `vault/Approved/` - Approved tasks
- `vault/Done/` - Completed tasks

## Next Steps

1. **Create Your First Task**
   - Follow "Step 2" above
   - Create EMAIL or PAYMENT task

2. **Run the System**
   - `python app.py`
   - View dashboard
   - See automatic processing

3. **Handle Approvals**
   - Menu option 4 to approve
   - Watch task move to approved folder

4. **Monitor Progress**
   - `python quick_status.py` anytime
   - Check `dashboard_state.json`
   - Read generated plans

5. **Customize**
   - Edit `config.py` for your needs
   - Adjust approval thresholds
   - Set check intervals

## Support & Tips

### Pro Tips
- Add multiple tasks, system processes all
- Check `vault/Plans/` for detailed action plans
- Approvals auto-saved for audit
- Use CRITICAL priority for urgent items
- Payment type auto-detects amounts

### Common Task Types
- **PAYMENT:** `Amount: 500` → Auto-creates invoice
- **EMAIL:** Outgoing client communication
- **PROCESS:** Internal workflow task
- **REPORT:** Generate and send reports

### Best Practices
1. Use clear task titles
2. Include all relevant details
3. Set correct priority level
4. Add dollar amounts for payments
5. Update status regularly

---

**You're Ready!** 🎉

Your Personal AI Employee system is fully operational. Start by creating a task file and running `python app.py` to see it in action!

**Questions?** Check the README.md for detailed documentation.