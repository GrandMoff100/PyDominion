import functools
import typing as t
from collections import defaultdict

from dominion.cards.card import Card
from dominion.cards.curse import Curse
from dominion.cards.victory import Victory
from dominion.player import Player

if t.TYPE_CHECKING:
    from .game import Game
else:
    Game = None  # pylint: disable=invalid-name


class Report:
    def __init__(self, game: Game) -> None:
        self.game = game

    @functools.cached_property
    def scores(self) -> t.Dict[Player, int]:
        return {
            player: sum(
                card.points(player.deck)
                for card in player.deck.cards
                if issubclass(card, (Victory, Curse))
            )
            for player in self.game.players
        }

    @property
    def winners(self) -> t.List[t.Tuple[Player, int]]:
        max_score = max(self.scores.values())
        return [
            (player, score)
            for player, score in self.scores.items()
            if score >= max_score
        ]

    @staticmethod
    def player_deck(player: Player) -> t.Dict[t.Type[Card], int]:
        total: t.Dict[t.Type[Card], int] = defaultdict(int)
        for card in player.deck.cards:
            total[card] += 1
        return dict(total)

    def view(self) -> str:
        scores = "\n".join(
            f"  - {player.player_id}: {score}" for player, score in self.scores.items()
        )
        supply = "\n".join(
            f"  - {card.name}: {count}" for card, count in self.game.supply.items()
        )
        decks = "\n".join(
            f"  - [{player.player_id}]: "
            + ", ".join(
                f"{card.name}: {count}"
                for card, count in self.player_deck(player).items()
            )
            for player in self.game.players
        )
        return (
            f"Scores:\n{scores}\n"
            f"Remaining Supply:\n{supply}\n"
            f"Player Decks:\n{decks}"
        )

    def __str__(self) -> str:
        return self.view()
