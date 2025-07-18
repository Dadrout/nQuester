import pygame
import os
import json
from settings import *
from npc import NPC

class Level:
    def __init__(self, level_name="base"):
        self.level_name = level_name
        self.npcs = []  # Changed from pygame.sprite.Group() to list
        self.obstacles = pygame.sprite.Group()
        
        # Camera
        self.camera_offset = pygame.math.Vector2()
        
        # Load level
        self.load_level()
        self.create_npcs()
        
        # Background
        self.load_background()
        
    def load_background(self):
        """Load background map image"""
        try:
            if self.level_name == "base":
                bg_path = os.path.join(MAPS_PATH, "Fortuna (Full Map).png")
            else:
                bg_path = os.path.join(MAPS_PATH, "Fortuna (Full Map).png")
                
            if os.path.exists(bg_path):
                self.background = pygame.image.load(bg_path)
                # Scale down if too large
                bg_size = self.background.get_size()
                if bg_size[0] > 2000 or bg_size[1] > 2000:
                    scale_factor = min(2000 / bg_size[0], 2000 / bg_size[1])
                    new_size = (int(bg_size[0] * scale_factor), int(bg_size[1] * scale_factor))
                    self.background = pygame.transform.scale(self.background, new_size)
            else:
                # Create simple background
                self.background = pygame.Surface((1600, 1200))
                self.background.fill((50, 80, 50))  # Dark green
        except:
            # Fallback background
            self.background = pygame.Surface((1600, 1200))
            self.background.fill((50, 80, 50))
    
    def load_level(self):
        """Load level data from JSON or create default"""
        try:
            if self.level_name == "base":
                json_path = os.path.join(MAPS_PATH, "Fortuna (Base Map).json")
            else:
                json_path = os.path.join(MAPS_PATH, "Fortuna (Full Map).json")
                
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    self.level_data = json.load(f)
            else:
                self.level_data = {}
        except:
            self.level_data = {}
    
    def create_npcs(self):
        """Create NPCs for the level"""
        # Mentor positions (spread around the entire map)
        mentors_data = [
            {"name": "Alikhan", "pos": [200, 200]},  # iOS Developer at 1Fit
            {"name": "Alibeck", "pos": [800, 200]},  # Software Engineer at nFactorial AI
            {"name": "Bahredin", "pos": [1400, 200]},  # Middle TypeScript developer at BCC
            {"name": "Bahaudin", "pos": [200, 600]},  # Backend developer at Surfaice
            {"name": "Gaziz", "pos": [800, 600]},  # Middle Frontend developer at Invictus Fitness
            {"name": "Shoqan", "pos": [1400, 600]},  # Middle frontend developer at BCC
            {"name": "Zhasulan", "pos": [200, 1000]},  # Senior iOS developer в KolesaGroup
            {"name": "Aimurat", "pos": [800, 1000]},  # AI Product Engineer @ Surfaice
            {"name": "Bernar", "pos": [1400, 1000]},
            {"name": "Diana", "pos": [500, 400]},
            {"name": "Tamyrlan", "pos": [1100, 800]},
        ]
        
        # Create mentor NPCs
        for mentor_data in mentors_data:
            mentor = NPC(
                mentor_data["pos"][0], 
                mentor_data["pos"][1], 
                mentor_data["name"],
                "mentor"
            )
            self.npcs.append(mentor)
        
        # Add final boss NPC
        final_boss = NPC(800, 400, "FinalBoss", "boss")
        self.npcs.append(final_boss)
        
        # Create some student NPCs (spread around)
        students_data = [
            {"name": "tired_student", "pos": (400, 600), "status": "tired"},
            {"name": "coding_student", "pos": (1100, 500), "status": "coding"},
            {"name": "coffee_student", "pos": (700, 1000), "status": "caffeinated"},
            {"name": "hungry_student", "pos": (300, 800), "status": "hungry"},
            {"name": "sleepy_student", "pos": (900, 300), "status": "sleepy"},
            {"name": "gaming_student", "pos": (1200, 800), "status": "gaming"},
            {"name": "music_student", "pos": (500, 1100), "status": "music"},
            {"name": "sport_student", "pos": (800, 700), "status": "sport"},
            {"name": "art_student", "pos": (200, 900), "status": "art"},
            {"name": "book_student", "pos": (1000, 200), "status": "book"}
        ]
        
        for student_data in students_data:
            student = NPC(
                student_data["pos"][0],
                student_data["pos"][1],
                student_data["name"],
                "student"
            )
            self.npcs.append(student)
    
    def setup_quests(self, quest_manager):
        """Setup quests for NPCs"""
        mentor_quests = [
            "quest_alikhan_01", "quest_alibeck_01", "quest_bahredin_01", "quest_bahaudin_01",
            "quest_gaziz_01", "quest_shoqan_01", "quest_zhasulan_01", "quest_aimurat_01",
            "quest_bernar_01", "quest_diana_frontend", "quest_tamyrlan_backend"
        ]
        student_quests = [
            "quest_student_tired", "quest_student_coding", "quest_student_coffee", "quest_student_hungry",
            "quest_student_sleepy", "quest_student_gaming", "quest_student_music", "quest_student_sport",
            "quest_student_art", "quest_student_book"
        ]
        mentor_reward = (10000 - len(student_quests)*100) // len(mentor_quests)
        student_reward = 100
        # Set up quests for ALL mentors
        for npc in self.npcs:
            if npc.name == "Alikhan":
                npc.set_quest("quest_alikhan_01", [
                    "У меня есть баг в iOS коде.",
                    "Найди ошибку за 15 секунд!"
                ], user_reward=mentor_reward)
            elif npc.name == "Alibeck":
                npc.set_quest("quest_alibeck_01", [
                    "Время тренировать нейросеть!",
                    "Перетащи данные с котиками к модели."
                ], user_reward=mentor_reward)
            elif npc.name == "Bahredin":
                npc.set_quest("quest_bahredin_01", [
                    "Я нашел `any` в нашей кодовой базе.",
                    "Это не просьба. Это ЧП. Исправь."
                ], user_reward=mentor_reward)
            elif npc.name == "Bahaudin":
                npc.set_quest("quest_bahaudin_01", [
                    "Сервер падает каждые 5 минут.",
                    "Найди утечку памяти в коде!"
                ], user_reward=mentor_reward)
            elif npc.name == "Gaziz":
                npc.set_quest("quest_gaziz_01", [
                    "React компонент не рендерится.",
                    "Проверь пропсы и состояние!"
                ], user_reward=mentor_reward)
            elif npc.name == "Shoqan":
                npc.set_quest("quest_shoqan_01", [
                    "У меня проблема с React компонентом.",
                    "Найди и исправь баги в JavaScript коде!"
                ], user_reward=mentor_reward)
            elif npc.name == "Zhasulan":
                npc.set_quest("quest_zhasulan_01", [
                    "CI/CD пайплайн сломан.",
                    "Исправь деплой конфигурацию!"
                ], user_reward=mentor_reward)
            elif npc.name == "Aimurat":
                npc.set_quest("quest_aimurat_01", [
                    "Найди все баги в коде.",
                    "Проведи полное тестирование!"
                ], user_reward=mentor_reward)
            elif npc.name == "Bernar":
                npc.set_quest("quest_bernar_01", [
                    "Ты думаешь, что готов к финальному испытанию?",
                    "Докажи, что ты достоин быть лучшим стартапером!",
                    "Пройди все этапы: архитектура, кодинг, тестирование!"
                ], user_reward=mentor_reward)
            elif npc.name == "FinalBoss":
                npc.set_quest("quest_final_boss", [
                    "Ты думаешь, что готов к настоящему испытанию?",
                    "Столкнись с главным боссом в эпической JRPG битве!",
                    "Чем больше у тебя пользователей, тем слабее босс!"
                ], user_reward=mentor_reward)
            elif npc.name == "Diana":
                npc.set_quest("quest_diana_frontend", [
                    "Привет! Я Diana, эксперт по фронтенд разработке.",
                    "Мне нужен помощник для создания красивого интерфейса.",
                    "Пройди мини-игру 'UI/UX Дизайнер' - создай отзывчивый интерфейс!",
                    "Покажи, что ты понимаешь принципы современного дизайна!"
                ], user_reward=mentor_reward)
            elif npc.name == "Tamyrlan":
                npc.set_quest("quest_tamyrlan_backend", [
                    "Привет! Я Tamyrlan, эксперт по бэкенд архитектуре.",
                    "Мне нужен помощник для создания масштабируемой системы.",
                    "Пройди мини-игру 'Архитектор API' - спроектируй REST API!",
                    "Покажи, что ты понимаешь принципы бэкенд разработки!"
                ], user_reward=mentor_reward)
            elif npc.name == "tired_student":
                npc.set_quest("quest_student_tired", [
                    "Кажется, я слышу цвета...",
                    "Можешь найти мне бутылку воды?"
                ], user_reward=student_reward)
            elif npc.name == "coding_student":
                npc.set_quest("quest_student_coding", [
                    "Я застрял в коде.",
                    "Помоги мне разобраться с этой проблемой!"
                ], user_reward=student_reward)
            elif npc.name == "coffee_student":
                npc.set_quest("quest_student_coffee", [
                    "Я устал от кофе.",
                    "Можешь мне помочь с этой проблемой?"
                ], user_reward=student_reward)
            elif npc.name == "hungry_student":
                npc.set_quest("quest_student_hungry", [
                    "Я голоден.",
                    "Можешь мне помочь с этой проблемой?"
                ], user_reward=student_reward)
            elif npc.name == "sleepy_student":
                npc.set_quest("quest_student_sleepy", [
                    "Я устал.",
                    "Можешь мне помочь с этой проблемой?"
                ], user_reward=student_reward)
            elif npc.name == "gaming_student":
                npc.set_quest("quest_student_gaming", [
                    "Я застрял в игре.",
                    "Помоги мне разобраться с этой проблемой!"
                ], user_reward=student_reward)
            elif npc.name == "music_student":
                npc.set_quest("quest_student_music", [
                    "Я устал от музыки.",
                    "Можешь мне помочь с этой проблемой?"
                ], user_reward=student_reward)
            elif npc.name == "sport_student":
                npc.set_quest("quest_student_sport", [
                    "Я устал от спорта.",
                    "Можешь мне помочь с этой проблемой?"
                ], user_reward=student_reward)
            elif npc.name == "art_student":
                npc.set_quest("quest_student_art", [
                    "Я застрял в творчестве.",
                    "Помоги мне разобраться с этой проблемой!"
                ], user_reward=student_reward)
            elif npc.name == "book_student":
                npc.set_quest("quest_student_book", [
                    "Я застрял в книгах.",
                    "Помоги мне разобраться с этой проблемой!"
                ], user_reward=student_reward)
    
    def update_camera(self, player):
        """Update camera to follow player"""
        # Center camera on player
        target_x = player.position.x - SCREEN_WIDTH // 2
        target_y = player.position.y - SCREEN_HEIGHT // 2
        
        # Clamp camera to background bounds
        max_x = self.background.get_width() - SCREEN_WIDTH
        max_y = self.background.get_height() - SCREEN_HEIGHT
        
        target_x = max(0, min(target_x, max_x))
        target_y = max(0, min(target_y, max_y))
        
        self.camera_offset.x = target_x
        self.camera_offset.y = target_y
    
    def get_nearby_npcs(self, player):
        """Get NPCs near player for interaction"""
        nearby_npcs = []
        for npc in self.npcs:
            if npc.can_interact(player.position):
                nearby_npcs.append(npc)
        return nearby_npcs
    
    def add_item(self, item_name, x, y):
        """Add collectible item to level"""
        # For now, just add to a simple list
        # Could be expanded to actual sprite objects
        pass
    
    def update(self, dt, player):
        """Update level"""
        self.update_camera(player)
        # No need to update sprite group since we're using a list
    
    def draw(self, screen):
        """Draw level"""
        # Draw background relative to camera
        screen.blit(self.background, (0, 0), 
                   pygame.Rect(self.camera_offset.x, self.camera_offset.y, 
                              SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Draw NPCs
        for npc in self.npcs:
            npc.draw(screen, self.camera_offset)
    
    def get_spawn_position(self):
        """Get player spawn position for this level"""
        return (400, 400)  # Default spawn position 