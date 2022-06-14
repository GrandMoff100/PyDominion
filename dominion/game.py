import inspect
import sys
import typing as t

from dominion.cards.action import Reaction
from dominion.cards.card import Card, CardTypes
from dominion.cards.curse import Curse
from dominion.cards.treasure import Copper, Gold, Silver, Treasure
from dominion.cards.victory import Duchy, Estate, Province
from dominion.deck import Deck
from dominion.errors import PlayerNotFoundError
from dominion.event import Event
from dominion.player import Player, Players, PlayerTypes
from dominion.report import Report


class Game:
    trash_pile: CardTypes
    kingdom_cards: t.Dict[t.Type[Card], int]
    base_cards: t.Dict[t.Type[Card], int]
    players: Players
    game_output: t.TextIO

    def __init__(
        self,
        players: PlayerTypes,
        kingdom_card_set: CardTypes,
        game_output: t.TextIO = sys.stdout,
        log_events: bool = False,
    ):
        self.log_events = log_events
        self.game_output = game_output
        self.trash_pile = []
        self.players = [player(Deck(self)) for player in players]
        self.out("[INIT] The players have been dealt!")
        self.kingdom_cards = {
            card: card.setup(self.players) for card in kingdom_card_set
        }
        self.base_cards = {
            card: card.setup(self.players)
            for card in [Copper, Silver, Gold, Estate, Duchy, Province, Curse]
        }
        self.out("[INIT] The Supply is setup!")

    @property
    def supply(self) -> t.Dict[t.Type[Card], int]:
        return dict(tuple(self.kingdom_cards.items()) + tuple(self.base_cards.items()))

    @property
    def available_cards(self) -> t.List[t.Type[Card]]:
        return [card for card, count in self.supply.items() if count > 0]

    @property
    def empty_supply_piles(self) -> t.List[t.Type[Card]]:
        return [card for card, count in self.base_cards.items() if count == 0] + [
            card for card, count in self.kingdom_cards.items() if count == 0
        ]

    def get_player(self, deck: Deck) -> Player:
        for player in self.players:
            if player.deck == deck:
                return player
        raise PlayerNotFoundError("This deck does not belong to a player!")

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
                card,
                f"Activate your {card.name} in response to the {card.name}?",
                [True, False],
            ):
                reaction_events[event](player.deck, card, *args, **kwargs)  # type: ignore[operator]

    def dispatch_event(self, deck: Deck, event: Event, *args, **kwargs) -> None:
        for player in deck.game.players:
            for hand_card in player.deck.hand:
                if issubclass(hand_card, Reaction):
                    self.call_reaction_effect(player, hand_card, event, *args, **kwargs)

    @property
    def ended(self) -> bool:
        if self.base_cards[Province] == 0:
            return True
        return len(self.empty_supply_piles) >= 3

    def play(self) -> Report:
        break_flag = False
        while not break_flag:
            for player in self.players:
                player.display_hand()
                player.action_phase()
                for card in player.deck.hand:
                    if issubclass(card, Treasure):
                        card.effect(player.deck)
                player.buy_phase()
                player.cleanup_phase()
                if self.ended:
                    break_flag = True
                    break
            if break_flag:
                break
        return Report(self)

    def log(self, deck: Deck, message: str, *args, **kwargs) -> None:
        self.out(f"[{self.get_player(deck).player_id}] {message}", *args, **kwargs)

    def out(self, *args, **kwargs) -> None:
        if self.log_events:
            return print(*args, **kwargs, file=self.game_output)  # type: ignore[arg-type]
        return None
