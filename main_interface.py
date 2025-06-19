import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from network_manager import show_network_manager
import os
import sys

class MainInterface:
    def __init__(self, root):
        self.root = root
        self.setup_main_window()
        self.create_interface()
        
    def setup_main_window(self):
        """Configure the main window"""
        self.root.title("NetMaster Pro")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.85)

        self.root.geometry(f"{window_width}x{window_height}")
        self.root.resizable(True, True)  # Allow resizing if desired
        self.root.configure(bg="#1a1a1a")
        
        # Center window on screen
        self.center_window()
        
        # Set icon
        try:
            icon_path = os.path.join("assets", "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_interface(self):
        """Create the main interface"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Header section
        self.create_header(main_frame)
        
        # Tools section
        self.create_tools_section(main_frame)
        
        # Footer section
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Create header with logo and title"""
        header_frame = tk.Frame(parent, bg="#1a1a1a")
        header_frame.pack(fill=tk.X, pady=(0, 40))
        
        # Logo
        try:
            logo_path = os.path.join("assets", "icon.ico")
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                # Convert ICO to RGBA if needed
                if logo_img.mode != 'RGBA':
                    logo_img = logo_img.convert('RGBA')
                logo_img = logo_img.resize((80, 80), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                
                logo_label = tk.Label(
                    header_frame,
                    image=self.logo_photo,
                    bg="#1a1a1a"
                )
                logo_label.pack(pady=(0, 15))
        except Exception as e:
            # Fallback to text logo
            tk.Label(
                header_frame,
                text="🌐",
                font=("Segoe UI", 48),
                fg="#0078d4",
                bg="#1a1a1a"
            ).pack(pady=(0, 15))
        
        # App title
        title_label = tk.Label(
            header_frame,
            text="NetMaster Pro",
            font=("Segoe UI", 32, "bold"),
            fg="#ffffff",
            bg="#1a1a1a"
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Network Tools & Utilities",
            font=("Segoe UI", 14),
            fg="#888888",
            bg="#1a1a1a"
        )
        subtitle_label.pack(pady=(5, 0))
    
    def create_tools_section(self, parent):
        """Create tools section with available modules"""
        tools_frame = tk.Frame(parent, bg="#1a1a1a")
        tools_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Section title
        section_title = tk.Label(
            tools_frame,
            text="Available Tools",
            font=("Segoe UI", 18, "bold"),
            fg="#ffffff",
            bg="#1a1a1a"
        )
        section_title.pack(pady=(0, 30))
        
        # Tools grid
        tools_container = tk.Frame(tools_frame, bg="#1a1a1a")
        tools_container.pack(expand=True)
        
        # WiFi to QR tool
        self.create_tool_card(
            tools_container,
            "📶 WiFi to QR",
            "Generate QR codes for WiFi networks\nScan to connect instantly",
            "wifitoqr.png",
            self.launch_wifi_to_qr,
            row=0, col=0
        )
        self.create_tool_card(
            tools_container,
            "🌐 Device Manager",
            "Scan, monitor and control devices\non your local network",
            "devices.png",  # use a valid icon file or None
            self.launch_network_manager,
            row=0, col=1
        )
        # Placeholder for future tools
        self.create_tool_card(
            tools_container,
            "🔧 More Tools",
            "Additional network utilities\nComing soon...",
            None,
            lambda: messagebox.showinfo("Coming Soon", "More tools will be added in future updates!"),
            row=0, col=2,
            disabled=True
        )
    
    def create_tool_card(self, parent, title, description, icon_file, command, row, col, disabled=False):
        """Create a tool card widget"""
        # Card frame
        card_frame = tk.Frame(
            parent,
            bg="#262626" if not disabled else "#1f1f1f",
            relief=tk.FLAT,
            bd=2
        )
        card_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Configure grid weights
        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)
        
        # Make card clickable if not disabled
        if not disabled:
            card_frame.bind("<Button-1>", lambda e: command())
            card_frame.bind("<Enter>", lambda e: self.on_card_enter(card_frame))
            card_frame.bind("<Leave>", lambda e: self.on_card_leave(card_frame))
            card_frame.configure(cursor="hand2")
        
        # Content frame
        content_frame = tk.Frame(card_frame, bg=card_frame["bg"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Icon
        try:
            if icon_file and not disabled:
                icon_path = os.path.join("assets", icon_file)
                if os.path.exists(icon_path):
                    icon_img = Image.open(icon_path).resize((64, 64), Image.Resampling.LANCZOS)
                    icon_photo = ImageTk.PhotoImage(icon_img)
                    
                    icon_label = tk.Label(
                        content_frame,
                        image=icon_photo,
                        bg=content_frame["bg"]
                    )
                    icon_label.image = icon_photo  # Keep reference
                    icon_label.pack(pady=(0, 15))
                    
                    if not disabled:
                        icon_label.bind("<Button-1>", lambda e: command())
                        icon_label.configure(cursor="hand2")
                else:
                    raise FileNotFoundError
            else:
                raise FileNotFoundError
        except:
            # Fallback to emoji icon
            emoji = "🔧" if disabled else "📶"
            icon_label = tk.Label(
                content_frame,
                text=emoji,
                font=("Segoe UI", 32),
                fg="#666666" if disabled else "#0078d4",
                bg=content_frame["bg"]
            )
            icon_label.pack(pady=(0, 15))
            
            if not disabled:
                icon_label.bind("<Button-1>", lambda e: command())
                icon_label.configure(cursor="hand2")
        
        # Title
        title_label = tk.Label(
            content_frame,
            text=title,
            font=("Segoe UI", 16, "bold"),
            fg="#cccccc" if disabled else "#ffffff",
            bg=content_frame["bg"]
        )
        title_label.pack()
        
        if not disabled:
            title_label.bind("<Button-1>", lambda e: command())
            title_label.configure(cursor="hand2")
        
        # Description
        desc_label = tk.Label(
            content_frame,
            text=description,
            font=("Segoe UI", 11),
            fg="#666666" if disabled else "#888888",
            bg=content_frame["bg"],
            wraplength=200,
            justify=tk.CENTER
        )
        desc_label.pack(pady=(10, 0))
        
        if not disabled:
            desc_label.bind("<Button-1>", lambda e: command())
            desc_label.configure(cursor="hand2")
        
        # Bind hover events to all child widgets
        if not disabled:
            for widget in content_frame.winfo_children():
                widget.bind("<Enter>", lambda e: self.on_card_enter(card_frame))
                widget.bind("<Leave>", lambda e: self.on_card_leave(card_frame))
        
        return card_frame
    
    def on_card_enter(self, card_frame):
        """Handle card hover enter"""
        card_frame.configure(bg="#2d2d2d")
        for widget in self.get_all_children(card_frame):
            if isinstance(widget, tk.Frame):
                widget.configure(bg="#2d2d2d")
    
    def on_card_leave(self, card_frame):
        """Handle card hover leave"""
        card_frame.configure(bg="#262626")
        for widget in self.get_all_children(card_frame):
            if isinstance(widget, tk.Frame):
                widget.configure(bg="#262626")
    
    def get_all_children(self, widget):
        """Recursively get all child widgets"""
        children = []
        for child in widget.winfo_children():
            children.append(child)
            children.extend(self.get_all_children(child))
        return children
    
    def create_footer(self, parent):
        """Create footer with version and info"""
        footer_frame = tk.Frame(parent, bg="#1a1a1a")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(30, 0))
        
        # Version info
        version_label = tk.Label(
            footer_frame,
            text="Version 1.0.0",
            font=("Segoe UI", 10),
            fg="#666666",
            bg="#1a1a1a"
        )
        version_label.pack(side=tk.LEFT)
        
        # Exit button
        exit_btn = tk.Button(
            footer_frame,
            text="Exit",
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg="#dc3545",
            activebackground="#c82333",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=20,
            pady=5,
            command=self.exit_application
        )
        exit_btn.pack(side=tk.RIGHT)
    
    def launch_wifi_to_qr(self):
        """Launch WiFi to QR module"""
        try:
            import wifitoqr
            wifitoqr.show_wifitoqr(self.root, self.show_main_interface)
        except ImportError as e:
            messagebox.showerror(
                "Module Error",
                f"Failed to load WiFi to QR module:\n{str(e)}\n\nPlease ensure wifitoqr.py is in the same directory."
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to launch WiFi to QR tool:\n{str(e)}"
            )
            
    def launch_network_manager(self):
        """Launch the Network Device Manager module"""
        try:
            import network_manager
            network_manager.show_network_manager(self.root, self.show_main_interface)
        except ImportError as e:
            messagebox.showerror(
                "Module Error",
                f"Failed to load Network Device Manager module:\n{str(e)}\n\nPlease ensure network_manager.py is in the same directory."
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to launch Network Device Manager:\n{str(e)}"
            )

    
    def show_main_interface(self):
        """Return to main interface"""
        self.create_interface()
    
    def exit_application(self):
        """Exit the application with confirmation"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit NetMaster Pro?"):
            self.root.quit()
            self.root.destroy()
            sys.exit()


def show_main_interface(root):
    """Show the main interface (for compatibility)"""
    MainInterface(root)


def run():
    """Run the main application"""
    root = tk.Tk()
    MainInterface(root)
    root.mainloop()


if __name__ == "__main__":
    run()