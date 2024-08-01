# player.py

class Player:
    def __init__(self, color):
        # set up the player with a color and captured stones count
        self.color = color
        self.captured_stones = 0

    def capture_stones(self, count):
        # increment captured stones count
        self.captured_stones += count
