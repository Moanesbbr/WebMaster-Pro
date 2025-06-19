import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import re
import qrcode
from PIL import Image, ImageTk
import threading
import sys
import os

class WiFiQRGenerator:
    def __init__(self, root, on_back=None):
        self.root = root
        self.on_back = on_back
        self.loader = None
        self.qr_photo = None
        
        # Clear existing widgets
        for widget in root.winfo_children():
            widget.destroy()
            
        self.root.title("NetMaster Pro - WiFi to QR")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        self.root.minsize(1000, 700)
        
        # Try to set icon
        try:
            self.root.iconbitmap(os.path.join("assets", "icon.ico"))
        except Exception:
            pass
            
        self.setup_styles()
        self.create_layout()
        self.selected_network = None
        self.all_networks = []
        
        # Initial network refresh
        self.refresh_networks_threaded()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Treeview styles
        style.configure(
            "Modern.Treeview",
            background="#2d2d2d",
            foreground="#ffffff",
            fieldbackground="#2d2d2d",
            borderwidth=0,
            font=('Segoe UI', 10),
            rowheight=30
        )
        style.configure(
            "Modern.Treeview.Heading",
            background="#404040",
            foreground="#ffffff",
            font=('Segoe UI', 11, 'bold'),
            relief="flat"
        )
        style.map("Modern.Treeview",
                 background=[('selected', '#0078d4')])
        
        # Button styles
        style.configure(
            "Modern.TButton",
            background="#0078d4",
            foreground="white",
            font=('Segoe UI', 10, 'bold'),
            padding=(15, 10),
            relief="flat",
            borderwidth=0
        )
        style.map(
            "Modern.TButton",
            background=[('active', '#106ebe'), ('pressed', '#005a9e')]
        )
        
        style.configure(
            "Search.TButton",
            background="#dc3545",
            foreground="white",
            font=('Segoe UI', 9),
            padding=(8, 6),
            relief="flat"
        )
        style.map(
            "Search.TButton",
            background=[('active', '#c82333')]
        )
    
    def create_layout(self):
        main_container = tk.Frame(self.root, bg='#1a1a1a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_header(main_container)
        
        content_frame = tk.Frame(main_container, bg='#1a1a1a')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        self.create_left_panel(content_frame)
        self.create_right_panel(content_frame)
    
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg='#1a1a1a', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        if self.on_back:
            back_btn = ttk.Button(
                header_frame,
                text="← Back to Menu",
                style="Modern.TButton",
                command=self.on_back
            )
            back_btn.pack(side=tk.LEFT, pady=15)
        
        title_label = tk.Label(
            header_frame,
            text="WiFi Networks & QR Code Generator",
            font=('Segoe UI', 28, 'bold'),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        title_label.pack(side=tk.LEFT, padx=(20, 0), pady=15)
        
        self.status_label = tk.Label(
            header_frame,
            text="Ready",
            font=('Segoe UI', 12),
            fg='#28a745',
            bg='#1a1a1a'
        )
        self.status_label.pack(side=tk.RIGHT, pady=15)
    
    def create_left_panel(self, parent):
        left_panel = tk.Frame(parent, bg='#262626', relief=tk.FLAT, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Header with title and refresh button
        header_frame = tk.Frame(left_panel, bg='#262626', height=60)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        title_frame = tk.Frame(header_frame, bg='#262626')
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(
            title_frame,
            text="📶 Available Networks",
            font=('Segoe UI', 18, 'bold'),
            fg='#ffffff',
            bg='#262626'
        ).pack(side=tk.LEFT, anchor=tk.W)
        
        refresh_btn = ttk.Button(
            header_frame,
            text="🔄 Refresh",
            style="Modern.TButton",
            command=self.refresh_networks_threaded
        )
        refresh_btn.pack(side=tk.RIGHT, pady=10)
        
        self.create_search_section(left_panel)
        self.create_networks_tree(left_panel)
    
    def create_search_section(self, parent):
        search_frame = tk.Frame(parent, bg='#262626')
        search_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Search input container
        search_container = tk.Frame(search_frame, bg='#404040', relief=tk.FLAT, bd=1)
        search_container.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            search_container,
            text="🔍",
            font=('Segoe UI', 12),
            fg='#888888',
            bg='#404040'
        ).pack(side=tk.LEFT, padx=(10, 5), pady=8)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        
        search_entry = tk.Entry(
            search_container,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            bg='#404040',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief=tk.FLAT,
            bd=0
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=8, padx=(0, 5))
        
        clear_btn = ttk.Button(
            search_container,
            text="✕",
            style="Search.TButton",
            command=self.clear_search,
            width=3
        )
        clear_btn.pack(side=tk.RIGHT, padx=(0, 5), pady=4)
        
        # Filter checkboxes
        filter_frame = tk.Frame(search_frame, bg='#262626')
        filter_frame.pack(fill=tk.X)
        
        self.show_connected_var = tk.BooleanVar(value=True)
        self.show_saved_var = tk.BooleanVar(value=True)
        
        connected_frame = tk.Frame(filter_frame, bg='#262626')
        connected_frame.pack(side=tk.LEFT, padx=(0, 30))
        
        connected_cb = tk.Checkbutton(
            connected_frame,
            text="🔗 Connected Networks",
            variable=self.show_connected_var,
            command=self.apply_filters,
            font=('Segoe UI', 10),
            fg='#28a745',
            bg='#262626',
            selectcolor='#404040',
            activebackground='#262626',
            activeforeground='#28a745',
            relief=tk.FLAT
        )
        connected_cb.pack()
        
        saved_frame = tk.Frame(filter_frame, bg='#262626')
        saved_frame.pack(side=tk.LEFT)
        
        saved_cb = tk.Checkbutton(
            saved_frame,
            text="💾 Saved Networks",
            variable=self.show_saved_var,
            command=self.apply_filters,
            font=('Segoe UI', 10),
            fg='#17a2b8',
            bg='#262626',
            selectcolor='#404040',
            activebackground='#262626',
            activeforeground='#17a2b8',
            relief=tk.FLAT
        )
        saved_cb.pack()
    
    def create_networks_tree(self, parent):
        tree_container = tk.Frame(parent, bg='#262626')
        tree_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            tree_container,
            style="Modern.Treeview",
            yscrollcommand=scrollbar.set,
            columns=('Security', 'Signal', 'Status'),
            show='tree headings',
            height=15
        )
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Configure columns
        self.tree.heading('#0', text='Network Name', anchor=tk.W)
        self.tree.heading('Security', text='Security', anchor=tk.W)
        self.tree.heading('Signal', text='Signal', anchor=tk.W)
        self.tree.heading('Status', text='Status', anchor=tk.W)
        
        self.tree.column('#0', width=250, minwidth=200)
        self.tree.column('Security', width=120, minwidth=100)
        self.tree.column('Signal', width=80, minwidth=60)
        self.tree.column('Status', width=120, minwidth=100)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_network_select)
        self.tree.bind('<Double-1>', self.on_double_click)
    
    def create_right_panel(self, parent):
        right_panel = tk.Frame(parent, bg='#262626', relief=tk.FLAT, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(15, 0))
        right_panel.pack_propagate(False)
        right_panel.configure(width=450)
        
        header_label = tk.Label(
            right_panel,
            text="📱 QR Code Generator",
            font=('Segoe UI', 18, 'bold'),
            fg='#ffffff',
            bg='#262626'
        )
        header_label.pack(pady=(20, 15))
        
        self.create_network_info_section(right_panel)
        
        # QR Code display frame - Fixed with proper sizing
        self.qr_frame = tk.Frame(right_panel, bg='#ffffff', relief=tk.SOLID, bd=2)
        self.qr_frame.pack(pady=5, padx=20)
        
        self.qr_label = tk.Label(
            self.qr_frame,
            text="Select a network\nto generate QR code",
            font=('Segoe UI', 12),
            fg='#666666',
            bg='#ffffff',
            width=32,
            height=16,
            justify=tk.CENTER
        )
        self.qr_label.pack(padx=15, pady=15)
        
        # Generate button with bottom margin
        self.generate_btn = ttk.Button(
            right_panel,
            text="🎯 Generate QR Code",
            style="Modern.TButton",
            command=self.generate_qr_code,
            state=tk.DISABLED
        )
        self.generate_btn.pack(pady=(15, 30))  # Added bottom margin
        
        self.create_instructions(right_panel)
    
    def create_network_info_section(self, parent):
        info_container = tk.Frame(parent, bg='#404040', relief=tk.FLAT)
        info_container.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.selected_label = tk.Label(
            info_container,
            text="No network selected",
            font=('Segoe UI', 12, 'bold'),
            fg='#ffffff',
            bg='#404040',
            wraplength=400,
            justify=tk.CENTER
        )
        self.selected_label.pack(pady=15)
        
        self.details_label = tk.Label(
            info_container,
            text="Select a WiFi network from the list to view details",
            font=('Segoe UI', 10),
            fg='#cccccc',
            bg='#404040',
            wraplength=400,
            justify=tk.CENTER
        )
        self.details_label.pack(pady=(0, 15))
    
    def create_instructions(self, parent):
        instructions_frame = tk.Frame(parent, bg='#1f1f1f', relief=tk.FLAT)
        instructions_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            instructions_frame,
            text="📋 How to use:",
            font=('Segoe UI', 12, 'bold'),
            fg='#ffffff',
            bg='#1f1f1f'
        ).pack(anchor=tk.W, padx=15, pady=(15, 5))
        
        instructions_text = """1. Select a WiFi network from the left panel
2. Click 'Generate QR Code' button
3. Scan the QR code with your phone's camera
4. Your device will connect automatically!"""
        
        tk.Label(
            instructions_frame,
            text=instructions_text,
            font=('Segoe UI', 10),
            fg='#cccccc',
            bg='#1f1f1f',
            justify=tk.LEFT
        ).pack(anchor=tk.W, padx=15, pady=(0, 15))
    
    def get_wifi_networks_windows(self):
        """Get WiFi networks on Windows using netsh commands"""
        try:
            networks = []
            creationflags = subprocess.CREATE_NO_WINDOW
            
            # Get currently connected network info
            current_result = subprocess.run(
                ['netsh', 'wlan', 'show', 'interfaces'],
                capture_output=True, text=True, encoding='cp1252', 
                errors='ignore', creationflags=creationflags, timeout=10
            )
            
            connected_ssid = None
            signal_strength = "Unknown"
            if current_result.returncode == 0:
                for line in current_result.stdout.split('\n'):
                    if 'SSID' in line and 'BSSID' not in line:
                        match = re.search(r'SSID\s*:\s*(.+)', line)
                        if match:
                            connected_ssid = match.group(1).strip()
                    elif 'Signal' in line:
                        signal_match = re.search(r'Signal\s*:\s*(\d+)%', line)
                        if signal_match:
                            signal_strength = f"{signal_match.group(1)}%"
            
            # Get all saved WiFi profiles
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'profiles'],
                capture_output=True, text=True, encoding='cp1252', 
                errors='ignore', creationflags=creationflags, timeout=10
            )
            
            if result.returncode != 0:
                return []
            
            # Process each profile
            for line in result.stdout.split('\n'):
                if 'All User Profile' in line:
                    match = re.search(r'All User Profile\s*:\s*(.+)', line)
                    if match:
                        ssid = match.group(1).strip()
                        
                        # Get profile details including password
                        detail_result = subprocess.run(
                            ['netsh', 'wlan', 'show', 'profile', f'name={ssid}', 'key=clear'],
                            capture_output=True, text=True, encoding='cp1252', 
                            errors='ignore', creationflags=creationflags, timeout=5
                        )
                        
                        security = "Unknown"
                        password = None
                        
                        if detail_result.returncode == 0:
                            for detail_line in detail_result.stdout.split('\n'):
                                if 'Authentication' in detail_line:
                                    auth_match = re.search(r'Authentication\s*:\s*(.+)', detail_line)
                                    if auth_match:
                                        security = auth_match.group(1).strip()
                                elif 'Key Content' in detail_line:
                                    key_match = re.search(r'Key Content\s*:\s*(.+)', detail_line)
                                    if key_match:
                                        password = key_match.group(1).strip()
                        
                        is_connected = ssid == connected_ssid
                        current_signal = signal_strength if is_connected else "N/A"
                        status = "Connected" if is_connected else "Saved"
                        
                        networks.append({
                            'ssid': ssid,
                            'security': security,
                            'signal': current_signal,
                            'status': status,
                            'password': password,
                            'is_connected': is_connected,
                            'is_saved': True
                        })
            
            return networks
            
        except subprocess.TimeoutExpired:
            messagebox.showerror("Timeout", "Network scan timed out. Please try again.")
            return []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get WiFi networks: {str(e)}")
            return []
    
    def show_loader(self):
        """Show loading dialog"""
        if hasattr(self, 'loader') and self.loader is not None:
            return
            
        self.loader = tk.Toplevel(self.root)
        self.loader.title('NetMaster Pro')
        self.loader.geometry('300x120')
        self.loader.resizable(False, False)
        self.loader.transient(self.root)
        self.loader.grab_set()
        self.loader.configure(bg='#262626')
        
        # Center on parent window
        self.loader.geometry(f"+{self.root.winfo_x() + 300}+{self.root.winfo_y() + 200}")
        
        tk.Label(
            self.loader, 
            text='🔄 Refreshing WiFi networks...', 
            font=('Segoe UI', 12),
            fg='#ffffff',
            bg='#262626'
        ).pack(pady=20)
        
        pb = ttk.Progressbar(self.loader, mode='indeterminate')
        pb.pack(fill=tk.X, padx=30, pady=10)
        pb.start(10)
    
    def hide_loader(self):
        """Hide loading dialog"""
        if hasattr(self, 'loader') and self.loader is not None:
            self.loader.destroy()
            self.loader = None
    
    def refresh_networks(self):
        """Refresh the list of WiFi networks"""
        self.status_label.config(text="Scanning...", fg='#ffc107')
        
        # Get networks (Windows only)
        networks = self.get_wifi_networks_windows()
        
        self.all_networks = networks
        self.apply_filters()
        
        count = len(networks)
        self.status_label.config(
            text=f"Found {count} network{'s' if count != 1 else ''}", 
            fg='#28a745'
        )
    
    def refresh_networks_threaded(self):
        """Refresh networks in a separate thread"""
        def refresh():
            try:
                self.show_loader()
                self.refresh_networks()
            finally:
                self.hide_loader()
        
        thread = threading.Thread(target=refresh, daemon=True)
        thread.start()
    
    def apply_filters(self):
        """Apply search and filter criteria to network list"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not hasattr(self, 'all_networks') or not self.all_networks:
            return
        
        search_term = self.search_var.get().lower() if hasattr(self, 'search_var') else ""
        show_connected = self.show_connected_var.get() if hasattr(self, 'show_connected_var') else True
        show_saved = self.show_saved_var.get() if hasattr(self, 'show_saved_var') else True
        
        # Filter networks
        filtered_networks = []
        for network in self.all_networks:
            # Search filter
            if search_term and search_term not in network['ssid'].lower():
                continue
            
            # Type filters
            if network['is_connected'] and not show_connected:
                continue
            if not network['is_connected'] and network['is_saved'] and not show_saved:
                continue
            
            filtered_networks.append(network)
        
        # Sort: connected first, then alphabetically
        filtered_networks.sort(key=lambda x: (not x['is_connected'], x['ssid'].lower()))
        
        # Add to tree
        for network in filtered_networks:
            status_icon = "🔗" if network['is_connected'] else "💾"
            display_status = f"{status_icon} {network['status']}"
            
            security_icon = "🔒" if network['security'] != "Open" else "🔓"
            display_security = f"{security_icon} {network['security']}"
            
            self.tree.insert('', tk.END,
                           text=network['ssid'],
                           values=(display_security, network['signal'], display_status))
    
    def on_search_change(self, *args):
        """Handle search input changes"""
        self.apply_filters()
    
    def clear_search(self):
        """Clear search input"""
        self.search_var.set("")
    
    def on_network_select(self, event):
        """Handle network selection"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        ssid = item['text']
        
        # Find the network data
        network_data = None
        for network in self.all_networks:
            if network['ssid'] == ssid:
                network_data = network
                break
        
        if network_data:
            self.selected_network = network_data
            
            # Update display
            status_icon = "🔗" if network_data['is_connected'] else "💾"
            self.selected_label.config(text=f"📶 {ssid}")
            
            details = f"{status_icon} {network_data['status']} • {network_data['security']}"
            if network_data['signal'] != "N/A":
                details += f" • Signal: {network_data['signal']}"
            
            self.details_label.config(text=details)
            self.generate_btn.config(state=tk.NORMAL)
    
    def on_double_click(self, event):
        """Handle double-click on network"""
        if self.selected_network:
            self.generate_qr_code()
    
    def generate_qr_code(self):
        """Generate and display QR code for selected network"""
        if not self.selected_network:
            messagebox.showwarning("No Selection", "Please select a WiFi network first.")
            return
        
        network = self.selected_network
        ssid = network['ssid']
        security = network['security']
        password = network.get('password', '')
        
        # Handle password requirements
        if ('WPA' in security.upper() or 'WEP' in security.upper()) and not password:
            response = messagebox.askyesno(
                "Password Required",
                f"Password for '{ssid}' is not available.\n\n"
                "This can happen if:\n"
                "• The password was changed recently\n"
                "• Network was saved on another device\n"
                "• System lacks permission to access password\n\n"
                "Would you like to enter the password manually?"
            )
            
            if response:
                password = simpledialog.askstring(
                    "Enter Password",
                    f"Enter password for '{ssid}':",
                    show='*'
                )
                if not password:
                    return
            else:
                return
        
        # Determine security type for QR code
        if password:
            security_type = "WPA" if "WPA" in security.upper() else ("WEP" if "WEP" in security.upper() else "nopass")
        else:
            security_type = "nopass"
        
        # Create WiFi QR code string
        wifi_config = f"WIFI:T:{security_type};S:{ssid};P:{password};H:false;;"
        
        try:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=8,  # Slightly smaller for better fit
                border=4,
            )
            qr.add_data(wifi_config)
            qr.make(fit=True)
            
            # Create QR code image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image = qr_image.resize((280, 280), Image.Resampling.LANCZOS)  # Fixed size
            
            # Convert to PhotoImage and store reference
            self.qr_photo = ImageTk.PhotoImage(qr_image)
            
            # Update label with QR code image
            self.qr_label.config(
                image=self.qr_photo, 
                text="",  # Clear text
                compound=tk.CENTER,
                width=280,  # Set explicit dimensions
                height=280
            )
            
            # Success message
            msg = f"✅ QR code generated for '{ssid}'!\n\nScan with your phone's camera to connect instantly."
            if not password:
                msg += "\n\nNote: This is an open network (no password required)."
            
            messagebox.showinfo("Success", msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code:\n{str(e)}")


def show_wifitoqr(root, on_back):
    """Initialize WiFi to QR converter"""
    WiFiQRGenerator(root, on_back)


def run():
    """Run the application standalone"""
    root = tk.Tk()
    show_wifitoqr(root, None)
    root.mainloop()


if __name__ == "__main__":
    run()