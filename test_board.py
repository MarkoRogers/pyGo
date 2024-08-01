# test_board.py

import unittest
from board import Board


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board(size=3)

    def test_initial_board(self):
        expected = [
            ['🟤', '🟤', '🟤'],
            ['🟤', '🟤', '🟤'],
            ['🟤', '🟤', '🟤']
        ]
        self.assertEqual(self.board.grid, expected)

    def test_place_stone(self):
        self.board.place_stone(1, 1, '⚫')
        self.assertEqual(self.board.grid[1][1], '⚫')

    def test_is_empty(self):
        self.assertTrue(self.board.is_empty(0, 0))
        self.board.place_stone(0, 0, '⚫')
        self.assertFalse(self.board.is_empty(0, 0))

    def test_remove_stone(self):
        self.board.place_stone(0, 0, '⚫')
        self.board.remove_stone(0, 0)
        self.assertTrue(self.board.is_empty(0, 0))

    def test_get_group(self):
        self.board.place_stone(0, 0, '⚫')
        self.board.place_stone(0, 1, '⚫')
        self.board.place_stone(1, 0, '⚫')
        self.board.place_stone(1, 1, '⚫')
        group = self.board.get_group(0, 0)
        expected_group = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.assertEqual(set(group), set(expected_group))

    def test_get_liberties(self):
        self.board.place_stone(0, 0, '⚫')
        self.board.place_stone(0, 1, '⚫')
        self.board.place_stone(1, 0, '⚫')
        self.board.place_stone(1, 1, '⚫')
        # (2, 2) should be a liberty
        liberties = self.board.get_liberties(2, 2)
        expected_liberties = {(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)}
        self.assertEqual(liberties, expected_liberties)

    def test_is_suicide(self):
        self.board = Board(size=3)
        self.board.place_stone(0, 0, '⚫')
        self.board.place_stone(0, 1, '⚫')
        self.board.place_stone(1, 0, '⚫')
        self.board.place_stone(1, 1, '⚫')
        # Place a stone at (2, 2) should result in suicide
        self.assertTrue(self.board.is_suicide(2, 2, '⚫'))

        # Clear the board and test a non-suicide move
        self.board = Board(size=3)
        self.board.place_stone(0, 0, '⚫')
        self.board.place_stone(0, 1, '⚫')
        self.board.place_stone(1, 0, '⚫')
        self.board.place_stone(1, 1, '⚫')
        # (0, 2) is not surrounded
        self.assertFalse(self.board.is_suicide(0, 2, '⚫'))


if __name__ == '__main__':
    unittest.main()
