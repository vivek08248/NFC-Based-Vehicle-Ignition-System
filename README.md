<div align="center">

# 🚗🔐 NFC-Based Vehicle Ignition System

**A 3-Factor Embedded Vehicle Security System**
### Wi-Fi Proximity Detection · NFC Authentication · Facial Recognition

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-IoT-orange?logo=espressif&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-5-red?logo=raspberrypi&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

*Theme-Based Project · Department of Electronics and Communication Engineering*
*Vasavi College of Engineering (Autonomous), Hyderabad — 2025–2026*

</div>

---

## 📖 Abstract

Conventional vehicle keys carry a significant security risk — they can be **lost, duplicated, or stolen**. This project implements an advanced ignition system that replaces the mechanical key with a **two-tier digital authentication pipeline**, layered on top of a **Wi-Fi proximity trigger**, to ensure a vehicle can only be started by its verified owner.

The system runs on a **Raspberry Pi 5** paired with an **ESP32** microcontroller and a **PN532 NFC reader module**. A registered driver must:

1. Be **detected in proximity** via the ESP32's Wi-Fi access point
2. **Tap an authorized NFC card**, which is verified against a stored ID database
3. Pass a **facial recognition check** against the driver's stored face encoding

Only when **all three checks pass** does the Raspberry Pi signal the ignition relay to enable engine start. A failed NFC scan or face mismatch keeps the ignition locked — and repeated failures trigger a local security alarm.

---

## 🖼️ System Flow

<p align="center">
  <img src="images/flow_diagram.png" alt="Process Flow Diagram" width="750">
</p>

```
          User Approaches Vehicle
                    │
                    ▼
      ESP32 Wi-Fi Access Point detects device
              (sends "USER_PRESENT")
                    │
                    ▼
        Raspberry Pi wakes / activates PN532
                    │
                    ▼
           User taps NFC Card / Phone
                    │
                    ▼
       ESP32 reads UID → sends to Raspberry Pi
                    │
                    ▼
        UID verified against driver database
             │                    │
         Invalid                Valid
             │                    │
             ▼                    ▼
      "Unknown Key"        Camera activates
      Ignition OFF                │
                                  ▼
                     Face captured & encoded
                                  │
                                  ▼
                  Compared against stored encodings
                 │                              │
            No Match                        Match
                 │                              │
                 ▼                              ▼
          Access Denied                 Access Granted
          Ignition OFF               → Engine Start Enabled
                 │
                 ▼
    3 failed attempts → Local alarm + lockout timer
```

---

## ✨ Key Features

- 🛰️ **Wi-Fi proximity trigger** — system arms only when the owner's device is detected nearby (ESP32 SoftAP client detection)
- 💳 **NFC authentication** — UID verification via PN532 reader over UART
- 🧠 **Facial recognition** — `face_recognition` + OpenCV encoding comparison with configurable tolerance
- 🚨 **Anti-brute-force lockout** — local alarm and lockout timer after repeated failed attempts (`MAX_FAILED_ATTEMPTS`)
- 🕵️ **UID masking** — driver card UIDs are masked in console output for privacy
- ➕ **Live driver registration mode** — register new NFC cards and face encodings from the console menu
- 💾 **Persistent driver database** — face encodings stored locally via `pickle`
- 🔋 **Power-aware ESP32 firmware** — CPU frequency capped to reduce power spikes

---

## 🧰 Hardware Components

| Component | Role |
|---|---|
| **Raspberry Pi 5** | Central controller — runs authentication logic, camera, and face recognition |
| **ESP32 Dev Module** | Hosts Wi-Fi SoftAP for proximity detection; relays serial signals to the Pi |
| **PN532 NFC Reader** (UART) | Reads NFC card/phone UID for authentication |
| **USB Webcam** | Captures driver's face for recognition |
| **Ignition Relay/Driver Circuit** | Switched on by the Pi once authentication succeeds |
| **USB-to-UART Adapter** | Serial link between Raspberry Pi and PN532/ESP32 |

