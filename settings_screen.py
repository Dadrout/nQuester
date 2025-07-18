import pygame
from settings import *
from improvements import get_improvement_manager

class SettingsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.improvement_manager = get_improvement_manager()
        self.settings_manager = self.improvement_manager.settings_manager if self.improvement_manager else None
        
        # UI elements
        self.buttons = []
        self.sliders = []
        self.checkboxes = []
        self.selected_option = 0
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI elements"""
        # Title
        title = {
            "text": "НАСТРОЙКИ",
            "rect": pygame.Rect(SCREEN_WIDTH//2 - 100, 50, 200, 50),
            "action": None
        }
        self.buttons.append(title)
        
        # Volume settings
        if self.settings_manager:
            # Master volume slider
            master_volume_slider = {
                "text": "Общая громкость",
                "rect": pygame.Rect(100, 150, 300, 30),
                "value": self.settings_manager.settings["master_volume"],
                "min": 0.0,
                "max": 1.0,
                "setting_key": "master_volume"
            }
            self.sliders.append(master_volume_slider)
            
            # Music volume slider
            music_volume_slider = {
                "text": "Громкость музыки",
                "rect": pygame.Rect(100, 200, 300, 30),
                "value": self.settings_manager.settings["music_volume"],
                "min": 0.0,
                "max": 1.0,
                "setting_key": "music_volume"
            }
            self.sliders.append(music_volume_slider)
            
            # SFX volume slider
            sfx_volume_slider = {
                "text": "Громкость звуков",
                "rect": pygame.Rect(100, 250, 300, 30),
                "value": self.settings_manager.settings["sfx_volume"],
                "min": 0.0,
                "max": 1.0,
                "setting_key": "sfx_volume"
            }
            self.sliders.append(sfx_volume_slider)
        
        # Graphics settings
        fullscreen_checkbox = {
            "text": "Полноэкранный режим",
            "rect": pygame.Rect(100, 320, 300, 30),
            "checked": self.settings_manager.settings["fullscreen"] if self.settings_manager else False,
            "setting_key": "fullscreen"
        }
        self.checkboxes.append(fullscreen_checkbox)
        
        show_tips_checkbox = {
            "text": "Показывать советы",
            "rect": pygame.Rect(100, 360, 300, 30),
            "checked": self.settings_manager.settings["show_tips"] if self.settings_manager else True,
            "setting_key": "show_tips"
        }
        self.checkboxes.append(show_tips_checkbox)
        
        auto_save_checkbox = {
            "text": "Автосохранение",
            "rect": pygame.Rect(100, 400, 300, 30),
            "checked": self.settings_manager.settings["auto_save"] if self.settings_manager else True,
            "setting_key": "auto_save"
        }
        self.checkboxes.append(auto_save_checkbox)
        
        # Demo mode button
        demo_button = {
            "text": "ДЕМО РЕЖИМ (10K пользователей)",
            "rect": pygame.Rect(100, 450, 300, 40),
            "action": "demo_mode"
        }
        self.buttons.append(demo_button)
        
        # Back button
        back_button = {
            "text": "НАЗАД",
            "rect": pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 50),
            "action": "back"
        }
        self.buttons.append(back_button)
    
    def handle_events(self):
        """Handle settings screen events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
                
                elif event.key == pygame.K_UP:
                    self.selected_option = max(0, self.selected_option - 1)
                
                elif event.key == pygame.K_DOWN:
                    self.selected_option = min(len(self.buttons) + len(self.sliders) + len(self.checkboxes) - 1, 
                                            self.selected_option + 1)
                
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return self.activate_selected()
                
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.adjust_selected(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                return self.handle_mouse_click(mouse_pos)
        
        return None
    
    def activate_selected(self):
        """Activate the selected option"""
        total_options = len(self.buttons) + len(self.sliders) + len(self.checkboxes)
        
        if self.selected_option < len(self.buttons):
            button = self.buttons[self.selected_option]
            if button["action"] == "back":
                return "back"
            elif button["action"] == "demo_mode":
                return self.activate_demo_mode()
        
        elif self.selected_option < len(self.buttons) + len(self.sliders):
            slider_index = self.selected_option - len(self.buttons)
            slider = self.sliders[slider_index]
            # Toggle slider adjustment mode
            return None
        
        else:
            checkbox_index = self.selected_option - len(self.buttons) - len(self.sliders)
            checkbox = self.checkboxes[checkbox_index]
            checkbox["checked"] = not checkbox["checked"]
            if self.settings_manager:
                self.settings_manager.update_setting(checkbox["setting_key"], checkbox["checked"])
        
        return None
    
    def adjust_selected(self, key):
        """Adjust the selected option value"""
        total_options = len(self.buttons) + len(self.sliders) + len(self.checkboxes)
        
        if self.selected_option < len(self.buttons):
            button = self.buttons[self.selected_option]
            if button["action"] == "demo_mode":
                if key == pygame.K_LEFT or key == pygame.K_RIGHT:
                    return self.activate_demo_mode()
        
        elif self.selected_option < len(self.buttons) + len(self.sliders):
            slider_index = self.selected_option - len(self.buttons)
            slider = self.sliders[slider_index]
            
            if key == pygame.K_LEFT:
                slider["value"] = max(slider["min"], slider["value"] - 0.1)
            elif key == pygame.K_RIGHT:
                slider["value"] = min(slider["max"], slider["value"] + 0.1)
            
            if self.settings_manager:
                self.settings_manager.update_setting(slider["setting_key"], slider["value"])
        
        return None
    
    def activate_demo_mode(self):
        """Activate demo mode with 10K users"""
        # Show confirmation message
        font_medium = pygame.font.Font(None, 32)
        confirm_text = "Демо режим активирован! 10,000 пользователей установлено."
        confirm_surface = font_medium.render(confirm_text, True, GREEN)
        confirm_rect = confirm_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # Draw confirmation
        self.screen.fill(BLACK)
        self.screen.blit(confirm_surface, confirm_rect)
        pygame.display.flip()
        
        # Wait 2 seconds
        pygame.time.wait(2000)
        
        return "demo_activated"
    
    def handle_mouse_click(self, mouse_pos):
        """Handle mouse clicks"""
        # Check buttons
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                if button["action"] == "back":
                    return "back"
                elif button["action"] == "demo_mode":
                    return self.activate_demo_mode()
        
        # Check sliders
        for slider in self.sliders:
            if slider["rect"].collidepoint(mouse_pos):
                # Calculate new value based on mouse position
                relative_x = (mouse_pos[0] - slider["rect"].x) / slider["rect"].width
                new_value = slider["min"] + (slider["max"] - slider["min"]) * relative_x
                slider["value"] = max(slider["min"], min(slider["max"], new_value))
                
                if self.settings_manager:
                    self.settings_manager.update_setting(slider["setting_key"], slider["value"])
        
        # Check checkboxes
        for checkbox in self.checkboxes:
            if checkbox["rect"].collidepoint(mouse_pos):
                checkbox["checked"] = not checkbox["checked"]
                if self.settings_manager:
                    self.settings_manager.update_setting(checkbox["setting_key"], checkbox["checked"])
        
        return None
    
    def draw(self):
        """Draw settings screen"""
        # Background
        self.screen.fill(BLACK)
        
        # Draw title
        title_surface = self.font_large.render("НАСТРОЙКИ", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 75))
        self.screen.blit(title_surface, title_rect)
        
        # Draw sliders
        for i, slider in enumerate(self.sliders):
            self.draw_slider(slider, i + len(self.buttons) == self.selected_option)
        
        # Draw checkboxes
        for i, checkbox in enumerate(self.checkboxes):
            self.draw_checkbox(checkbox, i + len(self.buttons) + len(self.sliders) == self.selected_option)
        
        # Draw buttons
        for i, button in enumerate(self.buttons):
            self.draw_button(button, i == self.selected_option)
        
        # Draw help text
        help_text = "Используйте стрелки для навигации, Enter для выбора"
        help_surface = self.font_small.render(help_text, True, GRAY)
        help_rect = help_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        self.screen.blit(help_surface, help_rect)
        
        pygame.display.flip()
    
    def draw_slider(self, slider, selected):
        """Draw a slider"""
        # Background
        color = YELLOW if selected else WHITE
        pygame.draw.rect(self.screen, color, slider["rect"], 2)
        
        # Text
        text_surface = self.font_medium.render(slider["text"], True, color)
        self.screen.blit(text_surface, (slider["rect"].x, slider["rect"].y - 30))
        
        # Slider fill
        fill_width = int(slider["rect"].width * (slider["value"] - slider["min"]) / (slider["max"] - slider["min"]))
        fill_rect = pygame.Rect(slider["rect"].x, slider["rect"].y, fill_width, slider["rect"].height)
        pygame.draw.rect(self.screen, GREEN, fill_rect)
        
        # Value text
        value_text = f"{int(slider['value'] * 100)}%"
        value_surface = self.font_small.render(value_text, True, color)
        self.screen.blit(value_surface, (slider["rect"].right + 10, slider["rect"].y))
    
    def draw_checkbox(self, checkbox, selected):
        """Draw a checkbox"""
        # Background
        color = YELLOW if selected else WHITE
        pygame.draw.rect(self.screen, color, checkbox["rect"], 2)
        
        # Text
        text_surface = self.font_medium.render(checkbox["text"], True, color)
        self.screen.blit(text_surface, (checkbox["rect"].x, checkbox["rect"].y + 5))
        
        # Checkbox
        checkbox_rect = pygame.Rect(checkbox["rect"].right - 30, checkbox["rect"].y + 5, 20, 20)
        pygame.draw.rect(self.screen, color, checkbox_rect, 2)
        
        if checkbox["checked"]:
            # Draw checkmark
            pygame.draw.line(self.screen, GREEN, 
                           (checkbox_rect.x + 5, checkbox_rect.y + 10),
                           (checkbox_rect.x + 8, checkbox_rect.y + 13), 2)
            pygame.draw.line(self.screen, GREEN,
                           (checkbox_rect.x + 8, checkbox_rect.y + 13),
                           (checkbox_rect.x + 15, checkbox_rect.y + 6), 2)
    
    def draw_button(self, button, selected):
        """Draw a button"""
        color = YELLOW if selected else WHITE
        pygame.draw.rect(self.screen, color, button["rect"], 2)
        
        text_surface = self.font_medium.render(button["text"], True, color)
        text_rect = text_surface.get_rect(center=button["rect"].center)
        self.screen.blit(text_surface, text_rect)
    
    def run(self):
        """Run settings screen"""
        running = True
        while running:
            result = self.handle_events()
            if result == "quit":
                return "quit"
            elif result == "back":
                return "menu"
            
            self.draw()
        
        return "menu" 