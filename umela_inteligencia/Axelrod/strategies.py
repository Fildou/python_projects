import sys
import random


# DEFECT = 0
# COOPERATE = 1



def AlwaysDefect(history):
    state = 0
    return state

def AlwaysCooperate(history):
    state = 1
    return state

def TitForTat(history):
    if len(history) == 0:
        return 1
    else:
        return history[-1][1]

def RandomStrategy(history):
    state = random.randint(0, 1)
    return state

def PeriodicCCD(history):
    if len(history) == 0:
        return 1
    if (len(history) + 1) % 3 == 0:
        return 0
    else:
        return 1

def PeriodicDDC(history):
    if len(history) == 0:
        return 0
    if (len(history) + 1) % 3 == 0:
        return 1
    else:
        return 0

def ScepticStrategy(history): # my strategy
    if len(history) == 0:
        return 0
    if history[-1][1] == 0:
        return 0
    else: return 1



