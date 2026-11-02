"""Game logic for Mystery Island: The Lost Lighthouse.

This module contains NO input() calls and NO print() calls.
Every function receives data and returns data, so it can be tested
with unittest without anyone typing at the keyboard.
"""

START_LOCATION = "Beach"
START_ENERGY = 5
MAX_ENERGY = 5

# The island map. Each location has a description, the places you can
# walk to (exits) and the item lying there (or None).
LOCATIONS = {
    "Beach": {
        "description": "Wet sand and broken planks. The dark lighthouse stands far away.",
        "exits": ["Jungle"],
        "item": None,
    },
    "Jungle": {
        "description": "Thick vines everywhere. Red berries hang from a bush.",
        "exits": ["Beach", "Cave"],
        "item": "rope",
    },
    "Cave": {
        "description": "Cold and quiet. A small spring of fresh water trickles in the corner.",
        "exits": ["Jungle", "Old Bridge"],
        "item": "lantern",
    },
    "Old Bridge": {
        "description": "A broken rope bridge over a fast river. The lighthouse is on the other side.",
        "exits": ["Cave", "Lighthouse"],
        "item": None,
    },
    "Lighthouse": {
        "description": "The top of the lighthouse. The great beacon is cold and dark.",
        "exits": ["Old Bridge"],
        "item": None,
    },
}


def new_game(name):
    """Return a brand-new player dictionary (fresh inventory every time)."""
    return {
        "name": name,
        "location": START_LOCATION,
        "energy": START_ENERGY,
        "inventory": [],          # a NEW list, never shared with an old game
        "drank_water": False,
        "game_over": False,
        "won": False,
    }


def clean_input(raw):
    """Remove spaces around the text and make it lowercase: ' EXIT ' -> 'exit'."""
    return raw.strip().lower()


def has_item(player, item):
    """Return True if the item is in the player's inventory."""
    return item in player["inventory"]


def can_cross_bridge(player):
    """Return True only if the player carries the rope."""
    return has_item(player, "rope")


def can_light_beacon(player):
    """Return True only if the player is at the Lighthouse with the lantern."""
    return player["location"] == "Lighthouse" and has_item(player, "lantern")


def is_win(player):
    """Return True if the player has won."""
    return player["won"]


def is_loss(player):
    """Return True if the game ended without a win."""
    return player["game_over"] and not player["won"]


def available_actions(player):
    """Return the list of action codes the player may choose right now."""
    if player["game_over"]:
        return []

    location = player["location"]
    place = LOCATIONS[location]
    actions = []

    for destination in place["exits"]:
        actions.append("go:" + destination)

    item = place["item"]
    if item is not None and not has_item(player, item):
        actions.append("take:" + item)

    if location == "Jungle":
        actions.append("eat berries")
    if location == "Cave" and not player["drank_water"]:
        actions.append("drink water")
    if location == "Old Bridge":
        actions.append("swim river")
    if location == "Lighthouse":
        actions.append("light beacon")

    return actions


def describe_action(action):
    """Turn an action code into friendly menu text."""
    if action.startswith("go:"):
        return "Walk to the " + action[3:] + " (costs 1 energy)"
    if action.startswith("take:"):
        return "Pick up the " + action[5:]
    labels = {
        "eat berries": "Eat the red berries",
        "drink water": "Drink from the spring",
        "swim river": "Try to swim across the river",
        "light beacon": "Light the beacon",
    }
    return labels.get(action, action)


def move_player(player, destination):
    """Move the player one step. Return a message describing what happened."""
    if destination == "Lighthouse" and player["location"] == "Old Bridge":
        if not can_cross_bridge(player):
            return "The bridge is broken. You need a rope to tie it before crossing."

    player["location"] = destination
    player["energy"] -= 1
    message = "You walk to the " + destination + ". " + LOCATIONS[destination]["description"]

    if player["energy"] <= 0:
        player["energy"] = 0
        player["game_over"] = True
        message += "\nYou collapse from exhaustion. The rescue boat sails past..."
    return message


def take_item(player, item):
    """Add the item to the inventory. Return a message."""
    player["inventory"].append(item)
    return "You picked up the " + item + "."


def apply_action(player, action):
    """Apply one action to the player and return a message.

    Rules:
    - If the game is over, nothing changes.
    - If the action is not allowed here, nothing changes (no energy cost).
    """
    if player["game_over"]:
        return "The game is over. No more moves."

    if action not in available_actions(player):
        return "You can't do that here."

    if action.startswith("go:"):
        return move_player(player, action[3:])

    if action.startswith("take:"):
        return take_item(player, action[5:])

    if action == "eat berries":
        player["energy"] = max(0, player["energy"] - 1)
        message = "The berries are sour and make you sick. You lose 1 energy."
        if player["energy"] == 0:
            player["game_over"] = True
            message += "\nYou are too weak to continue..."
        return message

    if action == "drink water":
        player["drank_water"] = True
        player["energy"] = min(MAX_ENERGY, player["energy"] + 1)
        return "The cool water refreshes you. You gain 1 energy."

    if action == "swim river":
        player["game_over"] = True
        return "The current is too strong. You are swept out to sea..."

    if action == "light beacon":
        if not can_light_beacon(player):
            return "It is too dark to find the beacon's wick. You need a lantern."
        player["won"] = True
        player["game_over"] = True
        return "The beacon blazes to life! The rescue boat turns toward the island. You are saved!"

    return "You can't do that here."
