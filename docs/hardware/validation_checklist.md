# Hardware Validation Checklist

> **🎯 Goal**: Systematic verification of all Pixel Plant components when hardware arrives

## 📦 Pre-Assembly Checklist

### Component Inventory
- [ ] ESP32-S3 FireBeetle with camera module
- [ ] RGB LED strip (WS2812B, 60 LEDs/meter, 1 meter)
- [ ] I2S Audio amplifier (MAX98357A)
- [ ] 40mm Speaker (4 Ohm, 3W)
- [ ] PIR motion sensor (BL412)
- [ ] Resistor kit (including 330Ω for LED data line)
- [ ] Jumper wires and breadboard
- [ ] USB cable for ESP32-S3

### Visual Inspection
- [ ] ESP32-S3 board - no visible damage, solder joints intact
- [ ] Camera module - lens clean, no cracks, properly seated
- [ ] LED strip - no damaged LEDs, solder points intact
- [ ] Audio amplifier - no bent pins, board undamaged
- [ ] Speaker - cone undamaged, wires secure
- [ ] PIR sensor - lens clean, no cracks

### Documentation Check
- [ ] All component datasheets available
- [ ] Pin diagrams and schematics ready
- [ ] Assembly guide reviewed
- [ ] Test sketches downloaded and ready

---

## ⚡ Power System Validation

### Basic Power Test
- [ ] ESP32-S3 powers on via USB (status LED lights)
- [ ] No excessive heat generation
- [ ] Serial monitor connection works at 115200 baud
- [ ] Power LED indicators function correctly

### Power Supply Measurements
**Equipment needed**: Multimeter

- [ ] 5V rail: **Measured**: _____ V (Expected: 4.8-5.2V)
- [ ] 3.3V rail: **Measured**: _____ V (Expected: 3.1-3.4V)
- [ ] Current draw (idle): **Measured**: _____ mA (Expected: <200mA)
- [ ] No short circuits detected

### Power Under Load
- [ ] LED strip connected - voltage stable under load
- [ ] Audio amplifier connected - no voltage drops during operation
- [ ] All components powered simultaneously without issues

---

## 🌈 LED System Validation

### Connection Test
Load: `firmware/examples/led_test/led_test.ino`

- [ ] **Basic Colors Test**: All LEDs display red, green, blue, white
- [ ] **Individual LED Test**: Each LED can be controlled individually
- [ ] **Connection Integrity**: No flickering or dead LEDs
- [ ] **Data Line**: 330Ω resistor in series with data line

### Performance Tests
- [ ] **Rainbow Pattern**: Smooth color transitions across strip
- [ ] **Breathing Animation**: Smooth brightness transitions
- [ ] **Chase Effect**: Moving patterns work correctly
- [ ] **Sparkle Effect**: Random LEDs light up and fade

### LED Strip Specific Tests
- [ ] **LED Count**: Verify actual LED count matches configuration (60 LEDs)
- [ ] **Color Order**: RGB vs GRB - colors display correctly
- [ ] **Power Consumption**: Strip doesn't exceed power supply capacity
- [ ] **Heat Generation**: LEDs don't overheat at full brightness

**Notes**: 
- LED Count: _____ (actual vs expected 60)
- Color Issues: _____________________
- Performance Issues: ________________

---

## 🔊 Audio System Validation

### Connection Test
Load: `firmware/examples/audio_test/audio_test.ino`

- [ ] **Silence Test**: No audio output when expected
- [ ] **Pure Tone Test**: Clear 440Hz sine wave audible
- [ ] **Volume Control**: Audio amplifier responds to volume changes
- [ ] **No Distortion**: Clean audio at moderate volumes

### I2S Interface Tests
- [ ] **BCLK Signal**: Bit clock present on GPIO 19
- [ ] **LRC Signal**: Left/Right clock present on GPIO 20
- [ ] **DIN Signal**: Data signal present on GPIO 21
- [ ] **Sample Rate**: 22050 Hz confirmed working

