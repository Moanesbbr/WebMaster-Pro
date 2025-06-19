# NetMaster Pro

**NetMaster Pro** is an open-source, extensible suite for advanced network management and control. Designed for professionals and enthusiasts, it provides a unified, modern interface to monitor, secure, and manage your network. More modules and features are coming soon.

---

## 🚀 Key Features

### 🌐 Network Device Manager

- **Network Scanning:** Discover all devices on your local network, including IP, MAC, hostname, vendor, and status.
- **Device Monitoring:** View real-time (simulated) bandwidth usage for each device.
- **Device Blocking/Unblocking:** Instantly block or unblock any device (except your own) using firewall rules (Windows) or iptables (Linux, requires admin privileges).
- **Bandwidth Limiting:** UI for setting per-device download/upload limits (placeholder in this version).
- **Bulk Actions:** Block or unblock all devices except your own with a single click.
- **Export Device List:** Export the full device list to text or CSV for auditing or reporting.
- **Context Menu:** Right-click any device for quick actions (monitor, block, unblock, limit bandwidth, refresh info).
- **Modern UI:** Professional, dark-themed interface with real-time updates.

### 📶 WiFi to QR

- **QR Code Generation:** Instantly generate QR codes for your WiFi networks, including passwords.
- **Easy Sharing:** Scan the QR code with your phone to connect instantly—no typing required.
- **Cross-Platform:** Works on Windows, Linux, and macOS (best experience on Windows).

---

## 🏗️ Project Structure

```
netmaster-pro/
├── src/netmaster_pro/          # Main package source code
│   ├── core/                   # Core business logic
│   │   ├── network_manager.py  # Network device management
│   │   └── wifi_qr_generator.py # WiFi QR code generation
│   ├── ui/                     # User interface components
│   │   ├── main_interface.py   # Main application window
│   │   └── splash_screen.py    # Splash screen
│   ├── utils/                  # Utility functions
│   └── assets/                 # Application assets (icons, images)
├── tests/                      # Test suite
├── .github/workflows/          # CI/CD configuration
├── pyproject.toml             # Modern Python packaging
├── setup.py                   # Legacy setup (for compatibility)
└── requirements.txt           # Dependencies
```

---

## 🛠️ Installation

### Option 1: Install from Source (Recommended)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/moanesbbr/netmaster-pro.git
   cd netmaster-pro
   ```

2. **Install in development mode:**

   ```bash
   pip install -e .
   ```

3. **Run the application:**
   ```bash
   netmaster-pro
   ```

### Option 2: Direct Run (Development)

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run from source:**
   ```bash
   cd src
   python -m netmaster_pro
   ```

---

## 🧪 Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Development Setup

1. **Clone and setup:**

   ```bash
   git clone https://github.com/moanesbbr/netmaster-pro.git
   cd netmaster-pro
   pip install -e ".[dev]"
   ```

2. **Run tests:**

   ```bash
   pytest
   ```

3. **Lint code:**

   ```bash
   flake8 src/
   ```

4. **Format code:**
   ```bash
   black src/
   ```

### Project Architecture

NetMaster Pro follows modern Python packaging standards:

- **`src/` layout:** Source code is organized in a `src/` directory for better packaging
- **Modular design:** Core functionality is separated from UI components
- **Type hints:** Code includes type annotations for better maintainability
- **Modern packaging:** Uses `pyproject.toml` for configuration
- **CI/CD:** Automated testing and linting via GitHub Actions

---

## 🔮 Vision & Roadmap

NetMaster Pro aims to become the all-in-one control center for your network, with planned features such as:

- Advanced device management and automation
- Bandwidth and traffic analytics
- Security and diagnostics tools
- Integration with smart home and IoT devices
- And much more

---

## 🤝 Contributing

NetMaster Pro is open source and welcomes contributions from the community. Whether you want to add new modules, improve the UI, or help with documentation, your input is valued.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Commit your changes:** `git commit -m 'Add amazing feature'`
4. **Push to the branch:** `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Use type hints for function parameters and return values

---

## 📋 Requirements

- **Python:** 3.8 or higher
- **Dependencies:**
  - `pillow` - Image processing
  - `qrcode` - QR code generation
  - `psutil` - System and process utilities

> **Note:** Some features (like device blocking) require administrator/root privileges.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Moanes BBR** - [GitHub](https://github.com/moanesbbr)

---

NetMaster Pro — Professional tools for professional networks. 🚀
