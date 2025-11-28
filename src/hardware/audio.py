"""
Audio System Hardware Abstraction
Text-to-speech output for caring personality
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class AudioSystem:
    """Text-to-speech audio output system"""

    def __init__(self, volume: int = 70, rate: int = 150,
                 voice_enabled: bool = True, simulate: bool = False):
        """
        Initialize audio system

        Args:
            volume: Volume level (0-100)
            rate: Speech rate in words per minute
            voice_enabled: Enable voice output
            simulate: If True, print to console instead of speaking
        """
        self.volume = volume
        self.rate = rate
        self.voice_enabled = voice_enabled
        self.simulate = simulate
        self.engine = None

        if not simulate and voice_enabled:
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', rate)
                self.engine.setProperty('volume', volume / 100.0)
                logger.info("Audio system initialized with pyttsx3")

            except Exception as e:
                logger.warning(f"Failed to initialize pyttsx3: {e}")
                logger.info("Falling back to simulation mode")
                self.simulate = True
        else:
            logger.info("Audio system running in simulation mode")

    def speak(self, text: str, wait: bool = True):
        """
        Speak text aloud

        Args:
            text: Text to speak
            wait: If True, block until speech completes
        """
        if not self.voice_enabled:
            return

        if self.simulate:
            print(f"\n[AUDIO] 🔊 '{text}'")
            return

        try:
            if wait:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                # Non-blocking speech
                self.engine.say(text)
                self.engine.startLoop(False)
                self.engine.iterate()
                self.engine.endLoop()

        except Exception as e:
            logger.error(f"Speech error: {e}")

    def set_volume(self, volume: int):
        """
        Set volume level

        Args:
            volume: 0-100
        """
        self.volume = max(0, min(100, volume))

        if not self.simulate and self.engine:
            self.engine.setProperty('volume', self.volume / 100.0)

    def set_rate(self, rate: int):
        """
        Set speech rate

        Args:
            rate: Words per minute (typically 100-200)
        """
        self.rate = rate

        if not self.simulate and self.engine:
            self.engine.setProperty('rate', rate)

    def enable_voice(self, enabled: bool):
        """Enable or disable voice output"""
        self.voice_enabled = enabled

    def close(self):
        """Clean up resources"""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
        logger.info("Audio system closed")


if __name__ == '__main__':
    """Test audio system"""
    logging.basicConfig(level=logging.INFO)

    audio = AudioSystem(simulate=True)

    # Test caring messages
    messages = [
        "Hey there! You need to hydrate!",
        "How about a snack? Take a walk! Stretch it out!",
        "Aw, it's not so bad! Give yourself a hug!",
        "Wonderful! You took care of yourself! I'm so proud!",
    ]

    for msg in messages:
        audio.speak(msg)
        import time
        time.sleep(1)

    audio.close()
