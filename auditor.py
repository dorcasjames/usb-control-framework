import os
import time
import hashlib
import datetime

WATCH_PATHS = ["/sdcard/usb_test_monitor"]
CHECK_INTERVAL = 3
AUDIT_LOG = "logs/file_audit.log"

def log_event(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(AUDIT_LOG, "a") as f:
        f.write(log_entry + "\n")

def get_file_hash(filepath):
    try:
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return "UNREADABLE"

def scan_files(path):
    file_map = {}
    try:
        for root, dirs, files in os.walk(path):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    stat = os.stat(filepath)
                    file_map[filepath] = {
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                        "hash": get_file_hash(filepath)
                    }
                except Exception:
                    pass
    except Exception:
        pass
    return file_map

def audit_transfers():
    os.makedirs("logs", exist_ok=True)
    print("[*] File Auditor started. Monitoring file movements...")
    print("[*] Press CTRL+C to stop.\n")

    snapshots = {}
    for path in WATCH_PATHS:
        if os.path.exists(path):
            snapshots[path] = scan_files(path)
            print(f"[*] Watching: {path}")

    if not snapshots:
        print("[!] No watchable paths found. Running in demo mode.")
        log_event("AUDITOR STARTED | No external storage found | Demo mode active")

    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            for path in WATCH_PATHS:
                if not os.path.exists(path):
                    continue

                current = scan_files(path)
                previous = snapshots.get(path, {})

                # Detect new files
                for filepath in current:
                    if filepath not in previous:
                        size = current[filepath]["size"]
                        fhash = current[filepath]["hash"]
                        message = (f"NEW FILE DETECTED | "
                                  f"Path: {filepath} | "
                                  f"Size: {size} bytes | "
                                  f"SHA256: {fhash}")
                        log_event(message)

                # Detect deleted files
                for filepath in previous:
                    if filepath not in current:
                        message = f"FILE DELETED | Path: {filepath}"
                        log_event(message)

                # Detect modified files
                for filepath in current:
                    if filepath in previous:
                        if current[filepath]["hash"] != previous[filepath]["hash"]:
                            message = (f"FILE MODIFIED | "
                                      f"Path: {filepath} | "
                                      f"New SHA256: {current[filepath]['hash']}")
                            log_event(message)

                snapshots[path] = current

    except KeyboardInterrupt:
        print("\n[*] File Auditor stopped.")
        log_event("AUDITOR STOPPED by user.")

if __name__ == "__main__":
    audit_transfers()
