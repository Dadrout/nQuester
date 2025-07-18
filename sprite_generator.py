import pygame
import os
import math
from settings import *

def create_cat_sprite(size=(32, 32)):
    """Create a cute cat sprite"""
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Cat body (orange)
    pygame.draw.ellipse(surface, (255, 165, 0), (4, 8, 24, 16))
    
    # Cat head (orange)
    pygame.draw.circle(surface, (255, 165, 0), (20, 12), 8)
    
    # Ears (orange triangles)
    pygame.draw.polygon(surface, (255, 165, 0), [(16, 6), (20, 2), (24, 6)])
    pygame.draw.polygon(surface, (255, 165, 0), [(20, 6), (24, 2), (28, 6)])
    
    # Eyes (green)
    pygame.draw.circle(surface, (0, 255, 0), (18, 10), 2)
    pygame.draw.circle(surface, (0, 255, 0), (22, 10), 2)
    
    # Nose (pink)
    pygame.draw.circle(surface, (255, 192, 203), (20, 14), 1)
    
    # Whiskers
    pygame.draw.line(surface, (255, 255, 255), (12, 12), (8, 10), 1)
    pygame.draw.line(surface, (255, 255, 255), (12, 14), (8, 14), 1)
    pygame.draw.line(surface, (255, 255, 255), (28, 12), (32, 10), 1)
    pygame.draw.line(surface, (255, 255, 255), (28, 14), (32, 14), 1)
    
    return surface

def create_dog_sprite(size=(32, 32)):
    """Create a cute dog sprite"""
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Dog body (brown)
    pygame.draw.ellipse(surface, (139, 69, 19), (4, 8, 24, 16))
    
    # Dog head (brown)
    pygame.draw.circle(surface, (139, 69, 19), (20, 12), 8)
    
    # Ears (brown)
    pygame.draw.ellipse(surface, (139, 69, 19), (16, 4, 6, 8))
    pygame.draw.ellipse(surface, (139, 69, 19), (22, 4, 6, 8))
    
    # Eyes (brown)
    pygame.draw.circle(surface, (139, 69, 19), (18, 10), 2)
    pygame.draw.circle(surface, (139, 69, 19), (22, 10), 2)
    
    # Nose (black)
    pygame.draw.circle(surface, (0, 0, 0), (20, 14), 1)
    
    # Tongue (red)
    pygame.draw.ellipse(surface, (255, 0, 0), (19, 16, 2, 4))
    
    return surface

def create_brain_sprite(size=(64, 64)):
    """Create a brain/AI model sprite"""
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Brain base (pink)
    pygame.draw.circle(surface, (255, 182, 193), (32, 32), 20)
    
    # Brain folds (darker pink)
    for i in range(5):
        y = 20 + i * 8
        pygame.draw.ellipse(surface, (255, 150, 150), (16, y, 32, 6))
    
    # Neural connections (blue lines)
    for i in range(8):
        x1 = 20 + i * 6
        y1 = 15 + (i % 3) * 10
        x2 = 25 + i * 6
        y2 = 25 + (i % 3) * 10
        pygame.draw.line(surface, (0, 100, 255), (x1, y1), (x2, y2), 2)
    
    # AI indicators (green dots)
    pygame.draw.circle(surface, (0, 255, 0), (20, 20), 3)
    pygame.draw.circle(surface, (0, 255, 0), (44, 20), 3)
    pygame.draw.circle(surface, (0, 255, 0), (32, 44), 3)
    
    return surface

