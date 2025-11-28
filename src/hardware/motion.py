"""
Motion Sensor Hardware Abstraction
PIR sensor for presence detection
"""

import logging
import time
from typing import Optional, Callable

logger = logging.getLogger(__name__)


class MotionSensor:
    """PIR motion sensor for presence detection"""

    def __init__(self, gpio_pin: int, enabled: bool = True,
                 simulate: bool = False):
        """
        Initialize motion sensor

        Args:
            gpio_pin: GPIO pin number (BCM)
            enabled: Enable motion detection
            simulate: If True, simulate random motion events
        """
        self.gpio_pin = gpio_pin
        self.enabled = enabled
        self.simulate = simulate
        self.gpio = None
        self.callback = None
        self._simulate_counter = 0

        if not simulate and enabled:
            try:
                import RPi.GPIO as GPIO
                self.GPIO = GPIO

                # Setup GPIO
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(gpio_pin, GPIO.IN)

                logger.info(f"Motion sensor initialized on GPIO {gpio_pin}")

            except ImportError:
                logger.warning("RPi.GPIO not available, falling back to simulation")
                self.simulate = True
            except Exception as e:
                logger.error(f"Motion sensor initialization failed: {e}")
                self.simulate = True
        else:
            logger.info("Motion sensor running in simulation mode")

    def is_motion_detected(self) -> bool:
        """
        Check if motion is currently detected

        Returns:
            True if motion detected, False otherwise
        """
        if not self.enabled:
            return False

        if self.simulate:
            # Simulate random motion every ~10 checks
            self._simulate_counter += 1
            if self._simulate_counter % 10 == 0:
                logger.debug("Simulated motion detected")
                return True
            return False

        try:
            return bool(self.GPIO.input(self.gpio_pin))
        except Exception as e:
            logger.error(f"Motion detection error: {e}")
            return False

    def add_event_callback(self, callback: Callable, edge: str = 'rising'):
        """
        Add callback for motion events

        Args:
            callback: Function to call when motion detected
            edge: 'rising', 'falling', or 'both'
        """
        if self.simulate:
            logger.info("Motion event callbacks not supported in simulation mode")
            return

        self.callback = callback

        try:
            edge_map = {
                'rising': self.GPIO.RISING,
                'falling': self.GPIO.FALLING,
                'both': self.GPIO.BOTH,
            }

            self.GPIO.add_event_detect(
                self.gpio_pin,
                edge_map.get(edge, self.GPIO.RISING),
                callback=lambda channel: callback()
            )

            logger.info(f"Motion event callback registered ({edge} edge)")

        except Exception as e:
            logger.error(f"Failed to add event callback: {e}")

    def remove_event_callback(self):
        """Remove motion event callback"""
        if self.simulate:
            return

        try:
            self.GPIO.remove_event_detect(self.gpio_pin)
            self.callback = None
            logger.info("Motion event callback removed")
        except Exception as e:
            logger.error(f"Failed to remove event callback: {e}")

    def wait_for_motion(self, timeout: Optional[float] = None) -> bool:
        """
        Block until motion is detected

        Args:
            timeout: Maximum time to wait in seconds (None = infinite)

        Returns:
            True if motion detected, False if timeout
        """
        if not self.enabled:
            return False

        if self.simulate:
            # Simulate motion after short delay
            wait_time = min(timeout or 2.0, 2.0)
            time.sleep(wait_time)
            logger.debug("Simulated motion detected (wait)")
            return True

        try:
            start_time = time.time()

            while True:
                if self.is_motion_detected():
                    return True

                if timeout is not None:
                    elapsed = time.time() - start_time
                    if elapsed >= timeout:
                        return False

                time.sleep(0.1)  # Check every 100ms

        except Exception as e:
            logger.error(f"Error waiting for motion: {e}")
            return False

    def enable(self, enabled: bool):
        """Enable or disable motion detection"""
        self.enabled = enabled

    def close(self):
        """Clean up GPIO resources"""
        if not self.simulate and self.GPIO:
            try:
                self.remove_event_callback()
                self.GPIO.cleanup(self.gpio_pin)
            except:
                pass
        logger.info("Motion sensor closed")


if __name__ == '__main__':
    """Test motion sensor"""
    logging.basicConfig(level=logging.INFO)

    sensor = MotionSensor(gpio_pin=17, simulate=True)

    # Test basic detection
    print("Testing motion detection...")
    for i in range(20):
        if sensor.is_motion_detected():
            print(f"  [{i}] Motion detected!")
        time.sleep(0.2)

    # Test wait
    print("\nWaiting for motion (2s timeout)...")
    detected = sensor.wait_for_motion(timeout=2.0)
    print(f"  Result: {'Motion!' if detected else 'Timeout'}")

    sensor.close()
