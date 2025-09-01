# Pixel Plant Development Environment Setup

> Complete guide to setting up your development environment for the Pixel Plant AI Companion

## 🎯 Quick Start

**Time to setup**: ~20 minutes  
**Skill level**: Beginner friendly  
**Platform**: Windows, macOS, Linux

### Prerequisites
- Computer with USB port
- Internet connection for downloads
- DFRobot FireBeetle ESP32-S3 (for hardware testing)

## 📥 Step 1: Install Arduino IDE

### Download and Install
1. **Visit**: [https://www.arduino.cc/en/software](https://www.arduino.cc/en/software)
2. **Download**: Arduino IDE 2.0+ (recommended) or 1.8.19+
3. **Install**: Follow the installer for your operating system

### Alternative: Arduino IDE Online
- Use [Arduino Web Editor](https://create.arduino.cc/editor) if you prefer cloud-based development
- Requires Arduino Create Agent for hardware communication

### VS Code Alternative (Advanced)
For experienced developers:
```bash
# Install VS Code extension
code --install-extension vsciot-vscode.vscode-arduino
```

## ⚙️ Step 2: Configure ESP32-S3 Board Support

### Add Board Manager URL
1. Open Arduino IDE
2. Go to **File → Preferences**
3. In **Additional Board Manager URLs**, add:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Click **OK**

### Install ESP32 Boards
1. Go to **Tools → Board → Boards Manager**
2. Search for **"ESP32"**
3. Install **"ESP32 by Espressif Systems"** (version 2.0.5+)
4. Wait for installation to complete

### Select Your Board
1. Go to **Tools → Board → ESP32 Arduino**
2. Select **"ESP32S3 Dev Module"**

### Configure Board Settings
For DFRobot FireBeetle ESP32-S3:
```
Board: "ESP32S3 Dev Module"
Upload Speed: "921600"
USB Mode: "Hardware CDC and JTAG"
USB CDC On Boot: "Enabled"
USB Firmware MSC On Boot: "Disabled"
USB DFU On Boot: "Disabled"
Upload Mode: "UART0 / Hardware CDC"
CPU Frequency: "240MHz (WiFi)"
Flash Mode: "QIO 80MHz"
Flash Size: "16MB (128Mb)"
Partition Scheme: "16M Flash (3MB APP/9MB FATFS)"
Core Debug Level: "None"
PSRAM: "OPI PSRAM"
Arduino Runs On: "Core 1"
Events Run On: "Core 1"
```

## 📚 Step 3: Install Required Libraries

### Method 1: Library Manager (Recommended)
1. Go to **Tools → Manage Libraries**
2. Install these libraries:

#### Core Libraries
- **FastLED** by Daniel Garcia (latest version)
- **ArduinoJson** by Benoit Blanchon (6.19+)

#### Audio Libraries
- **ESP32-audioI2S** by schreibfaul1
- **ESP32-I2S-Audio-Player** (alternative)

#### AI/ML Libraries
- **TensorFlowLite_ESP32** by TensorFlow Authors
- **EdgeImpulse-SDK** (optional, for custom models)

#### Utility Libraries
- **WiFiManager** by tzapu (for easy WiFi setup)
- **Preferences** (included with ESP32 core)
- **SPIFFS** (included with ESP32 core)

### Method 2: Manual Installation
If Library Manager doesn't work:

```bash
# Clone repositories to your libraries folder
cd ~/Documents/Arduino/libraries/

# FastLED
git clone https://github.com/FastLED/FastLED.git

# ESP32-audioI2S
git clone https://github.com/schreibfaul1/ESP32-audioI2S.git
```

### Verify Installation
Create a test sketch:
```cpp
#include <FastLED.h>
#include <ArduinoJson.h>
#include "WiFi.h"

void setup() {
  Serial.begin(115200);
  Serial.println("✅ All libraries loaded successfully!");
}

void loop() {
  delay(1000);
}
```

## 🔧 Step 3: Project Setup

### Clone the Repository
```bash
git clone https://github.com/your-username/pixel-plant.git
cd pixel-plant
```

### Open Main Project
1. Open Arduino IDE
2. **File → Open**
3. Navigate to: `firmware/pixel_plant/pixel_plant.ino`
4. The IDE will open all project files in tabs

### Project Structure Understanding
```
firmware/pixel_plant/
├── pixel_plant.ino          # Main sketch
├── config.h                 # Configuration constants
├── src/
│   ├── hardware/           # Hardware abstraction
│   ├── personality/        # AI personality engine
│   ├── ai/                 # Computer vision & behavior
│   └── utils/              # Helper functions
├── libraries/              # Custom libraries
└── examples/               # Component test sketches
```

## 🧪 Step 4: Test Your Setup

### Quick Verification Test
1. **Connect** ESP32-S3 via USB
2. **Select Port**: Tools → Port → (your ESP32 port)
3. **Load Test Sketch**: Open `firmware/examples/led_test/led_test.ino`
4. **Upload**: Click Upload button (→)
5. **Verify**: LEDs should show rainbow pattern

### Component Tests
Run these in order:
1. **LED Test**: `firmware/examples/led_test/`
2. **Audio Test**: `firmware/examples/audio_test/`
3. **PIR Test**: `firmware/examples/pir_test/`
4. **Camera Test**: `firmware/examples/camera_test/`

### Serial Monitor Setup
1. **Open**: Tools → Serial Monitor
2. **Set Baud Rate**: 115200
3. **Line Ending**: Both NL & CR
4. **Watch for**: Startup messages and test output

## 🔍 Step 5: Development Workflow

### Daily Development Cycle
```bash
# 1. Pull latest changes
git pull origin main

# 2. Make your changes
# Edit files in Arduino IDE

# 3. Test frequently
# Upload to hardware, check serial monitor

# 4. Commit your work
git add .
git commit -m "Add caring hydration reminders"
git push origin your-branch
```

### Code Organization Best Practices
- **Keep functions small** - max 50 lines
- **Use descriptive names** - `showCaringAnimation()` not `anim1()`
- **Comment your intentions** - explain the "why", not the "what"
- **Test on hardware frequently** - don't write too much without testing

### Debugging Tools
1. **Serial Monitor**: Primary debugging tool
2. **Serial Plotter**: Visualize sensor data
3. **ESP32 Exception Decoder**: Decode crash logs
4. **Logic Analyzer**: For I2S/SPI debugging (advanced)

## 🚨 Common Issues & Solutions

### ESP32 Not Found
**Problem**: "Port not found" or "device not recognized"
**Solutions**:
- Install CP210x USB drivers from Silicon Labs
- Try different USB cable (must support data)
- Press and hold BOOT button during upload
- Check if other software is using the port

### Library Conflicts
**Problem**: Compilation errors about missing libraries
**Solutions**:
```bash
# Clean library conflicts
rm -rf ~/Documents/Arduino/libraries/conflicting_lib
# Reinstall from Library Manager
```

### Memory Issues
**Problem**: "Not enough memory" during compilation
**Solutions**:
- Check Partition Scheme (use 16M Flash option)
- Remove unused #include statements
- Use PROGMEM for large constants

### Upload Failures
**Problem**: Upload fails or times out
**Solutions**:
- Lower upload speed to 460800 or 115200
- Press BOOT button right before upload
- Check power supply (use USB 3.0 port)
- Try pressing RESET then BOOT buttons

### WiFi Connection Issues
**Problem**: ESP32 can't connect to WiFi
**Solutions**:
```cpp
// Add to setup()
WiFi.mode(WIFI_STA);
WiFi.begin("YourNetwork", "YourPassword");
```

## ⚡ Performance Optimization

### Memory Management
```cpp
// Use PROGMEM for large strings
const char PROGMEM careTip[] = "Remember to hydrate!";

// Free unused memory
esp_wifi_stop();  // If not using WiFi

// Monitor memory usage
Serial.printf("Free heap: %d bytes\n", ESP.getFreeHeap());
```

### CPU Optimization
```cpp
// Use appropriate delays
delay(50);        // For animations
delayMicroseconds(10);  // For precise timing

// Optimize loops
for(int i = 0; i < LED_COUNT; i++) {
  // Keep loop body simple
}
```

## 🔧 Advanced Development Setup

### PlatformIO (Alternative to Arduino IDE)
```ini
# platformio.ini
[env:esp32s3]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino
lib_deps = 
  fastled/FastLED@^3.5.0
  bblanchon/ArduinoJson@^6.19.4
monitor_speed = 115200
```

### Custom Board Definitions
For specialized hardware configurations:
```cpp
// boards.txt additions for custom variants
pixel_plant_v1.name=Pixel Plant v1.0
pixel_plant_v1.vid.0=0x10c4
pixel_plant_v1.pid.0=0xea60
```

### Automated Testing
```cpp
// Simple unit test framework
void runTests() {
  assert(testLEDConnection() == true);
  assert(testAudioOutput() == true);
  assert(testSensorInput() == true);
  Serial.println("✅ All tests passed!");
}
```

## 🌐 Version Control Integration

### Git Workflow for Arduino
```bash
# Recommended .gitignore
*.tmp
*.bak
*~
.DS_Store
build/
```

### Branch Strategy
- **main**: Stable releases
- **develop**: Integration branch
- **feature/caring-reminders**: Feature branches
- **hotfix/audio-volume**: Critical fixes

## 📱 Mobile Development (Future)
For companion mobile apps:
- **Flutter**: Cross-platform development
- **React Native**: JavaScript-based mobile apps
- **Native**: iOS (Swift) / Android (Kotlin)

## 🤝 Contributing Guidelines

### Code Style
```cpp
// Use camelCase for variables
int currentMood = MOOD_HAPPY;

// Use descriptive function names
void showCaringReminder() {
  // Implementation
}

// Include caring philosophy in comments
// This gentle animation helps users feel supported
// without being overwhelming or demanding
```

### Pull Request Checklist
- [ ] Code compiles without warnings
- [ ] Hardware tested on actual device
- [ ] Documentation updated
- [ ] Caring philosophy maintained
- [ ] No hardcoded secrets

## 🆘 Getting Help

### Community Resources
- **GitHub Issues**: Technical problems and bugs
- **GitHub Discussions**: General questions and ideas
- **Arduino Forums**: ESP32-specific technical issues
- **Discord/Slack**: Real-time community chat (links in README)

### Documentation
- **API Reference**: `/docs/software/api.md`
- **Hardware Guide**: `/docs/hardware/assembly.md`
- **Troubleshooting**: `/docs/troubleshooting.md`

### Professional Support
For educational institutions or commercial projects:
- Email: support@pixelplant.ai (if available)
- Issue tracking with priority labels
- Educational discounts available

---

## ✅ Verification Checklist

Before you start developing:
- [ ] Arduino IDE 2.0+ installed
- [ ] ESP32 board package installed and configured
- [ ] All required libraries installed
- [ ] Hardware connected and recognized
- [ ] LED test sketch runs successfully
- [ ] Serial monitor shows clean output
- [ ] Git repository cloned
- [ ] Main project opens without errors

**Ready to build caring technology!** 🌿✨

*"The best development environment is one that gets out of your way so you can focus on creating technology that truly cares."*

---

*Last updated: December 2024*  
*If you find issues with this setup guide, please report them on GitHub Issues*