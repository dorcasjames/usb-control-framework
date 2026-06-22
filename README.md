# usb-control-framework
USB Device Control &amp; Monitoring Framework - Cybersecurity Project
# USB Device Control & Monitoring Framework

## Project Overview
A Python-based cybersecurity framework designed to detect, monitor, 
and restrict unauthorized USB activity on a system. Built as part of 
a practical cybersecurity scholarship programme.

## Features
- Real-time USB device detection
- Allowlist/Blocklist policy enforcement
- Automatic blocking of unauthorized devices
- File transfer monitoring with SHA256 integrity hashing
- Complete audit logging with timestamps
- Professional security report generation
- Interactive menu-driven interface

## Project Structure
usb-control-framework/
├── main.py          # Entry point and menu interface
├── monitor.py       # USB event detection
├── policy.py        # Allowlist/Blocklist enforcement
├── auditor.py       # File transfer monitoring
├── reporter.py      # Audit report generation
├── config/
│   ├── allowlist.json   # Approved USB devices
│   └── blocklist.json   # Banned USB devices
├── logs/
│   ├── usb_events.log   # USB connection events
│   └── file_audit.log   # File transfer events
└── reports/
└── usb_audit_report.txt  # Generated audit report
## Technologies Used
- Python 3.13
- hashlib (SHA256 file integrity)
- os / threading / datetime (system monitoring)

## How To Run
```bash
python3 main.py


#Security Techniques Implemented
Device fingerprinting (Vendor ID, Product ID)
Allowlist/Blocklist policy enforcement
SHA256 file integrity verification
Real-time audit logging
Insider threat detection

#DISCLAIMER
This is for educational purposes only
