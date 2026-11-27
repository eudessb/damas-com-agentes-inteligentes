from .board import Board


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

def get_capture_moves(board, player):
    """
    Retorna as capturas simples possíveis das peças comuns.

    Capturas podem acontecer nas quatro diagonais.
    """

    moves = []

    directions = [
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1)
    ]

    for row in range(Board.SIZE):
        for col in range(Board.SIZE):

            piece = board.get_piece(row, col)

            # Considera somente peças comuns do jogador.
            if piece != player:
                continue

            for dr, dc in directions:

                middle_row = row + dr
                middle_col = col + dc

                destination_row = row + 2 * dr
                destination_col = col + 2 * dc

                # Verifica os limites das posições.
                if not (
                    0 <= middle_row < Board.SIZE
                    and 0 <= middle_col < Board.SIZE
                    and 0 <= destination_row < Board.SIZE
                    and 0 <= destination_col < Board.SIZE
                ):
                    continue

                middle_piece = board.get_piece(
                    middle_row,
                    middle_col
                )

                destination_piece = board.get_piece(
                    destination_row,
                    destination_col
                )

                # Verifica se existe uma peça adversária
                # e se a casa de destino está vazia.
                if (
                    middle_piece * player < 0
                    and destination_piece == Board.EMPTY
                ):

                    moves.append({
                        "from": (row, col),
                        "to": (destination_row, destination_col),
                        "capture": (middle_row, middle_col)
                    })

    return moves

def get_multiple_capture_moves(board, row, col, player):
    piece = board.get_piece(row, col)

    if piece != player:
        return []

    directions = [
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1)
    ]

    sequences = []

    def explore(current_row, current_col, path):
        found_capture = False

        for dr, dc in directions:
            middle_row = current_row + dr
            middle_col = current_col + dc

            destination_row = current_row + 2 * dr
            destination_col = current_col + 2 * dc

            if not (
                0 <= middle_row < Board.SIZE
                and 0 <= middle_col < Board.SIZE
                and 0 <= destination_row < Board.SIZE
                and 0 <= destination_col < Board.SIZE
            ):
                continue

            middle_piece = board.get_piece(middle_row, middle_col)
            destination_piece = board.get_piece(
                destination_row, destination_col
            )

            if middle_piece * player >= 0:
                continue

            if destination_piece != Board.EMPTY:
                continue

            found_capture = True

            move = {
                "from": (current_row, current_col),
                "to": (destination_row, destination_col),
                "capture": (middle_row, middle_col)
            }

            # Simula a captura
            board.set_piece(current_row, current_col, Board.EMPTY)
            board.set_piece(middle_row, middle_col, Board.EMPTY)
            board.set_piece(destination_row, destination_col, piece)

            # Procura capturas a partir da nova posição
            explore(
                destination_row,
                destination_col,
                path + [move]
            )

            # Desfaz a captura para explorar outros caminhos
            board.set_piece(destination_row, destination_col, Board.EMPTY)
            board.set_piece(middle_row, middle_col, middle_piece)
            board.set_piece(current_row, current_col, piece)

        # Se não encontrou outra captura, terminou a sequência
        if not found_capture and path:
            sequences.append(path)

    explore(row, col, [])

    return sequences
