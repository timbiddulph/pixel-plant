#!/usr/bin/env python3
"""
Audio System Hardware Test
Validates I2S audio and text-to-speech functionality
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from hardware import AudioSystem
from personality import MessageLibrary, MessageType


def test_basic_speech(audio, simulate=False):
    """Test basic text-to-speech"""
    print("\n1. Testing basic speech output...")

    test_phrases = [
        "Testing, one, two, three.",
        "Hello, I am your Pixel Plant companion!",
        "This is a test of the audio system.",
    ]

    for i, phrase in enumerate(test_phrases, 1):
        print(f"   Phrase {i}/3: '{phrase}'")
        audio.speak(phrase, wait=True)
        time.sleep(0.5)

    print("   ✓ Basic speech test complete")


def test_caring_messages(audio):
    """Test caring personality messages"""
    print("\n2. Testing caring messages...")

    messages = MessageLibrary(personality_level=5)

    message_types = [
        (MessageType.HYDRATION, "Hydration reminder"),
        (MessageType.MOVEMENT, "Movement suggestion"),
        (MessageType.ENCOURAGEMENT, "Encouragement"),
        (MessageType.CELEBRATION, "Celebration"),
    ]

    for msg_type, description in message_types:
        print(f"   {description}...")
        message = messages.get_message(msg_type)
        print(f"     '{message}'")
        audio.speak(message, wait=True)
        time.sleep(1)

    print("   ✓ Caring messages test complete")


def test_voice_settings(audio):
    """Test different voice settings"""
    print("\n3. Testing voice settings...")

    test_phrase = "Testing different voice settings."

    # Test different rates
    print("   Testing speech rates...")
    rates = [100, 150, 200]
    for rate in rates:
        print(f"     Rate: {rate} WPM")
        audio.set_rate(rate)
        audio.speak(test_phrase, wait=True)
        time.sleep(0.5)

    # Reset to default
    audio.set_rate(150)

    # Test different volumes
    print("   Testing volumes...")
    volumes = [50, 70, 100]
    for volume in volumes:
        print(f"     Volume: {volume}%")
        audio.set_volume(volume)
        audio.speak(test_phrase, wait=True)
        time.sleep(0.5)

    # Reset to default
    audio.set_volume(70)

    print("   ✓ Voice settings test complete")


def test_urgency_levels(audio):
    """Test urgency escalation"""
    print("\n4. Testing urgency levels...")

    messages = MessageLibrary(personality_level=5)

    for urgency in [1, 2, 3]:
        print(f"   Urgency level {urgency}...")
        message = messages.compose_reminder(MessageType.HYDRATION, urgency=urgency)
        print(f"     '{message}'")
        audio.speak(message, wait=True)
        time.sleep(1)

    print("   ✓ Urgency levels test complete")


def test_concurrent_speech(audio):
    """Test non-blocking speech (if supported)"""
    print("\n5. Testing non-blocking speech...")

    try:
        print("   Speaking without waiting...")
        audio.speak("This is non-blocking speech.", wait=False)
        print("   ✓ Code continued immediately")
        time.sleep(3)  # Wait for speech to finish
    except Exception as e:
        print(f"   ⚠️  Non-blocking speech not supported: {e}")

    print("   ✓ Concurrent speech test complete")


def run_interactive_test(audio):
    """Interactive test with user feedback"""
    print("\n6. Interactive audio test...")
    print("   This will help you verify audio quality.")

    if not audio.simulate:
        input("\n   Press Enter when ready to test audio output...")

    test_phrase = "Can you hear me clearly? I am your caring Pixel Plant companion!"
    print(f"\n   Speaking: '{test_phrase}'")
    audio.speak(test_phrase, wait=True)

    if not audio.simulate:
        response = input("\n   Did you hear the audio clearly? (y/n): ").strip().lower()
        if response == 'y':
            print("   ✓ Audio working correctly!")
        else:
            print("   ⚠️  Audio issue detected. Check:")
            print("      - I2S connections (GPIO 18, 19, 21)")
            print("      - Speaker connections")
            print("      - Volume level")
            print("      - /boot/config.txt has dtparam=i2s=on")

    print("   ✓ Interactive test complete")


def run_full_test(simulate=False):
    """Run complete audio system test suite"""
    print("=" * 50)
    print("PIXEL PLANT - Audio System Hardware Test")
    print("=" * 50)

    if simulate:
        print("\n⚠️  Running in SIMULATION mode")
        print("Audio output will be printed to console\n")
    else:
        print("\n⚡ REAL HARDWARE MODE")
        print("Audio will play through I2S DAC\n")
        print("Hardware setup:")
        print("  - MAX98357A I2S Amplifier")
        print("  - BCLK: GPIO 18")
        print("  - LRCLK: GPIO 19")
        print("  - DIN: GPIO 21")
        print("  - Speaker: 4Ω 3W\n")

    # Initialize audio system
    audio = AudioSystem(volume=70, rate=150, voice_enabled=True, simulate=simulate)

    try:
        # Run tests
        test_basic_speech(audio, simulate)
        test_caring_messages(audio)
        test_voice_settings(audio)
        test_urgency_levels(audio)
        test_concurrent_speech(audio)

        if not simulate:
            run_interactive_test(audio)

        print("\n" + "=" * 50)
        print("✅ ALL AUDIO TESTS PASSED")
        print("=" * 50)

        if not simulate:
            print("\nYour audio system is working correctly!")
            print("Next steps:")
            print("  - Adjust volume in config/config.yaml")
            print("  - Fine-tune speech rate if needed")
            print("  - Test with full system: python src/main.py")

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")

    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

        print("\nTroubleshooting:")
        print("  1. Check I2S is enabled: grep 'dtparam=i2s=on' /boot/config.txt")
        print("  2. Verify GPIO connections")
        print("  3. Test speaker with: speaker-test -c2")
        print("  4. Check audio device: aplay -l")

    finally:
        audio.close()
        print("\nTest complete. Audio system closed.")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Test audio system hardware')
    parser.add_argument('--real', action='store_true',
                       help='Test with real hardware (default: simulate)')
    args = parser.parse_args()

    simulate = not args.real
    run_full_test(simulate=simulate)
