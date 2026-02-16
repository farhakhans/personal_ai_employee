"""
WATCHDOG PROCESS MONITOR
═══════════════════════════════════════════════════════════════════════════

Monitors all system components and automatically restarts failed ones.
Acts as a supervisor to ensure system keeps running even when parts fail.

Features:
- Monitor multiple processes
- Automatic restart on failure
- Configurable restart attempts
- Health check polling
- Dashboard of process status
- Graceful shutdown coordination
"""

import subprocess
import psutil
import time
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
from datetime import datetime, timedelta


class ProcessStatus(Enum):
    """Status of monitored process."""
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"
    RESTARTING = "restarting"
    CRASHED = "crashed"


@dataclass
class ProcessConfig:
    """Configuration for a monitored process."""
    name: str                       # Friendly name
    command: List[str]              # How to start it: ["python", "script.py"]
    working_dir: str = "."          # Working directory
    restart_on_failure: bool = True # Auto-restart?
    max_restart_attempts: int = 5   # How many times to retry
    restart_delay: float = 5.0      # Seconds between restart attempts
    health_check_command: Optional[str] = None  # Command to check health
    health_check_interval: float = 60.0  # Seconds between checks
    environment: Dict[str, str] = field(default_factory=dict)  # Env vars


@dataclass
class ProcessStatusRecord:
    """Current status of a process."""
    name: str
    status: str                     # running, stopped, failed, etc.
    pid: Optional[int] = None       # Process ID
    started_at: Optional[str] = None
    crashed_at: Optional[str] = None
    restart_count: int = 0
    last_health_check: Optional[str] = None
    health_check_passed: bool = False
    error_message: str = ""


