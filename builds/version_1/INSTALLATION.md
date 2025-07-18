# Инструкции по установке и запуску игры

## 🐍 Установка Python

### Windows:
1. **Скачайте Python** с официального сайта: https://www.python.org/downloads/
2. **Выберите Python 3.9+ или новее**
3. **ВАЖНО**: При установке поставьте галочку "Add Python to PATH"
4. **Проверьте установку**:
   ```bash
   python --version
   # или
   py --version
   ```

### macOS:
```bash
# Через Homebrew (рекомендуется)
brew install python

# Или скачайте с python.org
```

### Linux:
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip

# CentOS/RHEL
sudo yum install python3 python3-pip
```

## 🎮 Запуск игры

### Способ 1: Автоматический запуск
```bash
# Этот скрипт автоматически установит pygame если нужно
python run_game.py
```

### Способ 2: Ручная установка
```bash
# Установите pygame
pip install pygame==2.5.2

# Запустите игру
python main.py
```

### Способ 3: Через requirements.txt
```bash
# Установите зависимости
pip install -r requirements.txt

# Запустите игру
python main.py
```

## 🛠️ Устранение неполадок

### "Python was not found"
- Python не установлен или не добавлен в PATH
- Переустановите Python с галочкой "Add to PATH"
- Перезагрузите терминал/компьютер

### "pygame not found" 
```bash
pip install pygame
# или
python -m pip install pygame
```

### "Permission denied"
```bash
# Установите от имени пользователя
pip install --user pygame
```

### Проблемы с UTF-8
Если видите кракозябры вместо русского текста:
```bash
# Windows CMD
chcp 65001

# или используйте PowerShell
```

## 📁 Структура файлов
Убедитесь, что у вас есть все файлы:
```
nQuester/
├── main.py                          ✅ Основной файл
├── run_game.py                      ✅ Launcher
├── settings.py                      ✅ Настройки
├── player.py                        ✅ Игрок
├── npc.py                          ✅ NPC
├── level.py                        ✅ Уровни
├── quest_manager.py                ✅ Квесты
├── ui.py                           ✅ Интерфейс
├── minigames.py                    ✅ Мини-игры
├── requirements.txt                ✅ Зависимости
├── README.md                       ✅ Описание
├── Mentors/                        ✅ Картинки менторов
│   ├── Alikhan.png
│   ├── Alibeck.png
│   ├── Bahredin.png
│   └── ... (все 8 менторов)
└── Base and Full Map + HD Images/  ✅ Карты
    ├── Fortuna (Base Map).png
    ├── Fortuna (Full Map).png
    ├── Fortuna (Base Map).json
    └── Fortuna (Full Map).json
```

## 🎯 Быстрый тест
Если все установлено правильно, эта команда должна работать:
```bash
python -c "import pygame; print('✅ Все готово для игры!')"
```

## 💡 Альтернативные запуски

### Через double-click (Windows)
1. Переименуйте `main.py` в `main.pyw`
2. Двойной клик на файл

### Через IDLE
1. Откройте IDLE (поставляется с Python)
2. File → Open → main.py
3. F5 или Run → Run Module

### Через VS Code
1. Откройте папку в VS Code
2. Нажмите F5 или Run → Start Debugging
3. Выберите Python interpreter

---

**Если ничего не помогает:**
1. Проверьте антивирус (может блокировать pygame)
2. Попробуйте запустить от имени администратора
3. Обновите pip: `python -m pip install --upgrade pip`
4. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   venv\Scripts\activate    # Windows
   # или
   source venv/bin/activate # macOS/Linux
   pip install pygame
   python main.py
   ``` 