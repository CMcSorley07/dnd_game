import requests
import json
import time
import os

class AIInterface:
    def __init__(self, model_name="pplx-70b-online", base_url="https://api.perplexity.ai"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_key = os.environ.get("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise RuntimeError("Missing PERPLEXITY_API_KEY environment")
    
    ai_example_responses = [
        ("Found in a back alley, you find a door to a hole in the wall shop called The Funny Bone. "
        "As the door creaks open, you are greeted by a musty mix of brimstone and popcorn. "
        "Steping in, you see a skeleton in a tacky purple suit that suddenly jumps to life, "
        "only to introduce himself as Morty Smiles, a sentient skeleton who isn't sure why he's alive, "
        "but knows his purpose is to make people laugh. He is always DYING to tell you a joke, "
        "but often laughs so hard at his own jokes that he drops his jawbone. "
        "You can buy a number of comical goods, such as the Goulie Cushon, an inflatable balloon that screams when sat on. "
        "Or a chattering trap, which is a set of fake teeth that you can wind up and set loose to clamp onto someone's foot. "
        "Found in a back alley, you find a door to a hole in the wall shop called The Funny Bone. As the door creaks open, you are "
        "greeted by a musty mix of brimstone and popcorn. Steping in, you see a skeleton in a tacky purple suit that suddenly jumps "
        "to life, only to introduce himself as Morty Smiles, a sentient skeleton who isn't sure why he's alive, but knows his purpose "
        "is to make people laugh. He is always DYING to tell you a joke, but often laughs so hard at his own jokes that he drops his "
        "jawbone. You can buy a number of comical goods, such as the Goulie Cushon, an inflatable balloon that screams when sat on. "
        "Or a chattering trap, which is a set of fake teeth that you can wind up and set loose to clamp onto someone's foot."),

        ("Following the scent of warm sugar and cinnamon through the winding streets, you stumble upon an impossibly narrow storefront "
        "wedged between two larger buildings, no wider than six feet across. A wooden sign swings gently overhead, showing a loaf of "
        "bread tucked into a beetle's shell, with 'Snug as a Bug' painted in cheerful letters. As you duck through the tiny doorway, "
        "the aroma intensifies, it smells like every comfort food you've ever known, all at once. Behind a flower-dusted counter stands "
        "Grub the Bub, a plump gnome with a tall chef's hat that nearly scrapes the low seiling and round spectacles pearched on his "
        "button nose. He beams at you with genuine warmth, wiping his hands on his apron before gesturing excitedly to his display case. "
        "He has a number of popular dishes, such as Snugleberry Pie which has the effect of casting calm emotions on anyone who eats it "
        "and tastes like a warm hug, or the confessional cupcakes, which force you to say a secret on your mind, to finally get those "
        "burdening thoughts off your chest."),

        ("Crossing a bridge in the stonewall city of Greyhaven, you hear an odd splashing and chittering from below. Peering over the edge, "
        "you spot a ramshackle collection of driftwood, salvaged crates, and rusted metal forming a ship built directly into the bridge's "
        "underside. A weathered, crudely painted sign hangs from a roughly cut loop of thread that reads 'Trashure Trove - One man's trash is "
        "another man's legendary treasure!' Climbing down a old rickety ladder fashioned from tattered ropes and roting planks, you're hit "
        "with the scent of damp river water and mildew mixed with something oddly enticing, like old books and forgotten trinkets. Inside "
        "the cramped space, lit by flickering lanterns and glowing fungi, stands Nibbles, a strange man you can only describe as half rat, "
        "with twitching whiskers, a long scally tail, and sharp beady eyes that gleam with mischief. He wears a patchwork coat made from "
        "various fabrics and scavenged materials, each piece telling a story of its own. Nibbles squeaks as he gestures widely to his "
        "ever-changing inventory of oddities spread across waterlogged crates and makeshift shelves, explaining that he travels the waterways, "
        "collecting discarded items and forgotten relics to sell to adventurers like yourself. You can find him and his shop under any bridge"
        "selling a number of unique items, specialized to whatever rare or common goods can be scavenged from the riverbed below. \n\n As your eyes "
        "adjust to the dim light, you notice river stones glinting with an unusual sheen scattered across a crate-- Nibbles  squeeks excitedly "
        "that they are locally-sourced river stones and are rumored to hold peculiar magical properties. He scurries over to another shelf, "
        "pulling out a tattered, waterlogged journal with pages still legible despite their dampness, chattering about a merchant ship that met "
        "an unfortunate end upstream. A rusty compass catches your eye, and when you pick it up, Nibbles launches into an animated tale about "
        "plucking it from the riverbed just last week after the spring floods. But then he pauses, his wiskers twitching as he beckons you deeper "
        "into his cramped shop. 'Local treasures are fun and all,' he squeaks, 'but wait until you see what I've collected from distant watters!' "
        "He proudly displays a shelf of oddities that clearly don't belong to this region--a barnacle-encrusted lockbox from some far=off coast, "
        "a jeweled trinket that sparkles with faint magic, and a strange carved idol whose purpose even Nibbles admids he can't quite explain. "
        )
    ]
    def send_message(self, message, system=None):
        if system is None:
            # Construct an example system prompt with context
            system = (
                "You are a creative Dungeons & Dragons Dungeon Master. Keep responses concise and actionable. \n\n"
                "Example 1 - Shop Description:\n"
                f"{self.ai_example_responses[0]}\n\n"
                "Example 2 - Shop Description:\n"
                f"{self.ai_example_responses[1]}\n\n"
                "Example 3 - Shop Description of Nibbles 'Trashure Trove':\n"
                f"{self.ai_example_responses[2]}\n\n"
                "Now, I want you to generate similar types of actionable responses based on these examples."
            )
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        payload = {
            "model": "sonar-reasoning-pro",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": message},
            ],
            "max_tokens": 256,
        }

        backoff = 1.0
        for attempt in range(3): 
            try:
                print("Payload:", json.dumps(payload, indent=2)) # Debugging line to print the payload
                
                resp = requests.post(url, headers=headers, json=payload, timeout=60)
                print(f"Status code: {resp.status_code}")
                print(f"Response text: {resp.text}")
                if resp.status_code == 429:
                    time.sleep(backoff)
                    backoff *= 2
                    continue 
                resp.raise_for_status()
                result = resp.json()
                # Perplexity response format: choices[0].message.content
                return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            except requests.RequestException as e:
                if attempt == 2:
                    return f"Error communicating with Perplexity: {e}"
                time.sleep(backoff)
                backoff *= 2

        return "Failed to get response after multiple attempts."