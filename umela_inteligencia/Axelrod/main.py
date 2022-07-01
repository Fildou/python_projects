import sys
import pprint
import strategies


strategy = [strategies.AlwaysDefect, strategies.AlwaysCooperate, strategies.TitForTat,
              strategies.RandomStrategy, strategies.PeriodicCCD, strategies.PeriodicDDC, strategies.ScepticStrategy]

for i in range(len(strategy) - 1):
    p1Strategy = strategy[i]
    print("P1 chose strategy: ", p1Strategy.__name__)

    for j in range(len(strategy)):
        p2Strategy = strategy[j]
        print("P2 chose strategy: ", p2Strategy.__name__)
        p1Points, p2Points = 0, 0
        history = []

        for r in range(200):
            p1Pick = p1Strategy(history)
            p2Pick = p2Strategy([e[::-1] for e in history])

            if (p1Pick == p2Pick):
                if (p1Pick == 0):
                    p1Points += 1
                    p2Points += 1
                else:
                    p1Points += 3
                    p2Points += 3
            else:
                if (p1Pick == 0):
                    p1Points += 5
                elif (p2Pick == 0):
                    p2Points += 5
            history.append([p1Pick, p2Pick])
        print(history)

        if(p1Points > p2Points):
            print("winner is: ", p1Strategy.__name__)
        elif(p1Points < p2Points):
            print("winner is: ", p2Strategy.__name__)
        elif(p1Points == p2Points):
            print("tie")
        print("-----------------------------------------------------------------------------------------")


