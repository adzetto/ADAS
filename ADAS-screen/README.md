# ADAS Display for Raspberry Pi 5 (C++ Qt Version)

This guide provides instructions to set up and autostart a full-screen ADAS display application developed in C++ with the Qt framework on your Raspberry Pi 5. This approach offers better performance and responsiveness compared to Python-based solutions.

## Prerequisites

*   Raspberry Pi 5 (8GB recommended) with Raspberry Pi OS (64-bit) installed.
*   A display connected to your Raspberry Pi.
*   Internet connection for package installation.
*   Basic familiarity with C++ and the command line.

## 1. Install Qt and Build Tools

First, ensure your Raspberry Pi OS is up to date and install the necessary Qt libraries and build tools.

```bash
sudo apt update
sudo apt full-upgrade -y
sudo apt install build-essential qtbase5-dev libqt5widgets5 libqt5gui5 libqt5core5a -y
```

## 2. Place the Application Files

Create a directory for your ADAS display application and place the `adas_display.pro`, `main.cpp`, and `adasdisplay.h` files inside it. For example, in your home directory:

```bash
mkdir -p ~/ADAS-screen
mv adas_display.pro ~/ADAS-screen/
mv main.cpp ~/ADAS-screen/
mv adasdisplay.h ~/ADAS-screen/
```

## 3. Build the Application

Navigate to the `ADAS-screen` directory and build the application using `qmake` and `make`.

```bash
cd ~/ADAS-screen
qmake adas_display.pro
make
```

This will create an executable file named `adas_display` (or similar, depending on your `.pro` file configuration) in the same directory.

## 4. Configure Autostart (Systemd Service)

To make the ADAS display autostart on boot, we will create a `systemd` service.

### Create the Service File

```bash
sudo nano /etc/systemd/system/adas-display.service
```

Paste the following content into the `adas-display.service` file:

```service
[Unit]
Description=ADAS Display Application
After=graphical.target

[Service]
ExecStart=/home/pi/ADAS-screen/adas_display
Restart=always
User=pi
Group=pi
WorkingDirectory=/home/pi/ADAS-screen
Environment=DISPLAY=:0

[Install]
WantedBy=graphical.target
```

**Important:**
*   Replace `/home/pi/ADAS-screen/adas_display` with the actual path to your compiled executable if it's different.
*   Replace `User=pi` and `Group=pi` with your actual Raspberry Pi username if it's not `pi`.

Save the file (Ctrl+O, Enter, Ctrl+X).

### Enable and Start the Service

```bash
sudo systemctl enable adas-display.service
sudo systemctl start adas-display.service
```

To check the status of the service:

```bash
sudo systemctl status adas-display.service
```

## 5. Hide the Desktop Environment (Optional but Recommended)

To achieve a truly "plain like full screen" experience, you might want to disable the graphical desktop environment from starting, and let only your ADAS application run.

```bash
sudo raspi-config
```

Navigate to `System Options` -> `Boot / Auto Login` -> `Desktop Autologin` and select `Console Autologin`.

This will make the Raspberry Pi boot directly into the console, and then your `systemd` service will launch the Qt application on top of it.

## 6. Reboot and Test

Reboot your Raspberry Pi to see the changes:

```bash
sudo reboot
```

Your ADAS display application should now launch automatically in full-screen mode after boot.

## Usage

*   **Dashboard Mode:** Displays simulated LDW, BSD, Speed, TSR, and Auto Light status.
*   **Navigation:**
    *   Press the **Right Arrow key** to simulate the "Forward" button and cycle through display modes (Dashboard -> Rear View Camera -> Race Navigation).
    *   Press the **Left Arrow key** to simulate the "Backward" button and cycle in reverse.
*   **Quit:** Press the **Q key** to exit the application.

## Customization

*   **Visuals:** Modify the `main.cpp` and `adasdisplay.h` files to change fonts, colors, layouts, and integrate actual sensor data.
*   **Functionality:** For physical controls (potentiometer, buttons), you'll need to write C++ code to read GPIO inputs (e.g., using `wiringPi` or `pigpio` libraries) and trigger the appropriate slots or methods in your Qt application.