import random
import math
from tilesetLoad import *

########################################################################################################################
#Define Enemy base class
class Enemy(object):
    spot = (0,0)

    def __init__(self):
        pass

    def attack(self, other):
        pass

    def draw(self):
        pass

    def spawn(self):
        pass

    def die(self):
        pass

    def takeTurn(self):
        pass

########################################################################################################################
#Define Slimes
class Slime(Enemy):
    mapChar = "s"

    def __init__(self):
        self.health = 5
        self.maxHealth = 5
        self.evasion = .1
        self.strength = 3.5
        self.defense = 2.5

    #Define attack method for Slime
    def attack(self, other):
        hitChance = float(random.randint(0,10) / 10.0)
        if hitChance > other.evasion:
            defenseMultiplier = 0
            if other.inventory["Armor"] == "Cloth":
                defenseMultiplier = 1
            elif other.inventory["Armor"] == "Leather":
                defenseMultiplier = 1.5
            elif other.inventory["Armor"] == "Iron":
                defenseMultiplier = 2
            elif other.inventory["Armor"] == "Steel":
                defenseMultiplier = 2.5
            elif other.inventory["Armor"] == "Kevlar":
                defenseMultiplier = 3
            elif other.inventory["Armor"] == "Mythril":
                defenseMultiplier = 4
            elif other.inventory["Armor"] == "Adamantium":
                defenseMultiplier = 5
            other.health -= int(self.strength ** 2 / (other.defense * defenseMultiplier)) + 1

    def distFromPlayer(self, (r, c), player):
        return math.sqrt(((player.spot[1]) - c) ** 2 + ((player.spot[0]) - r) ** 2)

    #Define drawing for the Slimes
    def draw(self, player):
        if self.distFromPlayer(self.spot, player) < 6:
            center = (width / 2, height / 2) #Center spot in the window (x, y)
            drawFrom = (center[0] - (player.spot[1] * 64) - 32, center[1] - (player.spot[0] * 64) - 32) #The Player should be the middle of the window
            drawSpot = (drawFrom[0] + (self.spot[1] * 64), drawFrom[1] + (self.spot[0] * 64))
            #pygame.draw.rect(screen, MAGENTA, [self.spot[1] * 64, self.spot[0] * 64, 64, 64])
            #screen.blit(basicSlime, (self.spot[1] * 64, self.spot[0] * 64))
            screen.blit(basicSlime, (drawSpot[0], drawSpot[1]))

    #Define the spawning mechanism
    def spawn(self, floor):
        for r in range(len(floor.spaces)):
            for c in range(len(floor.spaces[r])):
                placementChance = random.randint(1, 100)
                if placementChance == 50 and floor.spaces[r][c] == ".":
                    self.spot = (r, c) #(y, x)

    #Define the dying mechanism
    def die(self, player):
        player.exp += 1

    #Define a turn taking mechanism
    def takeTurn(self, floor, player):
        if player.spot == (self.spot[0] + 1, self.spot[1]) or player.spot == (self.spot[0] - 1, self.spot[1]) or player.spot == (self.spot[0], self.spot[1] + 1) or player.spot == (self.spot[0], self.spot[1] - 1):
            self.attack(player)
            print "Slime attacks"
        else:
            moved = 0
            while not moved:
                moveDir = random.randint(0,3)
                if moveDir == 0:
                    #Move up
                    if floor.spaces[self.spot[0] - 1][self.spot[1]] == ".":
                        self.spot = (self.spot[0] - 1, self.spot[1])
                        moved = 1
                elif moveDir == 1:
                    #Move down
                    if floor.spaces[self.spot[0] + 1][self.spot[1]] == ".":
                        self.spot = (self.spot[0] + 1, self.spot[1])
                        moved = 1
                elif moveDir == 2:
                    #Move right
                    if floor.spaces[self.spot[0]][self.spot[1] + 1] == ".":
                        self.spot = (self.spot[0], self.spot[1] + 1)
                        moved = 1
                elif moveDir == 3:
                    #Move left
                    if floor.spaces[self.spot[0]][self.spot[1] - 1] == ".":
                        self.spot = (self.spot[0], self.spot[1] - 1)
                        moved = 1

