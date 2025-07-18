import pygame
import random
import os
from settings import *

class MentorLocation:
    def __init__(self, mentor_name, specialty):
        self.mentor_name = mentor_name
        self.specialty = specialty
        self.background = self.load_mentor_background()
        self.mentor_sprite = None
        self.load_mentor_sprite()
        
        # Player position in mentor location - start away from mentor
        self.player_x = 100  # Start on the left side
        self.player_y = SCREEN_HEIGHT // 2
        
        # Movement bounds (allow player to reach mentor)
        self.min_x = 50
        self.max_x = SCREEN_WIDTH - 100  # Allow player to get closer to mentor
        self.min_y = 50
        self.max_y = SCREEN_HEIGHT - 50
        
        # Mentor position (random placement)
        self.mentor_x = random.randint(200, SCREEN_WIDTH - 200)
        self.mentor_y = random.randint(100, SCREEN_HEIGHT - 200)
    
    def load_mentor_background(self):
        """Load individual background for each mentor"""
        locations_path = "Base and Full Map + HD Images/locations/"
        
        # Map mentors to specific background images
        mentor_backgrounds = {
            "Alikhan": "download.jpg",  # iOS developer
            "Alibeck": "download (1).jpg",  # AI/ML
            "Bahredin": "download (2).jpg",  # TypeScript
            "Bahaudin": "download (3).jpg",  # Backend
            "Gaziz": "Fantastic Buildings_ Modern.jpg",  # Frontend
            "Shoqan": "smockup_0.jpg",  # Mobile
            "Zhasulan": "d7c191ec41394bd18a55762e78961873.jpg",  # iOS
            "Aimurat": "download.jpg",  # AI/ML (reuse)
            "Bernar": "Fantastic Buildings_ Modern.jpg"  # BOSS (reuse)
        }
        
        background_file = mentor_backgrounds.get(self.mentor_name, "download.jpg")
        background_path = os.path.join(locations_path, background_file)
        
        try:
            if os.path.exists(background_path):
                background = pygame.image.load(background_path)
                # Scale to fit screen
                bg_w, bg_h = background.get_size()
                scale = max(SCREEN_WIDTH / bg_w, SCREEN_HEIGHT / bg_h)
                new_w, new_h = int(bg_w * scale), int(bg_h * scale)
                scaled_bg = pygame.transform.scale(background, (new_w, new_h))
                
                # Create surface and center the background
                surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                surf.blit(scaled_bg, ((SCREEN_WIDTH - new_w) // 2, (SCREEN_HEIGHT - new_h) // 2))
                print(f"✅ Загружен фон для {self.mentor_name}: {background_file}")
                return surf
            else:
                print(f"⚠️ Файл фона не найден: {background_path}")
        except Exception as e:
            print(f"❌ Ошибка загрузки фона для {self.mentor_name}: {e}")
        
        # Fallback to galletcity background
        return self.load_galletcity_background()
    
    def load_galletcity_background(self):
        try:
            from sprite_loader import get_sprite_loader
            sprite_loader = get_sprite_loader()
            background = sprite_loader.get_background("galletcity")
            if background:
                # Cover mode: fill the screen, crop excess
                bg_w, bg_h = background.get_size()
                scale = max(SCREEN_WIDTH / bg_w, SCREEN_HEIGHT / bg_h)
                new_w, new_h = int(bg_w * scale), int(bg_h * scale)
                scaled_bg = pygame.transform.scale(background, (new_w, new_h))
                surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                surf.blit(scaled_bg, ((SCREEN_WIDTH - new_w) // 2, (SCREEN_HEIGHT - new_h) // 2))
                return surf
        except Exception as e:
            print(f"Error loading galletcity background: {e}")
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg.fill((100, 150, 200))
        return bg
    
    def load_mentor_sprite(self):
        """Load mentor-specific sprite"""
        try:
            from sprite_loader import get_sprite_loader
            sprite_loader = get_sprite_loader()
            
            # Try to load mentor face first
            self.mentor_sprite = sprite_loader.get_mentor_face(self.mentor_name)
            if self.mentor_sprite:
                # Scale to appropriate size for location display
                self.mentor_sprite = pygame.transform.scale(self.mentor_sprite, (120, 120))
                print(f"Loaded mentor sprite for {self.mentor_name}")
            else:
                print(f"Failed to load mentor sprite for {self.mentor_name}")
                # Create a better fallback sprite
                self.create_fallback_mentor_sprite()
        except Exception as e:
            print(f"Error loading mentor sprite: {e}")
            self.create_fallback_mentor_sprite()
    
    def create_fallback_mentor_sprite(self):
        """Create a better fallback sprite for mentor"""
        self.mentor_sprite = pygame.Surface((120, 120), pygame.SRCALPHA)
        
        # Draw a more detailed fallback sprite
        # Body
        pygame.draw.rect(self.mentor_sprite, (100, 150, 255), (40, 60, 40, 50))
        # Head
        pygame.draw.circle(self.mentor_sprite, (255, 220, 180), (60, 40), 25)
        # Eyes
        pygame.draw.circle(self.mentor_sprite, (0, 0, 0), (55, 35), 3)
        pygame.draw.circle(self.mentor_sprite, (0, 0, 0), (65, 35), 3)
        # Mouth
        pygame.draw.arc(self.mentor_sprite, (0, 0, 0), (55, 45, 10, 8), 0, 3.14, 2)
        # Arms
        pygame.draw.rect(self.mentor_sprite, (100, 150, 255), (30, 70, 8, 25))
        pygame.draw.rect(self.mentor_sprite, (100, 150, 255), (82, 70, 8, 25))
    
    def update_player_position(self, dx, dy):
        """Update player position with bounds checking"""
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        
        # Keep player within bounds
        if self.min_x <= new_x <= self.max_x:
            self.player_x = new_x
        if self.min_y <= new_y <= self.max_y:
            self.player_y = new_y
    
    def get_player_position(self):
        """Get current player position"""
        return (self.player_x, self.player_y)
    
    def check_mentor_interaction(self, player_pos):
        """Check if player is close enough to interact with mentor"""
        # Use fixed mentor position
        mentor_center_x = self.mentor_x + 60  # Center of mentor sprite
        mentor_center_y = self.mentor_y + 60
        
        distance = ((player_pos[0] - mentor_center_x) ** 2 + (player_pos[1] - mentor_center_y) ** 2) ** 0.5
        return distance < 80  # Interaction radius - увеличен для удобства
    
    def draw(self, screen, player=None):
        """Draw the mentor location with galletcity background and player"""
        # Draw galletcity background
        screen.blit(self.background, (0, 0))
        
        # Draw mentor sprite (larger, like on main map) - fixed position on right
        if self.mentor_sprite:
            # Use fixed mentor position
            large_mentor = pygame.transform.scale(self.mentor_sprite, (120, 120))
            screen.blit(large_mentor, (self.mentor_x, self.mentor_y))
        
        # Draw player if provided - use actual position from mentor location
        if player:
            # Use the stored position in mentor location, not player's global position
            player.draw_at_position(screen, (self.player_x, self.player_y))
        
        # Draw mentor name with shadow for better visibility
        font_large = pygame.font.Font(None, 48)
        name_text = font_large.render(self.mentor_name, True, (255, 255, 255))
        name_shadow = font_large.render(self.mentor_name, True, (0, 0, 0))
        name_rect = name_text.get_rect(center=(self.mentor_x + 60, self.mentor_y - 40))
        
        # Draw shadow first
        shadow_rect = name_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        screen.blit(name_shadow, shadow_rect)
        screen.blit(name_text, name_rect)
        
        # Draw specialty with shadow
        font_medium = pygame.font.Font(None, 32)
        specialty_text = font_medium.render(f"Специализация: {self.specialty}", True, (255, 255, 255))
        specialty_shadow = font_medium.render(f"Специализация: {self.specialty}", True, (0, 0, 0))
        specialty_rect = specialty_text.get_rect(center=(self.mentor_x + 60, self.mentor_y - 10))
        
        # Draw shadow first
        shadow_rect = specialty_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        screen.blit(specialty_shadow, shadow_rect)
        screen.blit(specialty_text, specialty_rect)
        
        # Draw instructions
        font_medium = pygame.font.Font(None, 28)  # Increased font size
        instructions = [
            "WASD - движение",
            "Нажми E для взаимодействия",
            "Нажми ESC для возврата на карту"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = font_medium.render(instruction, True, (255, 255, 255))
            inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100 + i * 30))  # Increased spacing
            screen.blit(inst_text, inst_rect)

class MentorLocationManager:
    def __init__(self):
        self.locations = {}
        self.current_location = None
        self.create_locations()
    
    def create_locations(self):
        """Create locations for all mentors"""
        mentors = [
            ("Alikhan", "iOS"),
            ("Alibeck", "AI/ML"),
            ("Bahredin", "TypeScript"),
            ("Bahaudin", "Backend"),
            ("Gaziz", "Frontend"),
            ("Shoqan", "Frontend"),  # Fixed: changed from Mobile to Frontend
            ("Zhasulan", "iOS"),
            ("Aimurat", "AI/ML"),
            ("Bernar", "BOSS"),
            ("Diana", "Frontend"),  # Added Diana mentor
            ("Tamyrlan", "Backend")  # Added Tamyrlan mentor
        ]
        
        print("Creating mentor locations...")
        for mentor_name, specialty in mentors:
            print(f"Creating location for {mentor_name} ({specialty})")
            self.locations[mentor_name] = MentorLocation(mentor_name, specialty)
        print("Mentor locations created!")
    
    def enter_location(self, mentor_name):
        """Enter mentor's personal location"""
        if mentor_name in self.locations:
            self.current_location = self.locations[mentor_name]
            return True
        return False
    
    def exit_location(self):
        """Exit current location"""
        self.current_location = None
    
    def get_current_location(self):
        """Get current location"""
        return self.current_location
    
    def update_player_movement(self, dx, dy):
        """Update player movement in current location"""
        if self.current_location:
            self.current_location.update_player_position(dx, dy)
    
    def get_player_position(self):
        """Get player position in current location"""
        if self.current_location:
            return self.current_location.get_player_position()
        return (0, 0)
    
    def check_mentor_interaction(self):
        """Check if player can interact with mentor"""
        if self.current_location:
            return self.current_location.check_mentor_interaction(self.current_location.get_player_position())
        return False
    
    def draw_current_location(self, screen, player=None):
        """Draw current location"""
        if self.current_location:
            self.current_location.draw(screen, player) 