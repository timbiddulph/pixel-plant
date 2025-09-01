# Pixel Plant Assembly Guide

> **⚠️ Safety First**: Always power off your device before making connections. Use proper ESD precautions when handling electronic components.

## Prerequisites

### Required Components
Refer to the [Bill of Materials](BOM.md) for the complete component list.

### Tools Needed
- Soldering iron (temperature controlled recommended)
- Solder (60/40 rosin core or lead-free)
- Wire strippers
- Multimeter
- Small screwdrivers
- Hot glue gun (optional, for strain relief)

### Skills Required
- **Beginner**: Basic soldering and wiring
- **Time Estimate**: 2-4 hours for first build
- **Difficulty**: 6/10 (intermediate maker project)

## Step 1: Component Preparation

### 1.1 Inventory Check
- [ ] ESP32-S3 FireBeetle with camera
- [ ] RGB LED strip (1 meter)
- [ ] MAX98357A audio amplifier
- [ ] 40mm speaker
- [ ] PIR motion sensor
- [ ] Resistors and jumper wires

### 1.2 Test Components Individually
Before assembly, test each component:

```cpp
// Test code snippets available in:
// firmware/examples/led_test/
// firmware/examples/audio_test/
// firmware/examples/camera_test/
```

## Step 2: Power Distribution Planning

### 2.1 Power Requirements
| Component | Voltage | Current (typ) | Current (max) |
|-----------|---------|---------------|---------------|
| ESP32-S3 | 3.3V | 100mA | 500mA |
| LED Strip | 5V | 300mA (10 LEDs) | 3.6A (60 LEDs) |
| Audio Amp | 5V | 50mA | 1.5A |
| PIR Sensor | 3.3V | 20µA | 100µA |

### 2.2 Power Supply Strategy
- **USB Power**: 5V/2A minimum recommended
- **Battery Option**: 3.7V LiPo with boost converter
- **Power Distribution**: Use breadboard power rails

## Step 3: Breadboard Assembly

### 3.1 Layout Planning
```
    [ESP32-S3]
         |
    [Breadboard]
         |
[Audio] [PIR] [LEDs]
```

### 3.2 Power Rail Setup
1. Connect 5V and GND from ESP32-S3 to breadboard rails
2. Add decoupling capacitors (100µF, 10µF) near power connections
3. Use separate rails for 3.3V components if needed

### 3.3 Component Placement
- Place ESP32-S3 at one end of breadboard
- Keep analog components (audio) away from digital switching (LEDs)
- Maintain short wire runs where possible

## Step 4: Wiring Connections

### 4.1 ESP32-S3 Pin Assignments
```cpp
// Pin definitions for FireBeetle ESP32-S3
#define LED_DATA_PIN    18  // WS2812B data
#define AUDIO_BCLK      19  // I2S bit clock
#define AUDIO_LRC       20  // I2S left/right clock  
#define AUDIO_DIN       21  // I2S data
#define PIR_SENSOR      22  // PIR motion detection
#define CAMERA_PWR      23  // Camera power control
```

### 4.2 LED Strip Connection
| ESP32-S3 Pin | LED Strip Wire | Notes |
|--------------|----------------|-------|
| Pin 18 | DIN (Data) | Signal wire |
| 5V | +5V | Power (red wire) |
| GND | GND | Ground (white/black) |

**Important**: Add 330Ω resistor in series with data line to prevent signal issues.

### 4.3 Audio System Wiring
| ESP32-S3 Pin | MAX98357A Pin | Speaker Wire |
|--------------|---------------|--------------|
| Pin 19 | BCLK | - |
| Pin 20 | LRC | - |
| Pin 21 | DIN | - |
| 5V | VIN | - |
| GND | GND | - |
| - | OUT+ | Speaker + |
| - | OUT- | Speaker - |

### 4.4 PIR Sensor Connection
| ESP32-S3 Pin | PIR Sensor Pin |
|--------------|----------------|
| Pin 22 | OUT |
| 3.3V | VCC |
| GND | GND |

### 4.5 Camera Module
The camera is integrated with the ESP32-S3 FireBeetle - no additional wiring required.

## Step 5: Initial Testing

### 5.1 Power-On Test
1. Connect USB cable to ESP32-S3
2. Check power LED indicators
3. Measure voltages with multimeter:
   - 5V rail: 4.8-5.2V
   - 3.3V rail: 3.1-3.4V

### 5.2 Individual Component Tests

#### LED Test
```cpp
// Load firmware/examples/led_test/led_test.ino
// Should see rainbow pattern on LED strip
```

#### Audio Test  
```cpp
// Load firmware/examples/audio_test/audio_test.ino
// Should hear test tones from speaker
```

#### PIR Test
```cpp
// Load firmware/examples/pir_test/pir_test.ino  
// Wave hand in front of sensor, check serial output
```

#### Camera Test
```cpp
// Load firmware/examples/camera_test/camera_test.ino
// Check serial output for image capture confirmation
```