### Audio Quality Tests
- [ ] **Frequency Sweep**: Smooth transition from 200Hz to 2000Hz
- [ ] **Beep Pattern**: Clear, distinct beeps
- [ ] **Caring Tones**: Gentle, harmonious tones
- [ ] **White Noise**: Full frequency spectrum test

### Speaker Performance
- [ ] **Physical Check**: Cone moves freely, no rattling
- [ ] **Impedance**: 4 Ohm measurement confirmed
- [ ] **Power Handling**: No distortion at rated power
- [ ] **Frequency Response**: Reasonable response across audio range

**Notes**:
- Audio Quality Issues: ____________________
- Volume Level: _____ (1-10 scale)
- Distortion Present: Yes / No

---

## 🚶 Motion Sensor Validation

### Basic Function Test
Load: `firmware/examples/pir_test/pir_test.ino`

- [ ] **Power On**: PIR sensor LED indicator (if present) lights up
- [ ] **Calibration**: 10-second calibration period completed
- [ ] **Motion Detection**: Hand wave triggers sensor
- [ ] **Motion End**: Sensor returns to LOW state after motion stops

### Sensitivity Tests
- [ ] **Close Range**: Motion detected at 0.5 meters
- [ ] **Medium Range**: Motion detected at 1.5 meters  
- [ ] **Long Range**: Motion detected at 3+ meters
- [ ] **Different Angles**: Sensor detects motion from sides

### Performance Validation
- [ ] **Response Time**: <1 second from motion start to detection
- [ ] **Recovery Time**: Returns to idle within expected time
- [ ] **False Positives**: No triggers from air movement/temperature changes
- [ ] **Debouncing**: Clean state transitions without bouncing

### Adjustment Tests
- [ ] **Sensitivity Pot**: Turning clockwise increases sensitivity
- [ ] **Time Delay Pot**: Turning clockwise increases trigger duration
- [ ] **Optimal Settings**: Settings adjusted for desk environment

**Notes**:
- Detection Range: _____ meters
- False Positives: ____________________
- Optimal Sensitivity Setting: _________

---

## 📷 Camera System Validation

### Basic Function Test
Load: `firmware/examples/camera_test/camera_test.ino`

- [ ] **Initialization**: Camera initializes without errors
- [ ] **Image Capture**: Successfully captures JPEG images
- [ ] **Resolution**: Images captured at expected resolution
- [ ] **Memory**: PSRAM usage within acceptable limits

### Image Quality Tests
- [ ] **Focus**: Images are reasonably sharp
- [ ] **Exposure**: Images not over/under exposed in normal lighting
- [ ] **Color**: Colors appear natural and accurate
- [ ] **Noise**: Minimal noise in good lighting conditions

### Different Conditions
- [ ] **Bright Light**: Camera adjusts exposure appropriately
- [ ] **Low Light**: Images still usable in dim conditions
- [ ] **Movement**: Can detect motion blur for activity recognition
- [ ] **Different Distances**: Clear images at typical desk distances

### Technical Performance
- [ ] **Frame Rate**: Achieves reasonable FPS for AI processing
- [ ] **Memory Usage**: No memory leaks during continuous operation
- [ ] **Heat Generation**: Camera doesn't overheat during operation
- [ ] **Power Consumption**: Reasonable current draw

**Notes**:
- Image Quality (1-10): _____
- Frame Rate: _____ FPS
- Issues Observed: ____________________

---

## 🧪 System Integration Tests

### Combined System Test
Load: `firmware/pixel_plant/pixel_plant.ino`

- [ ] **Boot Sequence**: System boots cleanly with all components
- [ ] **Startup Animation**: LEDs show startup sequence
- [ ] **Audio Greeting**: Plays startup sound/message
- [ ] **Sensor Initialization**: All sensors initialize successfully

