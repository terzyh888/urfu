import random
import json
import os
from typing import List, Dict, Optional, Tuple


class Item:
    """Предмет в инвентаре или на карте."""
    def __init__(self, name: str, item_type: str, value: int):
        self.name = name
        self.item_type = item_type  # 'weapon', 'potion', 'treasure'
        self.value = value


class Entity:
    """Базовый класс для игрока и монстров."""
    def __init__(self, name: str, hp: int, attack: int, defense: int):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        actual_damage = max(1, amount - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage


class Player(Entity):
    """Игрок."""
    def __init__(self, name: str):
        super().__init__(name=name, hp=100, attack=15, defense=5)
        self.inventory: List[Item] = []
        self.gold: int = 0
        self.x: int = 0
        self.y: int = 0

    def heal(self, amount: int) -> None:
        self.hp = min(self.max_hp, self.hp + amount)


class GameMap:
    """Игровая карта-лабиринт."""
    def __init__(self, width: int = 10, height: int = 10):
        self.width = width
        self.height = height
        self.grid: List[List[str]] = []
        self.enemies: Dict[Tuple[int, int], Entity] = {}
        self.items: Dict[Tuple[int, int], Item] = {}
        self.exit_pos: Tuple[int, int] = (width - 1, height - 1)
        self.generate_map()

    def generate_map(self) -> None:
        """Создает пустую сетку и заполняет ее случайными объектами."""
        self.grid = [["." for _ in range(self.width)] for _ in range(self.height)]
        
        # Размещение врагов
        for _ in range(8):
            rx, ry = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if (rx, ry) != (0, 0) and (rx, ry) != self.exit_pos:
                enemy_types = [
                    ("Гоблин", 30, 8, 2),
                    ("Скелет", 40, 12, 3),
                    ("Орк", 60, 16, 5)
                ]
                name, hp, atk, df = random.choice(enemy_types)
                self.enemies[(rx, ry)] = Entity(name, hp, atk, df)
                self.grid[ry][rx] = "M"

        # Размещение предметов
        for _ in range(6):
            rx, ry = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if (rx, ry) != (0, 0) and (rx, ry) not in self.enemies and (rx, ry) != self.exit_pos:
                item_types = [
                    ("Зелье лечения", "potion", 25),
                    ("Ржавый меч", "weapon", 5),
                    ("Мешочек золота", "treasure", 50)
                ]
                name, itype, val = random.choice(item_types)
                self.items[(rx, ry)] = Item(name, itype, val)
                self.grid[ry][rx] = "I"

        # Установка выхода
        ex, ey = self.exit_pos
        self.grid[ey][ex] = "E"

    def render(self, player_x: int, player_y: int) -> None:
        """Отрисовывает карту в консоли."""
        print("\n" + "=" * (self.width * 2 + 3))
        for y in range(self.height):
            row_str = "| "
            for x in range(self.width):
                if x == player_x and y == player_y:
                    row_str += "P "
                else:
                    # Скрываем врагов и предметы до исследования, либо показываем
                    cell = self.grid[y][x]
                    row_str += f"{cell} "
            row_str += "|"
            print(row_str)
        print("=" * (self.width * 2 + 3))
        print(" Легенда: P - Игрок | M - Монстр | I - Предмет | E - Выход | . - Пусто")


class Game:
    """Главный класс игрового процесса."""
    def __init__(self):
        self.player: Optional[Player] = None
        self.game_map: Optional[GameMap] = None

    def start_new_game(self) -> None:
        name = input("Введите имя вашего героя: ").strip()
        if not name:
            name = "Странник"
        self.player = Player(name)
        self.game_map = GameMap(10, 10)
        print(f"\nДобро пожаловать в подземелье, {self.player.name}!")
        self.main_loop()

    def main_loop(self) -> None:
        while self.player.is_alive:
            self.game_map.render(self.player.x, self.player.y)
            print(f"\nЗдоровье: {self.player.hp}/{self.player.max_hp} | Атака: {self.player.attack} | Золото: {self.player.gold}")
            
            action = input("\nКуда идти? (w - вверх, s - вниз, a - влево, d - вправо) или q - выход: ").lower().strip()

            if action == 'q':
                print("Выход из игры.")
                break

            dx, dy = 0, 0
            if action == 'w': dy = -1
            elif action == 's': dy = 1
            elif action == 'a': dx = -1
            elif action == 'd': dx = 1
            else:
                print("Неверная команда!")
                continue

            new_x = self.player.x + dx
            new_y = self.player.y + dy

            # Проверка границ карты
            if 0 <= new_x < self.game_map.width and 0 <= new_y < self.game_map.height:
                self.player.x = new_x
                self.player.y = new_y
                self.handle_events()
            else:
                print("Там стена! Дальше пути нет.")

        if not self.player.is_alive:
            print("\nВы погибли в темных глубинах подземелья... Игра окончена.")

    def handle_events(self) -> None:
        pos = (self.player.x, self.player.y)

        # Проверка выхода
        if pos == self.game_map.exit_pos:
            print("\nПоздравляем! Вы нашли выход и победили в этом подземелье!")
            exit(0)

        # Проверка монстров
        if pos in self.game_map.enemies:
            enemy = self.game_map.enemies[pos]
            print(f"\nВнезапная встреча! На вас напал дикий {enemy.name}!")
            self.combat(enemy)
            if self.player.is_alive:
                del self.game_map.enemies[pos]
                self.game_map.grid[pos[1]][pos[0]] = "."

        # Проверка предметов
        elif pos in self.game_map.items:
            item = self.game_map.items[pos]
            print(f"\nВы нашли предмет: {item.name}!")
            if item.item_type == 'potion':
                self.player.heal(item.value)
                print(f"Вы выпили зелье и восстановили {item.value} HP.")
            elif item.item_type == 'weapon':
                self.player.attack += item.value
                print(f"Ваша атака увеличилась на {item.value}!")
            elif item.item_type == 'treasure':
                self.player.gold += item.value
                print(f"Вы подобрали сокровище стоимостью {item.value} золота!")
            
            self.player.inventory.append(item)
            del self.game_map.items[pos]
            self.game_map.grid[pos[1]][pos[0]] = "."

    def combat(self, enemy: Entity) -> None:
        while self.player.is_alive and enemy.is_alive:
            print(f"\n--- БОЙ --- [{self.player.name}: {self.player.hp} HP] vs [{enemy.name}: {enemy.hp} HP]")
            choice = input("1. Атаковать\n2. Попытаться сбежать\nВыберите действие: ").strip()

            if choice == '1':
                # Удар игрока
                dmg_to_enemy = self.player.attack
                actual_d_e = enemy.take_damage(dmg_to_enemy)
                print(f"Вы ударили {enemy.name} на {actual_d_e урона.")

                if not enemy.is_alive:
                    print(f"Вы победили монстра {enemy.name}!")
                    break

                # Удар врага в ответ
                dmg_to_player = enemy.attack
                actual_d_p = self.player.take_damage(dmg_to_player)
                print(f"{enemy.name} контратакует и наносит вам {actual_d_p} урона.")

            elif choice == '2':
                if random.random() > 0.5:
                    print("Вам удалось успешно сбежать с поля боя!")
                    # Отступление назад
                    self.player.x = max(0, self.player.x - 1)
                    break
                else:
                    print("Побег не удался! Враг преграждает путь.")
                    dmg_to_player = enemy.attack
                    actual_d_p = self.player.take_damage(dmg_to_player)
                    print(f"Враг пользуется моментом и наносит {actual_d_p} урона.")
            else:
                print("Неверный выбор.")


if __name__ == "__main__":
    game = Game()
    game.start_new_game()
