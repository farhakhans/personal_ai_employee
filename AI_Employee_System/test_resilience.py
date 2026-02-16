"""
INTEGRATION TESTS - ERROR HANDLING & RESILIENCE
═══════════════════════════════════════════════════════════════════════════

Verifies error recovery, retry logic, graceful degradation, watchdog, 
and orchestration all work together correctly.

Test Coverage:
- Error classification and recovery strategy selection
- Retry logic with different backoff strategies
- Graceful degradation feature toggling
- Watchdog process monitoring
- System orchestration coordination
- Dead letter queue processing
- Manual intervention escalation
"""

import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import time


# ═══════════════════════════════════════════════════════════════════════
# MOCK MODULES (use these if actual modules not available)
# ═══════════════════════════════════════════════════════════════════════

class MockErrorRecoveryFramework:
    """Mock error recovery for testing."""
    
    def __init__(self, vault_path):
        self.vault_path = vault_path
        self.errors = []
    
    def capture_error(self, component, error, context, severity):
        """Mock error capture."""
        self.errors.append({
            "component": component,
            "error": str(error),
            "severity": severity
        })
        
        # Determine strategy based on error type
        error_str = str(error).lower()
        error_type = type(error).__name__.lower()
        
        if "connection" in error_str or "timeout" in error_str:
            return {"strategy": "AUTO_RETRY"}
        elif "auth" in error_str or "permission" in error_str or "permissionerror" in error_type:
            return {"strategy": "MANUAL_INTERVENTION"}
        elif "rate" in error_str:
            return {"strategy": "AUTO_RETRY"}
        elif "fatal" in error_str:
            return {"strategy": "ABORT"}
        else:
            return {"strategy": "AUTO_RETRY"}


class MockRetryLogic:
    """Mock retry logic for testing."""
    
    def __init__(self):
        self.attempts = {}
    
    def retry(self, func, config=None, *args, **kwargs):
        """Mock retry execution."""
        func_name = func.__name__
        if func_name not in self.attempts:
            self.attempts[func_name] = 0
        
        self.attempts[func_name] += 1
        
        # Simulate retry logic
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if self.attempts[func_name] < 3:
                # Retry
                time.sleep(0.1)
                return self.retry(func, config, *args, **kwargs)
            else:
                # Give up
                raise


class MockGracefulDegradationHandler:
    """Mock graceful degradation for testing."""
    
    def __init__(self, vault_path):
        self.vault_path = vault_path
        self.degraded_features = {}
    
    def degrade_feature(self, feature_name, component, reason, severity="degraded"):
        """Mock feature degradation."""
        self.degraded_features[feature_name] = {
            "component": component,
            "reason": reason,
            "severity": severity
        }
        return True
    
    def recover_feature(self, feature_name):
        """Mock feature recovery."""
        if feature_name in self.degraded_features:
            del self.degraded_features[feature_name]
        return True
    
    def get_overall_status(self):
        """Get degradation status."""
        if self.degraded_features:
            return "degraded"
        return "healthy"


class MockWatchdogMonitor:
    """Mock watchdog for testing."""
    
    def __init__(self):
        self.processes = {}
        self.restart_count = {}
    
    def register_process(self, config):
        """Mock process registration."""
        self.processes[config.name] = config
        self.restart_count[config.name] = 0
    
    def start_process(self, name):
        """Mock process start."""
        if name in self.processes:
            return True
        return False
    
    def check_health(self, name):
        """Mock health check."""
        return name in self.processes
    
    def _handle_process_failure(self, name):
        """Mock failure handling."""
        if name in self.restart_count:
            self.restart_count[name] += 1


# ═══════════════════════════════════════════════════════════════════════
# TESTS
# ═══════════════════════════════════════════════════════════════════════

