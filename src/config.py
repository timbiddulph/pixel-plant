"""
Configuration Management
Loads and validates configuration from YAML file
"""

import os
import yaml
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List

logger = logging.getLogger(__name__)


@dataclass
class HardwareConfig:
    """Hardware pin assignments and settings"""
    led_gpio_pin: int
    led_width: int
    led_height: int
    led_brightness: int

    audio_bclk_pin: int
    audio_lrclk_pin: int
    audio_data_pin: int
    audio_volume: int

    camera_resolution: tuple[int, int]
    camera_framerate: int
    camera_rotation: int

    pir_gpio_pin: int
    pir_enabled: bool


@dataclass
class BehaviorConfig:
    """Behavioral monitoring thresholds"""
    sitting_threshold_minutes: int
    hydration_interval_minutes: int
    inactivity_sleep_minutes: int
    learning_enabled: bool
    pattern_window_days: int


@dataclass
class PersonalityConfig:
    """Personality and interaction settings"""
    caring_level: int
    voice_enabled: bool
    voice_rate: int
    voice_volume: float
    escalation_enabled: bool
    celebration_enabled: bool


@dataclass
class AnimationConfig:
    """LED animation preferences"""
    transition_style: str
    mood_update_seconds: int
    breathing_speed: float


@dataclass
class AIConfig:
    """AI/ML settings"""
    pose_detection_enabled: bool
    confidence_threshold: float
    model_path: str
    save_images: bool
    save_analytics_only: bool


@dataclass
class SystemConfig:
    """System-level settings"""
    log_level: str
    log_file: str
    data_directory: str
    auto_start: bool


@dataclass
class DebugConfig:
    """Development and debugging options"""
    simulate_hardware: bool
    console_visualization: bool
    performance_monitoring: bool


