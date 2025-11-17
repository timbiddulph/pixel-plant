# Pixel Plant AI Companion 🌿🤖

> *"Hey, there! You need to hydrate!"* - Your caring AI desktop companion

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Raspberry_Pi_Zero_2_W-red.svg)](https://www.raspberrypi.com/)
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

- Raspberry Pi Zero 2 W
- Pi Camera Module (Official Camera Module 2 or compatible OV5647)
- 32GB microSD Card (Class 10)
- Flexible RGB LED Strip (60 LED/m, WS2812B)
- Adafruit I2S Audio Amplifier (MAX98357A)
- 40mm Speaker (4 Ohm, 3W)
- Mini PIR Sensor (BL412)
- 5V 2.5A Power Supply (micro USB)
- Basic resistors and wiring components

**Total Cost**: ~£58-71 depending on camera choice (see [Bill of Materials](docs/hardware/BOM.md))

### Software Setup

1. **Flash Raspberry Pi OS**
   - Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
   - Flash Raspberry Pi OS Lite (64-bit) to SD card
   - Enable SSH and configure WiFi in Imager settings

2. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/pixel-plant.git
   cd pixel-plant
   ```

3. **Run setup script**
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```
   This will:
   - Enable camera and I2S audio interfaces
   - Install system dependencies
   - Create Python virtual environment
   - Install required Python packages

4. **Start the application**
   ```bash
   source venv/bin/activate
   python src/main.py
   ```

5. **Enable auto-start (optional)**
   ```bash
   sudo cp config/pixel-plant.service /etc/systemd/system/
   sudo systemctl enable pixel-plant
   sudo systemctl start pixel-plant
   ```

## 📖 Documentation

- **[Assembly Guide](docs/hardware/assembly.md)** - Step-by-step hardware setup
- **[Software Architecture](docs/software/architecture.md)** - Code structure and design
- **[API Reference](docs/software/api.md)** - Function and class documentation
- **[Customization Guide](docs/customization/README.md)** - Personalizing your Pixel Plant
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

## 🛠️ Project Structure

```
pixel-plant/
├── src/                     # Python application code
│   ├── main.py             # Main entry point
│   ├── ai/                 # Behavioral recognition & learning
│   ├── personality/        # Mood system & response generation
│   └── hardware/           # Hardware abstraction layer
├── config/                 # Configuration files
├── models/                 # Pre-trained ML models
├── scripts/                # Setup and utility scripts
├── tests/                  # Unit and integration tests
├── hardware/               # Wiring diagrams & schematics
│   ├── schematics/        # Circuit diagrams
│   └── 3d_models/         # Enclosure 3D files
├── docs/                   # Comprehensive documentation
│   ├── hardware/          # Assembly and wiring guides
│   ├── software/          # Code documentation
│   └── customization/     # User customization guides
├── examples/               # Usage examples and test scripts
└── requirements.txt        # Python dependencies
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

- **On-Device Processing**: All AI runs locally on Raspberry Pi Zero 2 W
- **No Cloud Dependency**: Core functionality works completely offline
- **Open Source**: Full transparency in code and data handling
- **User Control**: You own your data and behavior patterns
- **Local Storage**: All learned patterns stored on-device SD card

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
- **Raspberry Pi Foundation** for the powerful and accessible Pi Zero 2 W platform
- **Python Community** for the rich ML ecosystem (TensorFlow, OpenCV, MediaPipe)
- **Open Source Contributors** making caring technology possible

## 📞 Support

- **Documentation**: Check our [comprehensive guides](docs/)
- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/your-username/pixel-plant/issues)
- **Discussions**: Join community conversations in [GitHub Discussions](https://github.com/your-username/pixel-plant/discussions)
- **Community**: Connect with other builders and share your experience

---

**Ready to build technology that truly cares? Let's create the future, one caring companion at a time.** 🌟

*"The best technology doesn't just work—it cares."* - The Pixel Plant Philosophy