# Raspberry Pi Camera Traffic Sign Detection Setup

## Hardware Requirements

### WaveShare Fisheye Lens Camera (I) - Product Code: 22047
- **Sensor**: 5 megapixel OV5647
- **Lens**: Fisheye with 185° field of view (F/2.0, 1.55mm focal length)  
- **Resolution**: 2592×1944 photo, 1080p30/720p60/640x480p60-90 video
- **Size**: 32mm × 32mm
- **Connection**: 15-pin FFC cable (opposite side contact)
- **Power**: Supports 60V flat cable
- **Mounting**: 4 screw holes for IR LED board compatibility

### Raspberry Pi Models
- Compatible with all Raspberry Pi models
- **For Raspberry Pi 5**: Use "Raspberry Pi Camera Cable Standard - Mini - 200mm"
- **For older models**: Use included 15-pin FFC cable

## Physical Setup

### 1. Camera Connection
```bash
# Power off Raspberry Pi
sudo shutdown -h now

# Connect the camera:
# 1. Locate the CSI camera connector on your Pi
# 2. Gently lift the plastic clip
# 3. Insert the flat cable with contacts facing the HDMI port
# 4. Push the plastic clip down to secure
# 5. Power on the Pi
```

### 2. Enable Camera Interface
```bash
# Method 1: Using raspi-config
sudo raspi-config
# Navigate to: Interfacing Options > Camera > Enable

# Method 2: Edit config directly
echo 'start_x=1' | sudo tee -a /boot/config.txt
echo 'gpu_mem=128' | sudo tee -a /boot/config.txt
sudo reboot
```

### 3. Verify Camera Detection
```bash
# List camera devices
sudo dmesg | grep -i camera

# Test camera with libcamera
libcamera-hello --list-cameras

# Expected output should show:
# Available cameras:
# 0 : ov5647 [2592x1944] (/base/soc/i2c0mux/i2c@1/ov5647@36)
```

## Software Installation

### 1. System Updates
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y python3-pip python3-venv git cmake build-essential
sudo apt install -y libcamera-dev libcamera-apps
sudo apt install -y python3-libcamera python3-kms++
```

### 2. Install Miniconda (Recommended)
```bash
# Download and install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
chmod +x Miniconda3-latest-Linux-aarch64.sh
./Miniconda3-latest-Linux-aarch64.sh

# Reload shell or restart terminal
source ~/.bashrc
```

### 3. Create Conda Environment
```bash
# Navigate to TRAFFICSIGN directory
cd ~/ADAS/TRAFFICSIGN

# Create environment from yml file
conda env create -f environment_pi.yml

# Activate environment
conda activate adas-trafficsign-pi
```

### 4. Install Camera-Specific Dependencies
```bash
# Activate the conda environment
conda activate adas-trafficsign-pi

# Install picamera2 (latest camera library)
pip install picamera2[gui]==0.3.12

# Install additional Pi-specific packages
pip install gpiozero RPi.GPIO psutil
```

### 5. Test Camera Installation
```bash
# Test basic camera functionality
python3 -c "
from picamera2 import Picamera2
import time
picam2 = Picamera2()
print('Camera detected successfully!')
picam2.close()
"
```

## Usage

### 1. Basic Traffic Sign Detection
```bash
# Activate environment
conda activate adas-trafficsign-pi

# Run continuous detection (default settings)
python3 pi_camera_detector.py

# Run with custom parameters
python3 pi_camera_detector.py \
  --confidence 0.4 \
  --resolution 1920x1080 \
  --interval 0.5 \
  --duration 60
