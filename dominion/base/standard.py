import typing as t

from .card import BaseCard

if t.TYPE_CHECKING:
    from ..deck import Deck
else:
    Deck = None  # pylint: disable=invalid-name
    PlayerTypes = None  # pylint: disable=invalid-name


class StandardCard(BaseCard):
    ...


class Village(StandardCard):
    name: str = "Village"

    @classmethod
    def effect(cls, deck: Deck) -> None:
        deck.actions_remaining += 2
        deck.coins_remaining += 1


class Smithy(StandardCard):
    name: str = "Smithy"

    @classmethod
    def effect(cls, deck: Deck) -> None:
        deck.draw(3)  # Should this trigger reactions or not?


class Laboratory(StandardCard):
    name: str = "Laboratory"

    @classmethod
    def effect(cls, deck: Deck) -> None:
        deck.draw(2)
        deck.actions_remaining += 1


class CouncilRoom(StandardCard):
    name: str = "Council Room"

    @classmethod
    def effect(cls, deck: Deck) -> None:
        deck.draw(4)
        deck.buys_remaining += 1
        for player in deck.game.players:
            player.deck.draw(1)


class Festival(StandardCard):
    name: str = "Festival"

    @classmethod
    def effect(cls, deck: Deck) -> None:
        deck.actions_remaining += 2
        deck.buys_remaining += 1
        deck.coins_remaining += 2


class Market(StandardCard):
    name: str ="Market"

    @classmethod
    def effect(cls, deck: Deck) -> None:
        deck.actions_remaining += 1
        deck.buys_remaining += 1
        deck.coins_remaining += 1
        deck.draw(1)
