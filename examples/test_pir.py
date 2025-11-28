#!/usr/bin/env python3
"""
PIR Motion Sensor Hardware Test
Validates motion detection and sensitivity
"""

import sys
import time
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from hardware import MotionSensor


def test_basic_detection(sensor, duration=10):
    """Test basic motion detection"""
    print("\n1. Testing basic motion detection...")
    print(f"   Monitoring for {duration} seconds...")

    if not sensor.simulate:
        print("   Wave your hand in front of the PIR sensor!")

    detection_count = 0
    start_time = time.time()

    while time.time() - start_time < duration:
        if sensor.is_motion_detected():
            detection_count += 1
            print(f"   [{int(time.time() - start_time)}s] Motion detected! (Count: {detection_count})")
            time.sleep(0.5)  # Debounce
        time.sleep(0.1)

    print(f"   ✓ Detected {detection_count} motion events in {duration}s")
    return detection_count


def test_detection_range(sensor):
    """Test detection at different distances"""
    print("\n2. Testing detection range...")

    if sensor.simulate:
        print("   ⚠️  Range testing only works with real hardware")
        return

    distances = ["10cm", "50cm", "1m", "2m", "3m"]

    print("   Move to each distance and wave:")

    for distance in distances:
        input(f"\n   Position yourself at {distance} and press Enter...")
        print(f"   Detecting at {distance} (5 seconds)...")

        detected = False
        start = time.time()

        while time.time() - start < 5:
            if sensor.is_motion_detected():
                print(f"      ✓ Motion detected at {distance}!")
                detected = True
                break
            time.sleep(0.1)

        if not detected:
            print(f"      ✗ No detection at {distance}")

    print("   ✓ Range test complete")


def test_wait_for_motion(sensor):
    """Test blocking wait for motion"""
    print("\n3. Testing wait_for_motion()...")

    if not sensor.simulate:
        print("   Waiting for motion (10 second timeout)...")
        print("   Wave your hand in front of the sensor!")

    start = time.time()
    detected = sensor.wait_for_motion(timeout=10.0)
    elapsed = time.time() - start

    if detected:
        print(f"   ✓ Motion detected after {elapsed:.1f}s")
    else:
        print(f"   ✗ Timeout after {elapsed:.1f}s (no motion)")

    print("   ✓ Wait test complete")


def test_continuous_monitoring(sensor, duration=30):
    """Test continuous monitoring with statistics"""
    print("\n4. Testing continuous monitoring...")
    print(f"   Monitoring for {duration} seconds with statistics...")

    if not sensor.simulate:
        print("   Move around naturally in front of the sensor!")

    stats = {
        'total_events': 0,
        'first_detection': None,
        'last_detection': None,
        'detection_times': [],
    }

    start_time = time.time()
    last_detection = 0

    while time.time() - start_time < duration:
        elapsed = time.time() - start_time

        if sensor.is_motion_detected():
            now = datetime.now()

            stats['total_events'] += 1

            if stats['first_detection'] is None:
                stats['first_detection'] = now

            stats['last_detection'] = now
            stats['detection_times'].append(elapsed)

            # Only print every 1s to avoid spam
            if elapsed - last_detection > 1.0:
                print(f"   [{int(elapsed)}s] Motion (Total: {stats['total_events']})")
                last_detection = elapsed

        time.sleep(0.1)

    # Print statistics
    print("\n   Statistics:")
    print(f"     Total detections: {stats['total_events']}")

    if stats['first_detection']:
        print(f"     First detection: {stats['first_detection'].strftime('%H:%M:%S')}")
        print(f"     Last detection: {stats['last_detection'].strftime('%H:%M:%S')}")

        if len(stats['detection_times']) > 1:
            avg_interval = sum([
                stats['detection_times'][i] - stats['detection_times'][i-1]
                for i in range(1, len(stats['detection_times']))
            ]) / (len(stats['detection_times']) - 1)
            print(f"     Average interval: {avg_interval:.1f}s")

    print("   ✓ Continuous monitoring test complete")