```

### 2. Command Line Options
```bash
# Available parameters:
--model         # Path to TensorFlow Lite model (default: models/gtsrb_model.lite)
--confidence    # Confidence threshold 0.0-1.0 (default: 0.3)
--resolution    # Camera resolution WxH (default: 1920x1080)
--interval      # Detection interval in seconds (default: 1.0)
--duration      # Session duration in seconds (optional, default: indefinite)
--no-save       # Don't save results to JSON file
```

### 3. Example Commands

#### Continuous Detection (Press Ctrl+C to stop)
```bash
python3 pi_camera_detector.py
```

#### High-Frequency Detection (every 0.5 seconds)
```bash
python3 pi_camera_detector.py --interval 0.5 --confidence 0.4
```

#### 5-Minute Detection Session
```bash
python3 pi_camera_detector.py --duration 300 --resolution 1280x720
```

#### High-Sensitivity Detection
```bash
python3 pi_camera_detector.py --confidence 0.2 --interval 0.3
```

## Camera Optimization for Fisheye Lens

### 1. Fisheye Distortion Handling
The detector automatically applies center-crop preprocessing to reduce fisheye distortion effects:
- Crops to center square region (less distorted area)
- Maintains aspect ratio for better detection accuracy
- Optimized for 185° field of view

### 2. Camera Settings
```python
# The detector applies these optimizations:
- Auto white balance enabled
- Auto exposure enabled  
- 30 FPS frame rate
- RGB888 color format
- Center crop for distortion reduction
```

### 3. Recommended Mounting
- Mount camera horizontally for optimal road sign detection
- Position at dashboard level or higher
- Ensure unobstructed view of road ahead
- Consider vibration dampening for vehicle installation

## Performance Monitoring

### Real-time Output Example:
```
🚦 DETECTED: Stop (Confidence: 0.87) [Detection #15]
   📊 Top predictions:
      1. Stop (0.87)
      2. Yield (0.23)
      3. Priority road (0.12)

⚪ No sign detected [Detection #16] (Time: 145.2ms)

🚦 DETECTED: Speed limit (50km/h) (Confidence: 0.71) [Detection #17]
```

### Performance Metrics:
- **Capture Time**: Camera image acquisition (~10-20ms)
- **Preprocessing**: Image preparation (~5-15ms)  
- **Inference Time**: Model prediction (~50-150ms)
- **Total Time**: Complete detection cycle (~100-200ms)

## Troubleshooting

### Camera Not Detected
```bash
# Check camera connection
sudo dmesg | grep ov5647

# Verify camera interface enabled
sudo raspi-config
# Interface Options > Camera > Enable

# Check for hardware issues
sudo i2cdetect -y 1
# Should show device at address 0x36
```

### Permission Issues
```bash
# Add user to camera group
sudo usermod -a -G video $USER

# Set camera permissions
sudo chmod 666 /dev/video*

# Reboot to apply changes  
sudo reboot
```

### Performance Issues
```bash
# Increase GPU memory
sudo nano /boot/config.txt
# Add: gpu_mem=128

# Check system resources
htop
# Monitor CPU and memory usage during detection
```

### LibCamera Issues
```bash
# Install libcamera development packages
sudo apt install -y libcamera-dev libcamera-apps

# Verify libcamera installation
libcamera-hello --version
```

## Results and Output

### JSON Output Structure:
```json
{
  "detection_summary": {
    "total_detections": 150,
    "successful_detections": 23,
    "success_rate": 15.33,
    "average_capture_time_ms": 12.5,
    "average_inference_time_ms": 89.2,
    "camera_resolution": [1920, 1080],
    "detection_interval_s": 1.0
  },
  "detections": [...]
}
```

### Output Files:
- Results saved to: `output/pi_camera_detection_YYYYMMDD_HHMMSS.json`
- Automatic timestamping for each detection session
- Detailed performance metrics included

## System Integration

### Auto-Start on Boot (Optional)
```bash
# Create systemd service
sudo nano /etc/systemd/system/traffic-sign-detector.service

# Add service configuration:
[Unit]
Description=Traffic Sign Detector
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/ADAS/TRAFFICSIGN
Environment=PATH=/home/pi/miniconda3/envs/adas-trafficsign-pi/bin
ExecStart=/home/pi/miniconda3/envs/adas-trafficsign-pi/bin/python pi_camera_detector.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable service
sudo systemctl enable traffic-sign-detector.service
sudo systemctl start traffic-sign-detector.service
```

## Hardware Specifications Summary

| Specification | Value |
|---------------|-------|
| **Camera Sensor** | OV5647 5MP |
| **Lens Type** | Fisheye F/2.0 |
| **Focal Length** | 1.55mm |
| **Field of View** | 185° diagonal |
| **Max Resolution** | 2592×1944 |
| **Video Modes** | 1080p30, 720p60, 640×480p90 |
| **Interface** | 15-pin CSI |
| **Power** | 5V via Pi |
| **Dimensions** | 32×32mm |

This setup provides real-time traffic sign detection optimized for the wide field of view fisheye lens, with automatic distortion handling and performance monitoring.