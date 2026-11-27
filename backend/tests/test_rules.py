from src.game.board import Board
from src.game.rules import (
    get_simple_moves,
    get_capture_moves,
    get_multiple_capture_moves,
    get_legal_moves
)

def test_initial_white_moves():
    board = Board()

    moves = get_simple_moves(board, Board.WHITE)

    assert len(moves) == 7


def test_initial_black_moves():
    board = Board()

    moves = get_simple_moves(board, Board.BLACK)

    assert len(moves) == 7


def test_white_moves_forward():
    board = Board()

    moves = get_simple_moves(board, Board.WHITE)

    for move in moves:
        origin_row = move["from"][0]
        destination_row = move["to"][0]

        assert destination_row < origin_row


def test_black_moves_forward():
    board = Board()

    moves = get_simple_moves(board, Board.BLACK)

    for move in moves:
        origin_row = move["from"][0]
        destination_row = move["to"][0]

        assert destination_row > origin_row

def test_white_capture():
    board = Board()

    # Limpa o tabuleiro
    board.grid = [
        [Board.EMPTY for _ in range(8)]
        for _ in range(8)
    ]

    # Posiciona as peças
    board.set_piece(5, 2, Board.WHITE)
    board.set_piece(4, 3, Board.BLACK)

    moves = get_capture_moves(board, Board.WHITE)

    assert len(moves) == 1

    assert moves[0]["from"] == (5, 2)
    assert moves[0]["to"] == (3, 4)
    assert moves[0]["capture"] == (4, 3)


def test_black_capture():
    board = Board()

    board.grid = [
        [Board.EMPTY for _ in range(8)]
        for _ in range(8)
    ]

    board.set_piece(2, 3, Board.BLACK)
    board.set_piece(3, 4, Board.WHITE)

    moves = get_capture_moves(board, Board.BLACK)

    assert len(moves) == 1

    assert moves[0]["from"] == (2, 3)
    assert moves[0]["to"] == (4, 5)
    assert moves[0]["capture"] == (3, 4)


def test_capture_requires_empty_destination():
    board = Board()

    board.grid = [
        [Board.EMPTY for _ in range(8)]
        for _ in range(8)
    ]

    board.set_piece(5, 2, Board.WHITE)
    board.set_piece(4, 3, Board.BLACK)
    board.set_piece(3, 4, Board.WHITE)

    moves = get_capture_moves(board, Board.WHITE)

    assert len(moves) == 0

def test_multiple_capture_sequence():
    board = Board()
    board.grid = [
        [Board.EMPTY for _ in range(8)]
        for _ in range(8)
    ]

    board.set_piece(5, 0, Board.WHITE)
    board.set_piece(4, 1, Board.BLACK)
    board.set_piece(2, 3, Board.BLACK)

    sequences = get_multiple_capture_moves(
        board, 5, 0, Board.WHITE
    )

    assert len(sequences) == 1
    assert len(sequences[0]) == 2

    assert sequences[0][0]["to"] == (3, 2)
    assert sequences[0][1]["to"] == (1, 4)

    # A função deve preservar o tabuleiro original
    assert board.get_piece(5, 0) == Board.WHITE
    assert board.get_piece(4, 1) == Board.BLACK
    assert board.get_piece(2, 3) == Board.BLACK

def test_capture_is_mandatory():
    board = Board()
    board.grid = [
        [Board.EMPTY for _ in range(8)]
        for _ in range(8)
    ]

    board.set_piece(5, 0, Board.WHITE)
    board.set_piece(4, 1, Board.BLACK)

    # Outra peça branca possui movimento simples
    board.set_piece(5, 4, Board.WHITE)

    moves = get_legal_moves(board, Board.WHITE)

    assert len(moves) == 1
    assert len(moves[0]) == 1
    assert moves[0][0]["capture"] == (4, 1)

def test_must_choose_maximum_capture():
    board = Board()
    board.grid = [
        [Board.EMPTY for _ in range(8)]
        for _ in range(8)
    ]

    # Primeira peça branca consegue capturar uma peça
    board.set_piece(5, 0, Board.WHITE)
    board.set_piece(4, 1, Board.BLACK)

    # Segunda peça branca consegue capturar duas peças
    board.set_piece(5, 4, Board.WHITE)
    board.set_piece(4, 5, Board.BLACK)
    board.set_piece(2, 5, Board.BLACK)

    moves = get_legal_moves(board, Board.WHITE)

    assert len(moves) == 1
    assert len(moves[0]) == 2

def test_simple_moves_when_no_capture_exists():
    board = Board()
    board.grid = [
        [Board.EMPTY for _ in range(8)]
        for _ in range(8)
    ]

    board.set_piece(5, 2, Board.WHITE)

    moves = get_legal_moves(board, Board.WHITE)

    assert len(moves) == 2

    for move in moves:
        assert "capture" not in move
