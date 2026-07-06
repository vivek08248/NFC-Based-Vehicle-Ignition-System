import serial
import time

ESP32_PORT = "/dev/ttyUSB1"  # Adjust if it swaps to USB0
BAUD_RATE = 115200

print(f"Listening on {ESP32_PORT} at {BAUD_RATE} baud...")

try:
    with serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1) as ser:
        ser.reset_input_buffer()
        while True:
            if ser.in_waiting > 0:
                raw_bytes = ser.readline()
                print(f"RAW BYTES: {raw_bytes}")
                
                decoded_str = raw_bytes.decode('utf-8', errors='ignore').strip()
                print(f"DECODED STRING: '{decoded_str}'")
                
                if "USER_PRESENT" in decoded_str:
                    print("--> PYTHON DETECTED THE TRIGGER! <--\n")
            time.sleep(0.1)
except Exception as e:
    print(f"Port Error: {e}")