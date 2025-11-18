"""
Pixel Rise and Fall Animations
Inspired by the pixel plant in "The Long Way to a Small, Angry Planet"
where pixels rise up from the base to form images.

Animation Styles:
- Wave: Pixels rise column by column (left to right)
- Cascade: Pixels rise based on their final row position
- Synchronized: All pixels rise together at the same rate
- Waterfall: Pixels fall and rise in a flowing pattern
"""

import time
import copy


class PixelAnimator:
    """Handles rise and fall animations for 8x8 LED matrix patterns."""

    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height

    def rise_wave(self, pattern, steps=8, delay=0.05):
        """
        Pixels rise column by column from left to right.

        Args:
            pattern: 8x8 pattern to display
            steps: Number of animation steps per column
            delay: Delay between steps (seconds)

        Yields:
            Intermediate pattern states during animation
        """
        # Start with empty grid
        current = [[0] * self.width for _ in range(self.height)]

        for col in range(self.width):
            # Animate this column rising
            for step in range(steps):
                progress = (step + 1) / steps  # 0.0 to 1.0

                # Build current state with this column partially risen
                temp = copy.deepcopy(current)

                for row in range(self.height):
                    # Calculate how far this pixel should have risen
                    # Pixels start at bottom (row 7) and rise to their target row
                    target_row = row
                    current_row = self.height - 1 - int((self.height - 1 - target_row) * progress)

                    if current_row <= row:
                        # Pixel has reached its position
                        temp[row][col] = pattern[row][col]

                yield temp
                time.sleep(delay)

            # Finalize this column
            for row in range(self.height):
                current[row][col] = pattern[row][col]

        # Final state
        yield pattern

    def rise_cascade(self, pattern, steps=12, delay=0.04):
        """
        Pixels rise based on their final row position.
        Bottom rows rise first, top rows rise last.

        Args:
            pattern: 8x8 pattern to display
            steps: Number of animation steps
            delay: Delay between steps (seconds)

        Yields:
            Intermediate pattern states during animation
        """
        for step in range(steps + 1):
            progress = step / steps
            current = [[0] * self.width for _ in range(self.height)]

            for y in range(self.height):
                for x in range(self.width):
                    # Calculate when this pixel should start rising
                    # Bottom rows (y=7) start at progress=0
                    # Top rows (y=0) start at progress=0.7
                    start_progress = (self.height - 1 - y) / (self.height * 1.5)

                    if progress >= start_progress:
                        # Calculate rise progress for this specific pixel
                        pixel_progress = min(1.0, (progress - start_progress) * 2)

                        if pixel_progress >= 0.9:  # Pixel has risen
                            current[y][x] = pattern[y][x]

            yield current
            if step < steps:
                time.sleep(delay)

    def rise_synchronized(self, pattern, steps=10, delay=0.06):
        """
        All pixels rise together at the same rate.

        Args:
            pattern: 8x8 pattern to display
            steps: Number of animation steps
            delay: Delay between steps (seconds)

        Yields:
            Intermediate pattern states during animation
        """
        for step in range(steps + 1):
            progress = step / steps
            current = [[0] * self.width for _ in range(self.height)]

            # All pixels rise uniformly
            threshold_row = int((self.height - 1) * (1 - progress))

            for y in range(self.height):
                for x in range(self.width):
                    if y >= threshold_row:
                        current[y][x] = pattern[y][x]

            yield current
            if step < steps:
                time.sleep(delay)

    def fall_cascade(self, pattern, steps=10, delay=0.04):
        """
        Pixels fall based on their current row position.
        Top rows fall first, bottom rows fall last.

        Args:
            pattern: Current pattern to fall
            steps: Number of animation steps
            delay: Delay between steps (seconds)

        Yields:
            Intermediate pattern states during animation
        """
        for step in range(steps + 1):
            progress = step / steps
            current = copy.deepcopy(pattern)

            for y in range(self.height):
                for x in range(self.width):
                    # Top rows (y=0) start falling at progress=0
                    # Bottom rows (y=7) start falling at progress=0.7
                    start_progress = y / (self.height * 1.5)

                    if progress >= start_progress:
                        # Calculate fall progress for this pixel
                        pixel_progress = min(1.0, (progress - start_progress) * 2)

                        if pixel_progress >= 0.7:  # Pixel has fallen
                            current[y][x] = 0

            yield current
            if step < steps:
                time.sleep(delay)

    def fall_synchronized(self, pattern, steps=8, delay=0.05):
        """
        All pixels fall together at the same rate.

        Args:
            pattern: Current pattern to fall
            steps: Number of animation steps
            delay: Delay between steps (seconds)

        Yields:
            Intermediate pattern states during animation
        """
        for step in range(steps + 1):
            progress = step / steps
            current = copy.deepcopy(pattern)

            # All pixels fall uniformly
            threshold_row = int((self.height - 1) * progress)

            for y in range(self.height):
                for x in range(self.width):
                    if y <= threshold_row:
                        current[y][x] = 0

            yield current
            if step < steps:
                time.sleep(delay)

    def transition(self, from_pattern, to_pattern, style='cascade', fall_steps=8, rise_steps=10):
        """
        Complete transition from one pattern to another.
        Falls current pattern, then rises new pattern.

        Args:
            from_pattern: Current pattern (or None for first display)
            to_pattern: Target pattern
            style: Animation style ('wave', 'cascade', 'synchronized')
            fall_steps: Number of steps for fall animation
            rise_steps: Number of steps for rise animation

        Yields:
            All intermediate states during transition
        """
        # Fall current pattern (if exists)
        if from_pattern is not None:
            if style == 'cascade':
                yield from self.fall_cascade(from_pattern, steps=fall_steps)
            elif style == 'synchronized':
                yield from self.fall_synchronized(from_pattern, steps=fall_steps)
            else:  # default to cascade
                yield from self.fall_cascade(from_pattern, steps=fall_steps)

            # Brief pause at empty state
            empty = [[0] * self.width for _ in range(self.height)]
            yield empty
            time.sleep(0.1)

        # Rise new pattern
        if style == 'wave':
            yield from self.rise_wave(to_pattern, steps=rise_steps)
        elif style == 'cascade':
            yield from self.rise_cascade(to_pattern, steps=rise_steps)
        elif style == 'synchronized':
            yield from self.rise_synchronized(to_pattern, steps=rise_steps)
        else:  # default to cascade
            yield from self.rise_cascade(to_pattern, steps=rise_steps)


