import typing as t

from .deck import Deck

if t.TYPE_CHECKING:
    from .game import Game


class Player:
    """Implements custom player input and strategy into the game."""
    deck: Deck

    def __init__(self, deck: Deck):
        self.deck = deck

    def turn(self, game: Game):
        pass


PlayerTypes = t.List[t.Type[Player]]
