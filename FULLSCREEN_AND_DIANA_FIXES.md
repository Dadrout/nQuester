# Fullscreen and Diana Image Fixes

## Issues Fixed

### 1. Diana Mentor Image Not Loading
**Problem**: Diana's image wasn't being loaded because she wasn't included in the mentor files list in `sprite_loader.py`.

**Fix**: 
- Added "Diana.png" and "Tamyrlan.png" to the mentor files list in `sprite_loader.py`
- Now Diana's face will properly load and display in dialogues

**Files Changed**:
- `sprite_loader.py`: Added Diana and Tamyrlan to mentor_files list

### 2. Fullscreen Functionality
**Problem**: Game didn't have fullscreen support.

**Fix**: 
- Added fullscreen toggle functionality with F11 key
- Implemented in both main game and main menu
- Added proper screen mode switching

**Files Changed**:
- `main.py`: Added fullscreen support to Game class
- `main_menu.py`: Added fullscreen support to MainMenu class

## New Features

### Fullscreen Controls
- **F11**: Toggle between fullscreen and windowed mode
- Works in main menu and during gameplay
- Automatically detects screen resolution for fullscreen mode

### Updated Instructions
- Main menu now shows F11 for fullscreen toggle
- How to play screen includes fullscreen information
- All UI elements properly scale with screen size

## Technical Details

### Fullscreen Implementation
```python
def toggle_fullscreen(self):
    """Toggle between fullscreen and windowed mode"""
    self.fullscreen = not self.fullscreen
    if self.fullscreen:
        # Get the display info for fullscreen
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    else:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
```

### Diana Image Loading
```python
mentor_files = [
    "Alikhan.png", "Alibeck.png", "Bahredin.png", "Bahaudin.png",
    "Gaziz.png", "Shoqan.png", "Zhasulan.png", "Aimurat.png", "Bernar.png",
    "Diana.png", "Tamyrlan.png"  # Added Diana and Tamyrlan
]
```

## Testing

The fixes ensure that:
1. ✅ Diana mentor's image loads properly in dialogues
2. ✅ Fullscreen mode works with F11 key
3. ✅ All UI elements scale correctly in fullscreen
4. ✅ Game performance is maintained in both modes

## Usage

- Press **F11** at any time to toggle fullscreen mode
- Diana mentor will now show her proper image in dialogues
- All other mentors continue to work as before 