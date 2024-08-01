# board.py

class Board:
    def __init__(self, size=19):
        self.size = size
        self.grid = [['🟤' for _ in range(size)] for _ in range(size)]
        self.history = []

    def display(self):
        print("  " + " ".join(map(str, range(self.size))))
        for i, row in enumerate(self.grid):
            print(f"{i} " + " ".join(row))
        print()

    def place_stone(self, x, y, color):
        self.grid[x][y] = color

    def is_empty(self, x, y):
        return self.grid[x][y] == '🟤'

    def remove_stone(self, x, y):
        self.grid[x][y] = '🟤'

    def save_state(self):
        self.history.append([row[:] for row in self.grid])

    def restore_state(self):
        if self.history:
            self.grid = self.history.pop()

    def is_repetition(self):
        # check if the current board state matches any previous state
        return any(self.grid == state for state in self.history)

    def get_adjacent(self, x, y):
        adjacent = []
        if x > 0:
            adjacent.append((x - 1, y))
        if x < self.size - 1:
            adjacent.append((x + 1, y))
        if y > 0:
            adjacent.append((x, y - 1))
        if y < self.size - 1:
            adjacent.append((x, y + 1))
        return adjacent

    def get_group(self, x, y):
        color = self.grid[x][y]
        to_visit = [(x, y)]
        visited = set()
        group = []

        while to_visit:
            cx, cy = to_visit.pop()
            if (cx, cy) not in visited:
                visited.add((cx, cy))
                group.append((cx, cy))
                for nx, ny in self.get_adjacent(cx, cy):
                    if self.grid[nx][ny] == color and (nx, ny) not in visited:
                        to_visit.append((nx, ny))

        return group

    def get_liberties(self, x, y):
        group = self.get_group(x, y)
        liberties = set()

        for gx, gy in group:
            for nx, ny in self.get_adjacent(gx, gy):
                if self.is_empty(nx, ny):
                    liberties.add((nx, ny))

        return liberties

    def handle_capture(self, x, y, color):
        captured_stones = 0
        for nx, ny in self.get_adjacent(x, y):
            if self.grid[nx][ny] != color and self.grid[nx][ny] != '🟤':
                if not self.get_liberties(nx, ny):
                    group = self.get_group(nx, ny)
                    for gx, gy in group:
                        self.remove_stone(gx, gy)
                    captured_stones += len(group)
        return captured_stones

    def is_suicide(self, x, y, color):
        # temporarily place the stone
        self.place_stone(x, y, color)
        no_liberties = not self.get_liberties(x, y)

        # restore the board state
        self.remove_stone(x, y)

        if no_liberties:
            # place the stone temporarily
            self.place_stone(x, y, color)
            # check if placing the stone results in any of the player's groups having no liberties
            for nx, ny in self.get_adjacent(x, y):
                if self.grid[nx][ny] == color:
                    if not self.get_liberties(nx, ny):
                        self.remove_stone(x, y)
                        return True
            self.remove_stone(x, y)
            return False
        return False

    def calculate_score(self):
        black_area, white_area = 0, 0
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] == '⚫':
                    black_area += 1
                elif self.grid[x][y] == '⚪':
                    white_area += 1
                else:
                    black_adjacent, white_adjacent = False, False
                    for nx, ny in self.get_adjacent(x, y):
                        if self.grid[nx][ny] == '⚫':
                            black_adjacent = True
                        elif self.grid[nx][ny] == '⚪':
                            white_adjacent = True
                    if black_adjacent and not white_adjacent:
                        black_area += 1
                    elif white_adjacent and not black_adjacent:
                        white_area += 1
        return black_area, white_area
