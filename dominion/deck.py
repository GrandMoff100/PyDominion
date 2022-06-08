import random
import typing as t

from .player import Player
from .base import Card, CardTypes, Copper, Curse, Estate, Victory
from .event import Event

if t.TYPE_CHECKING:
    from .game import Game
else:
    Game = None  # pylint: disable=invalid-name


class Deck:
    draw_pile: CardTypes
    discard_pile: CardTypes
    hand: CardTypes
    buys: int
    actions: int
    coins: int
    game: Game

    def __init__(self, game: Game):
        self.game = game
        self.hand = []
        self.discard_pile = []
        self.buys = 0
        self.actions = 0
        self.coins = 0
        self.draw_pile = [
            Copper,
            Copper,
            Copper,
            Copper,
            Copper,
            Copper,
            Copper,
            Estate,
            Estate,
            Estate,
        ]
        random.shuffle(self.draw_pile)
        self.draw(5, trigger_reactions=False)

    def cleanup(self) -> None:
        self.discard(self.hand, trigger_reactions=False)
        self.draw(5)

    def discard(self, cards: CardTypes, trigger_reactions: bool = True) -> None:
        for card in cards:
            if trigger_reactions:
                self.game.dispatch_event(self, Event.DISCARD_EVENT, card)
            if card not in self.hand:
                raise ValueError(
                    f"Cannot discard this {card.__qualname__}, it is not in your hand."
                )
            self.discard_pile.insert(0, self.hand.pop(self.hand.index(card)))

    def gain(self, card: t.Type[Card]) -> None:
        self.game.dispatch_event(self, Event.GAIN_EVENT, card)
        self.discard_pile.append(card)

    def gain_to_hand(self, card: t.Type[Card]) -> None:
        self.game.dispatch_event(self, Event.GAIN_EVENT, card)
        self.hand.append(card)

    def trash(self, card: t.Type[Card]) -> None:
        self.game.dispatch_event(self, Event.TRASH_EVENT, card)
        self.game.trash_pile.append(card)

    @property
    def cards(self) -> CardTypes:
        return self.draw_pile + self.discard_pile + self.hand

    def draw(self, amount: int = 1, trigger_reactions: bool = True) -> CardTypes:
        if trigger_reactions:
            for _ in range(amount):
                if not self.draw_pile:
                    self.shuffle()
                self.hand.append(card := self.draw_pile.pop(0))
                self.game.dispatch_event(self, Event.DRAW_EVENT, card)
            return self.hand[len(self.hand) - amount : len(self.hand)]
        return []

    def reveal(self, card: t.Type[Card]) -> t.Type[Card]:
        if card in self.hand:
            self.game.log(
                f"{self.game.get_player(self).player_id!r} revealed a {card.name}"
            )
            self.game.dispatch_event(self, Event.REVEAL_EVENT, card)
            return card
        else:
            raise ValueError(f"Cannot reveal {card.name}, it is not in your hand.")

    def shuffle(self) -> None:
        self.draw_pile += random.sample(self.discard, len(self.discard))
        self.discard_pile = []

    @property
    def player(self) -> t.Optional[Player]:
        return self.game.get_player(self)

    @property
    def score(self):
        return sum(
            [
                card.points(self)
                for card in self.cards
                if issubclass(card, (Victory, Curse))
            ]
        )
