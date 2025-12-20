#!/usr/bin/env python3
"""
Build script to create standalone executable from the IP Device Management Interface
Uses PyInstaller to package the application
"""

import os
import sys
import subprocess
import platform
import shutil

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller found")
        return True
    except ImportError:
        print("✗ PyInstaller not found")
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing PyInstaller: {e}")
        return False

def build_executable():
    """Build the executable using PyInstaller"""
    print("\nBuilding executable...")
    print("=" * 60)
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=IPDeviceManager",
        "--onefile",
        "--icon=NONE",  # Can add icon file later
        "--hidden-import=ping3",
        "--hidden-import=tkinter",
        "--hidden-import=ipaddress",
        "--clean",
        "main.py"
    ]
    
    # Adjust for platform
    if platform.system() == "Windows":
        cmd.insert(4, "--noconsole")  # Windows: no console window
    elif platform.system() == "Darwin":  # macOS
        cmd.insert(4, "--windowed")  # macOS: no console window
        cmd.append("--osx-bundle-identifier=com.ipdevicemanager.app")
    else:  # Linux
        cmd.insert(4, "--noconsole")  # Linux: no console window
    
    try:
        subprocess.check_call(cmd)
        print("\n✓ Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error building executable: {e}")
        return False

def create_distribution():
    """Create distribution package"""
    print("\nCreating distribution package...")
    
    dist_dir = "dist"
    build_dir = "build"
    spec_file = "IPDeviceManager.spec"
    
    if os.path.exists(dist_dir):
        print(f"Distribution files are in: {os.path.abspath(dist_dir)}")
        
        if platform.system() == "Windows":
            exe_name = "IPDeviceManager.exe"
        else:
            exe_name = "IPDeviceManager"
        
        exe_path = os.path.join(dist_dir, exe_name)
        if os.path.exists(exe_path):
            print(f"✓ Executable created: {exe_path}")
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"  File size: {file_size:.2f} MB")
        else:
            print(f"✗ Executable not found at: {exe_path}")
    
    return True

def main():
    """Main build process"""
    print("=" * 60)
    print("IP Device Management Interface - Executable Builder")
    print("=" * 60)
    
    if not check_pyinstaller():
        if not install_pyinstaller():
            sys.exit(1)
    
    if not build_executable():
        sys.exit(1)
    
    create_distribution()
    
    print("\n" + "=" * 60)
    print("Build complete!")
    print("=" * 60)
    print("\nThe executable can be found in the 'dist' directory")
    print("You can distribute this executable without requiring Python to be installed.")
    print()

if __name__ == "__main__":
    main()

