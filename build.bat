@echo off
echo 🎮 nQuester Build Script for Windows
echo ======================================

echo 📦 Installing PyInstaller...
pip install pyinstaller

echo 🔨 Building version_1...
pyinstaller --onefile --windowed --name nQuester --distpath builds/version_1 --workpath builds/temp_version_1 --specpath builds/temp_version_1 --add-data "data;data" --add-data "Mentors;Mentors" --add-data "Base and Full Map + HD Images;Base and Full Map + HD Images" --add-data "Modern_Interiors_Free_v2.2;Modern_Interiors_Free_v2.2" --add-data "mc;mc" main.py

if %ERRORLEVEL% EQU 0 (
    echo ✅ Build completed successfully!
    echo 📁 Check builds/version_1/nQuester.exe
    echo 🚀 You can now run the game!
) else (
    echo ❌ Build failed!
    echo Check the error messages above.
)

pause 