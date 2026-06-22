import os
import datetime

USB_LOG = "logs/usb_events.log"
AUDIT_LOG = "logs/file_audit.log"
REPORT_FILE = "reports/usb_audit_report.txt"

def read_log(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return f.readlines()

def count_events(lines, keyword):
    return sum(1 for line in lines if keyword.upper() in line.upper())

def generate_report():
    os.makedirs("reports", exist_ok=True)

    usb_lines = read_log(USB_LOG)
    audit_lines = read_log(AUDIT_LOG)
    all_lines = usb_lines + audit_lines

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_usb = len([l for l in usb_lines if "CONNECTED" in l or "DISCONNECTED" in l])
    total_files = len(audit_lines)
    new_files = count_events(audit_lines, "NEW FILE")
    modified = count_events(audit_lines, "FILE MODIFIED")
    deleted = count_events(audit_lines, "FILE DELETED")
    blocked = count_events(all_lines, "BLOCKED")
    violations = count_events(all_lines, "UNAUTHORIZED")

    report = ""
    report += "=" * 62 + "\n"
    report += "   USB DEVICE CONTROL & MONITORING FRAMEWORK\n"
    report += "             SECURITY AUDIT REPORT\n"
    report += "=" * 62 + "\n\n"
    report += f"Report Generated : {timestamp}\n"
    report += f"Prepared By      : USB Control Framework v1.0\n"
    report += f"Classification   : CONFIDENTIAL\n\n"

    report += "-" * 62 + "\n"
    report += "SECTION 1 - EXECUTIVE SUMMARY\n"
    report += "-" * 62 + "\n"
    report += "This report summarizes all USB device activity and file\n"
    report += "transfer events detected by the monitoring framework.\n"
    report += "All events have been logged with timestamps and SHA256\n"
    report += "integrity hashes for forensic verification.\n\n"

    report += "-" * 62 + "\n"
    report += "SECTION 2 - EVENT STATISTICS\n"
    report += "-" * 62 + "\n"
    report += f"  Total USB Events Detected    : {total_usb}\n"
    report += f"  Total File Audit Events      : {total_files}\n"
    report += f"  New Files Detected           : {new_files}\n"
    report += f"  Files Modified               : {modified}\n"
    report += f"  Files Deleted                : {deleted}\n"
    report += f"  Blocked Device Attempts      : {blocked}\n"
    report += f"  Unauthorized Access Flags    : {violations}\n\n"

    report += "-" * 62 + "\n"
    report += "SECTION 3 - USB DEVICE EVENTS\n"
    report += "-" * 62 + "\n"
    if usb_lines:
        for line in usb_lines:
            report += f"  {line.strip()}\n"
    else:
        report += "  No USB connection events recorded.\n"
    report += "\n"

    report += "-" * 62 + "\n"
    report += "SECTION 4 - FILE AUDIT EVENTS\n"
    report += "-" * 62 + "\n"
    if audit_lines:
        for line in audit_lines:
            report += f"  {line.strip()}\n"
    else:
        report += "  No file audit events recorded.\n"
    report += "\n"

    report += "-" * 62 + "\n"
    report += "SECTION 5 - VIOLATIONS & SUSPICIOUS ACTIVITY\n"
    report += "-" * 62 + "\n"
    violations_found = [l for l in all_lines if
                       "BLOCKED" in l.upper() or
                       "UNAUTHORIZED" in l.upper() or
                       "SUSPICIOUS" in l.upper()]
    if violations_found:
        for line in violations_found:
            report += f"  [!] {line.strip()}\n"
    else:
        report += "  No violations detected in this session.\n"
    report += "\n"

    report += "-" * 62 + "\n"
    report += "SECTION 6 - RECOMMENDATIONS\n"
    report += "-" * 62 + "\n"
    report += "  1. Enforce strict allowlist policy for all USB devices.\n"
    report += "  2. Immediately investigate any BLOCKED device attempts.\n"
    report += "  3. Review all FILE MODIFIED events for data tampering.\n"
    report += "  4. Conduct regular audits of USB activity logs.\n"
    report += "  5. Train staff on USB security and insider threat risks.\n"
    report += "  6. Disable USB ports on sensitive workstations.\n"
    report += "  7. Implement SHA256 integrity checks on critical files.\n\n"

    report += "=" * 62 + "\n"
    report += "END OF REPORT\n"
    report += "=" * 62 + "\n"

    with open(REPORT_FILE, "w") as f:
        f.write(report)

    print(report)
    print(f"\n[+] Report saved to: {REPORT_FILE}")

if __name__ == "__main__":
    generate_report()