def create_button_sprite(text, size=(120, 40), color=BLUE):
    """Create a modern button sprite"""
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Button background with gradient
    pygame.draw.rect(surface, color, (0, 0, size[0], size[1]))
    pygame.draw.rect(surface, (255, 255, 255), (0, 0, size[0], size[1]), 2)
    
    # Add highlight
    pygame.draw.line(surface, (255, 255, 255), (2, 2), (size[0]-2, 2), 1)
    pygame.draw.line(surface, (255, 255, 255), (2, 2), (2, size[1]-2), 1)
    
    # Add shadow
    pygame.draw.line(surface, (100, 100, 100), (size[0]-2, 2), (size[0]-2, size[1]-2), 1)
    pygame.draw.line(surface, (100, 100, 100), (2, size[1]-2), (size[0]-2, size[1]-2), 1)
    
    # Text
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(size[0]//2, size[1]//2))
    surface.blit(text_surface, text_rect)
    
    return surface

def create_progress_bar_sprite(width=200, height=20, progress=0.5):
    """Create a progress bar sprite"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Background
    pygame.draw.rect(surface, (50, 50, 50), (0, 0, width, height))
    pygame.draw.rect(surface, (100, 100, 100), (0, 0, width, height), 2)
    
    # Progress fill
    fill_width = int(width * progress)
    pygame.draw.rect(surface, GREEN, (2, 2, fill_width-4, height-4))
    
    # Add shine effect
    pygame.draw.line(surface, (255, 255, 255), (2, 2), (fill_width-2, 2), 1)
    
    return surface

def create_particle_sprite(color=YELLOW, size=(8, 8)):
    """Create a particle effect sprite"""
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Particle with glow effect
    pygame.draw.circle(surface, color, (size[0]//2, size[1]//2), size[0]//2)
    pygame.draw.circle(surface, WHITE, (size[0]//2, size[1]//2), size[0]//4)
    
    return surface

def create_quest_marker_sprite():
    """Create a quest marker sprite"""
    surface = pygame.Surface((24, 24), pygame.SRCALPHA)
    
    # Exclamation mark background
    pygame.draw.circle(surface, YELLOW, (12, 12), 10)
    pygame.draw.circle(surface, (255, 255, 0), (12, 12), 8)
    
    # Exclamation mark
    pygame.draw.rect(surface, BLACK, (11, 6, 2, 8))
    pygame.draw.circle(surface, BLACK, (12, 18), 2)
    
    return surface

def create_success_effect_sprite():
    """Create a success effect sprite"""
    surface = pygame.Surface((64, 64), pygame.SRCALPHA)
    
    # Star shape
    points = []
    for i in range(5):
        angle = i * 72 - 90
        x = 32 + 20 * math.cos(math.radians(angle))
        y = 32 + 20 * math.sin(math.radians(angle))
        points.append((x, y))
    
    pygame.draw.polygon(surface, YELLOW, points)
    pygame.draw.polygon(surface, WHITE, points, 2)
    
    return surface

def save_sprite(sprite, filename):
    """Save sprite to file"""
    try:
        pygame.image.save(sprite, filename)
        print(f"✅ Saved sprite: {filename}")
    except Exception as e:
        print(f"❌ Failed to save {filename}: {e}")

def generate_all_sprites():
    """Generate all game sprites"""
    print("🎨 Generating game sprites...")
    
    # Create sprites directory if it doesn't exist
    sprites_dir = "data/sprites/minigame"
    os.makedirs(sprites_dir, exist_ok=True)
    
    # Generate sprites
    sprites = {
        "cat.png": create_cat_sprite(),
        "dog.png": create_dog_sprite(),
        "brain.png": create_brain_sprite(),
        "button_continue.png": create_button_sprite("Continue", (120, 40), GREEN),
        "button_retry.png": create_button_sprite("Retry", (120, 40), RED),
        "progress_bar.png": create_progress_bar_sprite(),
        "particle.png": create_particle_sprite(),
        "quest_marker.png": create_quest_marker_sprite(),
        "success_effect.png": create_success_effect_sprite(),
    }
    
    # Save all sprites
    for filename, sprite in sprites.items():
        filepath = os.path.join(sprites_dir, filename)
        save_sprite(sprite, filepath)
    
    print("🎨 All sprites generated successfully!")

if __name__ == "__main__":
    pygame.init()
    generate_all_sprites()
    pygame.quit()