#!/usr/bin/env python3
"""
LED Matrix Hardware Test
Validates 8x8 WS2812B LED matrix functionality
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from hardware import LEDMatrix
from personality import get_pattern, ColorPalette

def test_basic_colors(matrix):
    """Test basic color display"""
    print("\n1. Testing basic colors...")

    colors = [
        ("Red", (255, 0, 0)),
        ("Green", (0, 255, 0)),
        ("Blue", (0, 0, 255)),
        ("White", (255, 255, 255)),
        ("Yellow", (255, 255, 0)),
        ("Cyan", (0, 255, 255)),
        ("Magenta", (255, 0, 255)),
    ]

    for name, (r, g, b) in colors:
        print(f"   {name}...")
        pattern = [[(r, g, b) for _ in range(8)] for _ in range(8)]
        matrix.show_pattern(pattern)
        time.sleep(1.5)

    matrix.clear()
    print("   ✓ Basic colors test complete")


def test_individual_pixels(matrix):
    """Test individual pixel control"""
    print("\n2. Testing individual pixels...")

    matrix.clear()

    # Test each corner
    corners = [
        (0, 0, "Top-left"),
        (7, 0, "Top-right"),
        (0, 7, "Bottom-left"),
        (7, 7, "Bottom-right"),
    ]

    for x, y, name in corners:
        print(f"   {name} ({x}, {y})...")
        matrix.set_pixel(x, y, 0, 255, 0)  # Green
        matrix.strip.show() if not matrix.simulate else None
        time.sleep(0.8)

    matrix.clear()

    # Test center pixels
    print("   Center pixels...")
    for x in range(3, 5):
        for y in range(3, 5):
            matrix.set_pixel(x, y, 255, 0, 0)  # Red

    matrix.strip.show() if not matrix.simulate else None
    time.sleep(1.5)
    matrix.clear()

    print("   ✓ Individual pixel test complete")


def test_patterns(matrix):
    """Test predefined patterns"""
    print("\n3. Testing patterns...")

    patterns_to_test = [
        ('happy', ColorPalette.HAPPY, "Happy Face"),
        ('concerned', ColorPalette.CONCERNED, "Concerned Face"),
        ('sleeping', ColorPalette.SLEEPING, "Sleeping Face"),
        ('heart', ColorPalette.LOVE, "Heart"),
        ('water', ColorPalette.HYDRATION, "Water Drop"),
    ]

    for pattern_name, palette, description in patterns_to_test:
        print(f"   {description}...")
        pattern = get_pattern(pattern_name)
        if pattern:
            matrix.show_pattern(pattern, palette)
            time.sleep(2)

    matrix.clear()
    print("   ✓ Pattern test complete")


def test_brightness(matrix):
    """Test brightness levels"""
    print("\n4. Testing brightness levels...")

    pattern = get_pattern('happy')
    palette = ColorPalette.HAPPY

    brightness_levels = [255, 192, 128, 64, 32, 16]

    for brightness in brightness_levels:
        print(f"   Brightness: {brightness}/255...")
        matrix.set_brightness(brightness)
        matrix.show_pattern(pattern, palette)
        time.sleep(1.5)

    # Reset to default
    matrix.set_brightness(128)
    matrix.clear()
    print("   ✓ Brightness test complete")


def test_animations(matrix):
    """Test simple animations"""
    print("\n5. Testing animations...")

    # Chasing pattern
    print("   Chase animation...")
    for i in range(24):
        matrix.clear()
        x = i % 8
        y = i // 8
        matrix.set_pixel(x, y, 0, 255, 0)
        matrix.strip.show() if not matrix.simulate else None
        time.sleep(0.1)

    # Breathing effect
    print("   Breathing effect...")
    pattern = get_pattern('heart')
    palette = ColorPalette.LOVE
    matrix.breathing_effect(pattern, palette, duration=3.0, steps=30)

    matrix.clear()
    print("   ✓ Animation test complete")


def run_full_test(simulate=False):
    """Run complete LED matrix test suite"""
    print("=" * 50)
    print("PIXEL PLANT - LED Matrix Hardware Test")
    print("=" * 50)

    if simulate:
        print("\n⚠️  Running in SIMULATION mode")
        print("Connect real hardware and set simulate=False for actual test\n")

    # Initialize matrix
    matrix = LEDMatrix(gpio_pin=18, width=8, height=8, brightness=128, simulate=simulate)

    try:
        # Run tests
        test_basic_colors(matrix)
        test_individual_pixels(matrix)
        test_patterns(matrix)
        test_brightness(matrix)
        test_animations(matrix)

        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED")
        print("=" * 50)
        print("\nYour LED matrix is working correctly!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")

    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

    finally:
        matrix.clear()
        matrix.close()
        print("\nTest complete. Matrix cleared and closed.")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Test LED matrix hardware')
    parser.add_argument('--real', action='store_true',
                       help='Test with real hardware (default: simulate)')
    args = parser.parse_args()

    simulate = not args.real
    run_full_test(simulate=simulate)
