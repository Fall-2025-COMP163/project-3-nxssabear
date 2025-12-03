"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Vanessa Gray

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    
    enemy = {

        "goblin": {
            "name": "Goblin",  
            "health": 50,
            "max_health": 50,
            "strength": 8,
            "magic": 2,
            "xp_reward": 25,
            "gold_reward": 10
        },
        "orc": {
            "name": "Orc",
            "health": 80,
            "max_health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25
        },
        "dragon": {
            "name": "Dragon",
            "health": 200,
            "max_health": 200,
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100
        }
    }

    if enemy_type not in enemy:
        raise InvalidTargetError(f"Enemy type '{enemy_type}' is not recognized.")
    
    standard = enemy[enemy_type]

    norm = {
        "name": standard["name"],
        "health": standard["health"],
        "max_health": standard["max_health"],
        "strength": standard["strength"],
        "magic": standard["magic"],
        "xp_reward": standard["xp_reward"],
        "gold_reward": standard["gold_reward"]
    }
    return norm

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type

    if character_level <= 2:
        return create_enemy("goblin")
    elif 3 <= character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_counter = 0
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        if self.character['health'] <= 0:
            raise CharacterDeadError("Character is already dead and cannot fight.") 
        else:
            print("Battle started between " + self.character['name'] + " and " + self.enemy['name'] + "!")

        while self.combat_active:

            self.player_turn()
            result = self.check_battle_end()

            if not self.combat_active:
                break
            if result:
                break

            self.enemy_turn()
            result = self.check_battle_end()
            if result:
                break

            self.turn_counter += 1

        if result == 'player':
            rewards = get_victory_rewards(self.enemy)

            self.character['xp'] += rewards['xp']
            self.character['gold'] += rewards['gold']

            return {
                'winner': 'player',
                'xp_gained': rewards['xp'],
                'gold_gained': rewards['gold']
            }
        elif result == 'enemy':
            return {
                'winner': 'enemy',
                'xp_gained': 0,
                'gold_gained': 0
            }
        else:
            return {
                'winner': 'none',
                'xp_gained': 0,
                'gold_gained': 0
            }
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take player turn when combat is not active.")
        
        else:
            print(f"\n{self.character['name']}'s turn!")
            print("Choose an action:")
            print("1. Basic Attack")
            print("2. Special Ability")
            print("3. Try to Run")

            choice = input("Enter the number of your choice: ")

            if choice == '1':
                damage = self.calculate_damage(self.character, self.enemy)
                self.apply_damage(self.enemy, damage)
                display_battle_log(f"{self.character['name']} attacks {self.enemy['name']} for {damage} damage!")
            elif choice == '2':
               use_special_ability(self.character, self.enemy)
               print(f"{self.character['name']} used their special ability!")

            elif choice == '3':
                escaped = self.attempt_escape()
                if escaped:
                    display_battle_log(f"{self.character['name']} successfully escaped the battle!")
                else:
                    display_battle_log(f"{self.character['name']} failed to escape!")
            else:
                print("Invalid choice. Please select a valid action.")
                self.player_turn()  # Retry turn
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take enemy turn when combat is not active.")
        
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} attacks {self.character['name']} for {damage} damage!")

        if self.character['health'] <= 0:
            self.character['health'] = 0
            self.combat_active = False  
            display_battle_log(f"{self.character['name']} has been defeated!")
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        damage = attacker['strength'] - (defender['strength'] // 4)

        if damage < 1:
            damage = 1  
        
        return damage
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        if target['health'] - damage < 0:
            target['health'] = 0
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if self.enemy['health'] <= 0:
            self.combat_active = False
            return 'player'
        
        if self.character['health'] <= 0:
            self.combat_active = False
            return 'enemy'
        
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        import random

        possibility = random.randint(0, 1)

        if possibility == 1:
            self.combat_active = False
            return True
        
        return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    char_class = character['class']

    if char_class == "Warrior":
        return warrior_power_strike(character, enemy)
    elif char_class == "Mage":
        return mage_fireball(character, enemy)
    elif char_class == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif char_class == "Cleric":
        return cleric_heal(character)
    else:
       raise InvalidTargetError(f"Unknown character class '{char_class}' for special ability.")

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    damage = max(1,character["strength"]*2)
    enemy["health"] -= damage
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"Warrior used Power Strike dealing {damage} damage to {enemy['name']}"
def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    damage = max(1,character["magic"]*2)
    enemy["health"] -= damage
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"Mage used Fireball dealing {damage} damage to {enemy['name']}"

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    import random

    base = character["strength"] - (enemy["strength"] // 4)
    if base < 1:
        base = 1

    critical = random.randint(0, 1)

    if critical == 1:
        fin_damage = base * 3
        crit_msg = "It's a critical hit! "
    else:
        fin_damage = base
        crit_msg = "You missed the critical hit."

    enemy["health"] -= fin_damage
    if enemy["health"] < 0:
        enemy["health"] = 0

    return f"Rogue used Critical Strike dealing {fin_damage} damage to {enemy['name']}. {crit_msg}"

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    heal_amount = 30

    max_health = character["max_health"]
    current_health = character["health"]

    new_health = current_health + heal_amount

    if new_health > max_health:
        new_health = max_health

    real_heal = new_health - current_health

    character["health"] = new_health

    return f"Cleric healed for {real_heal} health points."
# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    return character['health'] > 0

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    return {
        'xp': enemy['xp_reward'],
        'gold': enemy['gold_reward']
    }

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print("\n=== Combat Status ===")
    
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

