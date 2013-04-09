#!/usr/bin/env python
import random
import itertools

class Board(Object):
    def __init__(self, numOfPlayers):
        {2: init2()}.get(numOfPlayers)()

    def init2():
        self.

class Player(Object):
    def __init__(self):
        self.minerals = 3
        self.energy = 3
        self.influence = 0
        self.actionQueue = []
        self.remainingShips = 20-3

    def tick(self, game, cardsToPick = None):
        if cardsToPick != None:
            pickCard(cardsToPick)
        else:
            playCard()

    def isActionQueueEmpty(self):
        return not self.actionQueue

class Game(Object):
    def __init__(self):
        self.actionCards = initActionCards()
        self.plantCards = initPlanetCards()
        self.technologyCards = initTechnologyCards()
        self.resolutionCards = initResolutionCards()
        self.playerOne = Player()
        self.players = [playerOne, Player()]
        self.playerOrder = itertools.cycle(players)
        self.board = Board()

    def hasWinner(self):
        return True

    def tick(self):
        if all([player.isActionQueueEmpty() for player in self.players]:
            # players ran out of actions
            # shuffle action cards and deal them out
            random.shuffle(self.actionCards)
            hands = [self.actionCards[x:x+100] for x in xrange(0, len(self.actionCards), 100)]
            # players keep picking actions until they each have 5 action cards in their queue

def runGame():
	game = Game()
	while !game.hasWinner()
	    game.tick()
    return game

def main():
	# number of games to run
    results = [runGame() for i in range(100)]   


if __name__ == "__main__":
    main()
