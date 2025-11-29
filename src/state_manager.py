"""
State Manager Module
Handles persistent state with auto-save and recovery
Designed for "always-on" operation with potential power loss
"""

import json
import logging
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class StateVersion(Enum):
    """State file version for migration support"""
    V1 = "1.0"
    CURRENT = V1


@dataclass
class PixelPlantState:
    """Core application state that needs persistence"""
    # Timestamps
    last_hydration_reminder: str  # ISO format
    last_movement_reminder: str
    last_seen: str  # Last time user was detected
    started_at: str  # When current session started

    # Current state
    current_mood: str
    concern_level: int
    is_sleeping: bool

    # Activity tracking
    sitting_start: Optional[str]  # ISO format or None
    total_sitting_seconds: float
    total_standing_seconds: float
    total_moving_seconds: float

    # Statistics
    reminders_sent_today: int
    hydration_count_today: int
    movement_count_today: int
    last_stats_reset: str  # Daily stats reset timestamp

    # Metadata
    version: str = StateVersion.CURRENT.value
    last_save: str = ""
    clean_shutdown: bool = False

    @classmethod
    def create_default(cls) -> 'PixelPlantState':
        """Create default state for first run"""
        now = datetime.now().isoformat()
        return cls(
            last_hydration_reminder=now,
            last_movement_reminder=now,
            last_seen=now,
            started_at=now,
            current_mood="content",
            concern_level=0,
            is_sleeping=False,
            sitting_start=None,
            total_sitting_seconds=0.0,
            total_standing_seconds=0.0,
            total_moving_seconds=0.0,
            reminders_sent_today=0,
            hydration_count_today=0,
            movement_count_today=0,
            last_stats_reset=now,
            clean_shutdown=False,
        )


