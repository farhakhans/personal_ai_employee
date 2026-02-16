"""
OPERATIONS GUIDE & DEPLOYMENT
═══════════════════════════════════════════════════════════════════════════

Complete guide for deploying and operating the resilient AI Employee system
in production with error recovery, retry logic, graceful degradation, and
watchdog monitoring.

Components:
1. error_recovery.py - Intelligent error handling
2. retry_logic.py - Retry with exponential backoff
3. graceful_degradation.py - Feature degradation
4. watchdog_monitor.py - Process health monitoring
5. system_orchestrator.py - Unified orchestration
"""


# ═══════════════════════════════════════════════════════════════════════
# DEPLOYMENT CHECKLIST
# ═══════════════════════════════════════════════════════════════════════

PRODUCTION_CHECKLIST = """
PRODUCTION DEPLOYMENT CHECKLIST
═══════════════════════════════════════════════════════════════════════

PRE-DEPLOYMENT
──────────────
☐ All integration tests passing (test_resilience.py)
☐ Error recovery framework initialized
☐ Retry logic configured for APIs (check max_retries, max_delay)
☐ Graceful degradation handlers registered for each component
☐ Watchdog monitor configured with all processes
☐ Vault directory structure exists (System/errors, System/recovery, etc)
☐ Vault/.gitignore configured to ignore sensitive logs
☐ Logging set up (logs directory exists, rotation configured)
☐ HITL framework enabled and reviewed
☐ Emergency alert procedures documented
☐ Monitoring dashboard URL bookmarked

DEPLOYMENT
──────────
☐ Pull latest code
☐ Run: python test_resilience.py (verify all tests pass)
☐ Run: python system_orchestrator.py (verify orchestrator initializes)
☐ Run: python watchdog_monitor.py --status (verify watchdog ready)
☐ Start watchdog: python watchdog_monitor.py --start
☐ Verify dashboard: Vault/Reports/watchdog_dashboard.html
☐ Verify orchestrator dashboard: Vault/Reports/orchestrator_dashboard.html
☐ Configure health check interval (default: 10 seconds)
☐ Review error logs (should be mostly empty on healthy startup)

POST-DEPLOYMENT (First 24 hours)
────────────────────────────────
☐ Monitor error rates (should be near 0)
☐ Monitor retry success rate (should be > 95% or investigate)
☐ Check for false positive alerts
☐ Verify watchdog is catching process crashes
☐ Verify recovery strategies working as intended
☐ No unhandled exceptions in logs
☐ Dashboard updates every check_interval (60 seconds default)

ONGOING OPERATIONS (Daily)
──────────────────────────
☐ Review metrics (Vault/System/metrics/{date}.json)
☐ Check dead letter queue (Vault/System/dead_letter/)
☐ Monitor retry success rate trend
☐ Process any pending manual interventions
☐ Review degradation notices in Vault/System/
☐ Archive old logs (keep last 30 days)
☐ Update escalation contacts in HITL framework
☐ Test recovery procedures monthly


ROLLBACK PROCEDURE
──────────────────
If system unstable after deployment:

1. Stop watchdog: Kill watchdog process
2. Kill all watcher processes manually
3. Check latest errors: tail Vault/System/logs/orchestrator.log
4. Revert code to previous version
5. Review error in test environment
6. Deploy fix
7. Re-run integration tests
8. Restart watchdog

"""

# ═══════════════════════════════════════════════════════════════════════
# CONFIGURATION GUIDE
# ═══════════════════════════════════════════════════════════════════════

