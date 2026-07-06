\# 3-Factor Embedded Vehicle Security System



A secure embedded vehicle ignition system that combines \*\*Wi-Fi proximity detection\*\*, \*\*NFC authentication\*\*, and \*\*facial recognition\*\* to provide multi-layered vehicle access control using \*\*Raspberry Pi 5\*\* and \*\*ESP32\*\*.



!\[Python](https://img.shields.io/badge/Python-3.x-blue)

!\[OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)

!\[ESP32](https://img.shields.io/badge/ESP32-IoT-orange)

!\[Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-5-red)

!\[License](https://img.shields.io/badge/License-MIT-yellow)



\---



\# Overview



Traditional vehicle keys are vulnerable to theft, duplication, and unauthorized use. This project introduces a \*\*three-factor authentication system\*\* that significantly improves vehicle security by requiring:



1\. \*\*Wi-Fi Proximity Detection\*\*

2\. \*\*NFC Authentication\*\*

3\. \*\*Facial Recognition\*\*



The Raspberry Pi acts as the central controller, coordinating all hardware modules and authentication stages before allowing the vehicle ignition system to start.



\---



\# Features



\- Three-factor authentication

\- Wi-Fi proximity detection using ESP32

\- NFC-based user verification

\- Facial recognition using OpenCV

\- OLED status display

\- User registration mode

\- Local security alarm after repeated failures

\- Driver database management

\- Low-power architecture

\- Modular embedded software design



\---



\# System Architecture



<p align="center">

<img src="images/flow\_diagram.png" width="750">

</p>



The authentication process consists of three sequential layers:



```

User Approaches Vehicle

&#x20;         │

&#x20;         ▼

ESP32 detects Wi-Fi Device

&#x20;         │

&#x20;         ▼

Raspberry Pi wakes up

&#x20;         │

&#x20;         ▼

User taps NFC Card

&#x20;         │

&#x20;         ▼

UID Verification

&#x20;         │

&#x20;         ▼

Face Recognition

&#x20;         │

&#x20;         ▼

Authentication Decision

&#x20;         │

&#x20;┌────────┴────────┐

&#x20;│                 │

&#x20;▼                 ▼

Access Granted   Access Denied

&#x20;│                 │

&#x20;▼                 ▼

Engine Start     Alarm \& Lockout

```



\---



\# Hardware Components



| Component | Purpose |

|-----------|----------|

| Raspberry Pi 5 | Main Processing Unit |

| ESP32 Development Board | Wi-Fi Proximity Detection |

| PN532 NFC Reader | NFC Authentication |

| USB Webcam | Facial Recognition |

| SSD1306 OLED Display | System Status Display |

| NFC Tags | Driver Authentication |

| USB-to-TTL Adapter | UART Communication |

| Power Supply | Raspberry Pi Power |



\---



\# Hardware



\### Raspberry Pi 5



<p align="center">

<img src="images/raspberry\_pi5.png" width="500">

</p>



\---



\### ESP32



<p align="center">

<img src="images/esp32.png" width="400">

</p>



\---



\# Repository Structure



```

NFC-Based-Vehicle-Ignition-System

│

├── README.md

├── LICENSE

├── .gitignore

│

├── docs

│   ├── Project\_Report.pdf

│   └── Images

│

├── raspberry\_pi

│   ├── vehicle\_security.py

│   ├── sniff.py

│   └── requirements.txt

│

├── esp32

│   └── esp32\_proximity.ino

│

├── images

│   ├── flow\_diagram.png

│   ├── raspberry\_pi5.png

│   ├── esp32.png

│   ├── authentication.png

│   └── demo\_output.png

│

└── hardware

&#x20;   └── components\_list.md

```



\---



\# Software Stack



\- Python 3

\- OpenCV

\- face\_recognition

\- NumPy

\- PySerial

\- Pillow

\- Adafruit SSD1306 Library

\- Adafruit PN532 Library

\- Arduino IDE

\- Raspberry Pi OS



\---



\# Authentication Flow



\### Layer 1 — Wi-Fi Proximity



ESP32 continuously broadcasts a Wi-Fi access point.



When the authorized device enters range:



\- ESP32 detects the client

\- Sends \*\*USER\_PRESENT\*\*

\- Raspberry Pi activates



\---



\### Layer 2 — NFC Verification



The user taps an NFC card.



The PN532 reads the UID and sends it to Raspberry Pi.



The UID is verified against the local database.



\---



\### Layer 3 — Facial Recognition



If the NFC card is valid,



\- Camera activates

\- Face is detected

\- Face encoding generated

\- Compared against stored encodings



If matched,



\*\*Vehicle ignition is enabled.\*\*



\---



\# Results



\### Face Authentication



<p align="center">

<img src="images/authentication.png" width="650">

</p>



\---



\### Successful System Execution



<p align="center">

<img src="images/demo\_output.png" width="650">

</p>



\---



\# Security Features



\- Multi-factor authentication

\- Unauthorized user detection

\- Face encoding database

\- Secure UID masking

\- Local lockout timer

\- Alarm on repeated failures

\- Modular authentication pipeline



\---



\# Future Improvements



\- Cloud database synchronization

\- Mobile application integration

\- GPS vehicle tracking

\- Infrared camera for night operation

\- AI-based spoof detection

\- Secure cloud logging

\- MQTT remote monitoring

\- CAN Bus integration



\---



\# Applications



\- Smart Vehicle Security

\- Fleet Management

\- Secure Vehicle Access

\- Embedded Authentication Systems

\- Smart Transportation

\- IoT-based Security



\---



\# References



\- Face Detection and Recognition using OpenCV

\- Raspberry Pi Documentation

\- ESP32 Documentation

\- PN532 NFC Documentation

\- OpenCV Documentation



\---



\# Authors



\*\*B. Praneeth Reddy\*\*



\*\*M. Shivanand Reddy\*\*



\*\*C. Vivek\*\*



Department of Electronics and Communication Engineering



Vasavi College of Engineering (Autonomous)



Hyderabad, India



\---



\# License



This project is released under the MIT License.



\---



\## If you found this project useful, consider giving it a ⭐ on GitHub.

