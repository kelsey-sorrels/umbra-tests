#!/usr/bin/env python
import random
import itertools
import time
import collections
import csv

class PlanetCard:
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

    def getProduceEnergy(self):
        return self.produceEnergy

    def getProduceMinerals(self):
        return self.produceMinerals

    def getProduceInfluence(self):
        return self.produceInfluence

    def getBuildShips(self):
        return self.buildShips

    def getInvadeEnergy(self):
        return self.invadeEnergy

    def getInvadeMinerals(self):
        return self.invadeMinerals

    def getInvadeInfluence(self):
        return self.invadeInfluence

class Space:
    def __init__(self, numPlanets):
        self.numPlanets = numPlanets
        self.ships = {}

    def getNumPlanets(self):
        return self.numPlanets

    def addShips(self, player, ships):
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

   def numOfEnemyShips(self, player):
        totalShips = 0
        for (spacePlayer, ships) in self.ships.items():
            if spacePlayer != player:
                totalShips += ships
        return totalShips

    def getEnemyShips(self, player):
        ships = []
        for (spacePlayer, ships) in self.ships.items():
            if spacePlayer != player and ships > 0:
                ships.append((spacePlayer, ships))
        return ships
class Board:
    def __init__(self, numOfPlayers):
        {2: self.init2}.get(numOfPlayers)()

    def init2(self):
        #                (-1,0)     (0,0)     (1, 0)
        self.spaces = {(-1,0):Space(2), (0,0):Space(0), (1,0):Space(2)}

    def getSpaces(self):
        return self.spaces

    def addSpace(self, space, pos):
        # space already exists?
        if findSpace(pos):
            raise "Trying to place new space where a space already exists (%d, %d)" % (x,y)
        else:
            self.spaces[pos] = space

    def findSpace(self, pos):
        if pos in self.spaces.keys:
            return self.spaces[pos]
        else:
            return None
        
    def findAdjacent(self, (x, y)):
        # 1 2
        # 0 x 5
        #   3 4
        return [findSpace((x-1, y)), findSpace((x-1, y-1)), findSpace((x, y-1)),
                findSpace((x, y+1)), findspace((x+1, y+1)), findspace((x+1, y))]

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

    def scorePlanet(self, planet):
        return planet.getProduceEnergy() + planet.getProduceMinerals() * 0.7 - planet.getInvadeEnergy() - planet.getInvadeMinerals() - planet.getInvadeInfluence() * 1.5

    def explore(self, game):
        # any ships next to an empty space?
        for (pos,space) in game.getBoard().getSpaces():
            if space.numShips(self) > 0:
                for space in game.getBoard().getAdjacent(pos):
                    if space is None:
                        # reveal the topmost hex and place it
                        newSpace = game.drawSpace()
                        # decide how many ships to move
                        numShips = space.numShips(self)
                        if newSpace.getNumPlanets() > 0:
                            planetCards = game.drawPlanetCards(newSpace.getNumPlanets() + 1)
                            numPlanetsToKeep = min(newSpace.getNumPlanets(), numShips)
                            # take planets cards and score them
                            scores = {}
                            for planetCard in planetCards:
                                scores[score(planetCard)] = planetCard
                            newPlanets = [p for (s, p) in scores[-numPlanetsToKeep:]]
                            # move ships from the exploring space to the new planets
                            for planetCard in newPlanets:
                                space.removeShips(self, 1)
                                planetCard.addShips(self, 1)
                        else:
                            # no planets to explore. Move one ship into the space
                            space.removeShips(self, 1)
                            newSpace.addShips(self, 1)
                        # either moved ships or got planets. Nothing else to do
                        break

    def resolveAttack(self, space, attacker, defender, attackerTactic, defenderTactic):
        pass

    def moveAttack(self, game):
        # any opponent ships in an adjacent space?
        for (pos,space) in game.getBoard().getSpaces():
            if space.numShips(self) > 0:
                for adjSpace in game.getBoard().getAdjacent(pos):
                    if adjSpace is not None and adjSpace.numOfEnemyShips(player) > 0:
                        space.removeShips(self, 1)
                        adjSpace.addShips(self, 1)
                        (defender, defenderShips) = adjSpace.getEnemyShips()[0]
                        defenderTactic = defender.chooseTactic(defenderShips)
                        attackerTactic = self.cooseTactic(1)
                        resolveAttack(adjSpace, self, defender, attackerTactic, defenderTactic)
                        # combat resolved, nothing left to do
                        return
        # if we got here, then there was no combar
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
        self.spaces = initSpaces()
        self.logRecord = []

    def initActionCards(self):
        return collections.deque([ActionCards.EXPLORE, ActionCards.MOVE_ATTACK, ActionCards.MOVE_ATTACK, ActionCards.INVADE,
                ActionCards.DEFEND, ActionCards.DISBAND, ActionCards.DISBAND, ActionCards.BUILD,
                ActionCards.BUILD, ActionCards.RESEARCH, ActionCards.PRODUCE, ActionCards.PRODUCE,
                ActionCards.TRADE, ActionCards.SABOTAGE, ActionCards.ESPIONAGE, ActionCards.COUP,
                ActionCards.POLITICS, ActionCards.CORRUPTION])

    def initPlanetCards(self):
        planetCards = []
        with open('data/planets.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile)
            headerline = reader.next()
            for row in reader:
                #name, produceEnergy, produceMinerals, produceInfluence, buildShips, invadeEnergy, invadeMinerals, invadeInfluence
                planetCards.append(PlanetCard(row[0], row[5], row[6], row[7], row[8], row[1], row[2], row[3]))
        return planetCards

    def initTechnologyCards(self):
        return []

    def initResolutionCards(self):
        return []

    def initSpaces(self):
        return []

    def log(self, msg):
        print(str(msg))
        self.logRecord.append(str(msg))

    def getBoard(self):
        return self.board

    def getLog(self):
        return '\n'.join(self.logRecord)

    def hasWinner(self):
        return False

    def drawSpace(self):
        return self.spaces.pop(0)

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
