from abc import ABC, abstractmethod


class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def choose_move(self, game):
        """
        Recebe uma partida e retorna um movimento legal.
        """
        pass

    def __str__(self):
        return self.name
