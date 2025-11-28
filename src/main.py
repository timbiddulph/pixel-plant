#!/usr/bin/env python3
"""
Pixel Plant AI Companion
Main application entry point

Caring technology inspired by "The Long Way to a Small, Angry Planet"
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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


class PixelPlant:
    """Main Pixel Plant AI Companion application"""

    def __init__(self):
        """Initialize the Pixel Plant system"""
        logger.info("🌿 Pixel Plant AI Companion starting...")

        # Load configuration
        self.config = get_config()

        # Initialize hardware
        self._init_hardware()

        # Initialize personality
        self.messages = MessageLibrary(
            personality_level=self.config.personality.caring_level
        )
        self.mood = MoodManager(initial_mood=Mood.CONTENT)
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

        # State tracking
        self.running = False
        self.last_mood_update = datetime.now()
        self.last_hydration_reminder = datetime.now()

        logger.info("✅ Pixel Plant initialized successfully")

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

    def start(self):
        """Start the Pixel Plant companion"""
        self.running = True

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

        # Say goodbye
        self._say_goodbye()

        # Save learned patterns
        self.learner.save_patterns()

        # Cleanup hardware
        self.led.close()
        self.audio.close()
        self.camera.close()
        self.pir.close()

        logger.info("✅ Pixel Plant stopped")

    def _main_loop(self):
        """Main application loop"""
        frame_count = 0

        while self.running:
            try:
                frame_start = time.time()

                # Update motion from PIR
                if self.pir.is_motion_detected():
                    self.behavior.update_motion(True)

                # Analyze camera frame (every few frames to save processing)
                if frame_count % 5 == 0:
                    frame = self.camera.capture_frame()
                    if frame is not None:
                        activity_state = self.behavior.analyze_frame(frame)
                        self.learner.log_activity('state_update', activity_state.value)

                # Check if user is away
                if self.behavior.is_user_away(self.config.behavior.inactivity_sleep_minutes):
                    self._enter_sleep_mode()
                    time.sleep(5)  # Sleep longer in away mode
                    continue

                # Check health reminders
                self._check_health_reminders()

                # Update mood display
                self._update_mood_display()

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

        # Log
        self.learner.log_activity('reminder_sent', 'movement', {'urgency': urgency})
        logger.info(f"Movement reminder sent (urgency {urgency}): '{message}'")

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

        # Log
        self.learner.log_activity('reminder_sent', 'hydration', {'urgency': urgency})
        logger.info(f"Hydration reminder sent: '{message}'")

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

    def _enter_sleep_mode(self):
        """Enter sleep mode when user is away"""
        if self.mood.current_mood != Mood.SLEEPING:
            logger.info("User appears away, entering sleep mode")
            self.mood.sleep()

            # Show sleeping face
            pattern, palette = self.mood.get_visual_representation()
            self.led.show_pattern(pattern, palette)

    def _wake_from_sleep(self):
        """Wake up when user returns"""
        logger.info("User detected, waking up")
        self.mood.wake()

        greeting = self.messages.get_message(MessageType.GREETING)
        self.audio.speak(greeting)


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
