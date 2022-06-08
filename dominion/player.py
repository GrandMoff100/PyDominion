import typing as t

from .event import Event
from .base import Card
from .deck import Deck


class Player:
    """Implements decision logic framework into the game."""

    deck: Deck
    player_id: str

    def __init__(self, deck: Deck, player_id: str):
        self.deck = deck
        self.player_id = player_id

    def action_phase(self):
        pass

    def buy_phase(self):
        pass

    def cleanup_phase(self):
        pass

    def choice(self, prompt: str, choices: t.List[t.Any]) -> t.Any:
        raise NotImplementedError


class Human(Player):
    """Implements human text prompts for decisions."""

    def choice(self, prompt: str, choices: t.List[t.Any]) -> t.Any:
        choice_map = {str(choice).lower(): choice for choice in choices}

        return choice_map[
            input(f"{prompt} ({'/'.join(map(str, choices))}): ").strip().lower()
        ]


PlayerTypes = t.List[t.Type[Player]]
