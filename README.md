# COMP 163 - Project 3:⚔️ Quest Chronicles

Name: Vanessa Gray
 
Date: 02-Dec-2025

| **AI Usage** | AI assisted in writing load and parse functions, debugging, load/save character function validation, and implementing core combat/quest logic. AI also helped me create this README file. |

---

# 1. Game Data Module

*This module handles loading and validating game data from text files.*

### Data Loading Functions
| load_quests | Load quest data from file. | data/quests.txt |
| load_items | Load item data from file. | data/items.txt |
| create_default_data_files | Create default quests.txt and items.txt files if they do not exist, and creates the data directory. | N/A |

### Expected Data Formats

Data files must be separated by blank lines (`\n\n`) into blocks.

#### Quest Data Format
* QUEST_ID, TITLE, DESCRIPTION, REWARD_XP (int), REWARD_GOLD (int), REQUIRED_LEVEL (int), PREREQUISITE (or NONE).

#### Item Data Format
* ITEM_ID, NAME, TYPE (weapon/armor/consumable), EFFECT (stat:value), COST (int), DESCRIPTION.

### Validation Functions
* validate_quest_data: Ensures required fields (quest_id, title, reward_xp, etc.) are present and numerical fields are integers.
* validate_item_data: Ensures required fields (item_id, name, etc.) are present, type is one of weapon|armor|consumable, and cost is an integer.
* validate_quest_prerequisites : Checks that every PREREQUISITE (if not "NONE") refers to a valid, existing quest ID.

---

# 2. Character Manager Module

*This module handles character creation, loading, and saving.*

### Management Functions

| create_character: Creates a new character dictionary with base stats determined by class (Warrior, Mage, Rogue, Cleric). |
| save_character: Writes character data to {character_name}_save.txt in data/save_games. List fields are saved as comma-separated strings. |
| load_character: Reads character data from a save file, parsing comma-separated strings back into Python lists. Includes comprehensive error handling for corrupted files. |
| list_saved_characters:  Returns a list of character names in the save directory. |
| delete_character: Removes a character's save file. |

### Operations & Growth
* **gain_experience(character, xp_amount)**: Adds XP, handles level-up (level +1, max\_health +15, strength +4, magic +3).
* **add_gold(character, amount)**: Updates gold total, raises ValueError if the result is negative.
* **heal_character(character, amount)**: Restores HP, capped at max_health.
* **revive_character(character)**: Restores health to 50% of max_health.

---

# 3. Inventory System Module

*This module handles inventory management, item usage, and equipment.*

### Inventory Core
* ** MAX_INVENTORY_SIZE **: Set to **20**.
* ** add_item_to_inventory **: Raises InventoryFullError if capacity is reached.
* ** remove_item_from_inventory **: Removes an item instance.
* ** count_item / get_inventory_space_remaining / clear_inventory **: Utility functions for tracking inventory contents.

### Item Usage and Equipment

| Function | Item Type Handled | Logic |
| :--- | :--- | :--- |
| use_item | consumable | Applies effect (e.g., health:20), then removes the item from inventory. |
| equip_weapon / equip_armor | weapon / armor | If an item is already equipped, its bonus is removed, and the old item is returned to inventory before the new item's bonus is applied and stored. |
| unequip_weapon / unequip_armor | N/A | Removes the stat bonus, returns the item to inventory, and clears the equipped slot. Raises InventoryFullError if the inventory cannot accept the item. |

---

# 4. Quest Handler Module

*This module handles quest management, dependencies, and completion.*

### Quest Lifecycle

| Function | Requirements/Result |
| :--- | :--- |
| accept_quest | Requires: Character **level** $\ge$ required\_level, **prerequisite** completed, quest not already active/completed. |
| complete_quest | Requires: Quest must be in active_quests. Removes from active, adds to completed, and grants reward_xp and reward_gold. |
| abandon_quest | Removes a quest from active_quests without rewards. |

### Retrieval & Statistics
* get_active_quests / get_completed_quests / get_available_quests: Functions to filter and retrieve full quest data dictionaries.
* get_quest_prerequisite_chain: Traces a quest's prerequisites backward to determine the entire dependency path.
* get_quest_completion_percentage: Calculates the percentage of all quests completed.

---

# 5. Combat System Module

*Handles combat mechanics via the SimpleBattle class.*

### Enemy Definitions (via `create_enemy`)
* **goblin**: health=50, strength=8, magic=2, xp\_reward=25, gold\_reward=10
* **orc**: health=80, strength=12, magic=5, xp\_reward=50, gold\_reward=25
* **dragon**: health=200, strength=25, magic=15, xp\_reward=200, gold\_reward=100

### `SimpleBattle` Class
* **Damage Formula**: attacker['strength'] - (defender['strength'] // 4).
* ** attempt_escape **: $50\%$ success chance.
* **use_special_ability**: Executes a class-specific action:
    * **Warrior**: Power Strike ($2 \times$ strength damage).
    * **Mage**: Fireball ($2 \times$ magic damage).
    * **Rogue**: Critical Strike ($3 \times$ strength damage, $50\%$ chance).
    * **Cleric**: Heal (restore 30 health).

---

# 6. Main Game Module

*This is the main game file that ties all modules together.*

### Game State
* Global variables: current_character, all_quests, all_items, game_running.

### Menu Functions
* main_menu(): Presents New Game, Load Game, and Exit options.
* new_game(): Prompts for name/class and uses character_manager.create_character.
* load_game(): Lists saved characters and loads selected file using character_manager.load_character.
