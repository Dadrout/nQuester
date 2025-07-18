#!/usr/bin/env python3
"""
Build script for nQuester game (macOS version)
Creates executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Install PyInstaller if not present"""
    print("📦 Installing PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_build():
    """Create the executable build for macOS"""
    version = "version_1"
    build_dir = f"builds/{version}"
    
    # Create build directory
    os.makedirs(build_dir, exist_ok=True)
    
    print(f"🔨 Building {version} for macOS...")
    
    # Get current directory
    current_dir = os.getcwd()
    
    # PyInstaller command for macOS
    cmd = [
        "pyinstaller",
        "--onedir",  # Use directory mode for macOS
        "--windowed",  # No console window
        "--name", "nQuester",
        "--distpath", build_dir,
        "--workpath", f"builds/temp_{version}",
        "--specpath", f"builds/temp_{version}",
        f"--add-data", f"{current_dir}/data:data",  # Include data folder
        f"--add-data", f"{current_dir}/Mentors:Mentors",  # Include mentors folder
        f"--add-data", f"{current_dir}/Base and Full Map + HD Images:Base and Full Map + HD Images",  # Include maps
        f"--add-data", f"{current_dir}/Modern_Interiors_Free_v2.2:Modern_Interiors_Free_v2.2",  # Include tilesets
        f"--add-data", f"{current_dir}/mc:mc",  # Include mc folder
        "main.py"
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully!")
        
        # Copy additional files that might be needed
        additional_files = [
            "README.md",
            "LICENSE",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "HACKATHON_SUBMISSION.md",
            "IMPROVEMENTS_README.md",
            "INSTALLATION.md"
        ]
        
        for file in additional_files:
            if os.path.exists(file):
                shutil.copy2(file, build_dir)
                print(f"📄 Copied {file}")
        
        # Create a simple launcher script for macOS
        launcher_content = f"""#!/bin/bash
echo "Starting nQuester {version}..."
cd "$(dirname "$0")"
./nQuester/nQuester
"""
        
        launcher_path = f"{build_dir}/launch.sh"
        with open(launcher_path, "w") as f:
            f.write(launcher_content)
        
        # Make launcher executable
        os.chmod(launcher_path, 0o755)
        
        print(f"🎮 Executable created in: {build_dir}/nQuester/")
        print(f"🚀 Use {build_dir}/launch.sh to run the game")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_version_info():
    """Create version info file"""
    version_info = f"""
# nQuester Version 1 Build Info (macOS)
Build Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Version: 1.0
Platform: macOS

Features:
- Fullscreen support (F11)
- Diana mentor fixed
- Shoqan specialization corrected
- All mentors working
- Complete quest system
- Multiple minigames
- Achievement system
- Save/Load system
- Sound effects and music

Controls:
- WASD/Arrows: Move
- E: Interact
- Q/Tab: Journal
- F5: Quick Save
- F9: Quick Load
- F11: Toggle Fullscreen
- ESC: Exit/Menu

Mentors Available:
- Alikhan (iOS)
- Alibeck (AI/ML)
- Bahredin (TypeScript)
- Bahaudin (Backend)
- Gaziz (Frontend)
- Shoqan (Frontend)
- Zhasulan (iOS)
- Aimurat (AI/ML)
- Bernar (BOSS)
- Diana (Frontend)
- Tamyrlan (Backend)

To run the game:
1. Open Terminal
2. Navigate to this folder
3. Run: ./launch.sh
4. Or double-click: nQuester/nQuester
"""
    
    with open("builds/version_1/VERSION_INFO.txt", "w", encoding="utf-8") as f:
        f.write(version_info)
    
    print("📝 Version info created")

def main():
    """Main build function"""
    print("🎮 nQuester Build Script (macOS)")
    print("=" * 35)
    
    # Check if PyInstaller is installed
    if not check_pyinstaller():
        print("PyInstaller not found. Installing...")
        install_pyinstaller()
    
    # Create build
    if create_build():
        create_version_info()
        print("\n🎉 Build completed successfully!")
        print("📁 Check the builds/version_1/ folder for your executable")
        print("🚀 Run: ./builds/version_1/launch.sh")
    else:
        print("\n❌ Build failed. Check the error messages above.")

if __name__ == "__main__":
    main() 