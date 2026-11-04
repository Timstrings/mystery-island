# Reflection

The concept I understand better now is separating game logic from input and output. Because `game.py` does not use `input()` or `print()`, its rules can be tested automatically without manually playing the game.

I also learned why `new_game()` creates a new inventory list: it prevents items such as the rope or lantern from carrying over into a replay. In addition, invalid input does not change the game state because the program checks whether an action is available before using energy or moving the player.

Overall, this project helped me understand how to organise Python code into logic, tests, and a user interface, and how unit tests can prove that a program works correctly.