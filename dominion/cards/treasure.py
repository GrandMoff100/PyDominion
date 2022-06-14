import typing as t

from .card import BaseCard

if t.TYPE_CHECKING:
    from ..deck import Deck
    from ..player import Players
else:
    Deck = None  # pylint: disable=invalid-name
    Players = None  # pylint: disable=invalid-name


class Treasure(BaseCard):  # pylint: disable=abstract-method
    pass


class Copper(Treasure):
    name: str = "Copper"

    @classmethod
    def effect(cls, deck: Deck) -> None:
        deck.coins += 1

    @classmethod
    def setup(cls, players: Players) -> int:
        """How many of a card type to start with depending on how many players."""
        return 60


class Silver(Treasure):
    name: str = "Silver"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        deck.coins += 2

    @classmethod
    def setup(cls, players: Players) -> int:
        """How many of a card type to start with depending on how many players."""
        return 40


class Gold(Treasure):
    name: str = "Gold"
    cost: int = 6

    @classmethod
    def effect(cls, deck: Deck) -> None:
        deck.coins += 3

    @classmethod
    def setup(cls, players: Players) -> int:
        """How many of a card type to start with depending on how many players."""
        return 30
