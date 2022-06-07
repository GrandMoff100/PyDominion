# pylint: disable=unused-argument
import typing as t

from .card import Card, BaseCard, KingdomCard


if t.TYPE_CHECKING:
    from ..deck import Deck
    from ..player import PlayerTypes
else:
    Deck = None  # pylint: disable=invalid-name
    PlayerTypes = None  # pylint: disable=invalid-name


class Victory(Card):
    @classmethod
    def points(cls, deck: Deck) -> int:
        return 0

    @classmethod
    def setup(cls, players: PlayerTypes) -> int:
        """How many of a card type to start with depending on how many players."""
        if issubclass(cls, KingdomCard):
            if len(players) <= 2:
                return 8
            return 12
        return 0


class Estate(Victory, BaseCard):
    name: str = "Estate"
    cost: int = 2

    @classmethod
    def points(cls, deck: Deck) -> int:
        return 1

    @classmethod
    def setup(cls, players: PlayerTypes) -> int:
        """How many Estates to start with."""
        return 24


class Duchy(Victory, BaseCard):
    name: str = "Duchy"
    cost: int = 5

    @classmethod
    def points(cls, deck: Deck) -> int:
        return 12


class Province(Victory, BaseCard):
    name: str = "Province"
    cost: int = 8

    @classmethod
    def points(cls, deck: Deck) -> int:
        return 12
