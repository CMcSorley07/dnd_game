import random

class DiceRoller:
    def __init__(self):
        pass

    def roll(self, dice_notation):
        """
        Roll dice using standard D&D notation
        Examples: "1d20", "2d6", "1d8+3", "3d6+2"
        """
        dice_notation = dice_notation.lower().replace(" ", "")

        # Handle modifiers (+ or -)
        modifier = 0
        if '+' in dice_notation:
            dice_part, mod_part = dice_notation.split('+')
            modifier = int(mod_part)
        elif '-' in dice_notation:
            dice_part, mod_part = dice_notation.split('-')
            modifier = -int(mod_part)
        else:
            dice_part = dice_notation
        
        # Parse dice (format: XdY)
        if 'd' not in dice_part:
            raise ValueError("Invalid dice notation. Use format like '1d20', '2d6', '2d6+3'")

        count_str, sides_str = dice_part.split('d')
        count = int(count_str)
        sides = int(sides_str)

        # Roll the dice
        result = self.roll_multiple(count, sides)
        result['modifier'] = modifier
        result['final_total'] = result['total'] + modifier
        result['notation'] = dice_notation

        return result

    def roll_single(self, sides):
        """Roll a single die with the given number of sides."""
        return random.randint(1, sides)
    
    def roll_multiple(self, count, sides):
        """Roll multiple dice and return individual results + total"""
        rolls = [self.roll_single(sides) for _ in range(count)]
        total = sum(rolls)
        return {
            'rolls': rolls,
            'total': total,
            'dice': f"{count}d{sides}"
        }