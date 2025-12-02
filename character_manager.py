"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Vanessa Gray

AI Usage: AI assisted in load character function validation in addition to debugging.

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")
    
    # Set base stats based on class
    if character_class == "Warrior":
        health = 120
        strength = 15
        magic = 5
    elif character_class == "Mage":
        health = 80
        strength = 8
        magic = 20
    elif character_class == "Rogue":
        health = 90
        strength = 12
        magic = 10
    elif character_class == "Cleric":
        health = 100
        strength = 10
        magic = 15

    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": health,
        "max_health": health,
        "strength": strength,
        "magic": magic,
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

    return character

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filename, "w") as f:
            f.write(f"NAME: {character['name']}\n")
            f.write(f"CLASS: {character['class']}\n")
            f.write(f"LEVEL: {character['level']}\n")
            f.write(f"HEALTH: {character['health']}\n")
            f.write(f"MAX_HEALTH: {character['max_health']}\n")
            f.write(f"STRENGTH: {character['strength']}\n")
            f.write(f"MAGIC: {character['magic']}\n")
            f.write(f"EXPERIENCE: {character['experience']}\n")
            f.write(f"GOLD: {character['gold']}\n")
            f.write(f"INVENTORY: {','.join(character['inventory'])}\n")
            f.write(f"ACTIVE_QUESTS: {','.join(character['active_quests'])}\n")
            f.write(f"COMPLETED_QUESTS: {','.join(character['completed_quests'])}\n")
        return True
    

    except (PermissionError, IOError) as e:
        print(f"Error saving character: {e}")
        return False 

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"Character '{character_name}' not found.")
    
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except:
        raise SaveFileCorruptedError(f"Could not read save file for '{character_name}'.")
   
    character = {}

    for line in lines:
        if line.strip() == "":
            continue
        if ": " not in line:
            raise InvalidSaveDataError(f"Invalid line format: {line.strip()}")
        
        key, value = line.strip().split(": ", 1)
        key = key.lower()   
        value = value.strip()

        if key in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
            try:
                value = int(value)
            except ValueError:
                raise InvalidSaveDataError(f"{key} must be an integer.")
        elif key in ["inventory", "active_quests", "completed_quests"]:
            if value == "":
                value = []
            else:
                value = value.split(",")    

        character[key] = value
    # Validate loaded character data
    validate_character_data(character)
    
    return character

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    if not os.path.exists(save_directory):
        return []
    
    files = os.listdir(save_directory)
    character_names = []

    for file in files:
        if file.endswith("_save.txt"):
            name = file[:-9]  # Remove "_save.txt"
            character_names.append(name)
    return character_names

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"Character '{character_name}' not found.")
    
    try:
        os.remove(filename)
    except:
        raise SaveFileCorruptedError(f"Could not delete save file for '{character_name}'.")
    
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    if character['health'] <= 0:
        raise CharacterDeadError("Cannot gain experience: character is dead.")
    
    level_up_xp = character['level'] * 100
    character['experience'] += xp_amount

    while character['experience'] >= level_up_xp:
        character['experience'] -= level_up_xp
        character['level'] += 1
        character['max_health'] += 15
        character['strength'] += 4
        character['magic'] += 3
        character['health'] = character['max_health']
        level_up_xp = character['level'] * 100

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    new_gold = character['gold'] + amount
    if new_gold < 0:
        raise ValueError("Not enough gold.")
    character['gold'] = new_gold
    return character['gold']


def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    before_heal = character['health'] + amount
    if before_heal > character['max_health']:
        current_healed = character['max_health'] - character['health']
        character['health'] = character['max_health']
    else:
        current_healed = amount
        character['health'] += amount
    return current_healed

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    if character['health'] <= 0:
        return True
    else:
        return False

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # Restore health to half of max_health
    if character['health'] <= 0:
        character['health'] = character['max_health'] // 2
        return True
# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    required_fields = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests" 
    ]

    for field in required_fields:
        if field not in character:
            raise InvalidSaveDataError(f"Missing required field: {field}")
        
    numeric_fields = [
        "level", "health", "max_health", "strength",
        "magic", "experience", "gold"       
    ]
    for field in numeric_fields:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f"{field} must be an integer.")
        
    list_fields = [
        "inventory", "active_quests", "completed_quests"
    ]
    for field in list_fields:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(f"{field} must be a list.")
    return True
    
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

