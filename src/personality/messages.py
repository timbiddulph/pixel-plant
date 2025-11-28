"""
Caring Message Library
Personality-rich responses for different situations
"""

import random
from enum import Enum
from typing import List, Optional


class MessageType(Enum):
    """Categories of caring messages"""
    HYDRATION = "hydration"
    MOVEMENT = "movement"
    STRETCH = "stretch"
    BREAK = "break"
    ENCOURAGEMENT = "encouragement"
    CELEBRATION = "celebration"
    GREETING = "greeting"
    GOODNIGHT = "goodnight"
    CHECKING_IN = "checking_in"
    CONCERN = "concern"
    GENTLE_REMINDER = "gentle_reminder"


class MessageLibrary:
    """Collection of caring messages with personality"""

    # Hydration reminders
    HYDRATION_MESSAGES = [
        "Hey there! You need to hydrate!",
        "Time for some water, friend!",
        "Your body's calling for hydration!",
        "Let's grab some water together!",
        "Hydration check! How about a drink?",
        "Water break time! Your cells will thank you!",
    ]

    # Movement encouragement
    MOVEMENT_MESSAGES = [
        "How about a snack? Take a walk! Stretch it out!",
        "Let's get moving! Your body needs it!",
        "Time to stretch those legs!",
        "A little walk would do wonders right now!",
        "Movement break! Let's go!",
        "Your muscles are calling for some action!",
    ]

    # Stretch suggestions
    STRETCH_MESSAGES = [
        "Stretch it out! Your back will love you!",
        "Time for a good stretch!",
        "Let's loosen up a bit!",
        "Stretch break! Reach for the sky!",
        "Your spine wants to say hello!",
    ]

    # Break reminders
    BREAK_MESSAGES = [
        "You've been working hard! Take a break!",
        "Break time! Step away for a moment!",
        "Let's pause and breathe!",
        "Time to rest those eyes and mind!",
        "You deserve a little break!",
    ]

    # Encouragement
    ENCOURAGEMENT_MESSAGES = [
        "Aw, it's not so bad! Give yourself a hug!",
        "You're doing great! Keep going!",
        "I believe in you!",
        "You've got this!",
        "Remember to be kind to yourself!",
        "One step at a time, friend!",
        "You're stronger than you think!",
    ]

    # Celebration
    CELEBRATION_MESSAGES = [
        "Wonderful! You took care of yourself! I'm so proud!",
        "Yes! That's what I'm talking about!",
        "You did it! Amazing!",
        "Look at you, being so responsible!",
        "That's the spirit! Well done!",
        "Proud of you for listening to your body!",
        "Excellent! Keep up the great work!",
    ]

    # Greetings
    GREETING_MESSAGES = [
        "Good to see you!",
        "Hello there, friend!",
        "Welcome back!",
        "Hey! Great to have you here!",
        "Hi! Ready for a good day?",
    ]

    # Goodnight
    GOODNIGHT_MESSAGES = [
        "Sleep well, friend!",
        "Sweet dreams! See you tomorrow!",
        "Rest well! You earned it!",
        "Goodnight! Take care!",
        "Time to recharge! Sleep tight!",
    ]

    # Check-in
    CHECKING_IN_MESSAGES = [
        "How are you doing?",
        "Just checking in on you!",
        "Everything okay over there?",
        "Wanted to see how you're feeling!",
        "How's it going, friend?",
    ]

    # Concern
    CONCERN_MESSAGES = [
        "I'm a bit worried about you...",
        "Hey, I noticed you haven't moved in a while...",
        "Are you okay? You've been sitting for quite some time.",
        "I care about you... can we take a break?",
        "I'm here for you, but I'm getting concerned...",
    ]

    # Gentle reminders
    GENTLE_REMINDER_MESSAGES = [
        "Just a gentle reminder...",
        "Not to nag, but...",
        "I know you're busy, however...",
        "Quick reminder from your caring friend...",
        "Hope I'm not bothering you, but...",
    ]

    def __init__(self, personality_level: int = 5):
        """
        Initialize message library

        Args:
            personality_level: 1-10, affects message frequency and style
        """
        self.personality_level = max(1, min(10, personality_level))
        self._message_history = []
        self._max_history = 50

    def get_message(self, message_type: MessageType,
                    avoid_recent: bool = True) -> str:
        """
        Get a random message of specified type

        Args:
            message_type: Type of message needed
            avoid_recent: If True, avoid recently used messages

        Returns:
            Message string
        """
        # Get message pool
        message_pool = self._get_message_pool(message_type)

        if not message_pool:
            return "Hey there!"

        # Filter out recent messages if requested
        if avoid_recent and len(self._message_history) > 0:
            recent = set(self._message_history[-5:])
            available = [m for m in message_pool if m not in recent]

            # If filtering removes everything, use full pool
            if not available:
                available = message_pool
        else:
            available = message_pool

        # Select random message
        message = random.choice(available)

        # Track in history
        self._message_history.append(message)
        if len(self._message_history) > self._max_history:
            self._message_history.pop(0)

        return message

    def _get_message_pool(self, message_type: MessageType) -> List[str]:
        """Get the message pool for a given type"""
        pools = {
            MessageType.HYDRATION: self.HYDRATION_MESSAGES,
            MessageType.MOVEMENT: self.MOVEMENT_MESSAGES,
            MessageType.STRETCH: self.STRETCH_MESSAGES,
            MessageType.BREAK: self.BREAK_MESSAGES,
            MessageType.ENCOURAGEMENT: self.ENCOURAGEMENT_MESSAGES,
            MessageType.CELEBRATION: self.CELEBRATION_MESSAGES,
            MessageType.GREETING: self.GREETING_MESSAGES,
            MessageType.GOODNIGHT: self.GOODNIGHT_MESSAGES,
            MessageType.CHECKING_IN: self.CHECKING_IN_MESSAGES,
            MessageType.CONCERN: self.CONCERN_MESSAGES,
            MessageType.GENTLE_REMINDER: self.GENTLE_REMINDER_MESSAGES,
        }
        return pools.get(message_type, [])

    def compose_reminder(self, message_type: MessageType,
                        urgency: int = 1) -> str:
        """
        Compose a caring reminder with appropriate urgency

        Args:
            message_type: Type of reminder
            urgency: 1-3, escalating concern level

        Returns:
            Complete reminder message
        """
        if urgency == 1:
            # Gentle, friendly
            return self.get_message(message_type)

        elif urgency == 2:
            # More insistent, still caring
            prefix = self.get_message(MessageType.GENTLE_REMINDER)
            main = self.get_message(message_type)
            return f"{prefix} {main}"

        else:
            # Concerned, but supportive
            prefix = self.get_message(MessageType.CONCERN)
            main = self.get_message(message_type)
            return f"{prefix} {main}"

    def get_celebration(self, achievement: str = "taking care") -> str:
        """
        Get a celebration message

        Args:
            achievement: What to celebrate

        Returns:
            Celebration message
        """
        base = self.get_message(MessageType.CELEBRATION)
        return base

    def clear_history(self):
        """Clear message history"""
        self._message_history = []


if __name__ == '__main__':
    """Test message library"""
    library = MessageLibrary(personality_level=5)

    print("=== CARING MESSAGE LIBRARY TEST ===\n")

    # Test each message type
    for msg_type in MessageType:
        print(f"{msg_type.value.upper()}:")
        for i in range(3):
            msg = library.get_message(msg_type)
            print(f"  - {msg}")
        print()

    # Test urgency levels
    print("URGENCY ESCALATION:")
    for urgency in [1, 2, 3]:
        msg = library.compose_reminder(MessageType.HYDRATION, urgency=urgency)
        print(f"  Level {urgency}: {msg}")