CONFIGURATION_GUIDE = """
CONFIGURATION GUIDE
═══════════════════════════════════════════════════════════════════════

1. ERROR RECOVERY CONFIGURATION
────────────────────────────────

error_recovery = ErrorRecoveryFramework(vault_path)

Error Severity Levels:
  • INFO - Informational, no action
  • WARNING - Warning, but system OK
  • ERROR - Error, but recoverable
  • CRITICAL - Major failure, needs attention
  • FATAL - System halt required

Recovery Strategies:
  • AUTO_RETRY - Retry with exponential backoff (ConnectionError, Timeout)
  • MANUAL_INTERVENTION - Queue for human review (AuthError, Unauthorized)
  • FALLBACK - Switch to alternate implementation (optional)
  • DEGRADE - Continue with reduced functionality (preferred over abort)
  • ABORT - Fatal error, system shutdown
  • DEAD_LETTER - Queue for later retry when system recovers


2. RETRY LOGIC CONFIGURATION
──────────────────────────────

from retry_logic import RetryConfig, BackoffStrategy

# Standard API retry (3 retries, exponential backoff 1-32 seconds)
config = RetryConfig(
    max_retries=3,              # Don't retry forever
    initial_delay=1.0,          # Start with 1 second
    max_delay=32.0,             # Cap at 32 seconds
    backoff_strategy=BackoffStrategy.EXPONENTIAL_JITTER  # Prevents thundering herd
)

# Rate-limited API (5 retries, longer delays to respect rate limit)
config = RetryConfig(
    max_retries=5,
    initial_delay=2.0,
    max_delay=120.0,            # Wait up to 2 minutes
    backoff_strategy=BackoffStrategy.EXPONENTIAL
)

# Database connection (shorter delays, quick failover)
config = RetryConfig(
    max_retries=2,
    initial_delay=0.5,
    max_delay=5.0,
    backoff_strategy=BackoffStrategy.LINEAR
)


3. GRACEFUL DEGRADATION CONFIGURATION
───────────────────────────────────────

from graceful_degradation import GracefulDegradationHandler

degradation = GracefulDegradationHandler(vault_path)

# Register handlers for specific components
degradation.degrade_feature(
    feature_name="Email Sending",    # Client-facing feature name
    component="gmail_watcher",        # Internal component
    reason="Gmail API rate limit",    # Why it's degraded
    degradation_level="reduced",      # FULL_SERVICE, REDUCED, DEGRADED, MINIMAL
    estimated_recovery=300            # Seconds until recovery expected
)

When degraded:
  ✓ System continues running
  ✓ User notices appear in Vault/System/
  ✓ Alternative workflows available (manual queue, fallback UI)
  ✓ Dashboard shows degraded status
  ✗ That specific feature is unavailable


4. WATCHDOG MONITOR CONFIGURATION
───────────────────────────────────

from watchdog_monitor import WatchdogMonitor, ProcessConfig

watchdog = WatchdogMonitor(
    vault_path=vault_path,
    check_interval=10.0        # Check every 10 seconds
)

# Register process
config = ProcessConfig(
    name="Email Watcher",
    command=["python", "gmail_watcher.py"],
    working_dir=".",
    restart_on_failure=True,
    max_restart_attempts=5,     # Stop after 5 crashes
    restart_delay=10.0          # Wait 10 seconds before restarting
)

watchdog.register_process(config)
watchdog.start_all()

Watchdog will:
  ✓ Monitor process health every check_interval
  ✓ Auto-restart if process crashes (up to max_restart_attempts)
  ✓ Run health checks (custom command if configured)
  ✓ Update dashboard every cycle
  ✓ Alert if process exceeds restart attempts


5. SYSTEM ORCHESTRATOR CONFIGURATION
──────────────────────────────────────

from system_orchestrator import create_integrated_orchestrator

# Create orchestrator with all modules
orchestrator = create_integrated_orchestrator(vault_path)

# Handle component error (main entry point)
result = orchestrator.handle_component_error(
    component="email_watcher",
    error=ConnectionError("Gmail API unreachable"),
    context={"attempt": 1, "timestamp": "2024-02-13T10:30:00"},
    severity="ERROR"
)

# Check system health
health = orchestrator.get_system_health()  # HEALTHY, DEGRADED, CRITICAL, RECOVERING

# Get metrics
metrics = orchestrator.get_metrics()
print(f"Uptime: {metrics.uptime_seconds}s")
print(f"Errors: {metrics.error_count}")
print(f"Retry success rate: {metrics.retry_success_rate:.1f}%")

# Process dead letter queue (retry failed operations)
result = orchestrator.process_dead_letter_queue()
print(f"Processed {result['processed']} items, {result['succeeded']} succeeded")

# Generate dashboards
orchestrator.save_dashboard()   # Vault/Reports/orchestrator_dashboard.html
orchestrator.save_metrics()     # Vault/System/metrics/{timestamp}.json


"""

