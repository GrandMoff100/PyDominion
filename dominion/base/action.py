import copy
import typing as t

from .card import KingdomCard, Card

if t.TYPE_CHECKING:
    from ..deck import Deck
    from ..player import PlayerTypes
else:
    Deck = None  # pylint: disable=invalid-name
    PlayerTypes = None  # pylint: disable=invalid-name


class Action(KingdomCard):
    @classmethod
    def play(cls, deck: Deck) -> None:
        deck.discard(cls)
        cls.effect(deck)

    @classmethod
    def setup(cls, players: PlayerTypes) -> int:
        """How many of a card type to start with depending on how many players."""
        return 10


class Reaction(Action):
    @classmethod
    def when_draw(cls, deck: Deck, card: t.Type[Card]) -> None:
        pass

    @classmethod
    def when_buy(cls, deck: Deck, card: t.Type[Card]) -> None:
        pass

    @classmethod
    def when_trash(cls, deck: Deck, card: t.Type[Card]) -> None:
        pass

    @classmethod
    def when_discard(cls, deck: Deck, card: t.Type[Card]) -> None:
        pass

    @classmethod
    def when_gain(cls, deck: Deck, card: t.Type[Card]) -> None:
        pass

    @classmethod
    def when_attack(cls, deck: Deck, card: t.Type[Card], targets: PlayerTypes) -> None:
        pass

    @classmethod
    def when_reveal(cls, deck: Deck, card: t.Type[Card]) -> None:
        pass


class Attack(Action):
    @classmethod
    def play(cls, deck: Deck) -> None:
        deck.discard(cls)
        targets = copy.copy(deck.game.players)
        for player in deck.game.players:
            for card in player.hand:
                if isinstance(card, Reaction):
                    card.when_attack(player.deck, cls, targets)
        cls.effect(deck, targets)

    @classmethod
    def effect(cls, deck: Deck, targets: PlayerTypes) -> None:
        pass
