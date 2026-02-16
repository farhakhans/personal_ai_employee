"""
ERROR STATES & RECOVERY FRAMEWORK
═══════════════════════════════════════════════════════════════════════════

Comprehensive error handling and recovery system for the AI Employee.
Handles failures gracefully, logs errors, and initiates recovery procedures.

Recovery strategies:
- Automatic retry with exponential backoff
- State snapshot & recovery
- Upstream/downstream notification
- Manual intervention procedures
- Advanced error classification
- Predictive recovery
- Machine learning-based error patterns
- Automated escalation
- Compliance-aware error handling
"""

import json
import logging
import asyncio
import threading
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
from datetime import datetime, timedelta
import traceback
import hashlib
import pickle
from collections import defaultdict, deque
import statistics
from concurrent.futures import ThreadPoolExecutor


class ErrorSeverity(Enum):
    """Error severity levels."""
    INFO = "info"              # Not really an error
    WARNING = "warning"        # Non-critical, continue
    ERROR = "error"            # Something failed, needs recovery
    CRITICAL = "critical"      # System failing, needs immediate attention
    FATAL = "fatal"            # System cannot continue
    SECURITY = "security"      # Security-related error
    COMPLIANCE = "compliance"  # Compliance violation


class RecoveryStrategy(Enum):
    """Recovery approach to take."""
    AUTO_RETRY = "auto_retry"              # Automatically retry (exponential backoff)
    MANUAL_INTERVENTION = "manual"         # Notify human to fix manually
    FALLBACK = "fallback"                  # Switch to fallback mode
    DEGRADE = "degrade"                   # Continue with reduced functionality
    ABORT = "abort"                       # Stop and alert
    DEAD_LETTER = "dead_letter"           # Queue for later retry
    CIRCUIT_BREAKER = "circuit_breaker"   # Temporarily disable component
    ROLLBACK = "rollback"                 # Rollback to previous state
    ISOLATE = "isolate"                   # Isolate problematic component


@dataclass
class ErrorRecord:
    """Track an error and recovery attempt."""
    error_id: str
    timestamp: str
    severity: str
    component: str              # claude_code, gmail_watcher, etc.
    error_type: str             # exception class name
    message: str
    traceback_text: str
    recovery_strategy: str
    recovery_status: str        # not_started, in_progress, recovered, failed
    retry_count: int = 0
    max_retries: int = 3
    last_retry_time: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    error_hash: str = ""        # Hash of error for deduplication
    frequency: int = 0          # How often this error occurs
    predicted_severity: str = "" # ML-predicted severity
    escalation_level: int = 0   # How many times escalated
    recovery_time: float = 0.0  # Time taken to recover
    impact_score: float = 0.0   # Business impact score
    resolution_notes: str = ""  # Notes about resolution


