#!/usr/bin/env python
import random
import itertools
import time
import collections
import csv

class PlanetCard:
    def __init__(self, name, produceEnergy, produceMinerals, produceInfluence, buildShips,
            invadeEnergy, invadeMinerals, invadeInfluence):
        self.name = name
        self.produceEnergy = produceEnergy
        self.produceMinerals = produceMinerals
        self.produceInfluence = produceInfluence
        self.ships = {}
        self.buildShips = buildShips
        self.invadeEnergy = invadeEnergy
        self.invadeMinerals = invadeMinerals
        self.invadeInfluence = invadeInfluence

    def getName(self):
        return self.name

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

    def numOfShips(self, player):
        if player not in self.ships.keys():
            return 0
        else:
            return self.ships[player]

    def addShips(self, player, numShips):
        if player not in self.ships.keys():
            self.ships[player] = 0
        self.ships[player] += numShips

    def removeShips(self, player, numShips):
        if player not in self.ships.keys() and numShips != 0:
            raise "Cannot remove ships from space. The player has no ships here."
        if self.ships[player] < numShips:
            raise "Cannot remove more ships than the player has in this space."
        self.ships[player] -= numShips

    def setSpace(self, space):
        self.space = space

    def getSpace(self):
        return self.space
class Space:
    def __init__(self, numPlanets):
        self.numPlanets = numPlanets
        self.ships = {}
        # players -> planets[]
        self.planets = {}

    def getNumPlanets(self):
        return self.numPlanets

    def addShips(self, player, ships):
        if player not in self.ships.keys():
            self.ships[player] = 0
        self.ships[player] += ships

    def removeShips(self, player, ships):
        if player not in self.ships.keys():
            raise "Trying to remove ships where there are none"
        elif self.ships[player] < ships:
            raise "Trying to remove ships when there are not enough"
        else:
            self.ships[player] -= ships

    def numOfShips(self, player):
        if player not in self.ships.keys():
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
        enemyShips = []
        for (spacePlayer, ships) in self.ships.items():
            if spacePlayer != player and ships > 0:
                enemyShips.append((spacePlayer, ships))
        return enemyShips

    def addPlanet(self, player, planet):
        if player not in self.planets.keys():
            self.planets[player] = []
        self.planets[player].append(planet)

    def getPlayersPlanets(self, player):
        return self.planets[player]

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
        if self.findSpace(pos):
            raise "Trying to place new space where a space already exists (%d, %d)" % (x,y)
        else:
            self.spaces[pos] = space

    def findSpace(self, pos):
        if pos in self.spaces.keys():
            return self.spaces[pos]
        else:
            return None
        
    def getAdjacent(self, (x, y)):
        # 1 2
        # 0 x 5
        #   3 4
        return [((x-1, y), self.findSpace((x-1, y))), ((x-1, y-1), self.findSpace((x-1, y-1))), ((x, y-1), self.findSpace((x, y-1))),
               ((x, y+1), self.findSpace((x, y+1))), ((x+1, y+1), self.findSpace((x+1, y+1))), ((x+1, y), self.findSpace((x+1, y)))]

    def plot(self):
        output = ''
        # find board bounds
        #print "self.spaces %s" % str(self.spaces)
         
        minX = sorted([x for ((x, y), space) in self.spaces.items()])[0]
        minY = sorted([y for ((x, y), space) in self.spaces.items()])[0]
        maxX = sorted([x for ((x, y), space) in self.spaces.items()])[-1]
        maxY = sorted([y for ((x, y), space) in self.spaces.items()])[-1]
        #print("xMin: %d xMax: %d yMin: %d yMax: %d" % (minX, maxX, minY, maxY))
        for j in range(minY, maxY + 1):
            for i in range(minX, maxX + 1):
                foundPlanet = False
                for ((x, y), space) in self.spaces.items():
                    if x == i and j == y:
                        if space.getNumPlanets() > 0:
                            output += str(space.getNumPlanets())
                        else:
                            output += '.'
                        foundPlanet = True
                        break
                if not foundPlanet:
                    output += ' '
            output += '\n'
        return output

