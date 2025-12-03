"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Vanessa Gray

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    inventory = character['inventory']

# Check inventory capacity
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")
    
    # Add item to inventory
    inventory.append(item_id)
    return True
    
def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # Check if item exists in inventory
    if item_id not in character['inventory']: 
        raise ItemNotFoundError("Item not found in inventory.")
    character['inventory'].remove(item_id) # Remove item
    return True
    
def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    if item_id in character['inventory']: # Check presence
        return True
    else:
        return False

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    #item counting
    # Use list.count() method
    return character['inventory'].count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    #space calculation
    inventory = character['inventory']
    
    reamining = MAX_INVENTORY_SIZE - len(inventory) # Calculate remaining space

    return reamining

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list

    removed_items = character['inventory'][:]
    character['inventory'] = []

    return removed_items
# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # item usage
    
    inventory = character['inventory']

    if item_id not in inventory: # Check item exists
        raise ItemNotFoundError("Item not found in inventory.")
    
    if item_data['type'] != 'consumable': # Check item type
        raise InvalidItemTypeError("Item is not consumable.")
    
    stat_name, value = parse_item_effect(item_data['effect']) # Parse effect
    apply_stat_effect(character, stat_name, value) # Apply effect
    remove_item_from_inventory(character, item_id) # Remove item

    return f"Used {item_id}, {stat_name} increased by {value}."

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # weapon equipping

    inventory = character['inventory']

    if item_id not in inventory: # Check item exists
        raise ItemNotFoundError("Item not found in inventory.")
    
    if item_data['type'] != 'weapon': # Check item type
        raise InvalidItemTypeError("Item is not a weapon.")
    
    # Unequip current weapon if exists
    if 'equipped_weapon' in character and character['equipped_weapon'] is not None:
        current_weapon_id = character['equipped_weapon']
       
        # Unequip current weapon
        current_weapon_data = character['game_data']['items'][current_weapon_id]
        current_weapon_effect = item_data['effect']  # This should ideally fetch the effect of the currently equipped weapon
        
        # Remove current weapon effect
        stat_name, value = parse_item_effect(current_weapon_effect)
        apply_stat_effect(character, stat_name, -value)  # Remove bonus
        add_item_to_inventory(character, current_weapon_id)  # Add back to inventory

    stat_name, value = parse_item_effect(item_data['effect']) # Parse new weapon effect
    apply_stat_effect(character, stat_name, value)  # Apply new weapon bonus

    character['equipped_weapon'] = item_id # Set new weapon
    character["equippe_weapon_effect"] = item_data['effect'] # Store effect

    remove_item_from_inventory(character, item_id) # Remove from inventory

    return f"Equipped {item_id}, {stat_name} increased by {value}."

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # armor equipping
    # Similar to equip_weapon but for armor
    inventory = character['inventory']

    if item_id not in inventory: # Check item exists
        raise ItemNotFoundError("Item not found in inventory.")
    
    if item_data['type'] != 'armor': # Check item type
        raise InvalidItemTypeError("Item is not armor.")
    
    if 'equipped_armor' in character and character['equipped_armor'] is not None:
        current_armor_id = character['equipped_armor'] # Get current armor ID

        current_armor_data = character['game_data']['items'][current_armor_id] # Fetch current armor data
        current_armor_effect = item_data['effect']  # This should ideally fetch the effect of the currently equipped armor
        
        stat_name, value = parse_item_effect(current_armor_effect) # Parse current armor effect
        apply_stat_effect(character, stat_name, -value)  # Remove bonus
        add_item_to_inventory(character, current_armor_id)  # Add back to inventory

    stat_name, value = parse_item_effect(item_data['effect']) # Parse new armor effect
    apply_stat_effect(character, stat_name, value)  # Apply new armor bonus

    character['equipped_armor'] = item_id # Set new armor
    character["equippe_armor_effect"] = item_data['effect'] # Store effect

    remove_item_from_inventory(character, item_id)

    return f"Equipped {item_data['name']}, {stat_name} increased by {value}."

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # weapon unequipping
    if "equipped_weapon" not in character or character['equipped_weapon'] is None:
        return None
    
    weapon_id = character["equipped_weapon"] # Get equipped weapon ID
    
    if len(character['inventory']) >= MAX_INVENTORY_SIZE: # Check inventory space
        raise InventoryFullError("Inventory is full.")
    
    effect = character["equippe_weapon_effect"]  # Get weapon effect

    stat_name,value = parse_item_effect(effect) # Parse effect

    apply_stat_effect(character, stat_name, -value)  # Remove bonus

    character['inventory'].append(weapon_id)


    character['equipped_weapon'] = None
    character["equippe_weapon_effect"] = None

    return weapon_id

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # armor unequipping
    inventory = character['inventory']

    if "equipped_armor" not in character or character['equipped_armor'] is None: # Check equipped armor
        return None
    
    armor_id = character["equipped_armor"] # Get equipped armor ID

    if len(inventory) >= MAX_INVENTORY_SIZE: # Check inventory space
        raise InventoryFullError("Inventory is full.")
    
    effect = character["equipped_armor_effect"]  # Get armor effect
 
    stat_name,value = parse_item_effect(effect) # Parse effect
    apply_stat_effect(character, stat_name, -value)  # Remove bonus

    inventory.append(armor_id) # Add armor back to inventory
    character['equipped_armor'] = None
    character["equipped_armor_effect"] = None

    return armor_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # purchasing

    cost = item_data['cost'] # Get item cost
    inventory = character['inventory'] # Get inventory

    if character['gold'] < cost: # Check gold
        raise InsufficientResourcesError("Not enough gold to purchase item.")
    
    if len(inventory) >= MAX_INVENTORY_SIZE: # Check inventory space
        raise InventoryFullError("Inventory is full.")
    
    character['gold'] -= cost # Deduct gold
    inventory.append(item_id)

    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # selling
    
    inventory = character['inventory']

    if item_id not in character['inventory']: # Check item exists
        raise ItemNotFoundError("Item not found in inventory.") 
    
    sell_price = item_data['cost'] // 2 # Calculate sell price
    inventory.remove(item_id)

    character['gold'] += sell_price # Add gold to character

    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # effect parsing
    
    if ":" not in effect_string: # Validate format
        raise ValueError("Invalid effect string format.")
    
    stat_name, value_str = effect_string.split(":", 1) # Split into stat and value

    try:
        value = int(value_str) # Convert value to integer
    except ValueError:
        raise ValueError("Effect value must be an integer.")
    
    return stat_name, value

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # stat application
    
    character[stat_name] += value

    if stat_name == 'health': # Ensure health does not exceed max_health
        if character['health'] > character['max_health']:
            character['health'] = character['max_health']

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # inventory display

    inventory = character['inventory']

    print("\n=== Inventory ===")

    if len(inventory) == 0: # Check if empty
        print("Inventory is empty.")
        return
    
    item_counts = {} # Count items
    for item_id in inventory: # Tally items
        if item_id in item_counts:
            item_counts[item_id] += 1
        else:
            item_counts[item_id] = 1
    
    for item_id, count in item_counts.items(): # Display each item
        item_name = item_data_dict[item_id]['name'] # Get item name
        item_type = item_data_dict[item_id]['type'] # Get item type
        print(f"{item_name} (Type: {item_type}) x{count}")
    
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