# ═══════════════════════════════════════════════════════════════════════
# PRODUCTION STARTUP SCRIPT
# ═══════════════════════════════════════════════════════════════════════

STARTUP_SCRIPT = """
#!/bin/bash
# startup.sh - Start AI Employee system with all resilience features

set -e  # Exit on error

echo "🤖 AI Employee System Startup"
echo "════════════════════════════════"
echo ""

# Check dependencies
echo "✓ Checking dependencies..."
python --version
python -c "import psutil; print(f'psutil: {psutil.__version__}')"

# Create vault structure
echo "✓ Creating vault directories..."
mkdir -p Vault/System/{logs,errors,recovery,dead_letter,degradation,metrics,watchdog}
mkdir -p Vault/Reports
mkdir -p Vault/Approvals

# Run integration tests
echo "✓ Running integration tests..."
python test_resilience.py --verbose

if [ $? -ne 0 ]; then
    echo "✗ Integration tests failed, aborting startup"
    exit 1
fi

echo "✓ Tests passed"
echo ""

# Start watchdog in background
echo "Starting Watchdog Monitor..."
nohup python watchdog_monitor.py --start > Vault/System/logs/watchdog.out 2>&1 &
WATCHDOG_PID=$!
echo "✓ Watchdog started (PID: $WATCHDOG_PID)"

# Wait for watchdog to initialize
sleep 2

# Check watchdog status
echo "✓ Verifying watchdog..."
python watchdog_monitor.py --status

# Generate initial dashboards
echo "✓ Generating dashboards..."
python system_orchestrator.py

# Save PID for later shutdown
echo $WATCHDOG_PID > .watchdog_pid

echo ""
echo "════════════════════════════════"
echo "✓ System Started Successfully"
echo ""
echo "Dashboards:"
echo "  • Vault/Reports/watchdog_dashboard.html"
echo "  • Vault/Reports/orchestrator_dashboard.html"
echo ""
echo "Logs:"
echo "  • Vault/System/logs/orchestrator.log"
echo "  • Vault/System/logs/watchdog.log"
echo ""
echo "Metrics:"
echo "  • Vault/System/metrics/"
echo ""
echo "To stop system: bash shutdown.sh"
echo ""

"""

# ═══════════════════════════════════════════════════════════════════════
# PRODUCTION SHUTDOWN SCRIPT
# ═══════════════════════════════════════════════════════════════════════

SHUTDOWN_SCRIPT = """
#!/bin/bash
# shutdown.sh - Graceful system shutdown

echo "🛑 AI Employee System Shutdown"
echo "════════════════════════════════"
echo ""

# Read watchdog PID
if [ -f .watchdog_pid ]; then
    WATCHDOG_PID=$(cat .watchdog_pid)
    echo "Stopping Watchdog Monitor (PID: $WATCHDOG_PID)..."
    
    # Try graceful shutdown
    kill -TERM $WATCHDOG_PID 2>/dev/null || true
    
    # Wait for process to exit
    sleep 2
    
    # Force kill if still running
    kill -KILL $WATCHDOG_PID 2>/dev/null || true
    
    rm .watchdog_pid
    echo "✓ Watchdog stopped"
else
    echo "⚠ No watchdog PID file found"
fi

# Generate final metrics
echo "✓ Saving final metrics..."
python -c "
from system_orchestrator import create_integrated_orchestrator
from pathlib import Path
orchestrator = create_integrated_orchestrator(Path('Vault'))
orchestrator.save_metrics()
print('  Metrics saved to Vault/System/metrics/')
"

echo ""
echo "════════════════════════════════"
echo "✓ System Stopped"
echo ""

"""

# ═══════════════════════════════════════════════════════════════════════
# COMMON OPERATIONS & TROUBLESHOOTING
# ═══════════════════════════════════════════════════════════════════════

