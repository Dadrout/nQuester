import pygame
import math
from settings import *
from sprite_loader import get_sprite_loader
from sound_manager import get_sound_manager

class Player:
    def __init__(self, x, y):
        # Position and movement
        self.position = pygame.math.Vector2(x, y)
        self.speed = PLAYER_SPEED
        self.direction = pygame.math.Vector2()
        self.facing_direction = "down"  # Направление, куда смотрит игрок
        
        # Load player sprite from new assets
        self.sprite_loader = get_sprite_loader()
        self.image = self.sprite_loader.get_player_sprite("idle")
        
        if self.image is None:
            # Fallback
            self.image = pygame.Surface((32, 32))
            self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Player stats
        self.current_users = 0
        self.quest_log = []
        self.inventory = {}
        
        # Animation
        self.animation_speed = ANIMATION_SPEED
        self.animation_time = 0
        
        # States
        self.interacting = False
        
        # Sound effects
        self.last_footstep_time = 0
        self.footstep_interval = 300  # milliseconds
        self.was_moving = False
        
    def get_input(self):
        """Handle player input for movement and interaction"""
        keys = pygame.key.get_pressed()
        
        # Movement
        self.direction.x = 0
        self.direction.y = 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
            self.facing_direction = "up"
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.facing_direction = "down"
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_direction = "left"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_direction = "right"
            
        # Normalize diagonal movement
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
    
    def update(self, dt):
        """Update player position and animation"""
        self.get_input()
        
        # Update position
        self.position += self.direction * self.speed
        self.rect.center = (int(self.position.x), int(self.position.y))
        
        # Handle footstep sounds
        is_moving = self.direction.magnitude() > 0
        current_time = pygame.time.get_ticks()
        
        if is_moving and not self.was_moving:
            # Started moving
            self.was_moving = True
        elif is_moving and self.was_moving:
            # Continue moving - play footstep sound periodically
            if current_time - self.last_footstep_time > self.footstep_interval:
                sound_manager = get_sound_manager()
                if sound_manager:
                    sound_manager.play_footstep()
                self.last_footstep_time = current_time
        elif not is_moving and self.was_moving:
            # Stopped moving
            self.was_moving = False
        
        # Update animation - use idle by default, walk only when moving
        if is_moving:
            self.animation_time += dt
            # Use walking sprite with animation and direction
            frame = int(self.animation_time * 8) % 4  # 8 FPS animation
            walk_sprite = self.sprite_loader.get_player_sprite("walk", frame, self.facing_direction)
            if walk_sprite:
                self.image = walk_sprite
            else:
                print(f"❌ Не удалось загрузить спрайт для направления: {self.facing_direction}, кадр: {frame}")
        else:
            # Используем первый кадр из анимации текущего направления (mc)
            idle_sprite = None
            if self.facing_direction in self.sprite_loader.player_walk_animations:
                idle_sprite = self.sprite_loader.player_walk_animations[self.facing_direction][0]
            if not idle_sprite:
                idle_sprite = self.sprite_loader.get_player_sprite("idle")
            if idle_sprite:
                self.image = idle_sprite
    
    def add_users(self, amount):
        """Add users to player's count"""
        self.current_users += amount
        if self.current_users > TARGET_USERS:
            self.current_users = TARGET_USERS
    
    def add_item(self, item_name):
        """Add item to inventory"""
        if item_name in self.inventory:
            self.inventory[item_name] += 1
        else:
            self.inventory[item_name] = 1
    
    def has_item(self, item_name):
        """Check if player has item"""
        return item_name in self.inventory and self.inventory[item_name] > 0
    
    def remove_item(self, item_name):
        """Remove item from inventory"""
        if self.has_item(item_name):
            self.inventory[item_name] -= 1
            if self.inventory[item_name] <= 0:
                del self.inventory[item_name]
    
    def draw(self, screen, camera_offset):
        """Draw player relative to camera"""
        draw_pos = self.rect.topleft - camera_offset
        screen.blit(self.image, draw_pos) 
    
    def draw_at_position(self, screen, position):
        """Draw player at specific position (for mentor locations)"""
        screen.blit(self.image, position) 