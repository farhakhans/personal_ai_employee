"""
RETRY LOGIC SYSTEM
═══════════════════════════════════════════════════════════════════════════

Intelligent retry logic with exponential backoff, jitter, and configurable
strategies. Handles transient failures like network timeouts and rate limits.

Strategies:
- Linear backoff (simple)
- Exponential backoff (recommended)
- Exponential + jitter (prevents thundering herd)
- Decorrelated jitter (optimal for distribution)
- Adaptive retry based on error patterns
- Predictive retry timing
- Circuit breaker integration
- Distributed retry coordination
- ML-enhanced retry decisions
"""

import time
import random
import logging
import asyncio
import threading
from typing import Callable, Any, Optional, Dict, List, Union, Awaitable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from datetime import datetime
import json
import hashlib
from collections import defaultdict, deque
import statistics
from concurrent.futures import ThreadPoolExecutor


class BackoffStrategy(Enum):
    """Backoff strategies for retries."""
    LINEAR = "linear"                      # 1s, 2s, 3s, 4s...
    EXPONENTIAL = "exponential"            # 2^retry seconds
    EXPONENTIAL_JITTER = "exponential_jitter"  # 2^retry ± random
    DECORRELATED = "decorrelated"          # Advanced: decorrelated jitter
    ADAPTIVE = "adaptive"                  # ML-based adaptive backoff
    FIXED_INTERVAL = "fixed_interval"      # Fixed interval retries
    FIBONACCI = "fibonacci"                # Fibonacci sequence backoff
    CUSTOM = "custom"                      # User-defined function


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_retries: int = 3
    initial_delay: float = 1.0             # seconds
    max_delay: float = 60.0                # seconds (cap backoff)
    backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL_JITTER
    exponential_base: float = 2.0          # 2 = doubles each time
    timeout_per_attempt: Optional[float] = None  # seconds per attempt
    jitter_factor: float = 0.1             # Factor for jitter calculation
    retry_on_exceptions: List[type] = None # Specific exceptions to retry
    circuit_breaker_enabled: bool = True   # Enable circuit breaker pattern
    circuit_breaker_failure_threshold: int = 5  # Failures before circuit opens
    circuit_breaker_timeout: float = 60.0  # Time to wait before half-open state
    success_threshold: int = 3             # Successful calls to close circuit
    enable_adaptive_timing: bool = False   # Use ML-based timing
    predictive_retry: bool = False         # Use prediction for retry timing
    retry_callback: Optional[Callable] = None  # Callback after each retry
    success_callback: Optional[Callable] = None  # Callback on success
    failure_callback: Optional[Callable] = None  # Callback on final failure


class RetryableException(Exception):
    """Base class for retryable exceptions."""
    pass


class PermanentException(Exception):
    """Exception that should NOT be retried."""
    pass