<table>
<tr>
<td align="center" width="50%">
<img src="images/raspberry_pi5.png" width="320" alt="Raspberry Pi 5"><br>
<b>Raspberry Pi 5 — Main Controller</b>
</td>
<td align="center" width="50%">
<img src="images/esp32.png" width="320" alt="ESP32 Dev Board"><br>
<b>ESP32 — Wi-Fi Proximity Node</b>
</td>
</tr>
</table>

---

## 🛠️ Software Stack

| Layer | Technology |
|---|---|
| Language | Python 3 (Raspberry Pi), C++ / Arduino (ESP32) |
| Computer Vision | OpenCV (`cv2`) |
| Face Recognition | `face_recognition` (dlib-based encodings) |
| Numerics | NumPy |
| Serial Comms | `pyserial` |
| NFC Driver | Adafruit PN532 UART library |
| Data Persistence | `pickle` (driver/face database) |
| Firmware IDE | Arduino IDE (ESP32 Dev Module) |
| OS | Raspberry Pi OS |

---

## 🔄 Authentication Pipeline — How It Works

### Layer 1 — Wi-Fi Proximity (`wait_for_esp32_proximity()`)
The ESP32 runs a SoftAP (`WiFi.softAP`) and continuously checks connected station count. When the owner's phone/device joins, it sends `USER_PRESENT` over serial (115200 baud) to the Raspberry Pi, which unblocks the main loop and proceeds — the system stays idle otherwise, saving power.

### Layer 2 — NFC Verification (`init_pn532()`, `scan_local_nfc()`)
The Raspberry Pi initializes the PN532 over UART and waits (with timeout) for a passive NFC target. On a tap, the card's UID is read and checked against the stored driver database (`mask_uid()` hides it from console logs for privacy).

### Layer 3 — Facial Recognition (`capture_face()`, `authenticate_user()`)
If the UID is valid, the Pi camera activates and searches each frame for a face using `face_recognition.face_locations`. Once detected (shown with a green "FACE DETECTED" box), the face is encoded and compared against the stored encoding for that UID within a set tolerance (default `0.5`).

### Decision & Ignition Control (`main()`)
- **Both checks pass** → console prints `ACCESS GRANTED — ENGINE START`, ignition relay is enabled
- **Either check fails** → `failed_attempts` increments; on reaching `MAX_FAILED_ATTEMPTS` (default 3), `trigger_local_alarm()` fires a countdown lockout
- System then resets and returns to waiting for Wi-Fi proximity

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
│   └── Project_Report.pdf
│
├── raspberry_pi
│   ├── TBP_NFC_ESP32_Cam.py      # Main controller: proximity + NFC + face auth
│   ├── driver_cam.txt            # Camera/driver notes
│   └── requirements.txt
│
├── esp32
│   └── esp32_nfc_wifi_ssid.ino   # SoftAP proximity broadcaster firmware
│
├── images
│   ├── flow_diagram.png
│   ├── raspberry_pi5.png
│   ├── esp32.png
│   ├── face_detected.png
│   └── access_granted.png
│
└── hardware
    └── components_list.md