# =============================================================================
# CONSOLE VISUALIZATION
# =============================================================================

def visualize_pattern_console(pattern, palette=None, clear_screen=True):
    """
    Display pattern in console with optional color indicators.

    Args:
        pattern: 8x8 pattern grid
        palette: Optional palette name to show
        clear_screen: Clear console before drawing
    """
    if clear_screen:
        print('\033[2J\033[H', end='')  # Clear screen and move cursor to top

    # ASCII characters for visualization
    chars = {0: ' ', 1: '█', 2: '▓', 3: '░'}

    for row in pattern:
        print(''.join(chars.get(p, '?') for p in row))

    if palette:
        print(f"\n[{palette}]")


def demo_animation(animation_name='cascade'):
    """
    Demonstrate rise/fall animations in console.

    Args:
        animation_name: 'wave', 'cascade', or 'synchronized'
    """
    from pixel_art import HAPPY_FACE, HEART, WATER_DROP

    animator = PixelAnimator()

    patterns = [
        ('Happy Face', HAPPY_FACE),
        ('Heart', HEART),
        ('Water Drop', WATER_DROP),
    ]

    print(f"\n🎬 Demonstrating '{animation_name}' animation style")
    print("=" * 50)

    current_pattern = None

    for name, pattern in patterns:
        print(f"\n→ {name}")
        time.sleep(0.5)

        # Animate transition
        for frame in animator.transition(current_pattern, pattern, style=animation_name):
            visualize_pattern_console(frame, clear_screen=True)

        current_pattern = pattern
        time.sleep(1)  # Hold final state

    print("\n✨ Animation complete!")


# =============================================================================
# DEMO CODE
# =============================================================================

if __name__ == '__main__':
    """Demo animations in console"""
    import sys

    if len(sys.argv) > 1:
        style = sys.argv[1]
    else:
        style = 'cascade'

    valid_styles = ['wave', 'cascade', 'synchronized']

    if style not in valid_styles:
        print(f"Usage: python animations.py [style]")
        print(f"Styles: {', '.join(valid_styles)}")
        print(f"Example: python animations.py cascade")
        sys.exit(1)

    print("\n🌿 Pixel Plant Rise/Fall Animation Demo")
    print("=" * 50)
    print("Press Ctrl+C to stop\n")

    try:
        demo_animation(style)
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo stopped")
