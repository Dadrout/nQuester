import pygame
import random
import json
import os
from settings import *
from sound_manager import get_sound_manager

class Item:
    """Предметы, которые дают бонусы игроку"""
    def __init__(self, name, description, icon, effect_type, effect_value, duration=0):
        self.name = name
        self.description = description
        self.icon = icon
        self.effect_type = effect_type  # "users", "speed", "luck", "energy"
        self.effect_value = effect_value
        self.duration = duration  # 0 = permanent, >0 = temporary
        self.obtained_time = 0

class ProgressTracker:
    """Отслеживание прогресса по квестам и студентам"""
    def __init__(self):
        self.quest_progress = {}
        self.student_progress = {}
        self.mentor_progress = {}
        self.total_quests = 0
        self.completed_quests = 0
        
    def update_quest_progress(self, quest_id, completed=False):
        if quest_id not in self.quest_progress:
            self.quest_progress[quest_id] = {"completed": False, "attempts": 0}
        
        if completed:
            self.quest_progress[quest_id]["completed"] = True
            self.completed_quests += 1
        else:
            self.quest_progress[quest_id]["attempts"] += 1
    
    def get_quest_progress_percentage(self):
        if self.total_quests == 0:
            return 0
        return (self.completed_quests / self.total_quests) * 100
    
    def update_student_progress(self, student_id, quest_completed=False):
        if student_id not in self.student_progress:
            self.student_progress[student_id] = {"quests_completed": 0, "total_quests": 0}
        
        if quest_completed:
            self.student_progress[student_id]["quests_completed"] += 1
    
    def get_student_progress_percentage(self, student_id):
        if student_id not in self.student_progress:
            return 0
        student = self.student_progress[student_id]
        if student["total_quests"] == 0:
            return 0
        return (student["quests_completed"] / student["total_quests"]) * 100

class RewardSystem:
    """Улучшенная система наград"""
    def __init__(self):
        self.items = []
        self.achievements = []
        self.user_bonuses = 0
        self.load_items()
    
    def load_items(self):
        """Загрузка предметов из файла или создание по умолчанию"""
        self.items_data = {
            "coffee": {
                "name": "Кофе",
                "description": "Дает +50 пользователей и ускоряет выполнение квестов",
                "icon": "☕",
                "effect_type": "users",
                "effect_value": 50,
                "duration": 0
            },
            "energy_drink": {
                "name": "Энергетик",
                "description": "Временно увеличивает скорость на 50%",
                "icon": "⚡",
                "effect_type": "speed",
                "effect_value": 1.5,
                "duration": 30000  # 30 секунд
            },
            "presentation": {
                "name": "Доклад",
                "description": "Привлекает +200 пользователей",
                "icon": "📊",
                "effect_type": "users",
                "effect_value": 200,
                "duration": 0
            },
            "certificate": {
                "name": "Сертификат",
                "description": "Постоянно увеличивает привлекательность",
                "icon": "🏆",
                "effect_type": "users",
                "effect_value": 100,
                "duration": 0
            },
            "debug_tool": {
                "name": "Отладочный инструмент",
                "description": "Увеличивает шанс найти баги",
                "icon": "🔧",
                "effect_type": "luck",
                "effect_value": 1.3,
                "duration": 0
            }
        }
    
    def give_reward(self, quest_id, difficulty="normal"):
        """Выдача награды за квест с учетом сложности"""
        base_users = 100
        
        # Множители сложности
        difficulty_multipliers = {
            "easy": 0.7,
            "normal": 1.0,
            "hard": 1.5,
            "boss": 3.0
        }
        
        multiplier = difficulty_multipliers.get(difficulty, 1.0)
        users_reward = int(base_users * multiplier)
        
        # Шанс получить предмет
        item_chance = 0.3 if difficulty == "normal" else 0.5 if difficulty == "hard" else 0.8
        item = None
        
        if random.random() < item_chance:
            item_name = random.choice(list(self.items_data.keys()))
            item_data = self.items_data[item_name]
            item = Item(
                item_data["name"],
                item_data["description"],
                item_data["icon"],
                item_data["effect_type"],
                item_data["effect_value"],
                item_data["duration"]
            )
        
        return {
            "users": users_reward,
            "item": item,
            "experience": int(50 * multiplier)
        }