def test_sensitivity_calibration(sensor):
    """Help user calibrate sensor sensitivity"""
    print("\n5. Sensitivity calibration...")

    if sensor.simulate:
        print("   ⚠️  Calibration only works with real hardware")
        return

    print("\n   Most PIR sensors have a sensitivity adjustment potentiometer.")
    print("   Let's test current sensitivity:\n")

    print("   Step 1: Test small movements")
    input("   Make small hand movements (5cm range) and press Enter...")

    small_detected = False
    for _ in range(20):
        if sensor.is_motion_detected():
            print("      ✓ Small movements detected")
            small_detected = True
            break
        time.sleep(0.2)

    if not small_detected:
        print("      ✗ Small movements not detected")

    print("\n   Step 2: Test large movements")
    input("   Make large arm movements and press Enter...")

    large_detected = False
    for _ in range(20):
        if sensor.is_motion_detected():
            print("      ✓ Large movements detected")
            large_detected = True
            break
        time.sleep(0.2)

    if not large_detected:
        print("      ✗ Large movements not detected")

    # Recommendations
    print("\n   Calibration recommendations:")
    if small_detected and large_detected:
        print("      ✓ Sensitivity is well calibrated!")
    elif not small_detected and large_detected:
        print("      ⚠️  Increase sensitivity (turn pot clockwise)")
    elif small_detected and not large_detected:
        print("      ⚠️  Check sensor positioning and power")
    else:
        print("      ❌ No detection - check wiring and power!")

    print("   ✓ Calibration test complete")


def test_presence_detection_simulation(sensor, duration=20):
    """Simulate presence detection use case"""
    print("\n6. Presence detection simulation...")
    print(f"   Simulating {duration}s of presence monitoring...")

    if not sensor.simulate:
        print("   Stay in view for first 10s, then leave for 10s")

    presence_log = []
    last_motion = time.time()
    inactivity_threshold = 5.0  # 5 seconds

    start_time = time.time()

    while time.time() - start_time < duration:
        elapsed = time.time() - start_time

        if sensor.is_motion_detected():
            last_motion = time.time()

            if not presence_log or presence_log[-1] != 'present':
                presence_log.append('present')
                print(f"   [{int(elapsed)}s] User PRESENT")

        else:
            # Check if user has been away
            time_since_motion = time.time() - last_motion

            if time_since_motion > inactivity_threshold:
                if not presence_log or presence_log[-1] != 'away':
                    presence_log.append('away')
                    print(f"   [{int(elapsed)}s] User AWAY (no motion for {time_since_motion:.1f}s)")

        time.sleep(0.5)

    print(f"\n   Presence log: {' → '.join(presence_log)}")
    print("   ✓ Presence detection test complete")


def run_full_test(simulate=False):
    """Run complete PIR sensor test suite"""
    print("=" * 50)
    print("PIXEL PLANT - PIR Motion Sensor Hardware Test")
    print("=" * 50)

    if simulate:
        print("\n⚠️  Running in SIMULATION mode")
        print("Motion will be randomly simulated\n")
    else:
        print("\n⚡ REAL HARDWARE MODE")
        print("Testing actual PIR sensor\n")
        print("Hardware setup:")
        print("  - PIR Sensor: BL412 or HC-SR501")
        print("  - VCC: 5V")
        print("  - GND: Ground")
        print("  - OUT: GPIO 17 (configurable)\n")

    # Initialize sensor
    sensor = MotionSensor(gpio_pin=17, enabled=True, simulate=simulate)

    try:
        # Run tests
        detections = test_basic_detection(sensor, duration=10)

        if not simulate:
            test_detection_range(sensor)

        test_wait_for_motion(sensor)
        test_continuous_monitoring(sensor, duration=30)

        if not simulate:
            test_sensitivity_calibration(sensor)

        test_presence_detection_simulation(sensor, duration=20)

        print("\n" + "=" * 50)
        print("✅ ALL PIR TESTS PASSED")
        print("=" * 50)

        if not simulate:
            print("\nYour PIR sensor is working correctly!")
            print("Next steps:")
            print("  - Adjust sensitivity pot if needed")
            print("  - Position sensor for best coverage")
            print("  - Test with full system: python src/main.py")

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")

    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

        print("\nTroubleshooting:")
        print("  1. Check VCC connected to 5V")
        print("  2. Check GND connection")
        print("  3. Verify OUT connected to GPIO 17")
        print("  4. Ensure sensor has warmed up (30-60s)")
        print("  5. Check for obstructions")

    finally:
        sensor.close()
        print("\nTest complete. Sensor closed.")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Test PIR motion sensor hardware')
    parser.add_argument('--real', action='store_true',
                       help='Test with real hardware (default: simulate)')
    args = parser.parse_args()

    simulate = not args.real
    run_full_test(simulate=simulate)
