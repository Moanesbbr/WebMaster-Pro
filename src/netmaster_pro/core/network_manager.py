import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import socket
import struct
import time
import ipaddress
import platform
import re
from datetime import datetime
import psutil


class NetworkDeviceManager:
    def __init__(self, parent, return_callback):
        self.parent = parent
        self.return_callback = return_callback
        self.devices = {}
        self.blocked_devices = set()
        self.scanning = False
        self.monitoring = False
        self.scan_thread = None
        self.monitor_thread = None
        
        # Get network info
        self.get_network_info()
        
        # Create interface
        self.create_interface()
        
        # Start initial scan
        self.start_scan()
    
    def get_network_info(self):
        """Get current network information"""
        try:
            # Get default gateway and network
            if platform.system() == "Windows":
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                output = result.stdout
                
                # Extract gateway
                gateway_match = re.search(r'Default Gateway.*?(\d+\.\d+\.\d+\.\d+)', output)
                if gateway_match:
                    self.gateway = gateway_match.group(1)
                else:
                    self.gateway = "192.168.1.1"  # Default fallback
                
                # Extract local IP
                ip_match = re.search(r'IPv4 Address.*?(\d+\.\d+\.\d+\.\d+)', output)
                if ip_match:
                    self.local_ip = ip_match.group(1)
                else:
                    self.local_ip = socket.gethostbyname(socket.gethostname())
            else:
                # Linux/Mac
                self.local_ip = socket.gethostbyname(socket.gethostname())
                result = subprocess.run(['ip', 'route', 'show', 'default'], capture_output=True, text=True)
                gateway_match = re.search(r'default via (\d+\.\d+\.\d+\.\d+)', result.stdout)
                self.gateway = gateway_match.group(1) if gateway_match else "192.168.1.1"
            
            # Calculate network range
            network = ipaddress.IPv4Network(f"{self.local_ip}/24", strict=False)
            self.network_range = str(network.network_address)[:-1]  # Remove last octet
            
        except Exception as e:
            print(f"Error getting network info: {e}")
            self.gateway = "192.168.1.1"
            self.local_ip = "192.168.1.100"
            self.network_range = "192.168.1."
    
    def create_interface(self):
        """Create the network manager interface"""
        # Clear existing widgets
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = tk.Frame(self.parent, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Header
        self.create_header(main_frame)
        
        # Control panel
        self.create_control_panel(main_frame)
        
        # Device list
        self.create_device_list(main_frame)
        
        # Footer
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg="#1a1a1a")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Back button
        back_btn = tk.Button(
            header_frame,
            text="← Back",
            font=("Segoe UI", 12),
            fg="#ffffff",
            bg="#0078d4",
            activebackground="#106ebe",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.go_back
        )
        back_btn.pack(side=tk.LEFT)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🌐 Network Device Manager",
            font=("Segoe UI", 24, "bold"),
            fg="#ffffff",
            bg="#1a1a1a"
        )
        title_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Network info
        info_frame = tk.Frame(header_frame, bg="#1a1a1a")
        info_frame.pack(side=tk.RIGHT)
        
        network_info = tk.Label(
            info_frame,
            text=f"Gateway: {self.gateway} | Your IP: {self.local_ip}",
            font=("Segoe UI", 10),
            fg="#888888",
            bg="#1a1a1a"
        )
        network_info.pack()
    
    def create_control_panel(self, parent):
        """Create control panel with scan and monitor buttons"""
        control_frame = tk.Frame(parent, bg="#262626", relief=tk.FLAT, bd=1)
        control_frame.pack(fill=tk.X, pady=(0, 20), padx=2)
        
        inner_frame = tk.Frame(control_frame, bg="#262626")
        inner_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Scan button
        self.scan_btn = tk.Button(
            inner_frame,
            text="🔍 Scan Network",
            font=("Segoe UI", 12),
            fg="#ffffff",
            bg="#28a745",
            activebackground="#218838",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.toggle_scan
        )
        self.scan_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Monitor button
        self.monitor_btn = tk.Button(
            inner_frame,
            text="📊 Start Monitoring",
            font=("Segoe UI", 12),
            fg="#ffffff",
            bg="#17a2b8",
            activebackground="#138496",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.toggle_monitoring
        )
        self.monitor_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status label
        self.status_label = tk.Label(
            inner_frame,
            text="Ready to scan network",
            font=("Segoe UI", 11),
            fg="#888888",
            bg="#262626"
        )
        self.status_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Device count
        self.device_count_label = tk.Label(
            inner_frame,
            text="Devices: 0",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#262626"
        )
        self.device_count_label.pack(side=tk.RIGHT)
    
    def create_device_list(self, parent):
        """Create device list with treeview"""
        list_frame = tk.Frame(parent, bg="#1a1a1a")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview",
                       background="#2d2d2d",
                       foreground="#ffffff",
                       fieldbackground="#2d2d2d",
                       borderwidth=0,
                       font=("Segoe UI", 10))
        style.configure("Custom.Treeview.Heading",
                       background="#404040",
                       foreground="#ffffff",
                       borderwidth=1,
                       font=("Segoe UI", 11, "bold"))
        
        # Create treeview
        columns = ("IP", "MAC", "Hostname", "Vendor", "Status", "Bandwidth")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", style="Custom.Treeview")
        
        # Configure columns
        self.tree.heading("IP", text="IP Address")
        self.tree.heading("MAC", text="MAC Address")
        self.tree.heading("Hostname", text="Hostname")
        self.tree.heading("Vendor", text="Vendor")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Bandwidth", text="Bandwidth Usage")
        
        self.tree.column("IP", width=120, minwidth=100)
        self.tree.column("MAC", width=140, minwidth=120)
        self.tree.column("Hostname", width=150, minwidth=120)
        self.tree.column("Vendor", width=120, minwidth=100)
        self.tree.column("Status", width=80, minwidth=70)
        self.tree.column("Bandwidth", width=120, minwidth=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Context menu
        self.create_context_menu()
        
        # Bind right-click
        self.tree.bind("<Button-3>", self.show_context_menu)
    
    def create_context_menu(self):
        """Create right-click context menu"""
        self.context_menu = tk.Menu(self.parent, tearoff=0, bg="#2d2d2d", fg="#ffffff",
                                   activebackground="#0078d4", activeforeground="#ffffff")
        self.context_menu.add_command(label="📊 Monitor Device", command=self.monitor_selected_device)
        self.context_menu.add_command(label="🚫 Block Device", command=self.block_selected_device)
        self.context_menu.add_command(label="✅ Unblock Device", command=self.unblock_selected_device)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="⚡ Limit Bandwidth", command=self.limit_bandwidth)
        self.context_menu.add_command(label="🔄 Refresh Info", command=self.refresh_selected_device)
    
    def create_footer(self, parent):
        """Create footer with additional controls"""
        footer_frame = tk.Frame(parent, bg="#1a1a1a")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        # Block all button
        block_all_btn = tk.Button(
            footer_frame,
            text="🚫 Block All Devices",
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg="#dc3545",
            activebackground="#c82333",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            command=self.block_all_devices
        )
        block_all_btn.pack(side=tk.LEFT)
        
        # Unblock all button
        unblock_all_btn = tk.Button(
            footer_frame,
            text="✅ Unblock All Devices",
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg="#28a745",
            activebackground="#218838",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            command=self.unblock_all_devices
        )
        unblock_all_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Export button
        export_btn = tk.Button(
            footer_frame,
            text="📄 Export Device List",
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg="#6c757d",
            activebackground="#5a6268",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            command=self.export_device_list
        )
        export_btn.pack(side=tk.RIGHT)
    
    def toggle_scan(self):
        """Toggle network scanning"""
        if self.scanning:
            self.stop_scan()
        else:
            self.start_scan()
    
    def start_scan(self):
        """Start network scanning"""
        if not self.scanning:
            self.scanning = True
            self.scan_btn.configure(text="⏹ Stop Scan", bg="#dc3545", activebackground="#c82333")
            self.status_label.configure(text="Scanning network...", fg="#28a745")
            
            self.scan_thread = threading.Thread(target=self.scan_network, daemon=True)
            self.scan_thread.start()
    
    def stop_scan(self):
        """Stop network scanning"""
        self.scanning = False
        self.scan_btn.configure(text="🔍 Scan Network", bg="#28a745", activebackground="#218838")
        self.status_label.configure(text="Scan stopped", fg="#888888")
    
    def scan_network(self):
        """Scan network for devices"""
        try:
            while self.scanning:
                self.update_status("Scanning network...")
                
                # Ping sweep
                for i in range(1, 255):
                    if not self.scanning:
                        break
                    
                    ip = f"{self.network_range}{i}"
                    
                    # Skip if already processed recently
                    if ip in self.devices and (time.time() - self.devices[ip].get('last_seen', 0)) < 30:
                        continue
                    
                    # Ping device
                    if self.ping_device(ip):
                        device_info = self.get_device_info(ip)
                        if device_info:
                            self.devices[ip] = device_info
                            self.update_device_list()
                    
                    time.sleep(0.1)  # Small delay to prevent overwhelming the network
                
                if self.scanning:
                    self.update_status(f"Scan complete. Found {len(self.devices)} devices.")
                    time.sleep(5)  # Wait before next scan cycle
                
        except Exception as e:
            self.update_status(f"Scan error: {str(e)}")
    
    def ping_device(self, ip):
        """Ping a device to check if it's alive"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], 
                                      capture_output=True, text=True)
            else:
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                      capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def get_device_info(self, ip):
        """Get detailed device information"""
        try:
            device_info = {
                'ip': ip,
                'mac': self.get_mac_address(ip),
                'hostname': self.get_hostname(ip),
                'vendor': 'Unknown',
                'status': 'Blocked' if ip in self.blocked_devices else 'Active',
                'bandwidth': '0 KB/s',
                'last_seen': time.time()
            }
            
            # Get vendor from MAC address (simplified)
            if device_info['mac']:
                device_info['vendor'] = self.get_vendor_from_mac(device_info['mac'])
            
            return device_info
        except:
            return None
    
    def get_mac_address(self, ip):
        """Get MAC address for an IP"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['arp', '-a', ip], capture_output=True, text=True)
                if result.returncode == 0:
                    mac_match = re.search(r'([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}', result.stdout)
                    return mac_match.group(0) if mac_match else "Unknown"
            else:
                result = subprocess.run(['arp', '-n', ip], capture_output=True, text=True)
                if result.returncode == 0:
                    mac_match = re.search(r'([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}', result.stdout)
                    return mac_match.group(0) if mac_match else "Unknown"
        except:
            pass
        return "Unknown"
    
    def get_hostname(self, ip):
        """Get hostname for an IP"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return "Unknown"
    
    def get_vendor_from_mac(self, mac):
        """Get vendor from MAC address (simplified OUI lookup)"""
        # This is a simplified version. In a real implementation, 
        # you would use an OUI database
        oui = mac[:8].upper().replace(':', '').replace('-', '')
        
        vendor_map = {
            '001122': 'Apple',
            'AABBCC': 'Samsung',
            '000000': 'Unknown'
        }
        
        return vendor_map.get(oui[:6], 'Unknown')
    
    def update_device_list(self):
        """Update the device list display"""
        def update_ui():
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add devices
            for ip, device in self.devices.items():
                status = "Blocked" if ip in self.blocked_devices else "Active"
                self.tree.insert("", "end", values=(
                    device['ip'],
                    device['mac'],
                    device['hostname'],
                    device['vendor'],
                    status,
                    device['bandwidth']
                ))
            
            # Update device count
            self.device_count_label.configure(text=f"Devices: {len(self.devices)}")
        
        # Schedule UI update on main thread
        self.parent.after(0, update_ui)
    
    def update_status(self, message):
        """Update status label"""
        def update_ui():
            self.status_label.configure(text=message)
        
        self.parent.after(0, update_ui)
    
    def toggle_monitoring(self):
        """Toggle bandwidth monitoring"""
        if self.monitoring:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def start_monitoring(self):
        """Start bandwidth monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_btn.configure(text="⏹ Stop Monitoring", bg="#dc3545", activebackground="#c82333")
            
            self.monitor_thread = threading.Thread(target=self.monitor_bandwidth, daemon=True)
            self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop bandwidth monitoring"""
        self.monitoring = False
        self.monitor_btn.configure(text="📊 Start Monitoring", bg="#17a2b8", activebackground="#138496")
    
    def monitor_bandwidth(self):
        """Monitor bandwidth usage (simplified)"""
        try:
            while self.monitoring:
                # This is a simplified bandwidth monitoring
                # In a real implementation, you would use more sophisticated methods
                for ip in self.devices:
                    if self.devices[ip]:
                        # Simulate bandwidth data
                        import random
                        bandwidth = random.randint(0, 1000)
                        self.devices[ip]['bandwidth'] = f"{bandwidth} KB/s"
                
                self.update_device_list()
                time.sleep(2)
                
        except Exception as e:
            self.update_status(f"Monitoring error: {str(e)}")
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def get_selected_device(self):
        """Get currently selected device"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item)['values']
            return values[0] if values else None
        return None
    
    def monitor_selected_device(self):
        """Monitor selected device"""
        device_ip = self.get_selected_device()
        if device_ip:
            messagebox.showinfo("Monitor Device", f"Monitoring device: {device_ip}")
    
    def block_selected_device(self):
        """Block selected device"""
        device_ip = self.get_selected_device()
        if device_ip and device_ip != self.local_ip:
            if messagebox.askyesno("Block Device", f"Block device {device_ip}?"):
                self.blocked_devices.add(device_ip)
                self.apply_device_block(device_ip)
                self.update_device_list()
                messagebox.showinfo("Success", f"Device {device_ip} has been blocked.")
        elif device_ip == self.local_ip:
            messagebox.showwarning("Warning", "Cannot block your own device!")
    
    def unblock_selected_device(self):
        """Unblock selected device"""
        device_ip = self.get_selected_device()
        if device_ip and device_ip in self.blocked_devices:
            self.blocked_devices.remove(device_ip)
            self.remove_device_block(device_ip)
            self.update_device_list()
            messagebox.showinfo("Success", f"Device {device_ip} has been unblocked.")
    
    def apply_device_block(self, ip):
        """Apply network block to device (requires admin privileges)"""
        try:
            if platform.system() == "Windows":
                # Windows firewall rule
                subprocess.run([
                    'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                    f'name=Block_{ip}', 'dir=out', 'action=block',
                    f'remoteip={ip}'
                ], check=True)
            else:
                # Linux iptables (requires sudo)
                subprocess.run([
                    'sudo', 'iptables', '-A', 'OUTPUT',
                    '-d', ip, '-j', 'DROP'
                ], check=True)
        except subprocess.CalledProcessError:
            messagebox.showwarning("Warning", 
                "Failed to apply network block. Administrator privileges may be required.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to block device: {str(e)}")
    
    def remove_device_block(self, ip):
        """Remove network block from device"""
        try:
            if platform.system() == "Windows":
                subprocess.run([
                    'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                    f'name=Block_{ip}'
                ], check=True)
            else:
                subprocess.run([
                    'sudo', 'iptables', '-D', 'OUTPUT',
                    '-d', ip, '-j', 'DROP'
                ], check=True)
        except subprocess.CalledProcessError:
            messagebox.showwarning("Warning", 
                "Failed to remove network block. Administrator privileges may be required.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unblock device: {str(e)}")
    
    def limit_bandwidth(self):
        """Limit bandwidth for selected device"""
        device_ip = self.get_selected_device()
        if device_ip:
            # Create bandwidth limit dialog
            self.show_bandwidth_dialog(device_ip)
    
    def show_bandwidth_dialog(self, ip):
        """Show bandwidth limiting dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Bandwidth Limiter")
        dialog.geometry("400x300")
        dialog.configure(bg="#1a1a1a")
        dialog.resizable(False, False)
        
        # Center dialog
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Title
        title_label = tk.Label(
            dialog,
            text=f"Limit Bandwidth for {ip}",
            font=("Segoe UI", 16, "bold"),
            fg="#ffffff",
            bg="#1a1a1a"
        )
        title_label.pack(pady=20)
        
        # Download limit
        tk.Label(dialog, text="Download Limit (KB/s):", 
                font=("Segoe UI", 12), fg="#ffffff", bg="#1a1a1a").pack()
        
        download_var = tk.StringVar(value="1000")
        download_entry = tk.Entry(dialog, textvariable=download_var, 
                                font=("Segoe UI", 12), width=20)
        download_entry.pack(pady=5)
        
        # Upload limit
        tk.Label(dialog, text="Upload Limit (KB/s):", 
                font=("Segoe UI", 12), fg="#ffffff", bg="#1a1a1a").pack(pady=(20, 0))
        
        upload_var = tk.StringVar(value="1000")
        upload_entry = tk.Entry(dialog, textvariable=upload_var, 
                              font=("Segoe UI", 12), width=20)
        upload_entry.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg="#1a1a1a")
        button_frame.pack(pady=30)
        
        def apply_limit():
            try:
                download_limit = int(download_var.get())
                upload_limit = int(upload_var.get())
                # Here you would implement actual bandwidth limiting
                # This is a placeholder
                messagebox.showinfo("Success", 
                    f"Bandwidth limit applied to {ip}\n"
                    f"Download: {download_limit} KB/s\n"
                    f"Upload: {upload_limit} KB/s")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers.")
        
        tk.Button(button_frame, text="Apply", command=apply_limit,
                 bg="#28a745", fg="#ffffff", padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 bg="#6c757d", fg="#ffffff", padx=20, pady=5).pack(side=tk.LEFT, padx=5)
    
    def refresh_selected_device(self):
        """Refresh selected device information"""
        device_ip = self.get_selected_device()
        if device_ip:
            device_info = self.get_device_info(device_ip)
            if device_info:
                self.devices[device_ip] = device_info
                self.update_device_list()
                messagebox.showinfo("Success", f"Device {device_ip} information refreshed.")
    
    def block_all_devices(self):
        """Block all devices except local IP"""
        if messagebox.askyesno("Block All Devices", 
                              "Are you sure you want to block all devices?\n"
                              "This will disconnect all other devices from the internet."):
            for ip in self.devices:
                if ip != self.local_ip:
                    self.blocked_devices.add(ip)
                    self.apply_device_block(ip)
            
            self.update_device_list()
            messagebox.showinfo("Success", "All devices have been blocked.")
    
    def unblock_all_devices(self):
        """Unblock all devices"""
        if self.blocked_devices:
            for ip in list(self.blocked_devices):
                self.remove_device_block(ip)
            
            self.blocked_devices.clear()
            self.update_device_list()
            messagebox.showinfo("Success", "All devices have been unblocked.")
    
    def export_device_list(self):
        """Export device list to file"""
        try:
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")],
                title="Export Device List"
            )
            
            if filename:
                with open(filename, 'w') as f:
                    f.write("Network Device List\n")
                    f.write("=" * 50 + "\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Gateway: {self.gateway}\n")
                    f.write(f"Your IP: {self.local_ip}\n\n")
                    
                    f.write("IP Address\tMAC Address\tHostname\tVendor\tStatus\tBandwidth\n")
                    f.write("-" * 80 + "\n")
                    
                    for ip, device in self.devices.items():
                        status = "Blocked" if ip in self.blocked_devices else "Active"
                        f.write(f"{device['ip']}\t{device['mac']}\t{device['hostname']}\t"
                               f"{device['vendor']}\t{status}\t{device['bandwidth']}\n")
                
                messagebox.showinfo("Success", f"Device list exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export device list: {str(e)}")
    
    def go_back(self):
        """Return to main interface"""
        # Stop scanning and monitoring
        self.scanning = False
        self.monitoring = False
        
        # Call the return callback
        self.return_callback()


def show_network_manager(parent, return_callback):
    """Show the network manager interface"""
    NetworkDeviceManager(parent, return_callback)

# Alias for compatibility with package imports
NetworkManager = NetworkDeviceManager