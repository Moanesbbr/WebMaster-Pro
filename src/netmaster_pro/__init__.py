"""
NetMaster Pro - Professional Network Management Suite

A comprehensive network management and control application providing
advanced device monitoring, WiFi QR code generation, and network security features.
"""

__version__ = "1.0.0"
__author__ = "NetMaster Pro Team"
__description__ = "Professional Network Management Suite"

from .core.network_manager import NetworkManager
from .core.wifi_qr_generator import WiFiQRGenerator
from .ui.main_interface import MainInterface
from .ui.splash_screen import SplashScreen

__all__ = [
    "NetworkManager",
    "WiFiQRGenerator", 
    "MainInterface",
    "SplashScreen",
    "__version__",
    "__author__",
    "__description__"
] 