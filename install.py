#!/usr/bin/env python3
"""
Installer script for IP Device Management Interface
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"Python version: {sys.version.split()[0]} ✓")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def create_launcher():
    """Create launcher script for the application"""
    print("\nCreating launcher scripts...")
    
    if platform.system() == "Windows":
        # Create batch file for Windows
        launcher_content = """@echo off
cd /d "%~dp0"
python main.py
pause
"""
        with open("launch.bat", "w") as f:
            f.write(launcher_content)
        print("✓ Created launch.bat")
        
        # Create PowerShell launcher
        ps_launcher = """# IP Device Management Interface Launcher
Set-Location $PSScriptRoot
python main.py
"""
        with open("launch.ps1", "w") as f:
            f.write(ps_launcher)
        print("✓ Created launch.ps1")
    else:
        # Create shell script for Unix-like systems
        launcher_content = """#!/bin/bash
cd "$(dirname "$0")"
python3 main.py
"""
        with open("launch.sh", "w") as f:
            f.write(launcher_content)
        os.chmod("launch.sh", 0o755)
        print("✓ Created launch.sh")

def verify_installation():
    """Verify that the installation is complete"""
    print("\nVerifying installation...")
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("✗ main.py not found")
        return False
    print("✓ main.py found")
    
    # Check if requirements are installed
    try:
        import ping3
        print("✓ ping3 module installed")
    except ImportError:
        print("✗ ping3 module not found")
        return False
    
    # Check if tkinter is available
    try:
        import tkinter
        print("✓ tkinter available")
    except ImportError:
        print("✗ tkinter not available (usually comes with Python)")
        return False
    
    return True

def main():
    """Main installation process"""
    print("=" * 60)
    print("IP Device Management Interface - Installer")
    print("=" * 60)
    
    if not check_python_version():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    create_launcher()
    
    if verify_installation():
        print("\n" + "=" * 60)
        print("Installation completed successfully!")
        print("=" * 60)
        print("\nTo run the application:")
        if platform.system() == "Windows":
            print("  - Double-click launch.bat")
            print("  - Or run: python main.py")
        else:
            print("  - Run: ./launch.sh")
            print("  - Or run: python3 main.py")
        print()
    else:
        print("\n" + "=" * 60)
        print("Installation verification failed!")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()

