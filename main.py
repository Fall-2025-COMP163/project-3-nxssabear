"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Vanessa Gray

AI Usage: AI was used to help generate the initial structure and functions of this module.

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice

    print("\n=== Main Menu ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    answer = input("Enter your choice (1-3): ").strip()
    if answer in ['1', '2', '3']:
        return int(answer)
    
    print("Invalid choice. Please select 1, 2, or 3.")
    return main_menu()
    
def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    print("\n=== New Game ===")

    name = input("Enter your character's name: ").strip()
    print("Choose your class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    print("4. Cleric")
    class_choice = input("Enter your choice (1-4): ").strip()

    class_map = {
        '1': 'Warrior',
        '2': 'Mage',
        '3': 'Rogue',
        '4': 'Cleric'
    }
 
    if class_choice not in class_map: 
        print("Invalid class choice. Please try again.")
        return new_game()   
    char_class = class_map[class_choice] 

    try: 
        current_character = character_manager.create_character(name, char_class) 
        print(f"Character '{name}' the {char_class} created successfully!")
    except InvalidCharacterClassError:
        print("Error: Invalid character class selected.")
        return 

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop

    print("\n=== Load Game ===")

    saved_characters = character_manager.list_saved_characters() 
    if not saved_characters:
        print("No saved characters found. Please start a new game.")
        return
    
    print("Saved Characters:")
    for i, char_name in enumerate(saved_characters, start=1):
        print(f"{i}. {char_name}") 
    
    answer = input("Enter the number of the character to load: ").strip()

    if not answer.isdigit():
        print("Invalid input. Please enter a number.")
        return 
    
    choice = int(answer)

    if choice < 1 or choice > len(saved_characters):
        print("Invalid choice. Please try again.")
        return
    
    char_name = saved_characters[choice - 1]

    try:
        current_character = character_manager.load_character(char_name)
        print(f"Character '{char_name}' loaded successfully!")
    except CharacterNotFoundError:
        print("Error: Character not found.")
        return
    except SaveFileCorruptedError:
        print("Error: Save file is corrupted.")
        return  
    except InvalidSaveDataError:
        print("Error: Save data is invalid.")
        return
    
    # Start game loop
    game_loop()
    

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    #  game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    while game_running:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Exiting to main menu.")
            game_running = False
        else:
            print("Invalid choice. Please select a valid option.")
    
def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # game menu
    print("\n=== Game Menu ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")

    answer = input("Enter your choice (1-6): ").strip()
    while answer not in ['1', '2', '3', '4', '5', '6']:
        print("Invalid choice. Please select a number between 1 and 6.")
        answer = input("Enter your choice (1-6): ").strip()

    return int(answer)
# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler

    character = current_character

    print("\n=== Character Stats ===")
    print(f"Name: {character['name']}")
    print(f"Class: {character['class']}")
    print(f"Level: {character['level']}")
    print(f"Health: {character['health']}/{character['max_health']}")
    print(f"Strength: {character['strength']}")
    print(f"Experience: {character['xp']}")
    print(f"Gold: {character['gold']}")
    print(f"Magic: {character['magic']}")
    print(f"Active Quests: {len(character['active_quests'])}")
    print(f"Completed Quests: {len(character['completed_quests'])}")

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system 
    inventory_system.display_inventory(current_character, all_items) 
    answer = input("Enter the item name to use/equip/drop or 'back' to return: ").strip()
    if answer.lower() == 'back':
        return

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler

    print("\n=== Quest Menu ===")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest (for testing)")
    print("7. Back")    

    answer = int(input("Enter your choice (1-7): ")).strip()

    if answer == 7:
        return

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions

    print("You venture forth into the unknown...")

    enemy = combat_system.get_random_enemy_for_level(current_character['level'])
    print(f"A crazy {enemy['name']} appears!")

    fight = combat_system.SimpleBattle(current_character, enemy)

    try:
        result = fight.start_battle()
    except CharacterDeadError:
            handle_character_death()
            return
    
    print("\n=== Battle Result ===")

    if result['victory'] == "player":
        print("You have defeated the enemy!")
        print(f"XP Gained: {result['xp_gained']}")
        print(f"Gold Gained: {result['gold_gained']}")

    elif result['victory'] == "enemy":
        print("You have been defeated...")
        handle_character_death()    
        return
    else:
        print("The battle has ended without a victor.")

    input("Press Enter to continue...")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    while True:
        print("\n=== Shop Menu ===")
        print(f"Current Gold: {current_character['gold']}")
        print("Available Items:")

        for item_name, item_info in all_items.items():
            print(f"- {item_name}: {item_info['cost']} gold")

        print("1. Buy Items")
        print("2. Sell Items")
        print("3. Back to Game Menu")
        
        answer = input("Enter your choice (1-3): ").strip()
        
        if answer == '1':
            item_id = input("Enter the name of the item to buy: ").strip()

            if item_id not in all_items:
                print("Item does not exist in shop.")
                continue

            item_data = all_items[item_id]

            try:
                inventory_system.purchase_item(current_character, item_id, item_data)
                print(f"Purchased {item_data['name']}!")
            except InsufficientResourcesError:
                print("You do not have enough gold.")
            except InventoryFullError:
                print("Your inventory is full.")

            input("\nPress ENTER to continue...")
            continue

        elif answer == '2':
            item_id = input("Enter the name of the item to sell: ").strip()

            if item_id not in all_items:
                print("Item does not exist in shop.")
                continue

            item_data = all_items[item_id]
            try:
                gold = inventory_system.sell_item(current_character, item_id, item_data)
                print(f"Sold {item_data['name']} for {gold} gold!")
                
            except ItemNotFoundError:
                print("You do not have that item in your inventory.")

        elif answer == '3':
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

    #  shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    #  save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    if current_character is None:
        print("No character to save.")
        return
    
    try: 
        character_manager.save_character(current_character)
        print(f"Character '{current_character['name']}' saved successfully!")
    except PermissionError:
        print("Error: Permission denied while saving the character.")
    except IOError: 
        print("Error: An I/O error occurred while saving the character.")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    try:
        all_quests = game_data.load_quests() 
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Data files missing. Creating default data files...")
        game_data.create_default_data_files()

        all_quests = game_data.load_quests()
        all_items = game_data.load_items()

    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        raise

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    print("\n=== You Have Died ===")
    print("1. Revive (Costs 50 gold)")
    print("2. Quit to Main Menu")

    while True:
        choice = input("Enter your choice (1-2): ").strip()

        if choice == '1':
            if current_character['gold'] < 50:
                print("You do not have enough gold to revive.")
                game_running = False
                return

            current_character['gold'] -= 50

            try:
                character_manager.revive_character(current_character, cost=50)
                print("You have been revived!")
                return
            except InsufficientResourcesError:
                print("You do not have enough gold to revive.")


        elif choice == '2':
            print("Exiting to main menu...")
            game_running = False
            return
        else:
            print("Invalid choice. Please select 1 or 2.")

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

