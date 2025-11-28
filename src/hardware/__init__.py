"""
Hardware Abstraction Layer
Provides unified interface for all hardware components
"""

from .led_matrix import LEDMatrix
from .audio import AudioSystem
from .camera import CameraSystem
from .motion import MotionSensor

__all__ = ['LEDMatrix', 'AudioSystem', 'CameraSystem', 'MotionSensor']
