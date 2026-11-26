
from game.board import Board


def get_simple_moves(board, player):
    """
    Retorna os movimentos diagonais simples das peças comuns.

    player:
        1  -> Brancas
        -1 -> Pretas

    Cada movimento é representado por:
        {
            "from": (linha_origem, coluna_origem),
            "to": (linha_destino, coluna_destino)
        }
    """

    moves = []

    # Brancas avançam para cima; pretas avançam para baixo.
    direction = -1 if player == Board.WHITE else 1

    for row in range(Board.SIZE):
        for col in range(Board.SIZE):

            piece = board.get_piece(row, col)

            # Considera somente peças comuns do jogador atual.
            if piece != player:
                continue

            # Diagonais para frente.
            for col_direction in [-1, 1]:

                new_row = row + direction
                new_col = col + col_direction

                # Verifica os limites do tabuleiro.
                if not (
                    0 <= new_row < Board.SIZE
                    and 0 <= new_col < Board.SIZE
                ):
                    continue

                # Verifica se a casa de destino está vazia.
                if board.get_piece(new_row, new_col) == Board.EMPTY:

                    moves.append({
                        "from": (row, col),
                        "to": (new_row, new_col)
                    })

    return moves
