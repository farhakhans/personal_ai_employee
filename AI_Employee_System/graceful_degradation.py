"""
GRACEFUL DEGRADATION HANDLER
═══════════════════════════════════════════════════════════════════════════

Allows system to continue operating in limited capacity when components fail.
Instead of complete failure, the system adapts to available resources.

Degradation modes:
1. Feature disabled (dependency unavailable)
2. Reduced performance (fallback to simpler algorithm)
3. Limited scope (fewer items processed)
4. Cached data (use stale data when fresh unavailable)
5. Manual mode (wait for human action)
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum
from datetime import datetime, timedelta


class DegradationLevel(Enum):
    """How degraded is the system?"""
    FULL_SERVICE = "full"              # All features working
    REDUCED = "reduced"                # Some features limited
    DEGRADED = "degraded"              # Major features limited
    MINIMAL = "minimal"                # Only critical features
    MANUAL = "manual"                  # Wait for human


@dataclass
class DegradedFeature:
    """A feature that's operating in degraded mode."""
    feature_name: str
    component: str                     # What failed (gmail_watcher, etc.)
    degradation_level: str             # Feature, performance, or scope
    reason: str                        # Why it's degraded
    since: str                         # When degradation started
    estimated_recovery: Optional[str] = None  # When it should recover
    workaround: str = ""               # What user should do
    auto_recover: bool = False         # Will it auto-recover?
    fallback_available: bool = False   # Is there a fallback?


class GracefulDegradationHandler:
    """Manages system degradation and recovery."""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.config_dir = vault_path / "System" / "degradation"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Current degraded features
        self.degraded_features: Dict[str, DegradedFeature] = {}
        
        # Load existing degradation state
        self._load_degradation_state()
    
    def degrade_feature(
        self,
        feature_name: str,
        component: str,
        reason: str,
        degradation_level: str = "feature",  # feature, performance, scope
        workaround: str = "",
        estimated_recovery: Optional[str] = None,
        fallback: Optional[Callable] = None
    ) -> DegradedFeature:
        """
        Mark a feature as degraded.
        
        Args:
            feature_name: User-friendly name (e.g., "Email Sending")
            component: Technical component (e.g., "gmail_watcher")
            reason: Why it's degraded
            degradation_level: Type of degradation
            workaround: What user should do
            estimated_recovery: When it should be fixed
            fallback: Function to call for fallback behavior
        """
        
        degraded = DegradedFeature(
            feature_name=feature_name,
            component=component,
            degradation_level=degradation_level,
            reason=reason,
            since=datetime.now().isoformat(),
            estimated_recovery=estimated_recovery,
            workaround=workaround,
            fallback_available=(fallback is not None)
        )
        
        self.degraded_features[feature_name] = degraded
        
        # Save state
        self._save_degradation_state()
        
        # Create user notification
        self._create_degradation_notice(degraded)
        
        return degraded
    
    def recover_feature(self, feature_name: str) -> bool:
        """Mark a feature as recovered."""
        
        if feature_name in self.degraded_features:
            del self.degraded_features[feature_name]
            self._save_degradation_state()
            
            # Notify recovery
            self._create_recovery_notice(feature_name)
            return True
        
        return False
    
    def get_overall_status(self) -> Dict[str, Any]:
        """Get overall system degradation status."""
        
        if not self.degraded_features:
            level = DegradationLevel.FULL_SERVICE
        elif len(self.degraded_features) <= 1:
            level = DegradationLevel.REDUCED
        elif len(self.degraded_features) <= 3:
            level = DegradationLevel.DEGRADED
        else:
            level = DegradationLevel.MINIMAL
        
        return {
            "overall_level": level.value,
            "degraded_features": {
                name: asdict(feature)
                for name, feature in self.degraded_features.items()
            },
            "feature_count": len(self.degraded_features),
            "status_updated": datetime.now().isoformat()
        }
    
    def is_feature_available(self, feature_name: str) -> bool:
        """Check if feature is fully available."""
        return feature_name not in self.degraded_features
    
    def should_enable_fallback(self, feature_name: str) -> bool:
        """Should fallback be used?"""
        feature = self.degraded_features.get(feature_name)
        if not feature:
            return False
        return feature.fallback_available
    
    def _create_degradation_notice(self, feature: DegradedFeature):
        """Create user-facing notice about degradation."""
        
        notice = f"""
# ⚠️ DEGRADATION NOTICE

**Feature:** {feature.feature_name}
**Status:** DEGRADED (as of {feature.since})
**Reason:** {feature.reason}

## What's Affected

{feature.workaround or "This feature is currently unavailable."}

## When Will It Be Fixed?

{feature.estimated_recovery or "Unknown - please check back later"}

## What You Should Do

1. {"Use fallback mode" if feature.fallback_available else "Wait for recovery"}
2. Check recovery notice when posted
3. Contact support if persistent

## Technical Details

- Component: {feature.component}
- Degradation Type: {feature.degradation_level}
- Auto-recovery: {"Yes" if feature.auto_recover else "No"}

Update: Will post recovery notice here when fixed.
"""
        
        notice_file = self.vault_path / "System" / f"NOTICE_{feature.feature_name.replace(' ', '_')}.md"
        notice_file.write_text(notice)
    
    def _create_recovery_notice(self, feature_name: str):
        """Create notice announcing recovery."""
        
        notice = f"""
# ✓ RECOVERY NOTICE

**Feature:** {feature_name}
**Status:** RECOVERED
**Time:** {datetime.now().isoformat()}

The previously degraded feature is now operating at full capacity.

All functionality has been restored.
"""
        
        notice_file = self.vault_path / "System" / f"RECOVERY_{feature_name.replace(' ', '_')}.md"
        notice_file.write_text(notice)
    
    def _save_degradation_state(self):
        """Save current degradation state."""
        
        state = {
            "timestamp": datetime.now().isoformat(),
            "features": {
                name: asdict(feature)
                for name, feature in self.degraded_features.items()
            }
        }
        
        state_file = self.config_dir / "current_degradation.json"
        state_file.write_text(json.dumps(state, indent=2))
    
    def _load_degradation_state(self):
        """Load previous degradation state."""
        
        state_file = self.config_dir / "current_degradation.json"
        if state_file.exists():
            with state_file.open() as f:
                state = json.load(f)
            
            # Restore degraded features
            for name, feature_data in state.get("features", {}).items():
                self.degraded_features[name] = DegradedFeature(**feature_data)


