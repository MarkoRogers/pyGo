# main.py

from game import Game

def main():
    # ask the user for the board size
    while True:
        try:
            board_size = int(input("enter the board size (e.g., 19 for a 19x19 board): "))
            if board_size < 2:
                print("board size must be at least 2.")
                continue
            break
        except ValueError:
            print("invalid input. please enter a valid number.")

    game = Game(board_size)

    # main game loop
    while True:
        game.board.display()
        move = input(f"player {game.current_player.color}, enter your move (row col) or 'pass': ")
        if move.lower() == 'pass':
            game.pass_turn()
        else:
            try:
                x, y = map(int, move.split())
                if x < 0 or x >= board_size or y < 0 or y >= board_size:
                    print("move out of bounds, try again.")
                    continue
                if not game.play_turn(x, y):
                    print("invalid move, try again.")
            except ValueError:
                print("invalid input, try again.")

if __name__ == "__main__":
    main()
