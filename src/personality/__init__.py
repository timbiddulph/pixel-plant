"""
Personality System
Caring responses, mood management, and visual expressions
"""

from .messages import MessageLibrary, MessageType
from .mood import MoodManager, Mood
from .animations import PixelAnimator
from .pixel_art import ColorPalette, get_pattern, ALL_PATTERNS
from .transitions import ColorTransition, PatternTransition, AnimationEffect

__all__ = [
    'MessageLibrary',
    'MessageType',
    'MoodManager',
    'Mood',
    'PixelAnimator',
    'ColorPalette',
    'get_pattern',
    'ALL_PATTERNS',
    'ColorTransition',
    'PatternTransition',
    'AnimationEffect',
]
