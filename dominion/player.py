from abc import abstractmethod
import uuid
import typing as t

from .base import Action

if t.TYPE_CHECKING:
    from .deck import Deck
else:
    Deck = None  # pylint: disable=invalid-name


class Player:
    """Implements decision logic framework into the game."""

    deck: Deck
    player_id: str

    def __init__(self, deck: Deck):
        self.deck = deck
        self.player_id = uuid.uuid4()

    def action_phase(self):
        while self.deck.actions_remaining > 0 and (
            actions := [card for card in self.deck.hand if issubclass(card, Action)]
        ):
            self.choice("Select an action:", actions, "action").play()  # TODO: Add the option to not use any actions (idk why you wouldn't want to, but whatever)

    def buy_phase(self):
        while self.deck.buys_remaining > 0 and not self.deck.game.ended and (
            affordable := [card for card in self.deck.game.available_cards if card.cost <= self.deck.coins_remaining]
        ):
            self.choice("Buy a card:", affordable, "buy").buy(self.deck)  # TODO: Add the option to not buy anything

    def cleanup_phase(self):
        self.deck.cleanup()

    @abstractmethod
    def choice(self, prompt: str, choices: t.List[t.Any], option_type: str) -> t.Any:
        raise NotImplementedError


class Human(Player):
    """Implements human text prompts for decisions."""

    def choice(self, prompt: str, choices: t.List[t.Any], option_type: str) -> t.Any:
        choice_map = {str(choice).lower(): choice for choice in choices}

        return choice_map[
            input(f"[{self.player_id}] ({option_type}) {prompt} ({'/'.join(map(str, choices))}): ")
            .strip()
            .lower()
        ]


PlayerTypes = t.List[t.Type[Player]]
