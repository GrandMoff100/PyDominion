import typing as t

from dominion.errors import (
    EmptySupplyPileError,
    NoActionsAvailableError,
    UnaffordableError,
)

if t.TYPE_CHECKING:
    from ..deck import Deck
    from ..player import Players
else:
    Deck = None  # pylint: disable=invalid-name
    Players = None  # pylint: disable=invalid-name


class Card:
    cost: int = 0
    name: str = "Blank Card"

    @classmethod
    def buy(cls, deck: Deck) -> None:
        if deck.buys <= 0:
            raise NoActionsAvailableError("You have no buys left.")
        if cls in deck.game.kingdom_cards:
            if deck.game.kingdom_cards[cls] <= 0:
                raise EmptySupplyPileError(f"Cannot buy a {cls.name}, none are left.")
            deck.game.kingdom_cards[cls] -= 1
        elif cls in deck.game.base_cards:
            if deck.game.base_cards[cls] <= 0:
                raise EmptySupplyPileError(f"Cannot buy a {cls.name}, none are left.")
            deck.game.base_cards[cls] -= 1
        if deck.coins >= cls.cost:
            deck.coins -= cls.cost
            deck.buys -= 1
            deck.discard_pile.append(cls)
            deck.game.log(deck, "You bought the", cls.name)
        else:
            raise UnaffordableError(f"You cannot afford to buy a {cls.name}")

    @classmethod
    def play(cls, deck: Deck) -> None:
        """Logs that this card was played."""
        deck.game.log(
            deck,
            f"[{deck.game.get_player(deck).player_id}] Played a {cls.name}",
        )

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """A method to implement card effects for Card subclasses"""
        raise NotImplementedError

    @classmethod
    def setup(cls, players: Players) -> int:  # pylint: disable=unused-argument
        """How many of a card type to start with depending on how many players."""
        return 0


class BaseCard(Card):  # pylint: disable=abstract-method
    pass


class KingdomCard(Card):  # pylint: disable=abstract-method
    @classmethod
    def setup(cls, players: Players) -> int:
        """How many of a card type to start with depending on how many players."""
        return 10


CardTypes = t.List[t.Type[Card]]
