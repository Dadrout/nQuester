import pygame
import sys
from settings import *
from player import Player
from level import Level
from quest_manager import QuestManager
from ui import UI
from minigames import MinigameManager
from sprite_loader import init_sprite_loader
from location_manager import LocationManager
from sound_manager import init_sound_manager, get_sound_manager
from achievements import init_achievement_manager, get_achievement_manager
from save_system import init_save_system, get_save_system
from main_menu import MainMenu, show_how_to_play, show_achievements, show_settings
from mentor_locations import MentorLocationManager
from boss_battle import BossBattle
from ending_screens import EndingScreen
from improvements import init_improvement_manager, get_improvement_manager

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("nQuester: Incubator Rush")
        self.clock = pygame.time.Clock()
        
        # Initialize sprite loader after pygame is initialized
        init_sprite_loader()
        
        # Initialize sound manager
        init_sound_manager()
        self.sound_manager = get_sound_manager()
        
        # Initialize achievement manager
        init_achievement_manager()
        self.achievement_manager = get_achievement_manager()
        
        # Initialize save system
        init_save_system()
        self.save_system = get_save_system()
        
        # Initialize improvement manager
        init_improvement_manager()
        self.improvement_manager = get_improvement_manager()
        
        # Game state
        self.state = EXPLORATION
        self.running = True
        self.in_mentor_location = False
        
        # Game objects
        self.player = Player(400, 400)
        self.level = Level("base")
        self.quest_manager = QuestManager()
        self.ui = UI()
        self.minigame_manager = MinigameManager(self.screen)
        self.location_manager = LocationManager()
        self.mentor_location_manager = MentorLocationManager()
        
        # Setup quests
        self.level.setup_quests(self.quest_manager)
        
        # Interaction
        self.current_npc = None
        self.last_interaction_time = 0
        
        # Victory condition
        self.game_won = False
        
        # Sound effects
        self.last_footstep_time = 0
        self.footstep_interval = 300  # milliseconds
        
        # Game statistics for achievements
        self.game_stats = {
            "completed_quests": 0,
            "swift_quests": 0,
            "ai_quests": 0,
            "typescript_quests": 0,
            "bugs_found": 0,
            "users": 0,
            "fastest_quest_time": 999,
            "perfect_quests": 0,
            "mentors_met": 0
        }
        
        # Auto-save timer
        self.last_autosave = pygame.time.get_ticks()
        self.autosave_interval = 30000  # 30 seconds
        
        # Initialize total quests count
        if self.improvement_manager:
            self.improvement_manager.progress_tracker.total_quests = len(self.quest_manager.quests_data)
        
        # Start background music
        if self.sound_manager:
            self.sound_manager.play_background_music()
            print("🎵 Background music started")
    
    def handle_events(self):
        """Handle game events"""
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == DIALOGUE:
                        self.ui.end_dialogue()
                        self.state = EXPLORATION
                    elif self.ui.journal_open:
                        self.ui.toggle_journal()
                    elif self.in_mentor_location:
                        # Exit mentor location
                        self.mentor_location_manager.exit_location()
                        self.in_mentor_location = False
                        # Play door close sound
                        if self.sound_manager:
                            self.sound_manager.play_door_close()
                    else:
                        self.running = False
                
                elif event.key == pygame.K_q or event.key == pygame.K_TAB:
                    if self.state == EXPLORATION:
                        self.ui.toggle_journal()
                
                elif event.key == pygame.K_e:
                    if self.state == EXPLORATION:
                        if self.in_mentor_location:
                            # In mentor location - interact with mentor
                            self.interact_with_mentor_in_location()
                        else:
                            # Check for NPC interaction on main map
                            if current_time - self.last_interaction_time > 500:  # Debounce
                                self.try_npc_interaction()
                                self.last_interaction_time = current_time
                    
                    elif self.state == DIALOGUE:
                        # Continue dialogue
                        if self.ui.next_dialogue_line():
                            # Dialogue finished - check if we need to start quest
                            if self.current_npc and self.current_npc.has_quest:
                                self.handle_quest_start()
                            self.state = EXPLORATION
                
                # Save/Load hotkeys
                elif event.key == pygame.K_F5:
                    # Quick save
                    if self.save_system:
                        self.save_system.auto_save(self)
                        if self.sound_manager:
                            self.sound_manager.play_sound("success")
                
                elif event.key == pygame.K_F9:
                    # Quick load
                    if self.save_system:
                        if self.save_system.load_autosave(self):
                            if self.sound_manager:
                                self.sound_manager.play_sound("success")
                        else:
                            if self.sound_manager:
                                self.sound_manager.play_sound("error")
    
    def try_npc_interaction(self):
        """Try to interact with nearby NPCs and doors"""
        # Check for door interaction (exit from mentor room)
        if self.location_manager.check_door_interaction(self.player.position):
            self.location_manager.exit_to_main_map()
            self.player.position = self.location_manager.player_position
            if self.sound_manager:
                self.sound_manager.play_door_close()
            return
            
        # Check for NPC interaction on main map
        if self.location_manager.current_location == "main_map":
            nearby_npcs = self.level.get_nearby_npcs(self.player)
            
            if nearby_npcs:
                npc = nearby_npcs[0]
                
                # Check if it's a mentor
                if npc.npc_type == "mentor":
                    # Enter mentor location
                    self.mentor_location_manager.enter_location(npc.name)
                    self.in_mentor_location = True
                    # Play door open sound
                    if self.sound_manager:
                        self.sound_manager.play_door_open()
                    return
                
                # Regular NPC interaction
                self.current_npc = npc
                interaction = npc.interact()
                
                # Play interaction sound
                if self.sound_manager:
                    self.sound_manager.play_sound("interaction")
                
                if interaction['type'] == 'quest_start':
                    self.ui.start_dialogue(interaction['dialogue'], interaction['npc_name'])
                    self.state = DIALOGUE
                elif interaction['type'] == 'dialogue':
                    self.ui.start_dialogue(interaction['dialogue'], interaction['npc_name'])
                    self.state = DIALOGUE
    
    def interact_with_mentor_in_location(self):
        """Interact with mentor in their personal location"""
        current_location = self.mentor_location_manager.get_current_location()
        if current_location:
            # Check if player is close enough to mentor
            if not current_location.check_mentor_interaction(current_location.get_player_position()):
                print("⚠️ Подойдите ближе к ментору для взаимодействия!")
                return
                
            mentor_name = current_location.mentor_name
            
            # Find the mentor NPC
            for npc in self.level.npcs:
                if npc.name == mentor_name:
                    self.current_npc = npc
                    break
            
            if self.current_npc:
                interaction = self.current_npc.interact()
                
                # Play interaction sound
                if self.sound_manager:
                    self.sound_manager.play_sound("interaction")
                
                if interaction['type'] == 'quest_start':
                    self.ui.start_dialogue(interaction['dialogue'], interaction['npc_name'])
                    self.state = DIALOGUE
                elif interaction['type'] == 'dialogue':
                    self.ui.start_dialogue(interaction['dialogue'], interaction['npc_name'])
                    self.state = DIALOGUE
    
    def handle_quest_start(self):
        """Handle quest start after dialogue"""
        if self.current_npc and self.current_npc.has_quest and (not self.current_npc.quest_completed or self.current_npc.quest_failed):
            quest_id = self.current_npc.quest_id
            quest_data = self.quest_manager.get_quest_data(quest_id)
            
            if quest_data:
                if quest_data["type"] == "minigame":
                    # Start quest and run minigame
                    self.quest_manager.start_quest(quest_id, self.player)
                    success = self.run_minigame(quest_data["minigame_id"])
                    
                    if success:
                        self.quest_manager.mark_minigame_completed(quest_id)
                        self.quest_manager.complete_quest(quest_id, self.player)
                        self.current_npc.complete_quest(self.player)
                        self.current_npc.quest_failed = False  # Reset failure state
                        
                        # Play success sound
                        if self.sound_manager:
                            self.sound_manager.play_sound("quest_complete")
                        
                        # Show user feedback immediately after success
                        user_feedback = quest_data.get("user_feedback", ["Отличная работа!"])
                        self.ui.start_dialogue(user_feedback, self.current_npc.name)
                        self.state = DIALOGUE
                        
                        # Check win condition
                        if self.player.current_users >= TARGET_USERS:
                            self.game_won = True
                    else:
                        # Quest failed
                        self.current_npc.fail_quest()
                        self.quest_manager.active_quests.pop(quest_id, None)
                        
                        # Play failure sound
                        if self.sound_manager:
                            self.sound_manager.play_sound("quest_fail")
                        
                        # Show failure feedback
                        failure_feedback = ["Не получилось! Попробуй еще раз!"]
                        self.ui.start_dialogue(failure_feedback, self.current_npc.name)
                        self.state = DIALOGUE
                
                elif quest_data["type"] == "boss_battle":
                    # Start boss battle
                    self.quest_manager.start_quest(quest_id, self.player)
                    success = self.run_boss_battle()
                    
                    if success:
                        self.quest_manager.mark_minigame_completed(quest_id)
                        self.quest_manager.complete_quest(quest_id, self.player)
                        self.current_npc.complete_quest()
                        self.current_npc.quest_failed = False
                        
                        # Play success sound
                        if self.sound_manager:
                            self.sound_manager.play_sound("quest_complete")
                        
                        # Show victory ending
                        ending_screen = EndingScreen(self.screen, is_victory=True)
                        ending_result = ending_screen.run()
                        
                        if ending_result == "exit":
                            return False
                        
                        # Show user feedback
                        user_feedback = quest_data.get("user_feedback", ["НЕВЕРОЯТНО! Ты победил босса!"])
                        self.ui.start_dialogue(user_feedback, self.current_npc.name)
                        self.state = DIALOGUE
                        
                        # Check win condition
                        if self.player.current_users >= TARGET_USERS:
                            self.game_won = True
                    else:
                        # Boss battle failed
                        self.current_npc.fail_quest()
                        self.quest_manager.active_quests.pop(quest_id, None)
                        
                        # Play failure sound
                        if self.sound_manager:
                            self.sound_manager.play_sound("quest_fail")
                        
                        # Show defeat ending
                        ending_screen = EndingScreen(self.screen, is_victory=False)
                        ending_result = ending_screen.run()
                        
                        if ending_result == "exit":
                            return False
                        
                        # Show failure feedback
                        failure_feedback = ["Босс оказался сильнее! Попробуй еще раз!"]
                        self.ui.start_dialogue(failure_feedback, self.current_npc.name)
                        self.state = DIALOGUE
                
                elif quest_data["type"] == "item_collection":
                    # Check if player has required items
                    required_items = quest_data.get("required_items", [])
                    has_all_items = all(item in self.player.inventory for item in required_items)
                    
                    if has_all_items:
                        # Complete quest
                        self.quest_manager.complete_quest(quest_id, self.player)
                        self.current_npc.complete_quest(self.player)
                        
                        # Remove items from inventory
                        for item in required_items:
                            if item in self.player.inventory:
                                self.player.inventory.pop(item, None)
                        
                        # Play success sound
                        if self.sound_manager:
                            self.sound_manager.play_sound("quest_complete")
                        
                        # Show user feedback
                        user_feedback = quest_data.get("user_feedback", ["✅ Все артефакты собраны!"])
                        self.ui.start_dialogue(user_feedback, self.current_npc.name)
                        self.state = DIALOGUE
                        
                        # Check if this was Diana's collector quest, give her final quest
                        if quest_id == "quest_diana_collector":
                            self.current_npc.set_quest("quest_diana_final", [
                                "Теперь, когда у тебя есть моя коллекция...",
                                "Покажи мне, что ты достоин получить мой главный артефакт!",
                                "Пройди специальную мини-игру: 'Коллекционер сокровищ'",
                                "Найди все спрятанные артефакты за ограниченное время!"
                            ])
                    else:
                        # Missing items
                        missing_items = [item for item in required_items if item not in self.player.inventory]
                        missing_text = ", ".join(missing_items)
                        feedback = [f"Тебе нужно собрать: {missing_text}"]
                        self.ui.start_dialogue(feedback, self.current_npc.name)
                        self.state = DIALOGUE
                
                elif quest_data["type"] == "clicker":
                    # Start clicker quest
                    self.quest_manager.start_quest(quest_id, self.player)
                    clicks_needed = quest_data.get("clicks_needed", 50)
                    time_limit = quest_data.get("time_limit", 30)
                    
                    success = self.minigame_manager.run_clicker_game(clicks_needed, time_limit)
                    
                    if success:
                        self.quest_manager.mark_minigame_completed(quest_id)
                        self.quest_manager.complete_quest(quest_id, self.player)
                        self.current_npc.complete_quest(self.player)
                        self.current_npc.quest_failed = False
                        
                        # Play success sound
                        if self.sound_manager:
                            self.sound_manager.play_sound("quest_complete")
                        
                        # Show user feedback
                        user_feedback = quest_data.get("user_feedback", ["Отличная работа!"])
                        self.ui.start_dialogue(user_feedback, self.current_npc.name)
                        self.state = DIALOGUE
                    else:
                        # Quest failed
                        self.current_npc.fail_quest()
                        self.quest_manager.active_quests.pop(quest_id, None)
                        
                        # Play failure sound
                        if self.sound_manager:
                            self.sound_manager.play_sound("quest_fail")
                        
                        # Show failure feedback
                        failure_feedback = ["Не получилось! Попробуй еще раз!"]
                        self.ui.start_dialogue(failure_feedback, self.current_npc.name)
                        self.state = DIALOGUE
                
                elif quest_data["type"] == "rhythm":
                    # Start rhythm quest
                    self.quest_manager.start_quest(quest_id, self.player)
                    beats_needed = quest_data.get("beats_needed", 20)
                    time_limit = quest_data.get("time_limit", 30)
                    
                    success = self.minigame_manager.run_rhythm_game(beats_needed, time_limit)
                    
                    if success:
                        self.quest_manager.mark_minigame_completed(quest_id)
                        self.quest_manager.complete_quest(quest_id, self.player)
                        self.current_npc.complete_quest(self.player)
                        self.current_npc.quest_failed = False
                        
                        # Play success sound
                        if self.sound_manager:
                            self.sound_manager.play_sound("quest_complete")
                        
                        # Show user feedback
                        user_feedback = quest_data.get("user_feedback", ["Отличная работа!"])
                        self.ui.start_dialogue(user_feedback, self.current_npc.name)
                        self.state = DIALOGUE
                    else:
                        # Quest failed
                        self.current_npc.fail_quest()
                        self.quest_manager.active_quests.pop(quest_id, None)
                        
                        # Play failure sound
                        if self.sound_manager:
                            self.sound_manager.play_sound("quest_fail")
                        
                        # Show failure feedback
                        failure_feedback = ["Не получилось! Попробуй еще раз!"]
                        self.ui.start_dialogue(failure_feedback, self.current_npc.name)
                        self.state = DIALOGUE
                
                elif quest_data["type"] == "color_picker":
                    # Start color picker quest
                    self.quest_manager.start_quest(quest_id, self.player)
                    colors_needed = quest_data.get("colors_needed", 5)
                    time_limit = quest_data.get("time_limit", 60)
                    
                    success = self.minigame_manager.run_color_picker_game(colors_needed, time_limit)
                    
                    if success:
                        self.quest_manager.mark_minigame_completed(quest_id)
                        self.quest_manager.complete_quest(quest_id, self.player)
                        self.current_npc.complete_quest(self.player)
                        self.current_npc.quest_failed = False
                        
                        # Play success sound
                        if self.sound_manager:
                            self.sound_manager.play_sound("quest_complete")
                        
                        # Show user feedback
                        user_feedback = quest_data.get("user_feedback", ["Отличная работа!"])
                        self.ui.start_dialogue(user_feedback, self.current_npc.name)
                        self.state = DIALOGUE
                    else:
                        # Quest failed
                        self.current_npc.fail_quest()
                        self.quest_manager.active_quests.pop(quest_id, None)
                        
                        # Play failure sound
                        if self.sound_manager:
                            self.sound_manager.play_sound("quest_fail")
                        
                        # Show failure feedback
                        failure_feedback = ["Не получилось! Попробуй еще раз!"]
                        self.ui.start_dialogue(failure_feedback, self.current_npc.name)
                        self.state = DIALOGUE
                
                elif quest_data["type"] == "fetch":
                    # Start fetch quest - player needs to collect items
                    self.quest_manager.start_quest(quest_id, self.player)
                    required_item = quest_data.get("item_to_fetch", "water_bottle")
                    
                    # For now, we'll simulate item collection
                    # In a full implementation, items would be scattered around the map
                    # and player would need to walk to them to collect
                    
                    # Simulate successful item collection
                    if not hasattr(self.player, 'inventory'):
                        self.player.inventory = {}
                    
                    self.player.add_item(required_item)
                    
                    # Complete quest
                    self.quest_manager.complete_quest(quest_id, self.player)
                    self.current_npc.complete_quest(self.player)
                    self.current_npc.quest_failed = False
                    
                    # Play success sound
                    if self.sound_manager:
                        self.sound_manager.play_sound("quest_complete")
                    
                    # Show user feedback
                    user_feedback = quest_data.get("user_feedback", ["Предмет найден! Спасибо!"])
                    self.ui.start_dialogue(user_feedback, self.current_npc.name)
                    self.state = DIALOGUE
        else:
            # Quest already completed or not available
            if self.current_npc and self.current_npc.quest_completed:
                self.ui.start_dialogue(["Квест уже выполнен! Спасибо за помощь!"], self.current_npc.name)
                self.state = DIALOGUE
    
    def run_minigame(self, minigame_id):
        """Run specified minigame"""
        # Play minigame music
        if self.sound_manager:
            self.sound_manager.play_music("minigame")
        
        result = False
        if minigame_id == "swift_debug":
            result = self.minigame_manager.run_swift_debug()
        elif minigame_id == "ai_training":
            result = self.minigame_manager.run_ai_training()
        elif minigame_id == "ts_quiz":
            result = self.minigame_manager.run_ts_quiz()
        elif minigame_id == "memory_leak_hunter":
            result = self.minigame_manager.run_memory_leak_hunter()
        elif minigame_id == "react_debug":
            result = self.minigame_manager.run_react_debug()
        elif minigame_id == "mobile_debug":
            result = self.minigame_manager.run_mobile_debug()
        elif minigame_id == "devops_pipeline":
            result = self.minigame_manager.run_devops_pipeline()
        elif minigame_id == "qa_testing":
            result = self.minigame_manager.run_qa_testing()
        elif minigame_id == "boss_challenge":
            result = self.minigame_manager.run_boss_challenge()
        elif minigame_id == "treasure_collector":
            result = self.minigame_manager.run_treasure_collector()
        elif minigame_id == "api_architect":
            result = self.minigame_manager.run_api_architect()
        elif minigame_id == "ui_designer":
            result = self.minigame_manager.run_ui_designer()
        else:
            result = True  # Default success for unknown minigames
        
        # Return to previous music
        if self.in_mentor_location and self.sound_manager:
            self.sound_manager.play_music("mentor_location")
        elif self.sound_manager:
            self.sound_manager.play_music("main_theme")
        
        return result
    
    def run_boss_battle(self):
        """Run boss battle"""
        try:
            # Play boss battle music
            if self.sound_manager:
                self.sound_manager.play_music("minigame")  # Use minigame music for boss battle
            
            # Create boss battle
            boss_battle = BossBattle(self.screen, self.player.current_users)
            result = boss_battle.run_battle()
            
            # Return to previous music
            if self.in_mentor_location and self.sound_manager:
                self.sound_manager.play_music("mentor_location")
            elif self.sound_manager:
                self.sound_manager.play_music("main_theme")
            
            return result
        except Exception as e:
            print(f"❌ Ошибка в битве с боссом: {e}")
            return False
    
    def update(self, dt):
        """Update game state"""
        if self.state == EXPLORATION:
            if self.in_mentor_location:
                # Update player in mentor location
                self.player.get_input()
                
                # Calculate movement based on input
                keys = pygame.key.get_pressed()
                dx = 0
                dy = 0
                
                # Use faster speed in mentor location
                mentor_speed = MENTOR_LOCATION_SPEED
                
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    dy = -mentor_speed * dt
                if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    dy = mentor_speed * dt
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    dx = -mentor_speed * dt
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    dx = mentor_speed * dt
                
                # Play footstep sound if moving
                if (dx != 0 or dy != 0) and self.sound_manager:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_footstep_time > self.footstep_interval:
                        self.sound_manager.play_footstep()
                        self.last_footstep_time = current_time
                
                # Update player animation even in mentor location
                self.player.update(dt)
                
                # Update position through mentor location manager
                self.mentor_location_manager.update_player_movement(dx, dy)
                
                # Update player position to match mentor location
                new_pos = self.mentor_location_manager.get_player_position()
                self.player.position.x = new_pos[0]
                self.player.position.y = new_pos[1]
                self.player.rect.center = (new_pos[0], new_pos[1])
            else:
                # Normal exploration
                old_pos = self.player.position.copy()
                self.player.update(dt)
                self.level.update(dt, self.player)
                
                # Play footstep sound if moving
                if self.player.position != old_pos and self.sound_manager:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_footstep_time > self.footstep_interval:
                        self.sound_manager.play_footstep()
                        self.last_footstep_time = current_time
        
        # Update game stats
        self.game_stats["users"] = self.player.current_users
        
        # Update improvement manager
        if self.improvement_manager:
            self.improvement_manager.update(dt)
        
        # Update achievements
        if self.achievement_manager:
            self.achievement_manager.update(self.game_stats)
        
        # Update UI animations
        self.ui.update_journal_gif_background(dt)
        self.ui.update_quest_gif_background(dt)
        self.ui.update_typing_animation(dt)
        
        # Update minigame GIF animations
        self.minigame_manager.update_minigame_gif_background(dt)
        
        # Auto-save
        current_time = pygame.time.get_ticks()
        if current_time - self.last_autosave > self.autosave_interval:
            if self.save_system:
                self.save_system.auto_save(self)
            self.last_autosave = current_time
        
        # Check for win condition
        if self.player.current_users >= TARGET_USERS and not self.game_won:
            self.show_victory_screen()
    
    def update_quest_stats(self, quest_id, success=True, time_taken=0):
        """Update statistics when quest is completed"""
        self.game_stats["completed_quests"] += 1
        
        # Track quest types
        if "swift" in quest_id.lower():
            self.game_stats["swift_quests"] += 1
        elif "ai" in quest_id.lower():
            self.game_stats["ai_quests"] += 1
        elif "ts" in quest_id.lower() or "typescript" in quest_id.lower():
            self.game_stats["typescript_quests"] += 1
        
        # Track fastest quest time
        if success and time_taken < self.game_stats["fastest_quest_time"]:
            self.game_stats["fastest_quest_time"] = time_taken
        
        # Track perfect quests (no retries)
        if success:
            self.game_stats["perfect_quests"] += 1
    
    def show_victory_screen(self):
        """Show victory screen"""
        self.game_won = True
        victory_messages = [
            "🎉 ПОЗДРАВЛЯЕМ! 🎉",
            f"Вы привлекли {self.player.current_users} пользователей!",
            "Ваш стартап готов к Demo Day!",
            "Инвесторы выстроились в очередь!",
            "",
            "🏆 ВЫ ПОБЕДИЛИ! 🏆",
            "nFactorial Incubator Rush завершен!",
            "Вы стали лучшим стартапером!",
            "",
            "Нажмите ESC для выхода"
        ]
        self.ui.start_dialogue(victory_messages, "nFactorial")
        self.state = DIALOGUE
    
    def draw(self):
        """Draw game"""
        self.screen.fill(BLACK)
        
        if self.state == EXPLORATION or self.state == DIALOGUE:
            if self.in_mentor_location:
                # Draw mentor location with player
                self.mentor_location_manager.draw_current_location(self.screen, self.player)
            else:
                # Draw main level
                self.level.draw(self.screen)
                
                # Draw player
                self.player.draw(self.screen, self.level.camera_offset)
            
            # Draw UI
            self.ui.display_hud(self.screen, self.player)
            
            if self.state == DIALOGUE:
                self.ui.display_dialogue(self.screen)
            
            # Draw journal
            self.ui.display_journal(self.screen, self.player, self.quest_manager)
            
            # Draw improvement system elements
            if self.improvement_manager:
                self.improvement_manager.draw_progress_bars(self.screen, self.player, self.quest_manager)
                self.improvement_manager.draw_reward_animations(self.screen)
                self.improvement_manager.draw_active_events(self.screen)
            
            # Draw achievement notifications
            if self.achievement_manager:
                self.achievement_manager.draw_notifications(self.screen)
            
            # Show win message
            if self.game_won and not self.ui.dialogue_active:
                self.draw_victory_overlay()
        
        pygame.display.flip()
    
    def draw_victory_overlay(self):
        """Draw victory overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(GREEN)
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        text = font.render("VICTORY!", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()

def run_game_with_menu():
    """Run the game with main menu"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("nQuester: Incubator Rush")
    
    # Initialize systems
    init_sprite_loader()
    init_sound_manager()
    init_achievement_manager()
    init_save_system()
    
    # Create a global player for settings
    from player import Player
    global_player = Player(0, 0)
    
    # Main menu loop
    while True:
        # Show main menu
        menu = MainMenu(screen)
        result = menu.run()
        
        if result == "start_game":
            # Show intro scene first
            from intro_scene import IntroScene
            intro = IntroScene(screen)
            intro_result = intro.run()
            
            if intro_result == "start_game":
                # Start the actual game
                game = Game()
                game.run()
            elif intro_result == "exit":
                break
        elif result == "how_to_play":
            show_how_to_play(screen)
        elif result == "achievements":
            show_achievements(screen)
        elif result == "settings":
            # Use the global player for settings
            show_settings(screen, global_player)
        elif result == "exit":
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game_with_menu() 