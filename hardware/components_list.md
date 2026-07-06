# 3-Factor Embedded Vehicle Security System
## Hardware Components List

### 1. Core Computing
- **Raspberry Pi 5**: The primary processing unit running the Python backend, facial recognition model (OpenCV), and hardware orchestration.
- **ESP32 Development Board**: Acts as a low-power Wi-Fi proximity beacon (Layer 1 trigger) to prevent the Raspberry Pi from continuously running and draining the vehicle battery.

### 2. Sensors & Interfaces
- **PN532 NFC/RFID Reader Module**: Configured in HSU (High-Speed UART) mode for reading physical security keys (Layer 2 authentication).
- **USB Webcam**: Connected to the Raspberry Pi 5 for capturing driver biometrics and performing facial recognition (Layer 3 authentication).
- **0.91-inch I2C OLED Display (SSD1306)**: Displays real-time system status, authentication progress, and error messages.
- **13.56 MHz NFC Tags/Cards**: Registered NFC cards used as authorized vehicle access keys.

### 3. Connectivity & Power
- **USB-to-TTL Serial Adapter (CP2102 / CH340)**: Connects the PN532 module to the Raspberry Pi over USB-UART, isolating it from the I2C bus for improved stability.
- **Jumper Wires** (Female-to-Female, Male-to-Female)
- **Micro-USB / USB-C Cables** for power and data transfer
- **5V / 5A USB-C Power Supply** for Raspberry Pi 5

---

## Summary

| Category | Components |
|----------|------------|
| Processing | Raspberry Pi 5, ESP32 |
| Authentication | PN532 NFC Reader, NFC Tags, USB Webcam |
| User Interface | SSD1306 OLED Display |
| Connectivity | USB-to-TTL Adapter, USB Cables, Jumper Wires |
| Power | 5V/5A Power Supply |