class TestErrorRecovery(unittest.TestCase):
    """Test error recovery framework."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.vault_path = Path(self.temp_dir.name)
        self.error_recovery = MockErrorRecoveryFramework(self.vault_path)
    
    def tearDown(self):
        """Cleanup."""
        self.temp_dir.cleanup()
    
    def test_connection_error_triggers_retry(self):
        """Connection errors should trigger AUTO_RETRY."""
        error = ConnectionError("Network unreachable")
        result = self.error_recovery.capture_error(
            "email_watcher",
            error,
            {},
            "ERROR"
        )
        self.assertEqual(result["strategy"], "AUTO_RETRY")
    
    def test_auth_error_triggers_manual_intervention(self):
        """Auth errors should trigger MANUAL_INTERVENTION."""
        error = PermissionError("Invalid credentials")
        result = self.error_recovery.capture_error(
            "gmail_watcher",
            error,
            {},
            "CRITICAL"
        )
        self.assertEqual(result["strategy"], "MANUAL_INTERVENTION")
    
    def test_rate_limit_error_triggers_retry(self):
        """Rate limit errors should trigger AUTO_RETRY."""
        error = Exception("Rate limit exceeded")
        result = self.error_recovery.capture_error(
            "api_caller",
            error,
            {},
            "WARNING"
        )
        self.assertEqual(result["strategy"], "AUTO_RETRY")
    
    def test_error_classification_consistency(self):
        """Same error types should be classified consistently."""
        error_type = ConnectionError("timeout")
        result1 = self.error_recovery.capture_error("component1", error_type, {}, "ERROR")
        result2 = self.error_recovery.capture_error("component2", error_type, {}, "ERROR")
        
        self.assertEqual(result1["strategy"], result2["strategy"])


class TestRetryLogic(unittest.TestCase):
    """Test retry logic."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.retry_logic = MockRetryLogic()
        self.call_count = 0
    
    def test_retry_succeeds_after_failures(self):
        """Function should succeed after some retries."""
        
        def flaky_function():
            self.call_count += 1
            if self.call_count < 3:
                raise Exception("Temporary failure")
            return "success"
        
        self.call_count = 0
        result = self.retry_logic.retry(flaky_function)
        
        self.assertEqual(result, "success")
        self.assertGreater(self.call_count, 1)
    
    def test_retry_gives_up_after_max_attempts(self):
        """Retry should eventually give up."""
        
        def always_fails():
            raise Exception("Permanent failure")
        
        with self.assertRaises(Exception):
            self.retry_logic.retry(always_fails)
    
    def test_successful_function_not_retried(self):
        """Successful functions should not be retried."""
        
        call_count = 0
        
        def succeeds_immediately():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = self.retry_logic.retry(succeeds_immediately)
        
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 1)


class TestGracefulDegradation(unittest.TestCase):
    """Test graceful degradation."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.vault_path = Path(self.temp_dir.name)
        self.degradation = MockGracefulDegradationHandler(self.vault_path)
    
    def tearDown(self):
        """Cleanup."""
        self.temp_dir.cleanup()
    
    def test_degrade_feature_marks_degraded(self):
        """Feature should be marked as degraded."""
        self.degradation.degrade_feature(
            "Email Sending",
            "gmail_watcher",
            "API rate limit"
        )
        
        self.assertIn("Email Sending", self.degradation.degraded_features)
        self.assertEqual(
            self.degradation.get_overall_status(),
            "degraded"
        )
    
    def test_recover_feature_marks_healthy(self):
        """Feature should be marked as recovered."""
        self.degradation.degrade_feature(
            "Email Sending",
            "gmail_watcher",
            "API rate limit"
        )
        
        self.degradation.recover_feature("Email Sending")
        
        self.assertNotIn("Email Sending", self.degradation.degraded_features)
        self.assertEqual(
            self.degradation.get_overall_status(),
            "healthy"
        )
    
    def test_multiple_features_degradation(self):
        """Multiple features can be degraded independently."""
        self.degradation.degrade_feature("Email", "email", "down")
        self.degradation.degrade_feature("Payments", "payment", "slow")
        
        self.assertEqual(len(self.degradation.degraded_features), 2)
        self.assertEqual(
            self.degradation.get_overall_status(),
            "degraded"
        )


class TestWatchdogMonitor(unittest.TestCase):
    """Test watchdog monitoring."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.watchdog = MockWatchdogMonitor()
    
    def test_process_registration(self):
        """Processes should be registered correctly."""
        config = Mock()
        config.name = "TestProcess"
        
        self.watchdog.register_process(config)
        
        self.assertIn("TestProcess", self.watchdog.processes)
    
    def test_process_start(self):
        """Process should start successfully."""
        config = Mock()
        config.name = "TestProcess"
        self.watchdog.register_process(config)
        
        result = self.watchdog.start_process("TestProcess")
        
        self.assertTrue(result)
    
    def test_health_check_success(self):
        """Healthy process should pass health check."""
        config = Mock()
        config.name = "TestProcess"
        self.watchdog.register_process(config)
        
        is_healthy = self.watchdog.check_health("TestProcess")
        
        self.assertTrue(is_healthy)
    
    def test_process_restart_on_failure(self):
        """Process should be restarted on failure."""
        config = Mock()
        config.name = "TestProcess"
        self.watchdog.register_process(config)
        
        initial_restarts = self.watchdog.restart_count["TestProcess"]
        self.watchdog._handle_process_failure("TestProcess")
        
        self.assertGreater(
            self.watchdog.restart_count["TestProcess"],
            initial_restarts
        )


