"""
Mood Management System
Tracks emotional state and maps to visual expressions
"""

from enum import Enum
from typing import Tuple, Optional
import logging

from .pixel_art import ColorPalette, get_pattern

logger = logging.getLogger(__name__)


class Mood(Enum):
    """Emotional states for the Pixel Plant"""
    HAPPY = "happy"
    VERY_HAPPY = "very_happy"
    CONTENT = "content"
    CONCERNED = "concerned"
    WORRIED = "worried"
    SLEEPING = "sleeping"
    THINKING = "thinking"
    CELEBRATING = "celebrating"


class MoodManager:
    """Manages emotional state and visual representation"""

    def __init__(self, initial_mood: Mood = Mood.CONTENT):
        """
        Initialize mood manager

        Args:
            initial_mood: Starting emotional state
        """
        self.current_mood = initial_mood
        self.concern_level = 0  # 0-10 scale
        self.previous_mood = None
        self.mood_history = []
        self._max_history = 100

    def update_mood(self, new_mood: Mood, reason: Optional[str] = None):
        """
        Update current mood

        Args:
            new_mood: New emotional state
            reason: Optional reason for mood change
        """
        if new_mood != self.current_mood:
            self.previous_mood = self.current_mood
            self.current_mood = new_mood

            # Track history
            self.mood_history.append({
                'mood': new_mood,
                'reason': reason,
                'concern_level': self.concern_level
            })

            if len(self.mood_history) > self._max_history:
                self.mood_history.pop(0)

            logger.info(f"Mood changed: {self.previous_mood.value} → {new_mood.value}"
                       + (f" ({reason})" if reason else ""))

    def escalate_concern(self, amount: int = 1):
        """
        Increase concern level

        Args:
            amount: How much to increase (default 1)
        """
        self.concern_level = min(10, self.concern_level + amount)

        # Update mood based on concern
        if self.concern_level >= 8:
            self.update_mood(Mood.WORRIED, "high concern")
        elif self.concern_level >= 4:
            self.update_mood(Mood.CONCERNED, "moderate concern")

        logger.debug(f"Concern escalated to {self.concern_level}/10")

    def reset_concern(self):
        """Reset concern level to 0"""
        old_level = self.concern_level
        self.concern_level = 0

        if old_level > 0:
            self.update_mood(Mood.HAPPY, "concern resolved")
            logger.debug("Concern reset")

    def celebrate(self):
        """Switch to celebration mood temporarily"""
        self.update_mood(Mood.CELEBRATING, "user achievement")
        self.reset_concern()

    def sleep(self):
        """Switch to sleeping mood"""
        self.update_mood(Mood.SLEEPING, "inactivity")
        self.concern_level = 0

    def wake(self):
        """Wake from sleeping mood"""
        self.update_mood(Mood.CONTENT, "activity detected")

    def get_visual_representation(self) -> Tuple[list, dict]:
        """
        Get LED pattern and color palette for current mood

        Returns:
            Tuple of (pattern, palette) for LED display
        """
        mood_map = {
            Mood.HAPPY: ('happy', ColorPalette.HAPPY),
            Mood.VERY_HAPPY: ('very_happy', ColorPalette.HAPPY),
            Mood.CONTENT: ('happy', ColorPalette.HAPPY),
            Mood.CONCERNED: ('concerned', ColorPalette.CONCERNED),
            Mood.WORRIED: ('worried', ColorPalette.WORRIED),
            Mood.SLEEPING: ('sleeping', ColorPalette.SLEEPING),
            Mood.THINKING: ('thinking', ColorPalette.NEUTRAL),
            Mood.CELEBRATING: ('very_happy', ColorPalette.CELEBRATING),
        }

        pattern_name, palette = mood_map.get(
            self.current_mood,
            ('happy', ColorPalette.HAPPY)
        )

        pattern = get_pattern(pattern_name)

        return pattern, palette

    def get_icon_for_message(self, message_type: str) -> Tuple[Optional[list], dict]:
        """
        Get icon pattern for a specific message type

        Args:
            message_type: Type of message being displayed

        Returns:
            Tuple of (pattern, palette) or (None, {}) if no icon
        """
        icon_map = {
            'hydration': ('water', ColorPalette.HYDRATION),
            'movement': ('walking', ColorPalette.SUCCESS),
            'stretch': ('stretching', ColorPalette.SUCCESS),
            'celebration': ('heart', ColorPalette.LOVE),
            'encouragement': ('heart', ColorPalette.LOVE),
            'break': ('sparkle', ColorPalette.CELEBRATING),
        }

        if message_type not in icon_map:
            return None, {}

        icon_name, palette = icon_map[message_type]
        pattern = get_pattern(icon_name)

        return pattern, palette

    def should_show_concern(self) -> bool:
        """Check if plant should show visible concern"""
        return self.concern_level >= 3

    def get_urgency_level(self) -> int:
        """
        Get current urgency level for messaging

        Returns:
            1 (gentle), 2 (moderate), or 3 (concerned)
        """
        if self.concern_level >= 7:
            return 3
        elif self.concern_level >= 4:
            return 2
        else:
            return 1

    def __repr__(self) -> str:
        """String representation"""
        return (
            f"MoodManager(mood={self.current_mood.value}, "
            f"concern={self.concern_level}/10)"
        )


if __name__ == '__main__':
    """Test mood manager"""
    logging.basicConfig(level=logging.INFO)

    mood = MoodManager()
    print(f"Initial: {mood}\n")

    # Test concern escalation
    print("Escalating concern:")
    for i in range(10):
        mood.escalate_concern()
        pattern, palette = mood.get_visual_representation()
        print(f"  Level {mood.concern_level}: {mood.current_mood.value}")

    print()

    # Test celebration
    print("Celebrating:")
    mood.celebrate()
    print(f"  {mood}")

    # Test icon retrieval
    print("\nMessage icons:")
    for msg_type in ['hydration', 'movement', 'celebration']:
        pattern, palette = mood.get_icon_for_message(msg_type)
        print(f"  {msg_type}: {'✓' if pattern else '✗'}")
