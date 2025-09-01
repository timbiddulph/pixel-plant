# Pixel Plant AI Companion 🌿🤖

> *"Hey, there! You need to hydrate!"* - Your caring AI desktop companion

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Arduino](https://img.shields.io/badge/Arduino-IDE_Compatible-blue.svg)](https://www.arduino.cc/)
[![ESP32](https://img.shields.io/badge/Platform-ESP32--S3-red.svg)](https://www.espressif.com/)
[![Community](https://img.shields.io/badge/Community-Welcome-green.svg)](CONTRIBUTING.md)

An AI-powered desktop companion inspired by Becky Chambers' novel "The Long Way to a Small, Angry Planet." The Pixel Plant monitors your behavior and provides caring health reminders through personality-rich interactions.

## ✨ Features

- **🎯 Behavioral Recognition**: Real-time analysis of sitting/standing and activity patterns
- **💬 Personality-Rich Responses**: Caring, adaptive reminders that feel genuine
- **🌈 Visual Expression**: Color-changing LED display showing mood and emotions  
- **🔊 Voice Interaction**: Text-to-speech with personality variations
- **🧠 Learning System**: Adapts to your patterns and preferences over time
- **🔒 Privacy-First**: All AI processing happens on-device

## 🚀 Quick Start

### Hardware Requirements

- DFRobot FireBeetle 2 ESP32-S3 with Camera (External Antenna)
- Flexible RGB LED Strip (60 LED/m)
- Adafruit I2S Audio Amplifier (MAX98357A)
- 40mm Speaker (4 Ohm, 3W)
- Mini PIR Sensor (BL412)
- Basic resistors and wiring components

**Total Cost**: ~£53 (see [Bill of Materials](docs/hardware/BOM.md))

### Software Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/pixel-plant.git
   cd pixel-plant
   ```

2. **Install Arduino IDE and ESP32 boards**
   - Download [Arduino IDE](https://www.arduino.cc/en/software)
   - Add ESP32 board manager: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
   - Install "ESP32 by Espressif Systems"

3. **Install required libraries**
   ```
   - TensorFlowLite_ESP32
   - FastLED
   - ESP32-I2S-Audio
   - ArduinoJson
   ```

4. **Flash the firmware**
   - Open `firmware/pixel_plant/pixel_plant.ino`
   - Select board: "ESP32S3 Dev Module"
   - Upload to your device

## 📖 Documentation

- **[Assembly Guide](docs/hardware/assembly.md)** - Step-by-step hardware setup
- **[Software Architecture](docs/software/architecture.md)** - Code structure and design
- **[API Reference](docs/software/api.md)** - Function and class documentation
- **[Customization Guide](docs/customization/README.md)** - Personalizing your Pixel Plant
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

## 🛠️ Project Structure

```
pixel-plant/
├── firmware/                 # ESP32-S3 Arduino code
│   ├── pixel_plant/         # Main sketch
│   ├── libraries/           # Custom libraries
│   └── examples/            # Test sketches
├── hardware/                # Wiring diagrams & schematics
│   ├── schematics/         # Circuit diagrams
│   ├── pcb/                # PCB designs (optional)
│   └── 3d_models/          # Enclosure 3D files
├── docs/                   # Comprehensive documentation
│   ├── hardware/           # Assembly and wiring guides
│   ├── software/           # Code documentation
│   └── customization/      # User customization guides
├── tools/                  # Development utilities
└── examples/               # Usage examples
```

## 🤖 How It Works

The Pixel Plant uses computer vision and sensor fusion to understand your work patterns:

1. **Behavioral Detection**: Camera analyzes your posture and movement
2. **Pattern Learning**: AI tracks your habits and optimal break times
3. **Caring Reminders**: Provides gentle, personalized health suggestions
4. **Visual Feedback**: LED expressions show the plant's mood and concerns
5. **Adaptive Responses**: Learns what reminder styles work best for you

## 🌟 Core Philosophy

The Pixel Plant embodies caring technology:

- **Genuine Care**: Responses feel authentic, not algorithmic
- **Gentle Persistence**: Reminders are caring, not nagging  
- **Emotional Intelligence**: Knows when to encourage vs. when to stay quiet
- **Growth-Oriented**: Celebrates improvements in your habits

## 🎨 Personality Examples

- **Hydration**: *"Hey there! You need to hydrate!"*
- **Movement**: *"How about a snack? Take a walk! Stretch it out!"*
- **Encouragement**: *"Aw, it's not so bad! Give yourself a hug!"*
- **Celebration**: *Cheerful color cycling when you take breaks*

## 🛡️ Privacy & Security

- **On-Device Processing**: All AI runs locally on ESP32-S3
- **No Cloud Dependency**: Core functionality works completely offline
- **Open Source**: Full transparency in code and data handling
- **User Control**: You own your data and behavior patterns

## 🤝 Contributing

We welcome contributions from makers, developers, and caring humans! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Code contribution guidelines
- Hardware design improvements
- Documentation enhancements
- Community support

## 📋 Roadmap

### v1.0 - Core Companion (Current)
- [x] Hardware assembly guides
- [x] Basic behavioral recognition
- [x] LED mood expressions
- [x] Text-to-speech personality

### v1.1 - Enhanced Intelligence
- [ ] Improved activity detection accuracy
- [ ] Learning algorithm refinements
- [ ] Voice command recognition
- [ ] Multiple user support

### v2.0 - Community Features
- [ ] Mobile companion app
- [ ] Community personality packs
- [ ] Integration APIs
- [ ] Advanced customization tools

## 🏆 Community Showcase

Share your Pixel Plant builds, customizations, and improvements:

- **[Gallery](docs/community/gallery.md)** - Community builds and modifications
- **[Success Stories](docs/community/stories.md)** - How the Pixel Plant helped users
- **[Variations](docs/community/variations.md)** - Creative implementations

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Becky Chambers** for the inspiring vision in "The Long Way to a Small, Angry Planet"
- **Espressif Systems** for the powerful ESP32-S3 platform
- **Arduino Community** for the accessible development ecosystem
- **Open Source Contributors** making caring technology possible

## 📞 Support

- **Documentation**: Check our [comprehensive guides](docs/)
- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/your-username/pixel-plant/issues)
- **Discussions**: Join community conversations in [GitHub Discussions](https://github.com/your-username/pixel-plant/discussions)
- **Community**: Connect with other builders and share your experience

---

**Ready to build technology that truly cares? Let's create the future, one caring companion at a time.** 🌟

*"The best technology doesn't just work—it cares."* - The Pixel Plant Philosophy