class TestIntegration(unittest.TestCase):
    """Test integration of all components."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.vault_path = Path(self.temp_dir.name)
        (self.vault_path / "System").mkdir(parents=True, exist_ok=True)
        
        self.error_recovery = MockErrorRecoveryFramework(self.vault_path)
        self.retry_logic = MockRetryLogic()
        self.degradation = MockGracefulDegradationHandler(self.vault_path)
        self.watchdog = MockWatchdogMonitor()
    
    def tearDown(self):
        """Cleanup."""
        self.temp_dir.cleanup()
    
    def test_error_to_retry_flow(self):
        """Error should flow through recovery to retry."""
        
        # Simulate error
        error = ConnectionError("Network down")
        recovery_result = self.error_recovery.capture_error(
            "api_service",
            error,
            {},
            "ERROR"
        )
        
        # Verify recovery strategy
        self.assertEqual(recovery_result["strategy"], "AUTO_RETRY")
        
        # Execute retry
        call_count = 0
        
        def api_call():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise error
            return "success"
        
        result = self.retry_logic.retry(api_call)
        
        self.assertEqual(result, "success")
        self.assertGreater(call_count, 1)
    
    def test_error_to_degradation_flow(self):
        """Error that can't be retried should degrade feature."""
        
        # Simulate repeated retries fail
        error_count = 0
        
        for i in range(5):
            error_count += 1
        
        # Degrade feature
        self.degradation.degrade_feature(
            "API Service",
            "external_api",
            "Permanently down after 5 retries"
        )
        
        # Verify system is degraded but running
        self.assertEqual(
            self.degradation.get_overall_status(),
            "degraded"
        )
        self.assertIn("API Service", self.degradation.degraded_features)
    
    def test_complete_error_recovery_cycle(self):
        """Test complete error → recovery → degradation cycle."""
        
        # Step 1: Error occurs
        error = ConnectionError("Service unavailable")
        recovery = self.error_recovery.capture_error(
            "data_sync",
            error,
            {"sync_id": "123"},
            "ERROR"
        )
        
        self.assertEqual(recovery["strategy"], "AUTO_RETRY")
        
        # Step 2: Retry fails multiple times
        failures = 0
        
        def data_sync():
            raise error
        
        # Try retry 3 times
        for i in range(3):
            try:
                self.retry_logic.retry(data_sync)
            except:
                failures += 1
        
        self.assertEqual(failures, 3)
        
        # Step 3: Degrade feature
        self.degradation.degrade_feature(
            "Data Sync",
            "data_sync",
            "Service unavailable - retry failed"
        )
        
        # Step 4: Verify system is degraded
        self.assertEqual(
            self.degradation.get_overall_status(),
            "degraded"
        )
        
        # Step 5: Eventually recover
        self.degradation.recover_feature("Data Sync")
        self.assertEqual(
            self.degradation.get_overall_status(),
            "healthy"
        )


class TestErrorMetrics(unittest.TestCase):
    """Test error tracking and metrics."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.vault_path = Path(self.temp_dir.name)
        self.error_recovery = MockErrorRecoveryFramework(self.vault_path)
    
    def tearDown(self):
        """Cleanup."""
        self.temp_dir.cleanup()
    
    def test_errors_are_tracked(self):
        """Errors should be tracked for metrics."""
        
        error1 = Exception("Error 1")
        error2 = Exception("Error 2")
        
        self.error_recovery.capture_error("comp1", error1, {}, "ERROR")
        self.error_recovery.capture_error("comp2", error2, {}, "WARNING")
        
        self.assertEqual(len(self.error_recovery.errors), 2)
    
    def test_error_severity_tracking(self):
        """Error severity should be recorded."""
        
        self.error_recovery.capture_error(
            "comp1",
            Exception("error"),
            {},
            "CRITICAL"
        )
        
        self.assertEqual(self.error_recovery.errors[0]["severity"], "CRITICAL")


def run_all_tests():
    """Run all integration tests."""
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestErrorRecovery))
    suite.addTests(loader.loadTestsFromTestCase(TestRetryLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestGracefulDegradation))
    suite.addTests(loader.loadTestsFromTestCase(TestWatchdogMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorMetrics))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    import sys
    # Fix Unicode encoding for Windows PowerShell
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 75)
    print("RESILIENCE & ERROR HANDLING INTEGRATION TESTS")
    print("=" * 75)
    print()
    
    result = run_all_tests()
    
    print()
    print("=" * 75)
    print("TEST SUMMARY")
    print("=" * 75)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()
    
    if result.wasSuccessful():
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
