import random
import json
from datetime import datetime

class Character:
    def __init__(self, name, health, attack, defense, critical_chance=0):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.critical_chance = critical_chance

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def attack_move(self, opponent):
        damage = random.randint(max(1, self.attack - 10), self.attack)

        if random.random() < self.critical_chance:
            damage *= 1.5
            print('Critical hit!')

        damage - max(1, damage - opponent.defense)
        opponent.take_damage(damage)
        return damage

class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name, quantity=1):
        current = self.items.get(item_name, 0)
        self.items[item_name] = current + quantity
        print(f"Added {quantity}x {item_name}.")

    def remove_item(self, item_name, quantity=1):
        current = self.items.get(item_name, 0)

        if current < quantity:
            print(f"You don't have {quantity}x {item_name}.")
            return False

        self.items[item_name] = current - quantity

        if self.items[item_name] == 0:
            del self.items[item_name]

        return True

    def has_items(self, item_name) -> bool:
        return self.items.get(item_name, 0) > 0

    def show_items(self) -> None:
        if not self.items:
            print('Nothing in inventory.')
            return

        print("\n===== INVENTORY =====")
        for item_name, quantity in self.items.items():
            print(f'{item_name} x{quantity}')

class Player(Character):
    def __init__(self, name, health, max_health, attack=20, defense=10, luck=5, critical_chance=0.1, gold=100,
                 level=1, xp=0, inventory=None):
        super().__init__(name, health, attack, defense, critical_chance)
        self.max_health = max_health
        self.luck = luck
        self.gold = gold
        self.level = level
        self.xp = xp
        self.inventory = inventory if inventory is not None else Inventory()

    def __str__(self):
        return f"{self.name}\nHP: {self.health}/{self.max_health}\nAttack: {self.attack}\nLevel: {self.level}\nXP: {self.xp}\nGold: {self.gold}"

    def show_stats(self) -> None:
        print(self)

    def gain_xp(self, amount):
        self.xp += amount

        while self.xp >= 100:
            self.xp -= 100
            self.level += 1
            self.max_health += 10
            self.health += 10
            self.attack += 2
            print(f"{self.name} leveled up!")

    def use_potion(self):
        if not self.inventory.has_items("Potion"):
            print("You don't have any potions.")
            return

        if random.random() < 0.2:
            print("The potion failed!")
            return

        self.inventory.remove_item("Potion")
        old_health = self.health
        self.health = min(self.health + 30, self.max_health)

        print(f"You recovered {self.health - old_health} HP!")

class Enemy(Character):
    def __init__(self, name, health, attack, gold_reward, xp_reward, defense=0, critical_chance=0):
        super().__init__(name, health, attack, defense, critical_chance)
        self.gold_reward = gold_reward
        self.xp_reward = xp_reward

    def __str__(self):
        return f"{self.name}\nHP: {self.health}\nAttack: {self.attack}\nGold: {self.gold_reward}\nXP: {self.xp_reward}"

enemy_data = {
    "Goblin": {
        "health": 40,
        "attack": 12,
        "gold_reward": 30,
        "xp_reward": 20
    },
    "Wolf": {
        "health": 35,
        "attack": 15,
        "gold_reward": 20,
        "xp_reward": 18
    },
    "Skeleton": {
        "health": 50,
        "attack": 14,
        "gold_reward": 35,
        "xp_reward": 25
    },
    "Dragon": {
        "health": 150,
        "attack": 30,
        "gold_reward": 200,
        "xp_reward": 100
    }
}

loot_table = {
    "Potion": 0.4,
    "Bandage": 0.3,
    "Rare Gem": 0.1,
    "Ancient Rune": 0.05,
}

def give_loot(player, loot):
    print("\nYou found:")
    for item_name, chance in loot.items():
        if random.random() < chance:
            player.inventory.add_item(item_name)

def create_enemy():
    enemy_name = random.choice(list(enemy_data.keys()))
    stats = enemy_data[enemy_name]
    enemy = Enemy(enemy_name, **stats)
    return enemy

def start_battle(player):
    enemy = create_enemy()
    battle_over = False
    result = None

    print(f"\nA wild {enemy.name} appeared!")

    while not battle_over:
        print("\n===== BATTLE =====")
        print(f"{player.name}: {player.health}/{player.max_health} HP")
        print(f"{enemy.name}: {enemy.health} HP")
        print("\n1. Attack")
        print("2. Use Potion")
        print("3. Run")

        battle_choice = input("> ").strip()
        result = battle(player, enemy, battle_choice)

        if result is True:
            print("You won!")
            battle_over = True
        elif result is False:
            print("You lost!")
            battle_over = True
        elif result == "ran":
            battle_over = True

    return result

