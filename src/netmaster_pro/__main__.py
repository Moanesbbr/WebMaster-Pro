#!/usr/bin/env python3
"""
Main entry point for NetMaster Pro.

This module provides the main entry point for running NetMaster Pro
as a module: python -m netmaster_pro
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from netmaster_pro.ui.splash_screen import SplashScreen
from netmaster_pro.ui.main_interface import MainInterface
import tkinter as tk

def launch_main():
    """Launch the main interface after splash screen closes"""
    root = tk.Tk()
    MainInterface(root)
    root.mainloop()

def main():
    """Main function for console script entry point"""
    # Show splash screen first, then launch main interface
    splash = SplashScreen(on_close=launch_main)
    splash.show()

if __name__ == "__main__":
    main() 