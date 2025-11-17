# Pixel Plant AI Companion - Project Brief for Claude

## 🌟 Project Overview

This project aims to build a real-world implementation of the "pixel plant" from Becky Chambers' novel "The Long Way to a Small, Angry Planet." The pixel plant is an AI-powered desktop companion that monitors user behavior and provides caring health reminders through personality-rich interactions.

## 📚 Literary Foundation

### Source Material Analysis
The pixel plant appears as a key character development tool in Chambers' novel, representing:

**Core Features from the Book:**
- **Behavioral recognition software** that detects when the user hasn't stood, taken breaks, or been active
- **Health monitoring capabilities** with gentle reminders: "Hey, there! You need to hydrate!" "How about a snack?" "Take a walk! Stretch it out!"
- **Personality-rich responses** that adapt to user emotions and situations
- **Visual display system** with "smiling face and color-changing petals that resembled nothing in nature"
- **Caring companion role** providing emotional support during difficult moments

**Thematic Significance:**
- Represents **found family care** - technology designed to genuinely support human wellbeing
- **Emotional support technology** that provides companionship in solitary work environments
- **Technology vs. Nature** - artificial but psychologically comforting presence
- **Gift economy of care** - small gestures that make challenging work conditions bearable

## 🎯 Project Goals

### Primary Objectives
1. **AI-Powered Behavioral Monitoring**: Real-time analysis of user activity patterns (sitting/standing, movement, presence)
2. **Personality-Rich Interaction**: Varied, caring responses that feel genuine and supportive
3. **Health & Wellness Support**: Proactive reminders for hydration, movement, breaks, and posture
4. **Emotional Companion**: Provides encouragement during difficult work moments
5. **Learning System**: Adapts to user's specific patterns and preferences over time

### Technical Goals
- **On-device AI processing** (no cloud dependency for privacy)
- **Real-time computer vision** for behavioral recognition
- **Natural text-to-speech** with personality variations
- **Expressive LED display** system for visual personality
- **Professional desktop form factor** suitable for office environments

## 🔧 Technical Architecture

### Hardware Platform
**Core System**: Raspberry Pi Zero 2 W
- **Quad-core 64-bit ARM Cortex-A53** @ 1GHz with excellent AI processing capabilities
- **512MB RAM** for sophisticated ML model inference and multitasking
- **Built-in WiFi and Bluetooth** for connectivity and future expansions
- **Full Linux OS** enables rich Python ML ecosystem (TensorFlow, OpenCV, MediaPipe)

**Camera**: Raspberry Pi Camera Module (Official or Compatible)
- **Option 1**: Pi Camera Module 2 (8MP Sony IMX219 sensor) - £25
- **Option 2**: Pi Camera Module 1.3 (5MP OV5647) - £10-15 used
- **Option 3**: Generic OV5647 camera module - £10-12
- **CSI interface** for fast, reliable video capture
- **Recommended**: Generic OV5647 for budget, or Camera Module 2 for best quality

### Component Breakdown
**Core Components** (~£58-71 total):
- Raspberry Pi Zero 2 W (£15)
- Pi Camera Module (£10-25 depending on option)
- 32GB microSD Card Class 10 (£8)
- Flexible RGB LED Strip 60 LED/Metre - 1m Black (£11.40)
- Adafruit I2S 3W Class D Amplifier - MAX98357A (£5.70)
- 40mm Speaker - 4 Ohm 3 Watt with wires (£4.00)
- Mini Basic PIR Sensor - BL412 (£1.90)
- 575-Piece Ultimate Resistor Kit (£6.00)
- Shipping: ~£4

**Power Requirements**:
- 5V 2.5A USB power supply (micro USB)
- Higher current than ESP32-S3 but readily available

### System Integration
```
┌─────────────────────────────────────────┐
│        Raspberry Pi Zero 2 W            │
│         (Linux + Python)                │
├─────────────────────────────────────────┤
│  • TensorFlow/OpenCV/MediaPipe         │
│  • Python ML Behavioral Recognition    │
│  • Text-to-Speech (pyttsx3/espeak)     │
│  • LED Animation Control (rpi_ws281x)  │
│  • Sensor Data Fusion                  │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼───┐    ┌────▼───┐    ┌───▼────┐
│Camera │    │ Audio  │    │  LEDs  │
│Vision │    │ Output │    │Display │
│       │    │        │    │        │
│Pi Cam │    │MAX98357│    │WS2812B │
│5-8 MP │    │+ Spkr  │    │60 LEDs │
│ (CSI) │    │ (I2S)  │    │(GPIO18)│
└───────┘    └────────┘    └────────┘
```

