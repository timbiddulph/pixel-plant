# Pixel Plant Development Environment Setup

> Complete guide to setting up your development environment for the Pixel Plant AI Companion

## 🎯 Quick Start

**Time to setup**: ~45 minutes
**Skill level**: Beginner friendly
**Platform**: Raspberry Pi Zero 2 W (development machine can be Windows, macOS, or Linux)

### Prerequisites
- Raspberry Pi Zero 2 W with power supply (5V 2.5A)
- 32GB microSD card (Class 10 or better)
- Pi Camera Module (CSI interface)
- Computer with SD card reader
- WiFi network access

## 📥 Step 1: Flash Raspberry Pi OS

### Download Raspberry Pi Imager
1. **Visit**: [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)
2. **Download**: Raspberry Pi Imager for your OS
3. **Install**: Run the installer

### Flash the SD Card
1. **Insert** microSD card into your computer
2. **Open** Raspberry Pi Imager
3. **Choose OS**: Raspberry Pi OS Lite (64-bit) - *No desktop environment needed*
4. **Choose Storage**: Select your microSD card
5. **Click the gear icon** ⚙️ for advanced options:

### Advanced Configuration (Important!)
```
Hostname: pixelplant.local
Enable SSH: Yes (use password authentication)
Set username and password:
  - Username: pi
  - Password: (choose a secure password)
Configure wireless LAN:
  - SSID: (your WiFi network name)
  - Password: (your WiFi password)
  - Country: (your country code, e.g., GB)
Set locale settings:
  - Timezone: (your timezone)
  - Keyboard: (your layout)
```

6. **Click Write** and wait for completion (~10 minutes)

## 🔧 Step 2: First Boot & SSH Access

### Power On Pi Zero 2 W
1. **Insert** flashed SD card into Pi
2. **Connect** camera module to CSI port (metal contacts facing board)
3. **Power on** via micro USB
4. **Wait** 2-3 minutes for first boot

### Connect via SSH
From your development machine:

```bash
# macOS/Linux
ssh pi@pixelplant.local

# Windows (PowerShell)
ssh pi@pixelplant.local

# If hostname doesn't resolve, find IP via router admin page
ssh pi@192.168.x.x
```

### Initial System Update
```bash
# Update package lists
sudo apt update

# Upgrade installed packages
sudo apt upgrade -y

# Install essential tools
sudo apt install -y git vim python3-pip python3-venv
```

## ⚙️ Step 3: Enable Hardware Interfaces

### Run Raspberry Pi Configuration
```bash
sudo raspi-config
```

Navigate using arrow keys:

1. **Interface Options → Camera** → Enable
2. **Interface Options → I2C** → Enable (for future sensors)
3. **Interface Options → SPI** → Enable (for future expansion)
4. **Performance → GPU Memory** → Set to 128MB (camera needs this)

**Reboot** when prompted:
```bash
sudo reboot
```

### Configure I2S Audio (MAX98357A)
After reboot, SSH back in and edit boot config:

```bash
sudo nano /boot/config.txt
```

Add these lines at the end:
```
# Enable I2S audio for MAX98357A
dtoverlay=hifiberry-dac
dtoverlay=i2s-mmap
```

Disable onboard audio (optional but recommended):
```
# Comment out or remove:
# dtparam=audio=on
```

Save (Ctrl+O, Enter) and exit (Ctrl+X).

### Verify Camera
```bash
# Test camera detection
libcamera-hello --list-cameras

# Should show your camera model (OV5647 or IMX219)
```

## 📚 Step 4: Clone Project and Setup Python Environment

### Clone the Repository
```bash
cd ~
git clone https://github.com/your-username/pixel-plant.git
cd pixel-plant
```

### Create Python Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Verify Python version (should be 3.9+)
python --version
```

### Install System Dependencies
```bash
# Install required system packages for OpenCV, audio, and LEDs
sudo apt install -y \
  libopencv-dev \
  python3-opencv \
  libatlas-base-dev \
  libhdf5-dev \
  libjasper-dev \
  libqtgui4 \
  libqt4-test \
  espeak \
  libespeak-dev \
  portaudio19-dev \
  python3-pyaudio
```

### Install Python Packages
```bash
# Ensure pip is up to date
pip install --upgrade pip

# Install from requirements.txt
pip install -r requirements.txt
```

Example `requirements.txt`:
```
# Core ML/Vision
numpy>=1.21.0
opencv-python-headless>=4.5.0
tflite-runtime>=2.5.0
mediapipe>=0.8.0

