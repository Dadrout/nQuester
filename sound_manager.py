import pygame
import os
import random
import math
import numpy as np
from settings import *

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_tracks = {}
        self.current_music = None
        self.sound_enabled = SOUND_ENABLED
        self.music_enabled = MUSIC_ENABLED
        self.background_music_file = "alexander-nakarada-superepic(chosic.com).mp3"
        
        # Create sounds directory
        os.makedirs(SOUNDS_PATH, exist_ok=True)
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.mixer_available = True
        except:
            print("⚠️ Sound system not available")
            self.mixer_available = False
            return
        
        # Load background music
        self.load_background_music()
        
        # Generate default sounds
        self.generate_default_sounds()
        self.load_sounds()
    
    def load_background_music(self):
        """Load the main background music file"""
        if not self.mixer_available:
            return
            
        music_path = self.background_music_file
        if os.path.exists(music_path):
            try:
                # Set music volume
                pygame.mixer.music.set_volume(MUSIC_VOLUME)
                print(f"✅ Background music loaded: {music_path}")
            except Exception as e:
                print(f"⚠️ Failed to load background music: {e}")
        else:
            print(f"⚠️ Background music file not found: {music_path}")
    
    def play_background_music(self):
        """Play the main background music in loop"""
        if not self.music_enabled or not self.mixer_available:
            return
            
        music_path = self.background_music_file
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                pygame.mixer.music.set_volume(MUSIC_VOLUME)
                print("🎵 Background music started")
            except Exception as e:
                print(f"⚠️ Failed to play background music: {e}")
    
    def stop_background_music(self):
        """Stop background music"""
        if self.mixer_available:
            pygame.mixer.music.stop()
            print("🔇 Background music stopped")
    
    def pause_background_music(self):
        """Pause background music"""
        if self.mixer_available:
            pygame.mixer.music.pause()
    
    def unpause_background_music(self):
        """Unpause background music"""
        if self.mixer_available:
            pygame.mixer.music.unpause()
    
    def set_background_music_volume(self, volume):
        """Set background music volume (0.0 to 1.0)"""
        if self.mixer_available:
            pygame.mixer.music.set_volume(volume)

    def generate_default_sounds(self):
        """Generate simple sound effects using numpy and pygame.sndarray"""
        if not self.mixer_available:
            return
        
        sample_rate = 22050
        duration = 0.1  # seconds
        samples = int(sample_rate * duration)
        
        # Create a simple beep sound (sine wave)
        frequency = 800  # Hz
        amplitude = 0.3
        t = np.linspace(0, duration, samples, False)
        wave = amplitude * np.sin(2 * np.pi * frequency * t)
        audio = np.array(wave * 32767, dtype=np.int16)
        # Make stereo if needed
        mixer_init = pygame.mixer.get_init()
        if mixer_init and mixer_init[2] == 2:
            audio = np.column_stack((audio, audio))
        sound_surface = pygame.sndarray.make_sound(audio)
        # Note: pygame.mixer.Sound doesn't have a save method
        # We'll use the sound directly without saving to file
    
    def load_sounds(self):
        """Load all sound effects"""
        if not self.mixer_available:
            return
        sound_files = {
            "interaction": "interaction.wav",
            "quest_complete": "quest_complete.wav", 
            "quest_fail": "quest_fail.wav",
            "button_click": "button_click.wav",
            "success": "success.wav",
            "error": "error.wav",
            "footstep": "footstep.wav",
            "door_open": "door_open.wav",
            "door_close": "door_close.wav",
            "typing": "typing.wav",
            "notification": "notification.wav",
            "achievement": "achievement.wav",
            "level_up": "level_up.wav",
            "coin": "coin.wav",
            "menu_select": "menu_select.wav",
            "menu_confirm": "menu_confirm.wav",
            "ambient_city": "ambient_city.wav",
            "ambient_office": "ambient_office.wav"
        }
        for sound_name, filename in sound_files.items():
            filepath = os.path.join(SOUNDS_PATH, filename)
            if os.path.exists(filepath):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                    self.sounds[sound_name].set_volume(SOUND_VOLUME)
                except:
                    print(f"⚠️ Failed to load sound: {filename}")
            else:
                self.create_simple_sound(sound_name, filename)
    
    def create_simple_sound(self, sound_name, filename):
        """Create a simple sound effect using numpy"""
        if not self.mixer_available:
            return
        sample_rate = 22050
        duration = 0.1
        samples = int(sample_rate * duration)
        frequencies = {
            "interaction": 800,
            "quest_complete": 1200,
            "quest_fail": 400,
            "button_click": 600,
            "success": 1000,
            "error": 300,
            "footstep": 200,
            "door_open": 500,
            "door_close": 400,
            "typing": 1500,
            "notification": 900,
            "achievement": 1500,
            "level_up": 2000,
            "coin": 1200,
            "menu_select": 700,
            "menu_confirm": 800,
            "ambient_city": 300,
            "ambient_office": 400
        }
        frequency = frequencies.get(sound_name, 800)
        amplitude = 0.3
        t = np.linspace(0, duration, samples, False)
        wave = amplitude * np.sin(2 * np.pi * frequency * t)
        audio = np.array(wave * 32767, dtype=np.int16)
        mixer_init = pygame.mixer.get_init()
        if mixer_init and mixer_init[2] == 2:
            audio = np.column_stack((audio, audio))
        sound_surface = pygame.sndarray.make_sound(audio)
        self.sounds[sound_name] = sound_surface
        self.sounds[sound_name].set_volume(SOUND_VOLUME)
        # Optionally save the sound
        # pygame.mixer.Sound.save(sound_surface, os.path.join(SOUNDS_PATH, filename))
    
    def play_sound(self, sound_name):
        if not self.sound_enabled or not self.mixer_available:
            return
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def play_footstep(self):
        """Play footstep sound when player moves"""
        self.play_sound("footstep")
    
    def play_door_open(self):
        """Play door opening sound"""
        self.play_sound("door_open")
    
    def play_door_close(self):
        """Play door closing sound"""
        self.play_sound("door_close")
    
    def play_typing(self):
        """Play typing sound for UI interactions"""
        self.play_sound("typing")
    
    def play_notification(self):
        """Play notification sound"""
        self.play_sound("notification")
    
    def play_achievement(self):
        """Play achievement sound"""
        self.play_sound("achievement")
    
    def play_level_up(self):
        """Play level up sound"""
        self.play_sound("level_up")
    
    def play_coin(self):
        """Play coin sound for rewards"""
        self.play_sound("coin")
    
    def play_menu_select(self):
        """Play menu selection sound"""
        self.play_sound("menu_select")
    
    def play_menu_confirm(self):
        """Play menu confirmation sound"""
        self.play_sound("menu_confirm")
    
    def play_ambient_city(self):
        """Play city ambient sound"""
        self.play_sound("ambient_city")
    
    def play_ambient_office(self):
        """Play office ambient sound"""
        self.play_sound("ambient_office")
    
    def play_quest_start(self):
        """Play quest start sound"""
        self.play_sound("quest_start")
    
    def play_quest_complete(self):
        """Play quest completion sound"""
        self.play_sound("quest_complete")
    
    def play_quest_fail(self):
        """Play quest failure sound"""
        self.play_sound("quest_fail")
    
    def play_button_click(self):
        """Play button click sound"""
        self.play_sound("button_click")
    
    def play_success(self):
        """Play success sound"""
        self.play_sound("success")
    
    def play_error(self):
        """Play error sound"""
        self.play_sound("error")
    
    def play_interaction(self):
        """Play interaction sound"""
        self.play_sound("interaction")
    
    def play_music(self, track_name=None):
        """Play background music - now uses the MP3 file"""
        if not self.music_enabled or not self.mixer_available:
            return
        
        # Use the main background music for all scenarios
        self.play_background_music()
    
    def stop_music(self):
        """Stop all music"""
        if self.mixer_available:
            pygame.mixer.music.stop()
    
    def set_sound_volume(self, volume):
        """Set sound effects volume"""
        for sound in self.sounds.values():
            sound.set_volume(volume)
    
    def set_music_volume(self, volume):
        """Set music volume"""
        if self.mixer_available:
            pygame.mixer.music.set_volume(volume)
    
    def toggle_sound(self):
        """Toggle sound effects on/off"""
        self.sound_enabled = not self.sound_enabled
    
    def toggle_music(self):
        """Toggle music on/off"""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_music()
        else:
            self.play_background_music()

sound_manager = None

def init_sound_manager():
    global sound_manager
    sound_manager = SoundManager()
    return sound_manager

def get_sound_manager():
    return sound_manager 