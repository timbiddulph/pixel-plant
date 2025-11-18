"""
Pixel Art Patterns for 8x8 LED Matrix
Defines emotional expressions and icons for the Pixel Plant

Pattern Format:
- 8x8 grid of integers
- 0 = off/background (black)
- 1 = primary color (face outline, main features)
- 2 = secondary color (eyes, details)
- 3 = accent color (highlights, special features)

Colors are mapped at runtime based on mood state.
"""

# =============================================================================
# EMOTIONAL EXPRESSIONS
# =============================================================================

HAPPY_FACE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],  # Eyes
    [0, 0, 2, 0, 0, 2, 0, 0],  # Pupils
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],  # Smile corners
    [0, 0, 1, 0, 0, 1, 0, 0],  # Smile curve
    [0, 0, 0, 1, 1, 0, 0, 0],  # Smile bottom
    [0, 0, 0, 0, 0, 0, 0, 0],
]

VERY_HAPPY_FACE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],  # Big happy eyes
    [0, 1, 2, 0, 0, 2, 1, 0],  # Pupils
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1],  # Wide smile
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

CONCERNED_FACE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],  # Eyes
    [0, 0, 2, 0, 0, 2, 0, 0],  # Pupils
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],  # Straight mouth
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

WORRIED_FACE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],  # Angled eyebrows (worried)
    [0, 0, 1, 0, 0, 1, 0, 0],  # Eyes
    [0, 0, 2, 0, 0, 2, 0, 0],  # Pupils
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],  # Frown top
    [0, 0, 1, 0, 0, 1, 0, 0],  # Frown curve
    [0, 1, 0, 0, 0, 0, 1, 0],  # Frown bottom
]

SLEEPING_FACE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],  # Closed eyes (horizontal lines)
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],  # Peaceful mouth
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

SLEEPING_ZZZ = [
    [0, 0, 0, 0, 3, 3, 3, 0],  # Z
    [0, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 3, 3, 3, 0],
    [0, 0, 3, 3, 0, 0, 0, 0],  # Z
    [0, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 3, 3, 0, 0, 0, 0],
    [3, 3, 0, 0, 0, 0, 0, 0],  # Z
    [0, 3, 0, 0, 0, 0, 0, 0],
]

THINKING_FACE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],  # Eyes looking up
    [0, 1, 2, 0, 0, 2, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],  # Small thoughtful mouth
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

# =============================================================================
# ICONS & SYMBOLS
# =============================================================================

