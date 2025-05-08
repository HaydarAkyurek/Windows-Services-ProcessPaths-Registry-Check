import subprocess   # To run Windows service commands
import os   # For file path operations
import platform   # To check OS version
import tkinter as tk   # For GUI interface
from tkinter import messagebox, filedialog   # For dialogs and file saving

# ----------------------
# Define default Windows services (sample list)
# ----------------------
default_services = {
    'AeLookupSvc', 'Appinfo', 'AppMgmt', 'AudioSrv', 'BITS', 'BrokerInfrastructure',
    'CertPropSvc', 'CoreMessagingRegistrar', 'CryptSvc', 'DcomLaunch', 'Dhcp',
    'Dnscache', 'EventLog', 'EventSystem', 'FontCache', 'gpsvc', 'IKEEXT',
    'iphlpsvc', 'LanmanServer', 'LanmanWorkstation', 'lmhosts', 'Netman', 'NlaSvc',
    'PlugPlay', 'Power', 'RpcSs', 'Schedule', 'SENS', 'ShellHWDetection', 'Spooler',
    'Themes', 'Winmgmt'
}   # These are considered "default/legitimate" Windows services

# ----------------------
# Functions to get current services
# ----------------------
def get_current_services():
    services = set()   # Initialize empty set to store service names
    result = subprocess.run(["sc", "query", "type=", "service", "state=", "all"], capture_output=True, text=True)   # Run 'sc query' to get all services
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("SERVICE_NAME:"):   # Extract service name lines
            service_name = line.split("SERVICE_NAME:")[1].strip()
            services.add(service_name)
    return services   # Return set of all running/installed services

def get_service_details(service_name):
    result = subprocess.run(["sc", "qc", service_name], capture_output=True, text=True)   # Query config/details of specific service
    return result.stdout.strip()   # Return output as string

# ----------------------
# GUI Functions
# ----------------------
def scan_services():
    current = get_current_services()   # Get all current services
    extras = current - default_services   # Find services that are NOT in default list
    listbox_services.delete(0, tk.END)   # Clear listbox
    for svc in sorted(extras):   # Insert each extra service found
        listbox_services.insert(tk.END, svc)

def show_service_details(event):
    selection = listbox_services.curselection()   # Get selected service from list
    if selection:
        svc_name = listbox_services.get(selection[0])
        details = get_service_details(svc_name)   # Get its details
        text_details.delete(1.0, tk.END)   # Clear text box
        text_details.insert(tk.END, f"Service: {svc_name}\n\n{details}")   # Display service details

def save_results():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])   # Open save dialog
    if file_path:
        with open(file_path, 'w') as f:   # Write results to file
            f.write("Extra Services:\n")
            for i in range(listbox_services.size()):
                f.write(f"- {listbox_services.get(i)}\n")
        messagebox.showinfo("Saved", f"Results saved to {file_path}")   # Notify user

def check_windows_version():
    version = platform.platform()   # Get OS version info
    if "Windows" not in version:
        messagebox.showerror("Error", "This tool is designed for Windows only.")   # Exit if not Windows
        root.destroy()
    return version   # Return OS version string

# ----------------------
# GUI Setup
# ----------------------
root = tk.Tk()   # Create main window
root.title("Windows Extra Services Checker")   # Set window title
root.geometry("600x500")   # Set window size

version_info = check_windows_version()   # Check and display OS version

frame_buttons = tk.Frame(root)   # Create frame for buttons
frame_buttons.pack(pady=5)

btn_scan_services = tk.Button(frame_buttons, text="Scan Services", command=scan_services)   # Button to scan services
btn_scan_services.grid(row=0, column=0, padx=5)

btn_save = tk.Button(frame_buttons, text="Save Results", command=save_results)   # Button to save results
btn_save.grid(row=0, column=1, padx=5)

listbox_services = tk.Listbox(root)   # Listbox to show extra services
listbox_services.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
listbox_services.bind('<<ListboxSelect>>', show_service_details)   # Bind selection to show details

text_details = tk.Text(root, height=10)   # Text area to show service details
text_details.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

lbl_info = tk.Label(root, text=f"Running on: {version_info}")   # Label to show Windows version
lbl_info.pack(pady=3)

root.mainloop()   # Run the GUI event loop
