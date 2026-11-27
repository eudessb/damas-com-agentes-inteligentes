
from .board import Board
from .rules import get_legal_moves


def apply_move(board, move):
    """
    Executa um movimento simples ou uma sequência de capturas.
    """

    moves = [move] if isinstance(move, dict) else move

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

    # Promoção ao final da jogada completa
    final_row, final_col = moves[-1]["to"]

    if piece == Board.WHITE and final_row == 0:
        board.set_piece(final_row, final_col, Board.WHITE_KING)

    elif piece == Board.BLACK and final_row == Board.SIZE - 1:
        board.set_piece(final_row, final_col, Board.BLACK_KING)

    return board


class CheckersGame:
    def __init__(self):
        self.board = Board()
        self.current_player = Board.WHITE

        self.winner = None
        self.status = "ongoing"
        self.draw_reason = None

        self.history = []

        # Guarda quantas vezes cada posição já apareceu
        self.position_counts = {}
        self._register_position()

        self._check_game_over()

    def get_legal_moves(self):
        if self.status != "ongoing":
            return []

        return get_legal_moves(self.board, self.current_player)

    def play_move(self, move):
        """
        Valida e executa uma jogada do jogador atual.
        """

        if self.status != "ongoing":
            raise ValueError("A partida já terminou.")

        legal_moves = self.get_legal_moves()

        if move not in legal_moves:
            raise ValueError("Movimento inválido.")

        player = self.current_player

        # Registra a jogada no histórico
        self.history.append({
            "player": player,
            "move": move
        })

        apply_move(self.board, move)

        # Alterna o jogador
        self.current_player = (
            Board.BLACK
            if player == Board.WHITE
            else Board.WHITE
        )

        # Registra a nova posição
        self._register_position()

        # Verifica empate por repetição
        position = self._get_position_key()

        if self.position_counts[position] >= 3:
            self.status = "draw"
            self.draw_reason = "threefold_repetition"
            return

        # Verifica se a partida terminou
        self._check_game_over()

    def _get_position_key(self):
        """
        Identifica uma posição considerando o tabuleiro
        e o jogador que deve jogar.
        """

        board_state = tuple(
            piece
            for row in self.board.grid
            for piece in row
        )

        return (board_state, self.current_player)

    def _register_position(self):
        position = self._get_position_key()

        self.position_counts[position] = (
            self.position_counts.get(position, 0) + 1
        )

    def _check_game_over(self):
        """
        Se o jogador atual não possui movimentos legais,
        o adversário vence.
        """

        if self.status != "ongoing":
            return

        legal_moves = get_legal_moves(
            self.board,
            self.current_player
        )

        if not legal_moves:
            self.status = "finished"
            self.winner = (
                Board.BLACK
                if self.current_player == Board.WHITE
                else Board.WHITE
            )

    def is_over(self):
        return self.status != "ongoing"

    def get_result(self):
        if self.status == "draw":
            return {
                "status": "draw",
                "winner": None,
                "reason": self.draw_reason
            }

        if self.status == "finished":
            return {
                "status": "finished",
                "winner": self.winner,
                "reason": "no_legal_moves"
            }

        return {
            "status": "ongoing",
            "winner": None,
            "reason": None
        }

    def print_game(self):
        self.board.print_board()

        if self.current_player == Board.WHITE:
            print("\nVez das brancas")
        else:
            print("\nVez das pretas")

        print(f"Status: {self.status}")
