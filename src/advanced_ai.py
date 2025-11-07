import requests
import json
import time


class AIInterface:
    def __init__(self, model_name="llama3.2:3b", base_url="http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.base_url = base_url
    
        self.example_responses = {
            "shop": """
        Found in a back alley, you find a door to a hole in the wall shop called The Funny Bone.
        As the door creaks open, you are greeted by a musty mix of brimstone and popcorn.
        Steping in, you see a skeleton in a tacky purple suit that suddenly jumps to life,
        only to introduce himself as Morty Smiles, a sentient skeleton who isn't sure why he's alive,
        but knows his purpose is to make people laugh. He is always DYING to tell you a joke,
        but often laughs so hard at his own jokes that he drops his jawbone.
        You can buy a number of comical goods, such as the Goulie Cushon, an inflatable balloon that screams when sat on.
        Or a chattering trap, which is a set of fake teeth that you can wind up and set loose to clamp onto someone's foot.
        Found in a back alley, you find a door to a hole in the wall shop called The Funny Bone. As the door creaks open, you are
        greeted by a musty mix of brimstone and popcorn. Steping in, you see a skeleton in a tacky purple suit that suddenly jumps
        to life, only to introduce himself as Morty Smiles, a sentient skeleton who isn't sure why he's alive, but knows his purpose
        is to make people laugh. He is always DYING to tell you a joke, but often laughs so hard at his own jokes that he drops his
        jawbone. You can buy a number of comical goods, such as the Goulie Cushon, an inflatable balloon that screams when sat on.
        Or a chattering trap, which is a set of fake teeth that you can wind up and set loose to clamp onto someone's foot.
        """,
            "food": """
        Following the scent of warm sugar and cinnamon through the winding streets, you stumble upon an impossibly narrow storefront
        wedged between two larger buildings, no wider than six feet across. A wooden sign swings gently overhead, showing a loaf of
        bread tucked into a beetle's shell, with 'Snug as a Bug' painted in cheerful letters. As you duck through the tiny doorway,
        the aroma intensifies, it smells like every comfort food you've ever known, all at once. Behind a flower-dusted counter stands
        Grub the Bub, a plump gnome with a tall chef's hat that nearly scrapes the low seiling and round spectacles pearched on his
        button nose. He beams at you with genuine warmth, wiping his hands on his apron before gesturing excitedly to his display case.
        He has a number of popular dishes, such as Snugleberry Pie which has the effect of casting calm emotions on anyone who eats it
        and tastes like a warm hug, or the confessional cupcakes, which force you to say a secret on your mind, to finally get those
        burdening thoughts off your chest.
        """,
            "merchant": """
        Crossing a bridge in the stonewall city of Greyhaven, you hear an odd splashing and chittering from below. Peering over the edge,
        you spot a ramshackle collection of driftwood, salvaged crates, and rusted metal forming a ship built directly into the bridge's
        underside. A weathered, crudely painted sign hangs from a roughly cut loop of thread that reads 'Trashure Trove - One man's trash is
        another man's legendary treasure!' Climbing down a old rickety ladder fashioned from tattered ropes and roting planks, you're hit
        with the scent of damp river water and mildew mixed with something oddly enticing, like old books and forgotten trinkets. Inside
        the cramped space, lit by flickering lanterns and glowing fungi, stands Nibbles, a strange man you can only describe as half rat,
        with twitching whiskers, a long scally tail, and sharp beady eyes that gleam with mischief. He wears a patchwork coat made from
        various fabrics and scavenged materials, each piece telling a story of its own. Nibbles squeaks as he gestures widely to his
        ever-changing inventory of oddities spread across waterlogged crates and makeshift shelves, explaining that he travels the waterways,
        collecting discarded items and forgotten relics to sell to adventurers like yourself. You can find him and his shop under any bridge
        selling a number of unique items, specialized to whatever rare or common goods can be scavenged from the riverbed below.

        As your eyes adjust to the dim light, you notice river stones glinting with an unusual sheen scattered across a crate-- Nibbles  squeeks excitedly
        that they are locally-sourced river stones and are rumored to hold peculiar magical properties. He scurries over to another shelf,
        pulling out a tattered, waterlogged journal with pages still legible despite their dampness, chattering about a merchant ship that met
        an unfortunate end upstream. A rusty compass catches your eye, and when you pick it up, Nibbles launches into an animated tale about
        plucking it from the riverbed just last week after the spring floods. But then he pauses, his wiskers twitching as he beckons you deeper
        into his cramped shop. 'Local treasures are fun and all,' he squeaks, 'but wait until you see what I've collected from distant watters!'
        He proudly displays a shelf of oddities that clearly don't belong to this region--a barnacle-encrusted lockbox from some far-off coast,
        a jeweled trinket that sparkles with faint magic, and a strange carved idol whose purpose even Nibbles admits he can't quite explain.
        """
        }

    def send_message(self, message, example_type=None, debug=False):
        # Compose system prompt for a concise, actionable DM
        system_prompt = (
            "You are a skilled Dungeon Master for a D&D-style game. "
            "You create vivid descriptions, NPC dialogue, and dynamic story events. "
            "Keep responses immersive, concise, and actionable for players."
        )

        # Optionally append an in-style example to guide tone/content
        if example_type and example_type in self.example_responses:
            system_prompt += f"\n\nExample ({example_type}):\n{self.example_responses[example_type]}"

        # Prefer sending system separately (supported by Ollama generate)
        payload = {
            "model": self.model_name,
            "system": system_prompt,
            "prompt": f"Player: {message}\nDM:",
            "stream": True
        }

        if debug:
            print("\nPayload being sent to Ollama:")
            print(json.dumps({**payload, "stream": False}, indent=2))

        backoff = 1.0
        for attempt in range(3):
            try:
                with requests.post(self.base_url, json=payload, timeout=60, stream=True) as resp:
                    resp.raise_for_status()
                    # Ensure we have an encoding for decode_unicode=True fallback
                    if resp.encoding is None:
                        resp.encoding = "utf-8"

                    # Stream JSON lines until "done": true
                    for line in resp.iter_lines(decode_unicode=True):
                        if not line:
                            continue
                        try:
                            chunk = json.loads(line)
                        except json.JSONDecodeError:
                            continue

                        if "response" in chunk:
                            print(chunk["response"], end="", flush=True)

                        if chunk.get("done"):
                            break

                print()  # newline after stream
                return None  # streamed output already printed

            except requests.RequestException as e:
                if attempt == 2:
                    return f"Error communicating with Ollama: {e}"
                time.sleep(backoff)
                backoff *= 2

        raise RuntimeError("Failed to get a response after multiple attempts.")


if __name__ == "__main__":
    ai = AIInterface()
    # Use a defined example type or None
    ai.send_message(
        "Describe a mysterious cave filled with ancient runes.",
        example_type="shop",
        debug=False
    )
    print("\n--- Llama 3.2 3B Response ---\n")