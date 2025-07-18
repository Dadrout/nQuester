#!/usr/bin/env python3
"""
nQuester: Incubator Rush - DEMO версия
Демонстрация концепта без pygame
"""

import time
import random

class GameDemo:
    def __init__(self):
        self.player_users = 0
        self.target_users = 10000
        self.completed_quests = []
        
        # Mentors and their quests
        self.mentors = {
            "Алихан Губаев (iOS)": {
                "quest": "Swift Debug Showdown", 
                "users": 500,
                "description": "Найди баг в Swift коде за 15 секунд!"
            },
            "Алибек Сеитов (AI/ML)": {
                "quest": "Train Your Brain",
                "users": 800, 
                "description": "Обучи нейросеть на котиках!"
            },
            "Бахредин Зургамбаев (TypeScript)": {
                "quest": "Strict Mode Madness",
                "users": 600,
                "description": "Ответь на вопросы по TypeScript типам!"
            },
            "Усталый студент": {
                "quest": "Burnout Simulator",
                "users": 300,
                "description": "Принеси воды уставшему студенту"
            }
        }
    
    def print_banner(self):
        """Print game banner"""
        print("🚀" + "="*50 + "🚀")
        print("    nQuester: Incubator Rush - DEMO")
        print("    2D RPG игра про nFactorial")
        print("🚀" + "="*50 + "🚀")
        print()
    
    def print_status(self):
        """Print current game status"""
        progress = (self.player_users / self.target_users) * 100
        progress_bar = "█" * int(progress // 5) + "░" * (20 - int(progress // 5))
        
        print(f"👥 Пользователи: {self.player_users:,}/{self.target_users:,}")
        print(f"📊 Прогресс: [{progress_bar}] {progress:.1f}%")
        print(f"✅ Выполнено квестов: {len(self.completed_quests)}")
        print()
    
    def show_available_quests(self):
        """Show available quests"""
        print("📋 Доступные квесты от менторов:")
        print("-" * 40)
        
        available = []
        for i, (mentor, data) in enumerate(self.mentors.items(), 1):
            if mentor not in self.completed_quests:
                available.append((i, mentor, data))
                print(f"{i}. {mentor}")
                print(f"   🎯 {data['quest']}")
                print(f"   👥 Награда: +{data['users']:,} пользователей")
                print(f"   💬 {data['description']}")
                print()
        
        return available
    
    def simulate_swift_debug(self):
        """Simulate Swift debugging minigame"""
        print("🛠️  МИНИ-ИГРА: Swift Debug Showdown")
        print("=" * 40)
        
        code_lines = [
            "1. let name = \"Alex\"",
            "2. var age: Int = 25", 
            "3. let users = 1000",
            "4. const isActive = true  ← БАГ!",
            "5. print(\"Hello World\")"
        ]
        
        print("Найди ошибку в Swift коде:")
        for line in code_lines:
            print(line)
        
        print("\nВ строке 4 используется 'const' вместо 'let'!")
        print("⏱️  Время: 12.3s / 15.0s")
        print("✅ УСПЕХ! Баг найден!")
        
        return True
    
    def simulate_ai_training(self):
        """Simulate AI training minigame"""
        print("🧠 МИНИ-ИГРА: Train Your Brain")
        print("=" * 40)
        
        print("Перетащи котиков к модели нейросети:")
        print("🐱 🐶 🐱 🧠 🐱 🐶 🐱")
        print("     ↓    ↓    ↓")
        print("        🧠")
        print("      МОДЕЛЬ")
        
        print("\n✅ Обучено на 5 котиках!")
        print("📊 Точность распознавания: 99%")
        print("🎉 Модель готова к продакшену!")
        
        return True
    
    def simulate_ts_quiz(self):
        """Simulate TypeScript quiz"""
        print("📝 МИНИ-ИГРА: Strict Mode Madness")
        print("=" * 40)
        
        questions = [
            {
                "q": "Какой тип у user.name?",
                "code": "const user = { id: 1, name: 'Alex' }",
                "answer": "string"
            },
            {
                "q": "Что не так с этим кодом?", 
                "code": "let value: any = 'hello'",
                "answer": "Используется any type"
            }
        ]
        
        score = 0
        for i, question in enumerate(questions, 1):
            print(f"\nВопрос {i}: {question['q']}")
            print(f"Код: {question['code']}")
            print(f"Ответ: {question['answer']}")
            score += 1
        
        print(f"\n✅ Результат: {score}/{len(questions)} правильных ответов!")
        return score >= len(questions) // 2
    
    def simulate_fetch_quest(self):
        """Simulate fetch quest"""
        print("🚶 КВЕСТ: Burnout Simulator")
        print("=" * 40)
        
        print("Усталый студент: 'Кажется, я слышу цвета...'")
        print("Задача: Найди бутылку воды")
        print()
        print("🚶 Идешь к кухне...")
        print("🔍 Ищешь в холодильнике...")
        print("💧 Нашел бутылку воды!")
        print("🚶 Возвращаешься к студенту...")
        print()
        print("Студент: 'Ах, гидратация... Теперь лучше!'")
        print("✅ Квест выполнен!")
        
        return True
    
    def run_quest(self, mentor, quest_data):
        """Run a specific quest"""
        print(f"\n🎮 Начинаем квест: {quest_data['quest']}")
        print(f"📝 Ментор: {mentor}")
        print()
        
        # Simulate different quest types
        if "Debug" in quest_data['quest']:
            success = self.simulate_swift_debug()
        elif "Brain" in quest_data['quest']:
            success = self.simulate_ai_training()
        elif "TypeScript" in quest_data['quest']:
            success = self.simulate_ts_quiz()
        else:
            success = self.simulate_fetch_quest()
        
        if success:
            self.player_users += quest_data['users']
            self.completed_quests.append(mentor)
            print(f"\n🎉 Квест выполнен!")
            print(f"👥 +{quest_data['users']:,} пользователей")
            print(f"📈 Всего пользователей: {self.player_users:,}")
        else:
            print("\n😔 Квест провален. Попробуй позже!")
        
        print("\n" + "="*50)
        return success
    
    def check_victory(self):
        """Check if player won"""
        if self.player_users >= self.target_users:
            print("🎉🎉🎉 ПОЗДРАВЛЯЕМ! 🎉🎉🎉")
            print(f"Вы привлекли {self.player_users:,} пользователей!")
            print("🚀 Ваш стартап готов к Demo Day!")
            print("💰 Инвесторы выстроились в очередь!")
            print()
            
            if len(self.completed_quests) == len(self.mentors):
                print("👑 ПЕРФЕКТНАЯ ПОБЕДА!")
                print("Все квесты выполнены!")
            
            return True
        return False
    
    def run_demo(self):
        """Run the game demo"""
        self.print_banner()
        
        print("🎯 ЦЕЛЬ: Привлечь 10,000 пользователей до Demo Day")
        print("🎮 ГЕЙМПЛЕЙ: Выполняй квесты от менторов nFactorial")
        print()
        
        while not self.check_victory():
            self.print_status()
            available_quests = self.show_available_quests()
            
            if not available_quests:
                print("Все квесты выполнены, но цель не достигнута!")
                break
            
            try:
                choice = input("Выберите квест (номер) или 'q' для выхода: ").strip()
                
                if choice.lower() == 'q':
                    break
                
                quest_num = int(choice)
                if 1 <= quest_num <= len(available_quests):
                    _, mentor, quest_data = available_quests[quest_num - 1]
                    self.run_quest(mentor, quest_data)
                    
                    # Simulate time passing
                    time.sleep(1)
                else:
                    print("Неверный номер квеста!")
                    
            except ValueError:
                print("Введите число или 'q'")
            except KeyboardInterrupt:
                print("\n\n👋 До свидания!")
                break
            
            print()
        
        print("\n🏁 ДЕМО ЗАВЕРШЕНО!")
        print("Это была демонстрация концепта игры.")
        print("Полная версия включает:")
        print("• 2D графику с картами nFactorial")
        print("• Интерактивные мини-игры")
        print("• Анимированных персонажей") 
        print("• Звуковые эффекты")
        print("• И много nFactorial мемов!")

def main():
    demo = GameDemo()
    demo.run_demo()

if __name__ == "__main__":
    main() 