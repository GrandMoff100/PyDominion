import typing as t

import random

from .base import Card, Copper, Estate, Victory, Curse, CardTypes


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
        self.draw(5)

    def cleanup(self) -> None:
        self.discard(self.hand)
        self.draw(5)

    def discard(self, cards: CardTypes) -> None:
        for card in cards:
            if card not in self.hand:
                raise ValueError(
                    f"Cannot discard this {card.__qualname__}, it is not in your hand."
                )
            self.discard_pile.insert(0, self.hand.pop(self.hand.index(card)))

    def gain(self, card: t.Type[Card]) -> None:
        self.discard_pile.append(card)

    def trash(self, card: t.Type[Card]) -> None:
        self.game.trash_pile.append(card)

    @property
    def cards(self) -> CardTypes:
        return self.draw_pile + self.discard_pile + self.hand

    def draw(self, amount: int = 1) -> CardTypes:
        for _ in range(amount):
            if not self.draw_pile:
                self.shuffle()
            self.hand.append(self.draw_pile.pop(0))
        return self.hand[len(self.hand) - amount : len(self.hand)]

    def shuffle(self) -> None:
        self.draw_pile += random.sample(self.discard, len(self.discard))
        self.discard_pile = []

    @property
    def score(self):
        return sum(
            [
                card.points(self)
                for card in self.cards
                if issubclass(card, (Victory, Curse))
            ]
        )
