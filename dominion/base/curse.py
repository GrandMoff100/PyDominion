import typing as t

from .card import BaseCard


if t.TYPE_CHECKING:
    from ..player import PlayerTypes
else:
    PlayerTypes = None  # pylint: disable=invalid-name


class Curse(BaseCard):
    name: str = "Curse"
    points: int = -1

    @classmethod
    def setup(cls, players: PlayerTypes) -> int:
        """How many Curses to start with."""
        if len(players) <= 2:
            return 10
        if len(players) == 3:
            return 20
        if len(players) >= 4:
            return 30
        return 0
