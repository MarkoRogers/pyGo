# test_game.py

import unittest
from game import Game

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(board_size=3)  # Initialize the game with a 3x3 board

    def test_suicide_move(self):
        self.game.play_turn(0, 0)  # Assuming player ⚫'s move
        self.game.play_turn(0, 1)
        self.game.play_turn(1, 0)
        self.game.play_turn(1, 1)
        # Place a stone at (2, 2) should result in suicide
        self.assertTrue(self.game.is_suicide(2, 2, '⚫'))

    def test_repetition(self):
        self.game.play_turn(0, 0)
        self.game.pass_turn()  # First pass
        self.game.play_turn(0, 1)
        self.game.pass_turn()  # Second pass
        self.assertTrue(self.game.board.is_repetition())

    def test_end_game(self):
        self.game.play_turn(0, 0)
        self.game.play_turn(0, 1)
        self.game.play_turn(0, 2)
        self.game.play_turn(1, 0)
        self.game.play_turn(1, 1)
        self.game.play_turn(1, 2)
        self.game.play_turn(2, 0)
        self.game.play_turn(2, 1)
        self.game.play_turn(2, 2)

        self.game.pass_turn()  # First pass
        result = self.game.pass_turn()  # Second pass
        self.assertEqual(result, '⚫')

if __name__ == '__main__':
    unittest.main()
