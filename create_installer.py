#!/usr/bin/env python3
"""
Installer creation script for IP Device Management Interface
Creates a proper installer package for Windows, Linux, and macOS
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def check_executable():
    """Check if executable exists"""
    dist_dir = "dist"
    if platform.system() == "Windows":
        exe_name = "IPDeviceManager.exe"
    else:
        exe_name = "IPDeviceManager"
    
    exe_path = os.path.join(dist_dir, exe_name)
    if os.path.exists(exe_path):
        print(f"✓ Found executable: {exe_path}")
        return exe_path
    else:
        print(f"✗ Executable not found: {exe_path}")
        print("  Please run build_executable.py first")
        return None

def create_windows_installer(exe_path):
    """Create Windows installer using Inno Setup or NSIS"""
    print("\nCreating Windows installer...")
    
    # Check for Inno Setup
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
    ]
    
    inno_compiler = None
    for path in inno_paths:
        if os.path.exists(path):
            inno_compiler = path
            break
    
    if inno_compiler:
        print("✓ Found Inno Setup")
        # Create Inno Setup script
        create_inno_script()
        try:
            subprocess.check_call([inno_compiler, "installer.iss"])
            print("✓ Windows installer created: dist/IPDeviceManager_Setup.exe")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Error creating installer: {e}")
            return False
    else:
        print("⚠ Inno Setup not found")
        print("  Creating simple installer package...")
        return create_simple_installer(exe_path, "windows")

def create_inno_script():
    """Create Inno Setup script"""
    script = """[Setup]
AppName=IP Device Management Interface
AppVersion=1.0
AppPublisher=IP Device Manager
DefaultDirName={autopf}\\IPDeviceManager
DefaultGroupName=IP Device Manager
OutputDir=dist
OutputBaseFilename=IPDeviceManager_Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "dist\\IPDeviceManager.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Icons]
Name: "{group}\\IP Device Manager"; Filename: "{app}\\IPDeviceManager.exe"
Name: "{group}\\{cm:UninstallProgram,IP Device Management Interface}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\IP Device Manager"; Filename: "{app}\\IPDeviceManager.exe"; Tasks: desktopicon
Name: "{userappdata}\\Microsoft\\Internet Explorer\\Quick Launch\\IP Device Manager"; Filename: "{app}\\IPDeviceManager.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\\IPDeviceManager.exe"; Description: "{cm:LaunchProgram,IP Device Management Interface}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;
"""
    
    with open("installer.iss", "w") as f:
        f.write(script)
    print("✓ Created installer.iss")

def create_simple_installer(exe_path, platform_type):
    """Create a simple installer package (zip with install script)"""
    print(f"\nCreating simple installer package for {platform_type}...")
    
    installer_dir = "installer_package"
    if os.path.exists(installer_dir):
        shutil.rmtree(installer_dir)
    os.makedirs(installer_dir)
    
    # Copy executable
    shutil.copy2(exe_path, installer_dir)
    
    # Copy README
    if os.path.exists("README.md"):
        shutil.copy2("README.md", installer_dir)
    
    # Create install script
    if platform_type == "windows":
        install_script = """@echo off
echo Installing IP Device Management Interface...
echo.

set INSTALL_DIR=%ProgramFiles%\\IPDeviceManager

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

copy "IPDeviceManager.exe" "%INSTALL_DIR%\\"
copy "README.md" "%INSTALL_DIR%\\"

echo.
echo Installation complete!
echo The application has been installed to: %INSTALL_DIR%
echo.
echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\IP Device Manager.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\IPDeviceManager.exe'; $Shortcut.Save()"

echo.
echo Desktop shortcut created!
pause
"""
        script_name = "install.bat"
    else:
        install_script = """#!/bin/bash
echo "Installing IP Device Management Interface..."
echo

INSTALL_DIR="/usr/local/bin"

sudo cp IPDeviceManager "$INSTALL_DIR/"
sudo chmod +x "$INSTALL_DIR/IPDeviceManager"

if [ -f README.md ]; then
    sudo mkdir -p /usr/local/share/ipdevicemanager
    sudo cp README.md /usr/local/share/ipdevicemanager/
fi

echo
echo "Installation complete!"
echo "The application has been installed to: $INSTALL_DIR"
echo "You can run it with: IPDeviceManager"
"""
        script_name = "install.sh"
    
    script_path = os.path.join(installer_dir, script_name)
    with open(script_path, "w") as f:
        f.write(install_script)
    
    if platform_type != "windows":
        os.chmod(script_path, 0o755)
    
    # Create uninstall script
    if platform_type == "windows":
        uninstall_script = """@echo off
echo Uninstalling IP Device Management Interface...
echo.

set INSTALL_DIR=%ProgramFiles%\\IPDeviceManager

if exist "%INSTALL_DIR%" (
    rmdir /s /q "%INSTALL_DIR%"
    echo Application removed.
) else (
    echo Application not found.
)

if exist "%USERPROFILE%\\Desktop\\IP Device Manager.lnk" (
    del "%USERPROFILE%\\Desktop\\IP Device Manager.lnk"
    echo Desktop shortcut removed.
)

echo.
echo Uninstallation complete!
pause
"""
        uninstall_name = "uninstall.bat"
    else:
        uninstall_script = """#!/bin/bash
echo "Uninstalling IP Device Management Interface..."
echo

sudo rm -f /usr/local/bin/IPDeviceManager
sudo rm -rf /usr/local/share/ipdevicemanager

echo
echo "Uninstallation complete!"
"""
        uninstall_name = "uninstall.sh"
    
    uninstall_path = os.path.join(installer_dir, uninstall_name)
    with open(uninstall_path, "w") as f:
        f.write(uninstall_script)
    
    if platform_type != "windows":
        os.chmod(uninstall_path, 0o755)
    
    # Create zip archive
    zip_name = f"IPDeviceManager_Installer_{platform_type}.zip"
    shutil.make_archive(zip_name.replace(".zip", ""), "zip", installer_dir)
    
    print(f"✓ Simple installer package created: {zip_name}")
    print(f"  Extract and run {script_name} to install")
    
    return True

def create_linux_installer(exe_path):
    """Create Linux installer (AppImage or DEB package)"""
    print("\nCreating Linux installer...")
    return create_simple_installer(exe_path, "linux")

def create_macos_installer(exe_path):
    """Create macOS installer (DMG or PKG)"""
    print("\nCreating macOS installer...")
    return create_simple_installer(exe_path, "macos")

def main():
    """Main installer creation process"""
    print("=" * 60)
    print("IP Device Management Interface - Installer Creator")
    print("=" * 60)
    
    exe_path = check_executable()
    if not exe_path:
        sys.exit(1)
    
    system = platform.system()
    
    if system == "Windows":
        if not create_windows_installer(exe_path):
            print("\n⚠ Could not create full installer, simple package created instead")
    elif system == "Linux":
        create_linux_installer(exe_path)
    elif system == "Darwin":  # macOS
        create_macos_installer(exe_path)
    else:
        print(f"⚠ Unsupported platform: {system}")
        print("Creating generic installer package...")
        create_simple_installer(exe_path, "generic")
    
    print("\n" + "=" * 60)
    print("Installer creation complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

