# === INSTALLATION & USAGE (on Windows) ===
# 1. Install Python from https://www.python.org/downloads/ (if not already installed)
# 2. Open Command Prompt (cmd) as Administrator
# 3. Install required dependency:
#    pip install psutil
# 4. Save this script as check_process_paths.py
# 5. Run the script with:
#    python check_process_paths.py

"""
This program was created to help users and system administrators verify the legitimacy
of critical Windows system processes. Malware and malicious actors often disguise their
programs by using the names of trusted Windows executables (such as spoolsv.exe or lsass.exe),
but place them in incorrect or suspicious locations on the file system.

By comparing the actual file paths of running processes against their expected official locations,
this tool quickly alerts the user if any known critical process is running from an unexpected directory —
a strong indicator of a possible malware infection or system compromise.

In short, this program is a fast and effective way to check for process impersonation and
improve system security visibility.
"""

import psutil
import os

# List of processes to monitor and their expected absolute paths
expected_locations = {
    "spoolsv.exe": r"C:\\Windows\\System32\\spoolsv.exe",
    "WerFault.exe": r"C:\\Windows\\System32\\WerFault.exe",
    "explorer.exe": r"C:\\Windows\\explorer.exe",
    "lsass.exe": r"C:\\Windows\\System32\\lsass.exe",
    # You can add more processes here as needed
}

def check_process_locations():
    print("Checking running processes and their file locations...\n")

    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            proc_name = proc.info['name']
            proc_exe = proc.info['exe']

            if proc_name in expected_locations:
                expected_path = expected_locations[proc_name]

                if proc_exe is None:
                    print(f"[?] {proc_name} (PID {proc.pid}) – File path NOT FOUND")
                    continue

                # Normalize paths (Windows is case-insensitive)
                if os.path.normcase(proc_exe) != os.path.normcase(expected_path):
                    print(f"[!] {proc_name} (PID {proc.pid}) – Expected: {expected_path} | Found: {proc_exe}")
                else:
                    print(f"[OK] {proc_name} (PID {proc.pid}) – Location is correct")

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

if __name__ == "__main__":
    check_process_locations()
