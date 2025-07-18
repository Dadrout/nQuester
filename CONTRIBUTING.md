# Руководство по участию в разработке nQuester

Спасибо за интерес к проекту nQuester! Мы рады приветствовать новых контрибьюторов.

## 🚀 Быстрый старт

### Установка окружения
```bash
# Клонируйте репозиторий
git clone https://github.com/Dadrout/nQuester.git
cd nQuester

# Установите зависимости
pip install -r requirements.txt

# Запустите игру
python main.py
```

## 🎯 Области для улучшений

### Приоритетные задачи
- [ ] Добавить новые мини-игры
- [ ] Улучшить систему звука
- [ ] Добавить больше анимаций
- [ ] Создать систему модов
- [ ] Добавить мультиплеер

### Квесты и контент
- [ ] Новые типы квестов
- [ ] Дополнительные NPC
- [ ] Больше локаций
- [ ] Новые достижения

### Технические улучшения
- [ ] Оптимизация производительности
- [ ] Улучшение архитектуры кода
- [ ] Добавление тестов
- [ ] Документация API

## 📝 Стандарты кода

### Python
- Используйте **Python 3.8+**
- Следуйте **PEP 8** стилю
- Добавляйте **типы** для функций
- Пишите **документацию** для классов и методов

### Git коммиты
Используйте [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new minigame system
fix: resolve inventory bug
docs: update README with new features
style: format code according to PEP 8
refactor: improve quest system architecture
test: add unit tests for player class
```

### Структура проекта
```
nQuester/
├── main.py              # Главный файл игры
├── core/                # Основные системы
│   ├── player.py       # Игрок
│   ├── npc.py          # NPC
│   └── quest_manager.py # Квесты
├── minigames/          # Мини-игры
├── ui/                 # Пользовательский интерфейс
├── assets/             # Ресурсы (спрайты, звуки)
├── tests/              # Тесты
└── docs/               # Документация
```

## 🧪 Тестирование

### Запуск тестов
```bash
# Установите pytest
pip install pytest

# Запустите тесты
pytest tests/
```

### Написание тестов
```python
def test_player_movement():
    player = Player(100, 100)
    initial_pos = player.position.copy()
    
    player.direction = pygame.math.Vector2(1, 0)
    player.update(1.0)
    
    assert player.position.x > initial_pos.x
```

## 🎮 Добавление новых функций

### Новая мини-игра
1. Создайте файл в `minigames/`
2. Наследуйтесь от `BaseMinigame`
3. Реализуйте методы `run()` и `draw()`
4. Добавьте в `minigame_manager.py`

### Новый NPC
1. Создайте спрайт в `assets/sprites/`
2. Добавьте в `npc.py`
3. Создайте квест в `quest_manager.py`
4. Добавьте локацию в `level.py`

### Новый тип квеста
1. Добавьте тип в `quest_manager.py`
2. Реализуйте обработку в `main.py`
3. Создайте соответствующую мини-игру
4. Обновите документацию

## 📋 Процесс Pull Request

1. **Форкните** репозиторий
2. Создайте **ветку** для вашей функции:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Разработайте** вашу функцию
4. **Протестируйте** изменения:
   ```bash
   python main.py
   pytest tests/
   ```
5. **Зафиксируйте** изменения:
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```
6. **Отправьте** в ваш форк:
   ```bash
   git push origin feature/amazing-feature
   ```
7. Создайте **Pull Request**

## 🐛 Сообщение об ошибках

При сообщении об ошибке укажите:

- **Описание** проблемы
- **Шаги** для воспроизведения
- **Ожидаемое** поведение
- **Фактическое** поведение
- **Версия** Python и pygame
- **Скриншоты** (если применимо)

## 💡 Предложения

Для предложений новых функций:

- Опишите **проблему**, которую решает функция
- Предложите **решение**
- Укажите **приоритет** (низкий/средний/высокий)
- Добавьте **примеры** использования

## 🤝 Коммуникация

- **Issues** - для багов и предложений
- **Discussions** - для общих вопросов
- **Pull Requests** - для кода

## 📄 Лицензия

Участвуя в проекте, вы соглашаетесь с [MIT лицензией](LICENSE).

---

**Спасибо за вклад в nQuester! 🎮** 