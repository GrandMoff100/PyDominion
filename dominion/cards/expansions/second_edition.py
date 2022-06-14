"""Module defining the Kingdom Cards for Dominion (Second Edition)"""
import typing as t

from dominion.cards.action import Action, Attack
from dominion.cards.expansions.first_edition import (
    Bureaucrat,
    Cellar,
    Chapel,
    CouncilRoom,
    Festival,
    Gardens,
    Laboratory,
    Library,
    Market,
    Militia,
    Mine,
    Moat,
    Moneylender,
    Remodel,
    Smithy,
    ThroneRoom,
    Village,
    Witch,
    Workshop,
)
from dominion.cards.treasure import Copper, Gold, Treasure
from dominion.deck import Deck
from dominion.player import Player

__all__ = (
    "Cellar",
    "Chapel",
    "Moat",
    "Harbinger",
    "Merchant",
    "Vassal",
    "Village",
    "Workshop",
    "Bureaucrat",
    "Gardens",
    "Militia",
    "Moneylender",
    "Poacher",
    "Remodel",
    "Smithy",
    "ThroneRoom",
    "Bandit",
    "CouncilRoom",
    "Festival",
    "Laboratory",
    "Library",
    "Market",
    "Mine",
    "Sentry",
    "Witch",
    "Artisan",
)


class Harbinger(Action):
    name: str = "Harbinger"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +1 Card
        +1 Action
        Look through your discard pile.
        You may put a card from it onto your deck.
        """
        deck.draw()
        deck.actions += 1
        if deck.discard_pile:
            if chosen_card := deck.game.get_player(deck).choice(
                cls,
                "What card from your discard pile do you choose?",
                deck.discard_pile,
            ):
                deck.discard_pile.remove(chosen_card)
                deck.draw_pile.insert(0, chosen_card)


class Merchant(Action):
    name: str = "Merchant"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +1 Card
        +1 Action
        The first time you play a Silver this turn +1 Coin
        """
        deck.draw()
        deck.actions += 1


class Vassal(Action):
    name: str = "Vassal"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        Discard the top card of your deck.
        If is an Action card you may play it.
        """


class Poacher(Action):
    name: str = "Poacher"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +1 Card
        +1 Action
        +1 Coin
        Discard one card per empty supply pile.
        """
        deck.draw()
        deck.actions += 1
        deck.coins += 1
        cards_to_discard = len(deck.game.empty_supply_piles)
        for i in range(cards_to_discard):
            deck.discard(
                [
                    deck.player.choice(
                        cls,
                        f"({i + 1}/{cards_to_discard}) Which card will you discard?",
                        deck.hand,
                    )
                ]
            )


class Bandit(Attack):
    name: str = "Bandit"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck, targets: t.List[Player]) -> None:  # type: ignore[override]
        """
        Gain a Gold.
        Each other player reveals the top two cards of their deck
        and trashes any other revealed treasure cards other than Copper
        and discards the rest.
        """
        deck.gain(Gold)
        for player in targets:
            for i, card in enumerate(player.deck.draw_pile[0:2]):
                player.deck.draw_pile.pop(i)
                if issubclass(card, Treasure) and card != Copper:
                    player.deck.trash(card)
                else:
                    player.deck.hand.append(card)
                    player.deck.discard([card])


class Sentry(Action):
    name: str = "Sentry"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +1 Card
        +1 Action
        Look at the top two cards of your deck.
        Trash and/or discard any number of them.
        Put the rest back on top in any order.
        """
        deck.draw()
        deck.actions += 1
        cards_to_put_back = []
        for i, card in enumerate(deck.draw_pile[0:2]):
            deck.game.out(f"Card {i + 1}/2: {card.name}")
            choice = deck.player.choice(
                cls, "What do you want to do with it?", ["Trash", "Discard", "Put Back"]
            )
            deck.draw_pile.remove(card)
            if choice == "Trash":
                deck.trash(card)
            elif choice == "Discard":
                deck.hand.append(card)
                deck.discard([card])
            elif choice == "Put Back":
                cards_to_put_back.append(card)
        if cards_to_put_back:
            first_card = deck.player.choice(
                cls, "Which card do you want to put back first?", cards_to_put_back
            )
            deck.draw_pile.insert(0, first_card)
            if len(cards_to_put_back) > 1:
                second_card = cards_to_put_back[cards_to_put_back.index(first_card) - 1]
                deck.draw_pile.insert(0, second_card)


class Artisan(Action):
    name: str = "Artisan"
    cost: int = 6

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        Gain a card to your hand costing up to 5 Coins.
        Put a card from your hand onto your deck.
        """
        choices = [card for card in deck.game.available_cards if card.cost <= 5]
        deck.gain_to_hand(
            deck.player.choice(
                cls, "Which card would you like to gain to your hand?", choices
            )
        )
        deck.hand.remove(
            card := deck.player.choice(
                cls,
                "Which card are you going to put on top of your deck from your hand?",
                deck.hand,
            )
        )
        deck.draw_pile.insert(0, card)
