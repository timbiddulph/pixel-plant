# VS Code Setup for Pixel Plant Development

> Alternative development environment setup using Visual Studio Code with Arduino extension

## 🎯 Overview

While the Pixel Plant is designed for Arduino IDE, VS Code offers a more powerful development experience with better IntelliSense, debugging, and project management.

**Recommended for**: Experienced developers who prefer VS Code  
**Difficulty**: Intermediate  
**Setup Time**: ~15 minutes

---

## 📥 Step 1: Install VS Code Extensions

### Core Extensions
```bash
# Install via VS Code Extensions panel or command line:
code --install-extension vsciot-vscode.vscode-arduino
code --install-extension ms-vscode.cpptools
code --install-extension twxs.cmake
```

### Essential Extensions
1. **Arduino** by Microsoft - Core Arduino development
2. **C/C++** by Microsoft - IntelliSense and debugging
3. **C/C++ Extension Pack** - Complete C++ toolchain

### Helpful Extensions
```bash
code --install-extension ms-vscode.cmake-tools
code --install-extension platformio.platformio-ide
code --install-extension formulahendry.code-runner
code --install-extension ms-vscode.vscode-json
```

---

## ⚙️ Step 2: Configure Arduino Extension

### Arduino IDE Path Configuration
1. Open VS Code Settings (`Ctrl+,`)
2. Search for "arduino"
3. Set **Arduino: Path** to your Arduino IDE installation:
   - **Windows**: `C:\Program Files (x86)\Arduino` or `C:\Users\[username]\AppData\Local\Programs\Arduino IDE`
   - **macOS**: `/Applications/Arduino.app`
   - **Linux**: `/usr/share/arduino` or `/opt/arduino`

### Board Configuration
1. Open Command Palette (`Ctrl+Shift+P`)
2. Run **Arduino: Board Manager**
3. Install **ESP32 by Espressif Systems**

---

## 🔧 Step 3: Project Configuration

### Create Arduino Project Settings
Create `.vscode/settings.json` in project root:

```json
{
    "arduino.path": "C:/Program Files (x86)/Arduino",
    "arduino.commandPath": "arduino_debug.exe",
    "arduino.logLevel": "info",
    "arduino.enableUSBDetection": true,
    "arduino.disableTestingOpen": false,
    "arduino.skipHeaderProvider": false,
    "arduino.additionalUrls": [
        "https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json"
    ],
    "C_Cpp.intelliSenseEngine": "Tag Parser",
    "C_Cpp.autocomplete": "Enabled"
}
```

### Arduino Configuration
Create `.vscode/arduino.json`:

```json
{
    "sketch": "firmware/pixel_plant/pixel_plant.ino",
    "board": "esp32:esp32:esp32s3",
    "configuration": "CPUFreq=240,FlashMode=qio,FlashSize=16M,PartitionScheme=app3M_fat9M_fact512k_16MB,PSRAM=opi",
    "port": "COM3"
}
```

**Note**: Update `port` to match your ESP32-S3 connection.

### C++ IntelliSense Configuration
Create `.vscode/c_cpp_properties.json`:

```json
{
    "configurations": [
        {
            "name": "ESP32",
            "includePath": [
                "${workspaceFolder}/**",
                "C:/Users/[USERNAME]/AppData/Local/Arduino15/packages/esp32/hardware/esp32/*/cores/esp32/**",
                "C:/Users/[USERNAME]/AppData/Local/Arduino15/packages/esp32/hardware/esp32/*/libraries/**",
                "C:/Users/[USERNAME]/Documents/Arduino/libraries/**",
                "${workspaceFolder}/firmware/pixel_plant/src/**"
            ],
            "defines": [
                "ARDUINO=10819",
                "ARDUINO_ESP32S3_DEV",
                "ESP32",
                "_GNU_SOURCE"
            ],
            "compilerPath": "C:/Users/[USERNAME]/AppData/Local/Arduino15/packages/esp32/tools/xtensa-esp32s3-elf-gcc/*/bin/xtensa-esp32s3-elf-gcc.exe",
            "cStandard": "c11",
            "cppStandard": "c++11",
            "intelliSenseMode": "gcc-x64"
        }
    ],
    "version": 4
}
```

**Important**: Replace `[USERNAME]` with your actual Windows username.

---

## 🚀 Step 4: VS Code Workflow

### Opening the Project
1. **File → Open Folder**
2. Select the `Pixel Plant` root directory
3. VS Code will recognize it as an Arduino project

### Building and Uploading
1. **Verify/Compile**: `Ctrl+Alt+R`
2. **Upload**: `Ctrl+Alt+U`  
3. **Open Serial Monitor**: `Ctrl+Alt+S`

### Command Palette Commands
- `Arduino: Initialize` - Set up new Arduino project
- `Arduino: Verify` - Compile sketch
- `Arduino: Upload` - Upload to board
- `Arduino: Open Serial Monitor` - View serial output
- `Arduino: Change Board Type` - Switch board configuration
- `Arduino: Change Baud Rate` - Adjust serial speed

---

## 🎨 Step 5: Enhanced Development Features

### IntelliSense and Code Completion
VS Code will provide:
- **Auto-completion** for Arduino and ESP32 functions
- **Error highlighting** before compilation
- **Function signatures** and parameter hints
- **Go to definition** for functions and variables

