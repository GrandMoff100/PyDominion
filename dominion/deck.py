import random
import typing as t

from dominion.cards.card import Card, CardTypes
from dominion.cards.curse import Curse
from dominion.cards.treasure import Copper
from dominion.cards.victory import Estate, Victory
from dominion.errors import CardNotFoundError
from dominion.event import Event
from dominion.player import Player

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
        self.buys = 1
        self.actions = 1
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
        self.draw(5, trigger_reactions=False)

    def discard(self, cards: CardTypes, trigger_reactions: bool = True) -> None:
        for card in list(cards):
            if card not in self.hand:
                raise CardNotFoundError(
                    f"Cannot discard this {card.name}, it is not in your hand."
                )
            if trigger_reactions:
                self.game.dispatch_event(self, Event.DISCARD_EVENT, card)
                self.game.log(self, "You discarded", card.name)
            self.discard_pile.insert(0, self.hand.pop(self.hand.index(card)))

    def gain(self, card: t.Type[Card], trigger_reactions: bool = True) -> t.Type[Card]:
        if trigger_reactions:
            self.game.dispatch_event(self, Event.GAIN_EVENT, card)
            self.game.log(self, "You gained a", card.name)
        self.discard_pile.append(card)
        return card

    def gain_to_hand(
        self, card: t.Type[Card], trigger_reactions: bool = True
    ) -> t.Type[Card]:
        if trigger_reactions:
            self.game.dispatch_event(self, Event.GAIN_EVENT, card)
            self.game.log(self, "You gained a", card.name, "to your hand.")
        self.hand.append(card)
        return card

    def trash(self, card: t.Type[Card], trigger_reactions: bool = True) -> t.Type[Card]:
        if trigger_reactions:
            self.game.dispatch_event(self, Event.TRASH_EVENT, card)
            self.game.log(self, "You trashed a", card.name)
        self.game.trash_pile.append(card)
        return card

    @property
    def cards(self) -> CardTypes:
        return self.draw_pile + self.discard_pile + self.hand

    def draw(self, amount: int = 1, trigger_reactions: bool = True) -> CardTypes:
        for _ in range(amount):
            if not self.draw_pile:
                self.shuffle()
            card = self.draw_pile.pop(0)
            if trigger_reactions:
                self.game.dispatch_event(self, Event.DRAW_EVENT, card)
                self.game.log(self, "You drew a", card.name)
            self.hand.append(card)
        return self.hand[len(self.hand) - amount : len(self.hand)]

    def reveal(self, card: t.Type[Card]) -> t.Type[Card]:
        if card in self.hand:
            self.game.dispatch_event(self, Event.REVEAL_EVENT, card)
            self.game.log(
                self, f"{self.game.get_player(self).player_id!r} revealed a {card.name}"
            )
            return card
        raise CardNotFoundError(f"Cannot reveal {card.name}, it is not in your hand.")

    def shuffle(self) -> None:
        self.draw_pile += random.sample(self.discard_pile, len(self.discard_pile))
        self.discard_pile = []

    @property
    def player(self) -> Player:
        return self.game.get_player(self)

    @property
    def score(self):
        return sum(
            card.points(self)
            for card in self.cards
            if issubclass(card, (Victory, Curse))
        )
