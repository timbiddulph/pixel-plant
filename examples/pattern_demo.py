#!/usr/bin/env python3
"""
Pixel Plant Pattern Demo
Demonstrates all available 8x8 pixel art patterns on the LED matrix

Usage:
    # Display all patterns sequentially
    sudo python pattern_demo.py

    # Display specific pattern
    sudo python pattern_demo.py --pattern happy

    # Console visualization only (no hardware required)
    python pattern_demo.py --console

Author: Pixel Plant Project
"""

import sys
import time
import argparse
import os

# Add src to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
src_dir = os.path.join(project_root, 'src')
sys.path.insert(0, src_dir)

try:
    from rpi_ws281x import PixelStrip, Color
    HAS_HARDWARE = True
except ImportError:
    print("Warning: rpi_ws281x not available. Running in console mode only.")
    HAS_HARDWARE = False

from personality.pixel_art import (
    EXPRESSIONS, ICONS, ColorPalette,
    get_colored_pattern, visualize_pattern
)
from personality.animations import PixelAnimator

# LED matrix configuration
LED_COUNT = 64        # 8x8 = 64 LEDs
LED_PIN = 18          # GPIO pin
LED_FREQ_HZ = 800000  # LED signal frequency
LED_DMA = 10          # DMA channel
LED_BRIGHTNESS = 80   # Brightness (0-255)
LED_INVERT = False
LED_CHANNEL = 0


def xy_to_index(x, y, width=8):
    """
    Convert (x, y) coordinates to LED index.
    Assumes serpentine/zigzag layout.
    """
    if y % 2 == 0:
        return y * width + x
    else:
        return y * width + (width - 1 - x)


def display_pattern_on_matrix(strip, pattern, palette):
    """
    Display a colored pattern on the LED matrix.

    Args:
        strip: PixelStrip object
        pattern: 8x8 pattern list
        palette: ColorPalette dictionary
    """
    colored = get_colored_pattern(pattern, palette)

    for y in range(8):
        for x in range(8):
            r, g, b = colored[y][x]
            idx = xy_to_index(x, y)
            # Note: WS2812B uses GRB order, not RGB
            strip.setPixelColor(idx, Color(g, r, b))

    strip.show()


def clear_matrix(strip):
    """Turn off all LEDs."""
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()


def breathing_effect(strip, pattern, palette, duration=3.0, steps=30):
    """
    Display pattern with breathing brightness effect.

    Args:
        strip: PixelStrip object
        pattern: 8x8 pattern
        palette: Color palette
        duration: Total duration in seconds
        steps: Number of brightness steps
    """
    import math

    for step in range(steps):
        # Calculate brightness using sine wave (0 to 1)
        brightness = (math.sin(2 * math.pi * step / steps) + 1) / 2

        # Create scaled palette
        scaled_palette = {}
        for key, (r, g, b) in palette.items():
            scaled_palette[key] = (
                int(r * brightness),
                int(g * brightness),
                int(b * brightness)
            )

        display_pattern_on_matrix(strip, pattern, scaled_palette)
        time.sleep(duration / steps)


def console_demo(animated=False, animation_style='cascade'):
    """
    Run console-only demo (no hardware required).

    Args:
        animated: If True, show rise/fall animations
        animation_style: 'cascade', 'wave', or 'synchronized'
    """
    if not animated:
        # Static display
        print("\n" + "=" * 50)
        print("PIXEL PLANT PATTERN LIBRARY - CONSOLE DEMO")
        print("=" * 50)

        print("\n📊 EMOTIONAL EXPRESSIONS")
        print("-" * 50)
        for name, pattern in EXPRESSIONS.items():
            print(f"\n{name.upper().replace('_', ' ')}:")
            visualize_pattern(pattern)

        print("\n\n🎨 ICONS & SYMBOLS")
        print("-" * 50)
        for name, pattern in ICONS.items():
            print(f"\n{name.upper()}:")
            visualize_pattern(pattern)

        print("\n" + "=" * 50)
        print("Legend: █ = primary, ▓ = secondary, ░ = accent,   = off")
        print("=" * 50)
    else:
        # Animated display
        print("\n" + "=" * 50)
        print(f"PIXEL PLANT ANIMATED DEMO - {animation_style.upper()}")
        print("=" * 50)
        print("\n✨ Watch pixels rise and fall between patterns!")
        print("Press Ctrl+C to stop\n")
        time.sleep(2)

        animator = PixelAnimator()

        # Select a few representative patterns
        demo_patterns = [
            ('Happy', EXPRESSIONS['happy']),
            ('Heart', ICONS['heart']),
            ('Water Drop', ICONS['water']),
            ('Concerned', EXPRESSIONS['concerned']),
            ('Stretching', ICONS['stretching']),
            ('Very Happy', EXPRESSIONS['very_happy']),
        ]

        current_pattern = None

        try:
            for name, pattern in demo_patterns:
                # Clear screen and show title
                print('\033[2J\033[H', end='')
                print(f"🌿 {name}")
                print("-" * 50)

                # Animate transition
                for frame in animator.transition(
                    current_pattern,
                    pattern,
                    style=animation_style,
                    fall_steps=8,
                    rise_steps=10
                ):
                    # Move cursor up to redraw
                    if current_pattern is not None:
                        print('\033[10A', end='')

                    chars = {0: ' ', 1: '█', 2: '▓', 3: '░'}
                    for row in frame:
                        print(''.join(chars.get(p, '?') for p in row))
                    print()

                current_pattern = pattern
                time.sleep(1.5)  # Hold final state

            print("\n✅ Animation demo complete!")
            print("=" * 50)

        except KeyboardInterrupt:
            print("\n\n⚠️  Demo interrupted")
            print("=" * 50)


