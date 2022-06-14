import random
import typing as t

from dominion.cards.card import Card
from dominion.cards.expansions.second_edition import Smithy
from dominion.cards.treasure import Gold, Silver
from dominion.cards.victory import Duchy, Province
from dominion.player import Player


class BigMoney(Player):
    def action_phase(self) -> None:
        pass

    def buy_phase(self) -> None:
        if self.deck.coins >= 8 and Province in self.deck.game.available_cards:
            Province.buy(self.deck)
        elif self.deck.coins >= 6 and Gold in self.deck.game.available_cards:
            Gold.buy(self.deck)
        elif self.deck.coins >= 5 and Duchy in self.deck.game.available_cards:
            Duchy.buy(self.deck)
        elif self.deck.coins >= 4 and Smithy in self.deck.game.available_cards:
            Smithy.buy(self.deck)
        elif self.deck.coins >= 3 and Silver in self.deck.game.available_cards:
            Silver.buy(self.deck)

    def choice(self, card: t.Type[Card], prompt: str, choices: t.List[t.Any]) -> t.Any:  # pylint: disable=unused-argument
        return random.choice(choices)


class BigMoneySmithy(BigMoney):
    def action_phase(self) -> None:
        if Smithy in self.deck.hand:
            Smithy.play(self.deck)

    def buy_phase(self) -> None:
        if self.deck.coins >= 8 and Province in self.deck.game.available_cards:
            Province.buy(self.deck)
        elif self.deck.coins >= 6 and Gold in self.deck.game.available_cards:
            Gold.buy(self.deck)
        elif self.deck.coins >= 5 and Duchy in self.deck.game.available_cards:
            Duchy.buy(self.deck)
        elif self.deck.coins >= 3 and Silver in self.deck.game.available_cards:
            Silver.buy(self.deck)
