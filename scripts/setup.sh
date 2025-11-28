#!/bin/bash
#
# Pixel Plant Setup Script
# Configures Raspberry Pi Zero 2 W for the Pixel Plant AI Companion
#

set -e  # Exit on error

echo "=============================================="
echo "  Pixel Plant AI Companion - Setup Script"
echo "=============================================="
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "⚠️  Warning: Not running on Raspberry Pi"
    echo "This script is designed for Raspberry Pi Zero 2 W"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Step 1/6: Updating system packages..."
echo "--------------------------------------"
sudo apt-get update
sudo apt-get upgrade -y

echo ""
echo "Step 2/6: Installing system dependencies..."
echo "--------------------------------------"
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    libjpeg-dev \
    zlib1g-dev \
    libatlas-base-dev \
    libopenblas-dev \
    espeak \
    portaudio19-dev \
    libhdf5-dev \
    libhdf5-serial-dev \
    libharfbuzz0b \
    libwebp7 \
    libtiff6 \
    libatlas-base-dev \
    libopenjp2-7 \
    libilmbase25

echo ""
echo "Step 3/6: Enabling hardware interfaces..."
echo "--------------------------------------"

# Enable camera
echo "Enabling camera interface..."
sudo raspi-config nonint do_camera 0

# Enable I2S for audio (if not already enabled)
if ! grep -q "dtparam=i2s=on" /boot/config.txt; then
    echo "Enabling I2S audio..."
    echo "dtparam=i2s=on" | sudo tee -a /boot/config.txt
fi

# Configure I2S audio device
if ! grep -q "dtoverlay=i2s-mmap" /boot/config.txt; then
    echo "Configuring I2S audio device..."
    echo "dtoverlay=i2s-mmap" | sudo tee -a /boot/config.txt
fi

echo "✓ Hardware interfaces configured"

echo ""
echo "Step 4/6: Creating Python virtual environment..."
echo "--------------------------------------"

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate venv
source venv/bin/activate

echo ""
echo "Step 5/6: Installing Python dependencies..."
echo "--------------------------------------"

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✓ Python dependencies installed"
else
    echo "⚠️  requirements.txt not found"
fi

echo ""
echo "Step 6/6: Setting up data directories..."
echo "--------------------------------------"

# Create data directory
DATA_DIR="$HOME/.pixel-plant"
mkdir -p "$DATA_DIR"
echo "✓ Data directory created: $DATA_DIR"

# Create models directory
mkdir -p models
echo "✓ Models directory created"

# Create log directory
sudo mkdir -p /var/log
sudo touch /var/log/pixel-plant.log
sudo chown $USER:$USER /var/log/pixel-plant.log
echo "✓ Log file created"

echo ""
echo "=============================================="
echo "✅ Setup complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "  1. Reboot your Raspberry Pi: sudo reboot"
echo "  2. After reboot, test hardware: python examples/test_all_hardware.py --real"
echo "  3. Run the application: python src/main.py"
echo ""
echo "Optional: Enable auto-start on boot"
echo "  sudo cp config/pixel-plant.service /etc/systemd/system/"
echo "  sudo systemctl enable pixel-plant"
echo "  sudo systemctl start pixel-plant"
echo ""
echo "Happy building! 🌿"
