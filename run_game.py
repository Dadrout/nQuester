#!/usr/bin/env python3
"""
nQuester: Incubator Rush
Launcher script with dependency checking
"""

import sys
import subprocess
import importlib

def check_and_install_pygame():
    """Check if pygame is installed, install if not"""
    try:
        import pygame
        print("✅ pygame найден!")
        return True
    except ImportError:
        print("❌ pygame не установлен. Устанавливаю...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame==2.5.2"])
            print("✅ pygame успешно установлен!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Ошибка установки pygame. Попробуйте установить вручную:")
            print("pip install pygame==2.5.2")
            return False

def main():
    """Main launcher function"""
    print("🚀 nQuester: Incubator Rush")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Требуется Python 3.7 или выше")
        print(f"Текущая версия: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python {sys.version}")
    
    # Check and install pygame
    if not check_and_install_pygame():
        sys.exit(1)
    
    print("\n🎮 Запускаю игру...")
    print("=" * 40)
    
    try:
        import main
        main.Game().run()
    except Exception as e:
        print(f"❌ Ошибка запуска игры: {e}")
        print("\nИнструкции по устранению неполадок:")
        print("1. Убедитесь, что все файлы игры находятся в одной папке")
        print("2. Проверьте, что папки 'Mentors' и 'Base and Full Map + HD Images' существуют")
        print("3. Попробуйте запустить напрямую: python main.py")
        sys.exit(1)

if __name__ == "__main__":
    main() 