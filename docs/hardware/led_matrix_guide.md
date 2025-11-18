# 8x8 WS2812B LED Matrix Guide

## Overview

The Pixel Plant uses an **8x8 WS2812B RGB LED matrix** (64 individually addressable LEDs) as its primary visual display system. This provides much richer expressiveness than a linear LED strip, enabling:

- **Simple faces and emotions** (happy, concerned, worried, sleeping)
- **Pixel art icons** (hearts, checkmarks, exclamation points)
- **Smooth animations** between mood states
- **2D patterns and effects** for personality expression

## Hardware Specifications

### 8x8 WS2812B Matrix
- **Total LEDs**: 64 (8 rows × 8 columns)
- **Voltage**: 5V DC
- **Current**:
  - Per LED (white, full brightness): ~60mA
  - Maximum theoretical: 64 × 60mA = 3.84A
  - Typical usage (colored, medium brightness): 1-2A
- **Data Protocol**: WS2812B (800 kHz single-wire)
- **Connections**: 3-wire (5V, GND, Data In)
- **Form Factor**: Typically 8cm × 8cm flexible PCB

### Common Matrix Types

**Option 1: Generic WS2812B 8x8 Matrix** (£8-10)
- Most affordable option
- Available from AliExpress, eBay, Amazon
- Quality varies by supplier
- Usually pre-soldered with connection wires

**Option 2: Adafruit NeoPixel 8x8 Matrix** (£11-15)
- Higher quality, consistent performance
- Excellent documentation and support
- Part numbers: 1487 (flexible) or 2612 (rigid)
- Made for makers, well-tested

**Option 3: BTF-Lighting WS2812B Panel** (£9-11)
- Good middle ground
- Reliable quality
- Often includes mounting holes

## Wiring to Raspberry Pi Zero 2 W

### Pin Connections

| Matrix Connector | Raspberry Pi Zero 2 W | Wire Color (typical) | Notes |
|------------------|----------------------|---------------------|-------|
| 5V / VCC | Pin 2 (5V Power) | Red | Power supply |
| GND | Pin 6 (Ground) | Black/White | Ground reference |
| DIN / Data In | GPIO 18 (Pin 12) | Green/Yellow | PWM0 data signal |

### Wiring Diagram

```
┌─────────────────────────────┐
│   Raspberry Pi Zero 2 W     │
│                             │
│  Pin 2 (5V)  ──────┬────────┼──→ [5V] Matrix
│                    │        │
│                    │        │
│  Pin 6 (GND) ──────┼────┬───┼──→ [GND] Matrix
│                    │    │   │
│                    │    │   │
│  Pin 12 (GPIO 18)──┼────┼───┼──→ [DIN] Matrix
│                    │    │   │         (through 330Ω)
└────────────────────┼────┼───┘
                     │    │
              ┌──────▼────▼──────┐
              │   [Optional]     │
              │ 1000µF Capacitor │  ← Across 5V and GND
              │ 330Ω Resistor    │  ← In series with data
              └──────────────────┘
```

### Important Hardware Considerations

**1. Data Line Protection**
- **Recommended**: Add a 330Ω-470Ω resistor between GPIO 18 and matrix DIN
- Protects against voltage spikes and signal reflections
- Place resistor as close to the Pi as possible

**2. Power Supply Decoupling**
- **Highly recommended**: 1000µF electrolytic capacitor across 5V and GND rails
- Place capacitor close to the LED matrix power input
- Helps prevent voltage drops during LED color changes
- Reduces noise and improves stability

**3. Power Considerations**
- If powering from Pi's 5V pin: Be aware of current limits
  - Pi Zero 2 W can typically supply 1-1.5A safely from 5V rail
  - This is sufficient for typical Pixel Plant usage (colored LEDs at medium brightness)
  - Avoid all LEDs at full white brightness simultaneously
- For maximum brightness: Consider external 5V power supply
  - Connect external 5V to matrix VCC
  - **Must share common ground** with Pi
  - Pi GPIO 18 provides data signal only

## Matrix LED Indexing

### Understanding the Grid Layout

Most WS2812B 8x8 matrices use a **zigzag/serpentine** layout:

```
LED Index Layout (Common Configuration):
   0  1  2  3  4  5  6  7
  15 14 13 12 11 10  9  8
  16 17 18 19 20 21 22 23
  31 30 29 28 27 26 25 24
  32 33 34 35 36 37 38 39
  47 46 45 44 43 42 41 40
  48 49 50 51 52 53 54 55
  63 62 61 60 59 58 57 56
```

**Note**: Always verify your specific matrix's data sheet - some use different patterns!

### Coordinate to Index Mapping (Python)

```python
def xy_to_index(x, y, width=8):
    """
    Convert (x, y) coordinates to linear LED index.
    Assumes serpentine/zigzag layout starting from top-left.

    Args:
        x: Column (0-7)
        y: Row (0-7)
        width: Matrix width (default 8)

    Returns:
        LED index (0-63)
    """
    if y % 2 == 0:
        # Even rows: left to right
        return y * width + x
    else:
        # Odd rows: right to left (zigzag)
        return y * width + (width - 1 - x)
```

### Alternative: Progressive Layout

Some matrices use a progressive layout (all rows left-to-right):

```python
def xy_to_index_progressive(x, y, width=8):
    """Convert (x, y) to index for progressive layout."""
    return y * width + x
```

**Test your matrix** with the test script to determine which layout it uses!

## Software Setup