HEART = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 0, 0],
    [1, 2, 2, 1, 2, 2, 1, 0],
    [1, 2, 2, 2, 2, 2, 1, 0],
    [0, 1, 2, 2, 2, 1, 0, 0],
    [0, 0, 1, 2, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

WATER_DROP = [
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 2, 1, 0, 0, 0],
    [0, 1, 2, 2, 2, 1, 0, 0],
    [0, 1, 2, 3, 2, 1, 0, 0],  # 3 = highlight
    [0, 1, 2, 2, 2, 1, 0, 0],
    [0, 0, 1, 2, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

CHECKMARK = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 0, 0],
    [1, 1, 0, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

EXCLAMATION = [
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

WALKING_PERSON = [
    [0, 0, 0, 1, 1, 0, 0, 0],  # Head
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],  # Body
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0],  # Arm
    [0, 0, 0, 1, 0, 0, 0, 0],  # Leg
    [0, 0, 0, 0, 1, 0, 0, 0],  # Other leg
    [0, 0, 0, 0, 0, 0, 0, 0],
]

STRETCHING_PERSON = [
    [0, 0, 1, 1, 1, 1, 0, 0],  # Arms up
    [0, 0, 0, 1, 1, 0, 0, 0],  # Head
    [0, 0, 0, 1, 1, 0, 0, 0],  # Body
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],  # Legs
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

SPARKLE = [
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 1, 0, 0, 0],
    [1, 0, 0, 2, 0, 0, 1, 0],
    [0, 0, 1, 2, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

QUESTION_MARK = [
    [0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

# =============================================================================
# COLOR PALETTES (RGB tuples)
# =============================================================================

class ColorPalette:
    """Color schemes for different moods and states."""

    # Happy/Content colors (green/blue)
    HAPPY = {
        0: (0, 0, 0),       # Background (off)
        1: (0, 50, 0),      # Primary (green outline)
        2: (0, 30, 0),      # Secondary (darker green)
        3: (0, 80, 20),     # Accent (bright green-cyan)
    }

    # Very Happy/Celebrating (bright multi-color)
    CELEBRATING = {
        0: (0, 0, 0),
        1: (50, 50, 0),     # Yellow
        2: (50, 20, 0),     # Orange
        3: (50, 0, 50),     # Magenta
    }

    # Concerned (yellow/amber)
    CONCERNED = {
        0: (0, 0, 0),
        1: (40, 40, 0),     # Yellow
        2: (30, 20, 0),     # Amber
        3: (50, 50, 10),    # Bright yellow
    }

    # Worried (orange/red)
    WORRIED = {
        0: (0, 0, 0),
        1: (50, 15, 0),     # Orange
        2: (40, 5, 0),      # Deep orange
        3: (60, 20, 0),     # Bright orange
    }

    # Sleeping (blue/purple)
    SLEEPING = {
        0: (0, 0, 0),
        1: (0, 0, 30),      # Deep blue
        2: (0, 0, 20),      # Darker blue
        3: (10, 0, 40),     # Purple
    }

    # Hydration reminder (cyan/blue)
    HYDRATION = {
        0: (0, 0, 0),
        1: (0, 30, 50),     # Cyan
        2: (0, 40, 60),     # Bright cyan
        3: (20, 50, 60),    # Light cyan (highlight)
    }

    # Love/Encouragement (pink/red)
    LOVE = {
        0: (0, 0, 0),
        1: (50, 0, 20),     # Deep pink
        2: (60, 0, 30),     # Bright pink
        3: (40, 0, 40),     # Magenta
    }

    # Success/Acknowledgment (green)
    SUCCESS = {
        0: (0, 0, 0),
        1: (0, 50, 10),     # Bright green
        2: (0, 40, 5),      # Green
        3: (10, 60, 20),    # Lime green
    }

    # Alert/Attention (red/orange)
    ALERT = {
        0: (0, 0, 0),
        1: (50, 20, 0),     # Orange-red
        2: (60, 10, 0),     # Red-orange
        3: (70, 30, 0),     # Bright orange
    }

    # Neutral/Thinking (white/gray)
    NEUTRAL = {
        0: (0, 0, 0),
        1: (30, 30, 30),    # Gray
        2: (20, 20, 20),    # Darker gray
        3: (50, 50, 50),    # Bright gray
    }


# =============================================================================
# PATTERN COLLECTIONS
# =============================================================================

EXPRESSIONS = {
    'happy': HAPPY_FACE,
    'very_happy': VERY_HAPPY_FACE,
    'concerned': CONCERNED_FACE,
    'worried': WORRIED_FACE,
    'sleeping': SLEEPING_FACE,
    'sleeping_zzz': SLEEPING_ZZZ,
    'thinking': THINKING_FACE,
}

ICONS = {
    'heart': HEART,
    'water': WATER_DROP,
    'check': CHECKMARK,
    'exclamation': EXCLAMATION,
    'walking': WALKING_PERSON,
    'stretching': STRETCHING_PERSON,
    'sparkle': SPARKLE,
    'question': QUESTION_MARK,
}

ALL_PATTERNS = {**EXPRESSIONS, **ICONS}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_pattern(name):
    """
    Get a pattern by name.

    Args:
        name: Pattern name (e.g., 'happy', 'heart', 'water')

    Returns:
        8x8 list pattern or None if not found
    """
    return ALL_PATTERNS.get(name)


def get_colored_pattern(pattern, palette):
    """
    Convert a pattern template to colored RGB values.

    Args:
        pattern: 8x8 list of integers (0-3)
        palette: Dictionary mapping integers to RGB tuples

    Returns:
        8x8 list of RGB tuples
    """
    colored = []
    for row in pattern:
        colored_row = [palette[pixel] for pixel in row]
        colored.append(colored_row)
    return colored


def visualize_pattern(pattern, palette=None):
    """
    Print a text visualization of the pattern.
    Useful for debugging and design.

    Args:
        pattern: 8x8 list pattern
        palette: Optional color palette (uses ASCII if None)
    """
    if palette is None:
        # Use ASCII characters for visualization
        chars = {0: ' ', 1: '█', 2: '▓', 3: '░'}
        for row in pattern:
            print(''.join(chars.get(p, '?') for p in row))
    else:
        # Show RGB values
        for row in pattern:
            colors = [palette[p] for p in row]
            print(colors)


def list_available_patterns():
    """List all available pattern names."""
    print("Available Expressions:")
    for name in EXPRESSIONS.keys():
        print(f"  - {name}")
    print("\nAvailable Icons:")
    for name in ICONS.keys():
        print(f"  - {name}")


# =============================================================================
# DEMO CODE
# =============================================================================

if __name__ == '__main__':
    """Demo: visualize all patterns"""
    print("=" * 40)
    print("PIXEL PLANT PATTERN LIBRARY")
    print("=" * 40)
    print()

    print("EXPRESSIONS:")
    print("-" * 40)
    for name, pattern in EXPRESSIONS.items():
        print(f"\n{name.upper()}:")
        visualize_pattern(pattern)

    print("\n" + "=" * 40)
    print("ICONS:")
    print("-" * 40)
    for name, pattern in ICONS.items():
        print(f"\n{name.upper()}:")
        visualize_pattern(pattern)

    print("\n" + "=" * 40)
    print("\nRun with --colors to see color palettes")