# Specific degradation handlers for common scenarios

class EmailDegradation:
    """Email system degradation strategies."""
    
    @staticmethod
    def handle_gmail_api_down(handler: GracefulDegradationHandler):
        """Gmail API is down."""
        handler.degrade_feature(
            feature_name="Email Monitoring",
            component="gmail_watcher",
            reason="Gmail API temporarily unavailable",
            degradation_level="feature",
            workaround="Manual email checking recommended. Auto-retry in 5 minutes.",
            estimated_recovery=(
                datetime.now() + timedelta(minutes=5)
            ).isoformat()
        )
    
    @staticmethod
    def handle_gmail_rate_limit(handler: GracefulDegradationHandler):
        """Gmail API rate limit hit."""
        handler.degrade_feature(
            feature_name="Email Sending",
            component="gmail_watcher",
            reason="Gmail API rate limit exceeded",
            degradation_level="scope",
            workaround="Email sending paused. Will resume in 1 hour.",
            estimated_recovery=(
                datetime.now() + timedelta(hours=1)
            ).isoformat(),
            fallback=lambda: print("Using cached drafts instead")
        )


class AnalyticsDegradation:
    """Analytics system degradation."""
    
    @staticmethod
    def handle_analytics_slow(handler: GracefulDegradationHandler):
        """Analytics processing is slow."""
        handler.degrade_feature(
            feature_name="Real-time Analytics",
            component="analytics",
            reason="High processing load",
            degradation_level="performance",
            workaround="Analytics will be available with 1-hour delay",
            fallback=lambda: print("Using simplified analytics")
        )
    
    @staticmethod
    def handle_report_generation_slow(handler: GracefulDegradationHandler):
        """Report generation is timing out."""
        handler.degrade_feature(
            feature_name="Report Generation",
            component="reporting",
            reason="Report too large or complex",
            degradation_level="scope",
            workaround="Generate reports for smaller date ranges",
            fallback=lambda: print("Using cached report")
        )


class ScheduleDegradation:
    """Schedule/calendar degradation."""
    
    @staticmethod
    def handle_calendar_read_only(handler: GracefulDegradationHandler):
        """Calendar in read-only mode."""
        handler.degrade_feature(
            feature_name="Calendar Management",
            component="calendar_mcp",
            reason="Calendar provider is read-only",
            degradation_level="feature",
            workaround="View calendar entries. Create events manually.",
            estimated_recovery=(
                datetime.now() + timedelta(hours=2)
            ).isoformat()
        )


class PaymentDegradation:
    """Payment system degradation."""
    
    @staticmethod
    def handle_payment_pending(handler: GracefulDegradationHandler):
        """Payment gateway is slow."""
        handler.degrade_feature(
            feature_name="Payment Processing",
            component="payment_gateway",
            reason="Payment gateway slow response",
            degradation_level="performance",
            workaround="Payments queued. Processing will take up to 30 minutes.",
            estimated_recovery=(
                datetime.now() + timedelta(minutes=30)
            ).isoformat()
        )
    
    @staticmethod
    def handle_payment_disabled(handler: GracefulDegradationHandler):
        """Payment system is down."""
        handler.degrade_feature(
            feature_name="Online Payments",
            component="payment_gateway",
            reason="Payment gateway offline",
            degradation_level="feature",
            workaround="Payments disabled. Contact accounting for manual processing.",
            estimated_recovery=(
                datetime.now() + timedelta(hours=1)
            ).isoformat(),
            fallback=lambda: print("Using manual payment workflow")
        )


# Dashboard display for degradation

