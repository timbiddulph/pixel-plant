# Pixel Plant Examples

This directory contains example scripts and demos for testing the Pixel Plant components.

## Pattern Demo

**File**: `pattern_demo.py`

Demonstrates all 8x8 LED matrix pixel art patterns including emotional expressions and icons.

### Usage

**List all available patterns:**
```bash
python pattern_demo.py --list
```

**Console visualization (no hardware required):**
```bash
# Static display
python pattern_demo.py --console

# Animated with rise/fall effects (inspired by the book!)
python pattern_demo.py --console --animate

# Try different animation styles
python pattern_demo.py --console --animate --style cascade
python pattern_demo.py --console --animate --style wave
python pattern_demo.py --console --animate --style synchronized
```

**Display on LED matrix (requires hardware):**
```bash
# Display all patterns sequentially
sudo python pattern_demo.py

# Display specific pattern
sudo python pattern_demo.py --pattern happy
sudo python pattern_demo.py --pattern heart
sudo python pattern_demo.py --pattern water
```

### Available Patterns

**Emotional Expressions:**
- `happy` - Smiling face (green, breathing effect)
- `very_happy` - Wide smile (yellow, celebrating)
- `thinking` - Thoughtful expression (gray/white)
- `concerned` - Straight mouth (yellow, gentle attention)
- `worried` - Frown (orange/red, urgent care)
- `sleeping` - Closed eyes (blue, peaceful)
- `sleeping_zzz` - ZZZ animation (blue with accents)

**Icons:**
- `heart` - For encouragement (pink/red)
- `water` - Hydration reminder (cyan/blue)
- `check` - Task completed (green)
- `exclamation` - Alert/attention (orange/red)
- `walking` - Movement reminder (green)
- `stretching` - Stretch reminder (green)
- `sparkle` - Celebration (multi-color)
- `question` - Check-in (yellow)

## Test Matrix

**File**: `test_matrix.py` (from hardware guide)

Basic LED matrix hardware test to verify wiring and functionality.

```bash
# Test individual LEDs, grid pattern, and colors
sudo python test_matrix.py
```

Expected behavior:
1. Each LED lights up sequentially (0-63)
2. Green checkerboard pattern appears
3. Matrix cycles through 6 colors
4. Matrix turns off

## Quick Animation Test

**File**: `quick_animation_test.py`

Interactive demo specifically for rise/fall animations inspired by the book.

```bash
# Run interactive demo
python quick_animation_test.py

# Choose animation style and watch pixels rise and fall!
```

This shows how pixels "rise up from the base" just like in Becky Chambers' novel.

## More Examples Coming Soon

Future examples will include:
- `test_camera.py` - Camera module testing
- `test_audio.py` - Audio output and TTS testing
- `test_pir.py` - PIR motion sensor testing
- Integration demos combining multiple components

## Requirements

### For Console Demos
- Python 3.7+
- No additional packages required

### For Hardware Demos
- Raspberry Pi Zero 2 W (or compatible)
- 8x8 WS2812B LED matrix connected to GPIO 18
- Python 3.7+
- `rpi_ws281x` library

Install hardware dependencies:
```bash
pip install rpi_ws281x
```

## Troubleshooting

**ModuleNotFoundError: No module named 'personality'**
- Make sure you're running from the project root or examples directory
- The script automatically adds the src directory to Python path

**Permission denied when accessing GPIO**
- Hardware demos must run with sudo: `sudo python pattern_demo.py`
- Console demos don't need sudo

**No LEDs lighting up**
- Check wiring (5V, GND, GPIO 18)
- Verify power supply can provide 2A+
- See [LED Matrix Guide](../docs/hardware/led_matrix_guide.md) for troubleshooting

## Contributing Examples

Have a cool demo or test script? Contributions welcome!

1. Create your example script in this directory
2. Add clear documentation and comments
3. Update this README with usage instructions
4. Submit a pull request

---

*Happy making!* 🌿✨
