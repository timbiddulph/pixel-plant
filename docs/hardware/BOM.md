# Bill of Materials (BOM)

## Core Components

### Main Processing Unit
| Component | Description | Quantity | Price (£) | Supplier | Notes |
|-----------|-------------|----------|-----------|----------|-------|
| Raspberry Pi Zero 2 W | Quad-core ARM Cortex-A53 @ 1GHz, 512MB RAM | 1 | £15.00 | The Pi Hut/Pimoroni | Built-in WiFi and Bluetooth |
| 32GB microSD Card | Class 10 or better | 1 | £8.00 | Various | For OS and application storage |

### Camera
| Component | Description | Quantity | Price (£) | Supplier | Notes |
|-----------|-------------|----------|-----------|----------|-------|
| Pi Camera Module | CSI interface camera | 1 | £10-25 | Various | **Option 1**: Pi Camera Module 2 (8MP) - £25<br>**Option 2**: Pi Camera Module 1.3 (5MP used) - £10-15<br>**Option 3**: Generic OV5647 module - £10-12 |

### Display & Visual Output
| Component | Description | Quantity | Price (£) | Supplier | Notes |
|-----------|-------------|----------|-----------|----------|-------|
| 8x8 LED Matrix | WS2812B RGB LED Matrix (64 LEDs) | 1 | £8-12 | Various | 5V addressable matrix, connects to GPIO 18, enables 2D personality expressions |

### Audio System
| Component | Description | Quantity | Price (£) | Supplier | Notes |
|-----------|-------------|----------|-----------|----------|-------|
| Adafruit I2S Audio Amplifier | MAX98357A Class D | 1 | £5.70 | Adafruit/Pimoroni | 3W mono amplifier, I2S interface |
| 40mm Speaker | 4 Ohm 3 Watt with wires | 1 | £4.00 | Various | Full range driver |

### Sensors
| Component | Description | Quantity | Price (£) | Supplier | Notes |
|-----------|-------------|----------|-----------|----------|-------|
| Mini PIR Sensor | BL412 Motion Detection | 1 | £1.90 | Various | 3.3V compatible |

### Electronic Components
| Component | Description | Quantity | Price (£) | Supplier | Notes |
|-----------|-------------|----------|-----------|----------|-------|
| Resistor Kit | 575-piece assorted resistors | 1 | £6.00 | Various | 1/4W through-hole |

### **Total Core Cost: £55-68 + ~£4 shipping = £59-72**
*(Price varies based on camera choice: budget OV5647 ~£59, official Camera Module 2 ~£72)*

## Optional Components

### Power Management
| Component | Description | Quantity | Price (£) | Supplier | Notes |
|-----------|-------------|----------|-----------|----------|-------|
| 5V 2.5A Power Supply | Official Pi power supply (micro USB) | 1 | £8-12 | The Pi Hut/Pimoroni | Recommended for stable operation |
| Power Bank | 10000mAh+ with 2.5A output | 1 | £15-30 | Various | For portable operation (~6+ hours) |
| Power Switch | Inline USB switch | 1 | £3-5 | Various | Easy power control |

### Enhanced Sensing
| Component | Description | Quantity | Price (£) | Supplier | Notes |
|-----------|-------------|----------|-----------|----------|-------|
| BME280 | Temperature/Humidity/Pressure | 1 | £5-8 | Various | I2C environmental monitoring |
| Light Sensor | BH1750 or similar | 1 | £3-5 | Various | I2C ambient light detection |
| Heatsink | Aluminum heatsink for Pi Zero | 1 | £2-4 | Various | Better thermal performance |

### Connectivity & Debug
| Component | Description | Quantity | Price (£) | Supplier | Notes |
|-----------|-------------|----------|-----------|----------|-------|
| Micro USB OTG Adapter | For keyboard/USB device connection | 1 | £3-5 | Various | Initial setup and debugging |
| Mini HDMI Adapter | For display output | 1 | £3-5 | Various | Optional, useful for debugging |
| CSI Camera Cable | 15-pin flat flex cable | 1 | £3-5 | Various | Extra length if needed |

## Tools Required

### Essential Tools
| Tool | Purpose | Estimated Cost |
|------|---------|----------------|
| Soldering Iron | Component assembly | £15-50 |
| Solder | 60/40 or lead-free | £5-10 |
| Wire Strippers | Cable preparation | £10-20 |
| Multimeter | Testing and debugging | £15-40 |

