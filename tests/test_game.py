import copy
import unittest

import game


def play(player, actions):
    """Helper: apply a list of actions one after another."""
    for action in actions:
        game.apply_action(player, action)
    return player


WIN_PATH = ["go:Jungle", "take:rope", "go:Cave", "take:lantern",
            "go:Old Bridge", "go:Lighthouse", "light beacon"]


class TestNewGame(unittest.TestCase):
    def test_t1_new_game_starts_at_beach_with_5_energy(self):
        player = game.new_game("Ada")
        self.assertEqual(player["location"], "Beach")
        self.assertEqual(player["energy"], 5)
        self.assertEqual(player["inventory"], [])
        self.assertFalse(player["game_over"])


class TestInputAndMovement(unittest.TestCase):
    def test_t2_invalid_command_leaves_state_unchanged(self):
        player = game.new_game("Ada")
        before = copy.deepcopy(player)
        game.apply_action(player, "banana")
        self.assertEqual(player, before)

    def test_t3_legal_move_changes_location_and_costs_one(self):
        player = game.new_game("Ada")
        game.apply_action(player, "go:Jungle")
        self.assertEqual(player["location"], "Jungle")
        self.assertEqual(player["energy"], 4)

    def test_t4_wrong_direction_rejected_without_cost(self):
        player = game.new_game("Ada")
        game.apply_action(player, "go:Lighthouse")
        self.assertEqual(player["location"], "Beach")
        self.assertEqual(player["energy"], 5)

    def test_clean_input_handles_spaces_and_capitals(self):
        self.assertEqual(game.clean_input("  EXIT "), "exit")


class TestInventoryAndPuzzles(unittest.TestCase):
    def test_t5_rope_collected_only_once(self):
        player = play(game.new_game("Ada"), ["go:Jungle", "take:rope", "take:rope"])
        self.assertEqual(player["inventory"].count("rope"), 1)

    def test_t6_bridge_blocked_without_rope(self):
        player = play(game.new_game("Ada"), ["go:Jungle", "go:Cave", "go:Old Bridge"])
        energy_before = player["energy"]
        game.apply_action(player, "go:Lighthouse")
        self.assertEqual(player["location"], "Old Bridge")
        self.assertEqual(player["energy"], energy_before)

    def test_t7_beacon_not_lit_without_lantern(self):
        player = play(game.new_game("Ada"),
                      ["go:Jungle", "take:rope", "go:Cave", "go:Old Bridge", "go:Lighthouse"])
        game.apply_action(player, "light beacon")
        self.assertFalse(game.is_win(player))

    def test_t8_correct_items_and_location_win(self):
        player = play(game.new_game("Ada"), WIN_PATH)
        self.assertTrue(game.is_win(player))
        self.assertGreater(player["energy"], 0)

    def test_cannot_win_away_from_lighthouse(self):
        player = play(game.new_game("Ada"), ["go:Jungle", "take:rope", "go:Cave", "take:lantern"])
        game.apply_action(player, "light beacon")
        self.assertFalse(game.is_win(player))


class TestEnergyAndOutcomes(unittest.TestCase):
    def test_t9_energy_exhaustion_causes_loss(self):
        player = play(game.new_game("Ada"),
                      ["go:Jungle", "go:Beach", "go:Jungle", "go:Beach", "go:Jungle"])
        self.assertEqual(player["energy"], 0)
        self.assertTrue(game.is_loss(player))

    def test_energy_never_negative_and_no_moves_after_game_over(self):
        player = play(game.new_game("Ada"),
                      ["go:Jungle", "go:Beach", "go:Jungle", "go:Beach", "go:Jungle"])
        game.apply_action(player, "go:Cave")
        self.assertEqual(player["energy"], 0)
        self.assertEqual(player["location"], "Jungle")

    def test_swimming_the_river_loses(self):
        player = play(game.new_game("Ada"), ["go:Jungle", "go:Cave", "go:Old Bridge", "swim river"])
        self.assertTrue(game.is_loss(player))

    def test_water_restores_energy_only_once(self):
        player = play(game.new_game("Ada"), ["go:Jungle", "go:Cave", "drink water", "drink water"])
        self.assertEqual(player["energy"], 4)

    def test_t10_replay_resets_state(self):
        old = play(game.new_game("Ada"), WIN_PATH)
        fresh = game.new_game("Ada")
        self.assertEqual(fresh["location"], "Beach")
        self.assertEqual(fresh["energy"], 5)
        self.assertEqual(fresh["inventory"], [])
        self.assertIsNot(fresh["inventory"], old["inventory"])


if __name__ == "__main__":
    unittest.main()
