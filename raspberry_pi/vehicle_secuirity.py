import cv2
import face_recognition
import numpy as np
import time
import os
import pickle
import serial
import atexit      
import signal      
import sys         
from adafruit_pn532.uart import PN532_UART

# --- OLED Imports ---
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# ---------------- Configuration ----------------
LOW_LIGHT_THRESHOLD = 80
DB_FILE = "face_database.pkl"
MAX_FAILED_ATTEMPTS = 3
LOCKOUT_DURATION = 10

# --- Fixed USB Port Mapping ---
ESP32_PORT = "/dev/ttyUSB1"  
PN532_PORT = "/dev/ttyUSB0"  
BAUD_RATE = 115200

# ---------------- Hardware Initialization ----------------
oled = None

def init_oled():
    """Initializes the 0.91" I2C OLED Display."""
    global oled
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
        oled.fill(0)
        oled.show()
        print("[HARDWARE OK] OLED Display Initialized.")
    except Exception as e:
        print(f"[ERROR] OLED not found on I2C: {e}")
        oled = None

def update_oled(line1="", line2="", line3=""):
    """Helper function to quickly write 3 lines of text to the OLED."""
    if oled is None: return
    try:
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        draw.text((0, 0), line1, font=font, fill=255)
        draw.text((0, 10), line2, font=font, fill=255)
        draw.text((0, 20), line3, font=font, fill=255)
        
        oled.image(image)
        oled.show()
    except Exception:
        pass 

# --- CLEAN EXIT HANDLERS ---
def clear_oled_on_exit():
    """Wipes the OLED screen when the program closes."""
    global oled
    if oled is not None:
        try:
            oled.fill(0)
            oled.show()
            print("\n[SYSTEM] OLED display cleared for shutdown.")
        except Exception:
            pass

atexit.register(clear_oled_on_exit)

def signal_handler(sig, frame):
    clear_oled_on_exit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ---------------- Initialization ----------------
def init_pn532():
    try:
        uart_connection = serial.Serial(PN532_PORT, baudrate=BAUD_RATE, timeout=0.1)
        pn = PN532_UART(uart_connection, debug=False)
        ic, ver, rev, support = pn.firmware_version
        print(f"[HARDWARE OK] PN532 found on {PN532_PORT} (Firmware: {ver}.{rev})")
        pn.SAM_configuration()
        return pn
    except Exception as e:
        print(f"[ERROR] Could not initialize PN532 on {PN532_PORT}: {e}")
        return None

def init_pi5_camera():
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return cap

# ---------------- Layer 1: Wi-Fi Proximity ----------------
def wait_for_esp32_proximity():
    """Listens to USB for the trigger using reliable readline logic."""
    print("\n" + "="*50)
    print(" NFC SECURITY SYSTEM ARMED - WAITING FOR WI-FI PROXIMITY")
    print("="*50)
    
    update_oled("NFC SECURITY", "SYSTEM ARMED", "Waiting for Wi-Fi...")
    
    try:
        with serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1) as ser:
            ser.reset_input_buffer()
            
            while True:
                if ser.in_waiting > 0:
                    raw_bytes = ser.readline()
                    decoded_str = raw_bytes.decode('utf-8', errors='ignore').strip()
                    
                    if "USER_PRESENT" in decoded_str:
                        print("\n>>> USER DETECTED <<<")
                        mac_address = "Unknown"
                        
                        if "MAC:" in decoded_str:
                            mac_address = decoded_str.split("MAC:")[1].strip()
                            print(f">>> Device MAC Address: {mac_address} <<<")
                            
                        update_oled("USER DETECTED", f"MAC: {mac_address}", "Waking Systems...")
                        return True
                        
                time.sleep(0.1)
                
    except serial.SerialException as e:
        print(f"[PORT ERROR] Cannot open {ESP32_PORT}. Check connection and permissions: {e}")
        update_oled("SYSTEM ERROR", "Check USB Port", "")
        time.sleep(2)
        return False

# ---------------- Layer 2: NFC Scan ----------------
def scan_local_nfc(pn532_instance):
    if pn532_instance is None:
        return None

    print("\n[SENSOR] NFC Reader Active. Please tap your Key (10s timeout)...")
    update_oled("NFC ACTIVE", "Please tap your", "Security Key...")
    
    uid = pn532_instance.read_passive_target(timeout=10.0)
    if uid is None:
        print("[SYSTEM] NFC Scan timed out.")
        update_oled("NFC TIMEOUT", "Scan Failed", "Returning to Sleep")
        return None
        
    update_oled("NFC USER DETECTED", "Processing...", "")
    return uid.hex()

# ---------------- Layer 3: Biometrics ----------------
def capture_face(prompt_text):
    update_oled("FACE REGISTRATION", "Look at Camera", "Wait for Green Box")
    cam = init_pi5_camera()
    time.sleep(1)
    face_encoding = None
    print(f"\n{prompt_text}")
    print("Wait for the GREEN BOX, press 's' to scan, 'q' to cancel.")

    while True:
        ret, frame = cam.read()
        if not ret: continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locs = face_recognition.face_locations(rgb_frame)

        for (top, right, bottom, left) in locs:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "FACE DETECTED", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Biometric Scanner", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            if len(locs) == 1:
                face_encoding = face_recognition.face_encodings(rgb_frame, locs)[0]
                update_oled("SUCCESS", "Face Captured", "Saving Profile...")
                break
            else:
                print("Please ensure exactly ONE face is in the frame.")
        elif key == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    return face_encoding

