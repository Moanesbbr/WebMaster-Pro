import tkinter as tk
from PIL import Image, ImageTk
import os
from . import main_interface


class SplashScreen:
    def __init__(self, on_close=None):
        self.root = tk.Tk()
        self.on_close = on_close
        self.logo = None
        
        self.setup_window()
        self.create_interface()
        self.load_assets()
        self.root.after(2000, self.close)
        
    def setup_window(self):
        self.root.overrideredirect(True)
        self.root.configure(bg="#1a1a1a")
        self.root.attributes('-topmost', True)
        
        width, height = 400, 250
        self.root.geometry(f"{width}x{height}")
        self.center_window(width, height)
        
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass
    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_interface(self):
        main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        self.logo_label = tk.Label(
            main_frame,
            bg="#1a1a1a",
            fg="#0078d4"
        )
        self.logo_label.pack(pady=(10, 0))
        
        tk.Label(
            main_frame,
            text="NetMaster Pro",
            font=("Segoe UI", 24, "bold"),
            fg="#ffffff",
            bg="#1a1a1a"
        ).pack(pady=(15, 5))
        
        tk.Label(
            main_frame,
            text="Network Tools & Utilities",
            font=("Segoe UI", 10),
            fg="#888888",
            bg="#1a1a1a"
        ).pack(pady=(0, 20))
        
        tk.Label(
            main_frame,
            text="Version 1.0.0",
            font=("Segoe UI", 8),
            fg="#444444",
            bg="#1a1a1a"
        ).pack(side=tk.BOTTOM)
    
    def load_assets(self):
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.ico")
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                if logo_img.mode != 'RGBA':
                    logo_img = logo_img.convert('RGBA')
                logo_img = logo_img.resize((64, 64), Image.Resampling.LANCZOS)
                self.logo = ImageTk.PhotoImage(logo_img)
                self.logo_label.configure(image=self.logo)
            else:
                self.logo_label.configure(text="🌐", font=("Segoe UI", 40))
        except Exception:
            self.logo_label.configure(text="🌐", font=("Segoe UI", 40))
    
    def close(self):
        try:
            self.root.destroy()
        except Exception:
            pass
        
        if self.on_close:
            self.on_close()
    
    def show(self):
        self.root.mainloop()


if __name__ == "__main__":
    def launch_main():
        root = tk.Tk()
        main_interface.MainInterface(root)
        root.mainloop()
    
    splash = SplashScreen(on_close=launch_main)
    splash.show()