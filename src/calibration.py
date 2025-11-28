"""
Interactive Calibration System
Guides users through personalized setup and calibration
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class CalibrationData:
    """Stores calibration data"""

    def __init__(self, data_directory: str):
        """
        Initialize calibration data

        Args:
            data_directory: Directory to store calibration
        """
        self.data_directory = Path(data_directory)
        self.calibration_file = self.data_directory / 'calibration.json'
        self.data = self._load()

    def _load(self) -> Dict:
        """Load existing calibration data"""
        if not self.calibration_file.exists():
            return self._get_defaults()

        try:
            with open(self.calibration_file, 'r') as f:
                data = json.load(f)
                logger.info("Loaded existing calibration data")
                return data
        except Exception as e:
            logger.error(f"Failed to load calibration: {e}")
            return self._get_defaults()

    def _get_defaults(self) -> Dict:
        """Get default calibration values"""
        return {
            'calibrated': False,
            'calibration_date': None,
            'pose': {
                'sitting_hip_y_mean': 0.6,
                'standing_hip_y_mean': 0.4,
                'forward_lean_threshold': 20.0,
            },
            'preferences': {
                'caring_level': 5,
                'voice_enabled': True,
                'reminder_frequency': 'normal',
            },
            'camera': {
                'rotation': 0,
                'brightness_adjustment': 0,
            },
            'led': {
                'brightness': 128,
            },
        }

    def save(self):
        """Save calibration data"""
        try:
            self.data['last_updated'] = datetime.now().isoformat()

            with open(self.calibration_file, 'w') as f:
                json.dump(self.data, f, indent=2)

            logger.info("Calibration data saved")

        except Exception as e:
            logger.error(f"Failed to save calibration: {e}")

    def mark_calibrated(self):
        """Mark calibration as complete"""
        self.data['calibrated'] = True
        self.data['calibration_date'] = datetime.now().isoformat()
        self.save()

    def is_calibrated(self) -> bool:
        """Check if system has been calibrated"""
        return self.data.get('calibrated', False)

    def update_pose_calibration(self, calibration: Dict):
        """Update pose calibration data"""
        self.data['pose'].update(calibration)
        self.save()

    def update_preferences(self, preferences: Dict):
        """Update user preferences"""
        self.data['preferences'].update(preferences)
        self.save()

    def get_pose_calibration(self) -> Dict:
        """Get pose calibration data"""
        return self.data.get('pose', {})

    def get_preferences(self) -> Dict:
        """Get user preferences"""
        return self.data.get('preferences', {})


class CalibrationWizard:
    """Interactive calibration wizard"""

    def __init__(self, calibration_data: CalibrationData,
                 camera_system, led_matrix, audio_system, pose_detector):
        """
        Initialize calibration wizard

        Args:
            calibration_data: CalibrationData instance
            camera_system: CameraSystem instance
            led_matrix: LEDMatrix instance
            audio_system: AudioSystem instance
            pose_detector: PoseDetector instance
        """
        self.calibration = calibration_data
        self.camera = camera_system
        self.led = led_matrix
        self.audio = audio_system
        self.pose = pose_detector

    def run_full_calibration(self, interactive: bool = True) -> bool:
        """
        Run complete calibration process

        Args:
            interactive: If True, prompt user for input

        Returns:
            True if calibration succeeded
        """
        logger.info("Starting calibration wizard...")

        try:
            if interactive:
                self._welcome()

            # Step 1: Camera calibration
            self._calibrate_camera(interactive)

            # Step 2: LED brightness
            self._calibrate_led_brightness(interactive)

            # Step 3: Audio volume
            self._calibrate_audio(interactive)

            # Step 4: Pose detection
            self._calibrate_pose(interactive)

            # Step 5: User preferences
            self._calibrate_preferences(interactive)

            # Mark as complete
            self.calibration.mark_calibrated()

            if interactive:
                self._completion_message()

            logger.info("Calibration completed successfully")
            return True

        except KeyboardInterrupt:
            logger.info("Calibration interrupted by user")
            return False

        except Exception as e:
            logger.error(f"Calibration failed: {e}", exc_info=True)
            return False

    def _welcome(self):
        """Welcome message"""
        print("\n" + "=" * 60)
        print("  Welcome to Pixel Plant Setup! 🌿")
        print("=" * 60)
        print("\nLet's calibrate your AI companion for the best experience.")
        print("This will take about 5 minutes.\n")

        self.audio.speak("Hello! Welcome to Pixel Plant setup!")
        time.sleep(1)

        input("Press Enter to begin...")
        print()

    def _calibrate_camera(self, interactive: bool):
        """Calibrate camera settings"""
        print("\n" + "-" * 60)
        print("STEP 1: Camera Calibration")
        print("-" * 60)

        if not interactive:
            return

        print("\nChecking camera orientation...")
        self.audio.speak("Let me check the camera")

        self.camera.start()
        time.sleep(1)

        frame = self.camera.capture_frame()

        if frame is None:
            print("⚠️  Could not capture frame. Using default settings.")
            return

        print("✓ Camera working")

        # Check if image is too dark or bright
        import numpy as np
        brightness = np.mean(frame)

        print(f"\nImage brightness: {brightness:.1f}/255")

        if brightness < 50:
            print("⚠️  Image is quite dark. Consider:")
            print("   - Adding more lighting")
            print("   - Adjusting camera position")
        elif brightness > 200:
            print("⚠️  Image is very bright. Consider:")
            print("   - Reducing lighting")
            print("   - Adjusting camera angle")
        else:
            print("✓ Image brightness looks good")

        # Check orientation
        print("\nPosition yourself in front of the camera.")
        input("Press Enter when ready...")

        frames_for_orientation = []
        for _ in range(5):
            frame = self.camera.capture_frame()
            if frame is not None:
                frames_for_orientation.append(frame)
            time.sleep(0.2)

        # TODO: Could analyze if person is in frame and oriented correctly
        print("✓ Camera calibration complete")

        self.calibration.data['camera']['calibrated'] = True
        self.calibration.save()

    def _calibrate_led_brightness(self, interactive: bool):
        """Calibrate LED brightness"""
        print("\n" + "-" * 60)
        print("STEP 2: LED Brightness")
        print("-" * 60)

        if not interactive:
            self.led.set_brightness(128)
            return

        self.audio.speak("Let's set the LED brightness")

        from personality import get_pattern, ColorPalette

        pattern = get_pattern('happy')
        palette = ColorPalette.HAPPY

        print("\nTesting different brightness levels...")

        brightness_levels = [64, 128, 192, 255]

        for brightness in brightness_levels:
            self.led.set_brightness(brightness)
            self.led.show_pattern(pattern, palette)
            print(f"\nBrightness: {brightness}/255")
            time.sleep(1.5)

        # Get user preference
        print("\nWhat brightness level looked best?")
        print("1. Dim (64)")
        print("2. Medium (128) - Recommended")
        print("3. Bright (192)")
        print("4. Very Bright (255)")

        choice = input("\nEnter choice (1-4) [2]: ").strip() or "2"

        brightness_map = {'1': 64, '2': 128, '3': 192, '4': 255}
        selected_brightness = brightness_map.get(choice, 128)

        self.led.set_brightness(selected_brightness)
        self.led.show_pattern(pattern, palette)

        print(f"\n✓ LED brightness set to {selected_brightness}")

        self.calibration.data['led']['brightness'] = selected_brightness
        self.calibration.save()

    def _calibrate_audio(self, interactive: bool):
        """Calibrate audio volume"""
        print("\n" + "-" * 60)
        print("STEP 3: Audio Volume")
        print("-" * 60)

        if not interactive:
            self.audio.set_volume(70)
            return

        print("\nTesting audio volume...")

        test_phrase = "This is a test of the audio volume"

        volumes = [50, 70, 90]

        for volume in volumes:
            self.audio.set_volume(volume)
            print(f"\nVolume: {volume}%")
            self.audio.speak(test_phrase)
            time.sleep(1)

        print("\nWhat volume level was most comfortable?")
        print("1. Quiet (50%)")
        print("2. Medium (70%) - Recommended")
        print("3. Loud (90%)")

        choice = input("\nEnter choice (1-3) [2]: ").strip() or "2"

        volume_map = {'1': 50, '2': 70, '3': 90}
        selected_volume = volume_map.get(choice, 70)

        self.audio.set_volume(selected_volume)
        self.audio.speak("Perfect! I'll use this volume.")

        print(f"\n✓ Audio volume set to {selected_volume}%")

        self.calibration.data['preferences']['audio_volume'] = selected_volume
        self.calibration.save()

    def _calibrate_pose(self, interactive: bool):
        """Calibrate pose detection"""
        print("\n" + "-" * 60)
        print("STEP 4: Posture Calibration")
        print("-" * 60)

        if not interactive or not self.pose:
            print("Skipping pose calibration (using defaults)")
            return

        self.audio.speak("Let's calibrate your sitting and standing positions")

        print("\nThis helps me recognize when you're sitting or standing.")
        print("I'll capture a few samples of each position.\n")

        # Collect sitting samples
        sitting_frames = []

        print("Please SIT in your normal working position.")
        input("Press Enter when ready...")

        print("Capturing sitting position... (stay still for 3 seconds)")
        self.audio.speak("Capturing sitting position")

        for i in range(10):
            frame = self.camera.capture_frame()
            if frame is not None:
                sitting_frames.append(frame)
            time.sleep(0.3)

        print(f"✓ Captured {len(sitting_frames)} sitting samples")

        # Collect standing samples
        standing_frames = []

        print("\nNow please STAND UP.")
        input("Press Enter when standing...")

        print("Capturing standing position... (stay still for 3 seconds)")
        self.audio.speak("Capturing standing position")

        for i in range(10):
            frame = self.camera.capture_frame()
            if frame is not None:
                standing_frames.append(frame)
            time.sleep(0.3)

        print(f"✓ Captured {len(standing_frames)} standing samples")

        # Analyze calibration
        all_frames = sitting_frames + standing_frames
        pose_calibration = self.pose.calibrate(all_frames)

        self.calibration.update_pose_calibration(pose_calibration)

        print("\n✓ Posture calibration complete")
        self.audio.speak("Great! Calibration complete")

    def _calibrate_preferences(self, interactive: bool):
        """Calibrate user preferences"""
        print("\n" + "-" * 60)
        print("STEP 5: Caring Preferences")
        print("-" * 60)

        if not interactive:
            return

        self.audio.speak("Finally, let's set your preferences")

        print("\nHow caring should I be?")
        print("This affects how often I check on you and remind you.\n")
        print("1. Very gentle (level 2)")
        print("2. Gentle (level 4)")
        print("3. Balanced (level 5) - Recommended")
        print("4. Attentive (level 7)")
        print("5. Very attentive (level 9)")

        choice = input("\nEnter choice (1-5) [3]: ").strip() or "3"

        caring_map = {'1': 2, '2': 4, '3': 5, '4': 7, '5': 9}
        caring_level = caring_map.get(choice, 5)

        preferences = {
            'caring_level': caring_level,
            'voice_enabled': True,
        }

        self.calibration.update_preferences(preferences)

        print(f"\n✓ Caring level set to {caring_level}/10")

    def _completion_message(self):
        """Completion message"""
        print("\n" + "=" * 60)
        print("  ✅ Calibration Complete!")
        print("=" * 60)
        print("\nYour Pixel Plant is now personalized for you!")
        print("\nYou can recalibrate anytime by running:")
        print("  python -m calibration\n")

        self.audio.speak("Calibration complete! I'm ready to care for you!")

        from personality import get_pattern, ColorPalette
        pattern = get_pattern('very_happy')
        palette = ColorPalette.CELEBRATING
        self.led.show_pattern(pattern, palette)

        time.sleep(2)


def run_calibration_wizard(config):
    """
    Run calibration wizard with hardware

    Args:
        config: Config object
    """
    from hardware import LEDMatrix, AudioSystem, CameraSystem
    from ai import PoseDetector

    # Initialize hardware
    led = LEDMatrix(
        gpio_pin=config.hardware.led_gpio_pin,
        brightness=128,
        simulate=config.debug.simulate_hardware
    )

    audio = AudioSystem(
        volume=70,
        simulate=config.debug.simulate_hardware
    )

    camera = CameraSystem(
        resolution=config.hardware.camera_resolution,
        framerate=config.hardware.camera_framerate,
        simulate=config.debug.simulate_hardware
    )

    pose = PoseDetector(
        confidence_threshold=config.ai.confidence_threshold,
        simulate=config.debug.simulate_hardware
    )

    # Create calibration data
    calibration_data = CalibrationData(config.system.data_directory)

    # Create wizard
    wizard = CalibrationWizard(calibration_data, camera, led, audio, pose)

    # Run calibration
    try:
        success = wizard.run_full_calibration(interactive=True)

        if success:
            print("\n✅ Setup complete! Starting Pixel Plant...\n")
            return calibration_data
        else:
            print("\n⚠️  Setup was not completed.")
            return None

    finally:
        led.close()
        audio.close()
        camera.close()
        pose.close()


if __name__ == '__main__':
    """Run calibration wizard standalone"""
    import sys
    from pathlib import Path

    # Add src to path
    sys.path.insert(0, str(Path(__file__).parent))

    import logging
    logging.basicConfig(level=logging.INFO)

    from config import get_config

    print("Loading configuration...")
    config = get_config()

    run_calibration_wizard(config)
