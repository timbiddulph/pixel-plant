"""
Behavioral Monitoring System
Tracks user activity, posture, and patterns
"""

import time
import logging
from enum import Enum
from typing import Optional, Dict
from datetime import datetime, timedelta

from .pose_detection import PoseDetector, PostureType

logger = logging.getLogger(__name__)


class ActivityState(Enum):
    """User activity states"""
    UNKNOWN = "unknown"
    SITTING = "sitting"
    STANDING = "standing"
    MOVING = "moving"
    AWAY = "away"


class BehaviorMonitor:
    """Monitors user behavior and activity patterns"""

    def __init__(self, pose_detection_enabled: bool = True,
                 confidence_threshold: float = 0.7,
                 simulate: bool = False):
        """
        Initialize behavior monitor

        Args:
            pose_detection_enabled: Enable AI pose detection
            confidence_threshold: Minimum confidence for detections
            simulate: Use simulated data instead of camera
        """
        self.pose_detection_enabled = pose_detection_enabled
        self.confidence_threshold = confidence_threshold
        self.simulate = simulate

        # State tracking
        self.current_state = ActivityState.UNKNOWN
        self.last_state_change = datetime.now()
        self.last_motion = datetime.now()
        self.sitting_start = None
        self.last_movement = None

        # Statistics
        self.total_sitting_time = timedelta()
        self.total_standing_time = timedelta()
        self.total_moving_time = timedelta()

        # Pose detection
        self.pose_detector = None
        self.poor_posture_count = 0  # Track consecutive poor posture detections

        if not simulate and pose_detection_enabled:
            self._init_pose_detection()
        else:
            logger.info("Behavior monitor running in simulation mode")

    def _init_pose_detection(self):
        """Initialize pose detection"""
        try:
            self.pose_detector = PoseDetector(
                confidence_threshold=self.confidence_threshold,
                simulate=self.simulate
            )
            logger.info("Pose detection initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize pose detection: {e}")
            self.simulate = True
            self.pose_detector = None

    def analyze_frame(self, frame) -> ActivityState:
        """
        Analyze camera frame for user activity

        Args:
            frame: Camera frame (NumPy array)

        Returns:
            Detected activity state
        """
        if self.simulate or frame is None or self.pose_detector is None:
            # Simulate activity cycling
            elapsed = (datetime.now() - self.last_state_change).total_seconds()

            if elapsed > 30:  # Change state every 30s for testing
                states = [ActivityState.SITTING, ActivityState.STANDING, ActivityState.MOVING]
                import random
                new_state = random.choice(states)
                self._update_state(new_state)

            return self.current_state

        # Use pose detector
        posture, confidence, landmarks = self.pose_detector.detect_posture(frame)

        # Map posture to activity state
        if posture == PostureType.ABSENT:
            detected_state = ActivityState.AWAY

        elif posture == PostureType.SITTING:
            detected_state = ActivityState.SITTING

        elif posture == PostureType.STANDING:
            detected_state = ActivityState.STANDING

        elif posture == PostureType.LEANING_FORWARD:
            # Poor posture while sitting
            detected_state = ActivityState.SITTING
            self.poor_posture_count += 1

            # Log warning after consecutive detections
            if self.poor_posture_count >= 5:
                logger.warning("Poor posture detected (leaning forward)")
                self.poor_posture_count = 0

        else:  # UNKNOWN
            detected_state = ActivityState.UNKNOWN

        # Update state if confident
        if confidence >= self.confidence_threshold:
            self._update_state(detected_state)

            # Reset poor posture count if not leaning
            if posture != PostureType.LEANING_FORWARD:
                self.poor_posture_count = 0

        return self.current_state

    def update_motion(self, motion_detected: bool):
        """
        Update based on motion sensor

        Args:
            motion_detected: True if PIR detected motion
        """
        if motion_detected:
            self.last_motion = datetime.now()

            # If we thought user was away, update state
            if self.current_state == ActivityState.AWAY:
                self._update_state(ActivityState.UNKNOWN)

    def _update_state(self, new_state: ActivityState):
        """Update activity state and track statistics"""
        if new_state == self.current_state:
            return

        now = datetime.now()
        elapsed = now - self.last_state_change

        # Update statistics for previous state
        if self.current_state == ActivityState.SITTING:
            self.total_sitting_time += elapsed
        elif self.current_state == ActivityState.STANDING:
            self.total_standing_time += elapsed
        elif self.current_state == ActivityState.MOVING:
            self.total_moving_time += elapsed

        # Update state
        old_state = self.current_state
        self.current_state = new_state
        self.last_state_change = now

        # Track sitting start time
        if new_state == ActivityState.SITTING:
            self.sitting_start = now
        elif old_state == ActivityState.SITTING:
            self.sitting_start = None

        logger.info(f"Activity state: {old_state.value} → {new_state.value}")

    def get_sitting_duration(self) -> timedelta:
        """
        Get current sitting duration

        Returns:
            Time sitting in current session
        """
        if self.current_state == ActivityState.SITTING and self.sitting_start:
            return datetime.now() - self.sitting_start
        return timedelta()

    def get_time_since_motion(self) -> timedelta:
        """
        Get time since last motion detected

        Returns:
            Time since motion
        """
        return datetime.now() - self.last_motion

    def should_remind_to_move(self, threshold_minutes: int = 45) -> bool:
        """
        Check if user should be reminded to move

        Args:
            threshold_minutes: Sitting time threshold

        Returns:
            True if reminder needed
        """
        sitting_duration = self.get_sitting_duration()
        return sitting_duration >= timedelta(minutes=threshold_minutes)

    def should_remind_hydration(self, interval_minutes: int = 60) -> bool:
        """
        Check if hydration reminder is due

        Args:
            interval_minutes: Reminder interval

        Returns:
            True if reminder needed
        """
        # TODO: Track last hydration reminder time
        # For now, use simple time-based logic
        if not hasattr(self, '_last_hydration_reminder'):
            self._last_hydration_reminder = datetime.now()

        elapsed = datetime.now() - self._last_hydration_reminder

        if elapsed >= timedelta(minutes=interval_minutes):
            self._last_hydration_reminder = datetime.now()
            return True

        return False

    def is_user_away(self, inactivity_minutes: int = 30) -> bool:
        """
        Check if user appears to be away

        Args:
            inactivity_minutes: Inactivity threshold

        Returns:
            True if user is likely away
        """
        time_since_motion = self.get_time_since_motion()
        return time_since_motion >= timedelta(minutes=inactivity_minutes)

    def get_statistics(self) -> Dict:
        """
        Get activity statistics

        Returns:
            Dictionary of statistics
        """
        return {
            'current_state': self.current_state.value,
            'sitting_duration': str(self.get_sitting_duration()),
            'total_sitting': str(self.total_sitting_time),
            'total_standing': str(self.total_standing_time),
            'total_moving': str(self.total_moving_time),
            'time_since_motion': str(self.get_time_since_motion()),
        }

    def reset_statistics(self):
        """Reset all statistics"""
        self.total_sitting_time = timedelta()
        self.total_standing_time = timedelta()
        self.total_moving_time = timedelta()

    def check_user_responded_to_movement_reminder(self, timeout_seconds: int = 300) -> bool:
        """
        Check if user stood up after movement reminder

        Args:
            timeout_seconds: How long to wait for response

        Returns:
            True if user stood up or moved within timeout
        """
        if not hasattr(self, '_movement_reminder_time'):
            return False

        time_since_reminder = (datetime.now() - self._movement_reminder_time).total_seconds()

        if time_since_reminder > timeout_seconds:
            # Timeout - consider no response
            delattr(self, '_movement_reminder_time')
            return False

        # Check if state changed from sitting
        if self.current_state in [ActivityState.STANDING, ActivityState.MOVING]:
            delattr(self, '_movement_reminder_time')
            return True

        return False

    def mark_movement_reminder_sent(self):
        """Mark that a movement reminder was just sent"""
        self._movement_reminder_time = datetime.now()

    def has_poor_posture(self) -> bool:
        """Check if user currently has poor posture"""
        return self.poor_posture_count > 0

    def get_posture_quality_score(self) -> float:
        """
        Get posture quality score (0-1)

        Returns:
            1.0 = good posture, 0.0 = poor posture
        """
        if self.poor_posture_count == 0:
            return 1.0
        elif self.poor_posture_count < 3:
            return 0.7
        elif self.poor_posture_count < 5:
            return 0.4
        else:
            return 0.0


if __name__ == '__main__':
    """Test behavior monitor"""
    logging.basicConfig(level=logging.INFO)

    monitor = BehaviorMonitor(simulate=True)

    print("=== BEHAVIOR MONITOR TEST ===\n")

    # Simulate monitoring cycle
    for i in range(5):
        # Simulate frame analysis
        state = monitor.analyze_frame(None)

        # Print statistics
        stats = monitor.get_statistics()
        print(f"\nCycle {i+1}:")
        print(f"  State: {stats['current_state']}")
        print(f"  Sitting: {stats['sitting_duration']}")
        print(f"  Since motion: {stats['time_since_motion']}")

        # Check reminders
        if monitor.should_remind_to_move(threshold_minutes=0):
            print("  → Movement reminder needed!")

        time.sleep(1)
