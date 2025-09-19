from src.ai_interface import AIInterface

def test_ai_connnection():
    """Test if we can talk to Ollama"""
    print("Testing connection to Ollama...")

    # Create AI interface
    ai = AIInterface()

    # Send test message
    response = ai.send_message("Hello! Can you roleplay as a D&D dungeon master? Just say yes or no.")

    print(f"AI Response: {response}")

if __name__ == "__main__":
    test_ai_connnection()