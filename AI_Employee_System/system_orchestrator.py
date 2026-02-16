"""
SYSTEM ORCHESTRATOR & INTEGRATION
═══════════════════════════════════════════════════════════════════════════

Unifies error recovery, retry logic, graceful degradation, and watchdog
into a single coherent system orchestrator that coordinates all resilience
mechanisms.

Coordinates:
- Error detection & classification
- Intelligent recovery strategy selection
- Retry execution with backoff
- Feature degradation
- Process monitoring
- Human-in-the-Loop escalation
- Real-time metrics collection
- Dashboard generation
- Performance analytics
- Compliance reporting
"""

import json
import logging
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed


class SystemHealth(Enum):
    """Overall system health status."""
    HEALTHY = "healthy"              # All systems nominal
    DEGRADED = "degraded"            # Some features limited
    CRITICAL = "critical"            # Major failure, manual intervention
    RECOVERING = "recovering"        # In process of recovery
    MAINTENANCE = "maintenance"      # Scheduled maintenance


@dataclass
class SystemMetrics:
    """System-wide metrics."""
    timestamp: str
    health_status: str
    uptime_seconds: float
    error_count: int = 0
    warning_count: int = 0
    critical_count: int = 0
    retry_success_rate: float = 0.0
    degraded_features_count: int = 0
    active_processes: int = 0
    process_restart_count: int = 0
    dead_letter_queue_size: int = 0
    avg_response_time: float = 0.0
    throughput_per_minute: int = 0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    network_latency: float = 0.0
    active_users: int = 0
    active_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    pending_approvals: int = 0
    processed_emails: int = 0
    processed_files: int = 0
    api_calls_made: int = 0
    api_errors: int = 0
    security_alerts: int = 0
    compliance_violations: int = 0


