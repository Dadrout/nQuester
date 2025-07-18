import pygame
from settings import *
from sprite_loader import get_sprite_loader

class LocationManager:
    def __init__(self):
        self.sprite_loader = get_sprite_loader()
        self.current_location = "main_map"  # main_map или имя ментора
        self.player_position = pygame.math.Vector2(400, 400)
        self.return_position = pygame.math.Vector2(400, 400)  # Позиция для возврата на карту
        
        # Размеры локаций
        self.main_map_size = (1600, 1200)  # Размер основной карты
        self.room_size = (25 * TILE_SIZE, 20 * TILE_SIZE)  # Размер комнаты ментора
        
        # Камера для каждой локации
        self.camera_offset = pygame.math.Vector2()
        
    def enter_mentor_room(self, mentor_name):
        """Войти в комнату ментора"""
        self.current_location = mentor_name
        # Центрируем игрока в комнате
        self.player_position = pygame.math.Vector2(
            self.room_size[0] // 2,
            self.room_size[1] // 2
        )
        self.update_camera()
        
    def exit_to_main_map(self):
        """Вернуться на основную карту"""
        self.current_location = "main_map"
        self.player_position = self.return_position
        self.update_camera()
        
    def update_camera(self):
        """Обновляет камеру для текущей локации"""
        if self.current_location == "main_map":
            # Камера для основной карты
            target_x = self.player_position.x - SCREEN_WIDTH // 2
            target_y = self.player_position.y - SCREEN_HEIGHT // 2
            
            # Ограничиваем камеру размерами карты
            max_x = self.main_map_size[0] - SCREEN_WIDTH
            max_y = self.main_map_size[1] - SCREEN_HEIGHT
            
            target_x = max(0, min(target_x, max_x))
            target_y = max(0, min(target_y, max_y))
            
            self.camera_offset.x = target_x
            self.camera_offset.y = target_y
        else:
            # Камера для комнаты ментора
            target_x = self.player_position.x - SCREEN_WIDTH // 2
            target_y = self.player_position.y - SCREEN_HEIGHT // 2
            
            # Ограничиваем камеру размерами комнаты
            max_x = self.room_size[0] - SCREEN_WIDTH
            max_y = self.room_size[1] - SCREEN_HEIGHT
            
            target_x = max(0, min(target_x, max_x))
            target_y = max(0, min(target_y, max_y))
            
            self.camera_offset.x = target_x
            self.camera_offset.y = target_y
    
    def get_current_background(self):
        """Получить фон для текущей локации"""
        if self.current_location == "main_map":
            # Возвращаем основную карту
            return None  # Будет загружена в level.py
        else:
            # Возвращаем комнату ментора
            return self.sprite_loader.get_mentor_room(self.current_location)
    
    def check_door_interaction(self, player_pos):
        """Проверить взаимодействие с дверью для выхода из комнаты"""
        if self.current_location != "main_map":
            # Дверь находится в позиции (12, 18) в комнате
            door_pos = pygame.math.Vector2(12 * TILE_SIZE, 18 * TILE_SIZE)
            distance = player_pos.distance_to(door_pos)
            
            if distance < 50:  # Радиус взаимодействия
                return True
        return False
    
    def get_mentor_in_room(self):
        """Получить ментора в текущей комнате"""
        if self.current_location != "main_map":
            return self.current_location
        return None
    
    def draw_location_info(self, screen):
        """Отобразить информацию о текущей локации"""
        if self.current_location != "main_map":
            # Показываем подсказку для выхода
            font = pygame.font.Font(None, 24)
            exit_text = "Нажмите E у двери для выхода"
            text_surface = font.render(exit_text, True, WHITE)
            screen.blit(text_surface, (10, SCREEN_HEIGHT - 40))
            
            # Показываем название локации
            location_text = f"Локация: {self.current_location}"
            location_surface = font.render(location_text, True, YELLOW)
            screen.blit(location_surface, (10, 70)) 