from .ai_interface import AIInterface
from .character import Character
from .dice import DiceRoller
from .game_state import game_state
from .combat import CombatSystem

class GameLoop:
    def __init__(self):
        self.ai = AIInterface()
        self.dice = DiceRoller()
        self.combat = CombatSystem()
        self.game_state = game_state()
        self.running = False

    """----------------"""
    """Start a New Game"""
    """----------------"""   
    
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

    """------------------"""
    """Character Creation"""
    """------------------"""
    
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



        # Classes selection
        classes = ['fighter', 'wizard', 'rogue', 'cleric', 'ranger', 'barbarian', 'bard', 'druid', 'monk', 'paladin', 'sorcerer', 'warlock']
        print(f"Avaliable classes: {', '.join(classes)}")

        character_class = None
        while character_class not in classes:
            character_class = input("Choose your class: ").lower()
            if character_class not in classes:
                print(f"Invalid class '{character_class}'. Please choose from: {', '.join(classes)}")

        character.character_class = character_class.capitalize()
        
        # Character background input
        character.background = input("Enter your background: ")
        
        # Alignment selection
        alignments = ['lawful good', 'neutral good', 'chaotic good', 'lawful neutral', 'true neutral', 'chaotic neutral', 'lawful evil', 'neutral evil', 'chaotic evil']
        print(f"Avaliable alignments: {', '.join(alignments)}")

        alignment = None
        while alignment not in alignments:
            alignment = input("Choose your alignment: ").lower()
            if alignment not in alignments:
                print(f"Invalid alignment '{alignment}'. Please choose from: {', '}.join(alignments)")

        character.alignment = alignment.title()

        # Roll abilities and apply racial bonuses
        character.roll_abilities()
        character.set_race(race)
        character.calculate_hp()

        # Add some proficiencies (simplified)
        character.add_skill_proficiency('perception')

        character.display_character()
        return character

    """--------------"""
    """Main Game Loop"""
    """--------------"""

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

    """-----------------"""
    """AI DM Role Prompt"""
    """-----------------"""

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
                - Keep responses under 250 words
                - End with "What will you do?"

            Start the adventure now."""

        return prompt
    
    """------------------------------------------"""
    """Developer Menu - For Testing Purposes Only"""
    """------------------------------------------"""

    def dev_menu(self):
        """Developer menu for testing purposes"""
        dev_help = {
            '1': "Print full game state: Dumps all variables and their values currently tracked in the game state (useful for deep debugging).",
            '2': "Print character details: Shows all data for the player character, even hidden/internal attributes.",
            '3': "Show recent history: Print the last 12 entries in the DM/player/AI action log.",
            '4': "Show latest AI prompt/context: Reveals exactly what context is being sent to the AI model.",
            '5': "Send test prompt to AI: Lets you enter any prompt and see what the AI model responds.",
            '6': "Roll custom dice: Enter any dice formula (like 3d6+2) and see random output.",
            '7': "Start debug combat round: Runs a simulated battle round with a simple enemy.",
            '8': "Save game now: Triggers save to the current or a new file immediately.",
            '9': "Load a save file: Lets you pick a file and loads the game state from it.",
            '10': "Edit player stats/inventory: Change player XP, gold, HP, or add/remove items—for testing.",
            '11': "List all save files: Quickly shows all available saved game files in the saves folder.",
            '12': "Exit Dev Menu: Return to the main menu/game turn.",
            'help': "Show this help text for every option."
        }

        dev_menu_options = {
            print("\n=== Developer Menu ==="),
            print("H. Help on dev menu options"),
            print("1. Print full game state"),
            print("2. Print character details"),
            print("3. Show recent action/AI/DM history"),
            print("4. Show latest AI prompt/context"),
            print("5. Send a test prompt to AI"),
            print("6. Roll custom dice"),
            print("7. Start debug combat round"),
            print("8. Save game now"),
            print("9. Load a save file"),
            print("10. Edit player stats/inventory"),
            print("11. List all save files"),
            print("12. Exit Dev Menu")
        }

        while True: 
            print(dev_menu_options)
            choice = input("Developer Option ('1'-'12' or 'help): ").strip().upper()

            if choice == 'H' or choice == 'HELP':
                for key, desc in dev_help.items():
                    print(f"{key}: {desc}")
            
            elif choice == '1':
                print("\n--- Full Game State ---")
                print(vars(self.game_state))
            
            elif choice == '2':
                print("\n--- Character Details ---")
                self.game_state.player.display_character()

            elif choice == '3':
                print("\n--- Recent History ---")
                history = self.game_state.get_recent_history[-12:]
                for entry in history:
                    print(entry)
            
            elif choice == '4':
                print("\n--- Latest AI Prompt/Context ---")
                context = self.game_state.get_context_for_ai()
                print(context)

            elif choice == '5':
                test_prompt = input("Enter test prompt for AI: ")
                response = self.ai.send_message(test_prompt)
                print("\nAI Response:", response)
            
            elif choice == '6':
                dice_input = input("Enter dice to roll (e.g., '1d20', '2d6+3'): ")
                try:
                    result = self.dice.roll(dice_input)
                    print(f"Roll result: {result['rolls']} + {result['modifier']} = {result['final_total']}")
                except Exception as e:
                    print(f"Error rolling dice: {e}")
                
            elif choice == '7':
                print("\n--- Starting Debug Combat Round ---")
                self.combat.start_combat(self.game_state.player)
            
            elif choice == '8':
                self.game_state.save_game()
                print("Game saved.")
            
            elif choice == '9':
                filename = input("Enter save file name to load: ")
                try:
                    self.game_state.load_game(filename)
                    print(f"Game loaded from {filename}.")
                except Exception as e:
                    print(f"Error loading game:", e)
            
            elif choice == '10':
                print("\n--- Edit Player Stats/Inventory ---")
                stat = input("Enter stat to edit (xp, gold, hp) or 'item' to add/remove item: ").strip().lower()
                if stat in ['xp', 'gold', 'hp']:
                    try:
                        value = int(input(f"Enter new value for {stat}: "))
                        setattr(self.game_state.player, stat, value)
                        print(f"{stat} updated to {value}.")
                    except ValueError:
                        print("Invalid value. Must be an integer.")
                elif stat == 'item':
                    action = input("Add or remove item? (a/r): ").strip().lower()
                    item = input("Enter item name: ").strip()
                    if action == 'a':
                        self.game_state.player.add_item(item)
                        print(f"Added {item} to inventory.")
                    elif action == 'r':
                        self.game_state.player.remove_item(item)
                        print(f"Removed {item} from inventory.")
                    else:
                        print("Invalid action. Use 'a' to add or 'r' to remove.")
                else:
                    print("Invalid stat/item option.")

            elif choice == '11':
                print("\n--- Available Save Files ---")
                self.game_state.list_save_files()

            elif choice == '12':
                print("Exiting Developer Menu.")
                break

            # FINISH ADDING DEV MENU OPTIONS

    """-------------------"""
    """Player Turn Options"""
    """-------------------"""

    def process_turn(self):
        """Process a single turn of the game"""
        print("\nYour turn:")
        print("1. Take a suggested action")
        print("2. Take a custom action")
        print("3. Check character sheet")
        print("4. Save game")
        print("5. Quit game")
        print("6. Developer Menu") # Delete in Final Build - ONLY FOR DEV TESTING PURPOSES
        
        choice = input("Choose (1-6): ").strip()

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
        elif choice == '6':
            self.dev_menu()
        else: 
            print("Invalid choice. Please select a valid option.")

    """----------------------"""
    """Player Action Handling"""
    """----------------------"""

    def handle_action(self, action):
        """Handle the player's action and AI response"""
        # Add action to history
        self.game_state.add_to_history("action", f"Player: {action}")

        # Send action to AI
        history = self.game_state.get_recent_history(5)
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

    """--------------------"""
    """Player Roll Handling"""
    """--------------------"""

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