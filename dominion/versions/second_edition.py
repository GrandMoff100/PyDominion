"""Module defining the Kingdom Cards for Dominion (Second Edition)"""
from ..base import Action, Attack
from ..deck import Deck
from .first_edition import (
    Bureaucrat,
    Cellar,
    Chapel,
    CouncilRoom,
    Festival,
    Gardens,
    Laboratory,
    Library,
    Market,
    Militia,
    Mine,
    Moat,
    Moneylender,
    Remodel,
    Smithy,
    ThroneRoom,
    Village,
    Witch,
    Workshop,
)

__all__ = (
    "Cellar",
    "Chapel",
    "Moat",
    "Harbinger",
    "Merchant",
    "Vassal",
    "Village",
    "Workshop",
    "Bureaucrat",
    "Gardens",
    "Militia",
    "Moneylender",
    "Poacher",
    "Remodel",
    "Smithy",
    "ThroneRoom",
    "Bandit",
    "CouncilRoom",
    "Festival",
    "Laboratory",
    "Library",
    "Market",
    "Mine",
    "Sentry",
    "Witch",
    "Artisan",
)


class Harbinger(Action):
    name: str = "Harbinger"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +1 Card
        +1 Action
        Look through your discard pile.
        You may put a card from it onto your deck.
        """
        deck.draw()
        deck.actions += 1
        if deck.discard_pile:
            if chosen_card := deck.game.get_player(deck).choice(
                "What card from your discard pile do you choose?",
                deck.discard_pile + [None],
            ):
                deck.discard_pile.remove(chosen_card)
                deck.draw_pile.insert(0, chosen_card)


class Merchant(Action):
    name: str = "Merchant"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +1 Card
        +1 Action
        The first time you play a Silver this turn +1 Coin
        """
        deck.draw()
        deck.actions += 1


class Vassal(Action):
    name: str = "Vassal"
    cost: int = 3


class Poacher(Action):
    name: str = "Poacher"
    cost: int = 3


class Bandit(Attack):
    name: str = "Bandit"
    cost: int = 5


class Sentry(Action):
    name: str = "Sentry"
    cost: int = 5


class Artisan(Action):
    name: str = "Artisan"
    cost: int = 6
