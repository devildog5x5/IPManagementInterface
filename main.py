#!/usr/bin/env python3
"""
IP Device Management Interface
A desktop application for managing and monitoring IP devices
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import threading
import socket
import subprocess
import platform
from datetime import datetime
from ipaddress import ip_address, ip_network
import ping3


class IPDeviceManager:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Device Management Interface")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Data file
        self.data_file = "devices.json"
        self.devices = self.load_devices()
        
        # Create UI
        self.create_menu()
        self.create_toolbar()
        self.create_main_panel()
        self.create_status_bar()
        
        # Auto-refresh timer
        self.auto_refresh = False
        self.refresh_interval = 30  # seconds
        
    def create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Devices...", command=self.import_devices)
        file_menu.add_command(label="Export Devices...", command=self.export_devices)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Network Scanner", command=self.open_network_scanner)
        tools_menu.add_command(label="Port Scanner", command=self.open_port_scanner)
        tools_menu.add_command(label="Network Info", command=self.show_network_info)
        tools_menu.add_separator()
        tools_menu.add_command(label="Ping All Devices", command=self.ping_all_devices)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Auto Refresh", command=self.toggle_auto_refresh)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_toolbar(self):
        """Create toolbar with common actions"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="➕ Add Device", command=self.add_device).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="✏️ Edit", command=self.edit_device).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🗑️ Delete", command=self.delete_device).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🔄 Refresh", command=self.refresh_devices).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📡 Ping", command=self.ping_selected).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(toolbar, text="🔍 Scan Network", command=self.open_network_scanner).pack(side=tk.LEFT, padx=2)
    
    def create_main_panel(self):
        """Create main content panel"""
        # Left panel - Device list
        left_panel = ttk.Frame(self.root)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(left_panel, text="IP Devices", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        # Search box
        search_frame = ttk.Frame(left_panel)
        search_frame.pack(fill=tk.X, pady=(5, 10))
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_devices)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Device list treeview
        tree_frame = ttk.Frame(left_panel)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Name", "IP Address", "Status", "Last Seen", "Notes")
        self.device_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            self.device_tree.heading(col, text=col)
            self.device_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.device_tree.yview)
        self.device_tree.configure(yscrollcommand=scrollbar.set)
        
        self.device_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.device_tree.bind("<Double-1>", lambda e: self.edit_device())
        self.device_tree.bind("<Button-3>", self.show_context_menu)
        
        # Right panel - Device details
        right_panel = ttk.LabelFrame(self.root, text="Device Details", padding=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=5, pady=5, ipadx=5, ipady=5)
        right_panel.config(width=300)
        
        self.detail_text = scrolledtext.ScrolledText(right_panel, width=35, height=30, wrap=tk.WORD)
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        
        self.device_tree.bind("<<TreeviewSelect>>", self.show_device_details)
        
        # Refresh device list
        self.refresh_device_list()
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_devices(self):
        """Load devices from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load devices: {e}")
                return []
        return []
    
    def save_devices(self):
        """Save devices to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.devices, f, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save devices: {e}")
            return False
    
    def refresh_device_list(self):
        """Refresh the device list display"""
        # Clear existing items
        for item in self.device_tree.get_children():
            self.device_tree.delete(item)
        
        # Add devices
        for device in self.devices:
            status = device.get("status", "Unknown")
            last_seen = device.get("last_seen", "Never")
            self.device_tree.insert("", tk.END, values=(
                device.get("name", ""),
                device.get("ip", ""),
                status,
                last_seen,
                device.get("notes", "")[:30] + "..." if len(device.get("notes", "")) > 30 else device.get("notes", "")
            ))
    
    def filter_devices(self, *args):
        """Filter devices based on search term"""
        search_term = self.search_var.get().lower()
        for item in self.device_tree.get_children():
            values = self.device_tree.item(item, "values")
            if any(search_term in str(v).lower() for v in values):
                self.device_tree.item(item, tags=("visible",))
            else:
                self.device_tree.item(item, tags=("hidden",))
        
        # Hide items with "hidden" tag
        self.device_tree.tag_configure("hidden", foreground="")
        for item in self.device_tree.get_children():
            if "hidden" in self.device_tree.item(item, "tags"):
                self.device_tree.detach(item)
            else:
                self.device_tree.reattach(item, "", 0)
    
    def add_device(self):
        """Open dialog to add a new device"""
        dialog = DeviceDialog(self.root, "Add Device")
        if dialog.result:
            device = dialog.result
            device["status"] = "Unknown"
            device["last_seen"] = "Never"
            self.devices.append(device)
            if self.save_devices():
                self.refresh_device_list()
                self.status_bar.config(text=f"Device '{device['name']}' added successfully")
    
    def edit_device(self):
        """Edit selected device"""
        selection = self.device_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to edit")
            return
        
        item = selection[0]
        index = self.device_tree.index(item)
        device = self.devices[index]
        
        dialog = DeviceDialog(self.root, "Edit Device", device)
        if dialog.result:
            self.devices[index].update(dialog.result)
            if self.save_devices():
                self.refresh_device_list()
                self.status_bar.config(text=f"Device '{device['name']}' updated successfully")
    
    def delete_device(self):
        """Delete selected device"""
        selection = self.device_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to delete")
            return
        
        item = selection[0]
        index = self.device_tree.index(item)
        device = self.devices[index]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{device['name']}'?"):
            self.devices.pop(index)
            if self.save_devices():
                self.refresh_device_list()
                self.status_bar.config(text=f"Device '{device['name']}' deleted")
    
    def show_device_details(self, event):
        """Show details of selected device"""
        selection = self.device_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        index = self.device_tree.index(item)
        device = self.devices[index]
        
        details = f"Name: {device.get('name', 'N/A')}\n"
        details += f"IP Address: {device.get('ip', 'N/A')}\n"
        details += f"MAC Address: {device.get('mac', 'N/A')}\n"
        details += f"Status: {device.get('status', 'Unknown')}\n"
        details += f"Last Seen: {device.get('last_seen', 'Never')}\n"
        details += f"Device Type: {device.get('type', 'N/A')}\n"
        details += f"Location: {device.get('location', 'N/A')}\n"
        details += f"\nNotes:\n{device.get('notes', 'N/A')}\n"
        
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(1.0, details)
    
    def show_context_menu(self, event):
        """Show context menu for device list"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Edit", command=self.edit_device)
        menu.add_command(label="Delete", command=self.delete_device)
        menu.add_separator()
        menu.add_command(label="Ping", command=self.ping_selected)
        menu.add_command(label="Port Scan", command=lambda: self.port_scan_selected())
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def ping_selected(self):
        """Ping the selected device"""
        selection = self.device_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to ping")
            return
        
        item = selection[0]
        index = self.device_tree.index(item)
        device = self.devices[index]
        ip = device.get('ip', '')
        
        if not ip:
            messagebox.showerror("Error", "Device has no IP address")
            return
        
        self.status_bar.config(text=f"Pinging {ip}...")
        threading.Thread(target=self.ping_device, args=(ip, index), daemon=True).start()
    
    def ping_device(self, ip, index=None):
        """Ping a device and update status"""
        try:
            response_time = ping3.ping(ip, timeout=3)
            if response_time is not None:
                status = "Online"
                last_seen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.status_bar.config(text=f"{ip} is online (Response: {response_time*1000:.2f}ms)")
            else:
                status = "Offline"
                last_seen = self.devices[index].get('last_seen', 'Never') if index is not None else 'Never'
                self.status_bar.config(text=f"{ip} is offline")
        except Exception as e:
            status = "Error"
            self.status_bar.config(text=f"Error pinging {ip}: {e}")
            return
        
        if index is not None:
            self.devices[index]['status'] = status
            if status == "Online":
                self.devices[index]['last_seen'] = last_seen
            self.save_devices()
            self.root.after(0, self.refresh_device_list)
    
    def ping_all_devices(self):
        """Ping all devices"""
        if not self.devices:
            messagebox.showinfo("No Devices", "No devices to ping")
            return
        
        self.status_bar.config(text="Pinging all devices...")
        for i, device in enumerate(self.devices):
            ip = device.get('ip', '')
            if ip:
                threading.Thread(target=self.ping_device, args=(ip, i), daemon=True).start()
    
    def refresh_devices(self):
        """Refresh device status"""
        self.refresh_device_list()
        self.status_bar.config(text="Device list refreshed")
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh feature"""
        self.auto_refresh = not self.auto_refresh
        if self.auto_refresh:
            self.schedule_refresh()
            self.status_bar.config(text="Auto-refresh enabled")
        else:
            self.status_bar.config(text="Auto-refresh disabled")
    
    def schedule_refresh(self):
        """Schedule next auto-refresh"""
        if self.auto_refresh:
            self.ping_all_devices()
            self.root.after(self.refresh_interval * 1000, self.schedule_refresh)
    
    def open_network_scanner(self):
        """Open network scanner window"""
        NetworkScannerWindow(self.root, self)
    
    def open_port_scanner(self):
        """Open port scanner window"""
        PortScannerWindow(self.root)
    
    def port_scan_selected(self):
        """Port scan the selected device"""
        selection = self.device_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to scan")
            return
        
        item = selection[0]
        index = self.device_tree.index(item)
        device = self.devices[index]
        ip = device.get('ip', '')
        
        if not ip:
            messagebox.showerror("Error", "Device has no IP address")
            return
        
        PortScannerWindow(self.root, target_ip=ip)
    
    def show_network_info(self):
        """Show network information"""
        NetworkInfoWindow(self.root)
    
    def import_devices(self):
        """Import devices from JSON file"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title="Import Devices",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    imported = json.load(f)
                self.devices.extend(imported)
                if self.save_devices():
                    self.refresh_device_list()
                    self.status_bar.config(text=f"Imported {len(imported)} devices")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import devices: {e}")
    
    def export_devices(self):
        """Export devices to JSON file"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            title="Export Devices",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.devices, f, indent=2)
                self.status_bar.config(text=f"Exported {len(self.devices)} devices")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export devices: {e}")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", 
            "IP Device Management Interface\n\n"
            "Version 1.0\n\n"
            "A comprehensive tool for managing and monitoring IP devices on your network.")


