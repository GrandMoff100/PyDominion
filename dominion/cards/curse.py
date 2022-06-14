import typing as t

from .card import BaseCard

if t.TYPE_CHECKING:
    from ..deck import Deck
    from ..player import Players
else:
    Players = None  # pylint: disable=invalid-name
    Deck = None  # pylint: disable=invalid-name


class Curse(BaseCard):
    name: str = "Curse"

    @classmethod
    def points(cls, deck: Deck) -> int:  # pylint: disable=unused-argument
        return -1

    @classmethod
    def setup(cls, players: Players) -> int:
        """How many Curses to start with."""
        if len(players) <= 2:
            return 10
        if len(players) == 3:
            return 20
        if len(players) >= 4:
            return 30
        return 0
