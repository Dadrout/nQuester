import pygame
import os
from settings import *

class IntroScene:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Load main mentor image
        self.main_mentor = None
        self.load_main_mentor()
        
        # Dialogue lines
        self.dialogue_lines = [
            "Добро пожаловать в nFactorial Incubator!",
            "",
            "Я главный ментор этого инкубатора.",
            "У тебя есть 10 недель, чтобы привлечь 10,000 пользователей.",
            "",
            "Правила простые:",
            "• Выполняй квесты менторов",
            "• Проходи мини-игры",
            "• Привлекай пользователей",
            "• Не выполнишь - вылетаешь из инкубатора!",
            "",
            "Вокруг города ты найдешь менторов:",
            "• Alikhan - iOS разработка",
            "• Alibeck - AI/ML",
            "• Bahredin - TypeScript",
            "• Bahaudin - Backend",
            "• Gaziz - Frontend",
            "• Shoqan - Mobile",
            "• Zhasulan - iOS",
            "• Aimurat - AI/ML",
            "• Bernar - BOSS (финальный вызов)",
            "",
            "Готов к вызову? Нажми E для начала!"
        ]
        
        self.current_line = 0
        self.typing_speed = 0.05  # seconds per character
        self.typing_time = 0
        self.typing_index = 0
        self.typing_active = True
        
        # Background
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((20, 30, 50))
    
    def load_main_mentor(self):
        """Load main mentor image"""
        try:
            mentor_path = "Mentors/main.jpg"
            if os.path.exists(mentor_path):
                self.main_mentor = pygame.image.load(mentor_path)
                # Scale to appropriate size
                self.main_mentor = pygame.transform.scale(self.main_mentor, (200, 200))
                print("✅ Загружен главный ментор")
            else:
                print(f"⚠️ Файл главного ментора не найден: {mentor_path}")
        except Exception as e:
            print(f"❌ Ошибка загрузки главного ментора: {e}")
    
    def update(self, dt):
        """Update typing animation"""
        if self.typing_active and self.current_line < len(self.dialogue_lines):
            self.typing_time += dt
            if self.typing_time >= self.typing_speed:
                self.typing_index += 1
                self.typing_time = 0
                
                current_text = self.dialogue_lines[self.current_line]
                if self.typing_index >= len(current_text):
                    self.typing_active = False
    
    def next_line(self):
        """Move to next dialogue line"""
        if self.current_line < len(self.dialogue_lines) - 1:
            self.current_line += 1
            self.typing_index = 0
            self.typing_active = True
            return False  # Not finished
        return True  # Finished
    
    def draw(self):
        """Draw the intro scene"""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw main mentor
        if self.main_mentor:
            mentor_x = SCREEN_WIDTH // 2 - 100
            mentor_y = 100
            self.screen.blit(self.main_mentor, (mentor_x, mentor_y))
        
        # Draw dialogue box
        box_width = SCREEN_WIDTH - 100
        box_height = 400
        box_x = 50
        box_y = SCREEN_HEIGHT - box_height - 50
        
        # Dialogue background
        dialogue_surface = pygame.Surface((box_width, box_height))
        dialogue_surface.set_alpha(230)
        dialogue_surface.fill((30, 40, 60))
        self.screen.blit(dialogue_surface, (box_x, box_y))
        
        # Border
        pygame.draw.rect(self.screen, (100, 150, 255), (box_x, box_y, box_width, box_height), 3)
        
        # Draw dialogue text
        text_x = box_x + 30
        text_y = box_y + 30
        line_height = 35
        
        # Calculate how many lines we can fit in the box
        max_lines = (box_height - 60) // line_height  # Leave space for margins
        
        # Determine which lines to show (scroll if needed)
        start_line = max(0, self.current_line - max_lines + 1)
        end_line = min(len(self.dialogue_lines), start_line + max_lines)
        
        for i in range(start_line, end_line):
            line = self.dialogue_lines[i]
            
            # If this is the current line being typed
            if i == self.current_line and self.typing_active:
                display_text = line[:self.typing_index]
            else:
                display_text = line
            
            if display_text:
                # Choose font based on line type
                if display_text.startswith("•"):
                    font = self.font_small
                    color = (200, 255, 200)
                    indent = 20
                elif display_text.startswith("Добро пожаловать") or display_text.startswith("Готов к вызову"):
                    font = self.font_medium
                    color = (255, 255, 200)
                    indent = 0
                elif display_text.startswith("Правила простые") or display_text.startswith("Вокруг города"):
                    font = self.font_medium
                    color = (255, 200, 100)
                    indent = 0
                else:
                    font = self.font_small
                    color = (255, 255, 255)
                    indent = 0
                
                text_surface = font.render(display_text, True, color)
                display_y = text_y + (i - start_line) * line_height
                self.screen.blit(text_surface, (text_x + indent, display_y))
        
        # Continue indicator
        if not self.typing_active:
            continue_text = "Нажми E для продолжения..."
            continue_surface = self.font_small.render(continue_text, True, (150, 150, 150))
            continue_rect = continue_surface.get_rect()
            continue_rect.bottomright = (box_x + box_width - 20, box_y + box_height - 20)
            self.screen.blit(continue_surface, continue_rect)
    
    def run(self):
        """Run the intro scene"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            dt = clock.tick(60) / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "exit"
                    elif event.key == pygame.K_e or event.key == pygame.K_RETURN:
                        if self.typing_active:
                            # Skip typing animation
                            self.typing_active = False
                            self.typing_index = len(self.dialogue_lines[self.current_line])
                        else:
                            # Move to next line
                            if self.next_line():
                                return "start_game"  # Intro finished
            
            # Update
            self.update(dt)
            
            # Draw
            self.draw()
            pygame.display.flip()
        
        return "exit" 