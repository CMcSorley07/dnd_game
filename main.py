from src.ai_interface import AIInterface
from src.dice import DiceRoller
from src.character import Character
from src.game_state import GameState
from src.combat import CombatSystem
from src.game_loop import GameLoop

def test_game_loop():
    """Test the main game loop"""
    print("Testing the game loop...")
    print("This will start the actual D&D game!")
    print("Type 'quit' during character creation to exit the test")

    try:
        game = GameLoop()
        game.start_new_game()
    except KeyboardInterrupt:
        print("\nGame loop test interupted by user")
    except Exception as e: 
        print(f"Game loop test error: {e}")

def test_combat_system():
    """Test the combat system"""
    print("Testing the combat system...")

    # Create a test character
    hero = Character("Test Fighter")
    hero.alignment = "Lawful Good"
    hero.character_class = "Fighter"
    hero.background = "Soldier"
    hero.roll_abilities()
    hero.set_race("Human") 
    hero.calculate_hp()
    hero.add_skill_proficiency('athletics')

    # Create a simple enemy (as a dictionary)
    goblin = {
        'name': 'Goblin',
        'armor_class': 15,
        'hit_points': 7,
        'dex_modifier': 2
    }

    combat = CombatSystem()

    # Test initiative

    characters = [
        {'name': hero.name, 'dex_modifier': hero.get_ability_modifier('dexterity')},
        goblin
    ]

    print("rolling initiative...")
    initiative_order = combat.roll_initiative(characters)

    for character in initiative_order:
        print(f"{character['name']}: {character['initiative']}")

    # Test attack roll
    print(f"\n{hero.name} attacks the Goblin!")
    attack_result = combat.make_attack_roll(hero, goblin)
    
    print(f"Attack roll: {attack_result['attack_roll']} + {attack_result['ability_modifier']} + {attack_result['proficiency_bonus']} = {attack_result['total']}")
    print(f"Target AC: {attack_result['target_ac']}")
    print(f"Hit: {'Yes' if attack_result['hit'] else 'No'}")
    
    if attack_result['hit']:
        # Test damage roll
        damage_result = combat.roll_damage("1d8", hero.get_ability_modifier('strength'))
        print(f"Damage: {damage_result['damage_roll']} + {damage_result['ability_modifier']} = {damage_result['total_damage']}")

def test_game_state():
    """Test game state save/load functionality"""
    print("Testing game state save/load...")

    # Create a character
    hero = Character("Test Hero")
    hero.alignment = "Lawful_Good"
    hero.character_class = "Fighter"
    hero.background = "Soldier"
    hero.roll_abilities()
    hero.set_race("Human")
    hero.calculate_hp()
    hero.add_skill_proficiency('athletics')
    hero.gold = 150

    # Create game state
    game = GameState()
    game.create_new_game(hero)

    # Add some history
    game.add_to_history("exploration", "Entered the dark forest")
    game.add_to_history("combat", "Fought a goblin")
    game.current_location = "Mysterious Cave"

    # Test AI context
    context = game.get_context_for_ai()
    print("AI Context:", context)

    # Save the game
    game.save_game()

    # Create new game state and load
    new_game = GameState()
    success = new_game.load_game(f"saves/{game.session_id}.json")

    if success:
        print(f"Loaded character: {new_game.player.name}")
        print(f"Location: {new_game.current_location}")
        print(f"History events: {len(new_game.history)}")
        new_game.player.display_character()
    else:
        print("Failed to load game.")


def test_character_creation():
    """Test character creation"""
    print("Testing character creation...")

    # Create new character
    hero = Character("Test Hero")
    hero.alignment = "Lawful Good"
    hero.character_class = "Fighter"
    hero.background = "Soldier"

    # Roll abilities first
    hero.roll_abilities()

    # Then set race (this will apply racial bonuses)
    hero.set_race("Human")

    # Calculate HP
    hero.calculate_hp()

    # Add some proficiencies (typical for a fighter)
    hero.add_skill_proficiency("athletics")
    hero.add_skill_proficiency("intimidation")
    hero.add_saving_throw_proficiency("strength")
    hero.add_saving_throw_proficiency("constitution")

    # Add some starting wealth
    hero.gold = 150
    hero.silver = 50
    hero.copper = 200

    # Display the character
    hero.display_character()

def test_dice_system():
    """Test the dice rolling system"""
    print("Testing dice system...")
    
    dice = DiceRoller()

    # Test some sample rolls
    test_rolls = ["1d20", "2d6", "1d8+3", "3d6-1"]

    for roll in test_rolls:
        result = dice.roll(roll)
        print(f"{roll}: {result['rolls']} + {result['modifier']} = {result['final_total']}")

def test_ai_connection():
    """Test if we can talk to Ollama"""
    print("Testing connection to Ollama...")

    # Create AI interface
    ai = AIInterface()

    # Send test message
    response = ai.send_message("Hello! Can you roleplay as a D&D dungeon master? Just say yes or no.")

    print(f"AI Response: {response}")

if __name__ == "__main__":
    game = GameLoop()
    game.start_new_game()