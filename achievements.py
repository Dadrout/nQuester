import pygame
from settings import *
from sound_manager import get_sound_manager

class Achievement:
    def __init__(self, id, title, description, icon, condition):
        self.id = id
        self.title = title
        self.description = description
        self.icon = icon
        self.condition = condition
        self.unlocked = False
        self.unlock_time = None
    
    def check_condition(self, game_state):
        """Check if achievement should be unlocked"""
        if not self.unlocked and self.condition(game_state):
            self.unlock()
            return True
        return False
    
    def unlock(self):
        """Unlock the achievement"""
        self.unlocked = True
        self.unlock_time = pygame.time.get_ticks()
        
        # Play achievement unlock sound
        sound_manager = get_sound_manager()
        if sound_manager:
            sound_manager.play_achievement()

class AchievementManager:
    def __init__(self):
        self.achievements = {}
        self.unlocked_achievements = []
        self.achievement_notifications = []
        
        self.setup_achievements()
    
    def setup_achievements(self):
        """Setup all achievements"""
        achievements_data = [
            {
                "id": "first_quest",
                "title": "Первый квест",
                "description": "Выполните свой первый квест",
                "icon": "🎯",
                "condition": lambda state: state.get("completed_quests", 0) >= 1
            },
            {
                "id": "swift_master",
                "title": "Swift Мастер",
                "description": "Выполните все iOS квесты",
                "icon": "🍎",
                "condition": lambda state: state.get("swift_quests", 0) >= 3
            },
            {
                "id": "ai_expert",
                "title": "AI Эксперт", 
                "description": "Обучите 5 нейросетей",
                "icon": "🤖",
                "condition": lambda state: state.get("ai_quests", 0) >= 5
            },
            {
                "id": "typescript_guru",
                "title": "TypeScript Гуру",
                "description": "Пройдите все TypeScript тесты",
                "icon": "📘",
                "condition": lambda state: state.get("typescript_quests", 0) >= 3
            },
            {
                "id": "debug_master",
                "title": "Debug Мастер",
                "description": "Найдите 10 багов в коде",
                "icon": "🐛",
                "condition": lambda state: state.get("bugs_found", 0) >= 10
            },
            {
                "id": "user_magnet",
                "title": "Магнит пользователей",
                "description": "Привлеките 5000 пользователей",
                "icon": "👥",
                "condition": lambda state: state.get("users", 0) >= 5000
            },
            {
                "id": "quest_hunter",
                "title": "Охотник за квестами",
                "description": "Выполните 10 квестов",
                "icon": "🗺️",
                "condition": lambda state: state.get("completed_quests", 0) >= 10
            },
            {
                "id": "speed_runner",
                "title": "Спидраннер",
                "description": "Выполните квест менее чем за 5 секунд",
                "icon": "⚡",
                "condition": lambda state: state.get("fastest_quest_time", 999) < 5
            },
            {
                "id": "perfectionist",
                "title": "Перфекционист",
                "description": "Выполните квест без ошибок",
                "icon": "💎",
                "condition": lambda state: state.get("perfect_quests", 0) >= 1
            },
            {
                "id": "mentor_friend",
                "title": "Друг менторов",
                "description": "Поговорите со всеми менторами",
                "icon": "🤝",
                "condition": lambda state: state.get("mentors_met", 0) >= 8
            }
        ]
        
        for data in achievements_data:
            achievement = Achievement(
                data["id"],
                data["title"], 
                data["description"],
                data["icon"],
                data["condition"]
            )
            self.achievements[data["id"]] = achievement
    
    def update(self, game_state):
        """Update achievements and check for unlocks"""
        for achievement in self.achievements.values():
            if achievement.check_condition(game_state):
                self.add_notification(achievement)
    
    def add_notification(self, achievement):
        """Add achievement notification"""
        notification = {
            "achievement": achievement,
            "start_time": pygame.time.get_ticks(),
            "duration": 3000  # 3 seconds
        }
        self.achievement_notifications.append(notification)
    
    def draw_notifications(self, screen):
        """Draw achievement notifications"""
        current_time = pygame.time.get_ticks()
        
        # Remove expired notifications
        self.achievement_notifications = [
            n for n in self.achievement_notifications 
            if current_time - n["start_time"] < n["duration"]
        ]
        
        # Draw active notifications
        for i, notification in enumerate(self.achievement_notifications):
            self.draw_notification(screen, notification, i)
    
    def draw_notification(self, screen, notification, index):
        """Draw a single achievement notification"""
        achievement = notification["achievement"]
        current_time = pygame.time.get_ticks()
        elapsed = current_time - notification["start_time"]
        progress = elapsed / notification["duration"]
        
        # Calculate position (slide in from right)
        if progress < 0.2:
            # Slide in
            x_offset = int((1 - progress / 0.2) * 300)
        elif progress > 0.8:
            # Slide out
            x_offset = int(((progress - 0.8) / 0.2) * 300)
        else:
            # Stay in place
            x_offset = 0
        
        x = SCREEN_WIDTH - 320 + x_offset
        y = 100 + index * 80
        
        # Background
        notification_surface = pygame.Surface((300, 60), pygame.SRCALPHA)
        notification_surface.fill((0, 0, 0, 200))
        pygame.draw.rect(notification_surface, (255, 255, 0), (0, 0, 300, 60), 2)
        
        screen.blit(notification_surface, (x, y))
        
        # Icon
        font_large = pygame.font.Font(None, 36)
        icon_surface = font_large.render(achievement.icon, True, (255, 255, 0))
        screen.blit(icon_surface, (x + 10, y + 10))
        
        # Title
        font_medium = pygame.font.Font(None, 24)
        title_surface = font_medium.render(achievement.title, True, (255, 255, 255))
        screen.blit(title_surface, (x + 50, y + 10))
        
        # Description
        font_small = pygame.font.Font(None, 18)
        desc_surface = font_small.render(achievement.description, True, (200, 200, 200))
        screen.blit(desc_surface, (x + 50, y + 35))
    
    def get_achievement_stats(self, game_state):
        """Get achievement statistics"""
        stats = {
            "total_achievements": len(self.achievements),
            "unlocked_achievements": len([a for a in self.achievements.values() if a.unlocked]),
            "completion_percentage": 0
        }
        
        if stats["total_achievements"] > 0:
            stats["completion_percentage"] = int((stats["unlocked_achievements"] / stats["total_achievements"]) * 100)
        
        return stats

# Global achievement manager
achievement_manager = None

def init_achievement_manager():
    """Initialize the global achievement manager"""
    global achievement_manager
    achievement_manager = AchievementManager()
    return achievement_manager

def get_achievement_manager():
    """Get the global achievement manager"""
    return achievement_manager 