class StateManager:
    """
    Manages persistent state with auto-save and recovery

    Features:
    - Auto-save on interval and on significant changes
    - Atomic writes to prevent corruption
    - State recovery after power loss
    - Thread-safe operations
    - Backup/restore capability
    """

    def __init__(self, data_directory: str, auto_save_interval: int = 60):
        """
        Initialize state manager

        Args:
            data_directory: Directory to store state files
            auto_save_interval: Seconds between auto-saves (default 60)
        """
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(parents=True, exist_ok=True)

        self.state_file = self.data_directory / 'pixel_plant_state.json'
        self.backup_file = self.data_directory / 'pixel_plant_state.backup.json'

        self.auto_save_interval = auto_save_interval
        self.state: PixelPlantState = PixelPlantState.create_default()

        # Thread safety
        self._lock = threading.Lock()
        self._dirty = False  # Track if state needs saving
        self._running = False
        self._auto_save_thread: Optional[threading.Thread] = None

        # Recovery info
        self.recovered_from_crash = False
        self.previous_uptime_seconds = 0.0

        # Load existing state
        self._load_state()

        logger.info("State manager initialized")

    def _load_state(self):
        """Load state from disk with recovery"""
        # Try loading primary state file
        state = self._try_load_file(self.state_file)

        # If primary failed, try backup
        if state is None and self.backup_file.exists():
            logger.warning("Primary state file corrupted, trying backup...")
            state = self._try_load_file(self.backup_file)
            if state:
                logger.info("Successfully recovered from backup")

        # Use loaded state or create new
        if state:
            self.state = state

            # Check if previous shutdown was clean
            if not self.state.clean_shutdown:
                self.recovered_from_crash = True
                started = datetime.fromisoformat(self.state.started_at)
                last_save = datetime.fromisoformat(self.state.last_save)
                self.previous_uptime_seconds = (last_save - started).total_seconds()

                logger.warning(
                    f"Recovered from unclean shutdown "
                    f"(uptime was {self.previous_uptime_seconds/3600:.1f} hours)"
                )
            else:
                logger.info("Loaded state from clean shutdown")

            # Reset for new session
            self.state.started_at = datetime.now().isoformat()
            self.state.clean_shutdown = False
            self._dirty = True
        else:
            logger.info("No previous state found, starting fresh")
            self.state = PixelPlantState.create_default()
            self._dirty = True

    def _try_load_file(self, file_path: Path) -> Optional[PixelPlantState]:
        """
        Attempt to load state from a file

        Args:
            file_path: Path to state file

        Returns:
            PixelPlantState if successful, None if failed
        """
        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Validate version
            version = data.get('version', '1.0')
            if version != StateVersion.CURRENT.value:
                logger.warning(f"State version {version} differs from current {StateVersion.CURRENT.value}")
                # Could add migration logic here

            # Create state from loaded data
            state = PixelPlantState(**data)
            logger.debug(f"Loaded state from {file_path.name}")
            return state

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {file_path.name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to load state from {file_path.name}: {e}")
            return None

    def save(self, force: bool = False):
        """
        Save current state to disk atomically

        Args:
            force: Force save even if not dirty
        """
        with self._lock:
            if not self._dirty and not force:
                return

            try:
                # Update metadata
                self.state.last_save = datetime.now().isoformat()

                # Convert to dict
                state_dict = asdict(self.state)

                # Write to temporary file first (atomic operation)
                temp_file = self.state_file.with_suffix('.tmp')
                with open(temp_file, 'w') as f:
                    json.dump(state_dict, f, indent=2)

                # Backup existing file before replacing
                if self.state_file.exists():
                    self.state_file.replace(self.backup_file)

                # Move temp file to primary location
                temp_file.replace(self.state_file)

                self._dirty = False
                logger.debug("State saved successfully")

            except Exception as e:
                logger.error(f"Failed to save state: {e}")

    def update(self, **kwargs):
        """
        Update state fields and mark as dirty

        Args:
            **kwargs: Field names and values to update
        """
        with self._lock:
            for key, value in kwargs.items():
                if hasattr(self.state, key):
                    setattr(self.state, key, value)
                    self._dirty = True
                else:
                    logger.warning(f"Unknown state field: {key}")

    def get(self, field: str) -> Any:
        """
        Get a state field value

        Args:
            field: Field name to retrieve

        Returns:
            Field value
        """
        with self._lock:
            return getattr(self.state, field, None)

    def get_state_dict(self) -> Dict[str, Any]:
        """Get complete state as dictionary"""
        with self._lock:
            return asdict(self.state)

    def start_auto_save(self):
        """Start background auto-save thread"""
        if self._running:
            logger.warning("Auto-save already running")
            return

        self._running = True
        self._auto_save_thread = threading.Thread(
            target=self._auto_save_loop,
            daemon=True,
            name="StateAutoSave"
        )
        self._auto_save_thread.start()
        logger.info(f"Auto-save started (interval: {self.auto_save_interval}s)")

    def stop_auto_save(self):
        """Stop background auto-save thread"""
        self._running = False
        if self._auto_save_thread:
            self._auto_save_thread.join(timeout=2.0)
        logger.info("Auto-save stopped")

    def _auto_save_loop(self):
        """Background thread that periodically saves state"""
        while self._running:
            time.sleep(self.auto_save_interval)
            if self._running:  # Check again after sleep
                self.save()

    def shutdown(self, clean: bool = True):
        """
        Prepare for shutdown

        Args:
            clean: Whether this is a clean shutdown
        """
        logger.info(f"Shutting down state manager ({'clean' if clean else 'unclean'})")

        # Stop auto-save
        self.stop_auto_save()

        # Mark shutdown status
        self.state.clean_shutdown = clean

        # Final save
        self.save(force=True)

    def reset_daily_stats(self):
        """Reset daily statistics (call at midnight)"""
        with self._lock:
            self.state.reminders_sent_today = 0
            self.state.hydration_count_today = 0
            self.state.movement_count_today = 0
            self.state.last_stats_reset = datetime.now().isoformat()
            self._dirty = True
        logger.info("Daily stats reset")

    def check_daily_reset(self):
        """Check if daily stats need to be reset"""
        last_reset = datetime.fromisoformat(self.state.last_stats_reset)
        now = datetime.now()

        # Reset if it's a new day
        if now.date() > last_reset.date():
            self.reset_daily_stats()