OPERATIONS_GUIDE = """
COMMON OPERATIONS & TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════

1. CHECK SYSTEM STATUS
──────────────────────

python watchdog_monitor.py --status
# Shows: Process name, Status, PID, Started time, Restarts, Health check

python system_orchestrator.py
# Shows: Health status, Uptime, Error counts, Retry rate, Degraded features


2. RESTART A SPECIFIC PROCESS
──────────────────────────────

python watchdog_monitor.py --restart "Email Watcher"
# Gracefully stops email watcher, waits 2 seconds, restarts it


3. VIEW RECENT ERRORS
─────────────────────

# Last 50 errors
tail -50 Vault/System/logs/orchestrator.log

# Errors from today
grep "$(date +%Y-%m-%d)" Vault/System/logs/orchestrator.log | grep ERROR

# Critical errors
grep CRITICAL Vault/System/logs/orchestrator.log | tail -20


4. PROCESS DEAD LETTER QUEUE
─────────────────────────────

# Check size
ls Vault/System/dead_letter/ | wc -l

# View pending items
cat Vault/System/dead_letter/COMPONENT_*.json | head -3

# Manually retry all
python -c "
from system_orchestrator import create_integrated_orchestrator
from pathlib import Path
orchestrator = create_integrated_orchestrator(Path('Vault'))
result = orchestrator.process_dead_letter_queue()
print(f'Processed: {result[\"processed\"]}, Succeeded: {result[\"succeeded\"]}')
"


5. VIEW DEGRADED FEATURES
──────────────────────────

cat Vault/System/degradation/current_degradation.json

# Shows: Lists all degraded features, why, estimated recovery


6. MANUAL INTERVENTION REQUESTS
───────────────────────────────

# List pending interventions
ls Vault/System/recovery/*.md

# Review intervention
cat Vault/System/recovery/INTERVENTION_*.md

# After fixing issue
# 1. Fix the problem
# 2. Run: python orchestrator.py --resolve-intervention INTERVENTION_ID
# 3. System will retry


7. ANALYZE METRICS
──────────────────

# View latest metrics
cat Vault/System/metrics/metrics_*.json | tail -1 |python -m json.tool

# Key metrics to monitor:
# - uptime_seconds: Should be increasing
# - error_count: Should be low and stable
# - retry_success_rate: Should be > 95%
# - degraded_features_count: Should be 0 in healthy state
# - dead_letter_queue_size: Should be low


8. TROUBLESHOOTING GUIDE
────────────────────────

Problem: Watchdog shows process keeps restarting
Solution:
  1. Check process logs: Vault/System/logs/{component}.log
  2. Look for recurring errors
  3. If auth error: Refresh credentials
  4. If network error: Check connectivity
  5. If database error: Check database status
  6. Increase max_restart_attempts if transient

Problem: High error rate (> 10% errors)
Solution:
  1. Check for external service outages (Gmail API, payment gateway)
  2. Check network connectivity
  3. Review error types in logs
  4. If rate-limited: Add delays, reduce request volume
  5. If auth: Refresh credentials
  6. Escalate P1 with context to on-call

Problem: System stuck in DEGRADED state
Solution:
  1. Check Vault/System/degradation/current_degradation.json
  2. Verify the underlying service is actually working
  3. Manually run health check: python health_check.py
  4. If health check passes: python orchestrator.py --recover-feature FEATURE_NAME
  5. If still fails: Escalate

Problem: Dead letter queue growing
Solution:
  1. Check oldest item: ls -lt Vault/System/dead_letter/ | tail -1
  2. If older than 1 hour: Likely permanent failure
  3. Review error message to determine if fixable
  4. For networking issues: Run process_dead_letter_queue() later
  5. For permanent failures: Remove from queue and document


9. ESCALATION CONTACTS
──────────────────────

On-Call Engineer: Check CONTACTS.md
Manager: 
Vendor Support URLs:
  • Gmail API: support.google.com
  • Payment Gateway: Check docs
  • Hosting: Check provider


10. DISASTER RECOVERY
─────────────────────

Data Loss Protection:
  ✓ All errors logged to Vault
  ✓ Dead letter queue stores unprocessed operations
  ✓ Metrics saved every check_interval
  ✓ Git backup of vault
  ✓ All failures recoverable using dead_letter queue

If System Crashes:
  1. Check .watchdog_pid exists
  2. Kill any orphaned processes: pkill -f "watchdog_monitor\|gmail_watcher"
  3. Run startup.sh to restart

If Vault Corrupted:
  1. Stop system: bash shutdown.sh
  2. Restore from git: git checkout HEAD Vault/
  3. Restart: bash startup.sh

"""