## Step 6: Software Installation

### 6.1 Arduino IDE Setup
1. Install Arduino IDE 2.0+
2. Add ESP32 board package:
   - File → Preferences
   - Additional Board Manager URLs: 
     `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
3. Install "ESP32 by Espressif Systems"

### 6.2 Library Installation
Install these libraries through Library Manager:
- `FastLED` by Daniel Garcia
- `ESP32-audioI2S` by schreibfaul1
- `ArduinoJson` by Benoit Blanchon
- `TensorFlowLite_ESP32` (for AI features)

### 6.3 Load Main Firmware
1. Open `firmware/pixel_plant/pixel_plant.ino`
2. Select board: "ESP32S3 Dev Module"
3. Configure settings:
   - Flash Size: 16MB
   - PSRAM: OPI PSRAM
   - Upload Speed: 921600
4. Upload firmware

## Step 7: Calibration & Testing

### 7.1 LED Brightness Calibration
```cpp
// Adjust in firmware/pixel_plant/config.h
#define LED_BRIGHTNESS_DEFAULT 50  // 0-255
#define LED_COUNT 60               // Match your strip
```

### 7.2 Audio Volume Setting
```cpp
// Adjust in audio configuration
#define AUDIO_VOLUME_DEFAULT 0.7   // 0.0-1.0
```

### 7.3 PIR Sensitivity
- Adjust PIR sensor potentiometers:
  - Sensitivity (Sx): Clockwise = more sensitive
  - Time delay (Tx): Clockwise = longer trigger time

### 7.4 Camera Positioning
- Ensure camera has clear view of desk area
- Adjust mounting angle for optimal person detection
- Test with different lighting conditions

## Step 8: Troubleshooting

### Common Issues

#### LEDs Not Working
- [ ] Check power supply (5V, adequate current)
- [ ] Verify data pin connection (Pin 18)
- [ ] Test with single LED first
- [ ] Check for reversed power connections

#### No Audio Output
- [ ] Verify I2S pin connections (19, 20, 21)
- [ ] Check speaker polarity
- [ ] Test with headphones on amplifier output
- [ ] Verify audio amplifier power

#### PIR False Triggers
- [ ] Reduce sensitivity setting
- [ ] Shield sensor from air currents
- [ ] Check for electrical interference
- [ ] Adjust mounting position

#### Camera Not Detected
- [ ] Check camera power pin (Pin 23)
- [ ] Verify ESP32-S3 firmware supports camera
- [ ] Test with example camera code
- [ ] Check for physical damage to camera module

#### ESP32 Won't Program
- [ ] Install CP2102 USB drivers
- [ ] Try different USB cable
- [ ] Hold BOOT button during upload
- [ ] Check USB port power capability

### Getting Help
If you encounter issues:
1. Check the [troubleshooting guide](../troubleshooting.md)
2. Search [GitHub Issues](https://github.com/your-repo/pixel-plant/issues)
3. Post detailed question with photos in Issues section

## Step 9: Enclosure Assembly

### 9.1 3D Printed Enclosure
Files available in `hardware/3d_models/`:
- `pixel_plant_base.stl` - Main housing
- `pixel_plant_lid.stl` - Top cover with camera opening
- `pixel_plant_diffuser.stl` - LED light diffuser

### 9.2 Assembly Instructions
1. Insert ESP32-S3 into mounting posts
2. Route LED strip around perimeter groove
3. Mount speaker in designated cavity
4. Secure PIR sensor in front panel
5. Connect all cables before closing enclosure

### 9.3 Alternative Enclosures
- **Project Box**: Modify plastic enclosure
- **Laser Cut**: Custom acrylic design
- **Wooden Box**: Natural materials option

## Step 10: Final Testing & Calibration

### 10.1 Full System Test
1. Power on complete assembly
2. Verify all LEDs light up correctly
3. Test audio output and personality responses
4. Check motion detection and camera functionality
5. Run extended operation test (30+ minutes)

### 10.2 Personalization Setup
1. Configure your work schedule
2. Set preferred reminder intervals
3. Calibrate activity detection for your workspace
4. Adjust personality settings

### 10.3 Performance Validation
- [ ] System runs stable for 1+ hours
- [ ] No overheating issues
- [ ] All sensors respond appropriately
- [ ] Audio is clear and pleasant
- [ ] LEDs display smooth animations

## Next Steps

Congratulations! Your Pixel Plant is assembled and ready to be your caring desktop companion.

### Recommended Next Actions:
1. Read the [User Guide](../software/user_guide.md)
2. Explore [Customization Options](../customization/README.md)
3. Join the [Community Discussions](https://github.com/your-repo/pixel-plant/discussions)
4. Share your build in the [Gallery](../community/gallery.md)

---

*"Every caring companion starts with careful assembly. Take your time, and your Pixel Plant will take care of you!"* 🌿✨