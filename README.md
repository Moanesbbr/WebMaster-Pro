# NetMaster Pro

A modern, modular suite of network tools and utilities with a beautiful interface. **NetMaster Pro is designed to eventually control and manage everything in your network—but in this first release, only the WiFi to QR tool is available.**

## Features (Current Version)

- Sleek, user-friendly interface
- Modular design: launch different network tools from a single app
- **WiFi to QR**: Generate QR codes for your WiFi networks (scan to connect instantly)
- More tools coming soon!

## Vision & Roadmap

NetMaster Pro aims to become your all-in-one network control center, with planned features such as:

- Network device management
- Bandwidth monitoring
- Security and diagnostics tools
- And much more!

For now, enjoy the WiFi to QR tool and stay tuned for future updates.

## Requirements

- Python 3.8+
- pip (Python package manager)
- The following Python packages:
  - tkinter (usually included with Python)
  - pillow
  - qrcode

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/netmasterpro.git
   cd netmasterpro
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run from source

```bash
python wifitoqr.py
```

or

```bash
python main_interface.py
```

### Build Windows EXE

To create a standalone Windows executable with a custom icon:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/icon.ico --name=netmasterpro wifitoqr.py
```

The EXE will be in the `dist/` folder.

## Notes

- The WiFi to QR tool can retrieve WiFi passwords for saved networks (best on Windows).
- On Linux/macOS, password retrieval may require extra permissions or manual entry.
- The app icon is set via `assets/icon.ico`.
- More network tools will be added in future updates!

## License

MIT License

---

Made with ❤️ for easy networking!