########################################################################################################################
#Define Rats
class Rat(Enemy):
    mapChar = "r"

    def __init__(self):
        self.health = 6
        self.maxHealth = 6
        self.evasion = .15
        self.strength = 4.5
        self.defense = 3

    #Define the attack mechanism for Rats
    def attack(self, other):
        hitChance = float(random.randint(0,10) / 10.0)
        if hitChance > other.evasion:
            defenseMultiplier = 0
            if other.inventory["Armor"] == "Cloth":
                defenseMultiplier = 1
            elif other.inventory["Armor"] == "Leather":
                defenseMultiplier = 1.5
            elif other.inventory["Armor"] == "Iron":
                defenseMultiplier = 2
            elif other.inventory["Armor"] == "Steel":
                defenseMultiplier = 2.5
            elif other.inventory["Armor"] == "Kevlar":
                defenseMultiplier = 3
            elif other.inventory["Armor"] == "Mythril":
                defenseMultiplier = 4
            elif other.inventory["Armor"] == "Adamantium":
                defenseMultiplier = 5
            other.health -= int(self.strength ** 2 / (other.defense * defenseMultiplier)) + 1

    def distFromPlayer(self, (r, c), player):
        return math.sqrt(((player.spot[1]) - c) ** 2 + ((player.spot[0]) - r) ** 2)

    #Define drawing for the Rats
    def draw(self, player):
        if self.distFromPlayer(self.spot, player) < 6:
            center = (width / 2, height / 2) #Center spot in the window (x, y)
            drawFrom = (center[0] - (player.spot[1] * 64) - 32, center[1] - (player.spot[0] * 64) - 32) #The Player should be the middle of the window
            drawSpot = (drawFrom[0] + (self.spot[1] * 64), drawFrom[1] + (self.spot[0] * 64))
            #pygame.draw.rect(screen, CYAN, [self.spot[1] * 64, self.spot[0] * 64, 64, 64])
            #screen.blit(basicRat, (self.spot[1] * 64, self.spot[0] * 64))
            screen.blit(basicRat, (drawSpot[0], drawSpot[1]))

    #Define the spawning mechanism
    def spawn(self, floor):
        for r in range(len(floor.spaces)):
            for c in range(len(floor.spaces[r])):
                placementChance = random.randint(1, 100)
                if placementChance == 50 and floor.spaces[r][c] == ".":
                    self.spot = (r, c) #(y, x)

    #Define the dying mechanism
    def die(self, player):
        player.exp += 2

    #Define a turn taking mechanism
    def takeTurn(self, floor, player):
        if player.spot == (self.spot[0] + 1, self.spot[1]) or player.spot == (self.spot[0] - 1, self.spot[1]) or player.spot == (self.spot[0], self.spot[1] + 1) or player.spot == (self.spot[0], self.spot[1] - 1):
            self.attack(player)
            print "Rat attacks"
        else:
            moved = 0
            while not moved:
                moveDir = random.randint(0,3)
                if moveDir == 0:
                    #Move up
                    if floor.spaces[self.spot[0] - 1][self.spot[1]] == ".":
                        self.spot = (self.spot[0] - 1, self.spot[1])
                        moved = 1
                elif moveDir == 1:
                    #Move down
                    if floor.spaces[self.spot[0] + 1][self.spot[1]] == ".":
                        self.spot = (self.spot[0] + 1, self.spot[1])
                        moved = 1
                elif moveDir == 2:
                    #Move right
                    if floor.spaces[self.spot[0]][self.spot[1] + 1] == ".":
                        self.spot = (self.spot[0], self.spot[1] + 1)
                        moved = 1
                elif moveDir == 3:
                    #Move left
                    if floor.spaces[self.spot[0]][self.spot[1] - 1] == ".":
                        self.spot = (self.spot[0], self.spot[1] - 1)
                        moved = 1