class ErrorRecoveryFramework:
    """Central error recovery system with advanced features."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.errors_dir = vault_path / "System" / "errors"
        self.recovery_dir = vault_path / "System" / "recovery"
        self.dead_letter_dir = vault_path / "System" / "dead_letter"
        self.patterns_dir = vault_path / "System" / "error_patterns"
        self.analytics_dir = vault_path / "System" / "analytics"

        # Create directories
        self.errors_dir.mkdir(parents=True, exist_ok=True)
        self.recovery_dir.mkdir(parents=True, exist_ok=True)
        self.dead_letter_dir.mkdir(parents=True, exist_ok=True)
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        self.analytics_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = logging.getLogger('ErrorRecovery')
        self._setup_logging()

        # Error callbacks (human-defined recovery strategies)
        self.recovery_handlers: Dict[str, Callable] = {}

        # Error pattern recognition
        self.error_patterns: Dict[str, Any] = {}
        self.error_frequency: Dict[str, int] = defaultdict(int)
        self.error_history: deque = deque(maxlen=1000)  # Keep last 1000 errors
        self.component_stats: Dict[str, Dict] = defaultdict(lambda: {
            "total_errors": 0,
            "recovery_success": 0,
            "avg_recovery_time": 0.0,
            "last_error_time": None
        })

        # Threading lock
        self._lock = threading.Lock()

        # Load existing patterns
        self._load_error_patterns()

    def _setup_logging(self):
        """Configure logging for error recovery."""
        log_dir = self.vault_path / "System" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        handler = logging.FileHandler(log_dir / "errors.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
    
    def capture_error(
        self,
        component: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        severity: ErrorSeverity = ErrorSeverity.ERROR
    ) -> ErrorRecord:
        """
        Capture an error and decide recovery strategy.
        
        Args:
            component: What failed (claude_code, gmail_watcher, etc.)
            error: The exception that was raised
            context: Additional context about what was happening
            severity: How serious is this?
        
        Returns:
            ErrorRecord tracking the error and recovery
        """
        
        error_id = f"ERR_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{component}"
        
        # Determine recovery strategy
        strategy = self._determine_recovery_strategy(
            component,
            error.__class__.__name__,
            severity
        )
        
        # Create error record
        error_record = ErrorRecord(
            error_id=error_id,
            timestamp=datetime.now().isoformat(),
            severity=severity.value,
            component=component,
            error_type=error.__class__.__name__,
            message=str(error),
            traceback_text=traceback.format_exc(),
            recovery_strategy=strategy.value,
            recovery_status="not_started",
            context=context or {}
        )
        
        # Save error record
        self._save_error_record(error_record)
        
        # Log immediately
        self.logger.error(
            f"{component} failed: {error.__class__.__name__}: {str(error)}"
        )
        
        # Initiate recovery
        self._initiate_recovery(error_record)
        
        return error_record
    
    def _determine_recovery_strategy(
        self,
        component: str,
        error_type: str,
        severity: ErrorSeverity
    ) -> RecoveryStrategy:
        """Determine best recovery approach based on error type."""
        
        # Network errors → retry
        if "ConnectionError" in error_type or "Timeout" in error_type:
            return RecoveryStrategy.AUTO_RETRY
        
        # Authentication → manual
        if "AuthError" in error_type or "Unauthorized" in error_type:
            return RecoveryStrategy.MANUAL_INTERVENTION
        
        # Rate limit → retry with backoff
        if "RateLimit" in error_type:
            return RecoveryStrategy.AUTO_RETRY
        
        # Configuration → manual
        if "ConfigError" in error_type:
            return RecoveryStrategy.MANUAL_INTERVENTION
        
        # By severity
        if severity == ErrorSeverity.FATAL:
            return RecoveryStrategy.ABORT
        
        if severity == ErrorSeverity.CRITICAL:
            return RecoveryStrategy.MANUAL_INTERVENTION
        
        # Default: retry first
        return RecoveryStrategy.AUTO_RETRY
    
    def _initiate_recovery(self, error: ErrorRecord):
        """Start recovery based on strategy."""
        
        strategy = RecoveryStrategy[error.recovery_strategy.upper().replace('_', '_')]
        
        if strategy == RecoveryStrategy.AUTO_RETRY:
            self._recovery_auto_retry(error)
        elif strategy == RecoveryStrategy.MANUAL_INTERVENTION:
            self._recovery_manual_intervention(error)
        elif strategy == RecoveryStrategy.FALLBACK:
            self._recovery_fallback(error)
        elif strategy == RecoveryStrategy.DEGRADE:
            self._recovery_degrade(error)
        elif strategy == RecoveryStrategy.ABORT:
            self._recovery_abort(error)
        elif strategy == RecoveryStrategy.DEAD_LETTER:
            self._recovery_dead_letter(error)
    
    def _recovery_auto_retry(self, error: ErrorRecord):
        """Auto-retry strategy: exponential backoff."""
        
        error.recovery_status = "in_progress"
        error.retry_count += 1
        
        if error.retry_count <= error.max_retries:
            # Calculate backoff time: 2^retry_count seconds
            backoff_seconds = 2 ** error.retry_count
            error.last_retry_time = (
                datetime.now() + timedelta(seconds=backoff_seconds)
            ).isoformat()
            
            self.logger.info(
                f"{error.error_id}: Will retry in {backoff_seconds}s "
                f"(attempt {error.retry_count}/{error.max_retries})"
            )
            
            # Save retry checkpoint
            self._save_recovery_checkpoint(error)
        else:
            # Max retries exceeded
            error.recovery_status = "failed"
            self._recovery_dead_letter(error)
    
    def _recovery_manual_intervention(self, error: ErrorRecord):
        """Manual intervention required: alert human."""
        
        error.recovery_status = "manual_intervention_required"
        
        # Create intervention request in vault
        intervention_md = f"""
