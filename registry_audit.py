# === INSTALLATION & USAGE ===
# 1. Install dependencies:
#    pip install winreg-alt tabulate
# 2. Save this script as registry_audit.py
# 3. Run it with:
#    python registry_audit.py

"""
This program audits **critical Windows Registry keys** commonly abused by malware for persistence.
It checks for suspicious or unexpected entries inside known auto-start and service keys.

It complements your earlier scripts (Service Checker & EXE Path Checker) by focusing on **Registry abuse detection**.
"""

import winreg as reg
from tabulate import tabulate

# Define keys to audit
AUDIT_KEYS = [
    {
        'root': reg.HKEY_CURRENT_USER,
        'path': r"Software\Microsoft\Windows\CurrentVersion\Run",
        'description': 'User Run (Auto-start apps at login)'
    },
    {
        'root': reg.HKEY_LOCAL_MACHINE,
        'path': r"Software\Microsoft\Windows\CurrentVersion\Run",
        'description': 'Machine Run (Auto-start apps for all users)'
    },
    {
        'root': reg.HKEY_LOCAL_MACHINE,
        'path': r"SYSTEM\CurrentControlSet\Services",
        'description': 'Installed Services'
    },
    {
        'root': reg.HKEY_LOCAL_MACHINE,
        'path': r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon",
        'description': 'Winlogon (Shell hijack risk)'
    },
    {
        'root': reg.HKEY_LOCAL_MACHINE,
        'path': r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows",
        'description': 'AppInit_DLLs (DLL injection risk)'
    }
]

def read_registry_key(root, path):
    results = []
    try:
        key = reg.OpenKey(root, path)
        i = 0
        while True:
            try:
                value_name, value_data, value_type = reg.EnumValue(key, i)
                results.append((value_name, value_data))
                i += 1
            except OSError:
                break
        reg.CloseKey(key)
    except FileNotFoundError:
        return []
    return results

def audit_registry():
    all_findings = []

    for item in AUDIT_KEYS:
        findings = read_registry_key(item['root'], item['path'])
        if findings:
            for name, data in findings:
                all_findings.append([item['description'], item['path'], name, data])

    if all_findings:
        print("\n[+] Suspicious or existing entries found:")
        headers = ["Category", "Registry Path", "Value Name", "Data"]
        print(tabulate(all_findings, headers=headers, tablefmt="grid"))
    else:
        print("\n[OK] No suspicious entries found in monitored Registry keys.")

if __name__ == "__main__":
    audit_registry()