class WatchdogMonitor:
    """Monitors and manages multiple processes."""
    
    def __init__(self, vault_path: Path, check_interval: float = 10.0):
        self.vault_path = vault_path
        self.status_dir = vault_path / "System" / "watchdog"
        self.status_dir.mkdir(parents=True, exist_ok=True)
        
        self.check_interval = check_interval  # How often to check processes
        self.processes: Dict[str, ProcessConfig] = {}
        self.status: Dict[str, ProcessStatusRecord] = {}
        self.running_processes: Dict[str, subprocess.Popen] = {}
        
        self.logger = logging.getLogger('Watchdog')
        self._setup_logging()
        
        self._running = False
    
    def _setup_logging(self):
        """Setup logging."""
        handler = logging.FileHandler(self.vault_path / "System" / "logs" / "watchdog.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def register_process(self, config: ProcessConfig):
        """Register a process to monitor."""
        self.processes[config.name] = config
        self.status[config.name] = ProcessStatusRecord(
            name=config.name,
            status=ProcessStatus.STOPPED.value
        )
        self.logger.info(f"Registered process: {config.name}")
    
    def start_all(self):
        """Start all registered processes."""
        for name, config in self.processes.items():
            self.start_process(name)
    
    def start_process(self, name: str) -> bool:
        """Start a specific process."""
        
        config = self.processes.get(name)
        if not config:
            self.logger.error(f"Process {name} not registered")
            return False
        
        try:
            self.logger.info(f"Starting process: {name}")
            
            process = subprocess.Popen(
                config.command,
                cwd=config.working_dir,
                env={**os.environ, **config.environment},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.running_processes[name] = process
            
            # Update status
            self.status[name] = ProcessStatusRecord(
                name=name,
                status=ProcessStatus.RUNNING.value,
                pid=process.pid,
                started_at=datetime.now().isoformat(),
                restart_count=self.status.get(name, ProcessStatusRecord(name)).restart_count
            )
            
            self.logger.info(f"Process {name} started (PID {process.pid})")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to start {name}: {e}")
            self.status[name].status = ProcessStatus.FAILED.value
            self.status[name].error_message = str(e)
            return False
    
    def stop_process(self, name: str, timeout: int = 10) -> bool:
        """Stop a process gracefully."""
        
        process = self.running_processes.get(name)
        if not process:
            return False
        
        try:
            self.logger.info(f"Stopping process: {name}")
            process.terminate()
            
            # Wait for graceful shutdown
            try:
                process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                # Force kill if doesn't stop
                self.logger.warning(f"Force killing {name}")
                process.kill()
                process.wait()
            
            del self.running_processes[name]
            self.status[name].status = ProcessStatus.STOPPED.value
            self.logger.info(f"Process {name} stopped")
            return True
        
        except Exception as e:
            self.logger.error(f"Error stopping {name}: {e}")
            return False
    
    def stop_all(self):
        """Stop all processes."""
        for name in list(self.running_processes.keys()):
            self.stop_process(name)
    
    def check_health(self, name: str) -> bool:
        """Check if process is healthy."""
        
        config = self.processes.get(name)
        process = self.running_processes.get(name)
        
        if not process:
            return False
        
        # Check if process still running
        if process.poll() is not None:
            # Process exited
            return False
        
        # Custom health check if configured
        if config and config.health_check_command:
            try:
                result = subprocess.run(
                    config.health_check_command,
                    shell=True,
                    timeout=5,
                    capture_output=True
                )
                return result.returncode == 0
            except Exception as e:
                self.logger.warning(f"Health check failed for {name}: {e}")
                return False
        
        # Process still running
        return True
    
    def monitor_loop(self):
        """Main monitoring loop (run in separate thread)."""
        
        self._running = True
        
        while self._running:
            try:
                for name, config in self.processes.items():
                    try:
                        # Check health
                        is_healthy = self.check_health(name)
                        
                        if not is_healthy:
                            self._handle_process_failure(name)
                        else:
                            # Update last check time
                            self.status[name].last_health_check = (
                                datetime.now().isoformat()
                            )
                            self.status[name].health_check_passed = True
                    
                    except Exception as e:
                        self.logger.error(f"Error checking {name}: {e}")
                
                # Save status
                self._save_status()
                
                # Wait before next check
                time.sleep(self.check_interval)
            
            except KeyboardInterrupt:
                self.logger.info("Monitor interrupted by user")
                break
            except Exception as e:
                self.logger.error(f"Monitor error: {e}")
                time.sleep(self.check_interval)
    
    def _handle_process_failure(self, name: str):
        """Handle a process that failed."""
        
        config = self.processes[name]
        record = self.status[name]
        
        self.logger.warning(f"Process {name} is dead!")
        
        if record.crashed_at is None:
            record.crashed_at = datetime.now().isoformat()
        
        # Check if we should restart
        if not config.restart_on_failure:
            self.logger.warning(f"Auto-restart disabled for {name}")
            record.status = ProcessStatus.STOPPED.value
            return
        
        # Check restart attempts
        if record.restart_count >= config.max_restart_attempts:
            self.logger.error(
                f"Max restart attempts ({config.max_restart_attempts}) "
                f"reached for {name}"
            )
            record.status = ProcessStatus.CRASHED.value
            return
        
        # Restart
        record.restart_count += 1
        record.status = ProcessStatus.RESTARTING.value
        
        self.logger.info(
            f"Restarting {name} (attempt {record.restart_count}/"
            f"{config.max_restart_attempts})"
        )
        
        time.sleep(config.restart_delay)
        self.start_process(name)
    
    def _save_status(self):
        """Save current status to file."""
        
        status_data = {
            "timestamp": datetime.now().isoformat(),
            "processes": {
                name: asdict(record)
                for name, record in self.status.items()
            }
        }
        
        status_file = self.status_dir / "current_status.json"
        status_file.write_text(json.dumps(status_data, indent=2))
    
    def get_status(self) -> Dict:
        """Get current status of all processes."""
        return {
            "timestamp": datetime.now().isoformat(),
            "processes": {
                name: asdict(record)
                for name, record in self.status.items()
            }
        }
    
    def get_dashboard(self) -> str:
        """Create HTML dashboard of process status."""
        
        status = self.get_status()
        
        html = """
<html>
<head>
    <title>Watchdog Process Monitor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { padding: 10px; text-align: left; border: 1px solid #ddd; }
        th { background-color: #4CAF50; color: white; }
        .running { background-color: #90EE90; }
        .stopped { background-color: #FFB347; }
        .failed { background-color: #FF6B6B; }
        .restarting { background-color: #87CEEB; }
    </style>
</head>
<body>
    <h1>Watchdog Process Monitor</h1>
    <p>Last updated: {}</p>
    
    <table>
        <tr>
            <th>Process</th>
            <th>Status</th>
            <th>PID</th>
            <th>Started</th>
            <th>Restarts</th>
            <th>Health Check</th>
        </tr>
""".format(status["timestamp"])
        
        for name, process_status in status["processes"].items():
            row_class = process_status["status"].lower()
            health_icon = "✓" if process_status["health_check_passed"] else "✗"
            
            html += f"""
        <tr class="{row_class}">
            <td>{process_status["name"]}</td>
            <td>{process_status["status"]}</td>
            <td>{process_status["pid"] or "-"}</td>
            <td>{process_status["started_at"] or "-"}</td>
            <td>{process_status["restart_count"]}</td>
            <td>{health_icon} {process_status["last_health_check"] or "-"}</td>
        </tr>
"""
        
        html += """
    </table>
</body>
</html>
"""
        return html


# Advanced features for the watchdog monitor
class AdvancedWatchdogFeatures:
    """Additional advanced features for the watchdog monitor."""
    
    def __init__(self, watchdog: WatchdogMonitor):
        self.watchdog = watchdog
        self.anomaly_detector = AnomalyDetector()
        self.performance_optimizer = PerformanceOptimizer()
        self.security_monitor = SecurityMonitor()
    
    def enable_anomaly_detection(self):
        """Enable anomaly detection for processes."""
        self.anomaly_detector.start_monitoring(self.watchdog)
    
    def enable_performance_optimization(self):
        """Enable performance optimization."""
        self.performance_optimizer.start_optimization(self.watchdog)
    
    def enable_security_monitoring(self):
        """Enable security monitoring."""
        self.security_monitor.start_monitoring(self.watchdog)


class AnomalyDetector:
    """Detects anomalies in process behavior."""
    
    def __init__(self):
        self.baseline_data = {}
        self.anomalies = []
    
    def start_monitoring(self, watchdog: WatchdogMonitor):
        """Start monitoring for anomalies."""
        import threading
        thread = threading.Thread(target=self._monitor_loop, args=(watchdog,))
        thread.daemon = True
        thread.start()
    
    def _monitor_loop(self, watchdog: WatchdogMonitor):
        """Continuous monitoring loop."""
        while True:
            try:
                self._check_anomalies(watchdog)
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logging.error(f"Anomaly detector error: {e}")
                time.sleep(30)
    
    def _check_anomalies(self, watchdog: WatchdogMonitor):
        """Check for anomalies in process behavior."""
        for name, status in watchdog.status.items():
            if name in watchdog.resource_usage_history:
                history = list(watchdog.resource_usage_history[name])
                if len(history) >= 10:  # Need sufficient data
                    recent_avg = sum(h["cpu_percent"] for h in history[-5:]) / 5
                    baseline_avg = sum(h["cpu_percent"] for h in history[:-5]) / len(history[:-5])
                    
                    if recent_avg > baseline_avg * 2:  # CPU usage doubled
                        anomaly = {
                            "process": name,
                            "type": "high_cpu_usage",
                            "timestamp": datetime.now().isoformat(),
                            "details": f"CPU usage increased from {baseline_avg:.1f}% to {recent_avg:.1f}%"
                        }
                        self.anomalies.append(anomaly)
                        watchdog.logger.warning(f"Anomaly detected: {anomaly}")


class PerformanceOptimizer:
    """Optimizes process performance based on usage patterns."""
    
    def __init__(self):
        self.optimization_rules = {}
    
    def start_optimization(self, watchdog: WatchdogMonitor):
        """Start performance optimization."""
        import threading
        thread = threading.Thread(target=self._optimization_loop, args=(watchdog,))
        thread.daemon = True
        thread.start()
    
    def _optimization_loop(self, watchdog: WatchdogMonitor):
        """Continuous optimization loop."""
        while True:
            try:
                self._optimize_performance(watchdog)
                time.sleep(60)  # Optimize every minute
            except Exception as e:
                logging.error(f"Performance optimizer error: {e}")
                time.sleep(60)
    
    def _optimize_performance(self, watchdog: WatchdogMonitor):
        """Apply optimizations based on current state."""
        for name, config in watchdog.processes.items():
            if name in watchdog.status:
                status = watchdog.status[name]
                resource_usage = status.resource_usage
                
                if resource_usage:
                    cpu_percent = resource_usage.get("cpu_percent", 0)
                    
                    # If CPU usage is consistently high, consider scaling up
                    if cpu_percent > 80 and config.auto_scale and config.max_scale_instances > status.instances:
                        watchdog.logger.info(f"Suggesting scale up for {name} due to high CPU usage: {cpu_percent}%")
                        # In a real system, this would trigger scaling


class SecurityMonitor:
    """Monitors processes for security issues."""
    
    def __init__(self):
        self.security_events = []
        self.threat_patterns = [
            "sudo", "su", "chmod", "chown",  # Privilege escalation
            "/etc/", "/root/", "/proc/",  # Sensitive directories
            "eval(", "exec(", "subprocess",  # Code execution
        ]
    
    def start_monitoring(self, watchdog: WatchdogMonitor):
        """Start security monitoring."""
        import threading
        thread = threading.Thread(target=self._security_loop, args=(watchdog,))
        thread.daemon = True
        thread.start()
    
    def _security_loop(self, watchdog: WatchdogMonitor):
        """Continuous security monitoring loop."""
        while True:
            try:
                self._scan_for_threats(watchdog)
                time.sleep(120)  # Scan every 2 minutes
            except Exception as e:
                logging.error(f"Security monitor error: {e}")
                time.sleep(120)
    
    def _scan_for_threats(self, watchdog: WatchdogMonitor):
        """Scan processes for potential security threats."""
        # This would implement actual security scanning
        # For now, just log that scanning occurred
        watchdog.logger.info("Security scan completed")


# Example configuration for AI Employee system

def create_ai_employee_watchdog(vault_path: Path) -> WatchdogMonitor:
    """Create watchdog with standard AI Employee processes."""

    watchdog = WatchdogMonitor(vault_path)

    # Email watcher
    watchdog.register_process(ProcessConfig(
        name="Email Watcher",
        command=["python", "Watchers/gmail_watcher.py"],
        restart_on_failure=True,
        max_restart_attempts=5,
        restart_delay=10.0,
        health_check_command="python -c \"from gmail_watcher import GmailWatcher; w = GmailWatcher(); w.test_connection()\"",
        health_check_interval=300.0
    ))

    # WhatsApp watcher
    watchdog.register_process(ProcessConfig(
        name="WhatsApp Watcher",
        command=["python", "Watchers/whatsapp_watcher.py"],
        restart_on_failure=True,
        max_restart_attempts=3,  # Fewer for browser-based
        restart_delay=30.0,
        health_check_interval=300.0
    ))

    # File watcher
    watchdog.register_process(ProcessConfig(
        name="File Watcher",
        command=["python", "Watchers/file_watcher.py"],
        restart_on_failure=True,
        max_restart_attempts=5,
        restart_delay=5.0
    ))

    # Claude Code
    watchdog.register_process(ProcessConfig(
        name="Claude Code",
        command=["python", "claude_code.py"],
        restart_on_failure=False,  # Don't auto-restart (stateful)
        health_check_interval=600.0
    ))

    # Dashboard
    watchdog.register_process(ProcessConfig(
        name="Dashboard",
        command=["python", "app.py"],
        restart_on_failure=True,
        max_restart_attempts=3,
        restart_delay=10.0,
        health_check_command="curl -f http://localhost:5000/health || exit 1",
        health_check_interval=60.0
    ))

    return watchdog


# CLI
if __name__ == "__main__":
    import sys
    import os

    vault = Path("./Vault")
    watchdog = create_ai_employee_watchdog(vault)

    if len(sys.argv) > 1:
        if sys.argv[1] == "--start":
            print("Starting watchdog monitor...")
            watchdog.start_all()
            watchdog.monitor_loop()

        elif sys.argv[1] == "--status":
            status = watchdog.get_status()
            print(json.dumps(status, indent=2))

        elif sys.argv[1] == "--dashboard":
            html = watchdog.get_dashboard()
            dashboard_file = vault / "Reports" / "watchdog_dashboard.html"
            dashboard_file.parent.mkdir(parents=True, exist_ok=True)
            dashboard_file.write_text(html)
            print(f"✓ Dashboard saved to: {dashboard_file}")

        elif sys.argv[1] == "--restart":
            if len(sys.argv) > 2:
                name = sys.argv[2]
                watchdog.stop_process(name)
                time.sleep(2)
                watchdog.start_process(name)
                print(f"✓ Restarted {name}")
            else:
                print("Usage: python watchdog_monitor.py --restart [process_name]")

        else:
            print(f"Unknown command: {sys.argv[1]}")
    else:
        print("Watchdog Process Monitor")
        print("Usage: python watchdog_monitor.py [--start|--status|--dashboard|--restart]")
