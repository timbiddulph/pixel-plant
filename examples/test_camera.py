#!/usr/bin/env python3
"""
Camera System Hardware Test
Validates Pi Camera Module and image capture
"""

import sys
import time
from pathlib import Path
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from hardware import CameraSystem


def test_camera_initialization(camera):
    """Test camera initialization"""
    print("\n1. Testing camera initialization...")

    if camera.simulate:
        print("   ⚠️  Simulation mode - using mock frames")
    else:
        print("   ✓ Camera initialized successfully")

    print(f"   Resolution: {camera.resolution}")
    print(f"   Frame rate: {camera.framerate} FPS")
    print(f"   Rotation: {camera.rotation}°")

    print("   ✓ Initialization test complete")


def test_frame_capture(camera, num_frames=10):
    """Test basic frame capture"""
    print(f"\n2. Testing frame capture ({num_frames} frames)...")

    camera.start()
    time.sleep(0.5)  # Let camera warm up

    successful = 0
    failed = 0

    for i in range(num_frames):
        frame = camera.capture_frame()

        if frame is not None:
            successful += 1
            print(f"   Frame {i+1:2d}: ✓ {frame.shape} {frame.dtype}")
        else:
            failed += 1
            print(f"   Frame {i+1:2d}: ✗ Failed")

        time.sleep(0.1)

    print(f"\n   Success: {successful}/{num_frames}")
    print(f"   Failed:  {failed}/{num_frames}")

    if successful > 0:
        print("   ✓ Frame capture test complete")
    else:
        print("   ✗ Frame capture test failed!")

    return successful > 0


def test_frame_rate(camera, duration=5):
    """Test actual frame rate"""
    print(f"\n3. Testing frame rate ({duration}s capture)...")

    camera.start()
    time.sleep(0.5)

    frames_captured = 0
    start_time = time.time()

    while time.time() - start_time < duration:
        frame = camera.capture_frame()
        if frame is not None:
            frames_captured += 1

    elapsed = time.time() - start_time
    actual_fps = frames_captured / elapsed

    print(f"   Frames captured: {frames_captured}")
    print(f"   Duration: {elapsed:.2f}s")
    print(f"   Actual FPS: {actual_fps:.1f}")
    print(f"   Target FPS: {camera.framerate}")

    if actual_fps >= camera.framerate * 0.8:
        print(f"   ✓ Frame rate is acceptable ({actual_fps:.1f} FPS)")
    else:
        print(f"   ⚠️  Frame rate lower than expected")

    print("   ✓ Frame rate test complete")


def test_image_quality(camera):
    """Test image quality metrics"""
    print("\n4. Testing image quality...")

    camera.start()
    time.sleep(0.5)

    frame = camera.capture_frame()

    if frame is None:
        print("   ✗ Could not capture frame for quality test")
        return

    # Calculate basic metrics
    print(f"   Image shape: {frame.shape}")
    print(f"   Data type: {frame.dtype}")

    # Check if completely black or white
    mean_brightness = np.mean(frame)
    print(f"   Mean brightness: {mean_brightness:.1f} (0-255)")

    if mean_brightness < 10:
        print("   ⚠️  Image is very dark - check lens cap and lighting")
    elif mean_brightness > 245:
        print("   ⚠️  Image is overexposed - reduce lighting")
    else:
        print("   ✓ Brightness looks good")

    # Check color channels
    if len(frame.shape) == 3:
        r_mean = np.mean(frame[:,:,0])
        g_mean = np.mean(frame[:,:,1])
        b_mean = np.mean(frame[:,:,2])

        print(f"   Red channel: {r_mean:.1f}")
        print(f"   Green channel: {g_mean:.1f}")
        print(f"   Blue channel: {b_mean:.1f}")

        # Check for dead channels
        if r_mean < 5 or g_mean < 5 or b_mean < 5:
            print("   ⚠️  One or more color channels may be dead")
        else:
            print("   ✓ All color channels active")

    # Check for variation (not stuck pixels)
    std_dev = np.std(frame)
    print(f"   Standard deviation: {std_dev:.1f}")

    if std_dev < 5:
        print("   ⚠️  Very low variation - camera might be stuck or covered")
    else:
        print("   ✓ Good image variation")

    print("   ✓ Quality test complete")


def test_different_resolutions(camera):
    """Test different resolution settings"""
    print("\n5. Testing different resolutions...")

    if camera.simulate:
        print("   ⚠️  Resolution testing only works with real hardware")
        return

    resolutions = [
        (320, 240),
        (640, 480),
        (1280, 720),
    ]

    original_resolution = camera.resolution

    for width, height in resolutions:
        print(f"\n   Testing {width}x{height}...")

        try:
            # Create new camera with this resolution
            test_cam = CameraSystem(
                resolution=(width, height),
                framerate=camera.framerate,
                simulate=False
            )

            test_cam.start()
            time.sleep(0.5)

            frame = test_cam.capture_frame()

            if frame is not None:
                print(f"      ✓ Captured {frame.shape}")
            else:
                print(f"      ✗ Failed to capture")

            test_cam.close()

        except Exception as e:
            print(f"      ✗ Error: {e}")

    print(f"\n   Restoring original resolution: {original_resolution}")
    print("   ✓ Resolution test complete")


