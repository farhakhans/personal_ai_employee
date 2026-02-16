# 📖 Company Handbook & Operational Guidelines

## Core Operating Rules

### 1. Task Processing
- ✓ **Always check `/vault/Needs_Action` folder FIRST** before any action
- ✓ Process tasks in priority order: CRITICAL → HIGH → MEDIUM → LOW
- ✓ Load existing task history before starting new tasks
- ✓ Create comprehensive plan for each task before execution

### 2. Approval Requirements
- ✓ **NEVER send payment without explicit approval**
- ✓ Obtain written approval for all expenses over $50
- ✓ For payments over $1,000, get senior approval
- ✓ Document all approval decisions in approval system
- ✓ Maintain audit trail for all financial transactions

### 3. Communication & Alerts
- ✓ **Flag any urgent/critical messages IMMEDIATELY**
- ✓ Send alerts for tasks overdue by more than 2 hours
- ✓ Notify immediately if critical system issues arise
- ✓ Provide unread notification count at dashboard
- ✓ Use emoji indicators for priority levels

### 4. Data Management
- ✓ Save all generated plans to `/vault/Plans/` folder
- ✓ Move completed tasks to `/vault/Done/` folder
- ✓ Keep approval records in `approvals.json`
- ✓ Maintain system logs for audit trail
- ✓ Backup dashboard state regularly

### 5. Business Rules
- ✓ Daily spending limit: $5,000
- ✓ Weekly spending limit: $15,000
- ✓ Monthly spending limit: $40,000
- ✓ Minimum auto-approval amount: < $50
- ✓ Maximum auto-approval amount: $50

## Workflow Procedures

### Task Lifecycle
1. **DETECTION** - New task added to `/vault/Needs_Action/`
2. **ANALYSIS** - System analyzes and categorizes task
3. **PLANNING** - Generates action plan automatically
4. **APPROVAL** - Requests human approval if needed
5. **EXECUTION** - Processes approved tasks
6. **COMPLETION** - Moves to `/vault/Done/` with confirmation
7. **ARCHIVE** - Maintains historical record

### Approval Process
1. Task flagged as requiring approval
2. Approval request created with unique ID
3. Notification sent to stakeholder
4. Stakeholder reviews and approves/rejects
5. Status updated in system
6. Task moves to appropriate folder
7. Confirmation sent to requestor

---

**Last Updated:** February 15, 2026
**Version:** 1.0
**Status:** ACTIVE
