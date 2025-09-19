import json
import os
from datetime import datetime
from .character import Character

class GameState:
    def __init__(self):
        self.player = None
        self.current_location = ""
        self.world_state = {}
        self.history = [] # Store all actions/events
        self.quests = []
        self.session_id = ""
        self.last_saved = None

    def create_new_game(self, character):
        """Start a new game with a character"""
        self.player = character
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.current_location = "Starting Village"
        self.add_to_history("game_start", f"New adventure begins with {character.name}")

    def add_to_history(self, event_type, description):
        """Add an event to the game history"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'description': description
        }
        self.history.append(event)

    def get_context_for_ai(self):
        """Get game context to send to AI"""
        context = {
            'character_name': self.player.name if self.player else "Unknown",
            'location': self.current_location,
            'recent_history': self.history[-5:] if len(self.history) > 5 else self.history,
            'character_stats': {
                'level': self.player.level if self.player else 1, 
                'race': self.player.race if self.player else "Unknown",
                'class': self.player.character_class if self.player else "Unknown",
                'hp': f"{self.player.hit_points}/{self.player.max_hit_points}" if self.player else "0/0"
            }
        }
        return context
    
    def save_game(self, filename=None):
        """Save the current game state"""
        if not filename:
            filename = f"saves/{self.session_id}.json"

        # Create saves directory if it doesn't exist
        os.makedirs('saves', exist_ok=True)

        # Convert character to directory
        character_data = self._character_to_dict(self.player) if self.player else None

        save_data = {
            'session_id': self.session_id,
            'player': character_data,
            'current_location': self.current_location,
            'world_state': self.world_state,
            'history': self.history,
            'quests': self.quests,
            'last_saved': datetime.now().isoformat(),
        }

        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)

        self.last_saved = datetime.now().isoformat()
        print(f"Game saved to {filename}")

    def load_game(self, filename):
        """ Load a saved game state"""
        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)
            
            self.session_id = save_data.get('session_id', '')
            self.current_location = save_data.get('current_location', '')
            self.world_state = save_data.get('world_state', {})
            self.history = save_data.get('history', [])
            self.quests = save_data.get('quests', [])
            self.last_saved = save_data.get('last_saved')

            # Reconstruct character
            character_data = save_data.get('player')
            if character_data:
                self.player = self._dict_to_character(character_data)

            print(f"Game loaded from {filename}")
            return True
        
        except FileNotFoundError:
            print(f"Save file {filename} not found.")
            return False
        except json.JSONDecodeError:
            print(f"Error reading save file {filename}.")
            return False
        
    def _character_to_dict(self, character):
        """Convert Character object to dictionary for saving"""
        return {
            'name': character.name,
            'level': character.level,
            'race': character.race,
            'character_class': character.character_class,
            'background': character.background,
            'alignment': character.alignment,
            'abilities': character.abilities,
            'hit_points': character.hit_points,
            'max_hit_points': character.max_hit_points,
            'armor_class': character.armor_class,
            'proficiency_bonus': character.proficiency_bonus,
            'speed': character.speed,
            'skill_proficiencies': character.skill_proficiencies,
            'saving_throw_proficiencies': character.saving_throw_proficiencies,
            'inventory': character.inventory,
            'equipment': character.equipment,
            'gold': character.gold,
            'silver': character.silver,
            'copper': character.copper,
            'experience_points': character.experience_points
        }

    def _dict_to_character(self, data):
        """Convert dicationary back to character object"""
        character = Character(data.get('name', ''))
        character.level = data.get('level', 1)
        character.race = data.get('race', '')
        character.character_class = data.get('character_class', '')
        character.background = data.get('background', '')
        character.alignment = data.get('alignment', '')
        character.abilities = data.get('abilities', character.abilities)
        character.hit_points = data.get('hit_points', 0)
        character.max_hit_points = data.get('max_hit_points', 0)
        character.armor_class = data.get('armor_class', 10)
        character.proficiency_bonus = data.get('proficiency_bonus', 2)
        character.speed = data.get('speed', 30)
        character.skill_proficiencies = data.get('skill_proficiencies', [])
        character.saving_throw_proficiencies = data.get('saving_throw_proficiencies', [])
        character.inventory = data.get('inventory', [])
        character.equipment = data.get('equipment', {})
        character.gold = data.get('gold', 0)
        character.silver = data.get('silver', 0)
        character.copper = data.get('copper', 0)
        character.experience_points = data.get('experience_points', 0)

        # Recalculate desired stats
        character.update_derived_stats()

        return character