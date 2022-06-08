"""Module defining the Kingdom Cards for Dominion (First Edition)"""
import typing as t

from ..base import Action, Attack, Card, KingdomCard, Reaction, Silver, Victory
from ..deck import Deck
from ..player import Player, PlayerTypes

__all__ = (
    "Cellar",
    "Chapel",
    "Moat",
    "Chancellor",
    "Village",
    "Woodcutter",
    "Workshop",
    "Bureaucrat",
    "Gardens",
    "Militia",
    "Moneylender",
    "Feast",
    "Remodel",
    "Smithy",
    "Spy",
    "Thief",
    "ThroneRoom",
    "CouncilRoom",
    "Festival",
    "Laboratory",
    "Library",
    "Market",
    "Mine",
    "Witch",
    "Adventurer",
)


class Cellar(Action):
    name: str = "Cellar"
    cost: int = 2

    @classmethod
    def effect(cls, deck: Deck, cards: t.List[Card]) -> None:
        """
        +1 Action
        Discard any number of cards, then draw that many.
        """
        deck.actions += 1
        deck.discard(cards)
        deck.draw(len(cards))


class Chapel(Action):
    name: str = "Chapel"
    cost: int = 2

    @classmethod
    def effect(cls, deck: Deck, cards: t.List[Card]) -> None:
        """Trash up to 4 cards from your hand"""
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
        """
        +2 Cards
        """
        deck.draw(2)

    @classmethod
    def when_attack(cls, deck: Deck, card: t.Type[Card], targets: PlayerTypes) -> None:
        """
        When another player plays an Attack card,
        you can first reveal this card and then be unaffected by it.
        """
        player = deck.game.get_player(deck)
        if player.reveal(cls):
            targets.remove(player)


class Chancellor(Action):
    name: str = "Chancellor"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +2 Coins
        You may immediately put your deck in the discard pile.
        """
        deck.coins += 2
        if (
            deck.game.get_player(deck).choice(
                "You may immediately put your deck in the discard pile:",
                ["Yes", "No"],
            )
            == "Yes"
        ):
            deck.discard_pile += deck.draw_pile
            deck.draw_pile = []


class Village(Action):
    name: str = "Village"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +1 Card
        +2 Actions
        """
        deck.draw()
        deck.actions += 2


class Woodcutter(Action):
    name: str = "Woodcutter"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +1 Buy
        +2 Coins
        """
        deck.buys += 1
        deck.coins += 2


class Workshop(Action):
    name: str = "Workshop"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """Gain a card costing up to four coins."""
        deck.game.get_player(deck).choice(
            "Gain a card costing up to four coins:",
            [card for card in deck.game.available_cards if card.cost <= 4],
        )


class Bureaucrat(Attack):
    name: str = "Bureaucrat"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        Gain a Silver onto your deck.
        Each other player reveals a Victory card from their hand and
        puts it onto their deck (or reveals a hand with no Victory cards).
        """
        deck.draw_pile.insert(0, Silver)
        for player in deck.game.players:
            for card in player.deck.hand:
                if issubclass(card, Victory):
                    player.deck.insert(0, card)
                    break


class Gardens(Victory, KingdomCard):
    name: str = "Gardens"
    cost: int = 4

    @classmethod
    def points(cls, deck: Deck) -> int:
        """Worth 1 Victory Point for every 10 cards in your deck (rounded down)."""
        return len(deck.cards) // 10


class Militia(Attack):
    name: str = "Militia"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck, targets: t.List[Player]) -> None:
        """
        +2 Coins
        Each other player discards down to 3 cards in their hand.
        """
        deck.coins += 2
        for player in targets:
            for _ in range(max([3, len(player.deck.hand)]) - 3):
                player.deck.discard(
                    player.choice(
                        "Choose one card from your hand to discard",
                        player.deck.hand,
                    )
                )


class Moneylender(Action):
    name: str = "Moneylender"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck) -> None:
        pass


class Feast(Action):
    name: str = "Feast"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck) -> None:
        pass


class Remodel(Action):
    name: str = "Remodel"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck) -> None:
        pass


class Smithy(Action):
    name: str = "Smithy"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck) -> None:
        pass


class Spy(Attack):
    name: str = "Spy"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck, targets: t.List[Player]) -> None:
        pass


class Thief(Attack):
    name: str = "Thief"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck, targets: t.List[Player]) -> None:
        pass


class ThroneRoom(Action):
    name: str = "Throne Room"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck) -> None:
        pass


class CouncilRoom(Action):
    name: str = "Council Room"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck) -> None:
        pass


class Festival(Action):
    name: str = "Festival"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck) -> None:
        pass


class Laboratory(Action):
    name: str = "Laboratory"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck) -> None:
        pass


class Library(Action):
    name: str = "Library"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck) -> None:
        pass


class Market(Action):
    name: str = "Market"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck) -> None:
        pass


class Mine(Action):
    name: str = "Mine"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck) -> None:
        pass


class Witch(Attack):
    name: str = "Witch"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck, targets: t.List[Player]) -> None:
        pass


class Adventurer(Action):
    name: str = "Adventurer"
    cost: int = 6

    @classmethod
    def effect(cls, deck: Deck) -> None:
        pass