class Config:
    """Main configuration object"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Load configuration from YAML file

        Args:
            config_path: Path to config.yaml (defaults to config/config.yaml)
        """
        if config_path is None:
            # Default to config/config.yaml relative to project root
            project_root = Path(__file__).parent.parent
            config_path = project_root / 'config' / 'config.yaml'

        self.config_path = Path(config_path)
        self._raw_config = self._load_yaml()

        # Parse into structured config objects
        self.hardware = self._parse_hardware()
        self.behavior = self._parse_behavior()
        self.personality = self._parse_personality()
        self.animations = self._parse_animations()
        self.ai = self._parse_ai()
        self.system = self._parse_system()
        self.debug = self._parse_debug()

        # Validate configuration
        self._validation_errors = []
        self._validation_warnings = []
        self.validate()

        # Log validation results
        if self._validation_warnings:
            for warning in self._validation_warnings:
                logger.warning(f"Config warning: {warning}")

        if self._validation_errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(
                f"  - {error}" for error in self._validation_errors
            )
            raise ValueError(error_msg)

    def _load_yaml(self) -> dict:
        """Load and parse YAML configuration file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _parse_hardware(self) -> HardwareConfig:
        """Parse hardware configuration section"""
        hw = self._raw_config['hardware']
        return HardwareConfig(
            led_gpio_pin=hw['led_matrix']['gpio_pin'],
            led_width=hw['led_matrix']['width'],
            led_height=hw['led_matrix']['height'],
            led_brightness=hw['led_matrix']['brightness'],

            audio_bclk_pin=hw['audio']['i2s_pins']['bclk'],
            audio_lrclk_pin=hw['audio']['i2s_pins']['lrclk'],
            audio_data_pin=hw['audio']['i2s_pins']['data'],
            audio_volume=hw['audio']['volume'],

            camera_resolution=tuple(hw['camera']['resolution']),
            camera_framerate=hw['camera']['framerate'],
            camera_rotation=hw['camera']['rotation'],

            pir_gpio_pin=hw['pir_sensor']['gpio_pin'],
            pir_enabled=hw['pir_sensor']['enabled'],
        )

    def _parse_behavior(self) -> BehaviorConfig:
        """Parse behavior configuration section"""
        b = self._raw_config['behavior']
        return BehaviorConfig(
            sitting_threshold_minutes=b['sitting_threshold_minutes'],
            hydration_interval_minutes=b['hydration_interval_minutes'],
            inactivity_sleep_minutes=b['inactivity_sleep_minutes'],
            learning_enabled=b['learning_enabled'],
            pattern_window_days=b['pattern_window_days'],
        )

    def _parse_personality(self) -> PersonalityConfig:
        """Parse personality configuration section"""
        p = self._raw_config['personality']
        return PersonalityConfig(
            caring_level=p['caring_level'],
            voice_enabled=p['voice_enabled'],
            voice_rate=p['voice_rate'],
            voice_volume=p['voice_volume'],
            escalation_enabled=p['escalation_enabled'],
            celebration_enabled=p['celebration_enabled'],
        )

    def _parse_animations(self) -> AnimationConfig:
        """Parse animation configuration section"""
        a = self._raw_config['animations']
        return AnimationConfig(
            transition_style=a['transition_style'],
            mood_update_seconds=a['mood_update_seconds'],
            breathing_speed=a['breathing_speed'],
        )

    def _parse_ai(self) -> AIConfig:
        """Parse AI configuration section"""
        ai = self._raw_config['ai']

        # Resolve model path relative to project root
        model_path = ai['model_path']
        if not model_path.startswith('/'):
            project_root = Path(__file__).parent.parent
            model_path = str(project_root / model_path)

        return AIConfig(
            pose_detection_enabled=ai['pose_detection_enabled'],
            confidence_threshold=ai['confidence_threshold'],
            model_path=model_path,
            save_images=ai['save_images'],
            save_analytics_only=ai['save_analytics_only'],
        )

    def _parse_system(self) -> SystemConfig:
        """Parse system configuration section"""
        s = self._raw_config['system']

        # Ensure data directory exists
        data_dir = Path(s['data_directory']).expanduser()
        data_dir.mkdir(parents=True, exist_ok=True)

        return SystemConfig(
            log_level=s['log_level'],
            log_file=s['log_file'],
            data_directory=str(data_dir),
            auto_start=s['auto_start'],
        )

    def _parse_debug(self) -> DebugConfig:
        """Parse debug configuration section"""
        d = self._raw_config['debug']
        return DebugConfig(
            simulate_hardware=d['simulate_hardware'],
            console_visualization=d['console_visualization'],
            performance_monitoring=d['performance_monitoring'],
        )

    def validate(self):
        """Validate configuration values"""
        self._validate_hardware()
        self._validate_behavior()
        self._validate_personality()
        self._validate_animations()
        self._validate_ai()
        self._validate_gpio_conflicts()

    def _validate_hardware(self):
        """Validate hardware configuration"""
        # GPIO pins
        valid_gpio_pins = list(range(2, 28))  # BCM numbering

        if self.hardware.led_gpio_pin not in valid_gpio_pins:
            self._validation_errors.append(
                f"Invalid LED GPIO pin: {self.hardware.led_gpio_pin}. Must be 2-27."
            )

        if self.hardware.pir_gpio_pin not in valid_gpio_pins:
            self._validation_errors.append(
                f"Invalid PIR GPIO pin: {self.hardware.pir_gpio_pin}. Must be 2-27."
            )

        # LED settings
        if not (0 <= self.hardware.led_brightness <= 255):
            self._validation_errors.append(
                f"LED brightness must be 0-255, got {self.hardware.led_brightness}"
            )

        if self.hardware.led_width != 8 or self.hardware.led_height != 8:
            self._validation_warnings.append(
                f"LED matrix is {self.hardware.led_width}x{self.hardware.led_height}. "
                "Patterns are designed for 8x8."
            )

        # Audio settings
        if not (0 <= self.hardware.audio_volume <= 100):
            self._validation_errors.append(
                f"Audio volume must be 0-100, got {self.hardware.audio_volume}"
            )

        # Camera settings
        if self.hardware.camera_rotation not in [0, 90, 180, 270]:
            self._validation_errors.append(
                f"Camera rotation must be 0, 90, 180, or 270, got {self.hardware.camera_rotation}"
            )

        if self.hardware.camera_framerate < 1 or self.hardware.camera_framerate > 30:
            self._validation_warnings.append(
                f"Camera framerate {self.hardware.camera_framerate} may cause issues. "
                "Recommended: 10-25 FPS"
            )

    def _validate_behavior(self):
        """Validate behavior configuration"""
        if self.behavior.sitting_threshold_minutes < 1:
            self._validation_errors.append(
                "Sitting threshold must be at least 1 minute"
            )

        if self.behavior.hydration_interval_minutes < 1:
            self._validation_errors.append(
                "Hydration interval must be at least 1 minute"
            )

        if self.behavior.inactivity_sleep_minutes < 1:
            self._validation_errors.append(
                "Inactivity sleep must be at least 1 minute"
            )

        if self.behavior.pattern_window_days < 1 or self.behavior.pattern_window_days > 30:
            self._validation_warnings.append(
                f"Pattern window of {self.behavior.pattern_window_days} days may be extreme. "
                "Recommended: 3-14 days"
            )

    def _validate_personality(self):
        """Validate personality configuration"""
        if not (1 <= self.personality.caring_level <= 10):
            self._validation_errors.append(
                f"Caring level must be 1-10, got {self.personality.caring_level}"
            )

        if not (50 <= self.personality.voice_rate <= 300):
            self._validation_warnings.append(
                f"Voice rate {self.personality.voice_rate} WPM may sound unnatural. "
                "Recommended: 100-200 WPM"
            )

        if not (0.0 <= self.personality.voice_volume <= 1.0):
            self._validation_errors.append(
                f"Voice volume must be 0.0-1.0, got {self.personality.voice_volume}"
            )

    def _validate_animations(self):
        """Validate animation configuration"""
        valid_styles = ['wave', 'cascade', 'synchronized', 'breathing']

        if self.animations.transition_style not in valid_styles:
            self._validation_errors.append(
                f"Invalid transition style: '{self.animations.transition_style}'. "
                f"Must be one of: {', '.join(valid_styles)}"
            )

        if self.animations.mood_update_seconds < 1:
            self._validation_warnings.append(
                "Mood update interval < 1s may cause excessive LED updates"
            )

        if self.animations.breathing_speed < 0.5 or self.animations.breathing_speed > 10:
            self._validation_warnings.append(
                f"Breathing speed {self.animations.breathing_speed}s may look unnatural. "
                "Recommended: 1-5 seconds"
            )

    def _validate_ai(self):
        """Validate AI configuration"""
        if not (0.0 <= self.ai.confidence_threshold <= 1.0):
            self._validation_errors.append(
                f"AI confidence threshold must be 0.0-1.0, got {self.ai.confidence_threshold}"
            )

        if self.ai.pose_detection_enabled and not Path(self.ai.model_path).exists():
            self._validation_warnings.append(
                f"Pose detection model not found at: {self.ai.model_path}. "
                "Pose detection will be disabled."
            )

    def _validate_gpio_conflicts(self):
        """Check for GPIO pin conflicts"""
        gpio_usage = {}

        # Track GPIO usage
        pins = [
            (self.hardware.led_gpio_pin, "LED Matrix"),
            (self.hardware.pir_gpio_pin, "PIR Sensor"),
            (self.hardware.audio_bclk_pin, "Audio BCLK"),
            (self.hardware.audio_lrclk_pin, "Audio LRCLK"),
            (self.hardware.audio_data_pin, "Audio Data"),
        ]

        for pin, component in pins:
            if pin in gpio_usage:
                self._validation_errors.append(
                    f"GPIO pin conflict: GPIO {pin} used by both "
                    f"'{gpio_usage[pin]}' and '{component}'"
                )
            else:
                gpio_usage[pin] = component

        # Warn about reserved pins
        reserved_pins = {
            0: "I2C ID EEPROM",
            1: "I2C ID EEPROM",
            14: "UART TX",
            15: "UART RX",
        }

        for pin, component in pins:
            if pin in reserved_pins:
                self._validation_warnings.append(
                    f"GPIO {pin} ({component}) conflicts with {reserved_pins[pin]}"
                )

    def get_validation_report(self) -> str:
        """
        Get formatted validation report

        Returns:
            Multi-line string with validation results
        """
        report = ["Configuration Validation Report", "=" * 40]

        if not self._validation_errors and not self._validation_warnings:
            report.append("✅ All validation checks passed!")
        else:
            if self._validation_errors:
                report.append(f"\n❌ Errors ({len(self._validation_errors)}):")
                for error in self._validation_errors:
                    report.append(f"  - {error}")

            if self._validation_warnings:
                report.append(f"\n⚠️  Warnings ({len(self._validation_warnings)}):")
                for warning in self._validation_warnings:
                    report.append(f"  - {warning}")

        return "\n".join(report)

    def __repr__(self) -> str:
        """String representation for debugging"""
        return (
            f"Config(\n"
            f"  hardware={self.hardware},\n"
            f"  behavior={self.behavior},\n"
            f"  personality={self.personality},\n"
            f"  animations={self.animations},\n"
            f"  ai={self.ai},\n"
            f"  system={self.system},\n"
            f"  debug={self.debug}\n"
            f")"
        )


# Global config instance (loaded on import)
_config: Optional[Config] = None


def load_config(config_path: Optional[str] = None) -> Config:
    """
    Load or reload configuration

    Args:
        config_path: Optional path to config file

    Returns:
        Config object
    """
    global _config
    _config = Config(config_path)
    return _config


def get_config() -> Config:
    """
    Get current configuration (loads default if not yet loaded)

    Returns:
        Config object
    """
    global _config
    if _config is None:
        _config = Config()
    return _config


if __name__ == '__main__':
    """Test configuration loading"""
    import logging
    logging.basicConfig(level=logging.INFO)

    try:
        config = load_config()
        print(config)
        print("\n" + config.get_validation_report())
        print("\n✅ Configuration loaded successfully!")
    except ValueError as e:
        print(f"\n❌ Configuration validation failed:\n{e}")
        exit(1)
