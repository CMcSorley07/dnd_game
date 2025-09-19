from src.ai_interface import AIInterface
from src.dice import DiceRoller

def test_dice_system():
    """Test the dice rolling system"""
    print("Testing dice system...")
    
    dice = DiceRoller()

    # Test some rolls
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
    test_dice_system()
    print()
    test_ai_connnection()