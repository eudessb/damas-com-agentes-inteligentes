import random

from .base_agent import BaseAgent


class RandomAgent(BaseAgent):
    def __init__(self):
        super().__init__("Random Agent")

    def choose_move(self, game):
        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return None

        return random.choice(legal_moves)
