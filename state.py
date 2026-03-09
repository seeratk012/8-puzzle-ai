class PuzzleState:
    def __init__(self, board, parent=None, move=None, depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth  # g(n)

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j

    def generate_children(self):
        children = []
        x, y = self.find_blank()
        moves = [("Up", -1, 0), ("Down", 1, 0),
                 ("Left", 0, -1), ("Right", 0, 1)]

        for move_name, dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_board = [row[:] for row in self.board]
                new_board[x][y], new_board[new_x][new_y] = (
                    new_board[new_x][new_y],
                    new_board[x][y],
                )
                children.append(
                    PuzzleState(new_board, self, move_name, self.depth + 1)
                )

        return children
