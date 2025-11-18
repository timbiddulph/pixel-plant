#!/usr/bin/env python3
"""
Quick animation test - shows rise/fall in action
Run this to see pixels rising and falling between patterns!
"""

import sys
import os
import time

# Add src to path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
src_dir = os.path.join(project_root, 'src')
sys.path.insert(0, src_dir)

from personality.pixel_art import HAPPY_FACE, HEART, WATER_DROP, CONCERNED_FACE
from personality.animations import PixelAnimator

def clear_and_print(pattern, title=""):
    """Clear screen and print pattern."""
    print('\033[2J\033[H', end='')  # Clear screen
    if title:
        print(f"🌿 {title}")
        print("-" * 30)

    chars = {0: ' ', 1: '█', 2: '▓', 3: '░'}
    for row in pattern:
        print('  ' + ''.join(chars.get(p, '?') for p in row))
    print()

def demo_style(style_name):
    """Demo a specific animation style."""
    print('\033[2J\033[H')
    print(f"\n{'='*50}")
    print(f"  PIXEL RISE & FALL DEMO - {style_name.upper()}")
    print(f"{'='*50}\n")
    print("  Watch the pixels rise from the base to form each image,")
    print("  then fall and rise again for the next pattern!\n")
    print("  (Just like in Becky Chambers' novel!)\n")
    time.sleep(3)

    animator = PixelAnimator()

    patterns = [
        ("Happy Face", HAPPY_FACE),
        ("Heart", HEART),
        ("Water Drop", WATER_DROP),
        ("Concerned Face", CONCERNED_FACE),
    ]

    current = None

    for name, pattern in patterns:
        for frame in animator.transition(current, pattern, style=style_name, fall_steps=6, rise_steps=8):
            clear_and_print(frame, name)
            time.sleep(0.08)

        current = pattern
        time.sleep(1.2)  # Hold

    print("\n  ✨ Animation complete!")
    print(f"  {'='*50}\n")

if __name__ == '__main__':
    styles = {
        '1': 'cascade',
        '2': 'wave',
        '3': 'synchronized'
    }

    print("\n🌿 Pixel Plant Animation Demo")
    print("=" * 50)
    print("\nChoose animation style:")
    print("  1. Cascade (bottom pixels rise first)")
    print("  2. Wave (columns rise left to right)")
    print("  3. Synchronized (all pixels rise together)")
    print("\nOr press Enter for cascade (default)")
    print("-" * 50)

    choice = input("\nYour choice (1-3): ").strip()

    if not choice:
        choice = '1'

    style = styles.get(choice, 'cascade')

    try:
        demo_style(style)
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo stopped\n")