### AI Capabilities
**Behavioral Recognition:**
- **Sitting vs Standing Detection** - Computer vision analysis of posture
- **Activity Pattern Learning** - Tracks movement and work rhythms
- **Presence Detection** - Face detection for desk occupancy
- **Inactivity Monitoring** - Time-based activity tracking
- **Work Session Analysis** - Understands focus periods and natural break points

**Personality System:**
- **Mood States**: Happy, Concerned, Worried, Sleeping
- **Adaptive Responses**: Learns user preferences and effective reminder styles
- **Emotional Context**: Adjusts tone based on detected stress or frustration
- **Varied Speech Patterns**: Multiple phrasings to avoid repetitive interactions

## 🚀 Development Roadmap

### Phase 1: Pi Setup & Basic Testing (Week 1)
- **OS Installation**: Flash Raspberry Pi OS Lite to SD card
- **System Configuration**: Enable camera, I2S audio, configure GPIO
- **Python Environment**: Set up virtual environment with required packages
- **Individual System Tests**: Verify camera, LEDs, audio independently via Python scripts
- **Remote Access**: Configure SSH and (optionally) VNC for headless development

### Phase 2: Software Foundation (Week 2)
- **LED Animation System**: Implement mood-based color patterns using rpi_ws281x library
- **Audio Output**: Configure I2S audio and text-to-speech with pyttsx3 or espeak
- **Camera Integration**: OpenCV/Picamera2 setup for image capture and processing
- **Sensor Fusion**: Combine PIR sensor (RPi.GPIO) with camera-based detection

### Phase 3: AI Implementation (Week 3)
- **Behavioral Recognition Models**: Deploy TensorFlow Lite or MediaPipe for activity detection
- **Learning Algorithm**: Track patterns and adapt reminder timing with Python ML
- **Personality Engine**: Implement mood states and context-aware responses
- **Health Monitoring**: Activity tracking with gentle reminder system

### Phase 4: Refinement & Enclosure (Week 4-5)
- **User Testing**: Fine-tune AI sensitivity for specific workspace
- **Response Optimization**: Refine speech patterns and visual expressions
- **Enclosure Design**: 3D printable desktop housing accommodating Pi Zero 2 W form factor
- **Service Configuration**: Set up systemd service for auto-start on boot
- **Final Integration**: Move from breadboard to permanent assembly

## 📝 Development Guidelines

### Code Organization
```
pixel-plant/
├── src/                      # Python application code
│   ├── main.py              # Main application entry point
│   ├── ai/                  # Behavioral recognition & learning
│   │   ├── behavior_monitor.py
│   │   ├── posture_detector.py
│   │   └── pattern_learner.py
│   ├── personality/         # Mood system & response generation
│   │   ├── personality_engine.py
│   │   └── messages.py
│   ├── hardware/            # Hardware abstraction layer
│   │   ├── camera.py
│   │   ├── led_controller.py
│   │   ├── audio.py
│   │   └── pir_sensor.py
│   └── utils/               # Helper functions
├── tests/                   # Unit and integration tests
├── config/                  # Configuration files
│   └── config.yaml          # System configuration
├── models/                  # Pre-trained ML models
├── scripts/                 # Setup and utility scripts
│   ├── setup.sh            # Initial Pi setup script
│   └── install_deps.sh     # Dependency installation
├── hardware/                # Wiring diagrams & schematics
├── enclosure/              # 3D printing files & assembly guides
├── docs/                   # Technical documentation & build guides
├── examples/               # Basic test code & demos
└── requirements.txt        # Python dependencies
```

### Programming Approach
- **Python 3.9+**: Modern Python with full ML ecosystem access
- **Modular Design**: Separate AI, personality, and hardware layers
- **Privacy-First**: All processing on-device, minimal cloud dependency
- **Open Source**: MIT license for community contributions and learning
- **Systemd Service**: Auto-start on boot for reliable operation

### AI Framework Integration
- **TensorFlow Lite**: Optimized for ARM processors, excellent pose detection
- **MediaPipe**: Google's ML framework for pose estimation and face detection
- **OpenCV**: Computer vision preprocessing and image analysis
- **Picamera2**: Native Pi camera interface with hardware acceleration
- **Custom Models**: Tailored activity recognition for desktop environments

## 🎨 Personality Design Philosophy

