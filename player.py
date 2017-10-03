from tilesetLoad import *
import random
########################################################################################################################
#Define Player Class
class Player(object):
    #Define default values and logistics for Player class

    spot = (1,1) #(y, x)
    inventory = {
    "Armor" : "Cloth",
    "Weapon" : "Wooden",
    "Gold" : 0
    }
    level = 1
    exp = 0

    #Armor Tiers:
    #Cloth - Defense bonus: x1
    #Leather - Defense bonus: x1.5
    #Iron - Defense bonus: x2
    #Steel - Defense bonus: x2.5
    #Kevlar - Defense bonus: x3
    #Mythril - Defense bonus: x4
    #Adamantium - Defense bonus: x5

    #Weapon Tiers:
    #Wooden - Attack bonus: x1
    #Stone - Attack bonus: x1.5
    #Iron - Attack bonus: x2
    #Steel - Attack bonus: x2.5
    #Mythril - Attack bonus: x3
    #Adamantium - Attack bonus: x4

    #Define class specific traits
    def __init__(self, playerType):
        if playerType == "Warrior":
            self.type = "Warrior"
            self.health = 20
            self.maxHealth = 20
            self.evasion = .3
            self.strength = 10
            self.defense = 10
            self.crit = .05
        if playerType == "Rogue":
            self.type = "Rogue"
            self.health = 18
            self.maxHealth = 18
            self.evasion = .6
            self.strength = 10
            self.defense = 8
            self.crit = .2

    #Define the attack method for the player:
    def attack(self, other):
        hitChance = float(random.randint(0,10) / 10.0)
        if hitChance > other.evasion:
            damageMultiplier = 0
            if self.inventory["Weapon"] == "Wooden":
                damageMultiplier = 1
            elif self.inventory["Weapon"] == "Stone":
                damageMultiplier = 1.5
            elif self.inventory["Weapon"] == "Iron":
                damageMultiplier = 2
            elif self.inventory["Weapon"] == "Steel":
                damageMultiplier = 2.5
            elif self.inventory["Weapon"] == "Mythril":
                damageMultiplier = 3
            elif self.inventory["Weapon"] == "Adamantium":
                damageMultiplier = 4
            critMultiplier = 1
            critc = float(random.randint(0,10) / 10)
            if critc > self.crit:
                critMultiplier = 1.5
            other.health -= int((self.strength * critMultiplier * damageMultiplier) / other.defense)

    #Define player drawing method
    def drawPlayer(self, width, height, screen):
        center = (width / 2 - 32, height / 2 - 32) #Center spot in the window (x, y)
        screen.blit(basicPlayer, (center[0], center[1]))

    #Define a method to find if an enemy is adjacent in the attempted direction
    def findAdjacentEnemy(self, direction, enemies):
        for e in enemies:
            if direction == "up":
                if e.spot == (self.spot[0] - 1, self.spot[1]):
                    return e
            elif direction == "down":
                if e.spot == (self.spot[0] + 1, self.spot[1]):
                    return e
            elif direction == "right":
                if e.spot == (self.spot[0], self.spot[1] + 1):
                    return e
            elif direction == "left":
                if e.spot == (self.spot[0], self.spot[1] - 1):
                    return e
        return False

    def spawnUp(self, floor):
        for r in range(len(floor.spaces)):
            for c in range(len(floor.spaces[r])):
                if floor.spaces[r][c] == "<":
                    self.spot = (r, c)

    def spawnDown(self, floor):
        for r in range(len(floor.spaces)):
            for c in range(len(floor.spaces[r])):
                if floor.spaces[r][c] == ">":
                    self.spot = (r, c)
