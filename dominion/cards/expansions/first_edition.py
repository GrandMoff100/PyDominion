"""Module defining the Kingdom Cards for Dominion (First Edition)"""
import typing as t

from dominion.cards.action import Action, Attack, Reaction
from dominion.cards.card import Card, KingdomCard
from dominion.cards.curse import Curse
from dominion.cards.treasure import Copper, Silver, Treasure
from dominion.cards.victory import Victory
from dominion.deck import Deck
from dominion.errors import CardNotFoundError
from dominion.player import Player, Players

__all__ = (
    "Cellar",
    "Chapel",
    "Moat",
    "Chancellor",
    "Village",
    "Woodcutter",
    "Workshop",
    "Bureaucrat",
    "Gardens",
    "Militia",
    "Moneylender",
    "Feast",
    "Remodel",
    "Smithy",
    "Spy",
    "Thief",
    "ThroneRoom",
    "CouncilRoom",
    "Festival",
    "Laboratory",
    "Library",
    "Market",
    "Mine",
    "Witch",
    "Adventurer",
)


class Cellar(Action):
    name: str = "Cellar"
    cost: int = 2

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +1 Action
        Discard any number of cards, then draw that many.
        """
        deck.actions += 1
        cards: t.List[t.Type[Card]] = []
        for _ in deck.hand:
            if card := deck.player.choice(
                cls,
                "What card would you like to discard? Press enter to stop.",
                deck.hand,
            ):
                cards.append(card)
            else:
                break
        deck.discard(cards)
        deck.draw(len(cards))


class Chapel(Action):
    name: str = "Chapel"
    cost: int = 2

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """Trash up to 4 cards from your hand"""
        cards: t.List[t.Type[Card]] = []
        for i in range(1, 5):
            if card := deck.player.choice(
                cls, f"[{i}/4] What card would you like to trash?", deck.hand
            ):
                cards.append(card)
            else:
                break
        for card in cards:
            if card in deck.hand:
                deck.trash(deck.hand.pop(deck.hand.index(card)))
            else:
                raise CardNotFoundError(
                    f"Cannot trash the {card.name}, it is not in your hand."
                )


class Moat(Reaction):
    name: str = "Moat"
    cost: int = 2

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +2 Cards
        """
        deck.draw(2)

    @classmethod
    def when_attack(cls, deck: Deck, card: t.Type[Card], targets: Players) -> None:
        """
        When another player plays an Attack card,
        you can first reveal this card and then be unaffected by it.
        """
        player = deck.game.get_player(deck)
        if player.deck.reveal(cls):
            targets.remove(player)


class Chancellor(Action):
    name: str = "Chancellor"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +2 Coins
        You may immediately put your deck in the discard pile.
        """
        deck.coins += 2
        if (
            deck.game.get_player(deck).choice(
                cls,
                "You may immediately put your deck in the discard pile:",
                ["Yes", "No"],
            )
            == "Yes"
        ):
            deck.discard_pile += deck.draw_pile
            deck.draw_pile = []


class Village(Action):
    name: str = "Village"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +1 Card
        +2 Actions
        """
        deck.draw()
        deck.actions += 2


class Woodcutter(Action):
    name: str = "Woodcutter"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +1 Buy
        +2 Coins
        """
        deck.buys += 1
        deck.coins += 2


class Workshop(Action):
    name: str = "Workshop"
    cost: int = 3

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """Gain a card costing up to four coins."""
        deck.game.get_player(deck).choice(
            cls,
            "Gain a card costing up to four coins:",
            [card for card in deck.game.available_cards if card.cost <= 4],
        )


class Bureaucrat(Attack):
    name: str = "Bureaucrat"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck) -> None:  # type: ignore[override]
        """
        Gain a Silver onto your deck.
        Each other player reveals a Victory card from their hand and
        puts it onto their deck (or reveals a hand with no Victory cards).
        """
        deck.draw_pile.insert(0, Silver)
        for player in deck.game.players:
            for card in player.deck.hand:
                if issubclass(card, Victory):
                    player.deck.draw_pile.insert(0, card)
                    break


class Gardens(Victory, KingdomCard):
    name: str = "Gardens"
    cost: int = 4

    @classmethod
    def points(cls, deck: Deck) -> int:
        """Worth 1 Victory Point for every 10 cards in your deck (rounded down)."""
        return len(deck.cards) // 10


class Militia(Attack):
    name: str = "Militia"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck, targets: t.List[Player]) -> None:  # type: ignore[override]
        """
        +2 Coins
        Each other player discards down to 3 cards in their hand.
        """
        deck.coins += 2
        for player in targets:
            for _ in range(max([3, len(player.deck.hand)]) - 3):
                player.deck.discard(
                    player.choice(
                        cls,
                        "Choose one card from your hand to discard",
                        player.deck.hand,
                    )
                )


class Moneylender(Action):
    name: str = "Moneylender"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        You may trash a Copper from your hand for +3 coins.
        """
        if Copper in deck.hand:
            deck.hand.remove(Copper)
            deck.trash(Copper)
            deck.coins += 3


class Feast(Action):
    name: str = "Feast"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        You may trash this card and gain a card costing up to 5 Coins.
        """
        deck.discard_pile.remove(cls)
        deck.trash(cls)
        choices = [card for card in deck.game.available_cards if card.cost <= 5]
        deck.gain(deck.player.choice(cls, "Which card do you want to gain?", choices))


class Remodel(Action):
    name: str = "Remodel"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        Trash a card from your hand.
        Gain a card costing up to 2 Coins more than it.
        """
        if deck.hand:
            trashed_card = deck.trash(
                deck.player.choice(
                    cls, "Which card do you want to trash from your hand?", deck.hand
                )
            )
            if available_card_choices := [
                card
                for card in deck.game.available_cards
                if card.cost >= trashed_card.cost + 2
            ]:
                deck.gain_to_hand(
                    deck.player.choice(
                        cls,
                        "Which Treasure do you want to gain?",
                        available_card_choices,
                    )
                )
            else:
                deck.game.log(deck, "No cards available to be gained.")