class Player:
    def __init__(self, playerNum, startingPlanets):
        self.playerNum = playerNum
        self.minerals = 3
        self.energy = 3
        self.influence = 0
        self.actionQueue = []
        self.remainingShips = 20-3
        self.planets = startingPlanets

    def getPlayerNum(self):
        return self.playerNum

    def getEnergy(self):
        return self.energy
    
    def getMinerals(self):
        return self.minerals

    def takeEnergy(self, num):
        self.energy -= num

    def takeMinerals(self, num):
        self.minerals -= num

    def pickCard(self, hand):
        if (self.minerals < 10 or self.energy < 10) and ActionCards.PRODUCE in hand:
            hand.remove(ActionCards.PRODUCE)
            self.actionQueue.append(ActionCards.PRODUCE)
        elif self.remainingShips > 0 and ActionCards.BUILD in hand:
            hand.remove(ActionCards.BUILD)
            self.actionQueue.append(ActionCards.BUILD)
        elif ActionCards.EXPLORE in hand:
            hand.remove(ActionCards.EXPLORE)
            self.actionQueue.append(ActionCards.EXPLORE)
        elif ActionCards.DISBAND in hand:
            hand.remove(ActionCards.DISBAND)
            self.actionQueue.append(ActionCards.DISBAND)
        else:
            self.actionQueue.append(hand.pop())
        return hand

    def tick(self, game):
        # reveal cards from queue left-to-right
        card = self.actionQueue.pop(0)
        game.log('player %d playing %s' % (self.playerNum, ActionCards.getName(card)))
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

    @staticmethod
    def scorePlanet(planet):
        return planet.getProduceEnergy() + planet.getProduceMinerals() * 0.7 - planet.getInvadeEnergy() - planet.getInvadeMinerals() - planet.getInvadeInfluence() * 1.5

    def explore(self, game):
        # any ships next to an empty space?
        for (pos,space) in game.getBoard().getSpaces().items():
            if space.numOfShips(self) > 0:
                game.log("Player %d exploring from %s" % (self.playerNum, str(pos)))
                adj = game.getBoard().getAdjacent(pos)
                # sort adjacent positions to eliminate any directional bias
                random.shuffle(adj)
                for (pos, exploreSpace) in adj:
                    if exploreSpace is None:
                        # reveal the topmost hex and place it
                        newSpace = game.drawSpace()
                        game.getBoard().addSpace(newSpace, pos)
                        game.log("Player %d revealing space with %d planets" % (self.playerNum, newSpace.getNumPlanets()))
                        # decide how many ships to move
                        numShips = space.numOfShips(self)
                        if newSpace is not None and newSpace.getNumPlanets() > 0:
                            planetCards = game.drawPlanetCards(newSpace.getNumPlanets() + 1)
                            numPlanetsToKeep = min(newSpace.getNumPlanets(), numShips)
                            # take planets cards and score them
                            scores = []
                            for planetCard in planetCards:
                                scores.append((Player.scorePlanet(planetCard), planetCard))
                            newPlanets = [p for (s, p) in scores[-numPlanetsToKeep:]]
                            # move ships from the exploring space to the new planets
                            for planetCard in newPlanets:
                                planetCard.setSpace(space)
                                space.removeShips(self, 1)
                                planetCard.addShips(self, 1)
                                self.planets.append(planetCard)
                                game.log("Added ship to planet %s" % planetCard.getName())
                        else:
                            # no planets to explore. Move one ship into the space
                            space.removeShips(self, 1)
                            newSpace.addShips(self, 1)
                            game.log('No planets in space. Moved one ship')
                        # either moved ships or got planets. Nothing else to do
                        game.log(game.getBoard().plot())
                        return 
        game.log("Player %d did not have any ships available to explore" % self.playerNum)

    def chooseTactic(self, space):
        pass

    @staticmethod
    def resolveAttack(space, attacker, defender, attackerTactic, defenderTactic):
        pass

    def moveAttack(self, game):
        # any opponent ships in an adjacent space?
        for (pos,space) in game.getBoard().getSpaces().items():
            if space.numOfShips(self) > 0:
                for (adjPos, adjSpace) in game.getBoard().getAdjacent(pos):
                    if adjSpace is not None and adjSpace.numOfEnemyShips(self) > 0:
                        game.log("Player %d moving %d ships from %s to %s" % (self.playerNum, 1, str(pos), str(adjPos)))
                        space.removeShips(self, 1)
                        adjSpace.addShips(self, 1)
                        (defender, defenderShips) = adjSpace.getEnemyShips(self)[0]
                        defenderTactic = defender.chooseTactic(defenderShips)
                        attackerTactic = self.chooseTactic(1)
                        game.log("Combat initiated")
                        Player.resolveAttack(adjSpace, self, defender, attackerTactic, defenderTactic)
                        # combat resolved, nothing left to do
                        return
        # if we got here, then there was no combat
        # any ships need to explore?
        #   move ships closer to adjacent space

    def invade(self, game):
        # any ships in space with opponent planet?
        #   pay invasion cost
        #   remove opponent ships
        #   place ships
        pass

    def defend(self, game):
        # any ships in space with planet?
        #   move ships to planet
        pass

    def disband(self, game):
        # find planet with most ships
        planet = sorted(self.planets, key = lambda p: p.numOfShips(self))[-1:][0]
        # move ships to space
        numShips = planet.numOfShips(self)
        planet.removeShips(self, numShips)
        planet.getSpace().addShips(self, numShips)
        game.log("Player %d moved %d ships from %s to its space" % (self.playerNum, numShips, planet.getName()))

    def build(self, game):
        # have enough resources to build?
        if self.minerals > 2 and self.energy > 3 and self.remainingShips > 0:
            #   pick planet with highest build
            planet = sorted(self.planets, key = lambda p: p.getBuildShips())[-1:][0]
            # pay energy and minerals
            self.energy -= 3
            self.minerals -= 2
            #   take ships from pool and put them on planet
            numShips = min(planet.getBuildShips(), self.remainingShips)
            self.remainingShips -= numShips
            planet.addShips(self, numShips)
            game.log("Player %d built %d ships on %s which now has %d ships" % (self.playerNum, numShips, planet.getName(), planet.numOfShips(self)))

    def research(self, game):
        pass

    def produce(self, game):
        maxPlanet = None
        # have more energy than minerals?
        if self.minerals < self.energy:
        #   find planet with most mineral production
            for planet in self.planets:
                if not maxPlanet or planet.getProduceMinerals() > maxPlanet.getProduceMinerals():
                    maxPlanet = planet
        else:
        #   find planet with most energy production
            for planet in self.planets:
                if not maxPlanet or planet.getProduceEnergy() > maxPlanet.getProduceEnergy():
                    maxPlanet = planet
        # produce from planet
        self.energy += maxPlanet.getProduceEnergy()
        self.minerals += maxPlanet.getProduceMinerals()
        self.influence += maxPlanet.getProduceInfluence()
        game.log('Player %d now has %d energy, %d minerals, %d influence' % (self.playerNum, self.energy, self.minerals, self.influence))

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
        if self.influence > 2:
        #   steal to have equal energy and minerals
            numEnergyWished = max(self.minerals - self.energy, 0)
            numMineralsWished = max(self.energy - self.minerals, 0)
            opponent = game.getOpponents(self)[0]
            opponentEnergy = opponent.getEnergy()
            opponentMinerals = opponent.getMinerals()
            numEnergyWished = min(opponentEnergy, numEnergyWished, 3)
            numMineralsWished = min(opponentMinerals, numMineralsWished, 2)
            opponent.takeEnergy(numEnergyWished)
            opponent.takeMinerals(numMineralsWished)
            self.energy += numEnergyWished
            self.minerals += numMineralsWished
            self.influence -= 2
            game.log("Player %d took %d energy %d minerals from player %d who now has %d energy %d minerals" %
                (self.playerNum, numEnergyWished, numMineralsWished, opponent.getPlayerNum(), opponent.getEnergy(), opponent.getMinerals()))
    
    def getActionQueue(self):
        return self.actionQueue

    def isActionQueueEmpty(self):
        return len(self.actionQueue) <= 0

    def getPlanets(self):
        return self.planets

