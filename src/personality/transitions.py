"""
Smooth Color Transitions
Creates smooth, organic transitions between colors and patterns
"""

import time
import math
from typing import List, Tuple, Optional, Dict


class ColorTransition:
    """Handles smooth color transitions"""

    @staticmethod
    def lerp_color(color1: Tuple[int, int, int],
                   color2: Tuple[int, int, int],
                   progress: float) -> Tuple[int, int, int]:
        """
        Linear interpolation between two colors

        Args:
            color1: Starting RGB color
            color2: Ending RGB color
            progress: 0.0 to 1.0

        Returns:
            Interpolated RGB color
        """
        r1, g1, b1 = color1
        r2, g2, b2 = color2

        r = int(r1 + (r2 - r1) * progress)
        g = int(g1 + (g2 - g1) * progress)
        b = int(b1 + (b2 - b1) * progress)

        return (r, g, b)

    @staticmethod
    def ease_in_out(progress: float) -> float:
        """
        Smooth ease-in-out function

        Args:
            progress: 0.0 to 1.0

        Returns:
            Eased progress value
        """
        # Cubic ease-in-out
        if progress < 0.5:
            return 4 * progress * progress * progress
        else:
            p = 2 * progress - 2
            return 1 + p * p * p / 2

    @staticmethod
    def pulse(progress: float) -> float:
        """
        Pulsing function (sine wave)

        Args:
            progress: 0.0 to 1.0

        Returns:
            Pulse value 0.0 to 1.0
        """
        return (math.sin(progress * 2 * math.pi) + 1) / 2

    @staticmethod
    def breathe(progress: float) -> float:
        """
        Breathing function (gentle sine wave)

        Args:
            progress: 0.0 to 1.0

        Returns:
            Breath value 0.3 to 1.0 (never fully off)
        """
        return 0.3 + 0.7 * ColorTransition.pulse(progress)

    @staticmethod
    def transition_palette(palette1: Dict, palette2: Dict,
                          progress: float, easing: bool = True) -> Dict:
        """
        Smoothly transition between two color palettes

        Args:
            palette1: Starting palette
            palette2: Ending palette
            progress: 0.0 to 1.0
            easing: Apply easing function

        Returns:
            Interpolated palette
        """
        if easing:
            progress = ColorTransition.ease_in_out(progress)

        result = {}
        keys = set(palette1.keys()) | set(palette2.keys())

        for key in keys:
            color1 = palette1.get(key, (0, 0, 0))
            color2 = palette2.get(key, (0, 0, 0))
            result[key] = ColorTransition.lerp_color(color1, color2, progress)

        return result

    @staticmethod
    def rainbow_cycle(progress: float, saturation: float = 1.0,
                     brightness: float = 1.0) -> Tuple[int, int, int]:
        """
        Generate rainbow colors

        Args:
            progress: 0.0 to 1.0 (position in rainbow)
            saturation: 0.0 to 1.0
            brightness: 0.0 to 1.0

        Returns:
            RGB color
        """
        # HSV to RGB conversion
        h = progress * 360  # Hue in degrees
        s = saturation
        v = brightness

        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        return (
            int((r + m) * 255),
            int((g + m) * 255),
            int((b + m) * 255)
        )


class PatternTransition:
    """Handles smooth pattern transitions"""

    @staticmethod
    def crossfade(pattern1: List[List], pattern2: List[List],
                  palette1: Dict, palette2: Dict,
                  progress: float, easing: bool = True) -> Tuple[List[List], Dict]:
        """
        Crossfade between two patterns

        Args:
            pattern1: Starting pattern
            pattern2: Ending pattern
            palette1: Starting palette
            palette2: Ending palette
            progress: 0.0 to 1.0
            easing: Apply easing

        Returns:
            Tuple of (current_pattern, current_palette)
        """
        if easing:
            progress = ColorTransition.ease_in_out(progress)

        # For now, just transition the palette
        # Pattern stays as pattern2 (could blend pixels in future)
        current_palette = ColorTransition.transition_palette(
            palette1, palette2, progress, easing=False
        )

        # Blend patterns if they differ
        if progress < 0.5:
            return pattern1, current_palette
        else:
            return pattern2, current_palette

    @staticmethod
    def fade_out_in(pattern1: List[List], pattern2: List[List],
                    palette1: Dict, palette2: Dict,
                    progress: float) -> Tuple[List[List], Dict]:
        """
        Fade out pattern1, then fade in pattern2

        Args:
            pattern1: Starting pattern
            pattern2: Ending pattern
            palette1: Starting palette
            palette2: Ending palette
            progress: 0.0 to 1.0

        Returns:
            Tuple of (current_pattern, current_palette)
        """
        if progress < 0.5:
            # Fade out first pattern
            fade_progress = progress * 2  # 0 to 1 over first half
            dimmed_palette = {}
            for key, color in palette1.items():
                dim_factor = 1.0 - fade_progress
                dimmed_palette[key] = (
                    int(color[0] * dim_factor),
                    int(color[1] * dim_factor),
                    int(color[2] * dim_factor)
                )
            return pattern1, dimmed_palette
        else:
            # Fade in second pattern
            fade_progress = (progress - 0.5) * 2  # 0 to 1 over second half
            dimmed_palette = {}
            for key, color in palette2.items():
                dim_factor = fade_progress
                dimmed_palette[key] = (
                    int(color[0] * dim_factor),
                    int(color[1] * dim_factor),
                    int(color[2] * dim_factor)
                )
            return pattern2, dimmed_palette


