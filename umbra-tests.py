#!/usr/bin/env python
import random
import itertools
import time
import collections
import csv

class Planet:
    def __init__(self, name, produceEnergy, produceMinerals, produceInfluence, buildShips,
            invadeEnergy, invadeMinerals, invadeInfluence):
        self.produceEnergy = produceEnergy
        self.produceMinerals = produceMinerals
        self.produceInfluence = produceInfluence
        self.ships = {}
        self.buildShips = buildShips
        self.invadeEnergy = invadeEnergy
        self.invadeMinerals = invadeMinerals
        self.invadeInfluence = invadeInfluence

class Space:
    def __init__(self, numPlanets):
        self.numPlanets = numPlanets
        self.ships = {}

    def getNumPlanets(self):
        return self.numPlanets

    def placeShips(self, player, ships):
        if player not in self.ships.keys:
            self.ships[player] = 0
        self.ships[player] += ships

    def removeShips(self, player, ships):
        if player not in self.ships.keys:
            raise "Trying to remove ships where there are none"
        elif self.ships[player] < ships:
            raise "Trying to remove ships when there are not enough"
        else:
            self.ships[player] -= ships

   def numOfShips(self, player):
       if player not in self.ships.keys:
           return 0
       else:
           return self.ships[player]


#
#   Hex neighbor ordering
#
#         0
#      5  |  1
#        \ /
#        / \ 
#      4  |  2
#         3

class Board:
    def __init__(self, numOfPlayers):
        {2: self.init2}.get(numOfPlayers)()

    def init2(self):
        #                (-1,0)     (0,0)     (1, 0)
        self.spaces = [[Space(2), Space(0), Space(2)]]

    def addSpace(self, space, (x, y)):
        # space already exists?
        if findSpace(x, y):
            raise "Trying to place new space where a space already exists (%d, %d)" % (x,y)
        else:
            pass

    def findAdjacent(self, (x, y)):
        pass

class Player:
    def __init__(self, startingPlanets):
        self.minerals = 3
        self.energy = 3
        self.influence = 0
        self.actionQueue = []
        self.remainingShips = 20-3
        self.planets = startingPlanets

    def pickCard(self, hand):
        if (self.minerals < 10 or self.energy < 10) and ActionCards.PRODUCE in hand:
            hand.remove(ActionCards.PRODUCE)
            self.actionQueue.append(ActionCards.PRODUCE)
        elif self.remainingShips > 0 and ActionCards.BUILD in hand:
            hand.remove(ActionCards.BUILD)
            self.actionQueue.append(ActionCards.BUILD)
        else:
            self.actionQueue.append(hand.pop())
        return hand

    def tick(self, game):
        # reveal cards from queue left-to-right
        card = self.actionQueue.pop(0)
        {ActionCards.EXPLORE: self.explore,
         ActionCards.MOVE_ATTACK: self.moveAttack,
         ActionCards.INVADE: self.invade,
         ActionCards.DEFEND: self.defend,
         ActionCards.DISBAND: self.disband,
         ActionCards.BUILD: self.build,
         ActionCards.RESEARCH: self.research,
         ActionCards.PRODUCE: self.produce,
         ActionCards.TRADE: self.trade,
         ActionCards.SABOTAGE: self.sabotage,
         ActionCards.ESPIONAGE: self.espionage,
         ActionCards.POLITICS: self.politics,
         ActionCards.COUP: self.coup,
         ActionCards.ELECTION: self.election,
         ActionCards.CORRUPTION: self.corruption}.get(card)(game)

    def explore(self, game):
        # any ships next to an empty space?
        # reveal the topmost hex and place it
        # decide how many ships to move
        # take planets cards and score them
        # take the top cards and place them and ships
        pass

    def moveAttack(self, game):
        # any opponent ships in an adjacent space?
        #   move ships to space
        #   attack
        # else
        # any ships need to explore?
        #   move ships closer to adjacent space

    def invade(self, game):
        # any ships in space with opponent planet?
        #   pay invasion cost
        #   remove opponent ships
        #   place ships

    def defend(self, game):
        # any ships in space with planet?
        #   move ships to planet

    def disband(self, game):
        # any ships on planets?
        #   move ships to space

    def build(self, game):
        # have enough resources to build?
        #   pick planet with highest build
        #   take ships from pool and put them on planet

    def research(self, game):
        pass

    def produce(self, game):
        # have more energy than minerals?
        #   find planet with most mineral production
        #   produce from planet
        # else
        #   find planet with most energy production
        #   produce from planet

    def trade(self, game):
        pass

    def sabotage(self, game):
        pass

    def espionage(self, game):
        pass

    def politics(self, game):
        pass

    def coup(self, game):
        pass

    def election(self, game):
        pass

    def corruption(self, game):
        # have two influence?
        #   steal to have equal energy and minerals
    
    def getActionQueue(self):
        return self.actionQueue

    def isActionQueueEmpty(self):
        return not self.actionQueue

