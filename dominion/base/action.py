import copy
import typing as t
from abc import abstractmethod

from ..event import Event
from .card import Card, KingdomCard

if t.TYPE_CHECKING:
    from ..deck import Deck
    from ..player import PlayerTypes
else:
    Deck = None  # pylint: disable=invalid-name
    PlayerTypes = None  # pylint: disable=invalid-name


class Action(KingdomCard):
    @classmethod
    def play(cls, deck: Deck) -> None:
        super(cls, Card).play(deck)
        deck.discard(cls)
        cls.effect(deck)

    @classmethod
    def setup(cls, players: PlayerTypes) -> int:
        """How many of a card type to start with depending on how many players."""
        return 10


class Reaction(Action):
    @classmethod
    @abstractmethod
    def when_draw(cls, deck: Deck, card: t.Type[Card]) -> None:
        """Abstract Reaction effects when a player draws a card."""

    @classmethod
    @abstractmethod
    def when_buy(cls, deck: Deck, card: t.Type[Card]) -> None:
        """Abstract Reaction effects when a player buys a card."""

    @classmethod
    @abstractmethod
    def when_trash(cls, deck: Deck, card: t.Type[Card]) -> None:
        """Abstract Reaction effects when a player trashs a card."""

    @classmethod
    @abstractmethod
    def when_discard(cls, deck: Deck, card: t.Type[Card]) -> None:
        """Abstract Reaction effects when a player discards a card."""

    @classmethod
    @abstractmethod
    def when_gain(cls, deck: Deck, card: t.Type[Card]) -> None:
        """Abstract Reaction effects when a player gains a card."""

    @classmethod
    @abstractmethod
    def when_attack(cls, deck: Deck, card: t.Type[Card], targets: PlayerTypes) -> None:
        """Abstract Reaction effects when a player plays an attack card."""

    @classmethod
    @abstractmethod
    def when_reveal(cls, deck: Deck, card: t.Type[Card]) -> None:
        """Abstract Reaction effects when a player reveals a card."""


class Attack(Action):
    @classmethod
    def play(cls, deck: Deck) -> None:
        super(cls, Card).play(deck)
        deck.discard(cls)
        targets = copy.copy(deck.game.players)
        deck.game.dispatch_event(deck, Event.ATTACK_EVENT, cls, targets)
        cls.effect(deck, targets)

    @classmethod
    @abstractmethod
    def effect(cls, deck: Deck, targets: PlayerTypes) -> None:
        """Abstract method for attack effects on players."""
