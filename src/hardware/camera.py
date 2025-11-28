"""
Camera System Hardware Abstraction
Pi Camera for behavioral monitoring
"""

import logging
import numpy as np
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class CameraSystem:
    """Pi Camera interface for pose detection"""

    def __init__(self, resolution: Tuple[int, int] = (640, 480),
                 framerate: int = 15, rotation: int = 0,
                 simulate: bool = False):
        """
        Initialize camera system

        Args:
            resolution: (width, height) tuple
            framerate: Target frames per second
            rotation: Camera rotation (0, 90, 180, 270)
            simulate: If True, generate dummy frames
        """
        self.resolution = resolution
        self.framerate = framerate
        self.rotation = rotation
        self.simulate = simulate
        self.camera = None
        self.is_capturing = False

        if not simulate:
            try:
                from picamera2 import Picamera2
                self.Picamera2 = Picamera2
                self.camera = Picamera2()

                # Configure camera
                config = self.camera.create_still_configuration(
                    main={"size": resolution, "format": "RGB888"}
                )
                self.camera.configure(config)

                logger.info(f"Camera initialized: {resolution} @ {framerate}fps")

            except ImportError:
                logger.warning("Picamera2 not available, falling back to simulation")
                self.simulate = True
            except Exception as e:
                logger.error(f"Camera initialization failed: {e}")
                self.simulate = True
        else:
            logger.info("Camera system running in simulation mode")

    def start(self):
        """Start camera capture"""
        if self.simulate:
            self.is_capturing = True
            logger.info("Camera simulation started")
            return

        try:
            self.camera.start()
            self.is_capturing = True
            logger.info("Camera capture started")
        except Exception as e:
            logger.error(f"Failed to start camera: {e}")
            self.is_capturing = False

    def stop(self):
        """Stop camera capture"""
        if self.simulate:
            self.is_capturing = False
            return

        try:
            if self.camera:
                self.camera.stop()
            self.is_capturing = False
            logger.info("Camera capture stopped")
        except Exception as e:
            logger.error(f"Failed to stop camera: {e}")

    def capture_frame(self) -> Optional[np.ndarray]:
        """
        Capture a single frame

        Returns:
            NumPy array (H, W, 3) in RGB format, or None on error
        """
        if not self.is_capturing:
            return None

        if self.simulate:
            # Generate dummy frame for testing
            height, width = self.resolution[1], self.resolution[0]
            frame = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
            return frame

        try:
            frame = self.camera.capture_array()

            # Apply rotation if needed
            if self.rotation == 90:
                frame = np.rot90(frame, k=1)
            elif self.rotation == 180:
                frame = np.rot90(frame, k=2)
            elif self.rotation == 270:
                frame = np.rot90(frame, k=3)

            return frame

        except Exception as e:
            logger.error(f"Frame capture error: {e}")
            return None

    def get_frame_size(self) -> Tuple[int, int]:
        """Get current frame size (width, height)"""
        if self.rotation in [90, 270]:
            # Rotated: swap width and height
            return (self.resolution[1], self.resolution[0])
        return self.resolution

    def close(self):
        """Clean up camera resources"""
        self.stop()
        if self.camera:
            try:
                self.camera.close()
            except:
                pass
        logger.info("Camera system closed")


if __name__ == '__main__':
    """Test camera system"""
    logging.basicConfig(level=logging.INFO)

    camera = CameraSystem(simulate=True)
    camera.start()

    # Capture a few test frames
    for i in range(3):
        frame = camera.capture_frame()
        if frame is not None:
            print(f"Frame {i+1}: shape={frame.shape}, dtype={frame.dtype}")

    camera.close()
