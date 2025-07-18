import pygame
from settings import *
from sprite_loader import get_sprite_loader
from PIL import Image
import os
from sound_manager import get_sound_manager

class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Sprite loader for mentor faces
        self.sprite_loader = get_sprite_loader()
        
        # Dialogue system
        self.dialogue_active = False
        self.current_dialogue = []
        self.dialogue_index = 0
        self.npc_name = ""
        
        # Typing animation for dialogue
        self.typing_speed = 0.03  # seconds per character
        self.typing_time = 0
        self.typing_index = 0
        self.typing_active = False
        
        # Quest journal
        self.journal_open = False
        
        # Remove GIF background - use simple dark background instead
        # self.journal_gif_frames = []
        # self.journal_current_frame = 0
        # self.journal_frame_delay = 0.1
        # self.journal_last_frame_time = 0
        # self.load_journal_gif_background()
        
        # GIF background for quest dialogues
        self.quest_gif_frames = []
        self.quest_current_frame = 0
        self.quest_frame_delay = 0.1
        self.quest_last_frame_time = 0
        self.load_quest_gif_background()
        
    def load_journal_gif_background(self):
        """Load GIF background for quest journal"""
        # Removed - using simple dark background instead
        pass
    
    def update_journal_gif_background(self, dt):
        """Update journal GIF animation"""
        # Removed - no longer using GIF background
        pass
    
    def load_quest_gif_background(self):
        """Load GIF background for quest dialogues"""
        try:
            gif_path = "tumblr_owi25v6uAo1r4gsiio1_1280_gif (1000×300).gif"
            print(f"🔍 Ищем GIF файл для квестов: {gif_path}")
            if os.path.exists(gif_path):
                print(f"✅ Файл найден для квестов: {gif_path}")
                # Open GIF with PIL
                gif = Image.open(gif_path)
                
                # Extract frames
                frame_count = getattr(gif, 'n_frames', 1)
                print(f"📊 Количество кадров в GIF для квестов: {frame_count}")
                for frame in range(frame_count):
                    gif.seek(frame)
                    # Convert PIL image to pygame surface
                    frame_surface = pygame.image.fromstring(gif.convert('RGBA').tobytes(), gif.size, 'RGBA')
                    
                    # Scale to fit dialogue box size
                    frame_surface = pygame.transform.scale(frame_surface, (SCREEN_WIDTH - 100, 150))
                    
                    # Add dark overlay for better text visibility
                    overlay = pygame.Surface((SCREEN_WIDTH - 100, 150))
                    overlay.set_alpha(100)
                    overlay.fill((0, 0, 0))
                    frame_surface.blit(overlay, (0, 0))
                    
                    self.quest_gif_frames.append(frame_surface)
                
                print(f"✅ Загружено {len(self.quest_gif_frames)} кадров GIF-фона для квестов")
            else:
                print(f"⚠️ GIF файл не найден для квестов: {gif_path}")
        except Exception as e:
            print(f"❌ Ошибка загрузки GIF для квестов: {e}")
    
    def update_quest_gif_background(self, dt):
        """Update quest GIF animation"""
        if self.quest_gif_frames:
            self.quest_last_frame_time += dt
            if self.quest_last_frame_time >= self.quest_frame_delay:
                self.quest_current_frame = (self.quest_current_frame + 1) % len(self.quest_gif_frames)
                self.quest_last_frame_time = 0
    
    def display_hud(self, screen, player):
        """Display HUD with user count and current quest"""
        # User counter (top-left)
        user_text = f"Пользователи: {player.current_users}/{TARGET_USERS}"
        user_surface = self.font_medium.render(user_text, True, WHITE)
        screen.blit(user_surface, (10, 10))
        
        # Progress bar
        progress_width = 200
        progress_height = 20
        progress_rect = pygame.Rect(10, 40, progress_width, progress_height)
        pygame.draw.rect(screen, GRAY, progress_rect)
        
        # Fill progress bar
        progress = player.current_users / TARGET_USERS
        fill_width = int(progress_width * progress)
        fill_rect = pygame.Rect(10, 40, fill_width, progress_height)
        pygame.draw.rect(screen, GREEN, fill_rect)
        
        # Current quest (top-right)
        if player.quest_log:
            current_quest = player.quest_log[0] if player.quest_log else None
            if current_quest:
                quest_text = f"Текущий квест: {current_quest}"
                quest_surface = self.font_small.render(quest_text, True, WHITE)
                quest_rect = quest_surface.get_rect()
                quest_rect.topright = (SCREEN_WIDTH - 10, 10)
                screen.blit(quest_surface, quest_rect)
        
        # Controls hint
        # controls_text = "WASD - движение, E - взаимодействие, Q - журнал"
        # controls_surface = self.font_small.render(controls_text, True, WHITE)
        # controls_rect = controls_surface.get_rect()
        # controls_rect.bottomleft = (10, SCREEN_HEIGHT - 10)
        # screen.blit(controls_surface, controls_rect)
    
    def start_dialogue(self, dialogue_lines, npc_name):
        """Start dialogue sequence"""
        self.dialogue_active = True
        self.current_dialogue = dialogue_lines
        self.dialogue_index = 0
        self.npc_name = npc_name
        self.typing_active = True
        self.typing_index = 0  # Начинаем с пустого текста
        self.typing_time = 0
        
        # Play dialogue start sound
        sound_manager = get_sound_manager()
        if sound_manager:
            sound_manager.play_interaction()
        
        print(f"🎬 Начинаем диалог с {npc_name}: текст будет появляться по буквам")
    
    def next_dialogue_line(self):
        """Move to next dialogue line"""
        if self.typing_active:
            # Skip typing animation
            self.typing_active = False
            self.typing_index = len(self.current_dialogue[self.dialogue_index])
        else:
            # Move to next line
            self.dialogue_index += 1
            if self.dialogue_index >= len(self.current_dialogue):
                self.end_dialogue()
                return True  # Dialogue finished
            else:
                # Start typing animation for next line
                self.typing_active = True
                self.typing_index = 0
                self.typing_time = 0
        return False
    
    def end_dialogue(self):
        """End dialogue"""
        self.dialogue_active = False
        self.current_dialogue = []
        self.dialogue_index = 0
        self.npc_name = ""
        self.typing_active = False
        self.typing_index = 0
    
    def update_typing_animation(self, dt):
        """Update typing animation"""
        if self.typing_active and self.dialogue_active:
            self.typing_time += dt
            if self.typing_time >= self.typing_speed:
                self.typing_index += 1
                self.typing_time = 0
                
                current_text = self.current_dialogue[self.dialogue_index]
                if self.typing_index >= len(current_text):
                    self.typing_active = False
                    print(f"✅ Анимация текста завершена для: {current_text[:30]}...")
    
    def display_dialogue(self, screen):
        """Display dialogue box"""
        if not self.dialogue_active or not self.current_dialogue:
            return
            
        # Dialogue box
        box_height = 150
        box_rect = pygame.Rect(50, SCREEN_HEIGHT - box_height - 50, 
                              SCREEN_WIDTH - 100, box_height)
        
        # Draw dialogue background - use only regular background for all dialogues
        dialogue_surface = pygame.Surface((box_rect.width, box_rect.height))
        dialogue_surface.set_alpha(230)
        dialogue_surface.fill(DIALOGUE_BG_COLOR[:3])
        screen.blit(dialogue_surface, box_rect.topleft)
        
        # Draw border
        pygame.draw.rect(screen, UI_BORDER_COLOR, box_rect, 3)
        
        # NPC name and face
        name_surface = self.font_medium.render(self.npc_name, True, YELLOW)
        
        # Show mentor face if available
        mentor_face = self.sprite_loader.get_mentor_face(self.npc_name)
        if mentor_face:
            # Draw mentor face on the left with proper spacing
            face_x = box_rect.x + 20
            face_y = box_rect.y + 20
            screen.blit(mentor_face, (face_x, face_y))
            # Adjust name position to avoid overlap - move it down
            name_x = face_x + mentor_face.get_width() + 20
            screen.blit(name_surface, (name_x, box_rect.y + 20))
        else:
            screen.blit(name_surface, (box_rect.x + 20, box_rect.y + 20))
        
        # Dialogue text - start below the name and face
        if self.dialogue_index < len(self.current_dialogue):
            dialogue_text = self.current_dialogue[self.dialogue_index]
            
            # Apply typing animation - start with empty text
            if self.typing_active and self.typing_index < len(dialogue_text):
                display_text = dialogue_text[:self.typing_index]
            else:
                display_text = dialogue_text
            
            # Calculate text start position
            if mentor_face:
                text_start_x = face_x + mentor_face.get_width() + 20
                text_start_y = box_rect.y + 50  # Below the name
            else:
                text_start_x = box_rect.x + 20
                text_start_y = box_rect.y + 50  # Below the name
            
            # Word wrap dialogue text
            words = display_text.split(' ')
            lines = []
            current_line = ""
            
            # Calculate max width for text
            max_text_width = box_rect.width - (text_start_x - box_rect.x) - 40
            
            for word in words:
                test_line = current_line + word + " "
                test_surface = self.font_medium.render(test_line, True, WHITE)  # Use medium font instead of small
                if test_surface.get_width() > max_text_width:
                    if current_line:
                        lines.append(current_line.strip())
                        current_line = word + " "
                    else:
                        lines.append(word)
                        current_line = ""
                else:
                    current_line = test_line
            
            if current_line:
                lines.append(current_line.strip())
            
            # Display lines
            y_offset = text_start_y
            for line in lines:
                line_surface = self.font_medium.render(line, True, WHITE)  # Use medium font instead of small
                screen.blit(line_surface, (text_start_x, y_offset))
                y_offset += 30  # Increased line spacing
        
        # Continue indicator
        continue_text = "Нажмите E для продолжения..."
        continue_surface = self.font_small.render(continue_text, True, GRAY)
        continue_rect = continue_surface.get_rect()
        continue_rect.bottomright = (box_rect.right - 20, box_rect.bottom - 10)
        screen.blit(continue_surface, continue_rect)
    
    def toggle_journal(self):
        """Toggle quest journal"""
        self.journal_open = not self.journal_open
        
        # Play journal toggle sound
        sound_manager = get_sound_manager()
        if sound_manager:
            sound_manager.play_button_click()
    
    def display_journal(self, screen, player, quest_manager):
        """Display quest journal with beautiful design"""
        if not self.journal_open:
            return
            
        # Journal background with simple dark background
        journal_width = 500
        journal_height = 600
        journal_rect = pygame.Rect(
            (SCREEN_WIDTH - journal_width) // 2,
            (SCREEN_HEIGHT - journal_height) // 2,
            journal_width, journal_height
        )
        
        # Simple dark background instead of GIF
        journal_surface = pygame.Surface((journal_width, journal_height))
        journal_surface.set_alpha(250)
        journal_surface.fill((20, 30, 50))  # Dark blue background
        screen.blit(journal_surface, journal_rect.topleft)
        
        # Beautiful border with glow effect
        border_color = (100, 150, 255)
        pygame.draw.rect(screen, border_color, journal_rect, 4)
        
        # Inner border for depth
        inner_rect = journal_rect.inflate(-8, -8)
        pygame.draw.rect(screen, (60, 100, 180), inner_rect, 2)
        
        # Title with shadow effect
        title_text = "📖 Журнал Квестов"
        title_surface = self.font_large.render(title_text, True, (255, 255, 200))
        title_shadow = self.font_large.render(title_text, True, (100, 100, 100))
        
        title_rect = title_surface.get_rect()
        title_rect.centerx = journal_rect.centerx
        title_rect.y = journal_rect.y + 25
        
        # Draw shadow first
        shadow_rect = title_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        screen.blit(title_shadow, shadow_rect)
        screen.blit(title_surface, title_rect)
        
        # Decorative line under title
        line_y = title_rect.bottom + 15
        pygame.draw.line(screen, (150, 200, 255), 
                        (journal_rect.x + 50, line_y), 
                        (journal_rect.right - 50, line_y), 3)
        
        # Active quests section
        quest_y = line_y + 30
        quest_title = "🎯 Активные Квесты"
        quest_title_surface = self.font_medium.render(quest_title, True, (255, 220, 150))
        screen.blit(quest_title_surface, (journal_rect.x + 30, quest_y))
        quest_y += 40
        
        if player.quest_log:
            for i, quest_id in enumerate(player.quest_log):
                quest_data = quest_manager.get_quest_data(quest_id)
                if quest_data:
                    quest_title = quest_data.get("title", quest_id)
                    mentor_name = quest_data.get("npc_id", "")
                    
                    # Quest background
                    quest_bg_rect = pygame.Rect(journal_rect.x + 20, quest_y - 5, 
                                              journal_width - 40, 50)  # Increased height for mentor face
                    quest_bg_surface = pygame.Surface((quest_bg_rect.width, quest_bg_rect.height))
                    quest_bg_surface.set_alpha(100)
                    quest_bg_surface.fill((100, 150, 255))
                    screen.blit(quest_bg_surface, quest_bg_rect.topleft)
                    
                    # Show mentor face if available
                    mentor_face = self.sprite_loader.get_mentor_face(mentor_name)
                    if mentor_face:
                        # Scale mentor face to fit in quest item
                        scaled_face = pygame.transform.scale(mentor_face, (40, 40))
                        face_x = journal_rect.x + 25
                        face_y = quest_y
                        screen.blit(scaled_face, (face_x, face_y))
                        
                        # Quest text with mentor face
                        quest_icon = "⚡" if "swift" in quest_id.lower() else "🤖" if "ai" in quest_id.lower() else "📝"
                        quest_text = f"{quest_icon} {quest_title}"
                        quest_surface = self.font_medium.render(quest_text, True, (255, 255, 255))
                        screen.blit(quest_surface, (face_x + 50, quest_y + 10))  # Offset for face
                        
                        # Mentor name below
                        mentor_surface = self.font_small.render(f"от {mentor_name}", True, (200, 200, 255))
                        screen.blit(mentor_surface, (face_x + 50, quest_y + 30))
                    else:
                        # Quest text without mentor face
                        quest_icon = "⚡" if "swift" in quest_id.lower() else "🤖" if "ai" in quest_id.lower() else "📝"
                        quest_text = f"{quest_icon} {quest_title}"
                        quest_surface = self.font_medium.render(quest_text, True, (255, 255, 255))
                        screen.blit(quest_surface, (journal_rect.x + 30, quest_y + 10))
                    
                    quest_y += 60  # Increased spacing for mentor face
        else:
            no_quests_surface = self.font_medium.render("📭 Нет активных квестов", True, (150, 150, 150))
            screen.blit(no_quests_surface, (journal_rect.x + 30, quest_y))
            quest_y += 40
        
        # Inventory section
        inv_y = quest_y + 20
        inventory_title = "🎒 Инвентарь"
        inventory_title_surface = self.font_medium.render(inventory_title, True, (255, 220, 150))
        screen.blit(inventory_title_surface, (journal_rect.x + 30, inv_y))
        inv_y += 40
        
        if player.inventory:
            for item, count in player.inventory.items():
                # Item background
                item_bg_rect = pygame.Rect(journal_rect.x + 20, inv_y - 5, 
                                         journal_width - 40, 30)
                item_bg_surface = pygame.Surface((item_bg_rect.width, item_bg_rect.height))
                item_bg_surface.set_alpha(80)
                item_bg_surface.fill((50, 150, 50))
                screen.blit(item_bg_surface, item_bg_rect.topleft)
                
                # Item icon and text
                item_icon = "💧" if "water" in item.lower() else "📦"
                item_text = f"{item_icon} {item} x{count}"
                item_surface = self.font_small.render(item_text, True, (200, 255, 200))
                screen.blit(item_surface, (journal_rect.x + 30, inv_y))
                inv_y += 35
        else:
            empty_inv_surface = self.font_small.render("📭 Инвентарь пуст", True, (150, 150, 150))
            screen.blit(empty_inv_surface, (journal_rect.x + 30, inv_y))
            inv_y += 35
        
        # Stats section
        stats_y = inv_y + 20
        stats_title = "📊 Статистика"
        stats_title_surface = self.font_medium.render(stats_title, True, (255, 220, 150))
        screen.blit(stats_title_surface, (journal_rect.x + 30, stats_y))
        stats_y += 40
        
        # User progress
        progress_text = f"👥 Пользователи: {player.current_users}/{TARGET_USERS}"
        progress_surface = self.font_small.render(progress_text, True, (200, 255, 200))
        screen.blit(progress_surface, (journal_rect.x + 30, stats_y))
        
        # Progress bar
        bar_width = journal_width - 60
        bar_height = 15
        bar_rect = pygame.Rect(journal_rect.x + 30, stats_y + 25, bar_width, bar_height)
        pygame.draw.rect(screen, (100, 100, 100), bar_rect)
        
        progress = player.current_users / TARGET_USERS
        fill_width = int(bar_width * progress)
        if fill_width > 0:
            fill_rect = pygame.Rect(journal_rect.x + 30, stats_y + 25, fill_width, bar_height)
            pygame.draw.rect(screen, (100, 255, 100), fill_rect)
        
        # Close instruction with glow
        close_text = "💡 Нажмите Q для закрытия"
        close_surface = self.font_small.render(close_text, True, (255, 255, 200))
        close_rect = close_surface.get_rect()
        close_rect.centerx = journal_rect.centerx
        close_rect.bottom = journal_rect.bottom - 25
        screen.blit(close_surface, close_rect) 