### File Navigation
- **Quick Open**: `Ctrl+P` to jump to any file
- **Symbol Search**: `Ctrl+Shift+O` to find functions/variables
- **Go to Definition**: `F12` on any function call
- **Find References**: `Shift+F12` to see where functions are used

### Debugging Support (Limited)
While full debugging isn't available for ESP32, you get:
- **Serial Monitor Integration**
- **Output Panel** for compilation errors
- **Problem Panel** for syntax issues
- **Task Runner** for custom build scripts

---

## 🔧 Step 6: Hardware-Specific Configuration

### ESP32-S3 Settings
For Pixel Plant hardware, use these settings in Command Palette:

1. **Arduino: Board Config**:
   - Board: "ESP32S3 Dev Module"
   - Upload Speed: "921600"
   - CPU Frequency: "240MHz (WiFi)"
   - Flash Mode: "QIO 80MHz" 
   - Flash Size: "16MB (128Mb)"
   - Partition Scheme: "16M Flash (3MB APP/9MB FATFS)"
   - PSRAM: "OPI PSRAM"

### Port Configuration
1. **Arduino: Select Serial Port**
2. Choose the port showing "ESP32-S3" or "Silicon Labs CP210x"

### Libraries in VS Code
Libraries are managed through Arduino IDE, but VS Code will recognize them for IntelliSense:
- FastLED
- ArduinoJson  
- ESP32-audioI2S

---

## 🧪 Step 7: Testing Your Setup

### Quick Test
1. Open `firmware/examples/led_test/led_test.ino`
2. Press `Ctrl+Alt+R` to verify compilation
3. Connect your ESP32-S3 
4. Press `Ctrl+Alt+U` to upload
5. Press `Ctrl+Alt+S` to open Serial Monitor

### Verify IntelliSense
- Type `FastLED.` and you should see auto-completion
- Hover over functions to see documentation
- `Ctrl+Click` on function names to go to definitions

---

## 🔍 Troubleshooting

### Common Issues

#### "Arduino path not found"
**Solution**: Verify Arduino IDE is installed and path is correct in settings.json

#### "Board not found"  
**Solution**: 
```bash
# In Arduino IDE, install ESP32 board package first
# Then restart VS Code
```

#### "IntelliSense not working"
**Solution**: Update include paths in `c_cpp_properties.json`:
```json
"includePath": [
    "C:/Users/YourUsername/AppData/Local/Arduino15/packages/**",
    "${workspaceFolder}/**"
]
```

#### "Upload failed"
**Solution**: 
- Check COM port in `arduino.json`
- Press BOOT button on ESP32-S3 during upload
- Try lower upload speed (460800 or 115200)

#### "Library not found"
**Solution**: Install libraries through Arduino IDE Library Manager, not VS Code

---

## ⚡ VS Code Advantages for Pixel Plant

### Better Code Organization
- **Multi-file editing** with tabs
- **Split view** for header and implementation files  
- **File explorer** with project tree
- **Integrated terminal** for git operations

### Enhanced Productivity
- **Find and Replace** across entire project
- **Code formatting** with consistent style
- **Git integration** for version control
- **Markdown preview** for documentation

### Advanced Features
- **Code snippets** for common patterns
- **Multiple cursors** for batch editing
- **Bracket matching** and **auto-indentation**
- **Integrated task runner** for custom build scripts

---

## 🎯 Recommended Workflow

### Daily Development
1. **Open project** in VS Code
2. **Edit code** with full IntelliSense support
3. **Verify frequently** with `Ctrl+Alt+R`
4. **Upload and test** with `Ctrl+Alt+U`
5. **Monitor serial** with `Ctrl+Alt+S`
6. **Commit changes** with integrated Git

### Project Management
- Use **Explorer panel** for file navigation
- Use **Search panel** for code search across project
- Use **Source Control panel** for Git operations
- Use **Extensions panel** for additional tools

---

## 📋 Quick Reference

### Essential Shortcuts
| Action | Shortcut |
|--------|----------|
| Verify/Compile | `Ctrl+Alt+R` |
| Upload | `Ctrl+Alt+U` |
| Serial Monitor | `Ctrl+Alt+S` |
| Command Palette | `Ctrl+Shift+P` |
| Quick Open File | `Ctrl+P` |
| Find in Files | `Ctrl+Shift+F` |
| Go to Definition | `F12` |
| Toggle Terminal | `Ctrl+`` ` |

### Arduino Commands
- `Arduino: Verify`
- `Arduino: Upload` 
- `Arduino: Open Serial Monitor`
- `Arduino: Change Board Type`
- `Arduino: Select Serial Port`
- `Arduino: Library Manager`

---

## 🎉 You're Ready!

VS Code is now configured for Pixel Plant development with:
- ✅ Arduino extension properly configured
- ✅ ESP32-S3 board support installed  
- ✅ IntelliSense working for code completion
- ✅ Build and upload workflow established
- ✅ Serial monitor integration

**Switch between Arduino IDE and VS Code as needed** - both will work with the same project files.

---

*"The best development environment is one that gets out of your way so you can focus on creating caring technology."* 🌿✨