# Camera
picamera2>=0.3.0

# Hardware Control
rpi-ws281x>=4.3.0  # LED strip control
RPi.GPIO>=0.7.1    # GPIO access
adafruit-circuitpython-neopixel>=6.0.0

# Audio/TTS
pyttsx3>=2.90
pyaudio>=0.2.11

# Utilities
pyyaml>=6.0
schedule>=1.1.0
```

**Note**: Some packages (like tflite-runtime and mediapipe) may take 10-20 minutes to install on Pi Zero 2 W.

## 🧪 Step 5: Hardware Testing

### LED Strip Test
```bash
# Ensure you're in virtual environment
source ~/pixel-plant/venv/bin/activate

# Run LED test (requires sudo for GPIO access)
sudo venv/bin/python examples/test_leds.py
```

### Camera Test
```bash
# Test camera capture
python examples/test_camera.py
```

### Audio Test
```bash
# Test text-to-speech
python examples/test_audio.py
```

### PIR Sensor Test
```bash
sudo venv/bin/python examples/test_pir.py
```

## 🔍 Step 6: Development Workflow

### Remote Development Options

#### Option 1: SSH + Command Line Editor
```bash
# Edit files directly on Pi
nano src/main.py
vim src/main.py
```

#### Option 2: VS Code Remote SSH (Recommended)
1. Install VS Code on your development machine
2. Install "Remote - SSH" extension
3. Connect: `Ctrl/Cmd+Shift+P` → "Remote-SSH: Connect to Host"
4. Enter: `pi@pixelplant.local`
5. Open folder: `/home/pi/pixel-plant`

#### Option 3: SSHFS Mount (macOS/Linux)
```bash
# Mount Pi filesystem locally
mkdir ~/pixelplant-remote
sshfs pi@pixelplant.local:/home/pi/pixel-plant ~/pixelplant-remote

# Edit with your local editor
code ~/pixelplant-remote
```

### Daily Development Cycle
```bash
# 1. SSH into Pi
ssh pi@pixelplant.local

# 2. Activate virtual environment
cd ~/pixel-plant
source venv/bin/activate

# 3. Pull latest changes
git pull origin main

# 4. Run the application
sudo venv/bin/python src/main.py

# 5. Test changes, iterate
# Ctrl+C to stop, edit code, run again

# 6. Commit your work
git add .
git commit -m "Add caring hydration reminders"
git push origin your-branch
```

### Code Organization Best Practices
- **Keep functions small** - max 50 lines
- **Use descriptive names** - `show_caring_animation()` not `anim1()`
- **Type hints** - Use Python type annotations for clarity
- **Docstrings** - Document all functions and classes
- **Test on hardware frequently** - don't write too much without testing

### Debugging Tools
1. **Print statements**: Quick and effective
2. **Python debugger**: `import pdb; pdb.set_trace()`
3. **Logging**: Use Python's logging module for production
4. **Remote debugging**: VS Code debugger via SSH

## 🚨 Common Issues & Solutions

### Camera Not Detected
**Problem**: `libcamera-hello` shows no cameras
**Solutions**:
- Check CSI cable connection (metal contacts face PCB)
- Ensure cable is fully seated in both connectors
- Run `sudo raspi-config` and enable camera interface
- Check GPU memory is set to 128MB
- Reboot after configuration changes

### LED Strip Not Working
**Problem**: No lights or incorrect colors
**Solutions**:
```python
# Must run with sudo for GPIO access
sudo venv/bin/python test_leds.py

# Check wiring:
# - Data: GPIO 18 (pin 12)
# - Power: 5V (pin 2 or 4)
# - Ground: GND (pin 6)
```

### Audio Not Working
**Problem**: No sound from speaker
**Solutions**:
- Check I2S configuration in `/boot/config.txt`
- Verify MAX98357A wiring (BCLK, LRCLK, DIN pins)
- Test with `speaker-test -t sine -f 440`
- Ensure audio device is listed: `aplay -l`

### Out of Memory Errors
**Problem**: Python crashes with memory errors
**Solutions**:
```bash
# Check available memory
free -h

# Create swap file (if needed)
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Set CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### WiFi Connection Issues
**Problem**: Pi loses WiFi connection
**Solutions**:
```bash
# Check connection status
iwconfig wlan0

# Reconnect
sudo systemctl restart dhcpcd

# Set static IP (in /etc/dhcpcd.conf)
interface wlan0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8
```

