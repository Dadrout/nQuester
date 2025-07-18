import json
import os
from settings import *
from sound_manager import get_sound_manager

class QuestManager:
    def __init__(self):
        self.quests_data = {}
        self.active_quests = {}
        self.completed_quests = []
        self.load_quests()
    
    def load_quests(self):
        """Load quests from JSON file or create default quests"""
        try:
            if os.path.exists('data/quests.json'):
                with open('data/quests.json', 'r', encoding='utf-8') as f:
                    self.quests_data = json.load(f)
            else:
                # Create default quests if file doesn't exist
                self.create_default_quests()
        except:
            self.create_default_quests()
    
    def create_default_quests(self):
        """Create default quests based on design document"""
        self.quests_data = {
            "quest_alikhan_01": {
                "id": "quest_alikhan_01",
                "npc_id": "Alikhan",
                "title": "Swift Debug Showdown",
                "dialogue_start": [
                    "У меня есть баг в iOS коде.",
                    "Найди ошибку за 15 секунд!"
                ],
                "dialogue_complete": "Отлично! Debugging skills на высоте!",
                "user_feedback": [
                    "🔥 Отличная работа! Код теперь работает стабильно!",
                    "Спасибо за помощь с iOS! Приложение больше не крашится!",
                    "Настоящий профессионал! Debugging на высшем уровне!"
                ],
                "type": "minigame",
                "minigame_id": "swift_debug",
                "reward": {"users": 500, "item": "iOS Certificate"}
            },
            "quest_alibeck_01": {
                "id": "quest_alibeck_01", 
                "npc_id": "Alibeck",
                "title": "Train Your Brain",
                "dialogue_start": [
                    "Время тренировать нейросеть!",
                    "Перетащи данные с котиками к модели."
                ],
                "dialogue_complete": "Модель обучена! Котики распознаются на 99%!",
                "user_feedback": [
                    "🤖 AI теперь работает идеально! Спасибо!",
                    "Модель стала намного умнее! Отличная работа!",
                    "Нейросеть теперь понимает котиков как никто другой!"
                ],
                "type": "minigame",
                "minigame_id": "ai_training",
                "reward": {"users": 800, "item": "AI Insight"}
            },
            "quest_bahredin_01": {
                "id": "quest_bahredin_01",
                "npc_id": "Bahredin", 
                "title": "Strict Mode Madness",
                "dialogue_start": [
                    "Я нашел `any` в нашей кодовой базе.",
                    "Это не просьба. Это ЧП. Исправь."
                ],
                "dialogue_complete": "Спасибо. Кодовая база в безопасности.",
                "user_feedback": [
                    "🔒 TypeScript теперь строгий! Спасибо за безопасность!",
                    "Код стал намного надежнее! Отличная работа!",
                    "Больше никаких any! Кодовая база спасена!"
                ],
                "type": "minigame",
                "minigame_id": "ts_quiz",
                "reward": {"users": 600, "item": "Type Safety Certificate"}
            },
            "quest_bahaudin_01": {
                "id": "quest_bahaudin_01",
                "npc_id": "Bahaudin",
                "title": "Memory Leak Hunter",
                "dialogue_start": [
                    "Сервер падает каждые 5 минут.",
                    "Найди утечку памяти в коде!"
                ],
                "dialogue_complete": "Сервер стабилен! Спасибо за помощь!",
                "user_feedback": [
                    "💾 Сервер больше не падает! Спасибо!",
                    "Память теперь используется эффективно! Отличная работа!",
                    "Сервер работает как часы! Настоящий профессионал!"
                ],
                "type": "minigame",
                "minigame_id": "memory_leak_hunter",
                "reward": {"users": 400, "item": "Backend Certificate"}
            },
            "quest_gaziz_01": {
                "id": "quest_gaziz_01",
                "npc_id": "Gaziz",
                "title": "React Debug Challenge",
                "dialogue_start": [
                    "React компонент не рендерится.",
                    "Проверь пропсы и состояние!"
                ],
                "dialogue_complete": "Компонент работает! Frontend спасен!",
                "user_feedback": [
                    "⚛️ React компонент теперь работает идеально!",
                    "Frontend спасен! Спасибо за отладку!",
                    "Компонент рендерится как надо! Отличная работа!"
                ],
                "type": "minigame",
                "minigame_id": "react_debug",
                "reward": {"users": 350, "item": "Frontend Certificate"}
            },
            "quest_shoqan_01": {
                "id": "quest_shoqan_01",
                "npc_id": "Shoqan",
                "title": "Frontend Debug Master",
                "dialogue_start": [
                    "У меня проблема с React компонентом.",
                    "Найди и исправь баги в JavaScript коде!"
                ],
                "dialogue_complete": "Компонент работает! Frontend dev на высоте!",
                "user_feedback": [
                    "⚛️ React компонент теперь стабильно! Спасибо!",
                    "JavaScript код исправлен! Отличная работа!",
                    "Настоящий frontend эксперт! Компонент спасен!"
                ],
                "type": "minigame",
                "minigame_id": "react_debug",
                "reward": {"users": 450, "item": "Frontend Certificate"}
            },
            "quest_zhasulan_01": {
                "id": "quest_zhasulan_01",
                "npc_id": "Zhasulan",
                "title": "iOS Debug Challenge",
                "dialogue_start": [
                    "У меня проблема с iOS приложением.",
                    "Найди и исправь баги в Swift коде!"
                ],
                "dialogue_complete": "iOS приложение работает! Отличная работа!",
                "user_feedback": [
                    "📱 iOS приложение теперь стабильно! Спасибо!",
                    "Swift код исправлен! Отличная работа!",
                    "Настоящий iOS разработчик! Приложение спасено!"
                ],
                "type": "minigame",
                "minigame_id": "swift_debug",
                "reward": {"users": 400, "item": "iOS Certificate"}
            },
            "quest_aimurat_01": {
                "id": "quest_aimurat_01",
                "npc_id": "Aimurat",
                "title": "AI Model Training",
                "dialogue_start": [
                    "Мне нужно обучить нейросеть.",
                    "Помоги с тренировкой AI модели!"
                ],
                "dialogue_complete": "Модель обучена! AI работает отлично!",
                "user_feedback": [
                    "🤖 AI модель обучена успешно! Спасибо!",
                    "Нейросеть теперь работает идеально! Отличная работа!",
                    "Настоящий AI/ML эксперт! Модель спасена!"
                ],
                "type": "minigame",
                "minigame_id": "ai_training",
                "reward": {"users": 600, "item": "AI Certificate"}
            },
            "quest_bernar_01": {
                "id": "quest_bernar_01",
                "npc_id": "Bernar",
                "title": "BOSS: Final Challenge",
                "dialogue_start": [
                    "Ты думаешь, что готов к финальному испытанию?",
                    "Докажи, что ты достоин быть лучшим стартапером!",
                    "Пройди все этапы: архитектура, кодинг, тестирование!"
                ],
                "dialogue_complete": "Импрессивно! Ты прошел финальное испытание!",
                "user_feedback": [
                    "🏆 НАСТОЯЩИЙ БОСС! Ты прошел все испытания!",
                    "Ты доказал, что достоин быть лучшим стартапером!",
                    "Архитектура, кодинг, тестирование - все на высоте!",
                    "Инвесторы будут в восторге от такого профессионала!"
                ],
                "type": "minigame",
                "minigame_id": "boss_challenge",
                "reward": {"users": 2000, "item": "BOSS Certificate"}
            },
            "quest_final_boss": {
                "id": "quest_final_boss",
                "npc_id": "FinalBoss",
                "title": "ФИНАЛЬНЫЙ БОСС",
                "dialogue_start": [
                    "Ты думаешь, что готов к настоящему испытанию?",
                    "Столкнись с главным боссом в эпической JRPG битве!",
                    "Чем больше у тебя пользователей, тем слабее босс!"
                ],
                "dialogue_complete": "НЕВЕРОЯТНО! Ты победил главного босса!",
                "user_feedback": [
                    "🏆 ЛЕГЕНДА! Ты победил главного босса!",
                    "Ты доказал, что достоин быть лучшим стартапером!",
                    "JRPG битва завершена! Ты настоящий герой!",
                    "Инвесторы будут в восторге от такого профессионала!"
                ],
                "type": "boss_battle",
                "reward": {"users": 5000, "item": "Legendary Certificate"}
            },
            "quest_diana_frontend": {
                "id": "quest_diana_frontend",
                "npc_id": "Diana",
                "title": "Фронтенд дизайнер",
                "dialogue_start": [
                    "Привет! Я Diana, эксперт по фронтенд разработке.",
                    "Мне нужен помощник для создания красивого интерфейса.",
                    "Пройди мини-игру 'UI/UX Дизайнер' - создай отзывчивый интерфейс!",
                    "Покажи, что ты понимаешь принципы современного дизайна!"
                ],
                "dialogue_complete": "Отличная работа! Ты настоящий дизайнер!",
                "user_feedback": [
                    "🎨 UI/UX ДИЗАЙНЕР!",
                    "Ты создал красивый интерфейс!",
                    "Diana довольна твоими навыками!",
                    "Ты готов к созданию современных веб-приложений!"
                ],
                "type": "minigame",
                "minigame_id": "ui_designer",
                "reward": {"users": 700, "item": "Frontend Certificate"}
            },
            "quest_tamyrlan_backend": {
                "id": "quest_tamyrlan_backend",
                "npc_id": "Tamyrlan",
                "title": "Бэкенд архитектор",
                "dialogue_start": [
                    "Привет! Я Tamyrlan, эксперт по бэкенд архитектуре.",
                    "Мне нужен помощник для создания масштабируемой системы.",
                    "Пройди мини-игру 'Архитектор API' - спроектируй REST API!",
                    "Покажи, что ты понимаешь принципы бэкенд разработки!"
                ],
                "dialogue_complete": "Отличная работа! Ты настоящий архитектор!",
                "user_feedback": [
                    "🏗️ АРХИТЕКТОР API!",
                    "Ты спроектировал отличную систему!",
                    "Tamyrlan доволен твоими навыками!",
                    "Ты готов к созданию масштабируемых приложений!"
                ],
                "type": "minigame",
                "minigame_id": "api_architect",
                "reward": {"users": 800, "item": "Backend Certificate"}
            },
            "quest_student_tired": {
                "id": "quest_student_tired",
                "npc_id": "tired_student",
                "title": "Burnout Simulator", 
                "dialogue_start": [
                    "Кажется, я слышу цвета...",
                    "Можешь найти мне бутылку воды?"
                ],
                "dialogue_complete": "Ах, гидратация. Чувствую себя... чуть более человеком.",
                "user_feedback": [
                    "💧 Спасибо за воду! Теперь могу кодить дальше!",
                    "Гидратация - ключ к успеху! Спасибо!",
                    "Вода спасла мой день! Теперь все хорошо!"
                ],
                "type": "fetch",
                "item_to_fetch": "water_bottle",
                "reward": {"users": 300, "item": "Energy Drink"}
            },
            # Новые разнообразные квесты
            "quest_student_coffee": {
                "id": "quest_student_coffee",
                "npc_id": "coffee_student",
                "title": "Кофейный кликер",
                "dialogue_start": [
                    "Мне нужен кофе! Много кофе!",
                    "Кликни 50 раз за 30 секунд!"
                ],
                "dialogue_complete": "Кофе готов! Теперь я могу кодить!",
                "user_feedback": [
                    "☕ Кофе спас мой день! Спасибо!",
                    "Теперь я полон энергии! Отличная работа!",
                    "Кофе - лучший друг программиста!"
                ],
                "type": "clicker",
                "clicks_needed": 50,
                "time_limit": 30,
                "reward": {"users": 200, "item": "Coffee"}
            },
            "quest_student_coding": {
                "id": "quest_student_coding",
                "npc_id": "coding_student",
                "title": "Поймай котика!",
                "dialogue_start": [
                    "Мне нужен котик для моего проекта!",
                    "Поймай всех котиков на карте!"
                ],
                "dialogue_complete": "Котики пойманы! Проект спасен!",
                "user_feedback": [
                    "🐱 Котики спасены! Спасибо!",
                    "Теперь у меня есть котики для проекта!",
                    "Котики - лучшие тестировщики!"
                ],
                "type": "minigame",
                "minigame_id": "treasure_collector",  # Используем нашу новую игру с котиками
                "reward": {"users": 400, "item": "Cat Certificate"}
            },
            "quest_student_hungry": {
                "id": "quest_student_hungry",
                "npc_id": "hungry_student",
                "title": "Голодный студент",
                "dialogue_start": [
                    "Я голоден! Очень голоден!",
                    "Принеси мне пиццу!"
                ],
                "dialogue_complete": "Пицца! Спасибо! Теперь я могу работать!",
                "user_feedback": [
                    "🍕 Пицца спасла мой день! Спасибо!",
                    "Теперь я сыт и готов к работе!",
                    "Пицца - лучшая еда для программиста!"
                ],
                "type": "fetch",
                "item_to_fetch": "pizza",
                "reward": {"users": 250, "item": "Pizza"}
            },
            "quest_student_sleepy": {
                "id": "quest_student_sleepy",
                "npc_id": "sleepy_student",
                "title": "Сонный студент",
                "dialogue_start": [
                    "Я так устал...",
                    "Найди мне подушку!"
                ],
                "dialogue_complete": "Подушка! Теперь я могу отдохнуть!",
                "user_feedback": [
                    "🛏️ Подушка спасла мой сон! Спасибо!",
                    "Теперь я отдохну и буду работать лучше!",
                    "Сон - важная часть программирования!"
                ],
                "type": "fetch",
                "item_to_fetch": "pillow",
                "reward": {"users": 150, "item": "Pillow"}
            },
            "quest_student_gaming": {
                "id": "quest_student_gaming",
                "npc_id": "gaming_student",
                "title": "Геймерский кликер",
                "dialogue_start": [
                    "Мне нужно прокачать персонажа!",
                    "Кликни 100 раз за 20 секунд!"
                ],
                "dialogue_complete": "Персонаж прокачан! Теперь я сильный!",
                "user_feedback": [
                    "🎮 Персонаж прокачан! Спасибо!",
                    "Теперь я сильный геймер!",
                    "Геймификация - будущее обучения!"
                ],
                "type": "clicker",
                "clicks_needed": 100,
                "time_limit": 20,
                "reward": {"users": 350, "item": "Gaming Certificate"}
            },
            "quest_student_music": {
                "id": "quest_student_music",
                "npc_id": "music_student",
                "title": "Музыкальный ритм",
                "dialogue_start": [
                    "Мне нужна музыка для кодинга!",
                    "Попади в ритм - кликай в такт!"
                ],
                "dialogue_complete": "Отличный ритм! Музыка вдохновляет!",
                "user_feedback": [
                    "🎵 Музыка спасла мой код! Спасибо!",
                    "Теперь я кодирую под ритм!",
                    "Музыка - лучший помощник программиста!"
                ],
                "type": "rhythm",
                "beats_needed": 20,
                "time_limit": 30,
                "reward": {"users": 300, "item": "Music Certificate"}
            },
            "quest_student_sport": {
                "id": "quest_student_sport",
                "npc_id": "sport_student",
                "title": "Спортивный вызов",
                "dialogue_start": [
                    "Мне нужно размяться!",
                    "Сделай 30 отжиманий (кликов)!"
                ],
                "dialogue_complete": "Отлично! Теперь я в форме!",
                "user_feedback": [
                    "💪 Спорт спас мое здоровье! Спасибо!",
                    "Теперь я сильный и здоровый!",
                    "Спорт - важная часть жизни программиста!"
                ],
                "type": "clicker",
                "clicks_needed": 30,
                "time_limit": 45,
                "reward": {"users": 200, "item": "Sport Certificate"}
            },
            "quest_student_art": {
                "id": "quest_student_art",
                "npc_id": "art_student",
                "title": "Художественный вкус",
                "dialogue_start": [
                    "Мне нужен вдохновляющий арт!",
                    "Найди красивые цвета!"
                ],
                "dialogue_complete": "Красивые цвета! Теперь я вдохновлен!",
                "user_feedback": [
                    "🎨 Арт вдохновил меня! Спасибо!",
                    "Теперь я создаю красивые интерфейсы!",
                    "Арт - важная часть дизайна!"
                ],
                "type": "color_picker",
                "colors_needed": 5,
                "time_limit": 60,
                "reward": {"users": 250, "item": "Art Certificate"}
            },
            "quest_student_book": {
                "id": "quest_student_book",
                "npc_id": "book_student",
                "title": "Книжный червь",
                "dialogue_start": [
                    "Мне нужна новая книга по программированию!",
                    "Принеси мне книгу!"
                ],
                "dialogue_complete": "Книга! Теперь я умнее!",
                "user_feedback": [
                    "📚 Книга расширила мои знания! Спасибо!",
                    "Теперь я знаю больше!",
                    "Книги - лучшие учителя!"
                ],
                "type": "fetch",
                "item_to_fetch": "book",
                "reward": {"users": 180, "item": "Book"}
            }
        }
    
    def start_quest(self, quest_id, player):
        """Start a quest"""
        if quest_id in self.quests_data and quest_id not in self.active_quests:
            quest = self.quests_data[quest_id].copy()
            self.active_quests[quest_id] = quest
            if quest_id not in player.quest_log:
                player.quest_log.append(quest_id)
            
            # Play quest start sound
            sound_manager = get_sound_manager()
            if sound_manager:
                sound_manager.play_quest_start()
            
            return True
        return False
    
    def check_completion(self, quest_id, player):
        """Check if quest completion conditions are met"""
        if quest_id not in self.active_quests:
            return False
            
        quest = self.active_quests[quest_id]
        
        if quest["type"] == "fetch":
            required_item = quest.get("item_to_fetch")
            return player.has_item(required_item)
        elif quest["type"] == "minigame":
            # Minigame completion is handled separately
            return quest.get("completed", False)
        elif quest["type"] == "clicker":
            # Clicker completion is handled separately
            return quest.get("completed", False)
        elif quest["type"] == "rhythm":
            # Rhythm completion is handled separately
            return quest.get("completed", False)
        elif quest["type"] == "color_picker":
            # Color picker completion is handled separately
            return quest.get("completed", False)
        elif quest["type"] == "boss_battle":
            # Boss battle completion is handled separately
            return quest.get("completed", False)
        
        return False
    
    def complete_quest(self, quest_id, player):
        """Complete a quest and give rewards"""
        if quest_id not in self.active_quests:
            return False
            
        quest = self.active_quests[quest_id]
        
        # Get improved rewards from improvement system
        try:
            from improvements import get_improvement_manager
            improvement_manager = get_improvement_manager()
            
            if improvement_manager:
                # Determine difficulty based on quest type
                difficulty = "normal"
                if "boss" in quest_id.lower():
                    difficulty = "boss"
                elif "final" in quest_id.lower():
                    difficulty = "hard"
                
                # Get enhanced reward
                reward_data = improvement_manager.reward_system.give_reward(quest_id, difficulty)
                users_gained = reward_data["users"]
                item = reward_data.get("item")
                
                # Apply reward
                player.current_users += users_gained
                
                # Add item to player inventory if received
                if item and hasattr(player, 'inventory'):
                    if not hasattr(player, 'inventory'):
                        player.inventory = []
                    player.inventory.append(item)
                
                # Show reward animation
                improvement_manager.show_reward_animation("пользователей", users_gained)
                if item:
                    improvement_manager.show_reward_animation("предмет", item.name)
                
                # Update progress tracking
                improvement_manager.progress_tracker.update_quest_progress(quest_id, completed=True)
                
                print(f"✅ Квест {quest_id} завершен! Получено {users_gained} пользователей")
                if item:
                    print(f"🎁 Получен предмет: {item.name}")
                
                # Remove from active and add to completed
                del self.active_quests[quest_id]
                if quest_id in player.quest_log:
                    player.quest_log.remove(quest_id)
                self.completed_quests.append(quest_id)
                
                # Play quest completion sound
                sound_manager = get_sound_manager()
                if sound_manager:
                    sound_manager.play_quest_complete()
                
                return True
        except Exception as e:
            print(f"⚠️ Ошибка в системе улучшений: {e}")
        
        # Fallback to original reward system
        reward = quest.get("reward", {})
        
        # Give rewards
        if "users" in reward:
            player.current_users += reward["users"]
        if "item" in reward:
            if hasattr(player, 'add_item'):
                player.add_item(reward["item"])
            
        # Remove from active and add to completed
        del self.active_quests[quest_id]
        if quest_id in player.quest_log:
            player.quest_log.remove(quest_id)
        self.completed_quests.append(quest_id)
        
        # Play quest completion sound
        sound_manager = get_sound_manager()
        if sound_manager:
            sound_manager.play_quest_complete()
        
        return True
    
    def get_quest_data(self, quest_id):
        """Get quest data by ID"""
        return self.quests_data.get(quest_id)
    
    def mark_minigame_completed(self, quest_id):
        """Mark minigame quest as completed"""
        if quest_id in self.active_quests:
            self.active_quests[quest_id]["completed"] = True 