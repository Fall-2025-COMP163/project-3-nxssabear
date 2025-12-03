"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Vanessa Gray

AI Usage: AI was used to help generate the initial structure and functions of this module.

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # quest acceptance
    if quest_id not in quest_data_dict: # Check quest exists
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    if character['level'] < quest_data_dict[quest_id]['required_level']: # Check level req
        raise InsufficientLevelError(f"Character level too low to accept quest '{quest_id}'.")
    
    if quest_data_dict[quest_id]['prerequisite'] != "NONE": # Check prerequisite
        prereq = quest_data_dict[quest_id]['prerequisite'] # Get prerequisite quest ID
        if prereq not in character['completed_quests']: # Verify completed
            raise QuestRequirementsNotMetError(f"Prerequisite quest '{prereq}' not completed for quest '{quest_id}'.")
    
    if quest_id in character['completed_quests']: # Check already completed
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' has already been completed.")
    
    if quest_id not in character['active_quests']: # Check not already active
        character['active_quests'].append(quest_id)
        return True
    
def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # quest completion
   
    if quest_id not in quest_data_dict: # Check quest exists
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    if quest_id not in character['active_quests']: # Check quest is active
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")
    
    character['active_quests'].remove(quest_id) # Remove from active quests
    character['completed_quests'].append(quest_id) # Add to completed quests

    reward_xp = quest_data_dict[quest_id]['reward_xp'] # Get reward XP
    reward_gold = quest_data_dict[quest_id]['reward_gold'] # Get reward gold

    character['experience'] += reward_xp
    character['gold'] += reward_gold

    return{'reward_xp': reward_xp, 'reward_gold': reward_gold}

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # quest abandonment
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")
    
    character['active_quests'].remove(quest_id)
    return True

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # active quest retrieval

    active_quests = []
    for quest_id in character['active_quests']: # Iterate active quests
        if quest_id in quest_data_dict:
            active_quests.append(quest_data_dict[quest_id])

    return active_quests
    
def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # completed quest retrieval
    completed_quests = []
 
    for quest_id in character['completed_quests']: # Iterate completed quests
        if quest_id in quest_data_dict:
            completed_quests.append(quest_data_dict[quest_id])

    return completed_quests

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # available quest search

    available = []

    for quest_id, quest_data in quest_data_dict.items(): # Iterate all quests
        if character['level'] >= quest_data['required_level']: # Check level req
            continue

        prereq = quest_data['prerequisite'] # Get prerequisite quest ID
        if prereq != "NONE" and prereq in character['completed_quests']: # Check prerequisite
            continue
        
        if quest_id not in character['completed_quests']: # Check not completed
            continue
        if quest_id not in character['active_quests']: # Check not active
            continue 
        
        available.append(quest_data)
    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # completion check
    if quest_id in character['completed_quests']:
        return True

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # active check
    if quest_id in character['active_quests']:
        return True

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # requirement checking
    # Check all requirements without raising exceptions
    
    if quest_id not in quest_data_dict: # Quest must exist
        return False 
    quest = quest_data_dict[quest_id] # Get quest data
    if character['level'] < quest['required_level']:
        return False

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order

    if quest_id not in quest_data_dict: # Check quest exists
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    chain = [] # Initialize chain list
    current_quest_id = quest_id # Start with given quest ID

    while True: # Loop until no more prerequisites
        if current_quest_id not in quest_data_dict:
            raise QuestNotFoundError(f"Quest '{current_quest_id}' not found ")
        chain.append(current_quest_id) # Add current quest to chain
        prerequisite = quest_data_dict[current_quest_id]['prerequisite']
        if prerequisite == "NONE": # No more prerequisites
            break

        current_quest_id = prerequisite # Move to prerequisite quest ID

    chain.reverse() # Reverse to get correct order
    return chain
            
# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # percentage calculation

    total_quests = len(quest_data_dict) # Total number of quests

    if total_quests == 0: # Avoid division by zero
        return 0.0
    
    completed_quests = len(character['completed_quests']) # Number completed
    percentage = (completed_quests / total_quests) * 100    
    return percentage
    
def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # reward calculation
    # Sum up reward_xp and reward_gold for all completed quests

    total_xp = 0
    total_gold = 0

    for quest_id in character['completed_quests']: # Iterate completed quests
        if quest_id in quest_data_dict: # Check quest exists
            total_xp += quest_data_dict[quest_id]['reward_xp']
            total_gold += quest_data_dict[quest_id]['reward_gold']

    return {'total_xp': total_xp, 'total_gold': total_gold}
    

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # level filtering
    
    filtered = [] # Initialize filtered list

    for quest_id, quest_data in quest_data_dict.items(): # Iterate all quests

        level = quest_data['required_level'] # Get quest level requirement
        if min_level <= level <= max_level: # Check if within range
            filtered.append(quest_data)

    return filtered

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Required Level: {quest_data['required_level']}")
    print(f"Rewards: {quest_data['reward_xp']} XP, {quest_data['reward_gold']} Gold")
    print(f"Prerequisite: {quest_data['prerequisite']}")
    

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # quest list display
    if not quest_list:
        print("No quests to display.")
        return
    
    print("\n=== Quest List ===")
    for quest in quest_list:
        print(f"- {quest['title']} (Level {quest['required_level']})")
        print(f"Rewards: {quest['reward_xp']} XP, {quest['reward_gold']} Gold")
        print()

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # progress display
    active_count = len(character['active_quests']) # Active quests count
    completed_count = len(character['completed_quests']) # Completed quests count
    completion_percentage = get_quest_completion_percentage(character, quest_data_dict) # Completion percentage
    total_rewards = get_total_quest_rewards_earned(character, quest_data_dict) # Total rewards earned

    print("\n=== Quest Progress ===")
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion Percentage: {completion_percentage:.2f}%")
    print(f"Total Rewards Earned: {total_rewards['total_xp']}")
    print(f"Total Gold Earned: {total_rewards['total_gold']}")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict
    
    for quest_id, quest_data in quest_data_dict.items(): # Iterate all quests
        prerequisite = quest_data['prerequisite'] # Get prerequisite
 
        if prerequisite != "NONE" and prerequisite not in quest_data_dict: # Check validity
            raise QuestNotFoundError(f"Quest '{quest_id}' has invalid prerequisite '{prerequisite}'.")
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

