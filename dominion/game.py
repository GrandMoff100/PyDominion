import copy
import io
import inspect
import sys
import typing as t

from dominion.base.action import Reaction

from .base import Card, CardTypes, Copper, Curse, Duchy, Estate, Gold, Province, Silver
from .deck import Deck
from .player import Player, PlayerTypes
from .event import Event


class Game:
    trash_pile: CardTypes
    kingdom_cards: t.Dict[t.Type[Card], int]
    base_cards: t.Dict[t.Type[Card], int]
    players: t.List[Player]
    gamelog: io.FileIO

    def __init__(
        self,
        players: PlayerTypes,
        kingdom_card_set: CardTypes,
        gamelog: io.FileIO = sys.stdout,
    ):
        self.gamelog = gamelog
        self.players = [player(Deck(self)) for player in players]
        self.trash_pile = []
        self.kingdom_cards = {card: card.setup(players) for card in kingdom_card_set}
        self.base_cards = {
            card: card.setup(players)
            for card in [Copper, Silver, Gold, Estate, Duchy, Province, Curse]
        }

    @property
    def available_cards(self) -> t.List[t.Type[Card]]:
        return [card for card, count in self.base_cards.items() if count > 0] + [
            card for card, count in self.kingdom_cards.items() if count > 0
        ]

    @property
    def current_player(self) -> t.Type[Player]:
        return self.players[0]

    def get_player(self, deck: Deck) -> t.Optional[Player]:
        for player in self.players:
            if player.deck == deck:
                return player
        return None

    def call_reaction_effect(
        self,
        player: Player,
        card: t.Type[Reaction],
        event: Event,
        *args,
        **kwargs,
    ) -> None:
        reaction_events = {
            Event.DRAW_EVENT: card.when_draw,
            Event.BUY_EVENT: card.when_buy,
            Event.TRASH_EVENT: card.when_trash,
            Event.DISCARD_EVENT: card.when_discard,
            Event.GAIN_EVENT: card.when_gain,
            Event.ATTACK_EVENT: card.when_attack,
            Event.REVEAL_EVENT: card.when_reveal,
        }
        if not inspect.isabstract(reaction_events[event]):
            if player.choice(
                f"Activate your {card.name} to the {card.name}?",
                [True, False],
            ):
                reaction_events[event](player.deck, card, *args, **kwargs)

    def dispatch_event(self, deck: Deck, event: Event, *args, **kwargs) -> None:
        for player in deck.game.players:
            for hand_card in player.hand:
                if issubclass(hand_card, Reaction):
                    self.call_reaction_effect(player, hand_card, event, *args, **kwargs)

    def log(self, deck: Deck, message: str) -> None:
        print(f"[{self.get_player(deck).player_id}] {message}", file=self.gamelog)

    @property
    def ended(self) -> bool:
        if self.base_cards[Province] == 0:
            return True
        empty_piles = [
            card for card, count in self.kingdom_cards.items() if count == 0
        ] + [card for card, count in self.base_cards.items() if count == 0]
        return len(empty_piles) >= 3