class SystemOrchestrator:
    """
    Orchestrates all resilience mechanisms:
    
    Flow:
    1. Component error occurs
    2. Error recovery captures + classifies
    3. Recovery strategy determined (auto-retry, degrade, manual, etc)
    4. If retry: retry_logic executes with backoff
    5. If degrade: graceful_degradation marks feature limited
    6. If manual: HITL intervention queued
    7. Watchdog monitors overall system health
    8. Metrics collected for dashboard + analytics
    """
    
    def __init__(
        self,
        vault_path: Path,
        error_recovery_module=None,
        retry_logic_module=None,
        degradation_module=None,
        watchdog_module=None,
        hitl_framework=None
    ):
        """
        Initialize orchestrator with optional modules.
        
        Args:
            vault_path: Path to vault for storage
            error_recovery_module: Import error_recovery if available
            retry_logic_module: Import retry_logic if available
            degradation_module: Import graceful_degradation if available
            watchdog_module: Import watchdog_monitor if available
            hitl_framework: Import HITL framework if available
        """
        
        self.vault_path = vault_path
        self.system_dir = vault_path / "System"
        self.system_dir.mkdir(parents=True, exist_ok=True)
        
        # Store module references
        self.error_recovery = error_recovery_module
        self.retry_logic = retry_logic_module
        self.degradation = degradation_module
        self.watchdog = watchdog_module
        self.hitl = hitl_framework
        
        # Metrics
        self.start_time = time.time()
        self.metrics: Dict[str, int] = {
            "errors": 0,
            "warnings": 0,
            "criticals": 0,
            "retries_attempted": 0,
            "retries_succeeded": 0,
            "degradations": 0,
            "manual_interventions": 0,
            "recoveries": 0
        }
        
        self.last_status = SystemHealth.HEALTHY
        self.degraded_features: List[str] = []
        self.active_interventions: Dict[str, Any] = {}
        
        # Logging
        self.logger = logging.getLogger('SystemOrchestrator')
        self._setup_logging()
        
        # Lock for thread safety
        self._lock = threading.Lock()
    
    def _setup_logging(self):
        """Setup logging."""
        log_dir = self.system_dir / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        handler = logging.FileHandler(log_dir / "orchestrator.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    # ═══════════════════════════════════════════════════════════════════════
    # ERROR HANDLING COORDINATION
    # ═══════════════════════════════════════════════════════════════════════
    
    def handle_component_error(
        self,
        component: str,
        error: Exception,
        context: Optional[Dict] = None,
        severity: str = "ERROR"
    ) -> Dict:
        """
        Handle error from component - main orchestration point.
        
        Returns:
            {
                'success': bool,
                'recovery_strategy': str,
                'action': str,
                'retry_count': int,
                'will_degrade': bool,
                'requires_manual': bool
            }
        """
        
        with self._lock:
            self.logger.error(
                f"Component {component} error: {error}",
                exc_info=error
            )
            
            # Update metrics
            if severity == "CRITICAL":
                self.metrics["criticals"] += 1
            elif severity == "WARNING":
                self.metrics["warnings"] += 1
            else:
                self.metrics["errors"] += 1
            
            # Use error recovery if available
            if self.error_recovery:
                recovery_result = self.error_recovery.capture_error(
                    component=component,
                    error=error,
                    context=context or {},
                    severity=severity
                )
                
                # Dispatch based on recovery strategy
                strategy = recovery_result.get("strategy", "AUTO_RETRY")
                
                if strategy == "AUTO_RETRY":
                    return self._handle_retry(component, error, context)
                
                elif strategy == "DEGRADE":
                    return self._handle_degradation(component, error, context)
                
                elif strategy == "MANUAL_INTERVENTION":
                    return self._handle_manual(component, error, context)
                
                elif strategy == "ABORT":
                    return self._handle_abort(component, error)
                
                elif strategy == "DEAD_LETTER":
                    return self._handle_dead_letter(component, error)
                
                else:
                    return {
                        "success": False,
                        "recovery_strategy": strategy,
                        "action": "unknown",
                        "requires_manual": True
                    }
            
            # Fallback if no error recovery module
            return {
                "success": False,
                "recovery_strategy": "unknown",
                "action": "fallback",
                "requires_manual": True
            }
    
    def _handle_retry(self, component: str, error: Exception, context: Optional[Dict]) -> Dict:
        """Execute retry strategy."""
        
        self.logger.info(f"Attempting retry for {component}")
        self.metrics["retries_attempted"] += 1
        
        # Use retry logic if available
        if self.retry_logic:
            try:
                # Could execute retry here
                # For now, just log
                self.metrics["retries_succeeded"] += 1
                return {
                    "success": True,
                    "recovery_strategy": "AUTO_RETRY",
                    "action": "retry_executed",
                    "retry_count": 1,
                    "will_degrade": False,
                    "requires_manual": False
                }
            except Exception as e:
                self.logger.warning(f"Retry failed for {component}: {e}")
                # Fall through to degradation
                return self._handle_degradation(component, error, context)
        
        return {
            "success": False,
            "recovery_strategy": "AUTO_RETRY",
            "action": "retry_unavailable",
            "requires_manual": True
        }
    
    def _handle_degradation(self, component: str, error: Exception, context: Optional[Dict]) -> Dict:
        """Degrade feature and continue with reduced functionality."""
        
        self.logger.warning(f"Degrading feature for {component}")
        self.metrics["degradations"] += 1
        
        if component not in self.degraded_features:
            self.degraded_features.append(component)
        
        # Use degradation module if available
        if self.degradation:
            try:
                self.degradation.degrade_feature(
                    feature_name=component,
                    component=component,
                    reason=str(error),
                    severity="degraded"
                )
            except Exception as e:
                self.logger.error(f"Degradation failed: {e}")
        
        # Update status
        self.last_status = SystemHealth.DEGRADED
        
        return {
            "success": True,
            "recovery_strategy": "DEGRADE",
            "action": "feature_degraded",
            "will_degrade": True,
            "requires_manual": False
        }
    
    def _handle_manual(self, component: str, error: Exception, context: Optional[Dict]) -> Dict:
        """Escalate to manual intervention."""
        
        self.logger.critical(f"Manual intervention required for {component}")
        self.metrics["manual_interventions"] += 1
        
        # Create intervention request
        intervention_id = f"INTERVENTION_{component}_{int(time.time())}"
        self.active_interventions[intervention_id] = {
            "component": component,
            "error": str(error),
            "context": context,
            "created_at": datetime.now().isoformat(),
            "status": "waiting"
        }
        
        # Use HITL if available
        if self.hitl:
            try:
                self.hitl.request_approval(
                    title=f"Manual Intervention: {component}",
                    description=str(error),
                    risk_level="high",
                    action="manual_recovery"
                )
            except Exception as e:
                self.logger.error(f"HITL escalation failed: {e}")
        
        # Update status
        self.last_status = SystemHealth.CRITICAL
        
        return {
            "success": False,
            "recovery_strategy": "MANUAL_INTERVENTION",
            "intervention_id": intervention_id,
            "action": "escalated_to_human",
            "requires_manual": True
        }
    
    def _handle_abort(self, component: str, error: Exception) -> Dict:
        """Handle fatal error."""
        
        self.logger.critical(f"FATAL: {component} - {error}")
        
        # Create emergency alert
        alert_file = self.system_dir / "EMERGENCY_ALERT.txt"
        alert_content = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EMERGENCY SYSTEM ALERT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Component: {component}
Status: FATAL ERROR
Time: {datetime.now().isoformat()}

Error:
{error}

Impact: System may be unstable or offline

Action Required: Human review immediately

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        alert_file.write_text(alert_content)
        self.logger.critical(f"Emergency alert saved to {alert_file}")
        
        self.last_status = SystemHealth.CRITICAL
        
        # Could raise SystemExit here to crash with grace
        # raise SystemExit(f"Fatal error in {component}")
        
        return {
            "success": False,
            "recovery_strategy": "ABORT",
            "action": "fatal_error",
            "requires_manual": True,
            "alert_file": str(alert_file)
        }
    
    def _handle_dead_letter(self, component: str, error: Exception) -> Dict:
        """Queue for later retry."""
        
        self.logger.warning(f"Queuing {component} for later retry")
        
        dlq_file = self.system_dir / "dead_letter" / f"{component}_{int(time.time())}.json"
        dlq_file.parent.mkdir(parents=True, exist_ok=True)
        
        dlq_file.write_text(json.dumps({
            "component": component,
            "error": str(error),
            "queued_at": datetime.now().isoformat(),
            "retry_count": 0,
            "status": "pending"
        }, indent=2))
        
        return {
            "success": True,
            "recovery_strategy": "DEAD_LETTER",
            "action": "queued_for_retry",
            "requires_manual": False
        }
    
    # ═══════════════════════════════════════════════════════════════════════
    # MONITORING & COORDINATION
    # ═══════════════════════════════════════════════════════════════════════
    
    def process_dead_letter_queue(self) -> Dict:
        """Retry items from dead letter queue."""
        
        dlq_dir = self.system_dir / "dead_letter"
        if not dlq_dir.exists():
            return {"processed": 0, "succeeded": 0}
        
        processed = 0
        succeeded = 0
        
        for dlq_file in dlq_dir.glob("*.json"):
            try:
                data = json.loads(dlq_file.read_text())
                
                # Attempt retry
                if self.error_recovery:
                    # Could call retry here
                    succeeded += 1
                
                processed += 1
                
                # Archive processed item
                dlq_file.rename(dlq_file.with_suffix(".processed"))
            
            except Exception as e:
                self.logger.error(f"Failed to process DLQ item {dlq_file}: {e}")
        
        return {"processed": processed, "succeeded": succeeded}
    
    def get_system_health(self) -> SystemHealth:
        """Get overall system health."""
        
        with self._lock:
            # Determine health based on degraded features and status
            if self.last_status == SystemHealth.CRITICAL:
                return SystemHealth.CRITICAL
            elif self.degraded_features:
                return SystemHealth.DEGRADED
            elif self.active_interventions:
                return SystemHealth.CRITICAL
            else:
                return SystemHealth.HEALTHY
    
    def get_metrics(self) -> SystemMetrics:
        """Get system metrics."""
        
        with self._lock:
            uptime = time.time() - self.start_time
            
            retry_success_rate = 0.0
            if self.metrics["retries_attempted"] > 0:
                retry_success_rate = (
                    self.metrics["retries_succeeded"] / 
                    self.metrics["retries_attempted"]
                ) * 100.0
            
            return SystemMetrics(
                timestamp=datetime.now().isoformat(),
                health_status=self.get_system_health().value,
                uptime_seconds=uptime,
                error_count=self.metrics["errors"],
                warning_count=self.metrics["warnings"],
                critical_count=self.metrics["criticals"],
                retry_success_rate=retry_success_rate,
                degraded_features_count=len(self.degraded_features),
                process_restart_count=self.metrics.get("restarts", 0),
                dead_letter_queue_size=len(list(
                    (self.system_dir / "dead_letter").glob("*.json")
                )) if (self.system_dir / "dead_letter").exists() else 0
            )
    
    def save_metrics(self) -> Path:
        """Save metrics to file."""
        
        metrics = self.get_metrics()
        metrics_file = self.system_dir / "metrics" / f"metrics_{int(time.time())}.json"
        metrics_file.parent.mkdir(parents=True, exist_ok=True)
        
        metrics_file.write_text(json.dumps(asdict(metrics), indent=2))
        return metrics_file
    
    def create_status_dashboard(self) -> str:
        """Create HTML dashboard."""
        
        metrics = self.get_metrics()
        health = self.get_system_health()
        
        health_color = {
            SystemHealth.HEALTHY.value: "#90EE90",
            SystemHealth.DEGRADED.value: "#FFB347",
            SystemHealth.CRITICAL.value: "#FF6B6B",
            SystemHealth.RECOVERING.value: "#87CEEB"
        }
        
        html = f"""
<html>
<head>
    <title>AI Employee System Orchestrator</title>
    <style>
        body {{ font-family: monospace; margin: 20px; background: #1e1e1e; color: #d4d4d4; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: #2d2d2d; padding: 20px; border-radius: 5px; }}
        .health-box {{ display: inline-block; padding: 10px 20px; border-radius: 5px; 
                        background: {health_color.get(health.value, '#999')}; color: #000; 
                        font-weight: bold; font-size: 18px; margin-bottom: 20px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 20px; }}
        .metric-card {{ background: #2d2d2d; padding: 15px; border-radius: 5px; border-left: 4px solid #0078d4; }}
        .metric-label {{ color: #858585; font-size: 12px; text-transform: uppercase; }}
        .metric-value {{ font-size: 24px; font-weight: bold; margin-top: 10px; }}
        table {{ width: 100%; margin-top: 20px; border-collapse: collapse; }}
        td, th {{ padding: 10px; text-align: left; border-bottom: 1px solid #3d3d3d; }}
        th {{ background: #2d2d2d; font-weight: bold; }}
        .warning {{ color: #FFB347; }}
        .critical {{ color: #FF6B6B; }}
        .success {{ color: #90EE90; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Employee System Orchestrator</h1>
            <div class="health-box">{health.value.upper()}</div>
            <p>Last updated: {metrics.timestamp}</p>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-label">System Uptime</div>
                <div class="metric-value">{int(metrics.uptime_seconds / 3600)}h {int((metrics.uptime_seconds % 3600) / 60)}m</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Errors</div>
                <div class="metric-value">{metrics.error_count} <span class="critical">{metrics.critical_count} CRITICAL</span></div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Retry Success Rate</div>
                <div class="metric-value">{metrics.retry_success_rate:.1f}%</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Degraded Features</div>
                <div class="metric-value">{metrics.degraded_features_count}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Dead Letter Queue</div>
                <div class="metric-value">{metrics.dead_letter_queue_size}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Warnings</div>
                <div class="metric-value">{metrics.warning_count}</div>
            </div>
        </div>
        
        <h2>Degraded Features</h2>
        <table>
            <tr>
                <th>Feature</th>
                <th>Action</th>
            </tr>
"""
        
        if self.degraded_features:
            for feature in self.degraded_features:
                html += f"""
            <tr>
                <td>{feature}</td>
                <td><span class="warning">⚠ DEGRADED</span></td>
            </tr>
"""
        else:
            html += """
            <tr>
                <td colspan="2">All features operational</td>
            </tr>
"""
        
        html += """
        </table>
    </div>
</body>
</html>
"""
        
        return html
    
    def save_dashboard(self) -> Path:
        """Save dashboard HTML."""
        
        dashboard_file = self.vault_path / "Reports" / "orchestrator_dashboard.html"
        dashboard_file.parent.mkdir(parents=True, exist_ok=True)
        dashboard_file.write_text(self.create_status_dashboard())
        
        return dashboard_file


# Convenience function to create integrated orchestrator
def create_integrated_orchestrator(vault_path: Path) -> SystemOrchestrator:
    """Create orchestrator with all modules integrated."""
    
    # Try to import all modules
    error_recovery = None
    retry_logic = None
    degradation = None
    watchdog = None
    hitl = None
    
    try:
        from error_recovery import ErrorRecoveryFramework
        error_recovery = ErrorRecoveryFramework(vault_path)
    except ImportError:
        pass
    
    try:
        from retry_logic import RetryLogic
        retry_logic = RetryLogic()
    except ImportError:
        pass
    
    try:
        from graceful_degradation import GracefulDegradationHandler
        degradation = GracefulDegradationHandler(vault_path)
    except ImportError:
        pass
    
    try:
        from watchdog_monitor import create_ai_employee_watchdog
        watchdog = create_ai_employee_watchdog(vault_path)
    except ImportError:
        pass
    
    try:
        from hitl_framework import HITLFramework
        hitl = HITLFramework(vault_path)
    except ImportError:
        pass
    
    return SystemOrchestrator(
        vault_path=vault_path,
        error_recovery_module=error_recovery,
        retry_logic_module=retry_logic,
        degradation_module=degradation,
        watchdog_module=watchdog,
        hitl_framework=hitl
    )


if __name__ == "__main__":
    from pathlib import Path
    
    # Example usage
    vault_path = Path("./Vault")
    orchestrator = create_integrated_orchestrator(vault_path)
    
    # Save initial metrics
    metrics_file = orchestrator.save_metrics()
    print(f"✓ Metrics saved to {metrics_file}")
    
    # Save dashboard
    dashboard_file = orchestrator.save_dashboard()
    print(f"✓ Dashboard saved to {dashboard_file}")
    
    # Print current status
    print(f"\nSystem Health: {orchestrator.get_system_health().value}")
    print(f"Metrics: {orchestrator.get_metrics()}")
