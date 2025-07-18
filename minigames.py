import pygame
import random
import time
import os
from settings import *
from PIL import Image
from sound_manager import get_sound_manager

class MinigameManager:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # GIF background for minigames
        self.minigame_gif_frames = []
        self.minigame_current_frame = 0
        self.minigame_frame_delay = 0.1
        self.minigame_last_frame_time = 0
        self.load_minigame_gif_background()
    
    def load_minigame_gif_background(self):
        """Load GIF background for minigames"""
        try:
            gif_path = "tumblr_owi25v6uAo1r4gsiio1_1280_gif (1000×300).gif"
            print(f"🔍 Ищем GIF файл для мини-игр: {gif_path}")
            if os.path.exists(gif_path):
                print(f"✅ Файл найден для мини-игр: {gif_path}")
                # Open GIF with PIL
                gif = Image.open(gif_path)
                
                # Extract frames
                frame_count = getattr(gif, 'n_frames', 1)
                print(f"📊 Количество кадров в GIF для мини-игр: {frame_count}")
                for frame in range(frame_count):
                    gif.seek(frame)
                    # Convert PIL image to pygame surface
                    frame_surface = pygame.image.fromstring(gif.convert('RGBA').tobytes(), gif.size, 'RGBA')
                    
                    # Scale to fit screen
                    frame_surface = pygame.transform.scale(frame_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    
                    # Add dark overlay for better text visibility
                    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    overlay.set_alpha(80)
                    overlay.fill((0, 0, 0))
                    frame_surface.blit(overlay, (0, 0))
                    
                    self.minigame_gif_frames.append(frame_surface)
                
                print(f"✅ Загружено {len(self.minigame_gif_frames)} кадров GIF-фона для мини-игр")
            else:
                print(f"⚠️ GIF файл не найден для мини-игр: {gif_path}")
        except Exception as e:
            print(f"❌ Ошибка загрузки GIF для мини-игр: {e}")
    
    def update_minigame_gif_background(self, dt):
        """Update minigame GIF animation"""
        if self.minigame_gif_frames:
            self.minigame_last_frame_time += dt
            if self.minigame_last_frame_time >= self.minigame_frame_delay:
                self.minigame_current_frame = (self.minigame_current_frame + 1) % len(self.minigame_gif_frames)
                self.minigame_last_frame_time = 0
    
    def draw_minigame_background(self):
        """Draw GIF background for minigames"""
        if self.minigame_gif_frames:
            # Draw current GIF frame
            current_frame = self.minigame_gif_frames[self.minigame_current_frame]
            self.screen.blit(current_frame, (0, 0))
        else:
            # Fallback to black background
            self.screen.fill(BLACK)
        
    def draw_text_with_background(self, text, font, color, position, bg_color=(0, 0, 0, 180)):
        """Draw text with semi-transparent background for better visibility"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        # Create background surface
        bg_surface = pygame.Surface((text_rect.width + 20, text_rect.height + 10))
        bg_surface.set_alpha(bg_color[3])
        bg_surface.fill(bg_color[:3])
        
        # Position background
        bg_rect = bg_surface.get_rect()
        if isinstance(position, tuple):
            bg_rect.center = position
        else:
            bg_rect.center = position.center
        
        # Draw background and text
        self.screen.blit(bg_surface, bg_rect)
        text_rect.center = bg_rect.center
        self.screen.blit(text_surface, text_rect)
        
        return text_rect
    
    def run_swift_debug(self):
        """Swift Debug Showdown minigame"""
        # Code lines with one bug
        code_lines = [
            "let name = \"Alex\"",  # Correct
            "var age: Int = 25",   # Correct  
            "let users = 1000",    # Correct
            "const isActive = true",  # BUG: should be 'let'
            "print(\"Hello World\")"  # Correct
        ]
        
        bug_line = 3  # Line with bug (0-indexed)
        start_time = time.time()
        time_limit = 15
        
        clock = pygame.time.Clock()
        
        while True:
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            current_time = time.time()
            remaining_time = time_limit - (current_time - start_time)
            
            if remaining_time <= 0:
                # Show failure feedback
                self.draw_minigame_background()
                title = self.font_large.render("Время истекло!", True, RED)
                title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
                self.screen.blit(title, title_rect)
                
                feedback_text = "Нужно найти ошибку за 15 секунд"
                feedback_surface = self.font_medium.render(feedback_text, True, YELLOW)
                feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH//2, 250))
                self.screen.blit(feedback_surface, feedback_rect)
                
                # Play failure sound
                sound_manager = get_sound_manager()
                if sound_manager:
                    sound_manager.play_quest_fail()
                
                pygame.display.flip()
                pygame.time.wait(2000)  # Show feedback for 2 seconds
                return False  # Time's up, failed
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if clicked on bug line
                    for i, line in enumerate(code_lines):
                        line_y = 200 + i * 40
                        if 100 <= mouse_pos[0] <= 800 and line_y <= mouse_pos[1] <= line_y + 30:
                            if i == bug_line:
                                # Play success sound
                                sound_manager = get_sound_manager()
                                if sound_manager:
                                    sound_manager.play_quest_complete()
                                return True  # Found the bug!
                            else:
                                # Ошибка: не та строка
                                self.draw_minigame_background()
                                title = self.font_large.render("Это не ошибка!", True, RED)
                                title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
                                self.screen.blit(title, title_rect)
                                feedback_text = "Попробуй снова через NPC!"
                                feedback_surface = self.font_medium.render(feedback_text, True, YELLOW)
                                feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH//2, 250))
                                self.screen.blit(feedback_surface, feedback_rect)
                                
                                # Play error sound
                                sound_manager = get_sound_manager()
                                if sound_manager:
                                    sound_manager.play_error()
                                
                                pygame.display.flip()
                                pygame.time.wait(2000)
                                return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            
            # Update GIF animation
            self.update_minigame_gif_background(dt)
            
            # Draw minigame
            self.draw_minigame_background()
            
            # Title
            self.draw_text_with_background("Swift Debug Showdown", self.font_large, WHITE, (SCREEN_WIDTH//2, 100))
            
            # Timer
            timer_text = f"Время: {remaining_time:.1f}s"
            self.draw_text_with_background(timer_text, self.font_medium, RED, (100, 30))
            
            # Instructions
            instruction = "Найдите ошибку в коде (кликните на строку с багом):"
            self.draw_text_with_background(instruction, self.font_medium, WHITE, (SCREEN_WIDTH//2, 150))
            
            # Code lines
            for i, line in enumerate(code_lines):
                y_pos = 200 + i * 40
                color = WHITE  # All lines look normal
                
                # Create background for code line
                line_text = f"{i+1}. {line}"
                line_surface = self.font_medium.render(line_text, True, color)
                line_rect = line_surface.get_rect()
                
                # Background for code line
                bg_surface = pygame.Surface((line_rect.width + 20, line_rect.height + 8))
                bg_surface.set_alpha(200)
                bg_surface.fill((0, 0, 0))
                bg_rect = bg_surface.get_rect()
                bg_rect.topleft = (90, y_pos - 4)
                
                # Highlight on hover
                mouse_pos = pygame.mouse.get_pos()
                if 100 <= mouse_pos[0] <= 800 and y_pos <= mouse_pos[1] <= y_pos + 30:
                    bg_surface.fill((50, 50, 50))
                    pygame.draw.rect(self.screen, GRAY, (90, y_pos-5, 720, 35), 2)
                
                self.screen.blit(bg_surface, bg_rect)
                self.screen.blit(line_surface, (100, y_pos))
            
            pygame.display.flip()
            clock.tick(60)
    
    def run_ai_training(self):
        """AI Training minigame - drag cats to model"""
        # Game objects
        model_rect = pygame.Rect(SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 - 50, 100, 100)
        
        cats = []
        dogs = []
        
        # Create cat and dog objects
        for i in range(5):
            cat_x = random.randint(50, SCREEN_WIDTH - 100)
            cat_y = random.randint(100, SCREEN_HEIGHT - 200)
            cats.append(pygame.Rect(cat_x, cat_y, 60, 40))
            
        for i in range(3):
            dog_x = random.randint(50, SCREEN_WIDTH - 100)
            dog_y = random.randint(100, SCREEN_HEIGHT - 200)
            dogs.append(pygame.Rect(dog_x, dog_y, 60, 40))
        
        cats_trained = 0
        dragging = None
        drag_offset = (0, 0)
        
        clock = pygame.time.Clock()
        
        while cats_trained < 5:
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if clicking on a cat
                    for i, cat in enumerate(cats):
                        if cat.collidepoint(mouse_pos):
                            dragging = ('cat', i)
                            drag_offset = (mouse_pos[0] - cat.x, mouse_pos[1] - cat.y)
                            break
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragging and dragging[0] == 'cat':
                        cat_index = dragging[1]
                        if cats[cat_index].colliderect(model_rect):
                            cats_trained += 1
                        cats.pop(cat_index)  # Remove trained cat
                    dragging = None
                elif event.type == pygame.MOUSEMOTION:
                    if dragging and dragging[0] == 'cat':
                        mouse_pos = pygame.mouse.get_pos()
                        cat_index = dragging[1]
                        cats[cat_index].x = mouse_pos[0] - drag_offset[0]
                        cats[cat_index].y = mouse_pos[1] - drag_offset[1]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            
            # Update GIF animation
            self.update_minigame_gif_background(dt)
            
            # Draw minigame
            self.draw_minigame_background()
            
            # Title
            self.draw_text_with_background("Train Your Brain", self.font_large, WHITE, (SCREEN_WIDTH//2, 50))
            
            # Instructions
            instruction = f"Перетащите котиков к модели! ({cats_trained}/5)"
            self.draw_text_with_background(instruction, self.font_medium, WHITE, (SCREEN_WIDTH//2, 80))
            
            # Draw model (brain)
            pygame.draw.rect(self.screen, GREEN, model_rect)
            brain_text = self.font_medium.render("🧠", True, WHITE)
            brain_rect = brain_text.get_rect(center=model_rect.center)
            self.screen.blit(brain_text, brain_rect)
            
            # Draw cats
            for cat in cats:
                pygame.draw.rect(self.screen, YELLOW, cat)
                cat_text = self.font_small.render("🐱", True, BLACK)
                cat_rect = cat_text.get_rect(center=cat.center)
                self.screen.blit(cat_text, cat_rect)
            
            # Draw dogs (distractors)
            for dog in dogs:
                pygame.draw.rect(self.screen, GRAY, dog)
                dog_text = self.font_small.render("🐶", True, BLACK)
                dog_rect = dog_text.get_rect(center=dog.center)
                self.screen.blit(dog_text, dog_rect)
            
            pygame.display.flip()
            clock.tick(60)
        
        return True
    
    def run_ts_quiz(self):
        """TypeScript Quiz minigame"""
        questions = [
            {
                "question": "Какой тип у user.name?",
                "code": "const user = { id: 1, name: 'Alex' }",
                "options": ["string", "number", "any"],
                "correct": 0
            },
            {
                "question": "Какой тип у user.age?", 
                "code": "const user = { age: 25, active: true }",
                "options": ["string", "number", "boolean"],
                "correct": 1
            },
            {
                "question": "Что не так с этим кодом?",
                "code": "let value: any = 'hello'",
                "options": ["Ничего", "Используется any", "Неверный синтаксис"],
                "correct": 1
            }
        ]
        
        # Shuffle questions to make them appear in different positions
        import random
        random.shuffle(questions)
        
        current_question = 0
        score = 0
        selected_option = None
        
        clock = pygame.time.Clock()
        
        while current_question < len(questions):
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            question_data = questions[current_question]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check option clicks
                    for i in range(len(question_data["options"])):
                        option_y = 350 + i * 50
                        option_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, option_y, 400, 40)
                        if option_rect.collidepoint(mouse_pos):
                            selected_option = i
                            if i == question_data["correct"]:
                                score += 1
                            current_question += 1
                            selected_option = None
                            break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            
            # Update GIF animation
            self.update_minigame_gif_background(dt)
            
            # Draw quiz
            self.draw_minigame_background()
            
            # Title
            self.draw_text_with_background("Strict Mode Madness", self.font_large, WHITE, (SCREEN_WIDTH//2, 50))
            
            # Progress
            progress_text = f"Вопрос {current_question + 1}/{len(questions)}"
            self.draw_text_with_background(progress_text, self.font_medium, WHITE, (100, 30))
            
            # Question
            self.draw_text_with_background(question_data["question"], self.font_medium, WHITE, (SCREEN_WIDTH//2, 150))
            
            # Code
            self.draw_text_with_background(question_data["code"], self.font_medium, YELLOW, (SCREEN_WIDTH//2, 200))
            
            # Options
            for i, option in enumerate(question_data["options"]):
                option_y = 350 + i * 50
                option_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, option_y, 400, 40)
                
                # Highlight on hover
                mouse_pos = pygame.mouse.get_pos()
                color = GRAY if option_rect.collidepoint(mouse_pos) else UI_BG_COLOR[:3]
                pygame.draw.rect(self.screen, color, option_rect)
                pygame.draw.rect(self.screen, WHITE, option_rect, 2)
                
                option_text = f"{chr(65 + i)}) {option}"
                # Add background for option text
                option_surface = self.font_medium.render(option_text, True, WHITE)
                option_text_rect = option_surface.get_rect(center=option_rect.center)
                
                # Create background for option text
                bg_surface = pygame.Surface((option_text_rect.width + 20, option_text_rect.height + 8))
                bg_surface.set_alpha(200)
                bg_surface.fill((0, 0, 0))
                bg_rect = bg_surface.get_rect(center=option_text_rect.center)
                
                self.screen.blit(bg_surface, bg_rect)
                self.screen.blit(option_surface, option_text_rect)
            
            pygame.display.flip()
            clock.tick(60)
        
        # Show results with feedback
        if score >= 2:
            return True
        else:
            # Show failure feedback
            self.draw_minigame_background()
            title = self.font_large.render("Результат", True, RED)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
            self.screen.blit(title, title_rect)
            
            result_text = f"Правильных ответов: {score}/{len(questions)}"
            result_surface = self.font_medium.render(result_text, True, WHITE)
            result_rect = result_surface.get_rect(center=(SCREEN_WIDTH//2, 250))
            self.screen.blit(result_surface, result_rect)
            
            feedback_text = "Нужно правильно ответить на минимум 2 вопроса из 3"
            feedback_surface = self.font_medium.render(feedback_text, True, YELLOW)
            feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH//2, 300))
            self.screen.blit(feedback_surface, feedback_rect)
            
            pygame.display.flip()
            pygame.time.wait(2000)  # Show feedback for 2 seconds
            return False
    
    def run_memory_leak_hunter(self):
        """Memory Leak Hunter minigame"""
        # Code with memory leaks
        code_lines = [
            "function createUser() {",
            "  const user = new User();",
            "  setInterval(() => {",  # Memory leak!
            "    user.update();",
            "  }, 1000);",
            "  return user;",
            "}",
            "",
            "function cleanup() {",
            "  // Missing cleanup",
            "  console.log('Done');",
            "}"
        ]
        
        leak_lines = [2, 8]  # Lines with memory leaks
        start_time = time.time()
        time_limit = 20
        found_leaks = []
        
        clock = pygame.time.Clock()
        
        while len(found_leaks) < len(leak_lines):
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            current_time = time.time()
            remaining_time = time_limit - (current_time - start_time)
            
            if remaining_time <= 0:
                return False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if clicked on leak line
                    for i, line in enumerate(code_lines):
                        line_y = 200 + i * 30
                        if 100 <= mouse_pos[0] <= 800 and line_y <= mouse_pos[1] <= line_y + 25:
                            if i in leak_lines and i not in found_leaks:
                                found_leaks.append(i)
                            elif i not in leak_lines:
                                # Ошибка: не та строка
                                self.draw_minigame_background()
                                title = self.font_large.render("Это не утечка!", True, RED)
                                title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
                                self.screen.blit(title, title_rect)
                                feedback_text = "Попробуй снова через NPC!"
                                feedback_surface = self.font_medium.render(feedback_text, True, YELLOW)
                                feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH//2, 150))
                                self.screen.blit(feedback_surface, feedback_rect)
                                pygame.display.flip()
                                pygame.time.wait(2000)
                                return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            
            # Update GIF animation
            self.update_minigame_gif_background(dt)
            
            # Draw minigame
            self.draw_minigame_background()
            
            # Title
            self.draw_text_with_background("Memory Leak Hunter", self.font_large, WHITE, (SCREEN_WIDTH//2, 100))
            
            # Timer
            timer_text = f"Время: {remaining_time:.1f}s"
            self.draw_text_with_background(timer_text, self.font_medium, RED, (100, 30))
            
            # Instructions
            instruction = f"Найдите утечки памяти! Найдено: {len(found_leaks)}/{len(leak_lines)}"
            self.draw_text_with_background(instruction, self.font_medium, WHITE, (SCREEN_WIDTH//2, 150))
            
            # Code lines
            for i, line in enumerate(code_lines):
                y_pos = 200 + i * 30
                color = GREEN if i in found_leaks else WHITE
                
                # Create background for code line
                line_text = f"{i+1:2d}. {line}"
                line_surface = self.font_medium.render(line_text, True, color)
                line_rect = line_surface.get_rect()
                
                # Background for code line
                bg_surface = pygame.Surface((line_rect.width + 20, line_rect.height + 8))
                bg_surface.set_alpha(200)
                bg_surface.fill((0, 0, 0))
                bg_rect = bg_surface.get_rect()
                bg_rect.topleft = (90, y_pos - 4)
                
                # Highlight on hover
                mouse_pos = pygame.mouse.get_pos()
                if 100 <= mouse_pos[0] <= 800 and y_pos <= mouse_pos[1] <= y_pos + 25:
                    bg_surface.fill((50, 50, 50))
                    pygame.draw.rect(self.screen, GRAY, (90, y_pos-2, 720, 30), 2)
                
                self.screen.blit(bg_surface, bg_rect)
                self.screen.blit(line_surface, (100, y_pos))
            
            pygame.display.flip()
            clock.tick(60)
        
        return True
    
    def run_react_debug(self):
        """React Debug Challenge minigame"""
        # React component with bugs
        code_lines = [
            "function UserProfile({ user }) {",
            "  const [loading, setLoading] = useState(true);",
            "  const [data, setData] = useState(null);",
            "",
            "  useEffect(() => {",
            "    fetchUserData(user.id);",  # Missing dependency!
            "  }, []);",  # Should include user.id
            "",
            "  return (",
            "    <div>",
            "      {loading && <Spinner />}",
            "      {data && <UserInfo data={data} />}",
            "    </div>",
            "  );",
            "}"
        ]
        
        bug_line = 5  # Line with bug
        start_time = time.time()
        time_limit = 15
        
        clock = pygame.time.Clock()
        
        while True:
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            current_time = time.time()
            remaining_time = time_limit - (current_time - start_time)
            
            if remaining_time <= 0:
                return False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i in range(len(code_lines)):
                        line_y = 200 + i * 30
                        if 100 <= mouse_pos[0] <= 800 and line_y <= mouse_pos[1] <= line_y + 25:
                            if i == bug_line:
                                return True
                            else:
                                self.draw_minigame_background()
                                title = self.font_large.render("Это не ошибка!", True, RED)
                                title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
                                self.screen.blit(title, title_rect)
                                feedback_text = "Попробуй снова через NPC!"
                                feedback_surface = self.font_medium.render(feedback_text, True, YELLOW)
                                feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH//2, 150))
                                self.screen.blit(feedback_surface, feedback_rect)
                                pygame.display.flip()
                                pygame.time.wait(2000)
                                return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            
            # Update GIF animation
            self.update_minigame_gif_background(dt)
            
            # Draw minigame
            self.draw_minigame_background()
            
            # Title
            self.draw_text_with_background("React Debug Challenge", self.font_large, WHITE, (SCREEN_WIDTH//2, 100))
            
            # Timer
            timer_text = f"Время: {remaining_time:.1f}s"
            self.draw_text_with_background(timer_text, self.font_medium, RED, (100, 30))
            
            # Instructions
            instruction = "Найдите ошибку в React компоненте:"
            self.draw_text_with_background(instruction, self.font_medium, WHITE, (SCREEN_WIDTH//2, 150))
            
            # Code lines
            for i, line in enumerate(code_lines):
                y_pos = 200 + i * 30
                color = WHITE
                
                # Create background for code line
                line_text = f"{i+1:2d}. {line}"
                line_surface = self.font_medium.render(line_text, True, color)
                line_rect = line_surface.get_rect()
                
                # Background for code line
                bg_surface = pygame.Surface((line_rect.width + 20, line_rect.height + 8))
                bg_surface.set_alpha(200)
                bg_surface.fill((0, 0, 0))
                bg_rect = bg_surface.get_rect()
                bg_rect.topleft = (90, y_pos - 4)
                
                # Highlight on hover
                mouse_pos = pygame.mouse.get_pos()
                if 100 <= mouse_pos[0] <= 800 and y_pos <= mouse_pos[1] <= y_pos + 25:
                    bg_surface.fill((50, 50, 50))
                    pygame.draw.rect(self.screen, GRAY, (90, y_pos-2, 720, 30), 2)
                
                self.screen.blit(bg_surface, bg_rect)
                self.screen.blit(line_surface, (100, y_pos))
            
            pygame.display.flip()
            clock.tick(60)
    
    def run_mobile_debug(self):
        """Mobile Debug minigame"""
        # Mobile app crash scenarios
        scenarios = [
            "Приложение крашится при повороте экрана",
            "Push-уведомления не приходят",
            "Приложение медленно загружается",
            "Кнопка не реагирует на нажатие"
        ]
        
        correct_solutions = [
            "Проверить onConfigurationChanged",
            "Проверить Firebase токены",
            "Оптимизировать изображения",
            "Проверить onClick listener"
        ]
        
        wrong_solutions = [
            "Перезапустить телефон",
            "Удалить приложение",
            "Игнорировать проблему",
            "Позвонить в поддержку"
        ]
        
        current_scenario = 0
        score = 0
        
        clock = pygame.time.Clock()
        
        while current_scenario < len(scenarios):
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            scenario = scenarios[current_scenario]
            correct = correct_solutions[current_scenario]
            wrong = wrong_solutions[current_scenario]
            
            # Randomize option positions
            options = [correct, wrong]
            random.shuffle(options)
            correct_index = options.index(correct)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check option clicks
                    for i in range(2):
                        option_y = 400 + i * 60
                        option_rect = pygame.Rect(SCREEN_WIDTH//2 - 250, option_y, 500, 50)
                        if option_rect.collidepoint(mouse_pos):
                            if i == correct_index:
                                score += 1
                            current_scenario += 1
                            break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            
            # Update GIF animation
            self.update_minigame_gif_background(dt)
            
            # Draw minigame
            self.draw_minigame_background()
            
            # Title
            self.draw_text_with_background("Mobile Debug Master", self.font_large, WHITE, (SCREEN_WIDTH//2, 100))
            
            # Progress
            progress_text = f"Сценарий {current_scenario + 1}/{len(scenarios)}"
            self.draw_text_with_background(progress_text, self.font_medium, WHITE, (100, 30))
            
            # Scenario
            self.draw_text_with_background(scenario, self.font_medium, WHITE, (SCREEN_WIDTH//2, 200))
            
            # Question
            question = "Выберите правильное решение:"
            self.draw_text_with_background(question, self.font_medium, YELLOW, (SCREEN_WIDTH//2, 250))
            
            # Options
            for i, option in enumerate(options):
                option_y = 400 + i * 60
                option_rect = pygame.Rect(SCREEN_WIDTH//2 - 250, option_y, 500, 50)
                
                # Highlight on hover
                mouse_pos = pygame.mouse.get_pos()
                color = GRAY if option_rect.collidepoint(mouse_pos) else UI_BG_COLOR[:3]
                pygame.draw.rect(self.screen, color, option_rect)
                pygame.draw.rect(self.screen, WHITE, option_rect, 2)
                
                option_text = f"{chr(65 + i)}) {option}"
                # Add background for option text
                option_surface = self.font_medium.render(option_text, True, WHITE)
                option_text_rect = option_surface.get_rect(center=option_rect.center)
                
                # Create background for option text
                bg_surface = pygame.Surface((option_text_rect.width + 20, option_text_rect.height + 8))
                bg_surface.set_alpha(200)
                bg_surface.fill((0, 0, 0))
                bg_rect = bg_surface.get_rect(center=option_text_rect.center)
                
                self.screen.blit(bg_surface, bg_rect)
                self.screen.blit(option_surface, option_text_rect)
            
            pygame.display.flip()
            clock.tick(60)
        
        return score >= 3  # Need at least 3/4 correct
    
    def run_devops_pipeline(self):
        """DevOps Pipeline Fix minigame"""
        # Pipeline configuration with errors
        pipeline_steps = [
            "git clone repository",
            "npm install dependencies", 
            "run tests",
            "build application",
            "deploy to staging",
            "run integration tests",
            "deploy to production"
        ]
        
        broken_steps = [2, 4]  # Steps that need fixing
        fixed_steps = []
        
        clock = pygame.time.Clock()
        
        while len(fixed_steps) < len(broken_steps):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if clicked on broken step
                    for i, step in enumerate(pipeline_steps):
                        step_y = 200 + i * 50
                        step_rect = pygame.Rect(100, step_y, 600, 40)
                        if step_rect.collidepoint(mouse_pos):
                            if i in broken_steps and i not in fixed_steps:
                                fixed_steps.append(i)
                            break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            
            # Draw minigame
            self.draw_minigame_background()
            
            # Title
            title = self.font_large.render("DevOps Pipeline Fix", True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
            self.screen.blit(title, title_rect)
            
            # Instructions
            instruction = f"Исправьте сломанные шаги пайплайна! Исправлено: {len(fixed_steps)}/{len(broken_steps)}"
            instruction_surface = self.font_medium.render(instruction, True, WHITE)
            instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(instruction_surface, instruction_rect)
            
            # Pipeline steps
            for i, step in enumerate(pipeline_steps):
                step_y = 200 + i * 50
                step_rect = pygame.Rect(100, step_y, 600, 40)
                
                # Color based on status
                if i in fixed_steps:
                    color = GREEN
                elif i in broken_steps:
                    color = RED
                else:
                    color = WHITE
                
                pygame.draw.rect(self.screen, color, step_rect)
                pygame.draw.rect(self.screen, WHITE, step_rect, 2)
                
                step_text = f"{i+1}. {step}"
                step_surface = self.font_medium.render(step_text, True, BLACK if color != WHITE else WHITE)
                step_text_rect = step_surface.get_rect(center=step_rect.center)
                self.screen.blit(step_surface, step_text_rect)
                
                # Highlight on hover
                mouse_pos = pygame.mouse.get_pos()
                if step_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, YELLOW, step_rect, 3)
            
            pygame.display.flip()
            clock.tick(60)
        
        return True
    
    def run_boss_challenge(self):
        """BOSS: Final Challenge - Multi-stage minigame"""
        stages = [
            {
                "name": "Архитектура",
                "description": "Спроектируй систему микросервисов",
                "time_limit": 20,
                "type": "architecture"
            },
            {
                "name": "Кодинг", 
                "description": "Напиши чистый и эффективный код",
                "time_limit": 25,
                "type": "coding"
            },
            {
                "name": "Тестирование",
                "description": "Проведи полное тестирование системы",
                "time_limit": 15,
                "type": "testing"
            }
        ]
        
        current_stage = 0
        stage_results = []
        
        for stage_idx, stage in enumerate(stages):
            # Show stage intro
            self.draw_minigame_background()
            title = self.font_large.render(f"Этап {stage_idx + 1}: {stage['name']}", True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
            self.screen.blit(title, title_rect)
            
            desc = self.font_medium.render(stage['description'], True, YELLOW)
            desc_rect = desc.get_rect(center=(SCREEN_WIDTH//2, 250))
            self.screen.blit(desc, desc_rect)
            
            time_text = f"Время: {stage['time_limit']} секунд"
            time_surface = self.font_medium.render(time_text, True, GREEN)
            time_rect = time_surface.get_rect(center=(SCREEN_WIDTH//2, 300))
            self.screen.blit(time_surface, time_rect)
            
            pygame.display.flip()
            pygame.time.wait(3000)  # Show stage intro for 3 seconds
            
            # Run stage
            stage_success = self.run_boss_stage(stage)
            stage_results.append(stage_success)
            
            if not stage_success:
                # Failed stage - show failure
                self.draw_minigame_background()
                title = self.font_large.render(f"Этап {stage_idx + 1} провален!", True, RED)
                title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
                self.screen.blit(title, title_rect)
                
                feedback = "Босс не доволен! Попробуй снова!"
                feedback_surface = self.font_medium.render(feedback, True, YELLOW)
                feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH//2, 250))
                self.screen.blit(feedback_surface, feedback_rect)
                
                pygame.display.flip()
                pygame.time.wait(2000)
                return False
        
        # All stages completed successfully
        self.draw_minigame_background()
        title = self.font_large.render("🏆 ВСЕ ЭТАПЫ ПРОЙДЕНЫ!", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(title, title_rect)
        
        subtitle = "Ты доказал, что достоин быть лучшим!"
        subtitle_surface = self.font_medium.render(subtitle, True, WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH//2, 250))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        pygame.display.flip()
        pygame.time.wait(3000)
        return True
    
    def run_boss_stage(self, stage):
        """Run individual boss stage"""
        if stage['type'] == 'architecture':
            return self.run_architecture_stage(stage)
        elif stage['type'] == 'coding':
            return self.run_coding_stage(stage)
        elif stage['type'] == 'testing':
            return self.run_testing_stage(stage)
        return False
    
    def run_architecture_stage(self, stage):
        """Architecture stage - design microservices (drag & check)"""
        services = [
            {"name": "User Service", "color": GREEN, "correct_pos": 0},
            {"name": "Auth Service", "color": BLUE, "correct_pos": 1},
            {"name": "Payment Service", "color": RED, "correct_pos": 2},
            {"name": "Notification Service", "color": YELLOW, "correct_pos": 3}
        ]
        # Initialize positions randomly
        import random
        random.shuffle(services)
        for i, service in enumerate(services):
            service['x'] = 100 + i * 200
            service['y'] = 300
        selected_service = None
        drag_offset = (0, 0)
        check_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 500, 200, 50)
        feedback = None
        feedback_time = 0
        clock = pygame.time.Clock()
        start_time = time.time()
        time_limit = stage['time_limit']
        while True:
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            current_time = time.time()
            remaining_time = time_limit - (current_time - start_time)
            if remaining_time <= 0:
                return False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check drag
                    for i, service in enumerate(services):
                        x = service.get('x', 100 + i * 200)
                        y = service.get('y', 300)
                        service_rect = pygame.Rect(x, y, 150, 80)
                        if service_rect.collidepoint(mouse_pos):
                            selected_service = i
                            drag_offset = (mouse_pos[0] - x, mouse_pos[1] - y)
                            break
                    # Check button
                    if check_button_rect.collidepoint(mouse_pos):
                        # Проверка порядка
                        expected_order = ["User Service", "Auth Service", "Payment Service", "Notification Service"]
                        sorted_services = sorted(services, key=lambda s: s['x'])
                        current_order = [s['name'] for s in sorted_services]
                        if current_order == expected_order:
                            return True
                        else:
                            feedback = "Неправильный порядок! Попробуй ещё раз."
                            feedback_time = time.time()
                elif event.type == pygame.MOUSEBUTTONUP:
                    selected_service = None
                elif event.type == pygame.MOUSEMOTION:
                    if selected_service is not None:
                        mouse_pos = pygame.mouse.get_pos()
                        services[selected_service]['x'] = mouse_pos[0] - drag_offset[0]
                        services[selected_service]['y'] = mouse_pos[1] - drag_offset[1]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            
            # Update GIF animation
            self.update_minigame_gif_background(dt)
            
            # Draw stage
            self.draw_minigame_background()
            
            # Title
            self.draw_text_with_background(f"Этап: {stage['name']}", self.font_large, WHITE, (SCREEN_WIDTH//2, 100))
            
            # Timer
            timer_text = f"Время: {remaining_time:.1f}s"
            self.draw_text_with_background(timer_text, self.font_medium, RED, (100, 30))
            
            # Instructions
            instruction = "Расставь микросервисы в правильном порядке (User → Auth → Payment → Notification):"
            self.draw_text_with_background(instruction, self.font_medium, WHITE, (SCREEN_WIDTH//2, 150))
            # Draw services
            for i, service in enumerate(services):
                x = service.get('x', 100 + i * 200)
                y = service.get('y', 300)
                service_rect = pygame.Rect(x, y, 150, 80)
                if selected_service == i:
                    pygame.draw.rect(self.screen, WHITE, service_rect, 3)
                pygame.draw.rect(self.screen, service['color'], service_rect)
                pygame.draw.rect(self.screen, WHITE, service_rect, 2)
                name_surface = self.font_small.render(service['name'], True, BLACK)
                name_rect = name_surface.get_rect(center=service_rect.center)
                self.screen.blit(name_surface, name_rect)
            # Draw check button
            pygame.draw.rect(self.screen, BLUE, check_button_rect)
            pygame.draw.rect(self.screen, WHITE, check_button_rect, 2)
            btn_text = self.font_medium.render("Проверить порядок", True, WHITE)
            btn_rect = btn_text.get_rect(center=check_button_rect.center)
            self.screen.blit(btn_text, btn_rect)
            # Feedback
            if feedback and time.time() - feedback_time < 2.0:
                fb_surface = self.font_medium.render(feedback, True, RED)
                fb_rect = fb_surface.get_rect(center=(SCREEN_WIDTH//2, 570))
                self.screen.blit(fb_surface, fb_rect)
            pygame.display.flip()
            clock.tick(60)
    
    def run_coding_stage(self, stage):
        """Coding stage - write clean code"""
        # Code with multiple bugs to find
        code_lines = [
            "function calculateTotal(items) {",
            "  let total = 0;",
            "  for (let i = 0; i < items.length; i++) {",
            "    total += items[i].price;",  # Missing null check
            "  }",
            "  return total;",
            "}",
            "",
            "function validateUser(user) {",
            "  if (user.name && user.email) {",
            "    return true;",  # Missing email validation
            "  }",
            "  return false;",
            "}"
        ]
        
        bugs = [3, 9]  # Lines with bugs
        found_bugs = []
        start_time = time.time()
        time_limit = stage['time_limit']
        
        clock = pygame.time.Clock()
        
        while len(found_bugs) < len(bugs):
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            current_time = time.time()
            remaining_time = time_limit - (current_time - start_time)
            
            if remaining_time <= 0:
                return False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, line in enumerate(code_lines):
                        line_y = 200 + i * 25
                        if 100 <= mouse_pos[0] <= 800 and line_y <= mouse_pos[1] <= line_y + 20:
                            if i in bugs and i not in found_bugs:
                                found_bugs.append(i)
                            elif i not in bugs:
                                # Wrong line clicked
                                self.draw_minigame_background()
                                title = self.font_large.render("Это не баг!", True, RED)
                                title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
                                self.screen.blit(title, title_rect)
                                
                                feedback = "Найди настоящие проблемы в коде!"
                                feedback_surface = self.font_medium.render(feedback, True, YELLOW)
                                feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH//2, 250))
                                self.screen.blit(feedback_surface, feedback_rect)
                                
                                pygame.display.flip()
                                pygame.time.wait(2000)
                                return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            
            # Update GIF animation
            self.update_minigame_gif_background(dt)
            
            # Draw stage
            self.draw_minigame_background()
            
            # Title
            self.draw_text_with_background(f"Этап: {stage['name']}", self.font_large, WHITE, (SCREEN_WIDTH//2, 100))
            
            # Timer
            timer_text = f"Время: {remaining_time:.1f}s"
            self.draw_text_with_background(timer_text, self.font_medium, RED, (100, 30))
            
            # Instructions
            instruction = f"Найди все баги в коде! Найдено: {len(found_bugs)}/{len(bugs)}"
            self.draw_text_with_background(instruction, self.font_medium, WHITE, (SCREEN_WIDTH//2, 150))
            
            # Code lines
            for i, line in enumerate(code_lines):
                y_pos = 200 + i * 25
                color = GREEN if i in found_bugs else WHITE
                line_surface = self.font_small.render(f"{i+1:2d}. {line}", True, color)
                self.screen.blit(line_surface, (100, y_pos))
                
                # Highlight on hover
                mouse_pos = pygame.mouse.get_pos()
                if 100 <= mouse_pos[0] <= 800 and y_pos <= mouse_pos[1] <= y_pos + 20:
                    pygame.draw.rect(self.screen, GRAY, (90, y_pos-2, 720, 25), 2)
            
            pygame.display.flip()
            clock.tick(60)
        
        return True
    
    def run_testing_stage(self, stage):
        """Testing stage - comprehensive testing"""
        # Test cases to complete
        test_cases = [
            {"name": "Unit Tests", "progress": 0, "target": 5},
            {"name": "Integration Tests", "progress": 0, "target": 3},
            {"name": "Performance Tests", "progress": 0, "target": 2}
        ]
        
        total_progress = 0
        total_target = sum(test['target'] for test in test_cases)
        start_time = time.time()
        time_limit = stage['time_limit']
        
        clock = pygame.time.Clock()
        
        while total_progress < total_target:
            current_time = time.time()
            remaining_time = time_limit - (current_time - start_time)
            
            if remaining_time <= 0:
                return False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Click on test cases to progress
                    for i, test in enumerate(test_cases):
                        test_rect = pygame.Rect(200, 300 + i * 100, 400, 60)
                        if test_rect.collidepoint(mouse_pos) and test['progress'] < test['target']:
                            test['progress'] += 1
                            total_progress += 1
                            break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            
            # Draw stage
            self.screen.fill(BLACK)
            
            # Title
            title = self.font_large.render(f"Этап: {stage['name']}", True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
            self.screen.blit(title, title_rect)
            
            # Timer
            timer_text = f"Время: {remaining_time:.1f}s"
            timer_surface = self.font_medium.render(timer_text, True, RED)
            self.screen.blit(timer_surface, (10, 10))
            
            # Progress
            progress_text = f"Прогресс: {total_progress}/{total_target}"
            progress_surface = self.font_medium.render(progress_text, True, WHITE)
            progress_rect = progress_surface.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(progress_surface, progress_rect)
            
            # Instructions
            instruction = "Кликни на тесты для их выполнения:"
            instruction_surface = self.font_medium.render(instruction, True, YELLOW)
            instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH//2, 200))
            self.screen.blit(instruction_surface, instruction_rect)
            
            # Draw test cases
            for i, test in enumerate(test_cases):
                test_rect = pygame.Rect(200, 300 + i * 100, 400, 60)
                
                # Background
                color = GREEN if test['progress'] >= test['target'] else GRAY
                pygame.draw.rect(self.screen, color, test_rect)
                pygame.draw.rect(self.screen, WHITE, test_rect, 2)
                
                # Test name and progress
                name_text = f"{test['name']}: {test['progress']}/{test['target']}"
                name_surface = self.font_medium.render(name_text, True, BLACK)
                name_rect = name_surface.get_rect(center=test_rect.center)
                self.screen.blit(name_surface, name_rect)
                
                # Highlight on hover
                mouse_pos = pygame.mouse.get_pos()
                if test_rect.collidepoint(mouse_pos) and test['progress'] < test['target']:
                    pygame.draw.rect(self.screen, YELLOW, test_rect, 3)
            
            pygame.display.flip()
            clock.tick(60)
        
        return True
    
    def run_qa_testing(self):
        """QA Testing minigame"""
        # Code with bugs to find
        code_lines = [
            "function calculateTotal(items) {",
            "  let total = 0;",
            "  for (let i = 0; i < items.length; i++) {",
            "    total += items[i].price;",  # Missing null check
            "  }",
            "  return total;",
            "}",
            "",
            "function validateEmail(email) {",
            "  return email.includes('@');",  # Too simple validation
            "}",
            "",
            "function getUser(id) {",
            "  return users.find(u => u.id === id);",  # No error handling
            "}"
        ]
        
        bug_lines = [3, 9, 12]  # Lines with bugs
        found_bugs = []
        
        clock = pygame.time.Clock()
        
        while len(found_bugs) < len(bug_lines):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if clicked on bug line
                    for i, line in enumerate(code_lines):
                        line_y = 200 + i * 30
                        if 100 <= mouse_pos[0] <= 800 and line_y <= mouse_pos[1] <= line_y + 25:
                            if i in bug_lines and i not in found_bugs:
                                found_bugs.append(i)
                            break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            
            # Draw minigame
            self.screen.fill(BLACK)
            
            # Title
            title = self.font_large.render("QA Bug Hunter", True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
            self.screen.blit(title, title_rect)
            
            # Instructions
            instruction = f"Найдите все баги в коде! Найдено: {len(found_bugs)}/{len(bug_lines)}"
            instruction_surface = self.font_medium.render(instruction, True, WHITE)
            instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(instruction_surface, instruction_rect)
            
            # Code lines
            for i, line in enumerate(code_lines):
                y_pos = 200 + i * 30
                color = GREEN if i in found_bugs else WHITE
                line_surface = self.font_medium.render(f"{i+1:2d}. {line}", True, color)
                self.screen.blit(line_surface, (100, y_pos))
                
                # Highlight on hover
                mouse_pos = pygame.mouse.get_pos()
                if 100 <= mouse_pos[0] <= 800 and y_pos <= mouse_pos[1] <= y_pos + 25:
                    pygame.draw.rect(self.screen, GRAY, (90, y_pos-2, 720, 30), 2)
            
            pygame.display.flip()
            clock.tick(60)
        
        return True 

    def run_treasure_collector(self):
        """Run cat collector minigame"""
        print("🎮 Запуск мини-игры: Поймай котика!")
        
        # Load cat sprite
        try:
            cat_sprite = pygame.image.load("cat.png")
            cat_sprite = pygame.transform.scale(cat_sprite, (60, 60))  # Scale cat to 60x60
            print("✅ Загружен спрайт котика")
        except:
            # Fallback cat sprite if file not found
            cat_sprite = pygame.Surface((60, 60))
            cat_sprite.fill((255, 200, 150))  # Orange cat
            pygame.draw.circle(cat_sprite, (255, 150, 100), (30, 20), 15)  # Head
            pygame.draw.circle(cat_sprite, (255, 150, 100), (30, 45), 20)  # Body
            pygame.draw.circle(cat_sprite, (0, 0, 0), (25, 15), 3)  # Left eye
            pygame.draw.circle(cat_sprite, (0, 0, 0), (35, 15), 3)  # Right eye
            print("⚠️ Файл cat.png не найден, создан fallback спрайт")
        
        # Game state
        collected_cats = 0
        total_cats = 5
        time_left = 45  # 45 seconds
        game_start_time = pygame.time.get_ticks()
        
        # Cat positions (random)
        cats = []
        for i in range(total_cats):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 200)
            cats.append({"x": x, "y": y, "collected": False})
        
        # Player position
        player_x = SCREEN_WIDTH // 2
        player_y = SCREEN_HEIGHT // 2
        player_speed = 6
        
        # Fonts
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            dt = clock.tick(60) / 1000.0
            
            # Update time
            current_time = pygame.time.get_ticks()
            time_left = max(0, 45 - (current_time - game_start_time) / 1000)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            
            # Handle input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player_y -= player_speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player_y += player_speed
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player_x -= player_speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player_x += player_speed
            
            # Keep player on screen
            player_x = max(20, min(SCREEN_WIDTH - 20, player_x))
            player_y = max(20, min(SCREEN_HEIGHT - 20, player_y))
            
            # Check cat collection
            for cat in cats:
                if not cat["collected"]:
                    distance = ((player_x - cat["x"])**2 + (player_y - cat["y"])**2)**0.5
                    if distance < 40:  # Collection radius
                        cat["collected"] = True
                        collected_cats += 1
                        
                        # Play cat collection sound
                        sound_manager = get_sound_manager()
                        if sound_manager:
                            sound_manager.play_sound("success")
            
            # Check win/lose conditions
            if collected_cats >= total_cats:
                return True  # Win
            elif time_left <= 0:
                return False  # Lose
            
            # Draw
            self.screen.fill((50, 100, 50))  # Green background
            
            # Draw cats
            for cat in cats:
                if not cat["collected"]:
                    # Cat glow effect
                    for i in range(3):
                        glow_radius = 35 + i * 5
                        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                        pygame.draw.circle(glow_surface, (255, 200, 150, 50 - i * 15), (glow_radius, glow_radius), glow_radius)
                        self.screen.blit(glow_surface, (cat["x"] - glow_radius, cat["y"] - glow_radius))
                    
                    # Draw cat sprite
                    cat_rect = cat_sprite.get_rect(center=(cat["x"], cat["y"]))
                    self.screen.blit(cat_sprite, cat_rect)
            
            # Draw player (catcher)
            pygame.draw.circle(self.screen, (0, 150, 255), (int(player_x), int(player_y)), 25)
            pygame.draw.circle(self.screen, (0, 100, 200), (int(player_x), int(player_y)), 20)
            
            # Draw UI
            # Progress
            progress_text = f"Котики: {collected_cats}/{total_cats}"
            progress_surface = font_medium.render(progress_text, True, WHITE)
            self.screen.blit(progress_surface, (20, 20))
            
            # Time
            time_text = f"Время: {int(time_left)}с"
            time_color = (255, 255, 255) if time_left > 10 else (255, 0, 0)
            time_surface = font_medium.render(time_text, True, time_color)
            self.screen.blit(time_surface, (20, 60))
            
            # Instructions
            instructions = [
                "WASD - движение",
                "Поймай всех котиков за 45 секунд!",
                "ESC - выйти"
            ]
            
            for i, instruction in enumerate(instructions):
                inst_surface = font_small.render(instruction, True, GRAY)
                self.screen.blit(inst_surface, (20, SCREEN_HEIGHT - 100 + i * 25))
            
            pygame.display.flip()
        
        return False 

    def run_api_architect(self):
        """Run API architect minigame"""
        print("🎮 Запуск мини-игры: Архитектор API")
        
        # Game state
        score = 0
        max_score = 100
        time_left = 120  # 2 minutes
        game_start_time = pygame.time.get_ticks()
        
        # API endpoints to design
        endpoints = [
            {"name": "GET /users", "correct": "Получить список пользователей", "points": 20},
            {"name": "POST /users", "correct": "Создать нового пользователя", "points": 20},
            {"name": "PUT /users/{id}", "correct": "Обновить пользователя", "points": 20},
            {"name": "DELETE /users/{id}", "correct": "Удалить пользователя", "points": 20},
            {"name": "GET /users/{id}", "correct": "Получить пользователя по ID", "points": 20}
        ]
        
        current_endpoint = 0
        selected_option = 0
        
        # Options for each endpoint
        options = [
            ["Получить список пользователей", "Удалить всех пользователей", "Создать пользователя", "Обновить пользователя"],
            ["Создать нового пользователя", "Удалить пользователя", "Получить пользователя", "Обновить пользователя"],
            ["Обновить пользователя", "Создать пользователя", "Удалить пользователя", "Получить пользователя"],
            ["Удалить пользователя", "Создать пользователя", "Обновить пользователя", "Получить пользователя"],
            ["Получить пользователя по ID", "Удалить пользователя", "Создать пользователя", "Обновить пользователя"]
        ]
        
        # Shuffle options for each endpoint to randomize positions
        import random
        for i in range(len(options)):
            # Create a copy of options for this endpoint
            endpoint_options = options[i].copy()
            correct_answer = endpoints[i]["correct"]
            
            # Remove correct answer temporarily
            endpoint_options.remove(correct_answer)
            
            # Shuffle wrong answers
            random.shuffle(endpoint_options)
            
            # Insert correct answer at random position
            correct_position = random.randint(0, len(endpoint_options))
            endpoint_options.insert(correct_position, correct_answer)
            
            # Update options
            options[i] = endpoint_options
        
        # Fonts
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            dt = clock.tick(60) / 1000.0
            
            # Update time
            current_time = pygame.time.get_ticks()
            time_left = max(0, 120 - (current_time - game_start_time) / 1000)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % 4
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % 4
                    elif event.key == pygame.K_RETURN:
                        # Check answer
                        if options[current_endpoint][selected_option] == endpoints[current_endpoint]["correct"]:
                            score += endpoints[current_endpoint]["points"]
                        
                        # Move to next endpoint
                        current_endpoint += 1
                        selected_option = 0
                        
                        if current_endpoint >= len(endpoints):
                            return score >= max_score * 0.8  # 80% to pass
            
            # Check time
            if time_left <= 0:
                return score >= max_score * 0.8
            
            # Draw
            self.screen.fill((20, 30, 50))
            
            # Title
            title_text = "🏗️ АРХИТЕКТОР API"
            title_surface = font_large.render(title_text, True, WHITE)
            self.screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 50))
            
            # Progress
            progress_text = f"Прогресс: {current_endpoint + 1}/{len(endpoints)}"
            progress_surface = font_medium.render(progress_text, True, WHITE)
            self.screen.blit(progress_surface, (20, 120))
            
            # Score
            score_text = f"Очки: {score}/{max_score}"
            score_surface = font_medium.render(score_text, True, WHITE)
            self.screen.blit(score_surface, (20, 150))
            
            # Time
            time_text = f"Время: {int(time_left)}с"
            time_color = (255, 255, 255) if time_left > 30 else (255, 0, 0)
            time_surface = font_medium.render(time_text, True, time_color)
            self.screen.blit(time_surface, (20, 180))
            
            if current_endpoint < len(endpoints):
                # Current endpoint
                endpoint_text = f"Спроектируй: {endpoints[current_endpoint]['name']}"
                endpoint_surface = font_medium.render(endpoint_text, True, YELLOW)
                self.screen.blit(endpoint_surface, (SCREEN_WIDTH // 2 - endpoint_surface.get_width() // 2, 220))
                
                # Options
                option_y = 280
                for i, option in enumerate(options[current_endpoint]):
                    color = YELLOW if i == selected_option else WHITE
                    option_surface = font_medium.render(f"{i+1}. {option}", True, color)
                    self.screen.blit(option_surface, (SCREEN_WIDTH // 2 - option_surface.get_width() // 2, option_y))
                    option_y += 40
            
            # Instructions
            instructions = [
                "WASD - выбор ответа",
                "ENTER - подтвердить",
                "Спроектируй REST API за 2 минуты!",
                "ESC - выйти"
            ]
            
            for i, instruction in enumerate(instructions):
                inst_surface = font_small.render(instruction, True, GRAY)
                self.screen.blit(inst_surface, (20, SCREEN_HEIGHT - 120 + i * 25))
            
            pygame.display.flip()
        
        return False

    def run_ui_designer(self):
        """Run UI/UX Designer minigame"""
        print("🎮 Запуск мини-игры: UI/UX Дизайнер")
        
        # Game state
        score = 0
        max_score = 100
        time_left = 90  # 1.5 minutes
        game_start_time = pygame.time.get_ticks()
        
        # UI components to arrange
        components = [
            {"name": "Header", "correct_x": 100, "correct_y": 50, "points": 20},
            {"name": "Navigation", "correct_x": 100, "correct_y": 100, "points": 20},
            {"name": "Content", "correct_x": 100, "correct_y": 150, "points": 20},
            {"name": "Sidebar", "correct_x": 300, "correct_y": 150, "points": 20},
            {"name": "Footer", "correct_x": 100, "correct_y": 400, "points": 20}
        ]
        
        # Draggable components
        draggable_components = []
        for i, comp in enumerate(components):
            draggable_components.append({
                "name": comp["name"],
                "x": 50 + i * 80,
                "y": 500,
                "width": 60,
                "height": 30,
                "dragging": False,
                "correct_x": comp["correct_x"],
                "correct_y": comp["correct_y"],
                "points": comp["points"]
            })
        
        # Fonts
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            dt = clock.tick(60) / 1000.0
            
            # Update time
            current_time = pygame.time.get_ticks()
            time_left = max(0, 90 - (current_time - game_start_time) / 1000)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for comp in draggable_components:
                        if (comp["x"] <= mouse_pos[0] <= comp["x"] + comp["width"] and
                            comp["y"] <= mouse_pos[1] <= comp["y"] + comp["height"]):
                            comp["dragging"] = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    for comp in draggable_components:
                        comp["dragging"] = False
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    for comp in draggable_components:
                        if comp["dragging"]:
                            comp["x"] = mouse_pos[0] - comp["width"] // 2
                            comp["y"] = mouse_pos[1] - comp["height"] // 2
            
            # Check component placement
            score = 0
            for comp in draggable_components:
                distance = ((comp["x"] - comp["correct_x"])**2 + (comp["y"] - comp["correct_y"])**2)**0.5
                if distance < 30:  # Close enough to correct position
                    score += comp["points"]
            
            # Check win/lose conditions
            if score >= max_score:
                return True  # Win
            elif time_left <= 0:
                return False  # Lose
            
            # Draw
            self.screen.fill((240, 240, 240))  # Light gray background
            
            # Draw design area
            pygame.draw.rect(self.screen, (255, 255, 255), (50, 50, 400, 400), 2)
            
            # Draw target positions
            for comp in components:
                pygame.draw.rect(self.screen, (200, 200, 200), 
                               (comp["correct_x"], comp["correct_y"], 60, 30), 1)
                text_surface = font_small.render(comp["name"], True, (100, 100, 100))
                self.screen.blit(text_surface, (comp["correct_x"] + 5, comp["correct_y"] + 5))
            
            # Draw draggable components
            for comp in draggable_components:
                color = (100, 150, 255) if comp["dragging"] else (150, 200, 255)
                pygame.draw.rect(self.screen, color, 
                               (comp["x"], comp["y"], comp["width"], comp["height"]))
                text_surface = font_small.render(comp["name"], True, (0, 0, 0))
                self.screen.blit(text_surface, (comp["x"] + 5, comp["y"] + 5))
            
            # Draw UI
            # Score
            score_text = f"Счет: {score}/{max_score}"
            score_surface = font_medium.render(score_text, True, (0, 0, 0))
            self.screen.blit(score_surface, (20, 20))
            
            # Time
            time_text = f"Время: {int(time_left)}с"
            time_color = (0, 0, 0) if time_left > 10 else (255, 0, 0)
            time_surface = font_medium.render(time_text, True, time_color)
            self.screen.blit(time_surface, (20, 60))
            
            # Instructions
            instructions = [
                "Перетащи компоненты в правильные позиции",
                "Создай красивый UI дизайн!",
                "ESC - выйти"
            ]
            
            for i, instruction in enumerate(instructions):
                inst_surface = font_small.render(instruction, True, (100, 100, 100))
                self.screen.blit(inst_surface, (20, SCREEN_HEIGHT - 100 + i * 25))
            
            pygame.display.flip()
        
        return False

    def run_clicker_game(self, clicks_needed, time_limit):
        """Run clicker minigame"""
        print(f"🎮 Запуск кликер-игры: {clicks_needed} кликов за {time_limit} секунд")
        
        # Game state
        clicks = 0
        game_start_time = pygame.time.get_ticks()
        
        # Fonts
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 24)
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            dt = clock.tick(60) / 1000.0
            
            # Update time
            current_time = pygame.time.get_ticks()
            time_left = max(0, time_limit - (current_time - game_start_time) / 1000)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicks += 1
                    
                    # Play click sound
                    sound_manager = get_sound_manager()
                    if sound_manager:
                        sound_manager.play_sound("click")
            
            # Check win/lose conditions
            if clicks >= clicks_needed:
                return True  # Win
            elif time_left <= 0:
                return False  # Lose
            
            # Draw
            self.draw_minigame_background()
            
            # Draw click button
            button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 100, 200, 200)
            button_color = (255, 100, 100) if clicks < clicks_needed else (100, 255, 100)
            pygame.draw.rect(self.screen, button_color, button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 3)
            
            # Draw click text
            click_text = f"КЛИКНИ!"
            click_surface = font_large.render(click_text, True, (255, 255, 255))
            click_rect = click_surface.get_rect(center=button_rect.center)
            self.screen.blit(click_surface, click_rect)
            
            # Draw progress
            progress_text = f"Клики: {clicks}/{clicks_needed}"
            progress_surface = font_medium.render(progress_text, True, WHITE)
            self.screen.blit(progress_surface, (20, 20))
            
            # Draw time
            time_text = f"Время: {int(time_left)}с"
            time_color = WHITE if time_left > 10 else RED
            time_surface = font_medium.render(time_text, True, time_color)
            self.screen.blit(time_surface, (20, 60))
            
            # Draw instructions
            instructions = [
                f"Кликни {clicks_needed} раз за {time_limit} секунд!",
                "Быстро! Быстро!",
                "ESC - выйти"
            ]
            
            for i, instruction in enumerate(instructions):
                inst_surface = font_small.render(instruction, True, GRAY)
                self.screen.blit(inst_surface, (20, SCREEN_HEIGHT - 100 + i * 25))
            
            pygame.display.flip()
        
        return False

    def run_rhythm_game(self, beats_needed, time_limit):
        """Run rhythm minigame"""
        print(f"🎮 Запуск ритм-игры: {beats_needed} ударов за {time_limit} секунд")
        
        # Game state
        beats = 0
        game_start_time = pygame.time.get_ticks()
        beat_interval = time_limit / beats_needed  # Time between beats
        last_beat_time = game_start_time
        
        # Fonts
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 24)
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            dt = clock.tick(60) / 1000.0
            
            # Update time
            current_time = pygame.time.get_ticks()
            time_left = max(0, time_limit - (current_time - game_start_time) / 1000)
            
            # Check for beat timing
            if current_time - last_beat_time >= beat_interval * 1000:
                # Visual beat indicator
                beat_indicator = True
                last_beat_time = current_time
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_SPACE:
                        # Check if click is on beat
                        time_since_last_beat = (current_time - last_beat_time) / 1000
                        if time_since_last_beat < beat_interval * 0.5:  # Within half beat
                            beats += 1
                            
                            # Play beat sound
                            sound_manager = get_sound_manager()
                            if sound_manager:
                                sound_manager.play_sound("beat")
            
            # Check win/lose conditions
            if beats >= beats_needed:
                return True  # Win
            elif time_left <= 0:
                return False  # Lose
            
            # Draw
            self.draw_minigame_background()
            
            # Draw rhythm circle
            circle_center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            circle_radius = 150
            
            # Beat indicator
            if 'beat_indicator' in locals() and beat_indicator:
                pygame.draw.circle(self.screen, (255, 255, 0), circle_center, circle_radius + 20)
                beat_indicator = False
            
            pygame.draw.circle(self.screen, (255, 100, 100), circle_center, circle_radius)
            pygame.draw.circle(self.screen, (255, 255, 255), circle_center, circle_radius, 5)
            
            # Draw rhythm text
            rhythm_text = "ПРОСТРАНСТВО"
            rhythm_surface = font_large.render(rhythm_text, True, (255, 255, 255))
            rhythm_rect = rhythm_surface.get_rect(center=circle_center)
            self.screen.blit(rhythm_surface, rhythm_rect)
            
            # Draw progress
            progress_text = f"Удары: {beats}/{beats_needed}"
            progress_surface = font_medium.render(progress_text, True, WHITE)
            self.screen.blit(progress_surface, (20, 20))
            
            # Draw time
            time_text = f"Время: {int(time_left)}с"
            time_color = WHITE if time_left > 10 else RED
            time_surface = font_medium.render(time_text, True, time_color)
            self.screen.blit(time_surface, (20, 60))
            
            # Draw instructions
            instructions = [
                f"Попади в ритм! {beats_needed} ударов за {time_limit} секунд!",
                "Нажимай ПРОСТРАНСТВО в такт!",
                "ESC - выйти"
            ]
            
            for i, instruction in enumerate(instructions):
                inst_surface = font_small.render(instruction, True, GRAY)
                self.screen.blit(inst_surface, (20, SCREEN_HEIGHT - 100 + i * 25))
            
            pygame.display.flip()
        
        return False

    def run_color_picker_game(self, colors_needed, time_limit):
        """Run color picker minigame"""
        print(f"🎮 Запуск игры с выбором цветов: {colors_needed} цветов за {time_limit} секунд")
        
        # Game state
        colors_found = 0
        game_start_time = pygame.time.get_ticks()
        
        # Available colors
        available_colors = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (255, 165, 0),  # Orange
            (128, 0, 128),  # Purple
            (255, 192, 203), # Pink
            (165, 42, 42)   # Brown
        ]
        
        # Shuffle colors
        import random
        random.shuffle(available_colors)
        target_colors = available_colors[:colors_needed]
        
        # Fonts
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            dt = clock.tick(60) / 1000.0
            
            # Update time
            current_time = pygame.time.get_ticks()
            time_left = max(0, time_limit - (current_time - game_start_time) / 1000)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if clicked on a color
                    for i, color in enumerate(available_colors):
                        color_x = 50 + (i % 5) * 120
                        color_y = 200 + (i // 5) * 80
                        color_rect = pygame.Rect(color_x, color_y, 100, 60)
                        
                        if color_rect.collidepoint(mouse_pos):
                            if color in target_colors and color not in [c for c in available_colors if c not in target_colors]:
                                colors_found += 1
                                target_colors.remove(color)
                                
                                # Play success sound
                                sound_manager = get_sound_manager()
                                if sound_manager:
                                    sound_manager.play_sound("success")
            
            # Check win/lose conditions
            if colors_found >= colors_needed:
                return True  # Win
            elif time_left <= 0:
                return False  # Lose
            
            # Draw
            self.screen.fill((50, 50, 50))  # Dark background
            
            # Draw title
            title_text = "Найди красивые цвета!"
            title_surface = font_large.render(title_text, True, WHITE)
            self.screen.blit(title_surface, (SCREEN_WIDTH//2 - title_surface.get_width()//2, 50))
            
            # Draw color palette
            for i, color in enumerate(available_colors):
                color_x = 50 + (i % 5) * 120
                color_y = 200 + (i // 5) * 80
                
                # Draw color rectangle
                pygame.draw.rect(self.screen, color, (color_x, color_y, 100, 60))
                pygame.draw.rect(self.screen, WHITE, (color_x, color_y, 100, 60), 2)
                
                # Highlight target colors
                if color in target_colors:
                    pygame.draw.rect(self.screen, (255, 255, 0), (color_x, color_y, 100, 60), 4)
            
            # Draw progress
            progress_text = f"Цвета: {colors_found}/{colors_needed}"
            progress_surface = font_medium.render(progress_text, True, WHITE)
            self.screen.blit(progress_surface, (20, 20))
            
            # Draw time
            time_text = f"Время: {int(time_left)}с"
            time_color = WHITE if time_left > 10 else RED
            time_surface = font_medium.render(time_text, True, time_color)
            self.screen.blit(time_surface, (20, 60))
            
            # Draw instructions
            instructions = [
                f"Найди {colors_needed} красивых цветов за {time_limit} секунд!",
                "Кликни на нужные цвета!",
                "ESC - выйти"
            ]
            
            for i, instruction in enumerate(instructions):
                inst_surface = font_small.render(instruction, True, GRAY)
                self.screen.blit(inst_surface, (20, SCREEN_HEIGHT - 100 + i * 25))
            
            pygame.display.flip()
        
        return False