# ═══════════════════════════════════════════════════════════════════════
# MONITORING CHECKLIST
# ═══════════════════════════════════════════════════════════════════════

MONITORING_CHECKLIST = """
MONITORING CHECKLIST (Daily)
═══════════════════════════════════════════════════════════════════════

Dashboard Checks
└─ 09:00 AM - Review overnight metrics
   ├─ Uptime: Should be 24h or more
   ├─ Error rate: Should be < 1%
   ├─ Retry success rate: Should be > 95%
   └─ Degraded features: Should be 0 (if 0, all good)

└─ Hourly - Check watchdog monitor
   ├─ Open: Vault/Reports/watchdog_dashboard.html
   ├─ Verify: All processes showing "running"
   ├─ Check: Restart count low (< 5 per process)
   └─ Alert: If any process stuck in "restarting"

└─ 12:00 PM - Check dead letter queue
   ├─ Count items: ls Vault/System/dead_letter/ | wc -l
   ├─ Alert if: > 10 items older than 1 hour
   ├─ Review: Sample 1-2 items to see error type
   └─ Action: Process queue if network recovered

└─ 05:00 PM - Weekly metrics backup
   ├─ Archive: cp -r Vault/System/metrics/ backups/metrics_$(date +%Y%m%d)
   ├─ Compress: gzip backups/metrics_*.tar.gz
   ├─ Upload: To backup storage
   └─ Verify: 7+ days of backup local

Error Log Review
└─ 09:15 AM
   ├─ Errors yesterday: wc -l Vault/System/logs/orchestrator.log
   ├─ New error types: grep ERROR Vault/System/logs/orchestrator.log | sort | uniq -c
   ├─ CRITICAL count: grep CRITICAL Vault/System/logs/orchestrator.log | wc -l
   └─ Investigation: Any pattern in error times?

Process Health
└─ Each hour (08:00-18:00)
   ├─ Gmail watcher response time
   ├─ File watcher poll count
   ├─ Payment processing latency
   ├─ API response times
   └─ Database query times

External Dependencies
└─ 09:30 AM
   ├─ Gmail API status: Check google.com/appsstatus
   ├─ Payment gateway: Check provider status page
   ├─ Database connectivity
   ├─ Network connectivity
   └─ Update Vault/System/DEPENDENCIES.txt if issues

Escalation
└─ If any of:
   ├─ Error count > 100 in 1 hour
   ├─ Retry success rate < 80%
   ├─ Critical error count > 5
   ├─ Process restarted > 10 times
   └─ Dead letter queue > 50 items
   
   Then: ESCALATE to on-call engineer with context


"""

# ═══════════════════════════════════════════════════════════════════════
# MAIN GUIDE
# ═══════════════════════════════════════════════════════════════════════

