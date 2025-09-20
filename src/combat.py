from .dice import DiceRoller

class CombatSystem:
    def __init__(self):
        self.dice = DiceRoller()

    def roll_initiative(self, characters):
        """Roll initiative for combat participants"""
        initiative_order = []

        for character in characters:
            roll = self.dice.roll("1d20")
            dex_mod = character.get('dex_modifier', 0)
            total = roll['final_total'] + dex_mod

            initiative_order.append({
                'name': character['name'],
                'initiative': total,
                'character': character
            })

        # Sort by initiative (highest first)
        initiative_order.sort(key=lambda x: x['initiative'], reverse=True)
        return initiative_order
    
    def make_attack_roll(self, attacker, defender, weapon_type="melee"):
        """Make an attack roll"""
        attack_roll = self.dice.roll("1d20")

        # Determine ability modifier based on weapon type
        if weapon_type == "melee":
            ability_mod = attacker.get_ability_modifier('strength')
        else: # ranged
            ability_mod = attacker.get_ability_modifier('dexterity')
        
        proficiency = attacker.proficiency_bonus
        total_attack = attack_roll['final_total'] + ability_mod + proficiency
        
        target_ac = defender.get('armor_class', 10)
        hit = total_attack >= target_ac

        return {
            'attack_roll': attack_roll['final_total'],
            'ability_modifier': ability_mod,
            'proficiency_bonus': proficiency,
            'total': total_attack,
            'target_ac': target_ac,
            'hit': hit
        }
    
    def roll_damage(self, weapon_damage, ability_modifier):
        """Roll damage for a weapon"""
        damage_roll = self.dice.roll(weapon_damage)
        total_damage = damage_roll['final_total'] + ability_modifier

        return {
            'damage_roll': damage_roll['final_total'],
            'ability_modifier': ability_modifier,
            'total_damage': max(1, total_damage) # Minimum 1 damage
        }