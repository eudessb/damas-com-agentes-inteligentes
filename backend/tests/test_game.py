from src.game.board import Board
from src.game.game import apply_move
from src.game.game import CheckersGame

def create_empty_board():
    board = Board()
    board.grid = [
        [Board.EMPTY for _ in range(8)]
        for _ in range(8)
    ]
    return board


def test_apply_simple_move():
    board = create_empty_board()

    board.set_piece(5, 2, Board.WHITE)

    move = {
        "from": (5, 2),
        "to": (4, 3)
    }

    apply_move(board, move)

    assert board.get_piece(5, 2) == Board.EMPTY
    assert board.get_piece(4, 3) == Board.WHITE


def test_apply_capture_move():
    board = create_empty_board()

    board.set_piece(5, 2, Board.WHITE)
    board.set_piece(4, 3, Board.BLACK)

    move = {
        "from": (5, 2),
        "to": (3, 4),
        "capture": (4, 3)
    }

    apply_move(board, move)

    assert board.get_piece(5, 2) == Board.EMPTY
    assert board.get_piece(4, 3) == Board.EMPTY
    assert board.get_piece(3, 4) == Board.WHITE


def test_white_promotion():
    board = create_empty_board()

    board.set_piece(1, 2, Board.WHITE)

    move = {
        "from": (1, 2),
        "to": (0, 3)
    }

    apply_move(board, move)

    assert board.get_piece(0, 3) == Board.WHITE_KING


def test_black_promotion():
    board = create_empty_board()

    board.set_piece(6, 3, Board.BLACK)

    move = {
        "from": (6, 3),
        "to": (7, 2)
    }

    apply_move(board, move)

    assert board.get_piece(7, 2) == Board.BLACK_KING


def test_apply_multiple_capture():
    board = create_empty_board()

    board.set_piece(5, 0, Board.WHITE)
    board.set_piece(4, 1, Board.BLACK)
    board.set_piece(2, 3, Board.BLACK)

    sequence = [
        {
            "from": (5, 0),
            "to": (3, 2),
            "capture": (4, 1)
        },
        {
            "from": (3, 2),
            "to": (1, 4),
            "capture": (2, 3)
        }
    ]

    apply_move(board, sequence)

    assert board.get_piece(5, 0) == Board.EMPTY
    assert board.get_piece(4, 1) == Board.EMPTY
    assert board.get_piece(2, 3) == Board.EMPTY
    assert board.get_piece(1, 4) == Board.WHITE

def create_game_with_empty_board():
    game = CheckersGame()

    game.board.grid = [
        [Board.EMPTY for _ in range(8)]
        for _ in range(8)
    ]

    game.current_player = Board.WHITE
    game.winner = None
    game.status = "ongoing"
    game.draw_reason = None

    game.history = []
    game.position_counts = {}
    game._register_position()

    return game


def test_game_starts_with_white():
    game = CheckersGame()

    assert game.current_player == Board.WHITE
    assert game.status == "ongoing"
    assert game.winner is None


def test_turn_changes_after_move():
    game = create_game_with_empty_board()

    game.board.set_piece(5, 2, Board.WHITE)
    game.board.set_piece(2, 1, Board.BLACK)

    move = {
        "from": (5, 2),
        "to": (4, 3)
    }

    game.play_move(move)

    assert game.current_player == Board.BLACK
    assert game.board.get_piece(4, 3) == Board.WHITE
    assert len(game.history) == 1


def test_invalid_move_is_rejected():
    game = create_game_with_empty_board()

    game.board.set_piece(5, 2, Board.WHITE)

    invalid_move = {
        "from": (5, 2),
        "to": (2, 5)
    }

    try:
        game.play_move(invalid_move)
        assert False, "Deveria rejeitar o movimento inválido."
    except ValueError:
        pass

    assert game.current_player == Board.WHITE
    assert len(game.history) == 0


def test_player_wins_when_opponent_has_no_pieces():
    game = create_game_with_empty_board()

    game.board.set_piece(5, 0, Board.WHITE)

    move = {
        "from": (5, 0),
        "to": (4, 1)
    }

    game.play_move(move)

    assert game.status == "finished"
    assert game.winner == Board.WHITE
    assert game.is_over()


def test_get_result_during_game():
    game = CheckersGame()

    result = game.get_result()

    assert result["status"] == "ongoing"
    assert result["winner"] is None