MAIN_GUIDE = """

╔═══════════════════════════════════════════════════════════════════════════╗
║                  AI EMPLOYEE SYSTEM - OPERATIONS GUIDE                    ║
║              Resilient Error Handling & Recovery System                  ║
╚═══════════════════════════════════════════════════════════════════════════╝


SYSTEM ARCHITECTURE
───────────────────

When Component Fails:
  
  1. Error Occurs
     └─ Exception thrown in component (gmail_watcher, file_watcher, etc)
  
  2. Error Recovery Catches It
     └─ Classifies by type: ConnectionError → Retry, AuthError → Manual, etc
     └─ Logs to Vault/System/errors/
  
  3. Recovery Strategy Executes
     ├─ AUTO_RETRY: Exponential backoff (1s, 2s, 4s, 8s...)
     ├─ MANUAL_INTERVENTION: Escalate to human
     ├─ DEGRADE: Feature limited, continue operation
     ├─ FALLBACK: Use alternate implementation
     ├─ DEAD_LETTER: Queue for later retry
     └─ ABORT: Fatal, shutdown system
  
  4. Retry Logic (if AUTO_RETRY)
     └─ Backoff strategies: Linear, Exponential, Exponential+Jitter, Decorrelated
     └─ Configurable max retries and max delay
     └─ Tracks success rate for metrics
  
  5. Graceful Degradation (if retries fail)
     └─ Feature marked as degraded
     └─ System continues with reduced functionality
     └─ User notices created in Vault/System/
  
  6. Watchdog Monitoring
     └─ Monitors process health every 10 seconds
     └─ Auto-restarts crashed processes (up to 5 times)
     └─ Updates dashboard
  
  7. System Orchestrator
     └─ Coordinates all components
     └─ Collects metrics
     └─ Manages system health status
     └─ Generates dashboards


QUICK START
───────────

Start production system with all resilience features:

  $ bash startup.sh
  
This will:
  ✓ Check all dependencies
  ✓ Run integration tests
  ✓ Start watchdog monitor
  ✓ Generate dashboards
  ✓ Ready for operations

Monitor in real-time:
  ✓ Open: Vault/Reports/watchdog_dashboard.html
  ✓ Refresh every 60 seconds to see updates


RECOVERY TIME OBJECTIVES
────────────────────────

Transient failures (network glitch, rate limit):
  └─ Recovery Time: 5-30 seconds (handled by retry logic)

Service degradation (API overloaded):
  └─ Recovery Time: 1-5 minutes (watchdog monitors, alerts on degradation)

Service outage (API down, database offline):
  └─ Recovery Time: 5-60 minutes (dead letter queue holds operations)
  └─ Manual review: Check EMERGENCY_ALERT.txt

Unrecoverable failures:
  └─ Recovery Time: Manual intervention required
  └─ Review: Vault/System/recovery/*.md intervention requests


KEY FILES & LOCATIONS
─────────────────────

Source Code:
  • error_recovery.py - Intelligent error classification & recovery
  • retry_logic.py - Retry with 4 backoff algorithms
  • graceful_degradation.py - Feature degradation handler
  • watchdog_monitor.py - Process monitoring & auto-restart
  • system_orchestrator.py - Unified orchestration

Logs:
  • Vault/System/logs/orchestrator.log - Main system log
  • Vault/System/logs/watchdog.log - Watchdog activity
  • Vault/System/logs/*.log - Component-specific logs

Storage:
  • Vault/System/errors/ - Captured errors
  • Vault/System/recovery/ - Intervention requests
  • Vault/System/dead_letter/ - Queued operations for retry
  • Vault/System/degradation/ - Feature degradation state
  • Vault/System/metrics/ - Historical metrics

Dashboards:
  • Vault/Reports/watchdog_dashboard.html - Process health
  • Vault/Reports/orchestrator_dashboard.html - System health

Configuration:
  • .env - Credentials & settings
  • config.json - System configuration


SUCCESS CRITERIA
────────────────

System is healthy when:
  ✓ Error rate < 1%
  ✓ Retry success rate > 95%
  ✓ All processes showing "running"
  ✓ 0 degraded features
  ✓ Dead letter queue < 5 items
  ✓ Process restarts < 2 per day
  ✓ No unhandled exceptions in logs


TROUBLESHOOTING
────────────────

See: OPERATIONS_GUIDE section below


NEED HELP?
──────────

1. Check logs: tail -100 Vault/System/logs/orchestrator.log
2. Review current status: python watchdog_monitor.py --status
3. Check dashboards: Open HTML files in Vault/Reports/
4. See full guide: This document


"""

# Print main guide
if __name__ == "__main__":
    print(MAIN_GUIDE)
    print("\n" + "=" * 75)
    print("FULL OPERATIONS GUIDE SECTIONS")
    print("=" * 75)
    print("\n1. PRODUCTION CHECKLIST")
    print("2. CONFIGURATION GUIDE")
    print("3. STARTUP SCRIPT (startup.sh)")
    print("4. SHUTDOWN SCRIPT (shutdown.sh)")
    print("5. COMMON OPERATIONS & TROUBLESHOOTING")
    print("6. MONITORING CHECKLIST")
    print("\n" + "=" * 75)
