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
**Core System**: DFRobot FireBeetle 2 ESP32-S3 with Camera (External Antenna)
- **ESP32-S3-WROOM-1-N16R8** with AI acceleration capabilities
- **16MB Flash + 8MB PSRAM** for sophisticated AI model storage
- **OV2640 2MP camera** (68° FOV) for behavioral monitoring
- **External WiFi antenna** for reliable connectivity and future expansions

### Component Breakdown
**Ordered Components** (£53.00 total):
- FireBeetle 2 ESP32-S3 with Camera - External Antenna (£20.10)
- Flexible RGB LED Strip 60 LED/Metre - 1m Black (£11.40)
- Adafruit I2S 3W Class D Amplifier - MAX98357A (£5.70)
- 40mm Speaker - 4 Ohm 3 Watt with wires (£4.00)
- Mini Basic PIR Sensor - BL412 (£1.90)
- 575-Piece Ultimate Resistor Kit (£6.00)
- Shipping: £3.90

### System Integration
```
┌─────────────────────────────────────────┐
│           ESP32-S3 Core System          │
├─────────────────────────────────────────┤
│  • AI Behavioral Recognition           │
│  • Text-to-Speech Processing           │
│  • LED Animation Control               │
│  • Sensor Data Fusion                  │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼───┐    ┌────▼───┐    ┌───▼────┐
│Camera │    │ Audio  │    │  LEDs  │
│Vision │    │ Output │    │Display │
│       │    │        │    │        │
│OV2640 │    │MAX98357│    │WS2812B │
│ 2MP   │    │+ Spkr  │    │60 LEDs │
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

### Phase 1: Hardware Setup & Basic Testing (Week 1)
- **Component Integration**: Wire all systems on breadboard
- **Individual System Tests**: Verify camera, LEDs, audio independently
- **Power Distribution**: Ensure stable 5V/3.3V supply to all components
- **Basic Connectivity**: Arduino IDE setup and ESP32-S3 programming environment

### Phase 2: Software Foundation (Week 2)
- **LED Animation System**: Implement mood-based color patterns and expressions
- **Audio Output**: Basic text-to-speech with personality variations
- **Camera Integration**: Image capture and basic computer vision setup
- **Sensor Fusion**: Combine PIR sensor with camera-based detection

### Phase 3: AI Implementation (Week 3)
- **Behavioral Recognition Models**: Deploy TensorFlow Lite for activity detection
- **Learning Algorithm**: Track patterns and adapt reminder timing
- **Personality Engine**: Implement mood states and context-aware responses
- **Health Monitoring**: Activity tracking with gentle reminder system

### Phase 4: Refinement & Enclosure (Week 4-5)
- **User Testing**: Fine-tune AI sensitivity for specific workspace
- **Response Optimization**: Refine speech patterns and visual expressions
- **Enclosure Design**: 3D printable desktop housing with professional appearance
- **Final Integration**: Move from breadboard to permanent assembly

## 📝 Development Guidelines

### Code Organization
```
pixel-plant/
├── firmware/                 # ESP32-S3 Arduino code
│   ├── src/
│   │   ├── main.cpp         # Main application loop
│   │   ├── ai/              # Behavioral recognition & learning
│   │   ├── personality/     # Mood system & response generation
│   │   ├── hardware/        # Hardware abstraction layer
│   │   └── utils/           # Helper functions
│   └── libraries/           # Custom libraries
├── hardware/                # Wiring diagrams & schematics
├── enclosure/              # 3D printing files & assembly guides
├── docs/                   # Technical documentation & build guides
├── examples/               # Basic test code & demos
└── tools/                  # Development utilities
```

### Programming Approach
- **Arduino IDE Compatible**: Use familiar development environment
- **Modular Design**: Separate AI, personality, and hardware layers
- **Privacy-First**: All processing on-device, minimal cloud dependency
- **Open Source**: MIT license for community contributions and learning

### AI Framework Integration
- **TensorFlow Lite Micro**: For on-device behavioral recognition
- **EdgeImpulse**: Model training and deployment pipeline
- **ESP-WHO Framework**: Espressif's AI vision toolkit for face detection
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
- **Real-time Operation**: <100ms response time for behavioral changes
- **Battery Efficiency**: Optional battery backup for 6+ hour operation
- **Memory Management**: Efficient use of 8MB PSRAM for AI models
- **Thermal Management**: Stable operation in typical office environments

### Connectivity Features
- **WiFi Integration**: Over-the-air updates and cloud model deployment
- **Local Processing**: Core functionality works offline
- **External Antenna**: Reliable connection for future expansions
- **I2S Audio**: High-quality digital audio output

### Expansion Possibilities
- **Voice Interaction**: Wake word detection and voice commands
- **Multiple Users**: Face recognition for personalized responses  
- **Environmental Sensing**: Temperature, humidity, air quality monitoring
- **Integration APIs**: Connect with smart home systems or health tracking apps

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