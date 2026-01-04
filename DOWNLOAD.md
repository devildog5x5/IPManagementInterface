# IP Management Interface - Downloads

Download ready-to-use executables and installers for the IP Management Dashboard application.

> **⚠️ Note:** Download links will be available after creating a GitHub Release. See [Creating a Release](#-creating-a-release) section below.

## 🎯 Recommended: MSI Installer

**[Download MSI Installer](https://github.com/devildog5x5/IPManagementInterface/releases/latest/download/IPManagementInterface-Setup.msi)**

**Size:** ~241 MB | **Version:** Latest

The MSI installer is the **recommended option** for Windows installation:

- ✅ **Professional Installation** - Standard Windows MSI installer
- ✅ **Easy Setup** - Guided installation wizard
- ✅ **Clean Uninstall** - Proper removal through Windows Settings
- ✅ **Desktop Shortcuts** - Optional desktop and Start Menu shortcuts
- ✅ **System Integration** - Properly registered Windows application

**Requirements:**
- Windows 10 or later (Windows 10, 11)
- .NET 8.0 Runtime (included in self-contained builds or install separately)

**Installation Notes:**
- Standard Windows installer experience
- Follow the installation wizard
- Optional: Create desktop shortcuts

---

## 💻 Standalone Executable

### Self-Contained Build (Recommended)

**[Download Self-Contained Executable](https://github.com/devildog5x5/IPManagementInterface/releases/latest/download/IPManagementInterface.exe)**

**Size:** ~173 MB | **Version:** Latest

A self-contained executable that includes everything needed to run:

- ✅ **No Installation Required** - Just download and run
- ✅ **Includes .NET Runtime** - No need to install .NET separately
- ✅ **Works on Older Windows** - Runs on Windows 7 SP1 and later
- ✅ **Portable** - Can run from any location
- ✅ **Single File** - Everything bundled in one executable

**Requirements:**
- Windows 7 SP1 or later (Windows 7, 8.1, 10, 11)
- No additional software needed - everything is included

**Usage:**
- Simply double-click `IPManagementInterface.exe` to launch
- No installation, no admin rights required
- Perfect for quick deployment or testing

---

## 📦 Creating a Release

To make the download links work, you need to create a GitHub Release and upload the build artifacts:

### Option 1: Using GitHub Website
1. Go to https://github.com/devildog5x5/IPManagementInterface/releases/new
2. Create a new release:
   - **Tag:** `v1.0.0` (or your version)
   - **Title:** `Release v1.0.0` (or your title)
   - **Description:** Add release notes
3. Upload the following files:
   - `IPManagementInterface\bin\Release\net8.0-windows\win-x64\publish\IPManagementInterface.exe`
   - `InstallerOutput\IPManagementInterface-Setup.msi`
4. Click "Publish release"

### Option 2: Using GitHub CLI (if installed)
```powershell
# Create release and upload files
gh release create v1.0.0 `
  "IPManagementInterface\bin\Release\net8.0-windows\win-x64\publish\IPManagementInterface.exe" `
  "InstallerOutput\IPManagementInterface-Setup.msi" `
  --title "Release v1.0.0" `
  --notes "Initial release with 9 themes, keyboard shortcuts, and enhanced features"
```

### Option 3: Build from Source
If you prefer to build from source, see the [Building from Source](#-building-from-source) section below.

---

## ✨ What's New

### Version Features:
- **9 Beautiful Themes**: Choose from Light, Dark, USMC, Olive Drab, Ocean, Sunset, Midnight, Forest, and Cyber themes
- **Keyboard Shortcuts**: Fast access with Ctrl+N (Add), Ctrl+F (Search), F5 (Refresh), Ctrl+A (Select All), and more
- **Bulk Operations**: Select multiple devices with Ctrl+Click, use Select All/Invert/Deselect buttons
- **Enhanced UI**: Improved tooltips, better visual feedback, scrollable settings
- **Device Management**: Full device discovery, monitoring, alerting, and management features

---

## 📋 Build Options

| Option | Type | Size | .NET Runtime | Best For |
|--------|------|------|--------------|----------|
| **MSI Installer** | Installer | ~241 MB | Required* | Production deployment |
| **Self-Contained Executable** | Standalone | ~173 MB | Included | Older Windows, portable use |

\* Can use self-contained build which includes runtime

---

## 🚀 Quick Start Guide

### Option 1: Standard Installation
**→ Download the [MSI Installer](#-recommended-msi-installer)**
- Professional Windows installation
- System integration
- Easy uninstallation

### Option 2: Portable Use
**→ Download the [Self-Contained Executable](#self-contained-build-recommended)**
- No installation needed
- Works on Windows 7 SP1+
- Perfect for USB drives or quick deployment

---

## 📦 What's Included

All versions include:
- ✅ Dashboard interface with tabbed device organization
- ✅ Device management (add, remove, edit devices)
- ✅ Multi-protocol support (HTTP/HTTPS, custom ports)
- ✅ Smart device discovery with network scanning
- ✅ Real-time status monitoring
- ✅ 9 beautiful themes (Light, Dark, USMC, Olive Drab, Ocean, Sunset, Midnight, Forest, Cyber)
- ✅ Keyboard shortcuts for fast workflow
- ✅ Bulk operations (select, refresh, delete multiple devices)
- ✅ Device statistics and reporting
- ✅ Persistent device storage
- ✅ Modern, colorful UI

---

## 🎨 Available Platforms

- **Windows Desktop** - Full-featured WPF application (this download page)
- **iOS** - .NET MAUI application (see [README_iOS_SETUP.md](README_iOS_SETUP.md))
- **Android** - .NET MAUI application (see [README_ANDROID.md](README_ANDROID.md))

---

## 🔗 Additional Resources

- **Repository:** [https://github.com/devildog5x5/IPManagementInterface](https://github.com/devildog5x5/IPManagementInterface)
- **Releases:** [https://github.com/devildog5x5/IPManagementInterface/releases](https://github.com/devildog5x5/IPManagementInterface/releases)
- **Documentation:** See [README.md](README.md) for detailed usage instructions
- **iOS Setup:** See [README_iOS_SETUP.md](README_iOS_SETUP.md) for iOS build instructions
- **Android Setup:** See [README_ANDROID.md](README_ANDROID.md) for Android build instructions
- **Deployment Guide:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for deployment information
- **Issues:** Report bugs or request features on GitHub Issues

---

## 📝 Installation Instructions

### MSI Installer
1. Download `IPManagementInterface-Setup.msi` from the [Releases page](https://github.com/devildog5x5/IPManagementInterface/releases)
2. Double-click to run the installer (admin rights may be required)
3. Follow the installation wizard
4. Launch from desktop shortcut or Start Menu

### Self-Contained Executable
1. Download `IPManagementInterface.exe` from the [Releases page](https://github.com/devildog5x5/IPManagementInterface/releases)
2. Double-click to run
3. No installation required!

---

## ❓ Troubleshooting

**Q: Which version should I use?**  
A: For most users, the MSI Installer is recommended. For portable use or older Windows versions, use the Self-Contained Executable.

**Q: Do I need to install .NET?**  
A: The Self-Contained Executable includes .NET and doesn't require separate installation. The MSI installer may require .NET 8.0 Runtime.

**Q: Will it work on Windows 7?**  
A: Yes! The Self-Contained Executable works on Windows 7 SP1 and later.

**Q: Can I run it from a USB drive?**  
A: Yes! Both the Self-Contained Executable and MSI installer support portable use.

**Q: The download links give 404 errors**  
A: You need to create a GitHub Release first. See the [Creating a Release](#-creating-a-release) section above.

---

## 🔧 Building from Source

If you prefer to build from source, see the [README.md](README.md) for detailed build instructions.

**Quick build commands:**
```powershell
# Self-contained build (recommended)
.\PublishForDistribution.ps1 -Configuration Release

# Standard build
dotnet build IPManagementInterface.sln --configuration Release

# MSI Installer
.\BuildWiXInstaller.ps1
```

After building, the files will be in:
- Executable: `IPManagementInterface\bin\Release\net8.0-windows\win-x64\publish\IPManagementInterface.exe`
- Installer: `InstallerOutput\IPManagementInterface-Setup.msi`

---

**Last Updated:** Latest Release