### Permission Errors
**Problem**: "Permission denied" for GPIO
**Solutions**:
```bash
# Run with sudo
sudo venv/bin/python src/main.py

# Or add user to gpio group
sudo usermod -a -G gpio,i2c,spi pi
# Then logout and back in
```

## ⚡ Performance Optimization

### Memory Management
```python
# Use generators for large data
def process_frames():
    for frame in camera.capture_continuous():
        yield process_frame(frame)

# Clear unused variables
del large_array
import gc
gc.collect()

# Monitor memory usage
import psutil
print(f"Memory: {psutil.virtual_memory().percent}%")
```

### CPU Optimization
```python
# Use NumPy operations (vectorized)
import numpy as np
result = np.mean(frame, axis=2)  # Fast

# Avoid Python loops for pixel operations
# BAD:
for y in range(height):
    for x in range(width):
        pixel = frame[y, x]

# GOOD:
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```

### Reduce Frame Processing
```python
# Skip frames for faster processing
frame_skip = 3
frame_count = 0

for frame in camera.capture_continuous():
    frame_count += 1
    if frame_count % frame_skip != 0:
        continue
    # Process frame
```

## 🔧 Production Setup

### Create Systemd Service
```bash
sudo nano /etc/systemd/system/pixel-plant.service
```

Add:
```ini
[Unit]
Description=Pixel Plant AI Companion
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/pi/pixel-plant
ExecStart=/home/pi/pixel-plant/venv/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable pixel-plant
sudo systemctl start pixel-plant

# Check status
sudo systemctl status pixel-plant

# View logs
sudo journalctl -u pixel-plant -f
```

### Auto-restart on Crash
The systemd service with `Restart=always` handles this automatically.

## 🌐 Version Control Integration

### Git Workflow for Python
```bash
# Recommended .gitignore
__pycache__/
*.pyc
*.pyo
venv/
.vscode/
*.egg-info/
dist/
build/
.DS_Store
*.log
config/local_config.yaml
```

### Branch Strategy
- **main**: Stable releases
- **develop**: Integration branch
- **feature/caring-reminders**: Feature branches
- **hotfix/audio-volume**: Critical fixes

## 🤝 Contributing Guidelines

### Code Style
```python
# Use snake_case for variables and functions
current_mood = Mood.HAPPY

# Use descriptive function names
def show_caring_reminder(message: str) -> None:
    """Display a caring reminder with appropriate LED animation.

    Args:
        message: The caring message to speak to the user
    """
    # Implementation

# Include caring philosophy in comments
# This gentle animation helps users feel supported
# without being overwhelming or demanding
```

### Type Hints
```python
from typing import Optional, List

def get_reminder(mood: Mood, category: str) -> Optional[str]:
    """Get appropriate reminder for mood and category."""
    pass
```

### Pull Request Checklist
- [ ] Code passes linting (flake8/pylint)
- [ ] Type hints included
- [ ] Hardware tested on actual Pi
- [ ] Documentation updated
- [ ] Caring philosophy maintained
- [ ] No hardcoded secrets

## 🆘 Getting Help

### Community Resources
- **GitHub Issues**: Technical problems and bugs
- **GitHub Discussions**: General questions and ideas
- **Raspberry Pi Forums**: Pi-specific technical issues
- **r/raspberry_pi**: Reddit community support

### Documentation
- **API Reference**: `/docs/software/api.md`
- **Hardware Guide**: `/docs/hardware/assembly.md`
- **Troubleshooting**: `/docs/troubleshooting.md`

---

## ✅ Verification Checklist

Before you start developing:
- [ ] Raspberry Pi OS flashed and booting
- [ ] SSH access working
- [ ] Camera interface enabled and detected
- [ ] I2S audio configured
- [ ] Python virtual environment created
- [ ] All required packages installed
- [ ] LED test script runs successfully
- [ ] Camera test captures images
- [ ] Audio test plays sounds
- [ ] Git repository cloned
- [ ] VS Code Remote SSH configured (optional)

**Ready to build caring technology!** 🌿✨

*"The best development environment is one that gets out of your way so you can focus on creating technology that truly cares."*

---

*Last updated: November 2024*
*If you find issues with this setup guide, please report them on GitHub Issues*
