import json
import os

ALLOWLIST_FILE = "config/allowlist.json"
BLOCKLIST_FILE = "config/blocklist.json"

def load_policy(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        data = json.load(f)
    return data.get("devices", [])

def check_device(vid, pid):
    blocklist = load_policy(BLOCKLIST_FILE)
    for device in blocklist:
        if device["vid"] == vid and device["pid"] == pid:
            return "BLOCKED", device.get("name", "Unknown Device")

    allowlist = load_policy(ALLOWLIST_FILE)
    for device in allowlist:
        if device["vid"] == vid and device["pid"] == pid:
            return "ALLOWED", device.get("name", "Unknown Device")

    return "UNKNOWN", "Unregistered Device"

def display_decision(vid, pid):
    status, name = check_device(vid, pid)

    if status == "ALLOWED":
        print(f"[+] ALLOWED  | {name} | VID: {vid} | PID: {pid}")
    elif status == "BLOCKED":
        print(f"[!] BLOCKED  | {name} | VID: {vid} | PID: {pid}")
    else:
        print(f"[?] UNKNOWN  | {name} | VID: {vid} | PID: {pid}")

    return status

if __name__ == "__main__":
    print("[*] Testing Policy Engine...\n")
    display_decision("0x0781", "0x5581")
    display_decision("0xdead", "0xbeef")
    display_decision("0x1234", "0x5678")
