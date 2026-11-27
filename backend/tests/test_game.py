
from src.game.board import Board
from src.game.game import apply_move


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
