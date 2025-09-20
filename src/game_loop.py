from .ai_interface import AIInterface
from .character import Character
from .dice import DiceRoller
from .game_state import GameState
from .combat import CombatSystem

class GameLoop:
    def __init__(self):
        self.ai = AIInterface()
        self.dice = DiceRoller()
        self.combat = CombatSystem()
        self.game_state = GameState()
        self.running = False

    def start_new_game(self):
        """Start a new D&D campaign"""
        print("Welcome to AI D&D!")

        # Character creation 
        character = self.create_character()

        # Initialize game state
        self.game_state.create_new_game(character)

        # Start the adventure
        self.running = True
        self.main_game_loop()

    def create_character(self):
        """Interactive character creation"""
        print("\n--- Character Creation ---")

        name = input("Enter your character's name: ")
        character = Character(name)

        # Race selection
        races = ['human', 'elf', 'dwarf', 'halfling', 'dragonborn', 'gnome', 'half-elf', 'half-orc', 'tiefling']
        print(f"Available races: {', '.join(races)}")

        race = None
        while race not in races:
            race = input("Choose your race: ").lower()
            if race not in races:
                print(f"Invalid race '{race}'. Please choose from: {', '.join(races)}")

        # Classes and background
        character.character_class = input("Enter your class: ")
        character.background = input("Enter your background: ")
        character.alignment = input("Enter your alignment: ")

        # Roll abilities and apply racial bonuses
        character.roll_abilities()
        character.set_race(race)
        character.calculate_hp()

        # Add some proficiencies (simplified)
        character.add_skill_proficiency('perception')

        character.display_character()
        return character
    
    def main_game_loop(self):
        """Main game loop"""
        # Initial AI setup
        setup_prompt = self.create_initial_prompt()
        response = self.ai.send_message(setup_prompt)

        print("\n" + "="*50)
        print("Dungeon Master: ")
        print(response)
        print("="*50)

        while self.running:
            self.process_turn()

    def create_initial_prompt(self):
        """Create the initial prompt for the AI"""
        context = self.game_state.get_context_for_ai()

        prompt = f"""You are a dungeon master for a D&D 5e campaign.

CHARACTER: {context['character_name']}, Level {context['character_stats']['level']} {context['character_stats']['race']} {context['character_stats']['class']}
LOCATION: {context['location']}

INSTRUCTIONS:
- Create an engaging fantasy adventure
- Present the scene and offer 2-3 action
- When actions require dice rolls, say "Please roll the [dice] for [action]"
- I will handle all the dice rolling and calculations
- You only Narrate outcomes based on the roll results I give you
- Keep responses under 150 words
- End with "What will you do?"

Start the adventure now."""

        return prompt
        
    def process_turn(self):
        """Process a single turn of the game"""
        print("\nYour turn:")
        print("1. Take a suggested action")
        print("2. Take a custom action")
        print("3. Check character sheet")
        print("4. Save game")
        print("5. Quit game")
            
        choice = input("Choose (1-5): ").strip()

        if choice == '1':
            action = input("Describe your action: ")
            self.handle_action(action)
        elif choice == '2':
            action = input("Describe your custom action: ")
            self.handle_action(action)
        elif choice == '3':
            self.game_state.player.display_character()
        elif choice == '4':
            self.game_state.save_game()
        elif choice == '5':
            self.quit_game()
        else: 
            print("Invalid choice. Please select a valid option.")

    def handle_action(self, action):
        """Handle the player's action and AI response"""
        # Add action to history
        self.game_state.add_to_history("action", f"Player: {action}")

        # Send action to AI
        context = self.game_state.get_context_for_ai()
        prompt = f"""
        The player wants to: {action}
        
        Character: {context['character_name']} (Level {context['character_stats']['level']} {context['character_stats']['race']} {context['character_stats']['class']})
        Current HP: {context['character_stats']['hp']}
        Location: {context['location']}

        Respond as a D&D DM. If this action needs a dice roll, ask for it specifically.
        Otherwise, narrate what happens and present new choices. 
        End with "What will you do?"
        """

        ai_response = self.ai.send_message(prompt)
        print("\n" + "="*50)
        print(ai_response)
        print("="*50)

        # Check if AI requested a dice roll
        if "roll" in ai_response.lower():
            self.handle_dice_request(ai_response, action)

        # Add AI response to history
        self.game_state.add_to_history("dm_response", ai_response)

    def handle_dice_request(self, ai_response , original_action):
        """Handle when AI requests a dice roll"""
        print("\nThe DM has requested a dice roll!")
        dice_input = input("Enter dice to roll (e.g., '1d20', '1d20+3'): ")

        try:
            result = self.dice.roll(dice_input)
            roll_total = result['final_total']

            print(f"You rolled: {result['rolls']} + {result['modifier']} = {roll_total}")

            # Send result back to AI
            context = self.game_state.get_context_for_ai()
            result_prompt = f"""
            The player attempted: {original_action}
            They rolled {dice_input} and got: {roll_total}

            Narrate the outcome based on the roll result.
            Then present new options and end with "What do you do?"
            """

            outcome = self.ai.send_message(result_prompt)

            print("\n" + "="*50)
            print("DUNGEON MASTER: ")
            print(outcome)
            print("="*50)

            # Add roll result to history
            self.game_state.add_to_history("dice_roll", f"{dice_input}: {roll_total}")
            self.game_state.add_to_history("outcome", outcome)

        except Exception as e:
            print(f"Error with dice roll: {e}")
    
    def quit_game(self):
        """Quit the game with save option"""
        save = input("Save before quitting? (y/n): ").lower()
        if save == 'y':
            self.game_state.save_game()

        print("Thanks for playing!")
        self.running = False

def main():
    """Main entry point"""
    game = GameLoop()
    game.start_new_game()

if __name__ == "__main__":
    main()