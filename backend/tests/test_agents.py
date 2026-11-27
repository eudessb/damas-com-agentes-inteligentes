
from src.game.board import Board
from src.game.game import CheckersGame
from src.agents.random_agent import RandomAgent


def test_random_agent_returns_legal_move():
    game = CheckersGame()
    agent = RandomAgent()

    move = agent.choose_move(game)

    assert move in game.get_legal_moves()


def test_random_agent_returns_none_when_no_moves():
    game = CheckersGame()

    # Cria uma situação sem movimentos para as brancas
    game.board.grid = [
        [Board.EMPTY for _ in range(8)]
        for _ in range(8)
    ]

    game.board.set_piece(0, 1, Board.WHITE)

    moves = game.get_legal_moves()

    agent = RandomAgent()
    move = agent.choose_move(game)

    assert moves == []
    assert move is None
