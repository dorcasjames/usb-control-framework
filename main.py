import os
import time
import threading
import datetime
from monitor import monitor_usb
from auditor import audit_transfers
from reporter import generate_report
from policy import display_decision

def print_banner():
    print("""
==============================================================
   USB DEVICE CONTROL & MONITORING FRAMEWORK
   Version 1.0 | Blue Team Security Tool
==============================================================
""")

def print_menu():
    print("""
[1] Start USB Monitor
[2] Start File Auditor
[3] Test Policy Engine
[4] Generate Audit Report
[5] View USB Event Log
[6] View File Audit Log
[7] Exit
""")

def view_log(filepath):
    if not os.path.exists(filepath):
        print(f"\n[!] Log file not found: {filepath}")
        return
    print(f"\n--- {filepath} ---")
    with open(filepath, "r") as f:
        contents = f.read()
    if contents.strip():
        print(contents)
    else:
        print("  Log is empty.")

def test_policy():
    print("\n[*] Policy Engine Test\n")
    test_devices = [
        ("0x0781", "0x5581"),
        ("0xdead", "0xbeef"),
        ("0x9999", "0x1111"),
    ]
    for vid, pid in test_devices:
        display_decision(vid, pid)

def main():
    print_banner()

    while True:
        print_menu()
        choice = input("Select option: ").strip()

        if choice == "1":
            print("\n[*] Starting USB Monitor... Press CTRL+C to stop.\n")
            try:
                monitor_usb()
            except KeyboardInterrupt:
                print("\n[*] Monitor stopped.")

        elif choice == "2":
            print("\n[*] Starting File Auditor... Press CTRL+C to stop.\n")
            try:
                audit_transfers()
            except KeyboardInterrupt:
                print("\n[*] Auditor stopped.")

        elif choice == "3":
            test_policy()

        elif choice == "4":
            print("\n[*] Generating audit report...\n")
            generate_report()

        elif choice == "5":
            view_log("logs/usb_events.log")

        elif choice == "6":
            view_log("logs/file_audit.log")

        elif choice == "7":
            print("\n[*] Exiting USB Control Framework. Goodbye.\n")
            break

        else:
            print("\n[!] Invalid option. Please select 1-7.")

if __name__ == "__main__":
    main()
