"""Mystery Island: The Lost Lighthouse. Run with: python main.py

This file handles only input and output. All game rules live in game.py.
"""

import game

QUIT_WORDS = ["q", "quit", "exit"]


def show_title():
    """Print the title screen and instructions."""
    print("=" * 50)
    print("   MYSTERY ISLAND: THE LOST LIGHTHOUSE")
    print("=" * 50)
    print("A storm left you stranded. Light the lighthouse beacon")
    print("so the rescue boat can find you.")
    print()
    print("How to play:")
    print("  - Type the number of an action and press Enter.")
    print("  - Walking costs 1 energy. You start with 5.")
    print("  - Type 'i' for inventory, 'h' for help, 'q' to quit.")
    print("  - Reach 0 energy and you lose.")
    print()


def show_status(player):
    """Print where the player is and how they are doing."""
    location = player["location"]
    print()
    print("-" * 50)
    print(f"Location: {location}   Energy: {player['energy']}/{game.MAX_ENERGY}")
    print(game.LOCATIONS[location]["description"])


def show_inventory(player):
    """Print the items the player carries."""
    if player["inventory"]:
        print("You carry: " + ", ".join(player["inventory"]))
    else:
        print("Your bag is empty.")


def show_menu(actions):
    """Print the numbered list of actions."""
    print("What will you do?")
    for number, action in enumerate(actions, start=1):
        print(f"  {number}. {game.describe_action(action)}")
    print("  i. Inventory   h. Help   q. Quit")


def ask_name():
    """Ask for a name until the player types something."""
    while True:
        name = input("What is your name? ").strip()
        if name:
            return name
        print("Please type at least one letter.")


def play_game():
    """Play one full game. Return True if the player quit."""
    player = game.new_game(ask_name())
    print(f"\nWelcome, {player['name']}. Good luck.")

    while not player["game_over"]:
        show_status(player)
        actions = game.available_actions(player)
        show_menu(actions)
        choice = game.clean_input(input("> "))

        if choice in QUIT_WORDS:
            print("You gave up. Goodbye.")
            return True
        if choice == "i":
            show_inventory(player)
            continue
        if choice == "h":
            show_title()
            continue
        if not choice.isdigit() or not 1 <= int(choice) <= len(actions):
            print(f"'{choice}' is not a valid choice. Type a number from 1 to {len(actions)}.")
            continue

        action = actions[int(choice) - 1]
        print(game.apply_action(player, action))

    print()
    if game.is_win(player):
        print(f"YOU WIN, {player['name']}! You escaped Mystery Island with {player['energy']} energy left.")
    else:
        print(f"GAME OVER, {player['name']}. The island keeps its secrets.")
    return False


def ask_replay():
    """Ask yes/no until a valid answer. Return True for yes."""
    while True:
        answer = game.clean_input(input("Play again? (y/n) "))
        if answer in ["y", "yes"]:
            return True
        if answer in ["n", "no"]:
            return False
        print("Please type y or n.")


def main():
    """Start the program and handle replays."""
    show_title()
    while True:
        quit_now = play_game()
        if quit_now or not ask_replay():
            print("Thanks for playing.")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye.")