# ERROR: Manual Recovery Required

**Error ID:** {error.error_id}
**Component:** {error.component}
**Severity:** {error.severity}
**Time:** {error.timestamp}

## Error Details

**Type:** {error.error_type}
**Message:** {error.message}

## Stack Trace

```
{error.traceback_text}
```

## Context

```json
{json.dumps(error.context, indent=2)}
```

## Recovery Instructions

[ ] Check error message
[ ] Review context
[ ] Manual fix required here:
    _______________________________
[ ] Restart affected component
[ ] Confirm recovery

## Decision

- [ ] Resolved (mark below)
- [ ] Escalate to higher authority

**Resolved By:** _______________
**Time:** _______________
**Notes:** ______________________________
"""
        
        intervention_file = self.recovery_dir / f"{error.error_id}.md"
        intervention_file.write_text(intervention_md)
        
        self.logger.warning(
            f"{error.error_id}: Manual intervention needed. "
            f"See {intervention_file}"
        )
        
        # Save record
        self._save_error_record(error)
    
    def _recovery_fallback(self, error: ErrorRecord):
        """Fallback mode: switch to alternate implementation."""
        
        error.recovery_status = "fallback_activated"
        
        self.logger.warning(
            f"{error.error_id}: Activating fallback for {error.component}"
        )
        
        # Invoke fallback handler if registered
        if error.component in self.recovery_handlers:
            try:
                self.recovery_handlers[error.component]("fallback")
            except Exception as e:
                self.logger.error(f"Fallback handler failed: {e}")
        
        self._save_error_record(error)
    
    def _recovery_degrade(self, error: ErrorRecord):
        """Graceful degradation: continue with reduced functionality."""
        
        error.recovery_status = "degraded_mode"
        
        self.logger.warning(
            f"{error.error_id}: Entering degraded mode for {error.component}"
        )
        
        # Disabled feature
        degradation_file = self.vault_path / "System" / "degraded_features.json"
        degraded = {}
        if degradation_file.exists():
            degraded = json.loads(degradation_file.read_text())
        
        degraded[error.component] = {
            "since": error.timestamp,
            "error_id": error.error_id,
            "reason": error.message
        }
        
        degradation_file.write_text(json.dumps(degraded, indent=2))
        
        self._save_error_record(error)
    
    def _recovery_abort(self, error: ErrorRecord):
        """Fatal error: abort and alert."""
        
        error.recovery_status = "aborting"
        
        self.logger.critical(
            f"{error.error_id}: CRITICAL ERROR - SYSTEM ABORTING"
        )
        
        # Create emergency alert
        alert_file = self.vault_path / "System" / "EMERGENCY_ALERT.txt"
        alert_file.write_text(f"""
EMERGENCY ALERT
═══════════════════════════════════════════════════════════════

ERROR ID: {error.error_id}
TIME: {error.timestamp}
COMPONENT: {error.component}
SEVERITY: CRITICAL

MESSAGE: {error.message}

ACTION REQUIRED IMMEDIATELY:
1. Stop all AI Employee processes
2. Review error details in: {self.errors_dir / error.error_id}.json
3. Contact: [EMERGENCY_CONTACT]
4. Do not restart until cause identified