class AnimationEffect:
    """Pre-built animation effects"""

    @staticmethod
    def breathing(pattern: List[List], palette: Dict,
                  duration: float = 2.0, steps: int = 30) -> List[Tuple[List[List], Dict]]:
        """
        Create breathing animation frames

        Args:
            pattern: Base pattern
            palette: Base palette
            duration: Duration in seconds
            steps: Number of frames

        Returns:
            List of (pattern, palette) tuples for each frame
        """
        frames = []

        for step in range(steps):
            progress = step / steps
            brightness = ColorTransition.breathe(progress)

            # Scale palette
            scaled_palette = {}
            for key, color in palette.items():
                scaled_palette[key] = (
                    int(color[0] * brightness),
                    int(color[1] * brightness),
                    int(color[2] * brightness)
                )

            frames.append((pattern, scaled_palette))

        return frames

    @staticmethod
    def pulse_attention(pattern: List[List], palette: Dict,
                       pulses: int = 3, steps_per_pulse: int = 20) -> List[Tuple[List[List], Dict]]:
        """
        Create attention-getting pulse animation

        Args:
            pattern: Base pattern
            palette: Base palette
            pulses: Number of pulses
            steps_per_pulse: Frames per pulse

        Returns:
            List of (pattern, palette) frames
        """
        frames = []

        for pulse in range(pulses):
            for step in range(steps_per_pulse):
                progress = step / steps_per_pulse
                brightness = ColorTransition.pulse(progress)

                # Make pulse more dramatic
                brightness = 0.3 + 0.7 * brightness

                scaled_palette = {}
                for key, color in palette.items():
                    scaled_palette[key] = (
                        int(color[0] * brightness),
                        int(color[1] * brightness),
                        int(color[2] * brightness)
                    )

                frames.append((pattern, scaled_palette))

        return frames

    @staticmethod
    def rainbow_cycle_effect(pattern: List[List], steps: int = 60) -> List[Tuple[List[List], Dict]]:
        """
        Create rainbow cycling effect

        Args:
            pattern: Base pattern
            steps: Number of frames

        Returns:
            List of (pattern, palette) frames
        """
        frames = []

        for step in range(steps):
            progress = step / steps

            # Create rainbow palette
            rainbow_palette = {}
            for key in range(4):  # Assuming 0-3 palette keys
                # Offset each key for variety
                offset_progress = (progress + key * 0.25) % 1.0
                rainbow_palette[key] = ColorTransition.rainbow_cycle(offset_progress)

            frames.append((pattern, rainbow_palette))

        return frames

    @staticmethod
    def gentle_wave(pattern: List[List], palette: Dict,
                   duration: float = 3.0, steps: int = 40) -> List[Tuple[List[List], Dict]]:
        """
        Create gentle color wave effect

        Args:
            pattern: Base pattern
            palette: Base palette
            duration: Duration in seconds
            steps: Number of frames

        Returns:
            List of (pattern, palette) frames
        """
        frames = []

        # Define two slightly different color variations
        palette_a = palette
        palette_b = {}
        for key, color in palette.items():
            # Shift colors slightly
            palette_b[key] = (
                min(255, int(color[0] * 1.1)),
                min(255, int(color[1] * 1.1)),
                min(255, int(color[2] * 0.9))
            )

        for step in range(steps):
            progress = step / steps
            wave_progress = ColorTransition.pulse(progress)

            current_palette = ColorTransition.transition_palette(
                palette_a, palette_b, wave_progress, easing=True
            )

            frames.append((pattern, current_palette))

        return frames


if __name__ == '__main__':
    """Test color transitions"""
    print("=== COLOR TRANSITION TEST ===\n")

    # Test color interpolation
    color1 = (255, 0, 0)  # Red
    color2 = (0, 0, 255)  # Blue

    print("Color interpolation (Red to Blue):")
    for i in range(11):
        progress = i / 10
        color = ColorTransition.lerp_color(color1, color2, progress)
        print(f"  {progress:.1f}: RGB{color}")

    print("\nEasing function:")
    for i in range(11):
        progress = i / 10
        eased = ColorTransition.ease_in_out(progress)
        print(f"  {progress:.1f} -> {eased:.2f}")

    print("\nRainbow cycle:")
    for i in range(8):
        progress = i / 8
        color = ColorTransition.rainbow_cycle(progress)
        print(f"  {progress:.2f}: RGB{color}")

    print("\n✅ Color transition test complete")
