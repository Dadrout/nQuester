import json
import os
import pickle
from datetime import datetime
from sound_manager import get_sound_manager

class SaveSystem:
    def __init__(self):
        self.save_dir = "data/saves/"
        os.makedirs(self.save_dir, exist_ok=True)
    
    def save_game(self, game_state, filename=None):
        """Save game state to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"save_{timestamp}.json"
        
        filepath = os.path.join(self.save_dir, filename)
        
        try:
            # Prepare save data
            save_data = {
                "timestamp": datetime.now().isoformat(),
                "player": {
                    "position": [game_state.player.position.x, game_state.player.position.y],
                    "current_users": game_state.player.current_users,
                    "inventory": game_state.player.inventory,
                    "quest_log": game_state.player.quest_log
                },
                "game_stats": game_state.game_stats,
                "completed_quests": game_state.quest_manager.completed_quests,
                "active_quests": list(game_state.quest_manager.active_quests.keys()),
                "achievements": {
                    achievement_id: achievement.unlocked 
                    for achievement_id, achievement in game_state.achievement_manager.achievements.items()
                }
            }
            
            # Save to JSON file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Game saved: {filepath}")
            
            # Play save success sound
            sound_manager = get_sound_manager()
            if sound_manager:
                sound_manager.play_success()
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to save game: {e}")
            return False
    
    def load_game(self, game_state, filename):
        """Load game state from file"""
        filepath = os.path.join(self.save_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"❌ Save file not found: {filepath}")
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Restore player data
            player_data = save_data.get("player", {})
            if "position" in player_data:
                game_state.player.position.x, game_state.player.position.y = player_data["position"]
            if "current_users" in player_data:
                game_state.player.current_users = player_data["current_users"]
            if "inventory" in player_data:
                game_state.player.inventory = player_data["inventory"]
            if "quest_log" in player_data:
                game_state.player.quest_log = player_data["quest_log"]
            
            # Restore game stats
            if "game_stats" in save_data:
                game_state.game_stats.update(save_data["game_stats"])
            
            # Restore quest data
            if "completed_quests" in save_data:
                game_state.quest_manager.completed_quests = save_data["completed_quests"]
            if "active_quests" in save_data:
                for quest_id in save_data["active_quests"]:
                    quest_data = game_state.quest_manager.get_quest_data(quest_id)
                    if quest_data:
                        game_state.quest_manager.active_quests[quest_id] = quest_data
            
            # Restore achievements
            if "achievements" in save_data and game_state.achievement_manager:
                for achievement_id, unlocked in save_data["achievements"].items():
                    if achievement_id in game_state.achievement_manager.achievements:
                        game_state.achievement_manager.achievements[achievement_id].unlocked = unlocked
            
            print(f"✅ Game loaded: {filepath}")
            
            # Play load success sound
            sound_manager = get_sound_manager()
            if sound_manager:
                sound_manager.play_success()
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to load game: {e}")
            return False
    
    def get_save_files(self):
        """Get list of available save files"""
        save_files = []
        if os.path.exists(self.save_dir):
            for filename in os.listdir(self.save_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.save_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            save_data = json.load(f)
                        
                        save_info = {
                            "filename": filename,
                            "timestamp": save_data.get("timestamp", ""),
                            "users": save_data.get("player", {}).get("current_users", 0),
                            "completed_quests": len(save_data.get("completed_quests", [])),
                            "filepath": filepath
                        }
                        save_files.append(save_info)
                    except:
                        continue
        
        # Sort by timestamp (newest first)
        save_files.sort(key=lambda x: x["timestamp"], reverse=True)
        return save_files
    
    def auto_save(self, game_state):
        """Auto-save game"""
        return self.save_game(game_state, "autosave.json")
    
    def load_autosave(self, game_state):
        """Load auto-save if available"""
        return self.load_game(game_state, "autosave.json")
    
    def delete_save(self, filename):
        """Delete a save file"""
        filepath = os.path.join(self.save_dir, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"✅ Deleted save: {filename}")
                return True
            except Exception as e:
                print(f"❌ Failed to delete save: {e}")
                return False
        return False

# Global save system
save_system = None

def init_save_system():
    """Initialize the global save system"""
    global save_system
    save_system = SaveSystem()
    return save_system

def get_save_system():
    """Get the global save system"""
    return save_system 