def test_rotation_settings(camera):
    """Test camera rotation"""
    print("\n6. Testing rotation settings...")

    rotations = [0, 90, 180, 270]

    for rotation in rotations:
        print(f"\n   Testing {rotation}° rotation...")

        try:
            test_cam = CameraSystem(
                resolution=camera.resolution,
                framerate=camera.framerate,
                rotation=rotation,
                simulate=camera.simulate
            )

            test_cam.start()
            time.sleep(0.3)

            frame = test_cam.capture_frame()

            if frame is not None:
                print(f"      ✓ Frame shape: {frame.shape}")

                # Check if dimensions swapped for 90/270
                if rotation in [90, 270]:
                    expected_swap = (camera.resolution[1], camera.resolution[0])
                    print(f"      Expected swap to: {expected_swap}")
            else:
                print(f"      ✗ Failed to capture")

            test_cam.close()

        except Exception as e:
            print(f"      ✗ Error: {e}")

    print("   ✓ Rotation test complete")


def test_save_sample_image(camera, output_path="test_capture.jpg"):
    """Save a sample image for visual inspection"""
    print(f"\n7. Saving sample image to {output_path}...")

    if camera.simulate:
        print("   ⚠️  Saving simulated frame (noise)")

    camera.start()
    time.sleep(0.5)

    frame = camera.capture_frame()

    if frame is None:
        print("   ✗ Could not capture frame")
        return

    try:
        # Try to save with opencv
        import cv2
        # Convert RGB to BGR for opencv
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, bgr_frame)
        print(f"   ✓ Image saved to {output_path}")
        print(f"   Open the file to verify image quality")

    except ImportError:
        print("   ⚠️  OpenCV not available, saving raw numpy array")
        np.save(output_path.replace('.jpg', '.npy'), frame)
        print(f"   ✓ Raw frame saved to {output_path.replace('.jpg', '.npy')}")


def run_full_test(simulate=False):
    """Run complete camera system test suite"""
    print("=" * 50)
    print("PIXEL PLANT - Camera System Hardware Test")
    print("=" * 50)

    if simulate:
        print("\n⚠️  Running in SIMULATION mode")
        print("Generating random test frames\n")
    else:
        print("\n⚡ REAL HARDWARE MODE")
        print("Testing actual Pi Camera Module\n")
        print("Hardware setup:")
        print("  - Pi Camera Module 2 (or compatible)")
        print("  - Connected via CSI ribbon cable")
        print("  - Camera interface enabled in raspi-config\n")
        print("⚠️  IMPORTANT: Remove lens cap if present!\n")

    # Initialize camera
    camera = CameraSystem(
        resolution=(640, 480),
        framerate=15,
        rotation=0,
        simulate=simulate
    )

    try:
        # Run tests
        test_camera_initialization(camera)

        success = test_frame_capture(camera, num_frames=10)

        if not success:
            print("\n❌ Frame capture failed - stopping tests")
            return

        test_frame_rate(camera, duration=5)
        test_image_quality(camera)

        if not simulate:
            test_different_resolutions(camera)
            test_rotation_settings(camera)

        test_save_sample_image(camera)

        print("\n" + "=" * 50)
        print("✅ ALL CAMERA TESTS PASSED")
        print("=" * 50)

        if not simulate:
            print("\nYour camera is working correctly!")
            print("Next steps:")
            print("  - Check test_capture.jpg for image quality")
            print("  - Adjust resolution in config/config.yaml if needed")
            print("  - Configure rotation if camera is mounted sideways")
            print("  - Test with full system: python src/main.py")

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")

    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

        print("\nTroubleshooting:")
        print("  1. Check camera is connected via CSI cable")
        print("  2. Enable camera: sudo raspi-config -> Interface Options -> Camera")
        print("  3. Check for camera: vcgencmd get_camera")
        print("  4. Test with raspistill: raspistill -o test.jpg")
        print("  5. Check /boot/config.txt has camera_auto_detect=1")
        print("  6. Remove lens cap!")

    finally:
        camera.close()
        print("\nTest complete. Camera closed.")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Test camera system hardware')
    parser.add_argument('--real', action='store_true',
                       help='Test with real hardware (default: simulate)')
    args = parser.parse_args()

    simulate = not args.real
    run_full_test(simulate=simulate)
