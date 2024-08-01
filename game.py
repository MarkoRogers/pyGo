# game.py

import sys
from board import Board
from player import Player


class Game:
    def __init__(self, board_size=19):
        # initialize the game with a board and two players
        self.board = Board(board_size)
        self.players = [Player('⚫'), Player('⚪')]
        self.current_player = self.players[0]
        self.pass_count = 0
        self.game_over = False  # flag to indicate if the game is over

    def switch_player(self):
        # switch to the other player
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def play_turn(self, x, y):
        # handle a player's move
        if self.game_over:
            print("game is over, no more moves allowed.")
            return False, 0

        if self.board.is_empty(x, y):
            if not self.is_suicide(x, y, self.current_player.color):
                self.board.save_state()  # save state before making the move
                self.board.place_stone(x, y, self.current_player.color)
                captured = self.board.handle_capture(x, y, self.current_player.color)

                if not self.board.is_repetition():
                    self.pass_count = 0
                    self.switch_player()
                    return True, captured
                else:
                    self.board.restore_state()  # restore the previous state
                    print("move is illegal due to repetition rule.")
            else:
                print("move is illegal due to suicide rule.")
        else:
            print("move is illegal, intersection is not empty.")
        return False, 0

    def pass_turn(self):
        # handle a pass turn
        if self.game_over:
            print("game is over, no more passes allowed.")
            return

        self.pass_count += 1
        if self.pass_count >= 2:
            self.end_game()
        else:
            self.switch_player()

    def end_game(self):
        # end the game and determine the winner
        black_score, white_score = self.board.calculate_score()
        print(f"black score: {black_score}, white score: {white_score}")
        if black_score > white_score:
            print("black wins!")
        elif white_score > black_score:
            print("white wins!")
        else:
            print("it's a draw!")
        self.game_over = True  # set the game over flag
        sys.exit()  # exit the program

    def is_suicide(self, x, y, color):
        # check if placing a stone at (x, y) would be suicide (no liberties)
        return self.board.is_suicide(x, y, color)
