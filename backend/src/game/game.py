from .board import Board
from .rules import get_simple_moves

def apply_move(board, move):
    """
    Executa um movimento simples ou uma sequência de capturas.
    """

    if isinstance(move, dict):
        moves = [move]
    else:
        moves = move

    if not moves:
        raise ValueError("A sequência de movimentos está vazia.")

    start_row, start_col = moves[0]["from"]
    piece = board.get_piece(start_row, start_col)

    if piece == Board.EMPTY:
        raise ValueError("Não existe peça na posição inicial.")

    for step in moves:
        from_row, from_col = step["from"]
        to_row, to_col = step["to"]

        board.set_piece(from_row, from_col, Board.EMPTY)

        if "capture" in step:
            capture_row, capture_col = step["capture"]
            board.set_piece(capture_row, capture_col, Board.EMPTY)

        board.set_piece(to_row, to_col, piece)

    # Verifica promoção após a jogada completa
    final_row, final_col = moves[-1]["to"]

    if piece == Board.WHITE and final_row == 0:
        board.set_piece(final_row, final_col, Board.WHITE_KING)

    elif piece == Board.BLACK and final_row == Board.SIZE - 1:
        board.set_piece(final_row, final_col, Board.BLACK_KING)

    return board

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