### Interaction Tests
- [ ] **Motion Triggers Response**: PIR sensor triggers LED and audio response
- [ ] **Camera Integration**: Camera captures when motion detected
- [ ] **Mood Display**: LEDs change based on system state
- [ ] **Serial Commands**: Debug commands work correctly

### Performance Integration
- [ ] **Memory Usage**: System stable with <10MB RAM usage
- [ ] **CPU Usage**: No watchdog resets or system freezes
- [ ] **Temperature**: System temperature within safe limits
- [ ] **Power Draw**: Total current <2A at full operation

### Long-term Stability
- [ ] **30 Minute Test**: System runs stable for extended period
- [ ] **Thermal Stability**: No overheating issues
- [ ] **Memory Stability**: No memory leaks over time
- [ ] **Sensor Reliability**: Consistent sensor performance

---

## 🔧 Troubleshooting Guide

### LED Issues
**No LEDs lighting up**:
- [ ] Check 5V power connection
- [ ] Verify data line connection (GPIO 18)
- [ ] Check 330Ω resistor in data line
- [ ] Try different LED strip section

**Some LEDs not working**:
- [ ] Check for damaged LEDs in strip
- [ ] Verify power supply adequate for LED count
- [ ] Check solder joints on LED strip

**Wrong colors displaying**:
- [ ] Try different color order in code (GRB vs RGB)
- [ ] Check for loose data line connections

### Audio Issues
**No audio output**:
- [ ] Check speaker connections (+ and -)
- [ ] Verify I2S pin connections (19, 20, 21)
- [ ] Check audio amplifier power (5V)
- [ ] Test with headphones on amplifier output

**Distorted audio**:
- [ ] Check power supply adequacy
- [ ] Verify speaker impedance (4 Ohm)
- [ ] Reduce volume level in code

### Motion Sensor Issues
**No motion detection**:
- [ ] Check 3.3V power to PIR sensor
- [ ] Verify signal pin connection (GPIO 22)
- [ ] Wait for full calibration period
- [ ] Adjust sensitivity potentiometer

**False motion triggers**:
- [ ] Reduce sensitivity setting
- [ ] Check for electrical interference
- [ ] Shield sensor from air currents

### Camera Issues
**Camera initialization fails**:
- [ ] Verify ESP32-S3 with camera module
- [ ] Check camera power pin (if applicable)
- [ ] Try camera reset
- [ ] Check PSRAM availability

**Poor image quality**:
- [ ] Clean camera lens
- [ ] Adjust lighting conditions
- [ ] Check camera settings in code
- [ ] Verify camera not overheating

---

## ✅ Validation Results Summary

### Component Status
| Component | Status | Notes |
|-----------|--------|-------|
| ESP32-S3 Board | ☐ Pass ☐ Fail | |
| LED Strip | ☐ Pass ☐ Fail | |
| Audio System | ☐ Pass ☐ Fail | |
| PIR Sensor | ☐ Pass ☐ Fail | |
| Camera | ☐ Pass ☐ Fail | |

### Integration Status
- [ ] All components work individually
- [ ] Components work together without conflicts
- [ ] System stable under normal operation
- [ ] Performance meets expectations
- [ ] Ready for personality/AI development

### Next Steps
If all validations pass:
- [ ] Proceed with personality system development
- [ ] Begin AI/behavioral recognition implementation
- [ ] Start enclosure design and assembly

If validations fail:
- [ ] Document specific issues found
- [ ] Research solutions for failed components
- [ ] Contact suppliers if hardware defects suspected
- [ ] Consider component substitutions if necessary

---

**Validation completed by**: ___________________
**Date**: ___________________  
**Total time spent**: _____ hours

**Overall assessment**: 
☐ Ready for development
☐ Minor issues to resolve  
☐ Major issues require attention
☐ Hardware replacement needed

**Additional notes**:
_________________________________________________
_________________________________________________
_________________________________________________