def hardware_demo(pattern_name=None):
    """Run hardware demo on LED matrix."""
    if not HAS_HARDWARE:
        print("Error: rpi_ws281x library not available.")
        print("Install with: pip install rpi_ws281x")
        return

    # Create LED strip object
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                       LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    print("\n🌿 Pixel Plant Pattern Demo")
    print("=" * 50)

    try:
        if pattern_name:
            # Display specific pattern
            demo_sequence = [(pattern_name, None)]
        else:
            # Display all patterns in sequence
            demo_sequence = [
                # Expressions with moods
                ('happy', (ColorPalette.HAPPY, "breathing")),
                ('very_happy', (ColorPalette.CELEBRATING, "static")),
                ('thinking', (ColorPalette.NEUTRAL, "static")),
                ('concerned', (ColorPalette.CONCERNED, "breathing")),
                ('worried', (ColorPalette.WORRIED, "breathing")),
                ('sleeping', (ColorPalette.SLEEPING, "breathing")),
                ('sleeping_zzz', (ColorPalette.SLEEPING, "static")),

                # Icons
                ('heart', (ColorPalette.LOVE, "breathing")),
                ('water', (ColorPalette.HYDRATION, "static")),
                ('check', (ColorPalette.SUCCESS, "static")),
                ('walking', (ColorPalette.HAPPY, "static")),
                ('stretching', (ColorPalette.HAPPY, "static")),
                ('exclamation', (ColorPalette.ALERT, "static")),
                ('sparkle', (ColorPalette.CELEBRATING, "static")),
            ]

        for item in demo_sequence:
            if len(item) == 2:
                name, config = item
            else:
                name = item
                config = None

            # Get pattern
            all_patterns = {**EXPRESSIONS, **ICONS}
            if name not in all_patterns:
                print(f"❌ Pattern '{name}' not found")
                continue

            pattern = all_patterns[name]

            # Determine palette and effect
            if config:
                palette, effect = config
            else:
                # Auto-select palette based on pattern type
                if name in ['happy', 'very_happy', 'walking', 'stretching']:
                    palette = ColorPalette.HAPPY
                elif name == 'concerned':
                    palette = ColorPalette.CONCERNED
                elif name == 'worried':
                    palette = ColorPalette.WORRIED
                elif name in ['sleeping', 'sleeping_zzz']:
                    palette = ColorPalette.SLEEPING
                elif name == 'heart':
                    palette = ColorPalette.LOVE
                elif name == 'water':
                    palette = ColorPalette.HYDRATION
                elif name in ['check', 'sparkle']:
                    palette = ColorPalette.SUCCESS
                elif name == 'exclamation':
                    palette = ColorPalette.ALERT
                else:
                    palette = ColorPalette.NEUTRAL
                effect = "breathing"

            print(f"\n✨ Displaying: {name.upper().replace('_', ' ')}")

            if effect == "breathing":
                breathing_effect(strip, pattern, palette, duration=3.0)
            else:
                display_pattern_on_matrix(strip, pattern, palette)
                time.sleep(2.0)

            # Brief pause between patterns
            clear_matrix(strip)
            time.sleep(0.5)

        print("\n✅ Demo complete!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")

    finally:
        # Clean up: turn off all LEDs
        clear_matrix(strip)
        print("🔌 Matrix cleared\n")


def main():
    parser = argparse.ArgumentParser(
        description='Pixel Plant 8x8 LED Matrix Pattern Demo'
    )
    parser.add_argument(
        '--console',
        action='store_true',
        help='Run console visualization only (no hardware needed)'
    )
    parser.add_argument(
        '--pattern',
        type=str,
        help='Display specific pattern (e.g., happy, heart, water)'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available patterns'
    )
    parser.add_argument(
        '--animate',
        action='store_true',
        help='Show rise/fall animations between patterns (console mode)'
    )
    parser.add_argument(
        '--style',
        type=str,
        choices=['cascade', 'wave', 'synchronized'],
        default='cascade',
        help='Animation style (cascade, wave, or synchronized)'
    )

    args = parser.parse_args()

    if args.list:
        print("\n📋 Available Patterns:")
        print("\nExpressions:")
        for name in EXPRESSIONS.keys():
            print(f"  • {name}")
        print("\nIcons:")
        for name in ICONS.keys():
            print(f"  • {name}")
        print()
        return

    if args.console or not HAS_HARDWARE:
        console_demo(animated=args.animate, animation_style=args.style)
    else:
        hardware_demo(args.pattern)


if __name__ == '__main__':
    main()