### Caring Companion Approach
Drawing from the book's themes, the pixel plant should embody:
- **Genuine Care**: Responses feel authentic, not algorithmic
- **Gentle Persistence**: Reminders are caring, not nagging
- **Emotional Intelligence**: Recognizes when to encourage vs. when to stay quiet
- **Growth-Oriented**: Celebrates small improvements in user habits

### Voice & Tone Guidelines
- **Warm & Encouraging**: "Hey there! You need to hydrate!" 
- **Supportive During Stress**: "Aw, it's not so bad! Give yourself a hug!"
- **Celebratory**: Acknowledges good habits and healthy choices
- **Respectfully Persistent**: Increases concern appropriately with extended inactivity

### Visual Personality (LED Expressions)
- **Happy State**: Gentle green/blue breathing effects
- **Concerned State**: Warm yellow pulsing
- **Worried State**: Urgent orange/red animations  
- **Sleeping State**: Dim blue/purple slow breathing
- **Celebration**: Bright, cheerful color cycling

## 🔬 Technical Specifications

### Performance Requirements
- **Real-time Operation**: <200ms response time for behavioral changes
- **Frame Rate**: 15-25 FPS for pose detection (vs 2-5 FPS on Pi Zero 1)
- **Boot Time**: ~20-30 seconds to operational (trade-off for Linux capabilities)
- **Memory Usage**: Efficient ML model loading within 512MB RAM
- **Thermal Management**: Stable operation in typical office environments (may benefit from small heatsink)

### Power Specifications
- **Idle**: ~120mA @ 5V
- **Active (AI processing)**: ~350mA @ 5V
- **Recommended Supply**: 5V 2.5A (official Pi power supply recommended)
- **Battery Backup**: More challenging than ESP32, requires larger capacity (~10000mAh for 6+ hours)

### Connectivity Features
- **Built-in WiFi**: 2.4GHz 802.11 b/g/n for OTA updates and remote access
- **Bluetooth 4.2**: For future wireless sensor integration
- **Local Processing**: Core functionality works completely offline
- **SSH Access**: Remote development and monitoring
- **I2S Audio**: High-quality digital audio output via GPIO

### Expansion Possibilities
- **Voice Interaction**: Wake word detection using PicoVoice or Snowboy
- **Multiple Users**: Face recognition for personalized responses (MediaPipe FaceMesh)
- **Environmental Sensing**: I2C/SPI sensors for temperature, humidity, air quality
- **Integration APIs**: Flask/FastAPI web service for smart home integration
- **Home Assistant**: Native integration possibilities

## 🌍 Community & Open Source Goals

### Educational Value
- **STEM Learning**: Accessible introduction to AI, computer vision, and embedded systems
- **Maker Community**: Comprehensive build guides for various skill levels
- **Workshop Ready**: Designed for educational environments and maker spaces

### Documentation Standards
- **Step-by-step Guides**: From breadboard prototype to finished product
- **Video Tutorials**: Visual assembly and programming demonstrations  
- **Troubleshooting**: Common issues and solutions
- **Customization Guides**: Adapting the system for different use cases

### Community Contributions
- **Model Training**: Tools for users to train custom behavioral recognition
- **Personality Variations**: Different character personalities and response styles
- **Hardware Variants**: Alternative sensors, displays, and form factors
- **Integration Examples**: Connecting with popular productivity and health apps

## 🎯 Success Metrics

### Functional Goals
- **Behavioral Recognition Accuracy**: 95%+ accuracy for sitting/standing detection
- **User Satisfaction**: Positive feedback on reminder effectiveness and timing
- **Reliability**: 24/7 operation with minimal maintenance
- **Response Variety**: 50+ unique reminder phrases and expressions

### Community Goals  
- **Open Source Adoption**: Active GitHub community with regular contributions
- **Educational Impact**: Used in classrooms and maker workshops
- **Maker Success**: Community members successfully building their own versions
- **Innovation**: Community-driven improvements and feature additions

---

## 🔥 Why This Project Matters

The Pixel Plant represents a new approach to human-computer interaction - technology that genuinely cares about human wellbeing rather than just extracting attention or data. By building this as an open-source project, we're demonstrating how AI can be used to support human flourishing in practical, everyday ways.

This project embodies the optimistic, human-centered technology vision found in Becky Chambers' work: AI that serves as a caring companion, not a replacement for human connection, but a thoughtful support system that helps us be healthier and happier.

**Ready to build technology that truly cares? Let's create the future, one caring companion at a time.** 🌟