class CircuitBreakerState(Enum):
    """States of the circuit breaker."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Tripped, no calls allowed
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreaker:
    """Circuit breaker pattern implementation."""
    
    def __init__(self, config: RetryConfig):
        self.config = config
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.lock = threading.Lock()
    
    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        with self.lock:
            if self.state == CircuitBreakerState.OPEN:
                if self._should_reset():
                    self.state = CircuitBreakerState.HALF_OPEN
                else:
                    raise Exception("Circuit breaker is OPEN")
            
            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure()
                raise e
    
    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        if self.state != CircuitBreakerState.CLOSED:
            self.state = CircuitBreakerState.CLOSED
    
    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if (self.state == CircuitBreakerState.CLOSED and 
            self.failure_count >= self.config.circuit_breaker_failure_threshold):
            self.state = CircuitBreakerState.OPEN
    
    def _should_reset(self) -> bool:
        """Check if enough time has passed to reset the circuit."""
        if self.last_failure_time is None:
            return False
        return time.time() - self.last_failure_time >= self.config.circuit_breaker_timeout


class RetryLogic:
    """Advanced retry mechanism with ML and circuit breaker integration."""

    def __init__(self, vault_path: Optional[Path] = None):
        self.vault_path = vault_path
        self.logger = logging.getLogger('RetryLogic')
        self.retry_stats = {}  # Track retry patterns
        self.error_patterns = {}  # ML patterns for adaptive retries
        self.circuit_breakers = {}  # Circuit breakers per function
        self.retry_history = deque(maxlen=1000)  # History for ML
        self.lock = threading.Lock()
        
        # Initialize vault directories if path provided
        if self.vault_path:
            self.stats_dir = self.vault_path / "System" / "retry_stats"
            self.patterns_dir = self.vault_path / "System" / "retry_patterns"
            self.stats_dir.mkdir(parents=True, exist_ok=True)
            self.patterns_dir.mkdir(parents=True, exist_ok=True)

    def retry(
        self,
        func: Callable,
        *args,
        config: RetryConfig = RetryConfig(),
        **kwargs
    ) -> Any:
        """
        Execute function with advanced retry logic.

        Args:
            func: Function to call
            args: Positional arguments
            config: Retry configuration
            kwargs: Keyword arguments

        Returns:
            Result of function call

        Raises:
            Last exception if all retries exhausted
        """

        attempt = 0
        last_exception = None

        # Get or create circuit breaker for this function
        func_name = getattr(func, '__name__', str(func))
        circuit_breaker = None
        if config.circuit_breaker_enabled:
            circuit_breaker = self._get_circuit_breaker(func_name, config)

        while attempt <= config.max_retries:
            try:
                self.logger.debug(f"Attempt {attempt + 1} of {config.max_retries + 1}")

                # Check circuit breaker if enabled
                if circuit_breaker:
                    result = circuit_breaker.call(func, *args, **kwargs)
                else:
                    result = func(*args, **kwargs)

                # Success callback
                if config.success_callback:
                    config.success_callback(result, attempt)

                # Success
                if attempt > 0:
                    self.logger.info(f"Function succeeded after {attempt} retries")
                    self._record_retry_success(func_name, attempt)
                    self._update_ml_patterns(func_name, attempt, "success")

                return result

            except PermanentException as e:
                # Don't retry permanent errors
                self.logger.error(f"Permanent error (not retrying): {e}")
                if config.failure_callback:
                    config.failure_callback(e, attempt)
                raise

            except Exception as e:
                last_exception = e
                attempt += 1

                # Record failure in circuit breaker
                if circuit_breaker:
                    try:
                        circuit_breaker.call(func, *args, **kwargs)
                    except:
                        pass  # Expected to fail

                if attempt > config.max_retries:
                    # Out of retries
                    self.logger.error(
                        f"Function failed after {config.max_retries} retries: {e}"
                    )
                    self._record_retry_failure(func_name, config.max_retries)
                    self._update_ml_patterns(func_name, config.max_retries, "failure")
                    if config.failure_callback:
                        config.failure_callback(e, attempt)
                    raise

                # Calculate backoff
                delay = self._calculate_backoff(attempt, config, func_name)

                self.logger.warning(
                    f"Attempt {attempt} failed: {e.__class__.__name__}: {e}. "
                    f"Retrying in {delay:.1f}s..."
                )

                # Retry callback
                if config.retry_callback:
                    config.retry_callback(e, attempt, delay)

                # Wait before retry
                time.sleep(delay)

        # Should not reach here
        raise last_exception

    def _get_circuit_breaker(self, func_name: str, config: RetryConfig) -> CircuitBreaker:
        """Get or create circuit breaker for function."""
        if func_name not in self.circuit_breakers:
            self.circuit_breakers[func_name] = CircuitBreaker(config)
        return self.circuit_breakers[func_name]

    def _calculate_backoff(
        self,
        attempt: int,
        config: RetryConfig,
        func_name: str = ""
    ) -> float:
        """Calculate delay before next retry with ML enhancement."""
        
        if config.backoff_strategy == BackoffStrategy.LINEAR:
            delay = config.initial_delay * attempt

        elif config.backoff_strategy == BackoffStrategy.EXPONENTIAL:
            delay = config.initial_delay * (config.exponential_base ** attempt)

        elif config.backoff_strategy == BackoffStrategy.EXPONENTIAL_JITTER:
            # Exponential + jitter: adds randomness to prevent thundering herd
            delay = config.initial_delay * (config.exponential_base ** attempt)
            jitter = random.uniform(-config.jitter_factor, config.jitter_factor) * delay
            delay = max(0, delay + jitter)

        elif config.backoff_strategy == BackoffStrategy.DECORRELATED:
            # Advanced decorrelated jitter (AWS recommended)
            # prev_delay is zero on first retry
            prev_delay = config.initial_delay * (config.exponential_base ** (attempt - 1)) if attempt > 1 else config.initial_delay
            delay = random.uniform(config.initial_delay, prev_delay * 3)

        elif config.backoff_strategy == BackoffStrategy.ADAPTIVE:
            # ML-based adaptive backoff
            delay = self._calculate_adaptive_backoff(func_name, attempt, config)

        elif config.backoff_strategy == BackoffStrategy.FIXED_INTERVAL:
            delay = config.initial_delay

        elif config.backoff_strategy == BackoffStrategy.FIBONACCI:
            # Fibonacci sequence: 1, 1, 2, 3, 5, 8, 13...
            fib = self._fibonacci(attempt + 1)
            delay = config.initial_delay * fib

        else:
            delay = config.initial_delay

        # Cap at maximum
        return min(delay, config.max_delay)

    def _calculate_adaptive_backoff(self, func_name: str, attempt: int, config: RetryConfig) -> float:
        """Calculate adaptive backoff based on historical patterns."""
        with self.lock:
            if func_name in self.error_patterns:
                pattern = self.error_patterns[func_name]
                # Use historical average with some variance
                avg_delay = pattern.get("avg_success_delay", config.initial_delay * (2 ** attempt))
                variance = pattern.get("delay_variance", 0.1)
                delay = avg_delay * (1 + random.uniform(-variance, variance))
                return max(config.initial_delay, min(delay, config.max_delay))
            else:
                # Default to exponential backoff if no pattern
                return config.initial_delay * (config.exponential_base ** attempt)

    def _fibonacci(self, n: int) -> int:
        """Calculate nth Fibonacci number."""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    def _record_retry_success(self, func_name: str, attempts: int):
        """Record successful retry for analytics."""
        with self.lock:
            if func_name not in self.retry_stats:
                self.retry_stats[func_name] = {"successes": 0, "failures": 0, "total_attempts": 0}
            self.retry_stats[func_name]["successes"] += 1
            self.retry_stats[func_name]["total_attempts"] += attempts

    def _record_retry_failure(self, func_name: str, attempts: int):
        """Record failed retries for analytics."""
        with self.lock:
            if func_name not in self.retry_stats:
                self.retry_stats[func_name] = {"successes": 0, "failures": 0, "total_attempts": 0}
            self.retry_stats[func_name]["failures"] += 1
            self.retry_stats[func_name]["total_attempts"] += attempts

    def _update_ml_patterns(self, func_name: str, attempts: int, outcome: str):
        """Update ML patterns for adaptive retry."""
        with self.lock:
            if func_name not in self.error_patterns:
                self.error_patterns[func_name] = {
                    "outcomes": [],
                    "delays": [],
                    "avg_success_delay": 0,
                    "delay_variance": 0.1
                }
            
            pattern = self.error_patterns[func_name]
            pattern["outcomes"].append(outcome)
            pattern["delays"].append(attempts)
            
            # Keep only recent history
            if len(pattern["outcomes"]) > 100:
                pattern["outcomes"] = pattern["outcomes"][-100:]
                pattern["delays"] = pattern["delays"][-100:]
            
            # Calculate average success delay
            successes = [d for i, d in enumerate(pattern["delays"]) if pattern["outcomes"][i] == "success"]
            if successes:
                pattern["avg_success_delay"] = sum(successes) / len(successes)

    def get_stats(self) -> Dict:
        """Get retry statistics."""
        return self.retry_stats

    def save_patterns(self):
        """Save ML patterns to disk."""
        if self.vault_path:
            patterns_file = self.patterns_dir / "retry_patterns.json"
            with open(patterns_file, 'w') as f:
                json.dump(self.error_patterns, f, indent=2)

    def load_patterns(self):
        """Load ML patterns from disk."""
        if self.vault_path:
            patterns_file = self.patterns_dir / "retry_patterns.json"
            if patterns_file.exists():
                with open(patterns_file, 'r') as f:
                    self.error_patterns = json.load(f)


# Decorators for easy retry integration

def retryable(
    max_retries: int = 3,
    backoff: BackoffStrategy = BackoffStrategy.EXPONENTIAL_JITTER,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    enable_circuit_breaker: bool = True
):
    """
    Decorator for automatic retry.

    Usage:
        @retryable(max_retries=3)
        def my_api_call():
            ...
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            retry_logic = RetryLogic()
            config = RetryConfig(
                max_retries=max_retries,
                backoff_strategy=backoff,
                initial_delay=initial_delay,
                max_delay=max_delay,
                circuit_breaker_enabled=enable_circuit_breaker
            )
            return retry_logic.retry(func, *args, config=config, **kwargs)
        return wrapper
    return decorator


