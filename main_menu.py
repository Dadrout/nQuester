import pygame
import random
import math
import os
from PIL import Image
from settings import *
from intro_scene import IntroScene
from sound_manager import get_sound_manager
from settings_screen import SettingsScreen
from achievements_screen import AchievementsScreen

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Menu state
        self.selected_option = 0  # Start with "Начать игру" selected
        self.menu_options = [
            "🎮 Начать игру",
            "📖 Как играть", 
            "🏆 Достижения",
            "⚙️ Настройки",
            "❌ Выход"
        ]
        
        # Load GIF background
        self.gif_frames = []
        self.current_frame = 0
        self.frame_delay = 0.1  # 100ms per frame
        self.last_frame_time = 0
        self.load_gif_background()
        
        # Fallback to pixel background if GIF fails
        if not self.gif_frames:
            self.background = self.generate_pixel_background()
        else:
            self.background = self.gif_frames[0]
        
        # Animation
        self.animation_time = 0
        self.particles = []
        self.generate_particles()
    
    def load_gif_background(self):
        """Load GIF background frames"""
        try:
            gif_path = "the world is ours.gif"
            if os.path.exists(gif_path):
                # Open GIF with PIL
                gif = Image.open(gif_path)
                
                # Extract frames
                frame_count = getattr(gif, 'n_frames', 1)
                for frame in range(frame_count):
                    gif.seek(frame)
                    # Convert PIL image to pygame surface
                    frame_surface = pygame.image.fromstring(gif.convert('RGBA').tobytes(), gif.size, 'RGBA')
                    
                    # Scale to fit screen
                    frame_surface = pygame.transform.scale(frame_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    
                    # Add dark overlay for better text visibility
                    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    overlay.set_alpha(100)
                    overlay.fill((0, 0, 0))
                    frame_surface.blit(overlay, (0, 0))
                    
                    self.gif_frames.append(frame_surface)
                
                print(f"✅ Загружено {len(self.gif_frames)} кадров GIF-фона")
            else:
                print(f"⚠️ GIF файл не найден: {gif_path}")
        except Exception as e:
            print(f"❌ Ошибка загрузки GIF: {e}")
    
    def update_gif_background(self, dt):
        """Update GIF animation"""
        if self.gif_frames:
            self.last_frame_time += dt
            if self.last_frame_time >= self.frame_delay:
                self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
                self.background = self.gif_frames[self.current_frame]
                self.last_frame_time = 0
    
    def generate_pixel_background(self):
        """Generate a startup/tech themed pixel art background"""
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg.fill((15, 25, 35))  # Dark tech blue base
        
        # Startup/tech themed colors
        colors = [
            (30, 50, 70),   # Dark tech blue
            (50, 80, 100),  # Medium tech blue
            (80, 120, 160), # Light tech blue
            (100, 150, 200), # Bright tech blue
            (120, 180, 220), # Very bright blue
            (60, 100, 140),  # Green-blue
            (80, 140, 100),  # Tech green
        ]
        
        # Create tech circuit pattern
        pixel_size = 3
        for x in range(0, SCREEN_WIDTH, pixel_size * 2):
            for y in range(0, SCREEN_HEIGHT, pixel_size * 2):
                if random.random() < 0.4:  # 40% chance for circuit pixel
                    color = random.choice(colors)
                    pygame.draw.rect(bg, color, (x, y, pixel_size, pixel_size))
        
        # Add circuit lines (horizontal and vertical)
        for i in range(8):
            # Horizontal circuit lines
            y = random.randint(50, SCREEN_HEIGHT - 50)
            for x in range(0, SCREEN_WIDTH, 20):
                if random.random() < 0.7:
                    pygame.draw.line(bg, random.choice(colors), (x, y), (x + 15, y), 2)
            
            # Vertical circuit lines
            x = random.randint(50, SCREEN_WIDTH - 50)
            for y in range(0, SCREEN_HEIGHT, 20):
                if random.random() < 0.7:
                    pygame.draw.line(bg, random.choice(colors), (x, y), (x, y + 15), 2)
        
        # Add startup-themed geometric shapes (like buildings, charts, etc.)
        for i in range(6):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(15, 40)
            color = random.choice(colors)
            
            # Different shapes for variety
            if i % 3 == 0:
                # Building-like rectangles
                pygame.draw.rect(bg, color, (x, y, size, size * 2))
            elif i % 3 == 1:
                # Chart-like lines
                points = [(x, y), (x + size, y - size//2), (x + size*2, y + size//2)]
                pygame.draw.lines(bg, color, False, points, 3)
            else:
                # Circuit nodes
                pygame.draw.circle(bg, color, (x, y), size//2)
        
        # Add some "data" or "code" elements
        for i in range(10):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            color = random.choice(colors)
            # Small data points
            pygame.draw.circle(bg, color, (x, y), 2)
        
        # Add gradient overlay for depth
        gradient = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        gradient.set_alpha(30)
        for y in range(SCREEN_HEIGHT):
            alpha = int(100 * (y / SCREEN_HEIGHT))
            color = (0, 0, 0, alpha)
            pygame.draw.line(gradient, color, (0, y), (SCREEN_WIDTH, y))
        
        bg.blit(gradient, (0, 0))
        return bg
    
    def generate_particles(self):
        """Generate floating particles for animation"""
        self.particles = []
        for _ in range(25):  # More particles
            particle = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'vx': random.uniform(-0.3, 0.3),
                'vy': random.uniform(-0.3, 0.3),
                'size': random.randint(1, 3),
                'color': (
                    random.randint(80, 150),   # Blue tones
                    random.randint(120, 200),  # Green-blue
                    random.randint(180, 255)   # Bright blue
                )
            }
            self.particles.append(particle)
    
    def update_particles(self, dt):
        """Update particle positions"""
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Wrap around screen
            if particle['x'] < 0:
                particle['x'] = SCREEN_WIDTH
            elif particle['x'] > SCREEN_WIDTH:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = SCREEN_HEIGHT
            elif particle['y'] > SCREEN_HEIGHT:
                particle['y'] = 0
    
    def draw_particles(self):
        """Draw floating particles"""
        for particle in self.particles:
            pygame.draw.circle(
                self.screen, 
                particle['color'], 
                (int(particle['x']), int(particle['y'])), 
                particle['size']
            )
    
    def draw_menu(self):
        """Draw the main menu"""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw particles
        self.draw_particles()
        
        # Draw title with glow effect
        title = "nQuester: Incubator Rush"
        title_surface = self.font_large.render(title, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 150))
        
        # Glow effect
        glow_surface = self.font_large.render(title, True, (100, 150, 255))
        glow_rect = glow_surface.get_rect(center=(SCREEN_WIDTH//2 + 2, 152))
        self.screen.blit(glow_surface, glow_rect)
        self.screen.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle = "Погрузись в мир стартапов и программирования!"
        subtitle_surface = self.font_medium.render(subtitle, True, (200, 200, 200))
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH//2, 220))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw menu options
        menu_y = 350
        for i, option in enumerate(self.menu_options):
            color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            
            # Highlight selected option
            if i == self.selected_option:
                # Draw selection box
                box_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, menu_y - 10, 400, 50)
                pygame.draw.rect(self.screen, (100, 150, 255, 100), box_rect)
                pygame.draw.rect(self.screen, (100, 150, 255), box_rect, 2)
            
            option_surface = self.font_medium.render(option, True, color)
            option_rect = option_surface.get_rect(center=(SCREEN_WIDTH//2, menu_y))
            self.screen.blit(option_surface, option_rect)
            
            menu_y += 70
        
        # Draw instructions
        instructions = [
            "↑↓ - Выбор опции",
            "Enter - Подтвердить",
            "F11 - Полноэкранный режим",
            "ESC - Выход"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_surface = self.font_small.render(instruction, True, (100, 100, 100))
            inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100 + i * 25))
            self.screen.blit(inst_surface, inst_rect)
    
    def handle_input(self, events):
        """Handle menu input"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    # Play menu selection sound
                    sound_manager = get_sound_manager()
                    if sound_manager:
                        sound_manager.play_menu_select()
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    # Play menu selection sound
                    sound_manager = get_sound_manager()
                    if sound_manager:
                        sound_manager.play_menu_select()
                elif event.key == pygame.K_RETURN:
                    # Play menu confirmation sound
                    sound_manager = get_sound_manager()
                    if sound_manager:
                        sound_manager.play_menu_confirm()
                    return self.selected_option
                elif event.key == pygame.K_ESCAPE:
                    return len(self.menu_options) - 1  # Exit option
                elif event.key == pygame.K_F11:
                    # Toggle fullscreen
                    self.toggle_fullscreen()
        
        return None
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        if pygame.display.get_surface().get_flags() & pygame.FULLSCREEN:
            # Currently fullscreen, switch to windowed
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            print("🖥️ Fullscreen: OFF")
        else:
            # Currently windowed, switch to fullscreen
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            print("��️ Fullscreen: ON")
    
    def run(self):
        """Run the main menu loop"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            dt = clock.tick(60) / 1000.0
            self.animation_time += dt
            
            # Update particles
            self.update_particles(dt)
            
            # Update GIF background
            self.update_gif_background(dt)
            
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return "exit"
            
            # Handle input
            result = self.handle_input(events)
            if result is not None:
                if result == 0:  # Start game
                    return "start_game"
                elif result == 1:  # How to play
                    return "how_to_play"
                elif result == 2:  # Achievements
                    return "achievements"
                elif result == 3:  # Settings
                    return "settings"
                elif result == 4:  # Exit
                    return "exit"
            
            # Draw
            self.draw_menu()
            pygame.display.flip()
        
        return "exit"

def show_how_to_play(screen):
    """Show how to play screen"""
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 24)
    
    instructions = [
        "🎮 КАК ИГРАТЬ",
        "",
        "🏃‍♂️ Движение: WASD или стрелки",
        "👥 Взаимодействие: E (возле NPC)",
        "📖 Журнал: Q или Tab",
        "💾 Сохранение: F5",
        "📂 Загрузка: F9",
        "🖥️ Полноэкранный режим: F11",
        "",
        "🎯 Цель:",
        "• Выполняй квесты менторов",
        "• Проходи мини-игры",
        "• Привлекай пользователей",
        "• Достигни 10,000 пользователей!",
        "",
        "🎮 Мини-игры:",
        "• Swift Debug - найди баги",
        "• AI Training - обучи нейросеть",
        "• TypeScript Quiz - строгая типизация",
        "• И многие другие!",
        "",
        "Нажми ESC для возврата в меню"
    ]
    
    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
        
        # Draw
        screen.fill((20, 30, 50))
        
        y_offset = 100
        for instruction in instructions:
            if instruction.startswith("🎮"):
                color = (255, 255, 255)
                font = font_large
            elif instruction.startswith("🎯") or instruction.startswith("🎮"):
                color = (255, 200, 100)
                font = font_medium
            elif instruction.startswith("•"):
                color = (200, 200, 200)
                font = font_medium
            else:
                color = (150, 150, 150)
                font = font_medium
            
            text_surface = font.render(instruction, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 40
        
        pygame.display.flip()

def show_achievements(screen):
    """Show achievements screen"""
    achievements_screen = AchievementsScreen(screen)
    return achievements_screen.run()

def show_settings(screen, player):
    """Show settings screen"""
    settings_screen = SettingsScreen(screen)
    return settings_screen.run() 