### Installing rpi_ws281x Library

```bash
# Activate virtual environment
source venv/bin/activate

# Install the library
pip install rpi_ws281x

# Test installation
python -c "import rpi_ws281x; print('Success!')"
```

### Basic Test Script

Create `examples/test_matrix.py`:

```python
#!/usr/bin/env python3
"""
8x8 LED Matrix Test for Pixel Plant
Tests individual LEDs and verifies wiring
"""

import time
from rpi_ws281x import PixelStrip, Color

# LED matrix configuration
LED_COUNT = 64        # 8x8 = 64 LEDs
LED_PIN = 18          # GPIO pin (must support PWM)
LED_FREQ_HZ = 800000  # LED signal frequency (Hz)
LED_DMA = 10          # DMA channel
LED_BRIGHTNESS = 64   # Brightness (0-255) - start low!
LED_INVERT = False    # Signal inversion
LED_CHANNEL = 0       # PWM channel

def xy_to_index(x, y, width=8):
    """Convert grid coordinates to LED index (serpentine layout)."""
    if y % 2 == 0:
        return y * width + x
    else:
        return y * width + (width - 1 - x)

def test_individual_leds(strip):
    """Light up each LED sequentially to verify wiring."""
    print("Testing individual LEDs (0-63)...")
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(50, 50, 50))  # Dim white
        strip.show()
        time.sleep(0.05)
        strip.setPixelColor(i, Color(0, 0, 0))  # Off
    strip.show()

def test_grid_pattern(strip):
    """Test grid coordinates with a checkerboard pattern."""
    print("Testing 8x8 grid pattern...")
    for y in range(8):
        for x in range(8):
            if (x + y) % 2 == 0:
                idx = xy_to_index(x, y)
                strip.setPixelColor(idx, Color(0, 50, 0))  # Green
    strip.show()
    time.sleep(2)

    # Clear
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def test_colors(strip):
    """Cycle through primary colors."""
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (0, 255, 255),  # Cyan
        (255, 0, 255),  # Magenta
    ]

    print("Testing colors...")
    for r, g, b in colors:
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(g, r, b))  # Note: GRB order!
        strip.show()
        time.sleep(1)

    # Clear
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def main():
    # Create LED strip object
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                       LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

    # Initialize library (must be called once)
    strip.begin()

    print("8x8 LED Matrix Test")
    print("===================")

    try:
        test_individual_leds(strip)
        time.sleep(1)
        test_grid_pattern(strip)
        time.sleep(1)
        test_colors(strip)

        print("\nTest complete!")

    except KeyboardInterrupt:
        print("\nTest interrupted")

    finally:
        # Clear all LEDs on exit
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()

if __name__ == '__main__':
    main()
```

### Running the Test

```bash
# Must run with sudo for GPIO access
sudo python examples/test_matrix.py
```

**Expected behavior:**
1. Each LED lights up briefly in sequence (0-63)
2. Checkerboard pattern appears in green
3. Entire matrix cycles through 6 colors
4. Matrix turns off

## Troubleshooting

### No LEDs Light Up

**Check Power:**
- Verify 5V and GND connections are secure
- Measure voltage at matrix power pins (should be ~5V)
- Check if power supply can provide sufficient current (2A+)

**Check Data Signal:**
- Verify GPIO 18 connection to DIN
- Ensure resistor (if used) is the correct value (330-470Ω)
- Try running test script with `sudo`
- Check if SPI is disabled in Pi config (it should be for GPIO 18 PWM)

### Only First Few LEDs Work

- **Insufficient power**: Increase power supply capacity or reduce brightness
- **Damaged LEDs**: One failed LED can break the chain
- **Weak data signal**: Check data line integrity

### Wrong Colors or Flickering

- **Inadequate power filtering**: Add or increase capacitor value
- **EMI interference**: Keep data wire short, use shielded cable if needed
- **Wrong color order**: Try swapping R/G/B values in code (some matrices are RGB, others GRB)

### Incorrect LED Sequence

- **Wrong index mapping**: Your matrix might use progressive instead of serpentine layout
- **Test methodology**: Run individual LED test and map physical position to index number
- **Modify mapping function**: Adjust `xy_to_index()` to match your matrix

## Safety Notes

⚠️ **Important Safety Considerations:**

1. **Current Draw**: Never exceed your power supply's rated current
2. **Heat**: Matrix can get warm at full brightness - ensure adequate ventilation
3. **ESD Protection**: Use anti-static precautions when handling
4. **Polarity**: Double-check 5V and GND polarity before powering on
5. **GPIO Protection**: Never exceed 3.3V on GPIO pins - use level shifter if needed

## Next Steps

Once your matrix is working:

1. **Create Simple Patterns**: Design 8x8 pixel art faces and icons
2. **Implement Animations**: Smooth transitions between emotional states
3. **Integrate with Personality**: Connect LED expressions to behavior monitoring
4. **Optimize Power**: Reduce brightness for battery operation
5. **Design Enclosure**: Create a housing that showcases the matrix display

## Resources

- **rpi_ws281x Documentation**: https://github.com/rpi-ws281x/rpi-ws281x-python
- **WS2812B Datasheet**: Detailed timing and electrical specifications
- **Pixel Art Tools**: Online editors for designing 8x8 icons
- **Community Patterns**: Share your LED animations and face designs

---

**Ready to give your Pixel Plant a face?** The 8x8 matrix opens up incredible possibilities for personality expression! 🌈✨
