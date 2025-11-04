import json
from .dice import DiceRoller

class Character:
    def __init__(self, name=""):
        self.name = name
        self.level = 1
        self.race = ""
        self.character_class = ""
        self.background = ""
        self.alignment = ""
        
        # Core ability scores (standard D&D 6 stats)
        self.abilities = {
            'strength': 10,
            'dexterity': 10,
            'constitution': 10,
            'intelligence': 10,
            'wisdom': 10,
            'charisma': 10
        }
        
        # Derived stats
        self.hit_points = 0
        self.max_hit_points = 0
        self.armor_class = 10
        self.proficiency_bonus = 2  # Level 1 starts with +2
        self.speed = 30  # Standard human speed
        
        # Saving throws (will be modified by proficiencies)
        self.saving_throws = {
            'strength': 0,
            'dexterity': 0,
            'constitution': 0,
            'intelligence': 0,
            'wisdom': 0,
            'charisma': 0
        }
        
        # Skills (simplified list of key D&D skills)
        self.skills = {
            'acrobatics': 0,      # Dex
            'athletics': 0,       # Str
            'deception': 0,       # Cha
            'history': 0,         # Int
            'insight': 0,         # Wis
            'intimidation': 0,    # Cha
            'investigation': 0,   # Int
            'medicine': 0,        # Wis
            'perception': 0,      # Wis
            'persuasion': 0,      # Cha
            'stealth': 0,         # Dex
            'survival': 0         # Wis
        }
        
        # Proficiencies
        self.skill_proficiencies = []
        self.saving_throw_proficiencies = []
        
        # Equipment and inventory
        self.inventory = []
        self.equipment = {'armor': None, 'weapons': [], 'shield': None}
        
        # Currency
        self.gold = 0
        self.silver = 0
        self.copper = 0
        
        # Experience
        self.experience_points = 0
        
        # Initialize dice roller for character creation
        self.dice = DiceRoller()

    # Inventory management methods
    def add_to_inventory(self, item): # add item to inventory
        self.inventory.append(item)

    def remove_from_inventory(self, item): # remove item from inventory
        if item in self.inventory:
            self.inventory.remove(item)

    def equip_item(self, item, slot):
        """
        Equip an item to the specified slot.
        slot must be one of "weapons" (list, "armor" (single), or "shield" (single).
        """
        if item not in self.inventory:
            print(f"{item} is not in inventory!")
            return False

        if slot == "weapons":
            self.equipment["weapons"].append(item)
            return True
        elif slot in ["armor", "shield"]:
            self.equipment[slot] = item
            return True
        else:
            print(f"Invalid equipment slot: {slot}")
            return False

    def unequip_item(self, item, slot):
        """
        Unequip an item from the specified slot.
        """
        if slot == "weapons":
            if slot == "weapons":
                if item in self.equipment["weapons"]:
                    self.equipment["weapons"].remove(item)
                    return True
            elif slot in ["armor", "shield"]:
                if self.equipment[slot] == item:
                    self.equipment[slot] = None
                    return True
            print(f"{item} is not equiped in {slot}.")
            return False
    
    def get_racial_bonuses(self):
        """Get ability score increases and traits based on race"""
        racial_bonuses = {
            'human': {
                'asi': {'strength': 1, 'dexterity': 1, 'constitution': 1, 'intelligence': 1, 'wisdom': 1, 'charisma': 1},
                'traits': ['Extra Language', 'Extra Skill']
            },
            'elf': {
                'asi': {'dexterity': 2},
                'traits': ['Darkvision', 'Fey Ancestry', 'Trance']
            },
            'dwarf': {
                'asi': {'constitution': 2},
                'traits': ['Darkvision', 'Dwarven Resilience', 'Stonecunning']
            },
            'halfling': {
                'asi': {'dexterity': 2},
                'traits': ['Lucky', 'Brave', 'Halfling Nimbleness']
            },
            'dragonborn': {
                'asi': {'strength': 2, 'charisma': 1},
                'traits': ['Draconic Ancestry', 'Breath Weapon', 'Damage Resistance']
            },
            'gnome': {
                'asi': {'intelligence': 2},
                'traits': ['Darkvision', 'Gnome Cunning']
            },
            'half-elf': {
                'asi': {'charisma': 2, 'choice': 2},  # +2 Cha, +1 to two different abilities
                'traits': ['Darkvision', 'Fey Ancestry', 'Extra Skills']
            },
            'half-orc': {
                'asi': {'strength': 2, 'constitution': 1},
                'traits': ['Darkvision', 'Relentless Endurance', 'Savage Attacks']
            },
            'tiefling': {
                'asi': {'intelligence': 1, 'charisma': 2},
                'traits': ['Darkvision', 'Hellish Resistance', 'Infernal Legacy']
            }
        }
        
        return racial_bonuses.get(self.race.lower(), {'asi': {}, 'traits': []})

    def apply_racial_bonuses(self):
        """Apply racial ability score increases"""
        if not self.race:
            return
        
        bonuses = self.get_racial_bonuses()
        asi = bonuses.get('asi', {})
        
        print(f"\nApplying {self.race} racial bonuses:")
        
        for ability, bonus in asi.items():
            if ability == 'choice':
                continue  # Handle choice bonuses separately
            
            old_score = self.abilities[ability]
            self.abilities[ability] += bonus
            print(f"  {ability.capitalize()}: {old_score} -> {self.abilities[ability]} (+{bonus})")
        
        # Handle racial traits
        traits = bonuses.get('traits', [])
        if traits:
            print(f"  Racial Traits: {', '.join(traits)}")
        
        # Update derived stats after racial bonuses
        self.update_derived_stats()

    def set_race(self, race):
        """Set character race and apply bonuses"""
        self.race = race
        self.apply_racial_bonuses()
    
    def get_ability_modifier(self, ability):
        """Calculate D&D ability modifier from ability score"""
        score = self.abilities.get(ability, 10)
        return (score - 10) // 2
    
    def calculate_saving_throw(self, ability):
        """Calculate saving throw bonus"""
        base_mod = self.get_ability_modifier(ability)
        proficiency = self.proficiency_bonus if ability in self.saving_throw_proficiencies else 0
        return base_mod + proficiency
    
    def calculate_skill(self, skill):
        """Calculate skill bonus"""
        # Map skills to their governing abilities
        skill_abilities = {
            'acrobatics': 'dexterity',
            'athletics': 'strength',
            'deception': 'charisma',
            'history': 'intelligence',
            'insight': 'wisdom',
            'intimidation': 'charisma',
            'investigation': 'intelligence',
            'medicine': 'wisdom',
            'perception': 'wisdom',
            'persuasion': 'charisma',
            'stealth': 'dexterity',
            'survival': 'wisdom'
        }
        
        ability = skill_abilities.get(skill, 'intelligence')
        base_mod = self.get_ability_modifier(ability)
        proficiency = self.proficiency_bonus if skill in self.skill_proficiencies else 0
        
        return base_mod + proficiency
    
    def update_derived_stats(self):
        """Update all derived stats after ability scores change"""
        # Update saving throws
        for ability in self.saving_throws:
            self.saving_throws[ability] = self.calculate_saving_throw(ability)
        
        # Update skills
        for skill in self.skills:
            self.skills[skill] = self.calculate_skill(skill)
        
        # Update AC (base 10 + dex modifier, will be modified by armor later)
        self.armor_class = 10 + self.get_ability_modifier('dexterity')
    
    def roll_abilities(self):
        """Roll ability scores using 4d6 drop lowest method"""
        print("Rolling ability scores (4d6, drop lowest)...")
        
        for ability in self.abilities.keys():
            # Roll 4d6, drop the lowest
            rolls = [self.dice.roll_single(6) for _ in range(4)]
            rolls.sort(reverse=True)  # Sort high to low
            total = sum(rolls[:3])    # Take the top 3
            
            self.abilities[ability] = total
            print(f"{ability.capitalize()}: {rolls} -> {total} (modifier: {self.get_ability_modifier(ability):+d})")
        
        # Apply racial bonuses if race is set
        if self.race:
            self.apply_racial_bonuses()
        
        # Update all derived stats
        self.update_derived_stats()
    
    def calculate_hp(self):
        class_hit_dice = {
            "barbarian": 12,
            "fighter": 10,
            "paladin": 10,
            "ranger": 10,
            "bard": 8,
            "cleric": 8,
            "druid": 8, 
            "monk": 8, 
            "rogue": 8,
            "warlock": 8,
            "wizard": 8,
            "sorcerer": 6,
            # add homebrew/classes as needed
        }
        con_mod = self.get_ability_modifier('constitution')
        hd = class_hit_dice.get(self.characterclass.lower(), 8) # hit dice
        base_hp = hd # Level 1: max value of hit die
        self.max_hitpoints = base_hp + con_mod
        self.hitpoints = self.max_hitpoints
        
        print(f"Hit Points: {self.hit_points}/{self.max_hit_points}")
    
    def add_skill_proficiency(self, skill):
        """Add skill proficiency"""
        if skill not in self.skill_proficiencies:
            self.skill_proficiencies.append(skill)
            self.skills[skill] = self.calculate_skill(skill)
    
    def add_saving_throw_proficiency(self, ability):
        """Add saving throw proficiency"""
        if ability not in self.saving_throw_proficiencies:
            self.saving_throw_proficiencies.append(ability)
            self.saving_throws[ability] = self.calculate_saving_throw(ability)
    
    def display_character(self):
        """Display character sheet"""
        print(f"\n=== {self.name} ===")
        print(f"Level {self.level} {self.race} {self.character_class}")
        print(f"Background: {self.background}")
        print(f"Alignment: {self.alignment}")
        print(f"Experience: {self.experience_points} XP")
        
        print(f"\nAbility Scores:")
        for ability, score in self.abilities.items():
            modifier = self.get_ability_modifier(ability)
            print(f"  {ability.capitalize()}: {score} ({modifier:+d})")
        
        print(f"\nCombat Stats:")
        print(f"  Hit Points: {self.hit_points}/{self.max_hit_points}")
        print(f"  Armor Class: {self.armor_class}")
        print(f"  Speed: {self.speed} feet")
        print(f"  Proficiency Bonus: +{self.proficiency_bonus}")
        
        print(f"\nSaving Throws:")
        for ability, bonus in self.saving_throws.items():
            prof_mark = "*" if ability in self.saving_throw_proficiencies else ""
            print(f"  {ability.capitalize()}: {bonus:+d} {prof_mark}")
        
        print(f"\nSkills:")
        for skill, bonus in self.skills.items():
            prof_mark = "*" if skill in self.skill_proficiencies else ""
            print(f"  {skill.capitalize()}: {bonus:+d} {prof_mark}")
        
        print(f"\nWealth:")
        print(f"  Gold: {self.gold}, Silver: {self.silver}, Copper: {self.copper}")