import pygame
import os
from settings import *

class SpriteSheet:
    def __init__(self, filename):
        """Конструктор. Загружает спрайт-лист."""
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Невозможно загрузить спрайт-лист: {filename}")
            raise SystemExit(e)

    def get_image(self, x, y, width, height):
        """
        Вырезает один кадр (спрайт) из большого листа.
        x, y - координаты верхнего левого угла кадра на листе.
        width, height - ширина и высота кадра.
        """
        image = pygame.Surface([width, height], pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image

class SpriteLoader:
    def __init__(self):
        self.characters_path = "Modern_Interiors_Free_v2.2/Modern tiles_Free/Characters_free/"
        self.interiors_path = "Modern_Interiors_Free_v2.2/Modern tiles_Free/Interiors_free/32x32/"
        self.mentors_path = "Mentors/"
        self.maps_path = "Base and Full Map + HD Images/"
        self.mc_path = "mc/"  # Путь к анимациям главного героя
        
        # Загруженные спрайты
        self.player_sprites = {}
        self.player_walk_animations = {}  # Анимации ходьбы для главного героя
        self.npc_sprites = {}
        self.mentor_faces = {}
        self.interior_tiles = {}
        self.room_maps = {}  # Отдельные локации для менторов
        
        # Загружаем все спрайты
        self.load_all_sprites()
        self.create_mentor_rooms()
    
    def load_all_sprites(self):
        """Загружает все спрайты"""
        print("Загрузка спрайтов...")
        
        try:
            self.load_character_sprites()
            self.load_mc_walk_animations()  # Загружаем анимации главного героя
            self.load_mentor_faces()
            self.load_interior_tiles()
            print("✅ Все спрайты загружены!")
        except Exception as e:
            print(f"❌ Ошибка загрузки спрайтов: {e}")
    
    def load_mc_walk_animations(self):
        """Загружает анимации ходьбы главного героя из папки mc"""
        directions = ["up", "down", "left", "right"]
        
        for direction in directions:
            direction_path = os.path.join(self.mc_path, direction)
            print(f"Проверяем папку: {direction_path}")
            if os.path.exists(direction_path):
                frames = []
                
                # Получаем все файлы в папке направления
                files = [f for f in os.listdir(direction_path) if f.endswith('.png')]
                files.sort()  # Сортируем для правильного порядка кадров
                print(f"Найдено файлов в {direction}: {len(files)}")
                
                for file in files:
                    try:
                        frame_path = os.path.join(direction_path, file)
                        print(f"Загружаем: {frame_path}")
                        frame = pygame.image.load(frame_path).convert_alpha()
                        # Масштабируем пропорционально: 16x16 -> 32x32 (2x увеличение)
                        frame = pygame.transform.scale(frame, (32, 32))
                        frames.append(frame)
                        print(f"✅ Успешно загружен кадр: {file}")
                    except (pygame.error, OSError) as e:
                        print(f"❌ Ошибка загрузки кадра {file} для направления {direction}: {e}")
                
                if frames:
                    self.player_walk_animations[direction] = frames
                    print(f"✅ Загружено {len(frames)} кадров для направления {direction}")
                else:
                    print(f"⚠️ Не удалось загрузить кадры для направления {direction}")
            else:
                print(f"⚠️ Папка {direction_path} не найдена")
    
    def load_character_sprites(self):
        """Загружает спрайты персонажей"""
        characters = ["Adam", "Alex", "Amelia", "Bob"]
        
        for char in characters:
            # Idle спрайт
            idle_path = os.path.join(self.characters_path, f"{char}_idle_16x16.png")
            if os.path.exists(idle_path):
                try:
                    sprite = pygame.image.load(idle_path)
                    # Масштабируем пропорционально: 16x16 -> 32x32 (2x увеличение)
                    sprite = pygame.transform.scale(sprite, (32, 32))
                    self.npc_sprites[f"{char.lower()}_idle"] = sprite
                    
                    if char == "Adam":
                        self.player_sprites["idle"] = sprite
                except (pygame.error, OSError) as e:
                    print(f"Ошибка загрузки idle для {char}: {e}")
            
            # Анимация ходьбы - используем idle как fallback
            run_path = os.path.join(self.characters_path, f"{char}_run_16x16.png")
            if os.path.exists(run_path):
                try:
                    # Используем SpriteSheet для правильной работы
                    spritesheet = SpriteSheet(run_path)
                    
                    # Размеры кадров на спрайт-листе
                    SPRITE_WIDTH = 16
                    SPRITE_HEIGHT = 16
                    
                    walk_frames = []
                    for i in range(4):  # 4 кадра анимации
                        frame = spritesheet.get_image(i * SPRITE_WIDTH, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
                        # Масштабируем пропорционально: 16x16 -> 32x32 (2x увеличение)
                        frame = pygame.transform.scale(frame, (32, 32))
                        walk_frames.append(frame)
                    
                    self.npc_sprites[f"{char.lower()}_walk"] = walk_frames
                    
                    if char == "Adam":
                        self.player_sprites["walk"] = walk_frames
                        
                except (pygame.error, OSError) as e:
                    print(f"Ошибка загрузки анимации для {char}: {e}")
                    # Fallback к idle спрайту
                    idle_sprite = self.npc_sprites.get(f"{char.lower()}_idle")
                    if idle_sprite:
                        if char == "Adam":
                            self.player_sprites["walk"] = [idle_sprite]
                        self.npc_sprites[f"{char.lower()}_walk"] = [idle_sprite]
    
    def load_mentor_faces(self):
        """Загружает лица менторов для диалогов"""
        mentor_files = [
            "Alikhan.png", "Alibeck.png", "Bahredin.png", "Bahaudin.png",
            "Gaziz.png", "Shoqan.png", "Zhasulan.png", "Aimurat.png", "Bernar.png"
        ]
        
        for mentor_file in mentor_files:
            path = os.path.join(self.mentors_path, mentor_file)
            if os.path.exists(path):
                face = pygame.image.load(path)
                # Масштабируем для диалогов
                face = pygame.transform.scale(face, (80, 80))
                name = mentor_file.replace(".png", "")
                self.mentor_faces[name] = face
    
    def load_interior_tiles(self):
        """Загружает тайлы интерьеров"""
        interiors_path = os.path.join(self.interiors_path, "Interiors_free_32x32.png")
        room_builder_path = os.path.join(self.interiors_path, "Room_Builder_free_32x32.png")
        
        if os.path.exists(interiors_path):
            self.interior_tiles["interiors"] = pygame.image.load(interiors_path)
            
        if os.path.exists(room_builder_path):
            self.interior_tiles["room_builder"] = pygame.image.load(room_builder_path)
    
    def create_mentor_rooms(self):
        """Создает отдельные локации для каждого ментора"""
        mentors = [
            {"name": "Alikhan", "type": "ios_lab"},
            {"name": "Alibeck", "type": "ai_lab"},
            {"name": "Bahredin", "type": "typescript_office"},
            {"name": "Bahaudin", "type": "backend_office"},
            {"name": "Gaziz", "type": "frontend_office"},
            {"name": "Shoqan", "type": "mobile_lab"},
            {"name": "Zhasulan", "type": "ios_room"},
            {"name": "Aimurat", "type": "ai_lab"},
            {"name": "Bernar", "type": "boss_office"}
        ]
        
        for mentor in mentors:
            room_surface = self.create_room_for_mentor(mentor["type"])
            self.room_maps[mentor["name"]] = room_surface
    
    def create_room_for_mentor(self, room_type):
        """Создает уникальную комнату для ментора с GalletCity фоном"""
        room_width, room_height = 25, 20  # Размер комнаты в тайлах
        room_surface = pygame.Surface((room_width * TILE_SIZE, room_height * TILE_SIZE))
        
        # Загружаем GalletCity как фон
        galletcity_path = os.path.join(self.maps_path, "galletcity.png")
        if os.path.exists(galletcity_path):
            try:
                galletcity_bg = pygame.image.load(galletcity_path)
                # Масштабируем под размер комнаты
                galletcity_bg = pygame.transform.scale(galletcity_bg, (room_width * TILE_SIZE, room_height * TILE_SIZE))
                room_surface.blit(galletcity_bg, (0, 0))
            except:
                # Fallback к базовому полу
                floor_tile = self.get_tile_from_sheet("interiors", 0, 0)
                if floor_tile:
                    for x in range(room_width):
                        for y in range(room_height):
                            room_surface.blit(floor_tile, (x * TILE_SIZE, y * TILE_SIZE))
        else:
            # Fallback к базовому полу
            floor_tile = self.get_tile_from_sheet("interiors", 0, 0)
            if floor_tile:
                for x in range(room_width):
                    for y in range(room_height):
                        room_surface.blit(floor_tile, (x * TILE_SIZE, y * TILE_SIZE))
        
        # Стены
        wall_tile = self.get_tile_from_sheet("room_builder", 0, 0)
        if wall_tile:
            # Верхняя и нижняя стены
            for x in range(room_width):
                room_surface.blit(wall_tile, (x * TILE_SIZE, 0))
                room_surface.blit(wall_tile, (x * TILE_SIZE, (room_height - 1) * TILE_SIZE))
            
            # Левая и правая стены
            for y in range(room_height):
                room_surface.blit(wall_tile, (0, y * TILE_SIZE))
                room_surface.blit(wall_tile, ((room_width - 1) * TILE_SIZE, y * TILE_SIZE))
        
        # Добавляем мебель в зависимости от типа комнаты
        self.add_furniture_to_room(room_surface, room_type)
        
        return room_surface
    
    def add_furniture_to_room(self, room_surface, room_type):
        """Добавляет мебель в комнату в зависимости от типа"""
        if room_type == "ios_lab":
            # Стол с компьютером
            desk_tile = self.get_tile_from_sheet("interiors", 1, 0)
            if desk_tile:
                room_surface.blit(desk_tile, (10 * TILE_SIZE, 8 * TILE_SIZE))
                
        elif room_type == "ai_lab":
            # Большой экран/монитор
            screen_tile = self.get_tile_from_sheet("interiors", 2, 0)
            if screen_tile:
                room_surface.blit(screen_tile, (8 * TILE_SIZE, 6 * TILE_SIZE))
                
        elif room_type == "typescript_office":
            # Книжная полка
            shelf_tile = self.get_tile_from_sheet("interiors", 3, 0)
            if shelf_tile:
                room_surface.blit(shelf_tile, (20 * TILE_SIZE, 5 * TILE_SIZE))
        
        # Добавляем дверь для выхода
        door_tile = self.get_tile_from_sheet("room_builder", 1, 0)
        if door_tile:
            room_surface.blit(door_tile, (12 * TILE_SIZE, 18 * TILE_SIZE))
    
    def get_player_sprite(self, state="idle", frame=0, direction="down"):
        """Получить спрайт игрока с анимацией"""
        # Сначала проверяем анимации главного героя из папки mc
        if state == "walk" and direction in self.player_walk_animations:
            walk_frames = self.player_walk_animations[direction]
            if walk_frames:
                return walk_frames[frame % len(walk_frames)]
            else:
                print(f"⚠️ Пустой список кадров для направления: {direction}")
        
        # Fallback к старым анимациям
        if state == "walk" and "walk" in self.player_sprites:
            walk_frames = self.player_sprites["walk"]
            return walk_frames[frame % len(walk_frames)]
        
        return self.player_sprites.get(state, self.player_sprites.get("idle"))
    
    def get_npc_sprite(self, character_name, state="idle", frame=0):
        """Получить спрайт NPC с анимацией"""
        if state == "walk":
            walk_frames = self.npc_sprites.get(f"{character_name.lower()}_walk", [])
            if walk_frames:
                return walk_frames[frame % len(walk_frames)]
        
        return self.npc_sprites.get(f"{character_name.lower()}_idle")
    
    def get_mentor_face(self, mentor_name):
        """Получает лицо ментора для диалогов"""
        return self.mentor_faces.get(mentor_name)
    
    def get_background(self, background_name):
        """Получает фоновое изображение"""
        try:
            if background_name == "galletcity":
                galletcity_path = os.path.join(self.maps_path, "galletcity.png")
                if os.path.exists(galletcity_path):
                    return pygame.image.load(galletcity_path)
        except:
            pass
        return None
    
    def get_mentor_room(self, mentor_name):
        """Получить локацию ментора"""
        return self.room_maps.get(mentor_name)
    
    def get_tile_from_sheet(self, sheet_name, tile_x, tile_y, tile_size=32):
        """Получить тайл из спрайт-листа"""
        if sheet_name in self.interior_tiles:
            sheet = self.interior_tiles[sheet_name]
            tile_rect = pygame.Rect(tile_x * tile_size, tile_y * tile_size, tile_size, tile_size)
            tile = sheet.subsurface(tile_rect)
            return tile
        return None

# Глобальный экземпляр загрузчика
sprite_loader = None

def init_sprite_loader():
    """Инициализация загрузчика спрайтов"""
    global sprite_loader
    if sprite_loader is None:
        sprite_loader = SpriteLoader()
    return sprite_loader

def get_sprite_loader():
    """Получить загрузчик спрайтов"""
    global sprite_loader
    if sprite_loader is None:
        sprite_loader = SpriteLoader()
    return sprite_loader 