class Smithy(Action):
    name: str = "Smithy"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +3 Cards
        """
        deck.draw(3)


class Spy(Attack):
    name: str = "Spy"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck, targets: t.List[Player]) -> None:  # type: ignore[override]
        """
        +1 Card
        +1 Action
        Each player (including you) reveals the top two cards of their deck
        and either discards it or puts it back.
        """
        deck.draw()
        deck.actions += 1
        for player in targets + [deck.player]:
            for i, card in enumerate(player.deck.draw_pile[0:2]):
                player.deck.reveal(card)
                if (
                    player.choice(cls, f"Discard the {card.name}", ["Yes", "No"])
                    == "Yes"
                ):
                    player.deck.hand.append(player.deck.draw_pile.pop(i))
                    player.deck.discard([card])


class Thief(Attack):
    name: str = "Thief"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck, targets: t.List[Player]) -> None:  # type: ignore[override]
        """
        Each other player reveals the top 2 cards of their deck.
        If they revealed any Treasure cards they trash one of them that you choose.
        You may gain any or all of these trashed cards.
        They discard the other Treasure cards.
        """
        for player in targets:
            choices = [
                card
                for card in player.deck.draw_pile[0:2]
                if issubclass(card, Treasure)
            ]
            if choices:
                target_card = deck.player.choice(
                    cls,
                    "Which one of their Treasure cards do you want to trash?",
                    choices,
                )
                player.deck.draw_pile.remove(target_card)
                player.deck.trash(target_card)
                if (
                    deck.player.choice(
                        cls,
                        f"Do you want to gain that {target_card.name}?",
                        ["Yes", "No"],
                    )
                    == "Yes"
                ):
                    deck.gain(target_card)
                    deck.game.trash_pile.remove(target_card)


class ThroneRoom(Action):
    name: str = "Throne Room"
    cost: int = 4

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        Choose an Action card from your hand.
        You may play it twice.
        """
        if action_cards_in_hand := [
            card for card in deck.hand if issubclass(card, Action)
        ]:
            card = deck.player.choice(
                cls,
                "Which action card do you wish to play twice?",
                action_cards_in_hand,
            )
            for _ in range(2):
                card.play(deck)


class CouncilRoom(Action):
    name: str = "Council Room"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +4 Cards
        +1 Buy
        Each other player draws a card.
        """
        deck.draw(4)
        deck.buys += 1
        for player in deck.game.players:
            player.deck.draw()


class Festival(Action):
    name: str = "Festival"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +2 Actions
        +1 Buy
        +2 Coins
        """
        deck.actions += 2
        deck.buys += 1
        deck.coins += 2


class Laboratory(Action):
    name: str = "Laboratory"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +2 Cards
        +1 Action
        """
        deck.draw(2)
        deck.actions += 1


class Library(Action):
    name: str = "Library"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        Draw until you have seven cards in your hand,
        skipping any Action cards you choose to,
        set those aside,
        discard them afterwards.
        """
        while len(deck.hand) < 7:
            drawn_card = deck.draw()[0]
            if issubclass(drawn_card, Action):
                if (
                    deck.player.choice(
                        cls,
                        f"Skip this {drawn_card.name}?",
                        ["Yes", "No"],
                    )
                    == "Yes"
                ):
                    deck.discard([drawn_card])


class Market(Action):
    name: str = "Market"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        +1 Card
        +1 Action
        +1 Buy
        +1 Coin
        """
        deck.draw()
        deck.actions += 1
        deck.buys += 1
        deck.coins += 1


class Mine(Action):
    name: str = "Mine"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        You may trash a Treasure card from your hand.
        Gain a Treasure card costing up to 3 Coins more than it.
        """
        if treasure_cards_in_hand := [
            card for card in deck.hand if issubclass(card, Treasure)
        ]:
            trashed_card = deck.trash(
                deck.player.choice(
                    cls, "Which Treasure do you want to trash?", treasure_cards_in_hand
                )
            )
            if available_treasure_cards := [
                card
                for card in deck.game.available_cards
                if issubclass(card, Treasure) and card.cost >= trashed_card.cost + 3
            ]:
                deck.gain_to_hand(
                    deck.player.choice(
                        cls,
                        "Which Treasure do you want to gain?",
                        available_treasure_cards,
                    )
                )
            else:
                deck.game.log(deck, "No Treasure cards available to be gained.")


class Witch(Attack):
    name: str = "Witch"
    cost: int = 5

    @classmethod
    def effect(cls, deck: Deck, targets: t.List[Player]) -> None:  # type: ignore[override]
        """
        +2 Cards
        Each other player gains a curse card.
        """
        deck.draw(2)
        for player in targets:
            player.deck.discard_pile.append(Curse)


class Adventurer(Action):
    name: str = "Adventurer"
    cost: int = 6

    @classmethod
    def effect(cls, deck: Deck) -> None:
        """
        Reveal cards from your deck until your reveal two Treasure cards.
        Put those Treasure cards in your hand and discard the other revealed cards.
        """
        revealed_treasure_cards: t.List[t.Type[Treasure]] = []
        while len(revealed_treasure_cards) < 2:
            card = deck.reveal(deck.draw()[0])
            if issubclass(card, Treasure):
                revealed_treasure_cards.append(card)
            else:
                deck.discard([card])
