"""Module defining the Kingdom Cards for Dominion (First Edition)"""
import typing as t

from ..base import Action, Card, Victory, KingdomCard, Reaction
from ..deck import Deck
from ..player import PlayerTypes


class Cellar(Action):
    name: str = "Cellar"
    cost: int = 2

    @classmethod
    def effect(cls, deck: Deck, cards: t.List[Card]) -> None:
        "+1 Action, Discard any number of cards, then draw that many."
        deck.actions += 1
        deck.discard(cards)
        deck.draw(len(cards))


class Chapel(Action):
    name: str = "Chapel"
    cost: int = 2

    @classmethod
    def effect(cls, deck: Deck, cards: t.List[Card]) -> None:
        "Trash up to 4 cards from your hand"
        if len(cards) <= 4:
            for card in cards:
                if card in deck.hand:
                    deck.trash(deck.hand.pop(deck.hand.index(card)))
                else:
                    raise ValueError(
                        f"Cannot trash the {card.name}, it is not in your hand."
                    )
        else:
            raise ValueError(f"Cannot trash more than four cards with the {cls.name}")


class Moat(Reaction):
    name: str = "Moat"
    cost: int = 2

    @classmethod
    def effect(cls, deck: Deck) -> None:
        "+2 Cards"
        deck.draw(2)

    @classmethod
    def when_attack(cls, deck: Deck, card: t.Type[Card], targets: PlayerTypes) -> None:
        "When another player plays an Attack card, you can first reveal this card and then be unaffected by it."
        player = deck.game.player_lookup(deck)
        if player.reveal(cls):
            targets.remove(player)


class Chancellor:
    name: str = "Chancellor"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        "+2 Coins, You may immediately put your deck in the discard pile."
        deck.coins += 2


class Village(Action):
    name: str = "Village"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        "+1 Card, +2 Actions"
        deck.draw()
        deck.actions += 2


class Woodcutter:
    @classmethod
    def effect(cls, deck: Deck) -> None:
        "+1 Buy, +2 Coins"
        deck.buys += 1
        deck.coins += 2


class Workshop:
    @classmethod
    def effect(cls, deck: Deck) -> None:
        "Gain a card costing up to four coins."


class Bureaucrat:
    pass


class Gardens(Victory, KingdomCard):
    name: str = "Gardens"
    cost: int = 4

    @classmethod
    def points(cls, deck: Deck) -> int:
        return len(deck.cards) // 10


class Militia:
    pass


class Moneylender:
    pass


class Feast:
    pass


class Remodel:
    pass


class Smithy:
    pass


class Spy:
    pass


class Thief:
    pass


class ThroneRoom:
    pass


class CouncilRoom:
    pass


class Festival:
    pass


class Laboratory:
    pass


class Library:
    pass


class Market:
    pass


class Mine:
    pass


class Witch:
    pass


class Adventurer:
    pass
