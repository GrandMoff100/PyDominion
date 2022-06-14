import typing as t
import uuid

from dominion.cards.action import Action
from dominion.cards.card import Card

if t.TYPE_CHECKING:
    from dominion.deck import Deck
else:
    Deck = None  # pylint: disable=invalid-name


def choice_repr(obj: t.Any) -> str:
    if isinstance(obj, type):  # Explicit isclass behavior
        if issubclass(obj, Card):
            return obj.name
    return str(obj)


class Player:
    """Implements decision logic framework into the game."""

    deck: Deck
    player_id: str

    def __init__(self, deck: Deck):
        self.deck = deck
        self.player_id = f"{self.__class__.__qualname__}-{uuid.uuid4()}"

    def display_hand(self) -> None:
        self.deck.game.log(
            self.deck,
            "Your Hand:",
            *[card.name for card in self.deck.hand],
        )

    def action_phase(self) -> None:
        raise NotImplementedError

    def buy_phase(self) -> None:
        raise NotImplementedError

    def cleanup_phase(self) -> None:
        self.deck.cleanup()
        self.deck.actions = 1
        self.deck.coins = 0
        self.deck.buys = 1

    def choice(
        self, card: t.Optional[t.Type[Card]], prompt: str, choices: t.List[t.Any]
    ) -> t.Any:
        raise NotImplementedError


class Human(Player):
    """Implements human text prompts for decisions."""

    def action_phase(self) -> None:
        while self.deck.actions > 0 and (
            actions := [card for card in self.deck.hand if issubclass(card, Action)]
        ):
            if target_action := self.choice(
                None,
                f"Actions: {self.deck.actions}\nWhich Action card would you like to play?",
                actions,
            ):
                target_action.play(self.deck)
            else:
                break

    def buy_phase(self) -> None:
        while self.deck.buys > 0:
            if target_card := self.choice(
                None,
                f"Buys: {self.deck.buys}\nWhich card would you like to buy?",
                [
                    card
                    for card in self.deck.game.available_cards
                    if card.cost <= self.deck.coins
                ],
            ):
                target_card.buy(self.deck)
            else:
                break

    def choice(
        self, card: t.Optional[t.Type[Card]], prompt: str, choices: t.List[t.Any]
    ) -> t.Any:
        choice_map = {choice_repr(choice).strip().lower(): choice for choice in choices}
        resp = input(
            f"[{self.player_id}] "
            f"{choice_repr(card)}: "
            f"{prompt} "
            f"({'/'.join(map(choice_repr, choices))}): "
        ).strip()
        if resp:
            return choice_map[resp.lower()]
        return None


Players = t.List[Player]
PlayerTypes = t.List[t.Type[Player]]
