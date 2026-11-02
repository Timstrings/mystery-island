# Mystery Island: The Lost Lighthouse

A text adventure written in Python using only the standard library. You wake up on an island after a storm. Light the lighthouse beacon before your energy runs out so the rescue boat can find you.

## Prerequisites

- Python 3.8 or newer (built and tested with Python 3.14)
- No packages to install

## How to run

```bash
python main.py
```

## How to run the tests

```bash
python -m unittest discover -s tests -v
```

## Map

```
Beach <-> Jungle <-> Cave <-> Old Bridge <-> Lighthouse
          (rope)    (lantern)  (needs rope)  (needs lantern)
```

## Game rules

| Rule | Detail |
|---|---|
| Start | Beach, 5 energy, empty inventory |
| Moving | Every legal move costs exactly 1 energy. You can only walk to neighbouring locations. |
| Items | Rope (Jungle) and lantern (Cave). Each can be picked up only once. Picking up is free. |
| Bridge | Crossing from Old Bridge to Lighthouse needs the rope. If you're blocked, you lose no energy. |
| Beacon | Needs the lantern and only works at the Lighthouse. If you're blocked, you lose no energy. |
| Win | Light the beacon at the Lighthouse while you still have energy. |
| Lose | Energy reaches 0 before you win, or you swim the river. |
| Invalid input | Shows a friendly message. Energy, location and inventory stay the same. |
| Replay | Starts a brand-new game: fresh energy, location and inventory. |

### Decisions with consequences

1. **Eat the red berries (Jungle):** you lose 1 energy.
2. **Drink from the spring (Cave):** you gain 1 energy, up to the maximum of 5. Works only once.
3. **Swim the river (Old Bridge):** you lose immediately.
4. **Walk back and forth:** wastes energy and can make you lose.

Energy is tight. The direct winning path takes 4 moves, so the shortest win finishes with exactly 1 energy left.

## Controls

- Type the number of an action and press Enter. Spaces are ignored, so ` 1 ` works.
- `i`: show inventory
- `h`: show help
- `q`, `quit` or `exit`: quit (any capitalisation, e.g. ` EXIT `)

## Example winning run

```
Beach       -> 1 (Walk to Jungle)       energy 4
Jungle      -> 3 (Pick up rope)
Jungle      -> 2 (Walk to Cave)         energy 3
Cave        -> 3 (Pick up lantern)
Cave        -> 2 (Walk to Old Bridge)   energy 2
Old Bridge  -> 2 (Walk to Lighthouse)   energy 1
Lighthouse  -> 2 (Light the beacon)     YOU WIN
```

## Example losing run

Walk Beach -> Jungle -> Beach -> Jungle -> Beach -> Jungle. Your energy reaches 0 and you lose.

## Project structure

```
main.py            Input and output only (menus, print, input)
game.py            All game rules as testable functions (no input/print)
tests/test_game.py 15 unittest tests, including acceptance tests T1-T10
```

### Key functions (game.py)

| Function | Returns | Purpose |
|---|---|---|
| `new_game(name)` | dict | A fresh player state with a new inventory list |
| `clean_input(raw)` | str | Removes surrounding spaces and lowercases the text |
| `available_actions(player)` | list | The actions allowed at the current location |
| `apply_action(player, action)` | str | Checks the action, updates state and returns a message |
| `move_player(player, dest)` | str | Moves the player, costs energy and checks the bridge rule |
| `can_cross_bridge(player)` | bool | True if the player has the rope |
| `can_light_beacon(player)` | bool | True if the player is at the Lighthouse with the lantern |
| `is_win(player)` / `is_loss(player)` | bool | Checks the outcome |

## Known limitations

- There's no save or load. Quitting loses your progress.
- There's only one winning path and the island is fixed (no random events).
- You choose actions by number, not by typing words like `go north`.
- Menu numbers can change after you pick up an item, because that item disappears from the menu.
- Pressing Ctrl+C or Ctrl+D exits the game politely instead of crashing.
