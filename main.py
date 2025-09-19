from src.ai_interface import AIInterface
from src.dice import DiceRoller
from src.character import Character

def test_character_creation():
    """Test character creation"""
    print("Character Creation Test""")

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
    hero.add_skill_proficiency("Athletics")
    hero.add_skill_proficiency("Intimidation")
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

def test_ai_connnection():
    """Test if we can talk to Ollama"""
    print("Testing connection to Ollama...")

    # Create AI interface
    ai = AIInterface()

    # Send test message
    response = ai.send_message("Hello! Can you roleplay as a D&D dungeon master? Just say yes or no.")

    print(f"AI Response: {response}")

if __name__ == "__main__":
    test_character_creation()
    test_dice_system()
    print()
    test_ai_connnection()