<div align="center">

# 🚗🔐 3-Factor Embedded Vehicle Security System

**Wi-Fi Proximity Detection · NFC Authentication · Facial Recognition**

A multi-layered embedded vehicle ignition security system built on **Raspberry Pi 5** and **ESP32**, designed to eliminate the vulnerabilities of traditional key-based vehicle access.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-IoT-orange?logo=espressif&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-5-red?logo=raspberrypi&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

</div>

---

## 📖 Overview

Traditional vehicle keys are vulnerable to **theft, duplication, and unauthorized use**. This project implements a **three-factor authentication pipeline** that a vehicle must pass before the ignition system is enabled:

1. 📶 **Wi-Fi Proximity Detection** — confirms the owner's registered device is nearby
2. 💳 **NFC Authentication** — verifies a registered NFC tag's UID
3. 👤 **Facial Recognition** — confirms the driver's identity via camera

The Raspberry Pi 5 acts as the central controller, orchestrating the ESP32, NFC reader, camera, and OLED display through each authentication stage before granting ignition access.

---

## 🖼️ System Architecture

<p align="center">
  <img src="https://github.com/vivek08248/NFC-Based-Vehicle-Ignition-System/raw/main/images/flow_diagram.png" alt="System Flow Diagram" width="600">
</p>

```
User Approaches Vehicle
        │
        ▼
ESP32 detects Wi-Fi Device
        │
        ▼
Raspberry Pi wakes up
        │
        ▼
User taps NFC Card
        │
        ▼
UID Verification
        │
        ▼
Face Recognition
        │
        ▼
Authentication Decision
   ┌────────┴────────┐
   │                 │
   ▼                 ▼
Access Granted    Access Denied
   │                 │
   ▼                 ▼
Engine Start      Alarm & Lockout
```

---

## ✨ Features

- 🔐 Three-factor authentication (Wi-Fi + NFC + Face)
- 📶 Wi-Fi proximity detection using ESP32
- 💳 NFC-based user verification
- 🧠 Facial recognition using OpenCV
- 🖥️ OLED real-time status display
- ➕ User registration mode
- 🚨 Local security alarm after repeated failures
- 🗂️ Driver database management
- 🔋 Low-power architecture
- 🧩 Modular embedded software design

---

## 🧰 Hardware Components

| Component | Purpose |
|---|---|
| Raspberry Pi 5 | Main processing unit |
| ESP32 Development Board | Wi-Fi proximity detection |
| PN532 NFC Reader | NFC authentication |
| USB Webcam | Facial recognition |
| SSD1306 OLED Display | System status display |
| NFC Tags | Driver authentication |
| USB-to-TTL Adapter | UART communication |
| Power Supply | Raspberry Pi power |

<table>
<tr>
<td align="center">
<img src="https://github.com/vivek08248/NFC-Based-Vehicle-Ignition-System/raw/main/images/raspberry_pi5.png" width="300" alt="Raspberry Pi 5"><br>
<b>Raspberry Pi 5</b>
</td>
<td align="center">
<img src="https://github.com/vivek08248/NFC-Based-Vehicle-Ignition-System/raw/main/images/esp32.png" width="300" alt="ESP32"><br>
<b>ESP32</b>
</td>
</tr>
</table>

---

## 📂 Repository Structure

```
NFC-Based-Vehicle-Ignition-System
│
├── README.md
├── LICENSE
├── .gitignore
│
├── docs
│   ├── Project_Report.pdf
│   └── Images
│
├── raspberry_pi
│   ├── vehicle_security.py
│   ├── sniff.py
│   └── requirements.txt
│
├── esp32
│   └── esp32_proximity.ino
│
├── images
│   ├── flow_diagram.png
│   ├── raspberry_pi5.png
│   ├── esp32.png
│   ├── authentication.png
│   └── demo_output.png
│
└── hardware
    └── components_list.md
```

---

## 🛠️ Software Stack

- Python 3
- OpenCV
- face_recognition
- NumPy
- PySerial
- Pillow
- Adafruit SSD1306 Library
- Adafruit PN532 Library
- Arduino IDE
- Raspberry Pi OS

---

## 🔄 Authentication Flow

### Layer 1 — Wi-Fi Proximity
The ESP32 continuously broadcasts a Wi-Fi access point. When the authorized device enters range, the ESP32 detects the client, sends a `USER_PRESENT` signal, and the Raspberry Pi activates.

### Layer 2 — NFC Verification
The user taps an NFC card. The PN532 reads the UID and sends it to the Raspberry Pi, which verifies it against the local driver database.

### Layer 3 — Facial Recognition
If the NFC card is valid, the camera activates, detects a face, generates a face encoding, and compares it against stored encodings. If matched, **vehicle ignition is enabled**.

---

## 🚀 Getting Started

### Prerequisites
- Raspberry Pi 5 with Raspberry Pi OS installed
- ESP32 with Arduino IDE configured
- PN532 NFC module wired via UART/I2C
- USB webcam connected to the Pi
- SSD1306 OLED display wired via I2C

### Setup

```bash
# Clone the repository
git clone https://github.com/vivek08248/NFC-Based-Vehicle-Ignition-System.git
cd NFC-Based-Vehicle-Ignition-System

# Install Python dependencies (on Raspberry Pi)
cd raspberry_pi
pip install -r requirements.txt
```

1. Flash `esp32/esp32_proximity.ino` onto the ESP32 using the Arduino IDE.
2. Update Wi-Fi credentials and device MAC address in the ESP32 sketch.
3. Register authorized NFC tags and face encodings using the registration mode.
4. Run the main controller script on the Raspberry Pi:

```bash
python3 vehicle_security.py
```

---

## 📊 Results

<table>
<tr>
<td align="center">
<img src="https://github.com/vivek08248/NFC-Based-Vehicle-Ignition-System/raw/main/images/authentication.png" width="400" alt="Face Authentication"><br>
<b>Face Authentication</b>
</td>
<td align="center">
<img src="https://github.com/vivek08248/NFC-Based-Vehicle-Ignition-System/raw/main/images/demo_output.png" width="400" alt="Successful System Execution"><br>
<b>Successful System Execution</b>
</td>
</tr>
</table>

---

## 🔒 Security Features

- Multi-factor authentication
- Unauthorized user detection
- Face encoding database
- Secure UID masking
- Local lockout timer
- Alarm on repeated failures
- Modular authentication pipeline

---

## 🔮 Future Improvements

- ☁️ Cloud database synchronization
- 📱 Mobile application integration
- 🛰️ GPS vehicle tracking
- 🌙 Infrared camera for night operation
- 🤖 AI-based spoof detection
- 📝 Secure cloud logging
- 📡 MQTT remote monitoring
- 🚗 CAN Bus integration

---

## 🎯 Applications

- Smart vehicle security
- Fleet management
- Secure vehicle access
- Embedded authentication systems
- Smart transportation
- IoT-based security

---

## 📚 References

- Face Detection and Recognition using OpenCV
- Raspberry Pi Documentation
- ESP32 Documentation
- PN532 NFC Documentation
- OpenCV Documentation

---

## 👥 Authors

**B. Praneeth Reddy** · **M. Shivanand Reddy** · **C. Vivek**

Department of Electronics and Communication Engineering
Vasavi College of Engineering (Autonomous), Hyderabad, India

---


<div align="center">

### ⭐ If you found this project useful, consider giving it a star on GitHub!

</div>
