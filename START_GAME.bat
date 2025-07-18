@echo off
chcp 65001 >nul
echo 🚀 nQuester: Incubator Rush 🚀
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo.
    echo 📋 Инструкции по установке:
    echo 1. Скачайте Python с https://www.python.org/downloads/
    echo 2. При установке поставьте галочку "Add Python to PATH"
    echo 3. Перезагрузите компьютер
    echo 4. Запустите этот файл снова
    echo.
    pause
    exit /b 1
)

echo ✅ Python найден!

REM Check if pygame is installed
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo ❌ pygame не установлен. Устанавливаю...
    python -m pip install pygame==2.5.2
    if errorlevel 1 (
        echo ❌ Ошибка установки pygame
        echo Попробуйте установить вручную: pip install pygame
        pause
        exit /b 1
    )
    echo ✅ pygame установлен!
)

echo ✅ Все зависимости готовы!
echo.
echo 🎮 Запускаю игру...
echo ================================
echo.

REM Try to run the main game
if exist "main.py" (
    python main.py
) else (
    echo ❌ Файл main.py не найден!
    echo Убедитесь, что все файлы игры находятся в этой папке
    pause
    exit /b 1
)

if errorlevel 1 (
    echo.
    echo ❌ Ошибка запуска игры
    echo 📋 Попробуйте демо-версию:
    echo python demo.py
    echo.
    pause
)

echo.
echo 🏁 Игра завершена!
pause 