def create_degradation_dashboard(
    handler: GracefulDegradationHandler,
    vault_path: Path
) -> str:
    """Create HTML dashboard showing current degradation status."""
    
    status = handler.get_overall_status()
    
    # Color coding
    level_colors = {
        "full": "green",
        "reduced": "yellow",
        "degraded": "orange",
        "minimal": "red"
    }
    
    color = level_colors.get(status["overall_level"], "gray")
    
    html = f"""
<html>
<head>
    <title>System Degradation Status</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .status {{ padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .full {{ background-color: #90EE90; }}
        .reduced {{ background-color: #FFFFE0; }}
        .degraded {{ background-color: #FFB347; }}
        .minimal {{ background-color: #FF6B6B; }}
        .feature {{ padding: 10px; margin: 5px 0; border-left: 4px solid #ccc; }}
    </style>
</head>
<body>
    <h1>System Status Dashboard</h1>
    
    <div class="status {status["overall_level"]}">
        <h2>Overall Status: {status["overall_level"].upper()}</h2>
        <p>Last updated: {status["status_updated"]}</p>
    </div>
    
    <h3>Degraded Features: {status["feature_count"]}</h3>
"""
    
    if status["degraded_features"]:
        for name, feature in status["degraded_features"].items():
            html += f"""
    <div class="feature">
        <strong>{feature["feature_name"]}</strong>
        <p>Component: {feature["component"]}</p>
        <p>Reason: {feature["reason"]}</p>
        <p>Degradation: {feature["degradation_level"]}</p>
        {f'<p>Expected recovery: {feature["estimated_recovery"]}</p>' if feature["estimated_recovery"] else ''}
    </div>
"""
    else:
        html += "<p>✓ All systems operational</p>"

    html += """
</body>
</html>
"""

    return html


# Enhanced predictive degradation functionality
class PredictiveDegradation:
    """ML-based predictive degradation system."""
    
    def __init__(self, handler: GracefulDegradationHandler):
        self.handler = handler
        self.model_trained = False
        self.degradation_predictors = {}
    
    def train_model(self, historical_data: List[Dict]):
        """Train the ML model on historical degradation data."""
        # In a real implementation, this would train an ML model
        # For now, we'll just store the data
        self.historical_data = historical_data
        self.model_trained = True
    
    def predict_degradation_risk(self, component: str, current_metrics: Dict) -> Tuple[float, str, List[str]]:
        """
        Predict degradation risk for a component.
        
        Returns:
            (risk_score, risk_reason, recommended_actions)
        """
        # Placeholder implementation - in reality this would use ML
        risk_score = 0.0
        risk_reason = ""
        actions = []
        
        # Example risk factors
        if current_metrics.get("error_rate", 0) > 0.1:
            risk_score += 0.3
            risk_reason += "High error rate detected. "
            actions.append("Monitor error logs")
        
        if current_metrics.get("response_time", 0) > 5.0:
            risk_score += 0.2
            risk_reason += "Slow response times. "
            actions.append("Check resource usage")
        
        if current_metrics.get("memory_usage", 0) > 0.8:
            risk_score += 0.25
            risk_reason += "High memory usage. "
            actions.append("Consider scaling resources")
        
        if current_metrics.get("cpu_usage", 0) > 0.9:
            risk_score += 0.3
            risk_reason += "High CPU usage. "
            actions.append("Optimize performance")
        
        return min(risk_score, 1.0), risk_reason.strip(), actions


# Adaptive degradation strategies
class AdaptiveDegradation:
    """Adaptive degradation based on real-time metrics."""
    
    def __init__(self, handler: GracefulDegradationHandler):
        self.handler = handler
        self.current_load = 0
        self.capacity = 100  # arbitrary unit
    
    def adjust_degradation_level(self, current_metrics: Dict):
        """Adjust degradation level based on current system metrics."""
        load = current_metrics.get("system_load", 0)
        
        if load > 0.9:  # Over 90% load
            # Aggressive degradation
            for feature_name, feature in self.handler.degraded_features.items():
                if feature.priority > 3:  # Lower priority features
                    # Further degrade lower priority features
                    pass
        elif load < 0.5:  # Under 50% load
            # Consider recovering some features
            for feature_name, feature in self.handler.degraded_features.items():
                if feature.priority <= 2 and feature.auto_recover:  # High priority auto-recover
                    self.handler.recover_feature(feature_name)


# CLI
if __name__ == "__main__":
    import sys

    vault = Path("./Vault")
    degradation = GracefulDegradationHandler(vault)

    if len(sys.argv) > 1:
        if sys.argv[1] == "--status":
            status = degradation.get_overall_status()
            print(json.dumps(status, indent=2))

        elif sys.argv[1] == "--dashboard":
            html = create_degradation_dashboard(degradation, vault)
            dashboard_file = vault / "Reports" / "degradation_dashboard.html"
            dashboard_file.parent.mkdir(parents=True, exist_ok=True)
            dashboard_file.write_text(html)
            print(f"✓ Dashboard saved to: {dashboard_file}")

        elif sys.argv[1] == "--patterns":
            print(json.dumps(degradation.degradation_patterns, indent=2))

        else:
            print("Usage: python graceful_degradation.py [--status|--dashboard|--patterns]")
    else:
        print("Graceful Degradation Handler initialized")
        print("Usage: python graceful_degradation.py [--status|--dashboard|--patterns]")