### Helpful Tools
| Tool | Purpose | Estimated Cost |
|------|---------|----------------|
| Breadboard | Prototyping | £5-10 |
| Jumper Wires | Connections | £5-10 |
| Hot Glue Gun | Strain relief | £5-15 |
| 3D Printer Access | Enclosure printing | £200+ or makerspace |

## Assembly Hardware

### Mechanical Components
| Component | Description | Quantity | Price (£) | Notes |
|-----------|-------------|----------|-----------|-------|
| M3 Screws | Various lengths 6-20mm | 10-20 | £3-5 | For enclosure assembly |
| M3 Nuts | Standard hex nuts | 10-20 | £2-3 | Enclosure hardware |
| Standoffs | M3 threaded, 10-15mm | 4-8 | £3-5 | PCB mounting |

### Wiring & Connections
| Component | Description | Quantity | Price (£) | Notes |
|-----------|-------------|----------|-----------|-------|
| Hookup Wire | 22-24 AWG stranded | 5m+ | £5-10 | Various colors |
| JST Connectors | 2.54mm pitch | 10+ | £5-10 | Modular connections |
| Heat Shrink Tubing | Assorted sizes | 1 pack | £5 | Wire protection |

## Enclosure Materials

### 3D Printing (Recommended)
| Material | Properties | Cost per kg | Notes |
|----------|------------|-------------|-------|
| PLA | Easy to print, eco-friendly | £15-25 | Good for desktop use |
| PETG | Stronger, clear options | £20-30 | Better durability |
| TPU | Flexible, shock absorbing | £25-35 | For gaskets/padding |

### Alternative Enclosures
| Option | Description | Estimated Cost | Notes |
|--------|-------------|----------------|-------|
| Project Box | Plastic enclosure | £5-15 | Requires modification |
| Laser Cut Acrylic | Custom design | £10-25 | Professional appearance |
| Wooden Box | Natural materials | £10-20 | Maker aesthetic |

## Supplier Recommendations

### UK Suppliers
- **Pimoroni**: Excellent service, maker-focused
- **The Pi Hut**: Good prices, wide selection  
- **RS Components**: Professional grade, fast delivery
- **Farnell**: Comprehensive catalog
- **Amazon**: Quick delivery, basic components

### International Suppliers
- **Adafruit**: Original designs, excellent tutorials
- **SparkFun**: High quality, good documentation
- **DFRobot**: Innovative modules, competitive pricing
- **AliExpress**: Budget options (longer shipping)

## Cost Optimization Tips

### Budget Build (~£52)
- Use generic OV5647 camera module instead of official Camera Module 2
- Use generic 8x8 WS2812B matrix instead of Adafruit NeoPixel
- Source resistors locally or use salvaged components
- 3D print enclosure at local makerspace
- Use breadboard for initial prototyping

### Professional Build (~£90)
- Official Pi Camera Module 2 (8MP)
- Include power bank for portability
- Add environmental sensors (BME280)
- Use premium connectors and wiring
- Professional heatsink solution

### Educational/Workshop Build (~£50)
- Bulk order Pi Zero 2 W units
- Generic OV5647 cameras (bulk pricing)
- Use common/standardized components
- Simplified assembly process
- Focus on learning objectives

## Availability Notes

### In Stock Usually
- Raspberry Pi Zero 2 W (check stock - can sell out)
- Generic OV5647 camera modules
- LED strips and basic components
- Common sensors and modules
- microSD cards

### Potential Supply Issues
- Pi Camera Module 2 (official) - popular item
- Raspberry Pi Zero 2 W - can be in high demand
- MAX98357A amplifier boards (check stock)

### Substitution Guidelines
- **Raspberry Pi Zero 2 W**: Pi 3A+ works but larger/more expensive; Pi Zero 1 NOT recommended (too slow for AI)
- **Pi Camera**: Any CSI-compatible camera; OV5647 and IMX219 sensors are well-supported
- **8x8 WS2812B Matrix**: Any 5V addressable LED matrix (Adafruit NeoPixel 8x8, generic WS2812B matrix, SK6812 matrix)
- **MAX98357A**: Other I2S amplifiers or PWM audio via GPIO (lower quality)
- **40mm Speaker**: 8 Ohm speakers with proper power rating (adjust amp settings)

## Quality Considerations

### Component Grades
- **Prototype**: Basic functionality, temporary assembly
- **Production**: Reliable operation, permanent installation  
- **Commercial**: Extended warranty, certified components

### Testing Requirements
- All components should be tested individually
- Verify power consumption before final assembly
- Check thermal performance under load
- Validate communication protocols

---

*Last updated: December 2024*
*Prices are estimates and may vary by supplier and region*