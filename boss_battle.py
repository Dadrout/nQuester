import pygame
import random
import time
import os
from settings import *
from sound_manager import get_sound_manager

class BossBattle:
    def __init__(self, screen, player_users):
        self.screen = screen
        self.player_users = player_users
        
        # Boss stats зависят от количества пользователей
        # Чем больше пользователей, тем слабее босс
        self.boss_hp = max(100, 500 - (player_users // 2))  # 10k юзеров = 0 HP, но min 100
        self.boss_max_hp = self.boss_hp
        self.boss_attack_power = max(10, 50 - (player_users // 200))
        self.boss_defense_power = max(5, 30 - (player_users // 300))
        
        # Player stats
        self.player_hp = 100
        self.player_max_hp = 100
        self.player_attack_power = 25
        self.player_defense_power = 15
        
        # Battle state
        self.battle_phase = "player_turn"  # player_turn, boss_turn, victory, defeat
        self.selected_action = 0  # 0=attack, 1=defend, 2=special, 3=demo
        self.battle_log = []
        self.animation_frame = 0
        
        # Load boss sprite
        self.load_boss_sprite()
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Battle UI
        self.action_buttons = [
            {"name": "Атака", "rect": pygame.Rect(50, 500, 150, 50)},
            {"name": "Защита", "rect": pygame.Rect(220, 500, 150, 50)},
            {"name": "Специальная атака", "rect": pygame.Rect(390, 500, 200, 50)},
            {"name": "ДЕМО АТАКА", "rect": pygame.Rect(610, 500, 200, 50)}
        ]
        
        # Special moves
        self.special_moves = [
            {"name": "Код-ревью", "damage": 40, "cost": 20},
            {"name": "Рефакторинг", "damage": 35, "cost": 15},
            {"name": "Оптимизация", "damage": 50, "cost": 30}
        ]
        
        self.clock = pygame.time.Clock()
    
    def load_boss_sprite(self):
        """Load boss sprite from main_boss.jpg"""
        try:
            boss_path = os.path.join("Mentors", "main_boss.jpg")
            if os.path.exists(boss_path):
                boss_image = pygame.image.load(boss_path)
                # Scale to appropriate size for battle
                self.boss_sprite = pygame.transform.scale(boss_image, (200, 200))
                print(f"✅ Загружен спрайт босса: {boss_path}")
            else:
                # Fallback sprite
                self.boss_sprite = pygame.Surface((200, 200))
                self.boss_sprite.fill(RED)
                print(f"⚠️ Файл босса не найден: {boss_path}")
        except Exception as e:
            print(f"❌ Ошибка загрузки спрайта босса: {e}")
            self.boss_sprite = pygame.Surface((200, 200))
            self.boss_sprite.fill(RED)
    
    def calculate_damage(self, attacker_attack, defender_defense, is_special=False):
        """Calculate damage with some randomness"""
        base_damage = attacker_attack - defender_defense
        if is_special:
            base_damage += 10
        
        # Add randomness
        damage = max(1, base_damage + random.randint(-5, 10))
        return damage
    
    def perform_player_attack(self):
        """Player attacks boss"""
        damage = self.calculate_damage(self.player_attack_power, self.boss_defense_power)
        self.boss_hp = max(0, self.boss_hp - damage)
        self.battle_log.append(f"Вы нанесли {damage} урона!")
        
        if self.boss_hp <= 0:
            self.battle_phase = "victory"
        else:
            self.battle_phase = "boss_turn"
    
    def perform_player_defend(self):
        """Player defends, reducing next damage"""
        self.player_defense_power += 10
        self.battle_log.append("Вы заняли оборонительную позицию!")
        self.battle_phase = "boss_turn"
    
    def perform_player_special_attack(self):
        """Player uses special attack"""
        if self.selected_action < len(self.special_moves):
            move = self.special_moves[self.selected_action]
            if self.player_hp > move["cost"]:
                damage = self.calculate_damage(self.player_attack_power, self.boss_defense_power, True)
                self.boss_hp = max(0, self.boss_hp - damage)
                self.player_hp -= move["cost"]
                self.battle_log.append(f"Специальная атака '{move['name']}' нанесла {damage} урона!")
                
                if self.boss_hp <= 0:
                    self.battle_phase = "victory"
                else:
                    self.battle_phase = "boss_turn"
            else:
                self.battle_log.append("Недостаточно HP для специальной атаки!")
                self.battle_phase = "player_turn"
    
    def perform_boss_attack(self):
        """Boss attacks player"""
        # Reset defense bonus
        self.player_defense_power = max(15, self.player_defense_power - 5)
        
        damage = self.calculate_damage(self.boss_attack_power, self.player_defense_power)
        self.player_hp = max(0, self.player_hp - damage)
        self.battle_log.append(f"Босс нанес {damage} урона!")
        
        if self.player_hp <= 0:
            self.battle_phase = "defeat"
        else:
            self.battle_phase = "player_turn"
    
    def perform_demo_attack(self):
        """Демо-атака: убивает босса за 1 удар"""
        self.boss_hp = 0
        self.battle_log.append("ДЕМО АТАКА! Босс повержен одним ударом!")
        self.battle_phase = "victory"
    
    def draw_battle_screen(self):
        """Draw the battle screen"""
        # Background
        self.screen.fill((20, 20, 40))
        
        # Draw boss
        boss_x = SCREEN_WIDTH // 2 - 100
        boss_y = 100
        self.screen.blit(self.boss_sprite, (boss_x, boss_y))
        
        # Boss HP bar
        hp_percentage = self.boss_hp / self.boss_max_hp
        hp_bar_width = 400
        hp_bar_height = 30
        hp_bar_x = SCREEN_WIDTH // 2 - hp_bar_width // 2
        hp_bar_y = 50
        
        # HP bar background
        pygame.draw.rect(self.screen, (100, 100, 100), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))
        # HP bar fill
        pygame.draw.rect(self.screen, (255, 0, 0), (hp_bar_x, hp_bar_y, hp_bar_width * hp_percentage, hp_bar_height))
        # HP bar border
        pygame.draw.rect(self.screen, WHITE, (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), 2)
        
        # Boss HP text
        hp_text = f"Босс HP: {self.boss_hp}/{self.boss_max_hp}"
        hp_surface = self.font_medium.render(hp_text, True, WHITE)
        self.screen.blit(hp_surface, (hp_bar_x, hp_bar_y - 30))
        
        # Player HP bar
        player_hp_percentage = self.player_hp / self.player_max_hp
        player_hp_bar_x = 50
        player_hp_bar_y = SCREEN_HEIGHT - 100
        player_hp_bar_width = 300
        player_hp_bar_height = 25
        
        # Player HP bar background
        pygame.draw.rect(self.screen, (100, 100, 100), (player_hp_bar_x, player_hp_bar_y, player_hp_bar_width, player_hp_bar_height))
        # Player HP bar fill
        pygame.draw.rect(self.screen, (0, 255, 0), (player_hp_bar_x, player_hp_bar_y, player_hp_bar_width * player_hp_percentage, player_hp_bar_height))
        # Player HP bar border
        pygame.draw.rect(self.screen, WHITE, (player_hp_bar_x, player_hp_bar_y, player_hp_bar_width, player_hp_bar_height), 2)
        
        # Player HP text
        player_hp_text = f"Ваше HP: {self.player_hp}/{self.player_max_hp}"
        player_hp_surface = self.font_medium.render(player_hp_text, True, WHITE)
        self.screen.blit(player_hp_surface, (player_hp_bar_x, player_hp_bar_y - 30))
        
        # Battle log
        log_y = 350
        for i, log_entry in enumerate(self.battle_log[-5:]):  # Show last 5 entries
            log_surface = self.font_small.render(log_entry, True, WHITE)
            self.screen.blit(log_surface, (50, log_y + i * 25))
        
        # Action buttons
        for i, button in enumerate(self.action_buttons):
            color = GRAY if i == self.selected_action else UI_BG_COLOR[:3]
            pygame.draw.rect(self.screen, color, button["rect"])
            pygame.draw.rect(self.screen, WHITE, button["rect"], 2)
            
            text_surface = self.font_medium.render(button["name"], True, WHITE)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)
        
        # Special moves info
        if self.selected_action == 2:  # Special attack selected
            special_y = 570
            for i, move in enumerate(self.special_moves):
                move_text = f"{i+1}. {move['name']} - Урон: {move['damage']}, Стоимость: {move['cost']} HP"
                move_surface = self.font_small.render(move_text, True, YELLOW)
                self.screen.blit(move_surface, (50, special_y + i * 20))
        
        # Battle phase indicator
        if self.battle_phase == "player_turn":
            phase_text = "Ваш ход - выберите действие"
        elif self.battle_phase == "boss_turn":
            phase_text = "Ход босса..."
        elif self.battle_phase == "victory":
            phase_text = "ПОБЕДА! Босс повержен!"
        elif self.battle_phase == "defeat":
            phase_text = "ПОРАЖЕНИЕ! Попробуйте еще раз!"
        
        phase_surface = self.font_large.render(phase_text, True, YELLOW)
        phase_rect = phase_surface.get_rect(center=(SCREEN_WIDTH // 2, 320))
        self.screen.blit(phase_surface, phase_rect)
        
        # Instructions
        instructions = [
            "WASD - выбор действия",
            "ENTER - подтвердить",
            "ESC - выйти из боя"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_surface = self.font_small.render(instruction, True, GRAY)
            self.screen.blit(inst_surface, (SCREEN_WIDTH - 200, 50 + i * 25))
    
    def handle_input(self, event):
        """Handle player input during battle"""
        if event.type == pygame.KEYDOWN:
            if self.battle_phase == "player_turn":
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.selected_action = (self.selected_action - 1) % len(self.action_buttons)
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.selected_action = (self.selected_action + 1) % len(self.action_buttons)
                elif event.key == pygame.K_RETURN:
                    if self.selected_action == 0:
                        self.perform_player_attack()
                    elif self.selected_action == 1:
                        self.perform_player_defend()
                    elif self.selected_action == 2:
                        self.perform_player_special_attack()
                    elif self.selected_action == 3:
                        self.perform_demo_attack()
                elif event.key == pygame.K_ESCAPE:
                    self.battle_phase = "defeat"
            elif event.key == pygame.K_ESCAPE:
                return "exit"
        
        return None
    
    def update(self, dt):
        """Update battle state"""
        if self.battle_phase == "boss_turn":
            # Add delay for boss turn
            self.animation_frame += dt
            if self.animation_frame > 1.0:  # 1 second delay
                self.perform_boss_attack()
                self.animation_frame = 0
    
    def run_battle(self):
        """Run the complete boss battle"""
        print(f"🎮 Начинается битва с боссом!")
        print(f"👥 Пользователи игрока: {self.player_users}")
        print(f"💪 Сила босса: HP={self.boss_hp}, Атака={self.boss_attack_power}, Защита={self.boss_defense_power}")
        
        while True:
            dt = self.clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                result = self.handle_input(event)
                if result == "exit":
                    return False
            
            self.update(dt)
            self.draw_battle_screen()
            pygame.display.flip()
            
            # Check battle end conditions
            if self.battle_phase == "victory":
                pygame.time.wait(2000)  # Show victory for 2 seconds
                return True
            elif self.battle_phase == "defeat":
                pygame.time.wait(2000)  # Show defeat for 2 seconds
                return False 