import inspect
import io
import sys
import typing as t

from .cards import (
    Card,
    CardTypes,
    Copper,
    Curse,
    Duchy,
    Estate,
    Gold,
    Province,
    Reaction,
    Silver,
)
from .deck import Deck
from .event import Event
from .player import Player, PlayerTypes


class Game:
    trash_pile: CardTypes
    kingdom_cards: t.Dict[t.Type[Card], int]
    base_cards: t.Dict[t.Type[Card], int]
    players: t.List[Player]
    game_output: io.FileIO

    def __init__(
        self,
        players: PlayerTypes,
        kingdom_card_set: CardTypes,
        game_output: io.FileIO = sys.stdout,
    ):
        self.game_output = game_output
        self.trash_pile = []
        self.kingdom_cards = {card: card.setup(players) for card in kingdom_card_set}
        self.base_cards = {
            card: card.setup(players)
            for card in [Copper, Silver, Gold, Estate, Duchy, Province, Curse]
        }
        self.raw_log("The Supply is setup!")
        self.players = [player(Deck(self)) for player in players]
        self.raw_log("The players have been dealt!")

    @property
    def available_cards(self) -> t.List[t.Type[Card]]:
        return [card for card, count in self.base_cards.items() if count > 0] + [
            card for card, count in self.kingdom_cards.items() if count > 0
        ]

    @property
    def empty_supply_piles(self) -> t.List[t.Type[Card]]:
        return [card for card, count in self.base_cards.items() if count == 0] + [
            card for card, count in self.kingdom_cards.items() if count == 0
        ]

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
        self.log(player.deck, f"[{event.name}] {args} {kwargs}")
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
        self.raw_log(f"[{self.get_player(deck).player_id}] {message}")

    def raw_log(self, message: str):
        print(message, file=self.game_output)

    @property
    def ended(self) -> bool:
        if self.base_cards[Province] == 0:
            return True
        return len(self.empty_supply_piles) >= 3

    def play(self) -> None:
        break_flag = False
        while not break_flag:
            for player in self.players:
                player.action_phase()
                player.buy_phase()
                player.cleanup_phase()
                if self.ended:
                    break_flag = True
            if break_flag:
                break