class RandomEvent:
    """Случайные события на карте"""
    def __init__(self, name, description, effect_type, effect_value, duration=0):
        self.name = name
        self.description = description
        self.effect_type = effect_type
        self.effect_value = effect_value
        self.duration = duration
        self.active = False
        self.start_time = 0

class EventManager:
    """Управление случайными событиями"""
    def __init__(self):
        self.events = []
        self.active_events = []
        self.event_timer = 0
        self.event_interval = 60000  # 1 минута
        self.setup_events()
    
    def setup_events(self):
        """Настройка случайных событий"""
        self.events = [
            RandomEvent(
                "Инвестор пришел!",
                "Инвестор заинтересован в вашем проекте! +300 пользователей",
                "users",
                300,
                30000  # 30 секунд
            ),
            RandomEvent(
                "Сервер упал!",
                "Технические проблемы! -100 пользователей",
                "users",
                -100,
                15000  # 15 секунд
            ),
            RandomEvent(
                "Вирусный тренд!",
                "Ваш проект стал вирусным! +500 пользователей",
                "users",
                500,
                45000  # 45 секунд
            ),
            RandomEvent(
                "Хакерская атака!",
                "Кибератака! Нужно быстро исправить баги",
                "bug_hunt",
                0,
                20000  # 20 секунд
            ),
            RandomEvent(
                "Конференция разработчиков",
                "Выступление на конференции! +400 пользователей",
                "users",
                400,
                60000  # 1 минута
            )
        ]
    
    def update(self, dt):
        """Обновление событий"""
        self.event_timer += dt
        
        # Проверка новых событий
        if self.event_timer >= self.event_interval:
            self.trigger_random_event()
            self.event_timer = 0
        
        # Обновление активных событий
        current_time = pygame.time.get_ticks()
        self.active_events = [
            event for event in self.active_events
            if current_time - event.start_time < event.duration
        ]
    
    def trigger_random_event(self):
        """Запуск случайного события"""
        if not self.events:
            return
        
        event = random.choice(self.events)
        event.active = True
        event.start_time = pygame.time.get_ticks()
        self.active_events.append(event)
        
        # Воспроизведение звука события
        sound_manager = get_sound_manager()
        if sound_manager:
            sound_manager.play_sound("event")
        
        print(f"🎲 Случайное событие: {event.name}")

class NPCInteraction:
    """Улучшенное взаимодействие с NPC"""
    def __init__(self):
        self.dialogue_states = {}  # Состояния диалогов для каждого NPC
        self.quest_completion_dialogues = {}
        self.setup_completion_dialogues()
    
    def setup_completion_dialogues(self):
        """Настройка диалогов после выполнения квестов"""
        self.quest_completion_dialogues = {
            "Alikhan": [
                "Отличная работа! Ты настоящий Swift мастер! 🍎",
                "Спасибо за помощь с iOS! Теперь приложение работает идеально!",
                "Ты спас наш мобильный проект! Настоящий профессионал!"
            ],
            "Alibeck": [
                "Импрессивно! AI теперь работает как часы! 🤖",
                "Нейросеть стала намного умнее! Спасибо!",
                "Ты превратил наш AI в настоящего гения!"
            ],
            "Bahredin": [
                "Кодовая база теперь в безопасности! 🔒",
                "TypeScript строгость восстановлена! Спасибо!",
                "Больше никаких any! Ты спас наш проект!"
            ],
            "Bahaudin": [
                "Сервер больше не падает! 💾",
                "Память теперь используется эффективно! Отличная работа!",
                "Ты настоящий backend эксперт!"
            ],
            "Gaziz": [
                "React компонент работает идеально! ⚛️",
                "Frontend спасен! Спасибо за отладку!",
                "Ты превратил наш UI в произведение искусства!"
            ],
            "Shoqan": [
                "Мобильное приложение стабильно! 📱",
                "Настоящий мобильный эксперт! Приложение спасено!",
                "Ты сделал наше приложение лучшим в App Store!"
            ],
            "Zhasulan": [
                "iOS приложение теперь стабильно! 📱",
                "Swift код исправлен! Настоящий iOS разработчик!",
                "Приложение работает как часы!"
            ],
            "Aimurat": [
                "AI модель обучена успешно! 🤖",
                "Нейросеть теперь работает идеально!",
                "Ты настоящий AI/ML эксперт!"
            ],
            "Bernar": [
                "Ты прошел все испытания! 🏆",
                "Настоящий БОСС! Инвесторы будут в восторге!",
                "Ты доказал, что достоин быть лучшим стартапером!"
            ]
        }
    
    def get_completion_dialogue(self, npc_name):
        """Получение диалога после выполнения квеста"""
        if npc_name in self.quest_completion_dialogues:
            dialogues = self.quest_completion_dialogues[npc_name]
            return random.choice(dialogues)
        return "Спасибо за помощь! Отличная работа!"

