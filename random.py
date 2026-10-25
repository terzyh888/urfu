import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
import os


@dataclass
class Task:
    """Представляет отдельную задачу в системе."""
    id: int
    title: str
    description: str
    priority: str  # 'низкий', 'средний', 'высокий'
    status: str = "в процессе"  # 'в процессе', 'выполнена', 'отменена'
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M")
    completed_at: Optional[str] = None

    def mark_completed(self) -> None:
        """Отмечает задачу как выполненную."""
        self.status = "выполнена"
        self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def mark_cancelled(self) -> None:
        """Отменяет задачу."""
        self.status = "отменена"


class TaskManager:
    """Управляет списком задач, их сохранением и фильтрацией."""

    def __init__(self, filename: str = "tasks.json") -> None:
        self.filename: str = filename
        self.tasks: List[Task] = []
        self.load_from_file()

    def add_task(self, title: str, description: str, priority: str) -> Task:
        """Создает и добавляет новую задачу."""
        new_id = max([task.id for task in self.tasks], default=0) + 1
        task = Task(
            id=new_id,
            title=title,
            description=description,
            priority=priority.lower()
        )
        self.tasks.append(task)
        self.save_to_file()
        return task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Ищет задачу по ее уникальному идентификатору."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def remove_task(self, task_id: int) -> bool:
        """Удаляет задачу по ID."""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_to_file()
            return True
        return False

    def filter_by_status(self, status: str) -> List[Task]:
        """Возвращает список задач с указанным статусом."""
        return [task for task in self.tasks if task.status == status.lower()]

    def get_statistics(self) -> Dict[str, Any]:
        """Возвращает общую статистику по всем задачам."""
        total = len(self.tasks)
        if total == 0:
            return {"total": 0, "completed": 0, "in_progress": 0, "cancelled": 0, "completion_rate": 0.0}

        completed = len([t for t in self.tasks if t.status == "выполнена"])
        in_progress = len([t for t in self.tasks if t.status == "в процессе"])
        cancelled = len([t for t in self.tasks if t.status == "отменена"])
        rate = round((completed / total) * 100, 2)

        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "cancelled": cancelled,
            "completion_rate": rate
        }

    def save_to_file(self) -> None:
        """Сохраняет все задачи в JSON-файл."""
        try:
            data = [asdict(task) for task in self.tasks]
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка при сохранении файла: {e}")

    def load_from_file(self) -> None:
        """Загружает задачи из JSON-файла, если он существует."""
        if not os.path.exists(self.filename):
            return
        
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.tasks = [Task(**item) for item in data]
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка при чтении файла данных: {e}")
            self.tasks = []


def print_task_table(tasks: List[Task]) -> None:
    """Выводит список задач в читаемом табличном виде."""
    if not tasks:
        print("\nСписок задач пуст.")
        return

    print("\n" + "=" * 80)
    print(f"{'ID':<4} | {'Название':<20} | {'Приоритет':<10} | {'Статус':<12} | {'Создано':<16}")
    print("-" * 80)
    for task in tasks:
        print(f"{task.id:<4} | {task.title[:18]:<20} | {task.priority:<10} | {task.status:<12} | {task.created_at:<16}")
    print("=" * 80)


def main() -> None:
    """Главная функция для демонстрации работы менеджера задач."""
    manager = TaskManager("demo_tasks.json")

    # Демонстрация добавления задач, если список пуст
    if not manager.tasks:
        manager.add_task("Изучить Python", "Пройти продвинутые темы ООП и декораторов", "высокий")
        manager.add_task("Написать отчет", "Подготовить квартальный отчет по проекту", "средний")
        manager.add_task("Купить продукты", "Молоко, хлеб, кофе", "низкий")

    while True:
        print("\n--- МЕНЕДЖЕР ЗАДАЧ ---")
        print("1. Показать все задачи")
        print("2. Добавить задачу")
        print("3. Завершить задачу")
        print("4. Удалить задачу")
        print("5. Показать статистику")
        print("6. Выход")

        choice = input("Выберите пункт меню (1-6): ").strip()

        if choice == "1":
            print_task_table(manager.tasks)

        elif choice == "2":
            title = input("Введите название задачи: ").strip()
            desc = input("Введите описание задачи: ").strip()
            priority = input("Введите приоритет (низкий/средний/высокий): ").strip()
            if title:
                manager.add_task(title, desc, priority if priority else "средний")
                print("Задача успешно добавлена!")
            else:
                print("Название не может быть пустым.")

        elif choice == "3":
            print_task_table(manager.tasks)
            try:
                task_id = int(input("Введите ID задачи для завершения: "))
                task = manager.get_task_by_id(task_id)
                if task:
                    task.mark_completed()
                    manager.save_to_file()
                    print(f"Задача #{task_id} отмечена как выполненная.")
                else:
                    print("Задача с таким ID не найдена.")
            except ValueError:
                print("Пожалуйста, введите корректный числовой ID.")

        elif choice == "4":
            print_task_table(manager.tasks)
            try:
                task_id = int(input("Введите ID задачи для удаления: "))
                if manager.remove_task(task_id):
                    print(f"Задача #{task_id} удалена.")
                else:
                    print("Задача с таким ID не найдена.")
            except ValueError:
                print("Пожалуйста, введите корректный числовой ID.")

        elif choice == "5":
            stats = manager.get_statistics()
            print("\n--- СТАТИСТИКА ПРОЕКТА ---")
            print(f"Всего задач: {stats['total']}")
            print(f"Выполнено: {stats['completed']}")
            print(f"В процессе: {stats['in_progress']}")
            print(f"Отменено: {stats['cancelled']}")
            print(f"Процент выполнения: {stats['completion_rate']}%")

        elif choice == "6":
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 6.")


if __name__ == "__main__":
    main()
