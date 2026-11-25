class Board:
    EMPTY = 0
    WHITE = 1
    WHITE_KING = 2
    BLACK = -1
    BLACK_KING = -2

    SIZE = 8

    def __init__(self):
        self.grid = self.create_initial_board()

    def create_initial_board(self):
        board = [
            [self.EMPTY for _ in range(self.SIZE)]
            for _ in range(self.SIZE)
        ]

        # Peças pretas nas três primeiras linhas
        for row in range(3):
            for col in range(self.SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = self.BLACK

        # Peças brancas nas três últimas linhas
        for row in range(5, 8):
            for col in range(self.SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = self.WHITE

        return board

    def print_board(self):
        symbols = {
            self.EMPTY: ".",
            self.WHITE: "b",
            self.WHITE_KING: "B",
            self.BLACK: "p",
            self.BLACK_KING: "P"
        }

        print("  0 1 2 3 4 5 6 7")

        for row in range(self.SIZE):
            print(row, end=" ")

            for col in range(self.SIZE):
                print(symbols[self.grid[row][col]], end=" ")

            print()

    def get_piece(self, row, col):
        return self.grid[row][col]

    def set_piece(self, row, col, piece):
        self.grid[row][col] = piece
