"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Vanessa Gray

AI Usage: AI assisted in writing load and parse functions as well and debugging this code.

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        raise MissingDataFileError(f"Quest data file '{filename}' not found.")
    except Exception:
        raise CorruptedDataError(f"Quest data file '{filename}' is corrupted or unreadable.")
    
    if content == "":
        raise InvalidDataFormatError("Quest file is empty.")
    
    blocks = [b.strip() for b in content.split("\n\n") if b.strip() != ""]
    
    quests = {}

    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip() != ""]
        quest_dict = parse_quest_block(lines)
        validate_quest_data(quest_dict)

        if "quest_id" not in quest_dict:
            # Raise the format error if the key is completely missing
            raise InvalidDataFormatError("Missing quest_id field.")

        # Retrieve the ID directly now that we know it exists
        quest_id = quest_dict["quest_id"]
        
        # Check if the retrieved ID is empty (e.g., if saved as quest_id: )
        if not quest_id:
            raise InvalidDataFormatError("Missing quest_id field.")

        quests[quest_id] = quest_dict

    return quests

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        raise MissingDataFileError(f"Item data file '{filename}' not found.")
    except Exception:
        raise CorruptedDataError(f"Item data file '{filename}' is corrupted or unreadable.")
    
    items = {}
    curent_block = []

    for line in content.splitlines():
        line = line.strip()

        if line == "":
            
            if curent_block:
                item_data = parse_item_block(curent_block)
                validate_item_data(item_data)
                
                if "item_id" not in item_data:
                    raise InvalidDataFormatError("Missing item_id field.")
                
                # Retrieve the value directly, now that its existence is confirmed
                item_id = item_data["item_id"] 

                # Check if the retrieved ID is empty (e.g., if saved as item_id: )
                if not item_id:
                    raise InvalidDataFormatError("Missing item_id field.")
                    
                items[item_id] = item_data
                curent_block = []
        else:
            curent_block.append(line)
   
    if curent_block:
        
        item_data = parse_item_block(curent_block)
        validate_item_data(item_data)

        if "item_id" not in item_data:
            raise InvalidDataFormatError("Missing item_id field.")
        
        # Retrieve the value directly, now that its existence is confirmed
        item_id = item_data["item_id"]

        # Check if the retrieved ID is empty
        if not item_id:
            raise InvalidDataFormatError("Missing item_id field.")
            
        items[item_id] = item_data

    return items
    

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    required_fields = [
        "quest_id", "title", "description", "reward_xp", "reward_gold", "required_level", "prerequisite"
    ]

    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")
        
    if not isinstance(quest_dict["reward_xp"], int):
        raise InvalidDataFormatError("reward_xp must be an integer")
    
    if not isinstance(quest_dict["reward_gold"], int):
        raise InvalidDataFormatError("reward_gold must be an integer")
    
    if not isinstance(quest_dict["required_level"], int):
        raise InvalidDataFormatError("required_level must be an integer")
    
    return True
    

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    required_fields = [
        "item_id", "name", "type", "effect", "cost", "description"
    ]

    valid_types = ["weapon", "armor", "consumable"]

    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")
        
    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
    
    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("cost must be an integer")
    
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists("data/quests.txt"):
        with open("data/quests.txt", "w") as f:
            f.write(
                "QUEST_ID: first_quest\n"
                "TITLE: The Beginning\n"
                "DESCRIPTION: Your journey starts here.\n"
                "REWARD_XP: 100\n"
                "REWARD_GOLD: 50\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n"
            )
    if not os.path.exists("data/items.txt"):
        with open("data/items.txt", "w") as f:
            f.write(
                "ITEM_ID: health_potion\n"
                "NAME: Health Potion\n"
                "TYPE: consumable\n"
                "EFFECT: health:20\n"
                "COST: 10\n"
                "DESCRIPTION: Restores 20 health points.\n"
            )

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    quest_info = {}

    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Invalid line format: {line}")
        
        key, value = line.split(": ", 1)
        key = key.strip().lower()
        value = value.strip()

        if key in ["reward_xp", "reward_gold", "required_level"]:
            try:
                value = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"{key} must be an integer.")
        
        quest_info[key] = value

    return quest_info

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic

    item_info = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Invalid line format: {line}")
        
        key, value = line.split(": ", 1)
        key = key.strip().lower()
        value = value.strip()

        if key == "cost":
            try:
                value = int(value)
            except ValueError:
                raise InvalidDataFormatError("cost must be an integer.")
        
        item_info[key] = value
    return item_info

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