def authenticate_user(uid, db):
    stored_encoding = db[uid]["encoding"]
    driver_name = db[uid]['name']
    print(f"\n[AUTH] Welcome, {driver_name}. Initializing camera...")
    
    update_oled("BIOMETRIC SCAN", f"Driver: {driver_name}", "Authenticating...")
    
    cam = init_pi5_camera()
    time.sleep(1)
    access_granted = False
    start_time = time.time()

    while time.time() - start_time < 10:
        ret, frame = cam.read()
        if not ret: continue

        cv2.putText(frame, f"Authenticating {driver_name}...", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow("Authentication Scan", frame)
        cv2.waitKey(1)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locs = face_recognition.face_locations(rgb_frame)

        if len(locs) > 0:
            encs = face_recognition.face_encodings(rgb_frame, locs)
            for current_encoding in encs:
                if True in face_recognition.compare_faces([stored_encoding], current_encoding, tolerance=0.5):
                    access_granted = True
                    break
        if access_granted: break

    cam.release()
    cv2.destroyAllWindows()
    return access_granted

# ---------------- Utility Functions ----------------
def mask_uid(uid):
    if not uid or len(uid) <= 3: return uid
    return "*" * (len(uid) - 3) + uid[-3:]

def trigger_local_alarm():
    print("\n" + "!" * 50)
    print("!!! THEFT DETECTED: LOCAL SECURITY ALARM TRIGGERED !!!")
    print("!" * 50)
    
    for i in range(LOCKOUT_DURATION, 0, -1):
        update_oled("!!! ALARM !!!", "THEFT DETECTED", f"Lockout: {i}s")
        print(f"[ALARM] Lockout active... {i}s remaining", end='\r')
        time.sleep(1)
        
    print("\n[SYSTEM] Lockout expired. System resetting to armed state.\n")

# ---------------- Main System Flow ----------------
def main():
    init_oled()
    update_oled("NFC SECURITY", "SYSTEM ARMED", "Loading DB...")
    
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'rb') as f:
            face_db = pickle.load(f)
    else:
        face_db = {}
        
    failed_attempts = 0
    pn532_instance = None

    while True:
        # STEP 1: Wait for Wi-Fi Proximity
        if not wait_for_esp32_proximity(): 
            continue

        # STEP 2: Initialize NFC Reader
        if pn532_instance is None:
            print("[SYSTEM] Powering up NFC Reader...")
            pn532_instance = init_pn532()
            
        if pn532_instance is None:
            print("[ERROR] Failed to start NFC. Ensure it is plugged into USB0.")
            update_oled("HARDWARE ERROR", "NFC Disconnected", "")
            time.sleep(2)
            continue

        # STEP 3: Trigger NFC Read
        current_uid = scan_local_nfc(pn532_instance)
        if not current_uid: 
            continue
            
        print(f"[SYSTEM] Valid NFC Tag Captured: {mask_uid(current_uid)}")

        # STEP 4: Secure Menu
        while True:
            update_oled("SECURE MENU", "Check Console to", "Select Option")
            print("\n=== VEHICLE CONTROL ===")
            print("1. Start Ignition (Biometric)")
            print("2. Register New Driver")
            print("3. Lock Vehicle (Return to Sleep)")
            choice = input("Select (1-3): ")

            if choice == '1':
                if current_uid in face_db:
                    if authenticate_user(current_uid, face_db):
                        print("\n>>> ACCESS GRANTED: ENGINE START <<<\n")
                        update_oled("ACCESS GRANTED", "Identity Verified", ">>> ENGINE START <<<")
                        failed_attempts = 0
                        time.sleep(15) # Hold Engine Start for 15s
                        break
                    else:
                        print("\n>>> ACCESS DENIED <<<\n")
                        update_oled("ACCESS DENIED", "Biometric Failure", "")
                        failed_attempts += 1
                        time.sleep(2)
                else:
                    print("\n>>> UNKNOWN KEY. Please register first. <<<\n")
                    update_oled("UNKNOWN KEY", "Access Denied", "Register Profile")
                    time.sleep(2)

                if failed_attempts >= MAX_FAILED_ATTEMPTS:
                    trigger_local_alarm()
                    failed_attempts = 0
                    break

            elif choice == '2':
                update_oled("REGISTER MODE", "Enter Name on", "Console...")
                name = input("Enter Name: ")
                enc = capture_face(f"Scanning {name}...")
                if enc is not None:
                    face_db[current_uid] = {"name": name, "encoding": enc}
                    with open(DB_FILE, 'wb') as f:
                        pickle.dump(face_db, f)
                    print("Driver Registered!")
                    update_oled("REGISTER SUCCESS", f"Welcome {name}", "Profile Saved")
                    time.sleep(2)
            
            elif choice == '3':
                print("Locking vehicle and resetting proximity sensor...")
                update_oled("VEHICLE LOCKED", "Resetting Sensors", "")
                time.sleep(1)
                break

if __name__ == "__main__":
    main()