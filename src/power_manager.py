"""
Power Manager Module
Handles low-power sleep mode and PIR-based wake functionality
Optimized for always-on operation with minimal power consumption
"""

import logging
import time
import threading
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Callable

logger = logging.getLogger(__name__)


class PowerState(Enum):
    """System power states"""
    ACTIVE = "active"           # Fully operational
    IDLE = "idle"               # Reduced activity, monitoring for user
    LIGHT_SLEEP = "light_sleep" # LED off, camera off, PIR monitoring
    DEEP_SLEEP = "deep_sleep"   # Everything off except PIR


class PowerManager:
    """
    Manages system power states for optimal always-on operation

    Features:
    - Progressive power reduction based on inactivity
    - PIR sensor wake from sleep
    - Configurable timeout periods
    - Wake callbacks for system components
    - Power state transition logging
    """

    def __init__(self,
                 idle_timeout_minutes: int = 5,
                 light_sleep_timeout_minutes: int = 15,
                 deep_sleep_timeout_minutes: int = 60,
                 pir_check_interval_seconds: float = 1.0):
        """
        Initialize power manager

        Args:
            idle_timeout_minutes: Minutes until IDLE state
            light_sleep_timeout_minutes: Minutes until LIGHT_SLEEP
            deep_sleep_timeout_minutes: Minutes until DEEP_SLEEP
            pir_check_interval_seconds: How often to check PIR in sleep
        """
        self.idle_timeout = timedelta(minutes=idle_timeout_minutes)
        self.light_sleep_timeout = timedelta(minutes=light_sleep_timeout_minutes)
        self.deep_sleep_timeout = timedelta(minutes=deep_sleep_timeout_minutes)
        self.pir_check_interval = pir_check_interval_seconds

        # State tracking
        self.current_state = PowerState.ACTIVE
        self.last_activity = datetime.now()
        self.state_changed_at = datetime.now()

        # Callbacks
        self.on_sleep_callbacks = []  # Called when entering sleep
        self.on_wake_callbacks = []   # Called when waking up
        self.get_pir_motion: Optional[Callable[[], bool]] = None

        # Threading
        self._running = False
        self._monitor_thread: Optional[threading.Thread] = None

        # Statistics
        self.wake_count = 0
        self.total_sleep_time = timedelta()
        self.last_sleep_start: Optional[datetime] = None

        logger.info("Power manager initialized")

    def register_sleep_callback(self, callback: Callable[[PowerState], None]):
        """
        Register callback to be called when entering sleep

        Args:
            callback: Function taking PowerState as argument
        """
        self.on_sleep_callbacks.append(callback)

    def register_wake_callback(self, callback: Callable[[], None]):
        """
        Register callback to be called when waking up

        Args:
            callback: Function with no arguments
        """
        self.on_wake_callbacks.append(callback)

    def register_pir_sensor(self, pir_check_func: Callable[[], bool]):
        """
        Register PIR sensor check function

        Args:
            pir_check_func: Function that returns True if motion detected
        """
        self.get_pir_motion = pir_check_func
        logger.info("PIR sensor registered with power manager")

    def report_activity(self):
        """Report user activity to reset sleep timers"""
        self.last_activity = datetime.now()

        # Wake from sleep if necessary
        if self.current_state != PowerState.ACTIVE:
            self._wake_up()

    def _wake_up(self):
        """Wake from sleep state"""
        old_state = self.current_state

        # Update statistics
        if self.last_sleep_start:
            sleep_duration = datetime.now() - self.last_sleep_start
            self.total_sleep_time += sleep_duration
            self.last_sleep_start = None

        self.wake_count += 1
        self.current_state = PowerState.ACTIVE
        self.state_changed_at = datetime.now()
        self.last_activity = datetime.now()

        logger.info(f"Waking from {old_state.value} (wake #{self.wake_count})")

        # Execute wake callbacks
        for callback in self.on_wake_callbacks:
            try:
                callback()
            except Exception as e:
                logger.error(f"Wake callback error: {e}")

    def _enter_sleep(self, new_state: PowerState):
        """
        Enter sleep state

        Args:
            new_state: Target sleep state
        """
        old_state = self.current_state

        if old_state == PowerState.ACTIVE:
            self.last_sleep_start = datetime.now()

        self.current_state = new_state
        self.state_changed_at = datetime.now()

        logger.info(f"Entering {new_state.value} from {old_state.value}")

        # Execute sleep callbacks
        for callback in self.on_sleep_callbacks:
            try:
                callback(new_state)
            except Exception as e:
                logger.error(f"Sleep callback error: {e}")

    def start_monitoring(self):
        """Start background power state monitoring"""
        if self._running:
            logger.warning("Power monitoring already running")
            return

        self._running = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True,
            name="PowerMonitor"
        )
        self._monitor_thread.start()
        logger.info("Power monitoring started")

    def stop_monitoring(self):
        """Stop background power monitoring"""
        self._running = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)
        logger.info("Power monitoring stopped")

    def _monitor_loop(self):
        """Background monitoring thread"""
        while self._running:
            # Determine sleep interval based on state
            if self.current_state == PowerState.ACTIVE:
                check_interval = 5.0  # Check every 5s when active
                self._check_sleep_transition()
            else:
                check_interval = self.pir_check_interval
                self._check_pir_wake()

            time.sleep(check_interval)

    def _check_sleep_transition(self):
        """Check if system should transition to sleep state"""
        if self.current_state == PowerState.ACTIVE:
            idle_time = datetime.now() - self.last_activity

            # Check for deep sleep first
            if idle_time >= self.deep_sleep_timeout:
                self._enter_sleep(PowerState.DEEP_SLEEP)
            # Then light sleep
            elif idle_time >= self.light_sleep_timeout:
                self._enter_sleep(PowerState.LIGHT_SLEEP)
            # Then idle
            elif idle_time >= self.idle_timeout:
                self._enter_sleep(PowerState.IDLE)

    def _check_pir_wake(self):
        """Check PIR sensor for motion to wake from sleep"""
        if self.current_state == PowerState.ACTIVE:
            return

        # Check PIR if function is registered
        if self.get_pir_motion:
            try:
                if self.get_pir_motion():
                    logger.debug("PIR motion detected, waking up")
                    self._wake_up()
            except Exception as e:
                logger.error(f"PIR check error: {e}")

    def get_state_info(self) -> dict:
        """Get current power state information"""
        idle_time = datetime.now() - self.last_activity
        state_duration = datetime.now() - self.state_changed_at

        return {
            'state': self.current_state.value,
            'idle_seconds': idle_time.total_seconds(),
            'state_duration_seconds': state_duration.total_seconds(),
            'wake_count': self.wake_count,
            'total_sleep_hours': self.total_sleep_time.total_seconds() / 3600,
        }

    def force_active(self):
        """Force system into active state (for manual wake)"""
        if self.current_state != PowerState.ACTIVE:
            logger.info("Forcing active state")
            self._wake_up()

    def force_sleep(self, state: PowerState = PowerState.LIGHT_SLEEP):
        """
        Force system into sleep state

        Args:
            state: Target sleep state (default LIGHT_SLEEP)
        """
        if state == PowerState.ACTIVE:
            logger.warning("Cannot force sleep to ACTIVE state")
            return

        logger.info(f"Forcing {state.value}")
        self._enter_sleep(state)

    def shutdown(self):
        """Prepare for shutdown"""
        logger.info("Power manager shutting down")
        self.stop_monitoring()

        # Log statistics
        uptime = datetime.now() - self.state_changed_at
        logger.info(
            f"Power stats - Uptime: {uptime.total_seconds()/3600:.1f}h, "
            f"Wakes: {self.wake_count}, "
            f"Sleep time: {self.total_sleep_time.total_seconds()/3600:.1f}h"
        )


class PowerAwareComponent:
    """
    Base class for components that need power state awareness

    Subclass this and implement sleep/wake methods
    """

    def on_sleep(self, sleep_state: PowerState):
        """
        Called when system enters sleep

        Args:
            sleep_state: Target sleep state
        """
        pass

    def on_wake(self):
        """Called when system wakes from sleep"""
        pass
