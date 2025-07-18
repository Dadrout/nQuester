import pygame
import os
from settings import *
from sprite_loader import get_sprite_loader

class NPC:
    def __init__(self, x, y, name, npc_type="student"):
        self.position = pygame.math.Vector2(x, y)
        self.name = name
        self.npc_type = npc_type
        
        # Load sprite
        self.sprite_loader = get_sprite_loader()
        self.load_sprite()
        
        # Ensure image exists
        if self.image is None:
            self.image = pygame.Surface((TILE_SIZE * 2, TILE_SIZE * 2))
            self.image.fill(RED if npc_type == "mentor" else YELLOW)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Quest related
        self.has_quest = False
        self.quest_id = None
        self.dialogue = []
        self.quest_completed = False
        self.quest_failed = False  # Track if quest was failed
        
        # Interaction
        self.interaction_range = 50
        self.show_quest_marker = False
        
    def load_sprite(self):
        """Load NPC sprite from mentors folder or create placeholder"""
        try:
            if self.npc_type == "mentor":
                # Use PNG photos from Mentors folder for mentors on map
                mentor_photo_path = os.path.join("Mentors", f"{self.name}.png")
                if os.path.exists(mentor_photo_path):
                    # Load mentor photo and scale to appropriate size for map
                    mentor_photo = pygame.image.load(mentor_photo_path)
                    # Scale to 64x64 pixels for map display
                    self.image = pygame.transform.scale(mentor_photo, (64, 64))
                    print(f"✅ Загружена фотография ментора {self.name}")
                else:
                    # Fallback to colored rectangle if photo not found
                    self.image = pygame.Surface((TILE_SIZE * 2, TILE_SIZE * 2))
                    self.image.fill(GREEN)
                    print(f"⚠️ Фотография не найдена для {self.name}: {mentor_photo_path}")
            elif self.npc_type == "boss":
                # Load boss sprite
                boss_photo_path = os.path.join("Mentors", "main_boss.jpg")
                if os.path.exists(boss_photo_path):
                    # Load boss photo and scale to appropriate size for map
                    boss_photo = pygame.image.load(boss_photo_path)
                    # Scale to 80x80 pixels for boss display (larger than mentors)
                    self.image = pygame.transform.scale(boss_photo, (80, 80))
                    print(f"✅ Загружен спрайт босса {self.name}")
                else:
                    # Fallback to colored rectangle if photo not found
                    self.image = pygame.Surface((TILE_SIZE * 2, TILE_SIZE * 2))
                    self.image.fill(RED)
                    print(f"⚠️ Фотография босса не найдена: {boss_photo_path}")
            else:
                # Student NPC - use character sprites
                characters = ["alex", "amelia", "bob"]  # Разные персонажи для студентов
                char_index = hash(self.name) % len(characters)
                char_name = characters[char_index]
                
                self.image = self.sprite_loader.get_npc_sprite(char_name)
                if self.image is None:
                    self.image = pygame.Surface((TILE_SIZE * 2, TILE_SIZE * 2))
                    self.image.fill(YELLOW)
        except (pygame.error, OSError) as e:
            print(f"Error loading sprite for {self.name}: {e}")
            # Fallback sprite
            self.image = pygame.Surface((TILE_SIZE * 2, TILE_SIZE * 2))
            self.image.fill(RED if self.npc_type == "mentor" else YELLOW)
    
    def set_quest(self, quest_id, dialogue, user_reward=0):
        """Set quest for this NPC"""
        self.quest_id = quest_id
        self.dialogue = dialogue
        self.has_quest = True
        self.show_quest_marker = True
        self.user_reward = user_reward

    def can_interact(self, player_pos):
        """Check if player is in interaction range"""
        distance = self.position.distance_to(player_pos)
        return distance <= self.interaction_range
    
    def interact(self):
        """Start interaction with NPC (with humor)"""
        if self.has_quest and not self.quest_completed:
            funny_lines = [
                "Я бы сам сделал, но у меня дедлайн...",
                "Говорят, если выполнить этот квест, появится баг в проде!",
                "Помоги, а то меня уволят в понедельник!",
                "Если справишься — куплю тебе кофе!",
                "Сделаешь — расскажу секретный лайфхак!",
                "Если не получится — скажем, что это фича!",
                "Выполнишь — получишь +100 к карме!",
                "Я уже три дня не спал, помоги!",
                "Если что — я тебя не знаю!",
                "Выполнишь — расскажу, как пройти собес в Google!"
            ]
            import random
            dialogue = self.dialogue + [random.choice(funny_lines)]
            return {
                'type': 'quest_start',
                'quest_id': self.quest_id,
                'dialogue': dialogue,
                'npc_name': self.name
            }
        elif self.has_quest and self.quest_failed:
            # Allow retry after failure with encouraging messages
            retry_messages = [
                "Не сдавайся! Попробуй еще раз!",
                "Ты можешь это сделать! Попробуй снова!",
                "Ошибки помогают учиться! Попробуй еще раз!",
                "Практика делает мастера! Попробуй снова!"
            ]
            import random
            retry_message = random.choice(retry_messages)
            return {
                'type': 'quest_start',
                'quest_id': self.quest_id,
                'dialogue': [retry_message],
                'npc_name': self.name
            }
        else:
            # Different student dialogues based on name
            if "tired" in self.name.lower():
                if self.quest_completed:
                    dialogue = ["Спасибо за воду! Теперь чувствую себя лучше!"]
                else:
                    dialogue = ["Уфф... Так устал... Нужен кофе..."]
            elif "coding" in self.name.lower():
                if self.quest_completed:
                    dialogue = ["Код стал намного чище! Спасибо!"]
                else:
                    dialogue = ["Код пишу, баги ловлю... Обычный день!"]
            elif "coffee" in self.name.lower():
                if self.quest_completed:
                    dialogue = ["Кофе и код - лучшая комбинация!"]
                else:
                    dialogue = ["Кофе - лучший друг программиста!"]
            else:
                if self.quest_completed:
                    dialogue = ["Спасибо за помощь! Все работает отлично!"]
                else:
                    dialogue = ["Привет! Как дела?"]
            
            return {
                'type': 'dialogue',
                'dialogue': dialogue,
                'npc_name': self.name
            }
    
    def complete_quest(self, player=None):
        """Mark quest as completed and give reward"""
        self.quest_completed = True
        self.show_quest_marker = False
        if player and hasattr(self, 'user_reward'):
            player.current_users += self.user_reward
    
    def fail_quest(self):
        """Mark quest as failed (allows retry)"""
        self.quest_failed = True
        self.show_quest_marker = True  # Show marker again for retry
    
    def draw(self, screen, camera_offset):
        """Draw NPC and quest marker"""
        draw_pos = self.rect.topleft - camera_offset
        screen.blit(self.image, draw_pos)
        
        # Draw name above NPC
        font = pygame.font.Font(None, 20)
        name_text = font.render(self.name, True, WHITE)
        name_rect = name_text.get_rect()
        name_rect.centerx = draw_pos[0] + self.rect.width // 2
        name_rect.bottom = draw_pos[1] - 5
        
        # Draw background for name
        name_bg = pygame.Surface((name_rect.width + 10, name_rect.height + 4))
        name_bg.set_alpha(180)
        name_bg.fill(BLACK)
        name_bg_rect = name_bg.get_rect(center=name_rect.center)
        screen.blit(name_bg, name_bg_rect)
        
        # Draw name
        screen.blit(name_text, name_rect)
        
        # Draw quest marker
        if self.show_quest_marker:
            marker_pos = (draw_pos[0] + self.rect.width // 2 - 12, draw_pos[1] - 24)
            try:
                marker_img = pygame.image.load("data/sprites/icon_quest.png")
                marker_img = pygame.transform.scale(marker_img, (24, 24))
                screen.blit(marker_img, marker_pos)
            except:
                pygame.draw.circle(screen, YELLOW, marker_pos, 8)
                font = pygame.font.Font(None, 24)
                text = font.render("!", True, BLACK)
                text_rect = text.get_rect(center=marker_pos)
                screen.blit(text, text_rect)

class MentorNPC(NPC):
    def __init__(self, x, y, name, specialty):
        super().__init__(x, y, name, "mentor")
        self.specialty = specialty

class StudentNPC(NPC):
    def __init__(self, x, y, name, status="active"):
        super().__init__(x, y, name, "student")
        self.status = status  # active, tired, coding, etc. 