class HumorSystem:
    """Система юмора и пасхалок"""
    def __init__(self):
        self.easter_eggs = []
        self.random_tips = []
        self.meme_references = []
        self.setup_humor_content()
    
    def setup_humor_content(self):
        """Настройка юмористического контента"""
        self.random_tips = [
            "💡 Совет: Кофе + Энергетик = Суперпрограммист",
            "💡 Совет: Лучший код - это код, который работает",
            "💡 Совет: Git commit -m 'fix' решает все проблемы",
            "💡 Совет: Stack Overflow - лучший друг разработчика",
            "💡 Совет: Ctrl+C, Ctrl+V - основа программирования",
            "💡 Совет: Баг - это не баг, это фича",
            "💡 Совет: Чем больше комментариев, тем лучше код",
            "💡 Совет: Python - лучший язык для всего",
            "💡 Совет: JavaScript - язык будущего",
            "💡 Совет: Rust - безопасность превыше всего"
        ]
        
        self.meme_references = [
            "🎮 'It just works' - Todd Howard",
            "🎮 'Hello World' - первый шаг к успеху",
            "🎮 '99 little bugs in the code...'",
            "🎮 'Stack Overflow is my documentation'",
            "🎮 'I don't always test my code, but when I do...'",
            "🎮 'Real programmers count from 0'",
            "🎮 'There are 10 types of people...'",
            "🎮 'Why do programmers prefer dark mode?'",
            "🎮 'Git: 'It's not a bug, it's an undocumented feature''",
            "🎮 'The best code is no code'"
        ]
    
    def get_random_tip(self):
        """Получение случайного совета"""
        return random.choice(self.random_tips)
    
    def get_random_meme(self):
        """Получение случайной мем-ссылки"""
        return random.choice(self.meme_references)

class SettingsManager:
    """Управление настройками игры"""
    def __init__(self):
        self.settings = {
            "master_volume": 0.7,
            "music_volume": 0.5,
            "sfx_volume": 0.8,
            "screen_resolution": "1280x720",
            "fullscreen": False,
            "show_tips": True,
            "auto_save": True,
            "difficulty": "normal"
        }
        self.load_settings()
    
    def load_settings(self):
        """Загрузка настроек из файла"""
        try:
            if os.path.exists('data/settings.json'):
                with open('data/settings.json', 'r') as f:
                    saved_settings = json.load(f)
                    self.settings.update(saved_settings)
        except:
            pass
    
    def save_settings(self):
        """Сохранение настроек в файл"""
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/settings.json', 'w') as f:
                json.dump(self.settings, f, indent=2)
        except:
            pass
    
    def update_setting(self, key, value):
        """Обновление настройки"""
        self.settings[key] = value
        self.save_settings()