def battle(player, enemy, choice):
    if choice == "1":
        damage = player.attack_move(enemy)
        print(f"{player.name} deals {damage} damage to {enemy.name}.")

        if not enemy.is_alive():
            player.gold += enemy.gold_reward
            player.gain_xp(enemy.xp_reward)
            give_loot(player, loot_table)
            return True

        damage = enemy.attack_move(player)
        print(f"{enemy.name} deals {damage} damage to {player.name}.")

        if not player.is_alive():
            return False

        return None

    elif choice == "2":
        player.use_potion()

        if not player.is_alive():
            return False

        damage = enemy.attack_move(player)
        print(f"{enemy.name} deals {damage} damage to {player.name}.")

        if not player.is_alive():
            return False

        return None

    elif choice == "3":
        print("You ran away!")
        return "ran"

    else:
        print("Invalid choice.")
        return None

def explore(player):
    outcome = random.choices(
        ["enemy", "treasure", "trap", "nothing"],
        weights=[40 - player.luck, 30 + player.luck, 15, 15]
    )[0]

    if outcome == 'enemy':
        start_battle(player)
        return None

    elif outcome == 'treasure':
        treasure = random.choices(
            ["Potion", "Gold", "Bandage", "Rare Gem", "Ancient Rune"],
            weights=[40, 20, 15, 10 + player.luck, 15 + player.luck / 2]
        )[0]
        if treasure == 'Gold':
            amounts = random.randint(5, 50)
            player.gold += amounts
            print(f'You got {amounts} gold.\nYou now have {player.gold} gold.')
        else:
            player.inventory.add_item(treasure)
        return None

    elif outcome == 'trap':
        print('You ran into a trap!')
        player.take_damage(random.randint(5, 15))
        if not player.is_alive():
            if player.inventory.has_items("Potion"):
                choice = input("You're about to die! Use a potion? (y/n) > ").strip().lower()
                if choice == "y":
                    player.use_potion()
                    if not player.is_alive():
                        print("You died.")
                        return "dead"
                else:
                    print("You died.")
                    return "dead"
            else:
                print("You died.")
                return "dead"

        return None

    else:
        print('Nothing happened...')
        return None

def save_game(player):
    player_data = {
        "name": player.name,
        "health": player.health,
        "max_health": player.max_health,
        "attack": player.attack,
        "defense": player.defense,
        "luck": player.luck,
        "critical_chance": player.critical_chance,
        "gold": player.gold,
        "level": player.level,
        "xp": player.xp,
        "inventory": player.inventory.items,
        "last_saved": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open("savegame.json", "w") as file:
        json.dump(player_data, file)

    print("Game saved!")

def load_game():
    try:
        with open("savegame.json", "r") as file:
            player_data = json.load(file)

            inventory = Inventory()
            inventory.items = player_data["inventory"]

            player = Player(
                player_data["name"],
                player_data["health"],
                player_data["max_health"],
                attack=player_data["attack"],
                defense=player_data["defense"],
                luck=player_data["luck"],
                critical_chance=player_data["critical_chance"],
                gold=player_data["gold"],
                level=player_data["level"],
                xp=player_data["xp"],
                inventory=inventory
            )

        print("Game loaded!")
        return player

    except FileNotFoundError:
        print("No save file found.")
        return None

def show_menu():
    print("\n==============================")
    print("       DUNGEON QUEST")
    print("==============================")
    print("1. Explore")
    print("2. Fight")
    print("3. Inventory")
    print("4. Character")
    print("5. Save")
    print("6. Load")
    print("7. Quit")

def main():
    player = Player("Ash", 100, 100)
    player.inventory.add_item("Potion", 2)

    while True:
        show_menu()
        choice = input("> ").strip()

        if choice == "1":
            result = explore(player)
            if result == "dead":
                print("Game over!")
                break

        elif choice == "2":
            start_battle(player)

        elif choice == "3":
            player.inventory.show_items()

        elif choice == "4":
            player.show_stats()

        elif choice == "5":
            save_game(player)

        elif choice == "6":
            loaded_player = load_game()

            if loaded_player is not None:
                player = loaded_player
                print("Save loaded successfully.")

        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")
if __name__ == '__main__':
    main()