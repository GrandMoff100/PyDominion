import typing as t

if t.TYPE_CHECKING:
    from ..deck import Deck
    from ..player import PlayerTypes
else:
    Deck = None  # pylint: disable=invalid-name
    PlayerTypes = None  # pylint: disable=invalid-name


class Card:
    cost: int = 0
    name: str = "Blank Card"

    @classmethod
    def buy(cls, deck: Deck) -> None:
        if deck.coins >= cls.cost:
            deck.coins -= cls.cost
            deck.discard.append(cls)
        else:
            raise ValueError(f"You does not have enough coins to buy the {cls.name}")

    @classmethod
    def play(cls, deck: Deck) -> None:
        """Logs that this card was played."""
        deck.game.log(f"[{deck.game.get_player(deck).player_id}] Played a {cls.name}")

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """A method to implement card effects for Card subclasses"""
        raise NotImplementedError

    @classmethod
    def setup(cls, players: PlayerTypes) -> int:  # pylint: disable=unused-argument
        """How many of a card type to start with depending on how many players."""
        return 0


class BaseCard(Card):  # pylint: disable=abstract-method
    pass


class KingdomCard(Card):  # pylint: disable=abstract-method
    @classmethod
    def setup(cls, players: PlayerTypes) -> int:
        """How many of a card type to start with depending on how many players."""
        return 10


CardTypes = t.List[t.Type[Card]]
