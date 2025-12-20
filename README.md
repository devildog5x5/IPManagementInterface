# IP Device Management Interface

A comprehensive desktop application for managing and monitoring IP devices on your network. This tool provides an intuitive GUI for tracking network devices, performing network scans, port scanning, and monitoring device status.

## Features

### Core Functionality
- **Device Management**: Add, edit, and delete IP devices with detailed information
- **Device Status Monitoring**: Ping devices to check online/offline status
- **Auto-refresh**: Automatically ping all devices at configurable intervals
- **Search & Filter**: Quickly find devices by name, IP, or other attributes
- **Device Details**: View comprehensive information about each device

### Network Tools
- **Network Scanner**: Scan network ranges to discover active hosts
- **Port Scanner**: Scan individual devices for open ports
- **Network Information**: View local network configuration and interfaces
- **Bulk Operations**: Ping all devices at once

### Data Management
- **Persistent Storage**: All devices saved to JSON file
- **Import/Export**: Import devices from or export to JSON files
- **Context Menu**: Right-click for quick actions on devices

## Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- ping3 library

## Installation

### Quick Install

1. Clone or download this repository
2. Run the installer:
   ```bash
   python install.py
   ```

### Git Setup

To initialize the Git repository and make the initial commit:

**Windows (PowerShell):**
```powershell
.\setup_git.ps1
```

**Linux/Mac:**
```bash
chmod +x setup_git.sh
./setup_git.sh
```

**Manual Git Setup:**
```bash
git init
git add .
git commit -m "Initial commit: IP Device Management Interface"
```

### Manual Install

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

### Windows

- Double-click `launch.bat` or run `python main.py` from command prompt

### Linux/Mac

- Run `./launch.sh` or `python3 main.py` from terminal

## Usage

### Adding a Device

1. Click the "➕ Add Device" button or use File menu
2. Fill in device information:
   - **Name**: Device identifier
   - **IP Address**: IPv4 address (required)
   - **MAC Address**: Optional MAC address
   - **Device Type**: Select from predefined types
   - **Location**: Physical location
   - **Notes**: Additional information

### Managing Devices

- **Edit**: Select a device and click "✏️ Edit" or double-click
- **Delete**: Select a device and click "🗑️ Delete"
- **Ping**: Select a device and click "📡 Ping" to check status
- **Search**: Use the search box to filter devices

### Network Scanning

1. Go to **Tools → Network Scanner**
2. Enter network range (e.g., `192.168.1.0/24`)
3. Click "Scan" to discover active hosts
4. Double-click results to add to device list

### Port Scanning

1. Select a device and right-click → "Port Scan"
2. Or go to **Tools → Port Scanner**
3. Enter target IP and port range
4. Click "Scan" to check for open ports

### Network Information

- Go to **Tools → Network Info** to view:
  - Hostname
  - Local IP address
  - Network interface configuration

## File Structure

```
IPManagementInterface/
├── main.py              # Main application
├── requirements.txt     # Python dependencies
├── install.py           # Installation script
├── launch.bat           # Windows launcher (created by installer)
├── launch.sh            # Unix launcher (created by installer)
├── launch.ps1           # PowerShell launcher (created by installer)
├── devices.json         # Device database (created at runtime)
├── README.md            # This file
└── .gitignore          # Git ignore rules
```

## Data Storage

Device information is stored in `devices.json` in the application directory. The file format is:

```json
[
  {
    "name": "Router",
    "ip": "192.168.1.1",
    "mac": "00:11:22:33:44:55",
    "type": "Router",
    "location": "Office",
    "notes": "Main router",
    "status": "Online",
    "last_seen": "2024-01-15 10:30:00"
  }
]
```

## Troubleshooting

### Ping Not Working
- Ensure you have network connectivity
- Some devices may block ICMP ping requests
- Check firewall settings

### Port Scan Slow
- Port scanning can be slow for large ranges
- Use smaller port ranges for faster results
- Some ports may be filtered by firewalls

### Import/Export Issues
- Ensure JSON files are valid
- Check file permissions
- Verify JSON structure matches expected format

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available for use and modification.

## Version

Current Version: 1.0

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

