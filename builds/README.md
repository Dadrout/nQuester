# nQuester Builds

This folder contains executable builds of the nQuester game.

## Available Builds

### version_1
- **Release Date**: Latest build
- **Features**: 
  - Fullscreen support (F11)
  - Diana mentor fixed
  - Shoqan specialization corrected
  - All mentors working
  - Complete quest system
  - Multiple minigames
  - Achievement system
  - Save/Load system
  - Sound effects and music

## How to Build

### Option 1: Using Python Script
```bash
python build_exe.py
```

### Option 2: Using Batch File (Windows)
```bash
build.bat
```

### Option 3: Manual PyInstaller
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name nQuester --distpath builds/version_1 --add-data "data;data" --add-data "Mentors;Mentors" --add-data "Base and Full Map + HD Images;Base and Full Map + HD Images" --add-data "Modern_Interiors_Free_v2.2;Modern_Interiors_Free_v2.2" --add-data "mc;mc" main.py
```

## Running the Game

1. Navigate to the build folder (e.g., `builds/version_1/`)
2. Run `nQuester.exe` (Windows) or `nQuester` (Linux/Mac)
3. Or use the provided `launch.bat` file

## Controls

- **WASD/Arrows**: Move
- **E**: Interact with NPCs
- **Q/Tab**: Open/Close Journal
- **F5**: Quick Save
- **F9**: Quick Load
- **F11**: Toggle Fullscreen
- **ESC**: Exit/Menu

## Mentors Available

- **Alikhan** (iOS)
- **Alibeck** (AI/ML)
- **Bahredin** (TypeScript)
- **Bahaudin** (Backend)
- **Gaziz** (Frontend)
- **Shoqan** (Frontend)
- **Zhasulan** (iOS)
- **Aimurat** (AI/ML)
- **Bernar** (BOSS)
- **Diana** (Frontend)
- **Tamyrlan** (Backend)

## Troubleshooting

If the game doesn't start:
1. Make sure all required files are in the same folder as the executable
2. Check that your system supports the game's requirements
3. Try running from command line to see error messages
4. Make sure you have the latest version of the build

## File Structure

Each build folder contains:
- `nQuester.exe` - The main executable
- `launch.bat` - Windows launcher script
- `VERSION_INFO.txt` - Build information
- Various documentation files
- Required data folders (data, Mentors, etc.) 