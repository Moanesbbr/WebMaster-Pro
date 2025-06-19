# NetMaster Pro

**NetMaster Pro** is an open-source, extensible suite for advanced network management and control. Designed for professionals and enthusiasts, it provides a unified, modern interface to monitor, secure, and manage your network. More modules and features are coming soon.

---

## Key Features

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

## Vision & Roadmap

NetMaster Pro aims to become the all-in-one control center for your network, with planned features such as:

- Advanced device management and automation
- Bandwidth and traffic analytics
- Security and diagnostics tools
- Integration with smart home and IoT devices
- And much more

---

## Getting Started

1. **Install Python 3.8+** and ensure `pip` is available.
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Launch the application:**
   ```bash
   python wifitoqr.py
   # or
   python main_interface.py
   ```

> **Note:** Some features (like device blocking) require administrator/root privileges.

---

## Open Source & Contributing

NetMaster Pro is open source and welcomes contributions from the community. Whether you want to add new modules, improve the UI, or help with documentation, your input is valued. Please open issues or pull requests to get involved.

---

## License

MIT License

---

NetMaster Pro — Professional tools for professional networks.
