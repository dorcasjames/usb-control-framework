import os
import time
import datetime

WATCH_PATH = "/dev"
CHECK_INTERVAL = 2

def ensure_logs():
    os.makedirs("logs", exist_ok=True)
    if not os.path.exists("logs/usb_events.log"):
        open("logs/usb_events.log", "w").close()

def log_event(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open("logs/usb_events.log", "a") as f:
        f.write(log_entry + "\n")

def get_usb_devices():
    devices = []
    try:
        for item in os.listdir(WATCH_PATH):
            if item.startswith(("sd", "usb", "ttyUSB")):
                devices.append(item)
    except PermissionError:
        pass
    return set(devices)

def monitor_usb():
    ensure_logs()
    print("[*] USB Monitor started. Watching for devices...")
    print("[*] Press CTRL+C to stop.\n")
    known_devices = get_usb_devices()

    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            current_devices = get_usb_devices()

            added = current_devices - known_devices
            removed = known_devices - current_devices

            for device in added:
                message = f"USB CONNECTED | Device: /dev/{device}"
                log_event(message)

            for device in removed:
                message = f"USB DISCONNECTED | Device: /dev/{device}"
                log_event(message)

            known_devices = current_devices

    except KeyboardInterrupt:
        print("\n[*] Monitor stopped by user.")
        log_event("MONITOR STOPPED by user.")

if __name__ == "__main__":
    monitor_usb()
