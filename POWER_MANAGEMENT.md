# Power Management & State Persistence

## Overview

The Pixel Plant is designed for **always-on operation** - meant to be plugged in continuously without manual shutdowns. This document describes the robust power management and state persistence systems that make this possible.

## Core Design Principles

1. **Expect Power Loss** - The system may lose power unexpectedly at any time
2. **Auto-Save Everything** - All important state is saved automatically and frequently
3. **Graceful Recovery** - System recovers cleanly from crashes and power loss
4. **Low Power Sleep** - Progressive power reduction during inactivity
5. **PIR Wake** - Motion detection wakes the system from sleep

---

## State Persistence

### What Gets Saved

The state manager ([src/state_manager.py:1](src/state_manager.py#L1)) automatically persists:

**Timestamps:**
- Last hydration reminder
- Last movement reminder
- Last time user was detected
- Session start time

**Current State:**
- Current mood (happy, concerned, worried, etc.)
- Concern escalation level
- Sleep state

**Activity Tracking:**
- When sitting session started
- Total sitting/standing/moving time
- Daily reminder statistics

**Metadata:**
- State file version (for migrations)
- Last save timestamp
- Clean vs unclean shutdown flag

### Auto-Save Strategy

State is saved automatically:

1. **On Interval** - Every 60 seconds (configurable)
2. **On Important Events** - When reminders are sent
3. **On State Changes** - When mood or power state changes
4. **On Shutdown** - Final save before exit

### Atomic Writes

State saves use atomic write operations:

```
1. Write to temporary file (.tmp)
2. Backup existing state to .backup file
3. Rename temp file to primary state file
```

This ensures the state file is never corrupted, even if power is lost mid-write.

### Recovery After Power Loss

On startup, the system:

1. **Loads previous state** from disk
2. **Checks shutdown flag** - Was previous shutdown clean?
3. **Calculates uptime** - How long was previous session?
4. **Restores timestamps** - Continues from last known state
5. **Logs recovery info** - Alerts about unexpected shutdown

Example log output:
```
⚠️  Recovered from unclean shutdown (previous uptime: 14.3 hours)
```

---

## Power Management

### Power States

The power manager ([src/power_manager.py:1](src/power_manager.py#L1)) implements four progressive power states:

#### 1. ACTIVE
- **Full operation** - All systems running
- **Camera active** - Pose detection running
- **LED display** - Showing mood/expressions
- **Audio enabled** - Can speak reminders
- **Frame rate** - Full speed (15 FPS)

#### 2. IDLE (after 5 minutes of inactivity)
- **Reduced activity** - Still monitoring
- **Camera active** - Lower frame rate
- **LED dimmed** - Subtle breathing effect
- **Audio enabled** - Can still remind
- **Purpose** - Reduce power while staying responsive

#### 3. LIGHT_SLEEP (after 15 minutes)
- **LED off** - No display
- **Camera off** - Not analyzing frames
- **PIR monitoring** - Checking for motion every 1 second
- **Audio ready** - Can wake and speak
- **Power savings** - Significant reduction

#### 4. DEEP_SLEEP (after 60 minutes)
- **Everything off** - Except PIR sensor
- **PIR monitoring** - Checking for motion
- **Minimal processing** - Lowest power consumption
- **Maximum savings** - Can run for days

### Transition Logic

```
User Active
    ↓ (5 min idle)
IDLE State
    ↓ (15 min total)
LIGHT_SLEEP State
    ↓ (60 min total)
DEEP_SLEEP State
    ↑ (PIR motion)
ACTIVE State (wake up!)
```

### PIR Wake Mechanism

When in sleep mode:

1. **PIR checked every 1 second** (configurable)
2. **Motion detected** → Immediate wake
3. **Wake callbacks executed** - Camera restart, LED on, etc.
4. **Greeting played** - "Hello! I see you're back!"
5. **State saved** - Record wake event

### Configuration

Edit [config/config.yaml:39](config/config.yaml#L39):

```yaml
power_management:
  enabled: true

  # Progressive sleep timeouts (minutes of inactivity)
  idle_timeout_minutes: 5        # Reduce activity
  light_sleep_timeout_minutes: 15  # LED off, camera off
  deep_sleep_timeout_minutes: 60   # Minimal power

  # PIR wake settings
  pir_wake_enabled: true
  pir_check_interval_seconds: 1.0

  # State persistence
  auto_save_interval_seconds: 60
  save_on_state_change: true
```

---

## Implementation Details

### State Manager Architecture

```python
from state_manager import StateManager

# Initialize (loads previous state if exists)
state = StateManager(
    data_directory="/home/pi/.pixel-plant",
    auto_save_interval=60  # seconds
)

# Start background auto-save thread
state.start_auto_save()

# Update state (marks dirty for next save)
state.update(
    last_hydration_reminder=datetime.now().isoformat(),
    concern_level=3
)

# Manual save (force immediate)
state.save(force=True)

# Clean shutdown
state.shutdown(clean=True)
```

### Power Manager Architecture

```python
from power_manager import PowerManager, PowerState

# Initialize with timeouts
power = PowerManager(
    idle_timeout_minutes=5,
    light_sleep_timeout_minutes=15,
    deep_sleep_timeout_minutes=60
)

# Register PIR sensor
power.register_pir_sensor(pir.is_motion_detected)

# Register callbacks
power.register_sleep_callback(on_sleep_handler)
power.register_wake_callback(on_wake_handler)

# Start monitoring thread
power.start_monitoring()

# Report user activity (resets timers)
power.report_activity()

# Check current state
if power.current_state == PowerState.LIGHT_SLEEP:
    # In sleep mode
    pass
```

### Integration Pattern

See [src/main_with_power_management.py:1](src/main_with_power_management.py#L1) for complete integration:

```python
class PixelPlant:
    def __init__(self):
        # Initialize state manager (loads previous state)
        self.state_manager = StateManager(...)

        # Check if recovering from crash
        if self.state_manager.recovered_from_crash:
            logger.warning("Recovered from unclean shutdown")

        # Initialize power manager
        self.power_manager = PowerManager(...)

        # Register callbacks
        self.power_manager.register_sleep_callback(self._on_sleep)
        self.power_manager.register_wake_callback(self._on_wake)

    def _on_sleep(self, sleep_state):
        """Called when entering sleep"""
        self.led.clear()
        self._save_current_state()

    def _on_wake(self):
        """Called when waking from sleep"""
        self.audio.speak("Hello! I see you're back!")
        self._save_current_state()
```

---

## File Locations

### State Files

All state files are stored in the data directory (`/home/pi/.pixel-plant`):

```
/home/pi/.pixel-plant/
├── pixel_plant_state.json        # Primary state file
├── pixel_plant_state.backup.json # Backup (previous save)
├── behavior_patterns.json         # Learning data (from PatternLearner)
└── pixel_plant_state.tmp          # Temporary file during save
```

### State File Format

Example `pixel_plant_state.json`:

```json
{
  "last_hydration_reminder": "2024-12-01T14:30:00",
  "last_movement_reminder": "2024-12-01T14:15:00",
  "last_seen": "2024-12-01T14:45:00",
  "started_at": "2024-12-01T08:00:00",
  "current_mood": "content",
  "concern_level": 2,
  "is_sleeping": false,
  "sitting_start": "2024-12-01T14:00:00",
  "total_sitting_seconds": 18450.0,
  "total_standing_seconds": 3200.0,
  "total_moving_seconds": 1250.0,
  "reminders_sent_today": 8,
  "hydration_count_today": 4,
  "movement_count_today": 4,
  "last_stats_reset": "2024-12-01T00:00:00",
  "version": "1.0",
  "last_save": "2024-12-01T14:45:30",
  "clean_shutdown": false
}
```

---

## Power Consumption Estimates

Estimated power consumption by state (Raspberry Pi Zero 2 W):

| State | Camera | LED | Audio | PIR | Total (est) |
|-------|--------|-----|-------|-----|-------------|
| ACTIVE | 250mA | 200mA | 50mA | 10mA | ~510mA (~2.5W) |
| IDLE | 150mA | 100mA | 20mA | 10mA | ~280mA (~1.4W) |
| LIGHT_SLEEP | 0mA | 0mA | 0mA | 10mA | ~100mA (~0.5W) |
| DEEP_SLEEP | 0mA | 0mA | 0mA | 10mA | ~80mA (~0.4W) |

**Notes:**
- LED power varies with brightness and pattern
- Pi Zero 2 W base consumption: ~80-100mA
- Actual measurements will vary

### Daily Power Usage Example

Assuming typical usage pattern:
- 8 hours ACTIVE (work day)
- 2 hours IDLE (breaks, lunch)
- 6 hours LIGHT_SLEEP (evening)
- 8 hours DEEP_SLEEP (night)

**Daily energy:** ~30 Wh (~0.03 kWh)
**Monthly energy:** ~0.9 kWh
**Annual cost:** ~£1.50 at UK electricity rates

---

## Testing & Validation

### Test State Persistence

```bash
# Start the system
python src/main_with_power_management.py

# Let it run for a few minutes, then kill power
# (simulate unexpected shutdown)
sudo poweroff -f

# Restart and check logs
python src/main_with_power_management.py

# Should see: "Recovered from unclean shutdown"
```

### Test Power States

```bash
# Enable debug logging to see state transitions
# Edit config.yaml: log_level: 'DEBUG'

# Run and watch for state changes
python src/main_with_power_management.py

# Logs should show:
# "Entering idle from active" (after 5 min)
# "Entering light_sleep from idle" (after 15 min)
# "PIR motion detected, waking up" (when you move)
```

### Test PIR Wake

```bash
# Let system enter LIGHT_SLEEP (15 min idle)
# Wave hand in front of PIR sensor
# Should immediately wake and greet

# Check logs:
# "PIR motion detected, waking up"
# "Waking from light_sleep (wake #1)"
# "Greeted user: 'Hello! I see you're back!'"
```

---

## Migration from Original main.py

The enhanced version is backward compatible. To migrate:

### Option 1: Replace main.py

```bash
cd ~/pixel-plant/src
cp main.py main_original.py  # Backup
cp main_with_power_management.py main.py
```

### Option 2: Use new main directly

```bash
# Update systemd service
sudo nano /etc/systemd/system/pixel-plant.service

# Change ExecStart to:
ExecStart=/home/pi/pixel-plant/venv/bin/python /home/pi/pixel-plant/src/main_with_power_management.py

sudo systemctl daemon-reload
sudo systemctl restart pixel-plant
```

### Configuration Update

Add power management section to [config/config.yaml:39](config/config.yaml#L39) (already done in this version).

---

## Troubleshooting

### State File Corruption

**Symptom:** "JSON decode error" on startup

**Solution:** The system automatically falls back to backup:
```
WARNING - Primary state file corrupted, trying backup...
INFO - Successfully recovered from backup
```

If both files are corrupted:
```bash
# Remove state files to start fresh
rm ~/.pixel-plant/pixel_plant_state*.json

# System will create new default state
python src/main_with_power_management.py
```

### Power Manager Not Working

**Symptom:** System never enters sleep

**Check:**
1. Config enabled: `power_management.enabled: true`
2. Logs show: "Power monitoring started"
3. No continuous activity preventing sleep

**Debug:**
```python
# Check power state info
power_info = power_manager.get_state_info()
print(power_info)
# {'state': 'active', 'idle_seconds': 120, ...}
```

### PIR Wake Not Working

**Symptom:** System stays in sleep, doesn't wake on motion

**Check:**
1. PIR enabled: `pir_wake_enabled: true`
2. PIR sensor working: `python examples/test_pir.py --real`
3. Logs show: "PIR sensor registered with power manager"

**Debug:**
```bash
# Enable debug logging
# Edit config.yaml: log_level: 'DEBUG'

# Should see:
# "Checking PIR for wake..."
# "PIR motion detected, waking up"
```

---

## Best Practices

### Always-On Operation

1. **Use quality power supply** - 5V 2.5A minimum
2. **Enable power management** - Reduces wear and power consumption
3. **Monitor logs** - Watch for unexpected shutdowns
4. **SD card quality** - Use high-quality card for frequent writes
5. **Log rotation** - Prevent log file from filling SD card

### State Management

1. **Don't edit state files manually** - Let the system manage them
2. **Backup data directory** - Periodically backup `~/.pixel-plant/`
3. **Check recovery logs** - Monitor for frequent unclean shutdowns
4. **Increase auto-save interval** - If SD card wear is a concern (trade-off: data loss)

### Power Optimization

1. **Adjust timeouts** - Tune based on your usage pattern
2. **Use deep sleep** - If leaving for extended periods
3. **LED brightness** - Lower brightness saves power
4. **Camera resolution** - Lower resolution uses less processing

---

## Future Enhancements

Possible additions:

1. **Systemd Watchdog** - Auto-restart if system hangs
2. **Battery Backup** - UPS support for graceful shutdown
3. **Remote Monitoring** - Web dashboard showing power state
4. **Wake Schedule** - Auto-wake at specific times
5. **Power Metrics** - Track and log power consumption
6. **SD Card Health** - Monitor write cycles and health

---

## Summary

The enhanced Pixel Plant system is designed for **true always-on operation**:

✅ **Auto-saves state every 60 seconds**
✅ **Recovers gracefully from power loss**
✅ **Progressive power reduction during inactivity**
✅ **PIR motion wake from sleep**
✅ **Atomic writes prevent corruption**
✅ **Clean shutdown detection**
✅ **Comprehensive logging**

**Result:** A reliable desktop companion that can be plugged in and left running indefinitely, surviving power outages and unexpected shutdowns without losing state or requiring manual intervention.

---

*"Built to run forever, designed to care always."* 🌿⚡
