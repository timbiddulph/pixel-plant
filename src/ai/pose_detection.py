"""
Pose Detection Module
Uses MediaPipe for real-time pose estimation
Detects sitting, standing, and movement patterns
"""

import logging
import numpy as np
from typing import Optional, Tuple, Dict
from enum import Enum

logger = logging.getLogger(__name__)


class PostureType(Enum):
    """Detected posture types"""
    UNKNOWN = "unknown"
    SITTING = "sitting"
    STANDING = "standing"
    LEANING_FORWARD = "leaning_forward"  # Poor posture
    ABSENT = "absent"  # No person detected


class PoseDetector:
    """MediaPipe-based pose detection"""

    def __init__(self, confidence_threshold: float = 0.7,
                 simulate: bool = False):
        """
        Initialize pose detector

        Args:
            confidence_threshold: Minimum confidence for detections
            simulate: Use simulated detections for testing
        """
        self.confidence_threshold = confidence_threshold
        self.simulate = simulate
        self.mp_pose = None
        self.pose = None

        # Simulation state
        self._sim_frame_count = 0
        self._sim_posture = PostureType.SITTING

        if not simulate:
            self._init_mediapipe()
        else:
            logger.info("Pose detector running in simulation mode")

    def _init_mediapipe(self):
        """Initialize MediaPipe Pose"""
        try:
            import mediapipe as mp

            self.mp_pose = mp.solutions.pose
            self.pose = self.mp_pose.Pose(
                min_detection_confidence=self.confidence_threshold,
                min_tracking_confidence=self.confidence_threshold,
                model_complexity=0,  # Lite model for Pi Zero 2 W
                enable_segmentation=False,  # Disable to save processing
            )

            logger.info("MediaPipe Pose initialized successfully")

        except ImportError:
            logger.warning("MediaPipe not available, falling back to simulation")
            self.simulate = True

        except Exception as e:
            logger.error(f"Failed to initialize MediaPipe: {e}")
            self.simulate = True

    def detect_posture(self, frame: np.ndarray) -> Tuple[PostureType, float, Optional[Dict]]:
        """
        Detect posture from camera frame

        Args:
            frame: RGB image from camera (H, W, 3)

        Returns:
            Tuple of (posture, confidence, landmarks_dict)
            - posture: Detected PostureType
            - confidence: Detection confidence (0-1)
            - landmarks_dict: Key body landmarks or None
        """
        if self.simulate:
            return self._simulate_detection()

        if frame is None or self.pose is None:
            return PostureType.UNKNOWN, 0.0, None

        try:
            # Process frame with MediaPipe
            results = self.pose.process(frame)

            if not results.pose_landmarks:
                # No person detected
                return PostureType.ABSENT, 0.0, None

            # Extract key landmarks
            landmarks = self._extract_landmarks(results.pose_landmarks)

            # Analyze posture
            posture, confidence = self._analyze_posture(landmarks)

            return posture, confidence, landmarks

        except Exception as e:
            logger.error(f"Pose detection error: {e}")
            return PostureType.UNKNOWN, 0.0, None

    def _simulate_detection(self) -> Tuple[PostureType, float, Optional[Dict]]:
        """Simulate pose detection for testing"""
        self._sim_frame_count += 1

        # Change posture every 100 frames (simulated)
        if self._sim_frame_count % 100 == 0:
            postures = [PostureType.SITTING, PostureType.STANDING, PostureType.LEANING_FORWARD]
            import random
            self._sim_posture = random.choice(postures)

        # Simulate confidence
        confidence = 0.85 + (np.random.random() * 0.15)  # 0.85-1.0

        # Simulate landmarks
        mock_landmarks = {
            'nose_y': 0.3,
            'shoulder_y': 0.4,
            'hip_y': 0.6,
            'torso_angle': 15.0 if self._sim_posture == PostureType.LEANING_FORWARD else 5.0
        }

        return self._sim_posture, confidence, mock_landmarks

    def _extract_landmarks(self, pose_landmarks) -> Dict:
        """
        Extract key landmarks from MediaPipe results

        Args:
            pose_landmarks: MediaPipe pose landmarks

        Returns:
            Dictionary of key points and measurements
        """
        landmarks = {}

        # Get landmark indices (MediaPipe standard)
        NOSE = 0
        LEFT_SHOULDER = 11
        RIGHT_SHOULDER = 12
        LEFT_HIP = 23
        RIGHT_HIP = 24

        lm = pose_landmarks.landmark

        # Y coordinates (0=top, 1=bottom)
        landmarks['nose_y'] = lm[NOSE].y
        landmarks['left_shoulder_y'] = lm[LEFT_SHOULDER].y
        landmarks['right_shoulder_y'] = lm[RIGHT_SHOULDER].y
        landmarks['left_hip_y'] = lm[LEFT_HIP].y
        landmarks['right_hip_y'] = lm[RIGHT_HIP].y

        # Average positions
        landmarks['shoulder_y'] = (lm[LEFT_SHOULDER].y + lm[RIGHT_SHOULDER].y) / 2
        landmarks['hip_y'] = (lm[LEFT_HIP].y + lm[RIGHT_HIP].y) / 2

        # Calculate torso angle (forward lean)
        shoulder_x = (lm[LEFT_SHOULDER].x + lm[RIGHT_SHOULDER].x) / 2
        hip_x = (lm[LEFT_HIP].x + lm[RIGHT_HIP].x) / 2
        shoulder_y = landmarks['shoulder_y']
        hip_y = landmarks['hip_y']

        # Angle from vertical
        dx = shoulder_x - hip_x
        dy = shoulder_y - hip_y
        landmarks['torso_angle'] = np.degrees(np.arctan2(dx, abs(dy)))

        # Visibility scores (average)
        landmarks['visibility'] = np.mean([
            lm[NOSE].visibility,
            lm[LEFT_SHOULDER].visibility,
            lm[RIGHT_SHOULDER].visibility,
            lm[LEFT_HIP].visibility,
            lm[RIGHT_HIP].visibility,
        ])

        return landmarks

    def _analyze_posture(self, landmarks: Dict) -> Tuple[PostureType, float]:
        """
        Analyze landmarks to determine posture

        Args:
            landmarks: Extracted landmark dictionary

        Returns:
            Tuple of (posture, confidence)
        """
        # Check visibility
        if landmarks.get('visibility', 0) < 0.5:
            return PostureType.UNKNOWN, 0.0

        nose_y = landmarks['nose_y']
        shoulder_y = landmarks['shoulder_y']
        hip_y = landmarks['hip_y']
        torso_angle = landmarks['torso_angle']

        # Thresholds (tunable based on camera setup)
        SITTING_THRESHOLD = 0.5  # Hip should be in lower half of frame
        FORWARD_LEAN_THRESHOLD = 20.0  # degrees from vertical

        confidence = landmarks['visibility']

        # Check for poor posture (leaning forward)
        if abs(torso_angle) > FORWARD_LEAN_THRESHOLD:
            return PostureType.LEANING_FORWARD, confidence

        # Determine sitting vs standing based on body position in frame
        # When sitting, body (especially hips) will be in lower portion of frame
        # When standing, body will be more centered/higher

        if hip_y > SITTING_THRESHOLD:
            # Hips in lower portion = sitting
            return PostureType.SITTING, confidence
        else:
            # Hips higher = standing
            return PostureType.STANDING, confidence

    def calibrate(self, frames: list) -> Dict:
        """
        Calibrate detector based on user's typical positions

        Args:
            frames: List of sample frames showing sitting and standing

        Returns:
            Calibration parameters
        """
        logger.info(f"Calibrating with {len(frames)} sample frames...")

        sitting_samples = []
        standing_samples = []

        for i, frame in enumerate(frames):
            posture, confidence, landmarks = self.detect_posture(frame)

            if confidence < self.confidence_threshold:
                continue

            # Assume first half are sitting, second half standing
            if i < len(frames) // 2:
                sitting_samples.append(landmarks)
            else:
                standing_samples.append(landmarks)

        # Calculate calibration thresholds
        calibration = {
            'sitting_hip_y_mean': np.mean([s['hip_y'] for s in sitting_samples]) if sitting_samples else 0.6,
            'standing_hip_y_mean': np.mean([s['hip_y'] for s in standing_samples]) if standing_samples else 0.4,
            'samples_collected': len(sitting_samples) + len(standing_samples),
        }

        logger.info(f"Calibration complete: {calibration}")

        return calibration

    def close(self):
        """Clean up resources"""
        if self.pose:
            try:
                self.pose.close()
            except:
                pass
        logger.info("Pose detector closed")


if __name__ == '__main__':
    """Test pose detector"""
    logging.basicConfig(level=logging.INFO)

    # Test with simulation
    detector = PoseDetector(simulate=True)

    print("=== POSE DETECTOR TEST ===\n")

    # Test detections
    for i in range(10):
        # Simulate frame
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

        posture, confidence, landmarks = detector.detect_posture(frame)

        print(f"Frame {i+1:2d}: {posture.value:15s} (confidence: {confidence:.2f})")

        if landmarks:
            print(f"          Torso angle: {landmarks['torso_angle']:.1f}°")

    detector.close()
    print("\n✅ Pose detector test complete")
