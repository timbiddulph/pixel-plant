"""
LED Matrix Hardware Abstraction
Controls 8x8 WS2812B RGB LED matrix for visual expressions
"""

import time
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class LEDMatrix:
    """Controls WS2812B 8x8 RGB LED matrix"""

    def __init__(self, gpio_pin: int, width: int = 8, height: int = 8,
                 brightness: int = 128, simulate: bool = False):
        """
        Initialize LED matrix

        Args:
            gpio_pin: GPIO pin number (BCM)
            width: Matrix width in pixels
            height: Matrix height in pixels
            brightness: Global brightness (0-255)
            simulate: If True, print to console instead of real hardware
        """
        self.gpio_pin = gpio_pin
        self.width = width
        self.height = height
        self.brightness = brightness
        self.simulate = simulate
        self.current_pattern = None

        if not simulate:
            try:
                from rpi_ws281x import PixelStrip, Color
                self.PixelStrip = PixelStrip
                self.Color = Color

                # LED strip configuration
                LED_COUNT = width * height  # 64 LEDs
                LED_PIN = gpio_pin
                LED_FREQ_HZ = 800000  # LED signal frequency (Hz)
                LED_DMA = 10  # DMA channel
                LED_BRIGHTNESS = brightness
                LED_INVERT = False
                LED_CHANNEL = 0

                self.strip = PixelStrip(
                    LED_COUNT, LED_PIN, LED_FREQ_HZ,
                    LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
                )
                self.strip.begin()
                logger.info(f"LED Matrix initialized on GPIO {gpio_pin}")

            except ImportError:
                logger.warning("rpi_ws281x not available, falling back to simulation")
                self.simulate = True
        else:
            logger.info("LED Matrix running in simulation mode")

    def clear(self):
        """Turn off all LEDs"""
        if self.simulate:
            print("\n[LED] Matrix cleared")
            return

        for i in range(self.width * self.height):
            self.strip.setPixelColor(i, self.Color(0, 0, 0))
        self.strip.show()

    def set_pixel(self, x: int, y: int, r: int, g: int, b: int):
        """
        Set individual pixel color

        Args:
            x: X coordinate (0-7)
            y: Y coordinate (0-7)
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return

        # Convert 2D coordinates to 1D strip index
        # Assuming zigzag wiring pattern (common for matrices)
        if y % 2 == 0:
            # Even rows go left to right
            index = y * self.width + x
        else:
            # Odd rows go right to left
            index = y * self.width + (self.width - 1 - x)

        if self.simulate:
            return  # Skip individual pixel updates in simulation

        self.strip.setPixelColor(index, self.Color(r, g, b))

    def show_pattern(self, pattern: List[List[tuple]], palette: Optional[dict] = None):
        """
        Display an 8x8 pattern on the matrix

        Args:
            pattern: 8x8 list of RGB tuples or integers (if palette provided)
            palette: Optional color palette mapping integers to RGB tuples
        """
        self.current_pattern = pattern

        for y in range(self.height):
            for x in range(self.width):
                pixel = pattern[y][x]

                # Apply palette if provided and pixel is an integer
                if palette is not None and isinstance(pixel, int):
                    r, g, b = palette.get(pixel, (0, 0, 0))
                elif isinstance(pixel, tuple) and len(pixel) == 3:
                    r, g, b = pixel
                else:
                    r, g, b = 0, 0, 0

                self.set_pixel(x, y, r, g, b)

        if self.simulate:
            self._visualize_console(pattern, palette)
        else:
            self.strip.show()

    def _visualize_console(self, pattern: List[List], palette: Optional[dict] = None):
        """Print pattern to console for debugging"""
        print("\n" + "=" * 20)
        chars = {0: ' ', 1: '█', 2: '▓', 3: '░'}

        for row in pattern:
            line = ""
            for pixel in row:
                if isinstance(pixel, int):
                    line += chars.get(pixel, '?')
                elif isinstance(pixel, tuple):
                    # Show intensity based on brightness
                    brightness = sum(pixel)
                    if brightness == 0:
                        line += ' '
                    elif brightness < 50:
                        line += '░'
                    elif brightness < 100:
                        line += '▓'
                    else:
                        line += '█'
                else:
                    line += '?'
            print(line)
        print("=" * 20)

    def breathing_effect(self, base_pattern: List[List], palette: dict,
                        duration: float = 2.0, steps: int = 30):
        """
        Apply breathing (pulsing) effect to current pattern

        Args:
            base_pattern: Pattern to pulse
            palette: Color palette
            duration: Full breath cycle duration (seconds)
            steps: Number of brightness steps
        """
        import math

        for step in range(steps):
            # Sine wave for smooth breathing
            phase = (step / steps) * 2 * math.pi
            brightness_factor = (math.sin(phase) + 1) / 2  # 0.0 to 1.0

            # Scale palette colors
            scaled_palette = {}
            for key, (r, g, b) in palette.items():
                scaled_palette[key] = (
                    int(r * brightness_factor),
                    int(g * brightness_factor),
                    int(b * brightness_factor)
                )

            self.show_pattern(base_pattern, scaled_palette)
            time.sleep(duration / steps)

    def set_brightness(self, brightness: int):
        """
        Set global brightness

        Args:
            brightness: 0-255
        """
        self.brightness = max(0, min(255, brightness))

        if not self.simulate:
            self.strip.setBrightness(self.brightness)
            self.strip.show()

    def close(self):
        """Clean up resources"""
        self.clear()
        logger.info("LED Matrix closed")


if __name__ == '__main__':
    """Test LED matrix with simulation"""
    logging.basicConfig(level=logging.INFO)

    # Test pattern
    test_pattern = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 2, 0, 0, 2, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 3, 3, 3, 3, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ]

    palette = {
        0: (0, 0, 0),
        1: (0, 50, 0),
        2: (0, 30, 0),
        3: (0, 80, 20),
    }

    matrix = LEDMatrix(gpio_pin=18, simulate=True)
    matrix.show_pattern(test_pattern, palette)
    time.sleep(2)
    matrix.clear()
    matrix.close()
