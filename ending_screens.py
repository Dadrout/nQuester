import pygame
import os
from settings import *

class EndingScreen:
    def __init__(self, screen, is_victory=True):
        self.screen = screen
        self.is_victory = is_victory
        self.clock = pygame.time.Clock()
        
        # Load ending images
        self.load_ending_images()
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Animation
        self.alpha = 0
        self.fade_speed = 2
        
    def load_ending_images(self):
        """Load ending images"""
        try:
            if self.is_victory:
                image_path = os.path.join("Mentors", "main_good.jpg")
                self.ending_image = pygame.image.load(image_path)
                print(f"✅ Загружено изображение хорошей концовки: {image_path}")
            else:
                image_path = os.path.join("Mentors", "main_bad.jpg")
                self.ending_image = pygame.image.load(image_path)
                print(f"✅ Загружено изображение плохой концовки: {image_path}")
            
            # Scale image to fit screen
            self.ending_image = pygame.transform.scale(self.ending_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"❌ Ошибка загрузки изображения концовки: {e}")
            # Fallback
            self.ending_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.ending_image.fill(GREEN if self.is_victory else RED)
    
    def get_ending_text(self):
        """Get ending text based on victory/defeat"""
        if self.is_victory:
            return [
                "🏆 ПОБЕДА! 🏆",
                "",
                "Ты победил Ассель в эпической битве!",
                "Твой стартап стал легендой в мире технологий.",
                "",
                "🎉 Достижения:",
                "• Победил финального босса",
                "• Привлек 10,000+ пользователей",
                "• Стал лучшим стартапером",
                "• Получил инвестиции от всех фондов",
                "",
                "🌟 Ты доказал, что можешь:",
                "• Создавать инновационные продукты",
                "• Собирать сильную команду",
                "• Побеждать в конкурентной борьбе",
                "• Достигать невозможного!",
                "",
                "🚀 Твой стартап теперь:",
                "• Лидер рынка",
                "• Мультимиллиардная компания",
                "• Пример для всех предпринимателей",
                "",
                "Нажми ESC для выхода"
            ]
        else:
            return [
                "💀 ПОРАЖЕНИЕ 💀",
                "",
                "Ассель оказалась сильнее...",
                "Твой стартап не выдержал испытания.",
                "",
                "😔 Что пошло не так:",
                "• Недостаточно пользователей",
                "• Слабая команда",
                "• Плохая стратегия",
                "• Недостаточно опыта",
                "",
                "💡 Уроки на будущее:",
                "• Нужно больше готовиться",
                "• Собирать сильную команду",
                "• Изучать конкурентов",
                "• Не сдаваться при неудачах",
                "",
                "🔄 Попробуй еще раз:",
                "• Набери больше пользователей",
                "• Улучши навыки",
                "• Изучи все технологии",
                "• И вернись сильнее!",
                "",
                "Нажми ESC для выхода"
            ]
    
    def draw_ending_screen(self):
        """Draw the ending screen"""
        # Draw background image
        self.screen.blit(self.ending_image, (0, 0))
        
        # Create overlay for text readability
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw text
        ending_text = self.get_ending_text()
        y_offset = 100
        
        for line in ending_text:
            if line.startswith("🏆") or line.startswith("💀"):
                color = (255, 215, 0) if self.is_victory else (255, 0, 0)
                font = self.font_large
            elif line.startswith("🎉") or line.startswith("😔"):
                color = (255, 200, 100) if self.is_victory else (255, 100, 100)
                font = self.font_medium
            elif line.startswith("•"):
                color = (200, 200, 200)
                font = self.font_small
            elif line.startswith("🌟") or line.startswith("💡") or line.startswith("🔄"):
                color = (100, 255, 100) if self.is_victory else (255, 150, 100)
                font = self.font_medium
            elif line.startswith("🚀"):
                color = (100, 200, 255)
                font = self.font_medium
            else:
                color = (150, 150, 150)
                font = self.font_small
            
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 40
    
    def run(self):
        """Run the ending screen"""
        print(f"🎬 Показываем {'хорошую' if self.is_victory else 'плохую'} концовку")
        
        while True:
            dt = self.clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
            
            self.draw_ending_screen()
            pygame.display.flip() 