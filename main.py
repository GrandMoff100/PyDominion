from dominion import Game, Human
from dominion.cards.expansions import first_edition as fe

game = Game(
    [Human, Human],
    [
        fe.Cellar,
        fe.ThroneRoom,
        fe.Village,
        fe.Smithy,
        fe.Workshop,
        fe.Remodel,
        fe.Chapel,
        fe.Festival,
        fe.Market,
        fe.Feast,
    ],
)

game.play()