class ActionCards:
    EXPLORE = 0
    MOVE_ATTACK = 1
    INVADE = 2
    DEFEND = 3
    DISBAND = 4
    BUILD = 5
    RESEARCH = 6
    PRODUCE = 7
    TRADE = 8
    SABOTAGE = 9
    ESPIONAGE = 10
    COUP = 11
    ELECTION = 12
    POLITICS = 13
    CORRUPTION = 14


class Game:
    def __init__(self):
        self.actionCards = self.initActionCards()
        self.plantCards = self.initPlanetCards()
        self.technologyCards = self.initTechnologyCards()
        self.resolutionCards = self.initResolutionCards()
        self.playerOne = Player([])
        self.players = [self.playerOne, Player([])]
        self.playerOrder = itertools.cycle(self.players)
        self.board = Board(len(self.players))
        self.logRecord = []

    def initActionCards(self):
        return collections.deque([ActionCards.EXPLORE, ActionCards.MOVE_ATTACK, ActionCards.MOVE_ATTACK, ActionCards.INVADE,
                ActionCards.DEFEND, ActionCards.DISBAND, ActionCards.DISBAND, ActionCards.BUILD,
                ActionCards.BUILD, ActionCards.RESEARCH, ActionCards.PRODUCE, ActionCards.PRODUCE,
                ActionCards.TRADE, ActionCards.SABOTAGE, ActionCards.ESPIONAGE, ActionCards.COUP,
                ActionCards.POLITICS, ActionCards.CORRUPTION])

    def initPlanetCards(self):
        planets = []
        with open('data/planets.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile)
            headerline = reader.next()
            for row in reader:
                #name, produceEnergy, produceMinerals, produceInfluence, buildShips, invadeEnergy, invadeMinerals, invadeInfluence
                planets.append(Planet(row[0], row[5], row[6], row[7], row[8], row[1], row[2], row[3]))
        return planets

    def initTechnologyCards(self):
        return []

    def initResolutionCards(self):
        return []

    def log(self, msg):
        print(str(msg))
        self.logRecord.append(str(msg))

    def getLog(self):
        return '\n'.join(self.logRecord)

    def hasWinner(self):
        return False

    def tick(self):
        if all([player.isActionQueueEmpty() for player in self.players]):
            # players ran out of actions
            self.log('players out of action cards')
            # shuffle action cards and deal them out
            self.log('shuffling action cards')
            random.shuffle(self.actionCards)
            handSize = len(self.actionCards)/len(self.players)
            self.log('hand size: %d' % (handSize))
            hands = [[self.actionCards[i] for i in range(j, len(self.actionCards), len(self.players))] for j in range(len(self.players))]
            self.log('starting hands: %s' % (str(hands)))
            # players keep picking actions until they each have 5 action cards in their queue
            for i in range(5):
                print hands
                hands = collections.deque([self.players[j].pickCard(hands[j]) for j in range(0, len(self.players))])
                hands.rotate(1)

            self.log('action queues: %s' % str([self.players[i].getActionQueue() for i in range(len(self.players))]))
        for player in self.players:
            player.tick(self)

def runGame():
    ticks = 0
    game = Game()
    while not game.hasWinner() and ticks < 500:
        ticks+=1
        game.tick()
    return game

def main():
	# number of games to run
    numGames = 1
    startTime = time.time()
    games = [runGame() for i in range(numGames)]
    print "Ran %d games in %d seconds" % (numGames, time.time() - startTime)
    for game in games:
        print '--------------Start Game Log---------------------'
        print game.getLog()

if __name__ == "__main__":
    main()