```

---

## 🚀 Getting Started

### Prerequisites
- Raspberry Pi 5 running Raspberry Pi OS, with a USB webcam attached
- ESP32 Dev Module + Arduino IDE (2.x recommended)
- PN532 NFC module wired to the Pi over UART
- Python 3 environment on the Pi

### 1. Clone the repository
```bash
git clone https://github.com/vivek08248/NFC-Based-Vehicle-Ignition-System.git
cd NFC-Based-Vehicle-Ignition-System
```

### 2. Flash the ESP32 firmware
Open `esp32/esp32_nfc_wifi_ssid.ino` in the Arduino IDE, set your desired `ssid` / `password` for the SoftAP, select **ESP32 Dev Module**, and upload.

### 3. Install Raspberry Pi dependencies
```bash
cd raspberry_pi
pip install -r requirements.txt
# Typical deps: opencv-python face_recognition numpy pyserial adafruit-circuitpython-pn532
```

### 4. Configure serial ports
Update the fixed port mappings at the top of `TBP_NFC_ESP32_Cam.py`:
```python
ESP32_PORT = "/dev/ttyUSB1"
PN532_PORT = "/dev/ttyUSB0"
BAUD_RATE  = 115200
```

### 5. Run the system
```bash
python3 TBP_NFC_ESP32_Cam.py
```
On first run, use the on-screen menu to **register a new driver** (captures NFC UID + face encoding). On subsequent runs, tap the registered card and let the camera verify your face to unlock ignition.

---

## 📊 Results

<table>
<tr>
<td align="center" width="50%">
<img src="images/face_detected.png" width="380" alt="Face Detected"><br>
<b>Live face detection during authentication</b>
</td>
<td align="center" width="50%">
<img src="images/access_granted.png" width="380" alt="Access Granted"><br>
<b>Successful dual-factor match → Engine Start</b>
</td>
</tr>
</table>

**Observed behavior:**
- Unknown/unregistered NFC card → `"Unknown Key. Please register first."`, ignition remains OFF
- Registered card + matching face → `"ACCESS GRANTED — ENGINE START"`
- Registered card + non-matching face → access denied, failed-attempt counter increments
- 3 consecutive failures → local alarm countdown, system resets to standby

---

## 🎓 Conclusion

The system successfully demonstrates that combining **NFC-based possession verification** with **biometric facial recognition**, gated by a **Wi-Fi proximity trigger**, produces a materially more secure and power-efficient vehicle access model than a traditional mechanical key. Each authentication layer independently reduces the chance of unauthorized access, and their combination ensures that possessing the NFC card alone is insufficient without also matching the registered driver's face.

---

## 🔮 Future Scope

- 🌙 Infrared / low-light imaging for night-time facial recognition
- ☁️ Cloud upload of face captures during unauthorized access attempts
- 📱 Companion mobile app for remote monitoring and driver management
- 🛰️ GPS-based vehicle tracking integration
- ⚡ Real-time hardware optimization for in-vehicle deployment
- 🤖 Improved recognition algorithms for higher speed and accuracy

---

## 🌍 Sustainable Development Goals

**SDG 11 — Sustainable Cities and Communities**
By replacing vulnerable physical keys with contactless NFC + biometric authentication, this project helps reduce vehicle theft and the financial losses that come with it, while supporting the broader shift toward smart, contactless access technology in urban transportation systems.

---

## 📚 References

1. I. Gupta, V. Patil, C. Kadam and S. Dumbre, "Face detection and recognition using Raspberry Pi," *IEEE WIECON-ECE*, Pune, India, 2016.
2. J. Mihal'ov and M. Hulič, "NFC/RFID technology using Raspberry Pi as platform used in smart home project," *IEEE 14th Int. Sci. Conf. on Informatics*, Poprad, Slovakia, 2017.
3. S. U. Masruroh, A. Fiade and I. R. Julia, "NFC Based Mobile Attendance System with Facial Authorization on Raspberry Pi and Cloud Server," *6th Int. Conf. on Cyber and IT Service Management (CITSM)*, Parapat, Indonesia, 2018.
4. A. Kumar, S. Chaudhary, S. Sangal, and R. Dhama, "Face Detection and Recognition using OpenCV," *International Journal of Computer Applications*, vol. 184, no. 11, pp. 23–32, May 2022.

---

## 👥 Authors

**B. Praneeth Reddy** · **M. Shivanand Reddy** · **C. Vivek**

**Guide:** Mr. V. Krishna Mohan, Associate Professor, E.C.E Department
**Head of Department:** Dr. E. Sreenivasa Rao, Professor & HOD, E.C.E Department

Department of Electronics and Communication Engineering
**Vasavi College of Engineering (Autonomous)**, Ibrahimbagh, Hyderabad – 500031
*Accredited by NAAC with 'A++' Grade*

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a star!

</div>
