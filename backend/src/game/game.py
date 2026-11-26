from .board import Board
from .rules import get_simple_moves


def main():
    board = Board()

    print("Tabuleiro inicial:")
    board.print_board()

    # Movimentos das peças brancas
    moves = get_simple_moves(board, Board.WHITE)

    print("\nMovimentos possíveis das brancas:")

    for move in moves:
        print(f'{move["from"]} -> {move["to"]}')

    print(f"\nTotal de movimentos: {len(moves)}")


if __name__ == "__main__":
    main()