########################################################################################################################
#Define Invincirat
class Invincirat(Enemy):
    mapChar = "R"
    spot = (7, 5) #(y,x)

    def __init__(self):
        self.health = 15
        self.maxHealth = 15
        self.evasion = .2
        self.strength = 6
        self.defense = 5

    #Define the attack mechanism for Invincirat
    def attack(self, other):
        hitChance = float(random.randint(0,10) / 10.0)
        if hitChance > other.evasion:
            defenseMultiplier = 0
            if other.inventory["Armor"] == "Cloth":
                defenseMultiplier = 1
            elif other.inventory["Armor"] == "Leather":
                defenseMultiplier = 1.5
            elif other.inventory["Armor"] == "Iron":
                defenseMultiplier = 2
            elif other.inventory["Armor"] == "Steel":
                defenseMultiplier = 2.5
            elif other.inventory["Armor"] == "Kevlar":
                defenseMultiplier = 3
            elif other.inventory["Armor"] == "Mythril":
                defenseMultiplier = 4
            elif other.inventory["Armor"] == "Adamantium":
                defenseMultiplier = 5
            other.health -= int(self.strength ** 2 / (other.defense * defenseMultiplier)) + 1

    def distFromPlayer(self, (r, c), player):
        return math.sqrt(((player.spot[1]) - c) ** 2 + ((player.spot[0]) - r) ** 2)

    #Define drawing for Invincirat
    def draw(self, player):
        if self.distFromPlayer(self.spot, player) < 6:
            center = (width / 2, height / 2) #Center spot in the window (x, y)
            drawFrom = (center[0] - (player.spot[1] * 64) - 32, center[1] - (player.spot[0] * 64) - 32) #The Player should be the middle of the window
            drawSpot = (drawFrom[0] + (self.spot[1] * 64), drawFrom[1] + (self.spot[0] * 64))
            #pygame.draw.rect(screen, CYAN, [self.spot[1] * 64, self.spot[0] * 64, 64, 64])
            #screen.blit(basicInvincirat, (self.spot[1] * 64, self.spot[0] * 64))
            screen.blit(basicInvincirat, (drawSpot[0], drawSpot[1]))

    #Define spawning for Invincirat
    def spawn(self):
        pass

    #Define dying for Invincirat
    def die(self, player):

        #Increase Player's Exp
        player.exp += 15

        #Upgrade Player's Weapon
        if player.inventory["Weapon"] == "Wooden":
            player.inventory["Weapon"] = "Stone"
        elif player.inventory["Weapon"] == "Stone":
            player.inventory["Weapon"] = "Iron"
        elif player.inventory["Weapon"] == "Iron":
            player.inventory["Weapon"] = "Steel"
        elif player.inventory["Weapon"] == "Steel":
            player.inventory["Weapon"] = "Mythril"
        elif player.inventory["Weapon"] == "Mythril":
            player.inventory["Weapon"] = "Adamantium"
        elif player.inventory["Weapon"] == "Stone":
            player.inventory["Weapon"] = "Iron"

        #Upgrade Player's Armor
        if player.inventory["Armor"] == "Cloth":
            player.inventory["Armor"] = "Leather"
        elif player.inventory["Armor"] == "Leather":
            player.inventory["Armor"] = "Iron"
        elif player.inventory["Armor"] == "Iron":
            player.inventory["Armor"] = "Steel"
        elif player.inventory["Armor"] == "Steel":
            player.inventory["Armor"] = "Kevlar"
        elif player.inventory["Armor"] == "Kevlar":
            player.inventory["Armor"] = "Mythril"
        elif player.inventory["Armor"] == "Mythril":
            player.inventory["Armor"] = "Adamantium"

        #Give the player 500 Gold
        player.inventory["Gold"] += 500

    #Define a turn taking mechanism
    def takeTurn(self, floor, player):
        if player.spot == (self.spot[0] + 1, self.spot[1]) or player.spot == (self.spot[0] - 1, self.spot[1]) or player.spot == (self.spot[0], self.spot[1] + 1) or player.spot == (self.spot[0], self.spot[1] - 1):
            self.attack(player)
            print "Invincirat attacks"
        else:
            moved = 0
            while not moved:
                moveDir = random.randint(0,3)
                if moveDir == 0:
                    #Move up
                    if floor.spaces[self.spot[0] - 1][self.spot[1]] == ".":
                        self.spot = (self.spot[0] - 1, self.spot[1])
                        moved = 1
                elif moveDir == 1:
                    #Move down
                    if floor.spaces[self.spot[0] + 1][self.spot[1]] == ".":
                        self.spot = (self.spot[0] + 1, self.spot[1])
                        moved = 1
                elif moveDir == 2:
                    #Move right
                    if floor.spaces[self.spot[0]][self.spot[1] + 1] == ".":
                        self.spot = (self.spot[0], self.spot[1] + 1)
                        moved = 1
                elif moveDir == 3:
                    #Move left
                    if floor.spaces[self.spot[0]][self.spot[1] - 1] == ".":
                        self.spot = (self.spot[0], self.spot[1] - 1)
                        moved = 1
