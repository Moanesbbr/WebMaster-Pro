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

from netmaster_pro.ui.main_interface import run

if __name__ == "__main__":
    run() 