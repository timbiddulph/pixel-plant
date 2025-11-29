#!/usr/bin/env python3
"""
Pixel Plant AI Companion - Enhanced Version
Main application with state persistence and power management

This version adds:
- Robust state persistence with auto-save
- State recovery after power loss
- Low-power sleep modes with PIR wake
- Graceful handling of unexpected shutdowns
"""

import sys
import time
import logging
import signal
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config import get_config
from hardware import LEDMatrix, AudioSystem, CameraSystem, MotionSensor
from personality import (
    MessageLibrary, MessageType, MoodManager, Mood,
    PixelAnimator, ColorPalette, get_pattern
)
from ai import BehaviorMonitor, ActivityState, PatternLearner
from state_manager import StateManager
from power_manager import PowerManager, PowerState

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


class PixelPlant:
    """Main Pixel Plant AI Companion application with power management"""

    def __init__(self):
        """Initialize the Pixel Plant system"""
        logger.info("🌿 Pixel Plant AI Companion starting...")

        # Load configuration
        self.config = get_config()

        # Initialize state manager (loads previous state if exists)
        self.state_manager = StateManager(
            data_directory=self.config.system.data_directory,
            auto_save_interval=self.config.power_management.auto_save_interval_seconds
        )

        # Check if recovering from crash
        if self.state_manager.recovered_from_crash:
            uptime_hours = self.state_manager.previous_uptime_seconds / 3600
            logger.warning(
                f"⚠️  Recovered from unclean shutdown "
                f"(previous uptime: {uptime_hours:.1f} hours)"
            )

        # Initialize hardware
        self._init_hardware()

        # Initialize power manager
        self.power_manager = PowerManager(
            idle_timeout_minutes=self.config.power_management.idle_timeout_minutes,
            light_sleep_timeout_minutes=self.config.power_management.light_sleep_timeout_minutes,
            deep_sleep_timeout_minutes=self.config.power_management.deep_sleep_timeout_minutes,
            pir_check_interval_seconds=self.config.power_management.pir_check_interval_seconds
        )

        # Register PIR sensor with power manager
        if self.config.power_management.pir_wake_enabled:
            self.power_manager.register_pir_sensor(self.pir.is_motion_detected)

        # Register power callbacks
        self.power_manager.register_sleep_callback(self._on_sleep)
        self.power_manager.register_wake_callback(self._on_wake)

        # Initialize personality
        self.messages = MessageLibrary(
            personality_level=self.config.personality.caring_level
        )

        # Restore mood from state
        saved_mood_str = self.state_manager.get('current_mood')
        saved_concern = self.state_manager.get('concern_level')
        try:
            initial_mood = Mood(saved_mood_str) if saved_mood_str else Mood.CONTENT
        except ValueError:
            initial_mood = Mood.CONTENT

        self.mood = MoodManager(initial_mood=initial_mood)
        self.mood.concern_level = saved_concern or 0

        self.animator = PixelAnimator()

        # Initialize AI
        self.behavior = BehaviorMonitor(
            pose_detection_enabled=self.config.ai.pose_detection_enabled,
            confidence_threshold=self.config.ai.confidence_threshold,
            simulate=self.config.debug.simulate_hardware
        )

        self.learner = PatternLearner(
            data_directory=self.config.system.data_directory,
            learning_enabled=self.config.behavior.learning_enabled,
            pattern_window_days=self.config.behavior.pattern_window_days
        )

        # Restore timestamps from state
        self._restore_state()

        # State tracking
        self.running = False

        logger.info("✅ Pixel Plant initialized successfully")

    def _restore_state(self):
        """Restore state from state manager"""
        # Restore hydration reminder timestamp
        last_hydration_str = self.state_manager.get('last_hydration_reminder')
        try:
            self.last_hydration_reminder = datetime.fromisoformat(last_hydration_str)
        except (ValueError, TypeError):
            self.last_hydration_reminder = datetime.now()

        # Restore last mood update
        self.last_mood_update = datetime.now()

        # Restore activity times if available
        sitting_start_str = self.state_manager.get('sitting_start')
        if sitting_start_str:
            try:
                self.behavior.sitting_start = datetime.fromisoformat(sitting_start_str)
            except (ValueError, TypeError):
                pass

        logger.info("State restored from previous session")

    def _init_hardware(self):
        """Initialize all hardware components"""
        simulate = self.config.debug.simulate_hardware

        self.led = LEDMatrix(
            gpio_pin=self.config.hardware.led_gpio_pin,
            width=self.config.hardware.led_width,
            height=self.config.hardware.led_height,
            brightness=self.config.hardware.led_brightness,
            simulate=simulate
        )

        self.audio = AudioSystem(
            volume=self.config.hardware.audio_volume,
            rate=self.config.personality.voice_rate,
            voice_enabled=self.config.personality.voice_enabled,
            simulate=simulate
        )

        self.camera = CameraSystem(
            resolution=self.config.hardware.camera_resolution,
            framerate=self.config.hardware.camera_framerate,
            rotation=self.config.hardware.camera_rotation,
            simulate=simulate
        )

        self.pir = MotionSensor(
            gpio_pin=self.config.hardware.pir_gpio_pin,
            enabled=self.config.hardware.pir_enabled,
            simulate=simulate
        )

    def _on_sleep(self, sleep_state: PowerState):
        """
        Called when entering sleep mode

        Args:
            sleep_state: Target sleep state
        """
        logger.info(f"💤 Entering {sleep_state.value}")

        # Update mood
        self.mood.sleep()
        self._update_state_from_mood()

        if sleep_state == PowerState.IDLE:
            # IDLE: Reduce camera frame rate, dim LEDs
            pattern, palette = self.mood.get_visual_representation()
            self.led.show_pattern(pattern, palette)

        elif sleep_state == PowerState.LIGHT_SLEEP:
            # LIGHT_SLEEP: Turn off LED and camera, keep PIR
            self.led.clear()
            # Note: Camera stop handled in main loop

        elif sleep_state == PowerState.DEEP_SLEEP:
            # DEEP_SLEEP: Everything off except PIR
            self.led.clear()

        # Save state immediately when going to sleep
        self._save_current_state()

    def _on_wake(self):
        """Called when waking from sleep"""
        logger.info("👁️  Waking up from sleep")

        # Update mood
        self.mood.wake()
        self._update_state_from_mood()

        # Greet user
        greeting = self.messages.get_message(MessageType.GREETING)
        self.audio.speak(greeting)

        # Show happy face
        pattern, palette = self.mood.get_visual_representation()
        self.led.show_pattern(pattern, palette)

        # Save state
        self._save_current_state()

    def start(self):
        """Start the Pixel Plant companion"""
        self.running = True

        # Start auto-save
        self.state_manager.start_auto_save()

        # Start power monitoring if enabled
        if self.config.power_management.enabled:
            self.power_manager.start_monitoring()

        # Start hardware
        self.camera.start()

        # Greet user
        self._greet_user()

        # Main loop
        try:
            logger.info("🌱 Pixel Plant is now active and caring!")
            self._main_loop()

        except KeyboardInterrupt:
            logger.info("Shutdown requested by user")

        finally:
            self.stop()

    def stop(self):
        """Stop the Pixel Plant and cleanup"""
        logger.info("🌿 Pixel Plant shutting down...")

        self.running = False

        # Stop power monitoring
        if self.config.power_management.enabled:
            self.power_manager.shutdown()

        # Say goodbye
        self._say_goodbye()

        # Save state
        self._save_current_state()

        # Save learned patterns
        self.learner.save_patterns()

        # Shutdown state manager (marks clean shutdown)
        self.state_manager.shutdown(clean=True)

        # Cleanup hardware
        self.led.close()
        self.audio.close()
        self.camera.close()
        self.pir.close()

        logger.info("✅ Pixel Plant stopped cleanly")

    def _main_loop(self):
        """Main application loop"""
        frame_count = 0

        while self.running:
            try:
                frame_start = time.time()

                # Check if we're in sleep mode
                power_state = self.power_manager.current_state

                if power_state == PowerState.DEEP_SLEEP:
                    # Deep sleep - minimal processing, PIR wake handled by power manager
                    time.sleep(1)
                    continue

                elif power_state == PowerState.LIGHT_SLEEP:
                    # Light sleep - no camera, just PIR monitoring
                    time.sleep(0.5)
                    continue

                # ACTIVE or IDLE state - normal operation

                # Update motion from PIR
                if self.pir.is_motion_detected():
                    self.behavior.update_motion(True)
                    self.power_manager.report_activity()  # Report to power manager

                # Analyze camera frame (every few frames to save processing)
                if frame_count % 5 == 0:
                    frame = self.camera.capture_frame()
                    if frame is not None:
                        activity_state = self.behavior.analyze_frame(frame)
                        self.learner.log_activity('state_update', activity_state.value)
                        self.power_manager.report_activity()  # User is present

                # Check daily stats reset
                self.state_manager.check_daily_reset()

                # Check health reminders (only in ACTIVE state)
                if power_state == PowerState.ACTIVE:
                    self._check_health_reminders()

                # Update mood display
                self._update_mood_display()

                # Periodic state save on important changes
                if frame_count % 100 == 0:  # Every 100 frames
                    self._save_current_state()

                # Frame timing
                frame_count += 1
                elapsed = time.time() - frame_start
                target_delay = 1.0 / self.config.hardware.camera_framerate

                if elapsed < target_delay:
                    time.sleep(target_delay - elapsed)

            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                time.sleep(1)

    def _greet_user(self):
        """Greet the user on startup"""
        greeting = self.messages.get_message(MessageType.GREETING)
        self.audio.speak(greeting)

        # Show happy face
        pattern, palette = self.mood.get_visual_representation()
        self.led.show_pattern(pattern, palette)

        logger.info(f"Greeted user: '{greeting}'")

    def _say_goodbye(self):
        """Say goodbye on shutdown"""
        goodbye = self.messages.get_message(MessageType.GOODNIGHT)
        self.audio.speak(goodbye)

        # Brief wave animation before clearing
        time.sleep(0.5)
        self.led.clear()

    def _check_health_reminders(self):
        """Check if health reminders are needed"""

        # Movement reminder
        if self.behavior.should_remind_to_move(
            self.config.behavior.sitting_threshold_minutes
        ):
            self._send_movement_reminder()

        # Hydration reminder
        time_since_hydration = datetime.now() - self.last_hydration_reminder
        if time_since_hydration >= timedelta(
            minutes=self.config.behavior.hydration_interval_minutes
        ):
            self._send_hydration_reminder()

    def _send_movement_reminder(self):
        """Send caring movement reminder"""
        urgency = self.mood.get_urgency_level()
        message = self.messages.compose_reminder(MessageType.MOVEMENT, urgency)

        # Show icon and speak
        icon, palette = self.mood.get_icon_for_message('movement')
        if icon:
            self.led.show_pattern(icon, palette)

        self.audio.speak(message)

        # Escalate concern
        if self.config.personality.escalation_enabled:
            self.mood.escalate_concern()
            self._update_state_from_mood()

        # Update state
        self.state_manager.update(
            last_movement_reminder=datetime.now().isoformat(),
            movement_count_today=self.state_manager.get('movement_count_today') + 1
        )

        # Log
        self.learner.log_activity('reminder_sent', 'movement', {'urgency': urgency})
        logger.info(f"Movement reminder sent (urgency {urgency}): '{message}'")

        # Save state on important event
        if self.config.power_management.save_on_state_change:
            self._save_current_state()

    def _send_hydration_reminder(self):
        """Send caring hydration reminder"""
        urgency = self.mood.get_urgency_level()
        message = self.messages.compose_reminder(MessageType.HYDRATION, urgency)

        # Show water drop icon
        icon, palette = self.mood.get_icon_for_message('hydration')
        if icon:
            self.led.show_pattern(icon, palette)

        self.audio.speak(message)

        # Update timestamp
        self.last_hydration_reminder = datetime.now()

        # Update state
        self.state_manager.update(
            last_hydration_reminder=self.last_hydration_reminder.isoformat(),
            hydration_count_today=self.state_manager.get('hydration_count_today') + 1
        )

        # Log
        self.learner.log_activity('reminder_sent', 'hydration', {'urgency': urgency})
        logger.info(f"Hydration reminder sent: '{message}'")

        # Save state on important event
        if self.config.power_management.save_on_state_change:
            self._save_current_state()

    def _update_mood_display(self):
        """Update LED display based on current mood"""
        now = datetime.now()
        elapsed = (now - self.last_mood_update).total_seconds()

        if elapsed < self.config.animations.mood_update_seconds:
            return

        self.last_mood_update = now

        # Get current mood representation
        pattern, palette = self.mood.get_visual_representation()

        # Apply breathing effect for organic feel
        if self.config.animations.transition_style == 'breathing':
            self.led.breathing_effect(
                pattern, palette,
                duration=self.config.animations.breathing_speed,
                steps=20
            )
        else:
            self.led.show_pattern(pattern, palette)

    def _save_current_state(self):
        """Save current application state"""
        self.state_manager.update(
            current_mood=self.mood.current_mood.value,
            concern_level=self.mood.concern_level,
            is_sleeping=(self.power_manager.current_state != PowerState.ACTIVE),
            sitting_start=self.behavior.sitting_start.isoformat() if self.behavior.sitting_start else None,
            total_sitting_seconds=self.behavior.total_sitting_time.total_seconds(),
            total_standing_seconds=self.behavior.total_standing_time.total_seconds(),
            total_moving_seconds=self.behavior.total_moving_time.total_seconds(),
            last_seen=datetime.now().isoformat(),
        )

    def _update_state_from_mood(self):
        """Update state manager when mood changes"""
        self.state_manager.update(
            current_mood=self.mood.current_mood.value,
            concern_level=self.mood.concern_level
        )


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}")
    sys.exit(0)


def main():
    """Main entry point"""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        plant = PixelPlant()
        plant.start()

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
