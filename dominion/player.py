import typing as t
import random
import time
import base64


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
        self.player_id = base64.b64encode(
            str(time.time()).zfill(24).encode()
        ).decode() + "".join(
            random.choice(
                "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
            )
            for _ in range(10)
        )

    def action_phase(self):
        raise NotImplementedError

    def buy_phase(self):
        raise NotImplementedError

    def cleanup_phase(self):
        raise NotImplementedError

    def choice(self, prompt: str, choices: t.List[t.Any]) -> t.Any:
        raise NotImplementedError


class Human(Player):
    """Implements human text prompts for decisions."""

    def choice(self, prompt: str, choices: t.List[t.Any]) -> t.Any:
        choice_map = {str(choice).lower(): choice for choice in choices}

        return choice_map[
            input(f"[{self.player_id}] {prompt} ({'/'.join(map(str, choices))}): ")
            .strip()
            .lower()
        ]


PlayerTypes = t.List[t.Type[Player]]
