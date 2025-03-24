import os
import subprocess
import pywhatkit
import schedule
import time
import psutil
import threading
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import json

# License File to Store Activated Keys
LICENSE_FILE = "license_data.json"

# Predefined License Keys with Expiry Date
VALID_LICENSE_KEYS = {
    "ABC123-XYZ789-LIC001": None,
    "DEF456-UVW123-LIC002": None,
    "GHI789-RST456-LIC003": None,
    "JKL012-MNO789-LIC004": None,
    "PQR345-CDE567-LIC005": None,
    "STU678-BCD890-LIC006": None,
    "VWX901-YZA234-LIC007": None,
    "MNB567-LOP123-LIC008": None,
    "QWE234-ASD345-LIC009": None,
    "ZXC567-ERT678-LIC010": None
}

# Store logs
desktop_status_logs = {}
bandwidth_usage_logs = {}
monitoring = {}
threads = []
graph_axes = []

def load_license_data():
    """Load license data from file."""
    if os.path.exists(LICENSE_FILE):
        with open(LICENSE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_license_data(data):
    """Save license data to file."""
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f)

def validate_license():
    """Check if the entered license key is valid and not expired."""
    entered_license = license_entry.get().strip()
    license_data = load_license_data()
    
    if entered_license in VALID_LICENSE_KEYS:
        if entered_license in license_data:
            expiry_date = datetime.strptime(license_data[entered_license], "%Y-%m-%d")
            if expiry_date > datetime.now():
                messagebox.showinfo("Success", "License validated successfully!")
                license_window.destroy()
                setup_main_gui()
                return
            else:
                messagebox.showerror("Error", "License expired. Please enter a new key.")
        else:
            expiry_date = datetime.now() + timedelta(days=30)
            license_data[entered_license] = expiry_date.strftime("%Y-%m-%d")
            save_license_data(license_data)
            messagebox.showinfo("Success", "License activated successfully!")
            license_window.destroy()
            setup_main_gui()
            return
    
    messagebox.showerror("Error", "Invalid license key. Please enter a valid key.")

def show_license_window():
    """Display a license entry window on startup."""
    global license_window, license_entry
    license_window = tk.Toplevel(root)
    license_window.title("License Activation")
    tk.Label(license_window, text="Enter License Key:").pack(pady=5)
    license_entry = tk.Entry(license_window, width=30)
    license_entry.pack(pady=5)
    tk.Button(license_window, text="Activate", command=validate_license).pack(pady=10)
    license_window.protocol("WM_DELETE_WINDOW", root.destroy)
    license_window.mainloop()

def setup_main_gui():
    """Setup the main GUI after license validation."""
    global ip_entry, whatsapp_entry, canvas, fig
    
    tk.Label(root, text="Enter Desktop IP:").grid(row=0, column=0, padx=10, pady=5)
    ip_entry = tk.Entry(root, width=30)
    ip_entry.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(root, text="Enter WhatsApp Number:").grid(row=1, column=0, padx=10, pady=5)
    whatsapp_entry = tk.Entry(root, width=30)
    whatsapp_entry.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Button(root, text="Start Monitoring", command=start_monitoring).grid(row=2, column=0, pady=10)
    tk.Button(root, text="Stop Monitoring", command=stop_monitoring).grid(row=2, column=1, pady=10)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
    graph_axes.extend([ax1, ax2])
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, pady=10)

def monitor_desktop(ip, whatsapp_number):
    """Monitor the connectivity and bandwidth usage of the given IP."""
    global monitoring
    monitoring[ip] = True
    desktop_status_logs[ip] = []
    bandwidth_usage_logs[ip] = []
    while monitoring[ip]:
        print(f"🔍 Checking connectivity for {ip}...")
        is_online = True  # Simulated check
        status = "ONLINE" if is_online else "OFFLINE"
        desktop_status_logs[ip].append(status)
        bandwidth_usage_logs[ip].append(100)  # Simulated bandwidth usage
        update_graph()
        time.sleep(1)

def update_graph():
    """Update the monitoring graph dynamically with bandwidth data."""
    fig.clear()
    ax1, ax2 = graph_axes
    
    ax1.clear()
    ax1.set_title("Desktop Connectivity")
    for ip, status_log in desktop_status_logs.items():
        ax1.plot(range(len(status_log)), [1 if s == "ONLINE" else 0 for s in status_log], marker='o', linestyle='-', label=f'Status {ip}')
    ax1.legend()
    
    ax2.clear()
    ax2.set_title("Bandwidth Usage")
    for ip, bandwidth_log in bandwidth_usage_logs.items():
        ax2.plot(range(len(bandwidth_log)), bandwidth_log, marker='o', linestyle='-', label=f'Bandwidth {ip}', color='g')
    ax2.legend()
    
    canvas.draw()

def start_monitoring():
    desktop_ip = ip_entry.get().strip()
    whatsapp_number = whatsapp_entry.get().strip()
    if not desktop_ip or not whatsapp_number:
        messagebox.showerror("Error", "Please enter a valid IP and WhatsApp number!")
        return
    thread = threading.Thread(target=monitor_desktop, args=(desktop_ip, whatsapp_number), daemon=True)
    threads.append(thread)
    thread.start()

def stop_monitoring():
    global monitoring
    for ip in monitoring.keys():
        monitoring[ip] = False
    print("🛑 Monitoring stopped.")
    update_graph()

# GUI Setup
root = tk.Tk()
root.title("Admin Console - Multi-Desktop Connectivity & Bandwidth Monitor")
show_license_window()
root.mainloop()