class ActionCards:
    @staticmethod
    def getName(card):
        if card == ActionCards.EXPLORE:
            return "Explore"
        elif card == ActionCards.MOVE_ATTACK:
            return "Move/Attack"
        elif card == ActionCards.INVADE:
            return "Invade"
        elif card == ActionCards.DEFEND:
            return "Defend"
        elif card == ActionCards.DISBAND:
            return "Disband"
        elif card == ActionCards.BUILD:
            return "Build"
        elif card == ActionCards.RESEARCH:
            return "Research"
        elif card == ActionCards.PRODUCE:
            return "Produce"
        elif card == ActionCards.TRADE:
            return "Trade"
        elif card == ActionCards.SABOTAGE:
            return "Sabotage"
        elif card == ActionCards.ESPIONAGE:
            return "Espionage"
        elif card == ActionCards.COUP:
            return "Coup"
        elif card == ActionCards.ELECTION:
            return "Election"
        elif card == ActionCards.POLITICS:
            return "Politics"
        elif card == ActionCards.CORRUPTION:
            return "Corruption"
        else:
            raise "Unknown card type given; %d" % card

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
        self.planetCards = self.initPlanetCards()
        self.technologyCards = self.initTechnologyCards()
        self.resolutionCards = self.initResolutionCards()
        self.playerOne = Player(1, sorted(self.drawPlanetCards(3), key = Player.scorePlanet)[-2:])
        self.players = [self.playerOne, Player(2, sorted(self.drawPlanetCards(3), key = Player.scorePlanet)[-2:])]
        self.playerOrder = itertools.cycle(self.players)
        self.board = Board(len(self.players))
        self.rounds = 0
        playerStartingPos = [None, (-1, 0), (1, 0)]
        for player in self.players:
            startingPos = playerStartingPos[player.getPlayerNum()]
            # place player ships on planet cards and one each on starting space
            for planet in player.getPlanets():
                # place planet cards on spaces
                space = self.board.findSpace(startingPos)
                space.addPlanet(player, planet)
                planet.setSpace(space)
                # start with one ship on each planet
                planet.addShips(player, 1)
            # start with one ship on starting space
            self.board.findSpace(startingPos).addShips(player, 1)
            
        self.spaces = self.initSpaces()
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
                planetCards.append(PlanetCard(row[0], int(row[5]), int(row[6]), int(row[7]), int(row[8]), int(row[1]), int(row[2]), int(row[3])))
        return planetCards

    def initTechnologyCards(self):
        return []

    def initResolutionCards(self):
        return []

    def initSpaces(self):
        spaces = []
        for i in range(10):
            spaces.append(Space(0))
        for i in range(10):
            spaces.append(Space(1))
        for i in range(10):
            spaces.append(Space(2))
        for i in range(3):
            spaces.append(Space(3))
        random.shuffle(spaces)
        return spaces

    def log(self, msg):
        # print msg
        self.logRecord.append(str(msg))

    def getBoard(self):
        return self.board

    def getLog(self):
        return '\n'.join(self.logRecord)

    def getOpponents(self, player):
        opponents = []
        for otherPlayer in self.players:
            if otherPlayer != player:
                opponents.append(otherPlayer)
        return opponents

    def getPlayers(self):
        return self.players

    def getWinner(self):
        for player in self.players:
            if len(player.getPlanets()) >= 8:
                return player
        return None

    def hasWinner(self):
        return self.getWinner() != None

    def numOfRounds(self):
        return self.rounds

    def drawSpace(self):
        if len(self.spaces) > 0:
            return self.spaces.pop(0)
        else:
            return None

    def drawPlanetCards(self, num):
        cards = []
        for i in range(min(num,  len(self.planetCards))):
            cards.append(self.planetCards.pop())
        return cards

    def tick(self):
        self.rounds += 1
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
                hands = collections.deque([self.players[j].pickCard(hands[j]) for j in range(0, len(self.players))])
                hands.rotate(1)

            self.log('action queues: %s' % str([self.players[i].getActionQueue() for i in range(len(self.players))]))
        for player in self.players:
            player.tick(self)

def runGame():
    maxRounds = 500
    game = Game()
    game.log('Start of game')
    while not game.hasWinner() and game.numOfRounds() < maxRounds:
        game.tick()
    if game.getWinner() != None:
        game.log("Player %d has won after %d rounds" % (game.getWinner().getPlayerNum(), game.numOfRounds()))
    else:
        game.log("Stopped after 500 rounds due to bordom")
        for player in game.getPlayers():
            game.log("Player %d has %d planets" % (player.getPlayerNum(), len(player.getPlanets())))
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
        print game.getBoard().plot()

if __name__ == "__main__":
    main()
