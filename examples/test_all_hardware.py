#!/usr/bin/env python3
"""
Complete Hardware Validation Test
Tests all Pixel Plant hardware components
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from hardware import LEDMatrix, AudioSystem, CameraSystem, MotionSensor
from personality import get_pattern, ColorPalette


def test_led_matrix(simulate=False):
    """Test LED matrix"""
    print("\n" + "=" * 50)
    print("1. LED MATRIX TEST")
    print("=" * 50)

    matrix = LEDMatrix(gpio_pin=18, simulate=simulate)

    try:
        print("   Testing rainbow colors...")
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for r, g, b in colors:
            pattern = [[(r, g, b) for _ in range(8)] for _ in range(8)]
            matrix.show_pattern(pattern)
            time.sleep(1)

        print("   Testing patterns...")
        pattern = get_pattern('happy')
        palette = ColorPalette.HAPPY
        matrix.show_pattern(pattern, palette)
        time.sleep(2)

        matrix.clear()
        print("   ✅ LED Matrix: PASS")
        return True

    except Exception as e:
        print(f"   ❌ LED Matrix: FAIL - {e}")
        return False

    finally:
        matrix.close()


def test_audio_system(simulate=False):
    """Test audio/TTS system"""
    print("\n" + "=" * 50)
    print("2. AUDIO SYSTEM TEST")
    print("=" * 50)

    audio = AudioSystem(simulate=simulate)

    try:
        test_phrases = [
            "Hey there! Testing audio system!",
            "You need to hydrate!",
            "Let's take a break!",
        ]

        for i, phrase in enumerate(test_phrases, 1):
            print(f"   Speaking phrase {i}/3...")
            audio.speak(phrase)
            time.sleep(1)

        print("   ✅ Audio System: PASS")
        return True

    except Exception as e:
        print(f"   ❌ Audio System: FAIL - {e}")
        return False

    finally:
        audio.close()


def test_camera_system(simulate=False):
    """Test camera system"""
    print("\n" + "=" * 50)
    print("3. CAMERA SYSTEM TEST")
    print("=" * 50)

    camera = CameraSystem(resolution=(640, 480), simulate=simulate)

    try:
        print("   Starting camera...")
        camera.start()
        time.sleep(1)

        print("   Capturing 5 test frames...")
        for i in range(5):
            frame = camera.capture_frame()
            if frame is not None:
                print(f"      Frame {i+1}: {frame.shape}, {frame.dtype}")
                time.sleep(0.2)
            else:
                print(f"      Frame {i+1}: Failed")
                return False

        print("   ✅ Camera System: PASS")
        return True

    except Exception as e:
        print(f"   ❌ Camera System: FAIL - {e}")
        return False

    finally:
        camera.close()


def test_motion_sensor(simulate=False):
    """Test PIR motion sensor"""
    print("\n" + "=" * 50)
    print("4. MOTION SENSOR TEST")
    print("=" * 50)

    sensor = MotionSensor(gpio_pin=17, simulate=simulate)

    try:
        if not simulate:
            print("   Motion sensor armed - move in front of sensor...")
            print("   Waiting up to 10 seconds for motion...")

            detected = sensor.wait_for_motion(timeout=10.0)

            if detected:
                print("   Motion detected!")
            else:
                print("   No motion detected (timeout)")

        else:
            print("   Testing motion detection (simulated)...")
            for i in range(20):
                if sensor.is_motion_detected():
                    print(f"      Motion detected at check {i+1}")
                time.sleep(0.1)

        print("   ✅ Motion Sensor: PASS")
        return True

    except Exception as e:
        print(f"   ❌ Motion Sensor: FAIL - {e}")
        return False

    finally:
        sensor.close()


def test_integration(simulate=False):
    """Test components working together"""
    print("\n" + "=" * 50)
    print("5. INTEGRATION TEST")
    print("=" * 50)

    matrix = LEDMatrix(gpio_pin=18, simulate=simulate)
    audio = AudioSystem(simulate=simulate)
    camera = CameraSystem(simulate=simulate)

    try:
        print("   Starting integrated sequence...")

        # Show pattern and speak
        pattern = get_pattern('heart')
        palette = ColorPalette.LOVE
        matrix.show_pattern(pattern, palette)
        audio.speak("Integration test in progress!")
        time.sleep(2)

        # Start camera
        camera.start()
        frame = camera.capture_frame()

        if frame is not None:
            print(f"   Camera captured: {frame.shape}")

        # Change mood
        pattern = get_pattern('happy')
        palette = ColorPalette.HAPPY
        matrix.show_pattern(pattern, palette)
        audio.speak("All systems working together!")

        time.sleep(2)
        matrix.clear()

        print("   ✅ Integration Test: PASS")
        return True

    except Exception as e:
        print(f"   ❌ Integration Test: FAIL - {e}")
        return False

    finally:
        matrix.close()
        audio.close()
        camera.close()


def run_all_tests(simulate=False):
    """Run complete hardware validation suite"""
    print("\n" + "╔" + "=" * 48 + "╗")
    print("║  PIXEL PLANT - COMPLETE HARDWARE TEST SUITE  ║")
    print("╚" + "=" * 48 + "╝")

    if simulate:
        print("\n⚠️  SIMULATION MODE")
        print("For real hardware testing, use --real flag\n")
    else:
        print("\n⚡ REAL HARDWARE MODE")
        print("Testing actual Raspberry Pi hardware\n")

    results = {}

    # Run all tests
    results['LED Matrix'] = test_led_matrix(simulate)
    results['Audio System'] = test_audio_system(simulate)
    results['Camera System'] = test_camera_system(simulate)
    results['Motion Sensor'] = test_motion_sensor(simulate)
    results['Integration'] = test_integration(simulate)

    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)

    for component, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {component:20s} {status}")

    print("=" * 50)

    all_passed = all(results.values())

    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Hardware is ready!")
        print("You can now run the main application: python src/main.py")
    else:
        print("\n⚠️  Some tests failed. Please check hardware connections.")
        print("Refer to docs/hardware/troubleshooting.md for help.")

    return all_passed


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Test all Pixel Plant hardware components'
    )
    parser.add_argument(
        '--real',
        action='store_true',
        help='Test with real hardware (default: simulate)'
    )

    args = parser.parse_args()

    simulate = not args.real

    try:
        success = run_all_tests(simulate=simulate)
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
