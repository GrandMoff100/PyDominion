from bots.bigmoney import BigMoney, BigMoneySmithy
from dominion import Game
from dominion.cards.expansions import first_edition as fe

kingdom = [
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
]

scores = {BigMoney: 0, BigMoneySmithy: 0}

for i in range(10000):
    print("Game:", i)
    report = Game(scores, kingdom).play()
    for winner in report.winners:
        scores[winner[0].__class__] += 1
print("Done")

print(scores)