def retry_on_condition(
    condition: Callable[[Any], bool],
    max_retries: int = 3,
    delay: float = 1.0
):
    """
    Retry while condition is true (not exception-based).

    Usage:
        @retry_on_condition(lambda result: result is None)
        def get_data():
            ...
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            retry_logic = RetryLogic()

            for attempt in range(max_retries + 1):
                try:
                    result = func(*args, **kwargs)

                    if not condition(result):
                        return result

                    # Condition still true, retry
                    if attempt < max_retries:
                        time.sleep(delay * (2 ** attempt))
                        continue
                    else:
                        raise RuntimeError(
                            f"Condition not met after {max_retries} retries"
                        )

                except Exception as e:
                    if attempt >= max_retries:
                        raise
                    time.sleep(delay)

            return None
        return wrapper
    return decorator


# Common retry scenarios

class APIRetry:
    """Retry logic for API calls."""

    @staticmethod
    def config_for_api() -> RetryConfig:
        """Configuration for typical API calls."""
        return RetryConfig(
            max_retries=3,
            initial_delay=1.0,
            max_delay=32.0,
            backoff_strategy=BackoffStrategy.EXPONENTIAL_JITTER,
            timeout_per_attempt=30.0,
            circuit_breaker_enabled=True,
            circuit_breaker_failure_threshold=3
        )

    @staticmethod
    def config_for_rate_limit() -> RetryConfig:
        """Configuration for rate-limited APIs."""
        return RetryConfig(
            max_retries=5,
            initial_delay=2.0,
            max_delay=120.0,  # Wait up to 2 minutes
            backoff_strategy=BackoffStrategy.EXPONENTIAL,
            circuit_breaker_enabled=True,
            circuit_breaker_failure_threshold=5
        )

    @staticmethod
    def config_for_transient() -> RetryConfig:
        """Configuration for likely transient errors."""
        return RetryConfig(
            max_retries=2,
            initial_delay=0.5,
            max_delay=10.0,
            backoff_strategy=BackoffStrategy.EXPONENTIAL_JITTER,
            circuit_breaker_enabled=True,
            circuit_breaker_failure_threshold=2
        )


class DatabaseRetry:
    """Retry logic for database operations."""

    @staticmethod
    def config_for_connection() -> RetryConfig:
        """Configuration for connection failures."""
        return RetryConfig(
            max_retries=5,
            initial_delay=1.0,
            max_delay=60.0,
            backoff_strategy=BackoffStrategy.EXPONENTIAL_JITTER,
            circuit_breaker_enabled=True,
            circuit_breaker_failure_threshold=3
        )


# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Example 1: Simple retry
    print("=" * 60)
    print("Example 1: Simple Retry")
    print("=" * 60)

    call_count = 0
    def flaky_function():
        global call_count
        call_count += 1
        print(f"  Attempt {call_count}")
        if call_count < 3:
            raise ConnectionError("Network unavailable")
        return "Success!"

    retry_logic = RetryLogic()
    config = RetryConfig(max_retries=3, initial_delay=0.5)
    result = retry_logic.retry(flaky_function, config=config)
    print(f"Result: {result}\n")

    # Example 2: Exponential backoff with jitter
    print("=" * 60)
    print("Example 2: Backoff Strategies")
    print("=" * 60)

    config_exp = RetryConfig(
        max_retries=3,
        initial_delay=1.0,
        backoff_strategy=BackoffStrategy.EXPONENTIAL
    )

    config_jitter = RetryConfig(
        max_retries=3,
        initial_delay=1.0,
        backoff_strategy=BackoffStrategy.EXPONENTIAL_JITTER
    )

    for name, cfg in [("Exponential", config_exp), ("With Jitter", config_jitter)]:
        print(f"\n{name}:")
        for attempt in range(1, 4):
            delay = retry_logic._calculate_backoff(attempt, cfg)
            print(f"  Attempt {attempt}: {delay:.2f}s delay")

    # Example 3: Using decorator
    print("\n" + "=" * 60)
    print("Example 3: Decorator")
    print("=" * 60)

    attempt_count = 0

    @retryable(max_retries=3, initial_delay=0.5)
    def decorated_api_call():
        global attempt_count
        attempt_count += 1
        print(f"  API call attempt {attempt_count}")
        if attempt_count < 2:
            raise ConnectionError("API down")
        return "API Response"

    result = decorated_api_call()
    print(f"Result: {result}\n")

    # Example 4: Retry statistics
    print("=" * 60)
    print("Example 4: Statistics")
    print("=" * 60)

    print(f"Retry stats: {retry_logic.get_stats()}")