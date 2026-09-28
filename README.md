# Dungeon Quest

A turn-based RPG that runs in the terminal. Explore, fight monsters, collect loot, level up, and save your progress between sessions.

## Features

- Exploring can lead to an enemy, treasure, a trap or nothing. Your luck stat changes the odds.
- Turn-based battles against a Goblin, Wolf, Skeleton or Dragon, with attack, potion and run options.
- Critical hits, a chance for potions to fail, and a last-chance potion prompt when a trap would kill you.
- XP and levelling: every 100 XP raises your level, max health and attack.
- Loot drops from a weighted loot table.
- Save and load your game to a JSON file.

## Run it

Needs Python 3.8 or newer. No extra packages.

```
python dungeon_quest.py
```

Your progress is saved to `savegame.json` in the same folder.

## How the code is organised

| Class | Job |
| --- | --- |
| `Character` | Shared health, attack, defense and damage logic |
| `Player` | Extends `Character` with XP, gold, luck, levelling and potions |
| `Enemy` | Extends `Character` with gold and XP rewards |
| `Inventory` | Adds, removes and lists items |

Enemy stats live in the `enemy_data` dictionary and drop rates in `loot_table`, so adding a monster or item means adding one entry.

## What I practised

- Classes and inheritance
- Weighted randomness with `random.choices`
- Saving and loading with the `json` module
- Breaking a big program into small functions

## Ideas for next time

- A shop that spends gold
- Equipment that changes attack and defense
- Split the file into modules (`characters.py`, `battle.py`, `save.py`)
