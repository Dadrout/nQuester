# nQuester Build Guide

This guide explains how to create executable builds of the nQuester game for different platforms.

## Prerequisites

1. **Python 3.8+** installed
2. **PyInstaller** (will be installed automatically by the build scripts)
3. **All game dependencies** (install with `pip install -r requirements.txt`)

## Build Scripts

### For macOS
```bash
python3 build_exe_macos.py
```

### For Windows
```bash
python3 build_exe_windows.py
```

### For Linux
```bash
python3 build_exe.py
```

## Build Output

After a successful build, you'll find:

### macOS Build
- Location: `builds/version_1/`
- Files:
  - `nQuester.app/` - macOS application bundle
  - `nQuester/` - Executable directory
  - `launch.sh` - Launcher script
  - `VERSION_INFO.txt` - Build information
  - Documentation files

### Windows Build
- Location: `builds/version_1/`
- Files:
  - `nQuester.exe` - Windows executable
  - `launch.bat` - Launcher script
  - `VERSION_INFO.txt` - Build information
  - Documentation files

## Running the Builds

### macOS
```bash
cd builds/version_1/
./launch.sh
# OR
open nQuester.app
```

### Windows
```bash
cd builds/version_1/
launch.bat
# OR double-click nQuester.exe
```

### Linux
```bash
cd builds/version_1/
./nQuester
```

## Build Features

### Version 1 Features
- ✅ Fullscreen support (F11)
- ✅ Diana mentor fixed
- ✅ Shoqan specialization corrected
- ✅ All mentors working
- ✅ Complete quest system
- ✅ Multiple minigames
- ✅ Achievement system
- ✅ Save/Load system
- ✅ Sound effects and music

### Included Data
- All game sprites and assets
- Mentor images
- Map data
- Sound files
- Documentation

## Troubleshooting

### Build Fails
1. Make sure PyInstaller is installed: `pip install pyinstaller`
2. Check that all game files are present
3. Ensure you're in the correct directory
4. Try running the build script with verbose output

### Game Doesn't Start
1. Check that all required files are in the build directory
2. Try running from command line to see error messages
3. Make sure your system meets the requirements
4. Check file permissions (especially on macOS/Linux)

### Missing Assets
1. Verify that all data folders are included in the build
2. Check the `--add-data` parameters in the build script
3. Ensure file paths are correct for your platform

## Manual Build Commands

### macOS
```bash
pyinstaller --onedir --windowed --name nQuester --distpath builds/version_1 --add-data "data:data" --add-data "Mentors:Mentors" --add-data "Base and Full Map + HD Images:Base and Full Map + HD Images" --add-data "Modern_Interiors_Free_v2.2:Modern_Interiors_Free_v2.2" --add-data "mc:mc" main.py
```

### Windows
```bash
pyinstaller --onefile --windowed --name nQuester --distpath builds/version_1 --add-data "data;data" --add-data "Mentors;Mentors" --add-data "Base and Full Map + HD Images;Base and Full Map + HD Images" --add-data "Modern_Interiors_Free_v2.2;Modern_Interiors_Free_v2.2" --add-data "mc;mc" main.py
```

## Version Management

To create a new version:

1. Update the version number in the build script
2. Create a new build directory: `builds/version_X/`
3. Run the appropriate build script
4. Update the version info and documentation

## Distribution

### For Distribution
1. Test the build thoroughly
2. Create a zip file of the build directory
3. Include the VERSION_INFO.txt file
4. Test on a clean system

### File Structure for Distribution
```
nQuester_v1.0_macOS.zip
├── nQuester.app/
├── launch.sh
├── VERSION_INFO.txt
├── README.md
└── LICENSE
```

## Performance Notes

- macOS builds use `--onedir` for better compatibility
- Windows builds use `--onefile` for easier distribution
- Linux builds can use either depending on preference
- All builds include all necessary assets and dependencies

## Security Notes

- The builds are self-contained and don't require internet access
- No external dependencies are downloaded at runtime
- All assets are bundled within the executable
- The game doesn't require elevated permissions

## Support

If you encounter issues:
1. Check the build logs for error messages
2. Verify all dependencies are installed
3. Test on a clean system
4. Check platform-specific requirements 