class DeviceDialog:
    def __init__(self, parent, title, device=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Fields
        ttk.Label(self.dialog, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.name_var = tk.StringVar(value=device.get('name', '') if device else '')
        ttk.Entry(self.dialog, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(self.dialog, text="IP Address:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.ip_var = tk.StringVar(value=device.get('ip', '') if device else '')
        ttk.Entry(self.dialog, textvariable=self.ip_var, width=30).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(self.dialog, text="MAC Address:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.mac_var = tk.StringVar(value=device.get('mac', '') if device else '')
        ttk.Entry(self.dialog, textvariable=self.mac_var, width=30).grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(self.dialog, text="Device Type:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.type_var = tk.StringVar(value=device.get('type', '') if device else '')
        type_combo = ttk.Combobox(self.dialog, textvariable=self.type_var, width=27)
        type_combo['values'] = ('Router', 'Switch', 'Server', 'Workstation', 'Printer', 'Camera', 'IoT Device', 'Other')
        type_combo.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(self.dialog, text="Location:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        self.location_var = tk.StringVar(value=device.get('location', '') if device else '')
        ttk.Entry(self.dialog, textvariable=self.location_var, width=30).grid(row=4, column=1, padx=10, pady=5)
        
        ttk.Label(self.dialog, text="Notes:").grid(row=5, column=0, sticky=tk.NW, padx=10, pady=5)
        self.notes_text = tk.Text(self.dialog, width=30, height=5)
        self.notes_text.grid(row=5, column=1, padx=10, pady=5)
        if device:
            self.notes_text.insert(1.0, device.get('notes', ''))
        
        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        self.dialog.wait_window()
    
    def ok_clicked(self):
        """Handle OK button click"""
        name = self.name_var.get().strip()
        ip = self.ip_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Name is required")
            return
        
        if not ip:
            messagebox.showerror("Error", "IP address is required")
            return
        
        # Validate IP address
        try:
            ip_address(ip)
        except ValueError:
            messagebox.showerror("Error", "Invalid IP address")
            return
        
        self.result = {
            'name': name,
            'ip': ip,
            'mac': self.mac_var.get().strip(),
            'type': self.type_var.get().strip(),
            'location': self.location_var.get().strip(),
            'notes': self.notes_text.get(1.0, tk.END).strip()
        }
        
        self.dialog.destroy()


class NetworkScannerWindow:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        
        self.window = tk.Toplevel(parent)
        self.window.title("Network Scanner")
        self.window.geometry("600x500")
        
        ttk.Label(self.window, text="Network Range (e.g., 192.168.1.0/24):").pack(pady=10)
        
        input_frame = ttk.Frame(self.window)
        input_frame.pack(pady=5)
        
        self.network_var = tk.StringVar(value="192.168.1.0/24")
        ttk.Entry(input_frame, textvariable=self.network_var, width=25).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Scan", command=self.start_scan).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.window, text="Scan Results:").pack(pady=(20, 5))
        
        # Results treeview
        tree_frame = ttk.Frame(self.window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("IP Address", "Status", "Hostname")
        self.result_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_tree.bind("<Double-1>", self.add_device_from_scan)
        
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Add Selected to Devices", command=self.add_device_from_scan).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        
        self.scan_results = []
    
    def start_scan(self):
        """Start network scan"""
        network_str = self.network_var.get().strip()
        
        try:
            network = ip_network(network_str, strict=False)
        except ValueError:
            messagebox.showerror("Error", "Invalid network range")
            return
        
        # Clear previous results
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.scan_results = []
        
        self.status_label = ttk.Label(self.window, text="Scanning...")
        self.status_label.pack()
        
        threading.Thread(target=self.scan_network, args=(network,), daemon=True).start()
    
    def scan_network(self, network):
        """Scan network for active hosts"""
        hosts = list(network.hosts())
        total = len(hosts)
        found = 0
        
        for i, host in enumerate(hosts):
            ip = str(host)
            try:
                response_time = ping3.ping(ip, timeout=1)
                if response_time is not None:
                    found += 1
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                    except:
                        hostname = "Unknown"
                    
                    result = {'ip': ip, 'hostname': hostname, 'status': 'Online'}
                    self.scan_results.append(result)
                    
                    self.window.after(0, lambda r=result: self.result_tree.insert(
                        "", tk.END, values=(r['ip'], r['status'], r['hostname'])
                    ))
            except:
                pass
            
            if i % 10 == 0:
                self.window.after(0, lambda: self.status_label.config(
                    text=f"Scanning... {i}/{total} ({found} found)"
                ))
        
        self.window.after(0, lambda: self.status_label.config(
            text=f"Scan complete. Found {found} active hosts."
        ))
    
    def add_device_from_scan(self, event=None):
        """Add selected scan result to devices"""
        selection = self.result_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to add")
            return
        
        item = selection[0]
        values = self.result_tree.item(item, "values")
        ip = values[0]
        hostname = values[2]
        
        # Check if device already exists
        for device in self.main_app.devices:
            if device.get('ip') == ip:
                messagebox.showinfo("Exists", f"Device with IP {ip} already exists")
                return
        
        device = {
            'name': hostname if hostname != "Unknown" else f"Device-{ip}",
            'ip': ip,
            'mac': '',
            'type': 'Unknown',
            'location': '',
            'notes': f"Discovered via network scan",
            'status': 'Online',
            'last_seen': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.main_app.devices.append(device)
        if self.main_app.save_devices():
            self.main_app.refresh_device_list()
            messagebox.showinfo("Success", f"Device '{device['name']}' added successfully")


class PortScannerWindow:
    def __init__(self, parent, target_ip=None):
        self.window = tk.Toplevel(parent)
        self.window.title("Port Scanner")
        self.window.geometry("500x400")
        
        ttk.Label(self.window, text="Target IP:").pack(pady=10)
        
        input_frame = ttk.Frame(self.window)
        input_frame.pack(pady=5)
        
        self.ip_var = tk.StringVar(value=target_ip if target_ip else "")
        ttk.Entry(input_frame, textvariable=self.ip_var, width=20).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(input_frame, text="Ports:").pack(side=tk.LEFT, padx=5)
        self.ports_var = tk.StringVar(value="1-1000")
        ttk.Entry(input_frame, textvariable=self.ports_var, width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, text="Scan", command=self.start_scan).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.window, text="Open Ports:").pack(pady=(20, 5))
        
        # Results
        self.result_text = scrolledtext.ScrolledText(self.window, width=50, height=15)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=10)
    
    def start_scan(self):
        """Start port scan"""
        ip = self.ip_var.get().strip()
        ports_str = self.ports_var.get().strip()
        
        if not ip:
            messagebox.showerror("Error", "IP address is required")
            return
        
        try:
            ip_address(ip)
        except ValueError:
            messagebox.showerror("Error", "Invalid IP address")
            return
        
        # Parse port range
        try:
            if '-' in ports_str:
                start, end = map(int, ports_str.split('-'))
                ports = range(start, end + 1)
            else:
                ports = [int(ports_str)]
        except:
            messagebox.showerror("Error", "Invalid port range")
            return
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Scanning {ip}...\n\n")
        
        threading.Thread(target=self.scan_ports, args=(ip, ports), daemon=True).start()
    
    def scan_ports(self, ip, ports):
        """Scan ports on target IP"""
        open_ports = []
        total = len(ports)
        
        for i, port in enumerate(ports):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    open_ports.append(port)
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "Unknown"
                    self.window.after(0, lambda p=port, s=service: self.result_text.insert(
                        tk.END, f"Port {p}: OPEN ({s})\n"
                    ))
            except:
                pass
            
            if i % 100 == 0:
                self.window.after(0, lambda: self.result_text.insert(
                    tk.END, f"Progress: {i}/{total} ports scanned...\n"
                ))
        
        self.window.after(0, lambda: self.result_text.insert(
            tk.END, f"\nScan complete. Found {len(open_ports)} open ports.\n"
        ))


class NetworkInfoWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Network Information")
        self.window.geometry("500x400")
        
        self.info_text = scrolledtext.ScrolledText(self.window, width=60, height=20)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(self.window, text="Refresh", command=self.refresh_info).pack(pady=5)
        ttk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=5)
        
        self.refresh_info()
    
    def refresh_info(self):
        """Refresh network information"""
        info = "Network Information\n" + "=" * 50 + "\n\n"
        
        # Hostname
        try:
            hostname = socket.gethostname()
            info += f"Hostname: {hostname}\n"
        except:
            info += "Hostname: Unable to determine\n"
        
        # IP Address
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            info += f"Local IP Address: {local_ip}\n"
        except:
            info += "Local IP Address: Unable to determine\n"
        
        # Network interfaces (platform specific)
        info += "\nNetwork Interfaces:\n"
        info += "-" * 50 + "\n"
        
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['ipconfig'], capture_output=True, text=True, timeout=5)
                info += result.stdout
            else:
                result = subprocess.run(['ifconfig'], capture_output=True, text=True, timeout=5)
                info += result.stdout
        except Exception as e:
            info += f"Error retrieving network interfaces: {e}\n"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = IPDeviceManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()

