import requests
import os
import urllib.request
from pathlib import Path

class SpriteDownloader:
    def __init__(self):
        self.sprites_dir = Path("data/sprites")
        self.sprites_dir.mkdir(parents=True, exist_ok=True)
        
        # Список бесплатных спрайтов (создаем простые альтернативы)
        self.sprite_urls = {
            # Простые геометрические спрайты как альтернатива
            "player_alt": None,  # Будем создавать программно
            "student_alt": None,
            "ui_elements": None
        }
    
    def create_simple_sprites(self):
        """Создает дополнительные простые спрайты"""
        import pygame
        
        pygame.init()
        
        # Создаем папку для дополнительных спрайтов
        additional_dir = self.sprites_dir / "additional"
        additional_dir.mkdir(exist_ok=True)
        
        # 1. Спрайт игрока (альтернативный)
        player_alt = pygame.Surface((32, 32), pygame.SRCALPHA)
        # Круглая голова
        pygame.draw.circle(player_alt, (255, 218, 185), (16, 10), 8)
        # Тело
        pygame.draw.rect(player_alt, (0, 100, 200), (12, 18, 8, 12))
        # Глаза
        pygame.draw.circle(player_alt, (0, 0, 0), (13, 8), 1)
        pygame.draw.circle(player_alt, (0, 0, 0), (19, 8), 1)
        # Улыбка
        pygame.draw.arc(player_alt, (0, 0, 0), (12, 10, 8, 4), 0, 3.14, 2)
        
        pygame.image.save(player_alt, additional_dir / "player_alt.png")
        print("Создан альтернативный спрайт игрока")
        
        # 2. Спрайт студента (альтернативный)
        student_alt = pygame.Surface((32, 32), pygame.SRCALPHA)
        # Круглая голова
        pygame.draw.circle(student_alt, (255, 218, 185), (16, 10), 8)
        # Тело
        pygame.draw.rect(student_alt, (100, 150, 100), (12, 18, 8, 12))
        # Глаза
        pygame.draw.circle(student_alt, (0, 0, 0), (13, 8), 1)
        pygame.draw.circle(student_alt, (0, 0, 0), (19, 8), 1)
        # Очки
        pygame.draw.circle(student_alt, (0, 0, 0), (13, 8), 3, 1)
        pygame.draw.circle(student_alt, (0, 0, 0), (19, 8), 3, 1)
        pygame.draw.line(student_alt, (0, 0, 0), (16, 8), (16, 8), 1)
        
        pygame.image.save(student_alt, additional_dir / "student_alt.png")
        print("Создан альтернативный спрайт студента")
        
        # 3. UI элементы
        # Кнопка паузы
        pause_button = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(pause_button, (100, 100, 200), (0, 0, 32, 32))
        pygame.draw.rect(pause_button, (255, 255, 255), (10, 8, 4, 16))
        pygame.draw.rect(pause_button, (255, 255, 255), (18, 8, 4, 16))
        pygame.image.save(pause_button, additional_dir / "pause_button.png")
        
        # Кнопка звука
        sound_button = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(sound_button, (100, 100, 200), (0, 0, 32, 32))
        pygame.draw.circle(sound_button, (255, 255, 255), (16, 16), 8)
        pygame.draw.circle(sound_button, (100, 100, 200), (16, 16), 4)
        pygame.image.save(sound_button, additional_dir / "sound_button.png")
        
        # Иконка квеста
        quest_icon = pygame.Surface((24, 24), pygame.SRCALPHA)
        # Звездочка
        points = [(12, 2), (14, 8), (20, 8), (16, 12), (18, 18), (12, 14), (6, 18), (8, 12), (4, 8), (10, 8)]
        pygame.draw.polygon(quest_icon, (255, 255, 0), points)
        pygame.image.save(quest_icon, additional_dir / "quest_icon.png")
        
        print("Созданы UI элементы")
        
        pygame.quit()
    
    def create_animation_frames(self):
        """Создает кадры анимации для игрока"""
        import pygame
        
        pygame.init()
        
        animation_dir = self.sprites_dir / "animations"
        animation_dir.mkdir(exist_ok=True)
        
        # Анимация ходьбы игрока (4 кадра)
        for frame in range(4):
            surface = pygame.Surface((32, 32), pygame.SRCALPHA)
            
            # Тело
            pygame.draw.rect(surface, (0, 100, 200), (8, 8, 16, 20))
            
            # Голова
            pygame.draw.circle(surface, (255, 218, 185), (16, 8), 6)
            
            # Глаза
            pygame.draw.circle(surface, (0, 0, 0), (14, 6), 1)
            pygame.draw.circle(surface, (0, 0, 0), (18, 6), 1)
            
            # Руки (анимированные)
            if frame == 0:
                pygame.draw.rect(surface, (255, 218, 185), (4, 12, 4, 8))
                pygame.draw.rect(surface, (255, 218, 185), (24, 12, 4, 8))
            elif frame == 1:
                pygame.draw.rect(surface, (255, 218, 185), (4, 10, 4, 8))
                pygame.draw.rect(surface, (255, 218, 185), (24, 14, 4, 8))
            elif frame == 2:
                pygame.draw.rect(surface, (255, 218, 185), (4, 14, 4, 8))
                pygame.draw.rect(surface, (255, 218, 185), (24, 10, 4, 8))
            else:
                pygame.draw.rect(surface, (255, 218, 185), (4, 12, 4, 8))
                pygame.draw.rect(surface, (255, 218, 185), (24, 12, 4, 8))
            
            # Ноги (анимированные)
            if frame == 0 or frame == 2:
                pygame.draw.rect(surface, (50, 50, 50), (10, 28, 4, 4))
                pygame.draw.rect(surface, (50, 50, 50), (18, 28, 4, 4))
            else:
                pygame.draw.rect(surface, (50, 50, 50), (8, 28, 4, 4))
                pygame.draw.rect(surface, (50, 50, 50), (20, 28, 4, 4))
            
            pygame.image.save(surface, animation_dir / f"player_walk_{frame}.png")
        
        print("Созданы кадры анимации ходьбы")
        
        pygame.quit()
    
    def create_environment_sprites(self):
        """Создает спрайты окружения"""
        import pygame
        
        pygame.init()
        
        env_dir = self.sprites_dir / "environment"
        env_dir.mkdir(exist_ok=True)
        
        # Дерево
        tree = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(tree, (139, 69, 19), (14, 20, 4, 12))  # Ствол
        pygame.draw.circle(tree, (34, 139, 34), (16, 12), 8)     # Крона
        pygame.image.save(tree, env_dir / "tree.png")
        
        # Камень
        rock = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(rock, (128, 128, 128), (16, 16), 8)
        pygame.image.save(rock, env_dir / "rock.png")
        
        # Цветок
        flower = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(flower, (255, 255, 0), (16, 16), 4)  # Центр
        for i in range(8):
            angle = i * 45
            x = 16 + 6 * pygame.math.Vector2(1, 0).rotate(angle)[0]
            y = 16 + 6 * pygame.math.Vector2(1, 0).rotate(angle)[1]
            pygame.draw.circle(flower, (255, 192, 203), (int(x), int(y)), 2)
        pygame.image.save(flower, env_dir / "flower.png")
        
        # Дверь
        door = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(door, (139, 69, 19), (8, 8, 16, 24))
        pygame.draw.rect(door, (160, 82, 45), (10, 10, 12, 20))
        pygame.draw.circle(door, (255, 215, 0), (22, 16), 2)  # Ручка
        pygame.image.save(door, env_dir / "door.png")
        
        print("Созданы спрайты окружения")
        
        pygame.quit()
    
    def download_all(self):
        """Загружает и создает все спрайты"""
        print("Создание дополнительных спрайтов...")
        
        try:
            self.create_simple_sprites()
            self.create_animation_frames()
            self.create_environment_sprites()
            
            print("✅ Все спрайты созданы успешно!")
            print(f"📁 Спрайты сохранены в: {self.sprites_dir}")
            
        except Exception as e:
            print(f"❌ Ошибка при создании спрайтов: {e}")

if __name__ == "__main__":
    downloader = SpriteDownloader()
    downloader.download_all() 