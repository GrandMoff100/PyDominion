import typing as t


from .base import CardTypes, Card, Copper, Silver, Gold, Estate, Duchy, Province, Curse
from .deck import Deck
from .player import Player, PlayerTypes


class Game:
    trash_pile: CardTypes
    kingdom_cards: t.Dict[t.Type[Card], int]
    base_cards: t.Dict[t.Type[Card], int]
    players: t.List[Player]

    def __init__(self, players: PlayerTypes, kingdom_card_set: CardTypes):
        self.players = [player(Deck(self)) for player in players]
        self.trash_pile = []
        self.kingdom_cards = {card: card.setup(players) for card in kingdom_card_set}
        self.base_cards = {
            card: card.setup(players)
            for card in [Copper, Silver, Gold, Estate, Duchy, Province, Curse]
        }

    def play(self) -> None:
        pass

    @property
    def current_player(self) -> t.Type[Player]:
        return self.players[0]

    def player_lookup(self, deck: Deck) -> t.Optional[Player]:
        for player in self.players:
            if player.deck == deck:
                return player

    @property
    def ended(self) -> bool:
        if self.base_cards[Province] == 0:
            return True
        empty_piles = [
            card for card, count in self.kingdom_cards.items() if count == 0
        ] + [card for card, count in self.base_cards.items() if count == 0]
        return len(empty_piles) >= 3
