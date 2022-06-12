import base64
import random
import time
import typing as t

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

    def action_phase(self) -> None:
        raise NotImplementedError

    def buy_phase(self) -> None:
        raise NotImplementedError

    def cleanup_phase(self) -> None:
        self.deck.discard(self.deck.hand)
        self.deck.draw(5)
        self.deck.actions = 1
        self.deck.coins = 0
        self.deck.buys = 1

    def choice(self, prompt: str, choices: t.List[t.Any]) -> t.Any:
        raise NotImplementedError


class Human(Player):
    """Implements human text prompts for decisions."""

    def action_phase(self) -> None:
        pass

    def choice(self, prompt: str, choices: t.List[t.Any]) -> t.Any:
        choice_map = {str(choice).lower(): choice for choice in choices}

        return choice_map[
            input(f"[{self.player_id}] {prompt} ({'/'.join(map(str, choices))}): ")
            .strip()
            .lower()
        ]


PlayerTypes = t.List[t.Type[Player]]
