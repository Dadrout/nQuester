import pygame
from settings import *
from achievements import get_achievement_manager
from improvements import get_improvement_manager

class AchievementsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.achievement_manager = get_achievement_manager()
        self.improvement_manager = get_improvement_manager()
        
        # UI elements
        self.achievements_list = []
        self.selected_achievement = 0
        self.scroll_offset = 0
        self.setup_achievements_list()
    
    def setup_achievements_list(self):
        """Setup achievements list"""
        if not self.achievement_manager:
            return
        
        self.achievements_list = []
        for achievement in self.achievement_manager.achievements.values():
            self.achievements_list.append(achievement)
    
    def handle_events(self):
        """Handle achievements screen events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
                
                elif event.key == pygame.K_UP:
                    self.selected_achievement = max(0, self.selected_achievement - 1)
                    self.adjust_scroll()
                
                elif event.key == pygame.K_DOWN:
                    self.selected_achievement = min(len(self.achievements_list) - 1, 
                                                 self.selected_achievement + 1)
                    self.adjust_scroll()
                
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return self.show_achievement_details()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                return self.handle_mouse_click(mouse_pos)
        
        return None
    
    def adjust_scroll(self):
        """Adjust scroll to keep selected achievement visible"""
        visible_achievements = 8  # Number of achievements visible at once
        if self.selected_achievement < self.scroll_offset:
            self.scroll_offset = self.selected_achievement
        elif self.selected_achievement >= self.scroll_offset + visible_achievements:
            self.scroll_offset = self.selected_achievement - visible_achievements + 1
    
    def show_achievement_details(self):
        """Show detailed information about selected achievement"""
        if 0 <= self.selected_achievement < len(self.achievements_list):
            achievement = self.achievements_list[self.selected_achievement]
            
            # Show achievement details in a popup
            details = [
                f"🏆 {achievement.title}",
                "",
                achievement.description,
                "",
                f"Статус: {'✅ Разблокировано' if achievement.unlocked else '🔒 Заблокировано'}",
                f"Иконка: {achievement.icon}",
                "",
                "Нажмите любую клавишу для возврата"
            ]
            
            return self.show_popup(details)
        
        return None
    
    def show_popup(self, lines):
        """Show a popup with text lines"""
        popup_width = 400
        popup_height = 300
        popup_x = (SCREEN_WIDTH - popup_width) // 2
        popup_y = (SCREEN_HEIGHT - popup_height) // 2
        
        # Popup background
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill((50, 50, 50))
        pygame.draw.rect(popup_surface, WHITE, popup_surface.get_rect(), 2)
        
        # Draw text lines
        y_offset = 20
        for line in lines:
            if line.startswith("🏆"):
                text_surface = self.font_medium.render(line, True, YELLOW)
            elif line.startswith("✅"):
                text_surface = self.font_small.render(line, True, GREEN)
            elif line.startswith("🔒"):
                text_surface = self.font_small.render(line, True, RED)
            else:
                text_surface = self.font_small.render(line, True, WHITE)
            
            text_rect = text_surface.get_rect(center=(popup_width//2, y_offset))
            popup_surface.blit(text_surface, text_rect)
            y_offset += 30
        
        # Show popup
        self.screen.blit(popup_surface, (popup_x, popup_y))
        pygame.display.flip()
        
        # Wait for key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    waiting = False
                    break
        
        return None
    
    def handle_mouse_click(self, mouse_pos):
        """Handle mouse clicks"""
        # Check if clicking on achievement list
        list_rect = pygame.Rect(50, 150, SCREEN_WIDTH - 100, 400)
        if list_rect.collidepoint(mouse_pos):
            # Calculate which achievement was clicked
            relative_y = mouse_pos[1] - list_rect.y
            achievement_index = (relative_y // 50) + self.scroll_offset
            
            if 0 <= achievement_index < len(self.achievements_list):
                self.selected_achievement = achievement_index
                return self.show_achievement_details()
        
        return None
    
    def draw(self):
        """Draw achievements screen"""
        # Background
        self.screen.fill(BLACK)
        
        # Draw title
        title_surface = self.font_large.render("ДОСТИЖЕНИЯ", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 75))
        self.screen.blit(title_surface, title_rect)
        
        # Draw statistics
        self.draw_statistics()
        
        # Draw achievements list
        self.draw_achievements_list()
        
        # Draw help text
        help_text = "Используйте стрелки для навигации, Enter для деталей"
        help_surface = self.font_small.render(help_text, True, GRAY)
        help_rect = help_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        self.screen.blit(help_surface, help_rect)
        
        pygame.display.flip()
    
    def draw_statistics(self):
        """Draw achievement statistics"""
        if not self.achievement_manager:
            return
        
        stats = self.achievement_manager.get_achievement_stats({})
        
        # Statistics background
        stats_rect = pygame.Rect(50, 100, SCREEN_WIDTH - 100, 40)
        pygame.draw.rect(self.screen, (30, 30, 30), stats_rect)
        pygame.draw.rect(self.screen, WHITE, stats_rect, 1)
        
        # Statistics text
        stats_text = f"Разблокировано: {stats['unlocked_achievements']}/{stats['total_achievements']} ({stats['completion_percentage']:.1f}%)"
        stats_surface = self.font_small.render(stats_text, True, WHITE)
        stats_rect_text = stats_surface.get_rect(center=stats_rect.center)
        self.screen.blit(stats_surface, stats_rect_text)
    
    def draw_achievements_list(self):
        """Draw achievements list"""
        if not self.achievement_manager:
            return
        
        list_rect = pygame.Rect(50, 150, SCREEN_WIDTH - 100, 400)
        pygame.draw.rect(self.screen, (30, 30, 30), list_rect)
        pygame.draw.rect(self.screen, WHITE, list_rect, 1)
        
        # Draw visible achievements
        visible_count = 8
        for i in range(visible_count):
            achievement_index = self.scroll_offset + i
            if achievement_index >= len(self.achievements_list):
                break
            
            achievement = self.achievements_list[achievement_index]
            is_selected = (achievement_index == self.selected_achievement)
            
            # Achievement background
            achievement_rect = pygame.Rect(60, 160 + i * 50, SCREEN_WIDTH - 120, 40)
            color = YELLOW if is_selected else (50, 50, 50)
            pygame.draw.rect(self.screen, color, achievement_rect)
            pygame.draw.rect(self.screen, WHITE, achievement_rect, 1)
            
            # Achievement icon
            icon_surface = self.font_medium.render(achievement.icon, True, WHITE)
            self.screen.blit(icon_surface, (70, 170 + i * 50))
            
            # Achievement title
            title_color = WHITE if achievement.unlocked else GRAY
            title_surface = self.font_small.render(achievement.title, True, title_color)
            self.screen.blit(title_surface, (110, 170 + i * 50))
            
            # Achievement status
            status_icon = "✅" if achievement.unlocked else "🔒"
            status_surface = self.font_small.render(status_icon, True, GREEN if achievement.unlocked else RED)
            status_rect = status_surface.get_rect()
            status_rect.right = SCREEN_WIDTH - 70
            status_rect.centery = 170 + i * 50 + 10
            self.screen.blit(status_surface, status_rect)
        
        # Draw scroll indicators
        if self.scroll_offset > 0:
            up_arrow = self.font_small.render("↑", True, WHITE)
            self.screen.blit(up_arrow, (SCREEN_WIDTH - 40, 160))
        
        if self.scroll_offset + visible_count < len(self.achievements_list):
            down_arrow = self.font_small.render("↓", True, WHITE)
            self.screen.blit(down_arrow, (SCREEN_WIDTH - 40, 160 + visible_count * 50))
    
    def run(self):
        """Run achievements screen"""
        running = True
        while running:
            result = self.handle_events()
            if result == "quit":
                return "quit"
            elif result == "back":
                return "menu"
            
            self.draw()
        
        return "menu" 