class ImprovementManager:
    """Главный менеджер всех улучшений"""
    def __init__(self):
        self.progress_tracker = ProgressTracker()
        self.reward_system = RewardSystem()
        self.event_manager = EventManager()
        self.npc_interaction = NPCInteraction()
        self.humor_system = HumorSystem()
        self.settings_manager = SettingsManager()
        
        # Анимации наград
        self.reward_animations = []
        self.animation_timer = 0
    
    def update(self, dt):
        """Обновление всех систем"""
        self.event_manager.update(dt)
        self.update_reward_animations(dt)
    
    def update_reward_animations(self, dt):
        """Обновление анимаций наград"""
        self.animation_timer += dt
        
        # Удаление завершенных анимаций
        self.reward_animations = [
            anim for anim in self.reward_animations
            if pygame.time.get_ticks() - anim["start_time"] < anim["duration"]
        ]
    
    def show_reward_animation(self, reward_type, value):
        """Показ анимации награды"""
        animation = {
            "type": reward_type,
            "value": value,
            "start_time": pygame.time.get_ticks(),
            "duration": 3000,  # 3 секунды
            "y_offset": 0
        }
        self.reward_animations.append(animation)
        
        # Воспроизведение звука награды
        sound_manager = get_sound_manager()
        if sound_manager:
            sound_manager.play_sound("reward")
    
    def draw_reward_animations(self, screen):
        """Отрисовка анимаций наград"""
        current_time = pygame.time.get_ticks()
        
        for animation in self.reward_animations:
            elapsed = current_time - animation["start_time"]
            progress = elapsed / animation["duration"]
            
            # Анимация появления/исчезновения
            if progress < 0.3:
                alpha = int(255 * (progress / 0.3))
            elif progress > 0.7:
                alpha = int(255 * ((1 - progress) / 0.3))
            else:
                alpha = 255
            
            # Позиция (поднимается вверх)
            y_offset = int(50 * progress)
            x = SCREEN_WIDTH // 2
            y = SCREEN_HEIGHT // 2 - 100 - y_offset
            
            # Текст награды
            font = pygame.font.Font(None, 48)
            text = f"+{animation['value']} {animation['type']}"
            text_surface = font.render(text, True, (255, 255, 0))
            text_surface.set_alpha(alpha)
            
            # Центрирование текста
            text_rect = text_surface.get_rect(center=(x, y))
            screen.blit(text_surface, text_rect)
    
    def draw_progress_bars(self, screen, player, quest_manager):
        """Отрисовка прогресс-баров"""
        # Прогресс-бар квестов
        quest_progress = self.progress_tracker.get_quest_progress_percentage()
        self.draw_progress_bar(screen, 10, 70, 200, 15, quest_progress, 
                             "Квесты", (0, 255, 0))
        
        # Прогресс-бар пользователей
        user_progress = (player.current_users / TARGET_USERS) * 100
        self.draw_progress_bar(screen, 10, 90, 200, 15, user_progress,
                             "Пользователи", (0, 150, 255))
        
        # Прогресс-бар студентов
        student_progress = self.get_student_progress()
        self.draw_progress_bar(screen, 10, 110, 200, 15, student_progress,
                             "Студенты", (255, 150, 0))
    
    def draw_progress_bar(self, screen, x, y, width, height, percentage, label, color):
        """Отрисовка отдельного прогресс-бара"""
        # Фон
        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))
        
        # Заполнение
        fill_width = int(width * percentage / 100)
        pygame.draw.rect(screen, color, (x, y, fill_width, height))
        
        # Граница
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 2)
        
        # Текст
        font = pygame.font.Font(None, 20)
        text = f"{label}: {percentage:.1f}%"
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (x + 5, y + 2))
    
    def get_student_progress(self):
        """Получение прогресса студентов"""
        if not self.progress_tracker.student_progress:
            return 0
        
        total_progress = 0
        for student_id in self.progress_tracker.student_progress:
            total_progress += self.progress_tracker.get_student_progress_percentage(student_id)
        
        return total_progress / len(self.progress_tracker.student_progress)
    
    def draw_active_events(self, screen):
        """Отрисовка активных событий"""
        if not self.event_manager.active_events:
            return
        
        y_offset = 150
        for event in self.event_manager.active_events:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - event.start_time
            remaining = event.duration - elapsed
            
            # Фон события
            event_surface = pygame.Surface((300, 60), pygame.SRCALPHA)
            event_surface.fill((255, 0, 0, 150))
            
            # Текст события
            font = pygame.font.Font(None, 20)
            name_surface = font.render(event.name, True, (255, 255, 255))
            desc_surface = font.render(event.description, True, (200, 200, 200))
            
            # Таймер
            timer_text = f"Осталось: {remaining // 1000}с"
            timer_surface = font.render(timer_text, True, (255, 255, 0))
            
            # Отрисовка
            screen.blit(event_surface, (SCREEN_WIDTH - 320, y_offset))
            screen.blit(name_surface, (SCREEN_WIDTH - 310, y_offset + 5))
            screen.blit(desc_surface, (SCREEN_WIDTH - 310, y_offset + 25))
            screen.blit(timer_surface, (SCREEN_WIDTH - 310, y_offset + 40))
            
            y_offset += 70

# Глобальные экземпляры
improvement_manager = None

def init_improvement_manager():
    """Инициализация менеджера улучшений"""
    global improvement_manager
    improvement_manager = ImprovementManager()

def get_improvement_manager():
    """Получение менеджера улучшений"""
    return improvement_manager 