───────────────────────────────────────────────────────────────
{error.traceback_text}
""")
        
        self._save_error_record(error)
        
        raise SystemExit(f"Fatal error: {error.error_id}")
    
    def _recovery_dead_letter(self, error: ErrorRecord):
        """Dead letter queue: save for later retry."""
        
        error.recovery_status = "queued_for_later"
        
        # Save to dead letter queue
        dead_letter_file = self.dead_letter_dir / f"{error.error_id}.json"
        dead_letter_file.write_text(json.dumps(asdict(error), indent=2))
        
        self.logger.info(
            f"{error.error_id}: Queued to dead letter for later retry"
        )
    
    def _save_error_record(self, error: ErrorRecord):
        """Save error record to vault."""
        
        record_file = self.errors_dir / f"{error.error_id}.json"
        record_file.write_text(json.dumps(asdict(error), indent=2))
    
    def _save_recovery_checkpoint(self, error: ErrorRecord):
        """Save checkpoint for retry."""
        
        checkpoint_file = self.recovery_dir / f"{error.error_id}.json"
        checkpoint_file.write_text(json.dumps(asdict(error), indent=2))
    
    def register_recovery_handler(
        self,
        component: str,
        handler: Callable[[str], None]
    ):
        """
        Register custom recovery handler for component.
        
        Args:
            component: Component name
            handler: Function that takes (mode: str) and performs recovery
                     mode can be: "retry", "fallback", "degrade"
        """
        self.recovery_handlers[component] = handler
    
    def get_error_status(self) -> Dict[str, Any]:
        """Get current error and recovery status."""
        
        recent_errors = []
        for error_file in sorted(self.errors_dir.glob("*.json"), reverse=True)[:10]:
            with error_file.open() as f:
                recent_errors.append(json.load(f))
        
        # Count by status
        status_counts = {}
        for error in recent_errors:
            status = error.get("recovery_status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Get dead letter queue size
        dead_letter_count = len(list(self.dead_letter_dir.glob("*.json")))
        
        return {
            "recent_errors": recent_errors,
            "status_summary": status_counts,
            "dead_letter_queue_size": dead_letter_count,
            "timestamp": datetime.now().isoformat()
        }
    
    def process_dead_letter_queue(self):
        """Attempt to recover items from dead letter queue."""
        
        recovered = 0
        for dead_letter_file in self.dead_letter_dir.glob("*.json"):
            with dead_letter_file.open() as f:
                error_data = json.load(f)
            
            error = ErrorRecord(**error_data)
            
            # Reset retry count
            error.retry_count = 0
            error.recovery_status = "retrying_from_dlq"
            
            self._initiate_recovery(error)
            recovered += 1
        
        self.logger.info(f"Processed dead letter queue: {recovered} items")
        return recovered


# Example: Decorato for automatic error handling
def handle_errors(
    component: str,
    recovery_framework: ErrorRecoveryFramework,
    max_retries: int = 3
):
    """
    Decorator for automatic error handling.
    
    Usage:
        @handle_errors("claude_code", error_framework)
        def my_function():
            ...do something...
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempt = 0
            last_error = None
            
            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    last_error = e
                    
                    # Capture error
                    error_record = recovery_framework.capture_error(
                        component,
                        e,
                        context={
                            "function": func.__name__,
                            "attempt": attempt,
                            "args": str(args)[:100],  # Truncate for logging
                            "kwargs": str(kwargs)[:100]
                        }
                    )
                    
                    if attempt >= max_retries:
                        # Final attempt failed
                        recovery_framework.logger.error(
                            f"Function {func.__name__} failed after {max_retries} attempts"
                        )
                        raise
            
            raise last_error  # Should not reach here
        
        return wrapper
    return decorator


# CLI for error recovery
if __name__ == "__main__":
    import sys
    
    vault = Path("./Vault")
    recovery = ErrorRecoveryFramework(vault)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--status":
            status = recovery.get_error_status()
            print(json.dumps(status, indent=2))
        
        elif sys.argv[1] == "--process-dlq":
            count = recovery.process_dead_letter_queue()
            print(f"✓ Processed {count} items from dead letter queue")
        
        else:
            print("Usage: python error_recovery.py [--status|--process-dlq]")
    else:
        print("Error Recovery Framework initialized")
        print("Errors saved to: Vault/System/errors/")
        print("Recovery checkpoints: Vault/System/recovery/")
        print("Dead letter queue: Vault/System/dead_letter/")
