# AI Learning Log

## Entry 1

Topic: Why new_game() creates a new inventory list

What AI said: Reusing the same list would carry items such as the rope into the next game.

My experiment: I ran the tests and checked test_t10_replay_resets_state.

My conclusion: Each replay gets a fresh [], so items collected in a previous game do not return.

## Entry 2

Topic: Why invalid input does not cost energy

What AI said: apply_action checks available_actions first and returns early.

My experiment: I typed “banana” and blank input in the game; my energy stayed at 5.

My conclusion: The input is checked before any game state changes, so invalid commands have no effect.