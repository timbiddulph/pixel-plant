# Pixel Plant - Quick Start Guide

## 🚀 For Immediate Testing (Development Machine)

You can test the Pixel Plant software in **simulation mode** on your Mac/PC before deploying to Raspberry Pi:

### 1. Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install basic dependencies (simulation doesn't need Pi-specific libs)
pip install PyYAML numpy
```

### 2. Test Configuration

```bash
# Test that config loads properly
python src/config.py
```

### 3. Test Individual Components

```bash
# Test LED matrix (simulated - prints to console)
python examples/test_leds.py

# Test all hardware (simulated)
python examples/test_all_hardware.py
```

### 4. Run Main Application (Simulated)

```bash
# Enable simulation mode in config/config.yaml
# Set: debug.simulate_hardware: true

python src/main.py
```

---

## 🔧 For Raspberry Pi Deployment

### 1. Transfer Files to Raspberry Pi

```bash
# From your development machine
scp -r pixel-plant pi@raspberrypi.local:~/
```

### 2. Run Setup Script

```bash
# On Raspberry Pi
cd ~/pixel-plant
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 3. Reboot

```bash
sudo reboot
```

### 4. Test Hardware

```bash
cd ~/pixel-plant
source venv/bin/activate

# Test individual components
python examples/test_leds.py --real
python examples/test_all_hardware.py --real
```

### 5. Run Application

```bash
# Manual start
python src/main.py

# Or enable auto-start
sudo cp config/pixel-plant.service /etc/systemd/system/
sudo systemctl enable pixel-plant
sudo systemctl start pixel-plant

# Check status
sudo systemctl status pixel-plant

# View logs
sudo journalctl -u pixel-plant -f
```

---

## 📁 Project Structure

```
pixel-plant/
├── src/
│   ├── main.py              ← Main application entry point
│   ├── config.py            ← Configuration management
│   ├── hardware/            ← Hardware abstraction layer
│   │   ├── led_matrix.py
│   │   ├── audio.py
│   │   ├── camera.py
│   │   └── motion.py
│   ├── personality/         ← Caring personality system
│   │   ├── messages.py
│   │   ├── mood.py
│   │   ├── animations.py
│   │   └── pixel_art.py
│   └── ai/                  ← Behavioral monitoring
│       ├── behavior_monitor.py
│       └── pattern_learning.py
├── config/
│   ├── config.yaml          ← Main configuration file
│   └── pixel-plant.service  ← Systemd service file
├── examples/
│   ├── test_leds.py         ← LED matrix test
│   └── test_all_hardware.py ← Complete hardware test
├── scripts/
│   └── setup.sh             ← Raspberry Pi setup script
└── requirements.txt         ← Python dependencies
```

---

## ⚙️ Configuration

Edit [config/config.yaml](config/config.yaml) to customize:

- **Hardware pins**: GPIO assignments for LED, audio, PIR
- **Behavior thresholds**: Sitting time, hydration intervals
- **Personality settings**: Caring level, voice preferences
- **Animation styles**: Transition effects, breathing speed
- **Debug options**: Simulation mode, console visualization

---

## 🧪 Testing Modes

### Simulation Mode (Development)
- No hardware required
- Prints to console
- Fast iteration
- Set `debug.simulate_hardware: true`

### Real Hardware Mode (Raspberry Pi)
- Requires physical components
- Full functionality
- Use `--real` flag on test scripts
- Set `debug.simulate_hardware: false`

---

## 🎨 Customization

### Add New Messages
Edit [src/personality/messages.py](src/personality/messages.py)

### Create New LED Patterns
Edit [src/personality/pixel_art.py](src/personality/pixel_art.py)

### Adjust Caring Behavior
Edit [config/config.yaml](config/config.yaml) - `behavior` and `personality` sections

---

## 🐛 Troubleshooting

### Config won't load
```bash
pip install PyYAML
```

### Hardware not detected
```bash
# Check GPIO access
groups  # Should include 'gpio'

# Check camera
vcgencmd get_camera

# Check I2S audio
aplay -l
```

### Permission errors
```bash
sudo usermod -a -G gpio,i2c,spi pi
sudo reboot
```

---

## 📚 Next Steps

1. **Test in simulation** - Verify software works on your machine
2. **Assemble hardware** - Follow [docs/hardware/assembly.md](docs/hardware/assembly.md)
3. **Deploy to Pi** - Use setup script
4. **Validate hardware** - Run test scripts with `--real`
5. **Customize** - Adjust personality, messages, animations
6. **Share!** - Show us your build in GitHub Discussions

---

**Happy building!** 🌿✨
