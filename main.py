import pygame
import random
import math

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
            self.health = 15
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
    def drawPlayer(self):
        #pygame.draw.rect(screen, RED, [self.spot[1] * 64, self.spot[0] * 64, 64, 64])
        center = (width / 2, height / 2) #Center spot in the window (x, y)
        screen.blit(basicPlayer, (center[0], center[1]))
        #screen.blit(basicPlayer, (self.spot[1] * 64, self.spot[0] * 64))

    def findAdjacentEnemy(self, direction):
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

########################################################################################################################
#Define Floor Class
class Floor(object):
    #The floor spaces
    spaces = []
    def __init__(self):
        self.spaces = []

    #Define floor template creation
    def create(self, x, y):
        if x % 2 == 0:
            x += 1
        if y % 2 == 0:
            y += 1
        for i in range(y):
            self.spaces.append([])
            for j in range(x):
                if j % 2 == 0 or i == 0 or i == y - 1 or i % 2 == 0:
                    self.spaces[i].append("#")
                elif j % 2 == 1:
                    self.spaces[i].append("&")

    def generate(self, x, y):
        self.create(x,y)
        roomAttempts = (x * y) / 4
        for a in range(roomAttempts):
            rx = random.randint(0, x) #Random x placement
            ry = random.randint(0, y) #Random y placement
            rw = random.randint(4, x / 2) #Random width
            rh = random.randint(4, y / 2) #Random height
            if rx + rw < x and ry + rh < y:
                if self.checkRoom(rx, ry, rw, rh):
                    self.createRoom(rx, ry, rw, rh)

        #Check again from other spots
        for r in range(len(self.spaces)):
            for c in range(len(self.spaces)):
                spots = []
                if self.spaces[r][c] == "&":
                    spots.append((r, c))
                while spots:
                    loc = spots[len(spots) - 1]
                    neighbors = []
                    neighborA = (loc[0] + 2, loc[1]) #The spot below
                    neighborB = (loc[0] - 2, loc[1]) #The spot above
                    neighborC = (loc[0], loc[1] - 2) #The spot to the right
                    neighborD = (loc[0], loc[1] + 2) #The spot to the left
                    #Check neighbors
                    if self.isValid(neighborA):
                        neighbors.append(neighborA)
                    if self.isValid(neighborB):
                        neighbors.append(neighborB)
                    if self.isValid(neighborC):
                        neighbors.append(neighborC)
                    if self.isValid(neighborD):
                        neighbors.append(neighborD)
                    #Pop the spot if it has no neighbors
                    if len(neighbors) == 0:
                        spots.pop()
                    else:
                        randSpot = random.randint(0, 3) % len(neighbors)
                        if randSpot == 0:
                            spots.append(neighbors[0])
                            self.spaces[neighbors[0][0]][neighbors[0][1]] = "."
                            mid = ((loc[0] + neighbors[0][0]) / 2, (loc[1] + neighbors[0][1]) / 2)
                            self.spaces[mid[0]][mid[1]] = "."
                        elif randSpot == 1:
                            spots.append(neighbors[1])
                            self.spaces[neighbors[1][0]][neighbors[1][1]] = "."
                            mid = ((loc[0] + neighbors[1][0]) / 2, (loc[1] + neighbors[1][1]) / 2)
                            self.spaces[mid[0]][mid[1]] = "."
                        elif randSpot == 2:
                            spots.append(neighbors[2])
                            self.spaces[neighbors[2][0]][neighbors[2][1]] = "."
                            mid = ((loc[0] + neighbors[2][0]) / 2, (loc[1] + neighbors[2][1]) / 2)
                            self.spaces[mid[0]][mid[1]] = "."
                        elif randSpot == 3:
                            spots.append(neighbors[3])
                            self.spaces[neighbors[3][0]][neighbors[3][1]] = "."
                            mid = ((loc[0] + neighbors[3][0]) / 2, (loc[1] + neighbors[3][1]) / 2)
                            self.spaces[mid[0]][mid[1]] = "."

        #Set any straggling blocks
        for r in range(len(self.spaces)):
            for s in range(len(self.spaces[r])):
                if self.spaces[r][s] == "&":
                    self.spaces[r][s] = "."
                elif self.spaces[r][s] == "#":
                    self.spaces[r][s] = "X"

    #Define a space checking function
    def isValid(self, (y,x)):
        if y > 0 and y < len(self.spaces) and x > 0 and x < len(self.spaces[0]):
            if self.spaces[y][x] == "&":
                return True
        return False

    #Checks if space for the room is available
    def checkRoom(self, rx, ry, rw, rh):
        for y in range(rh):
            for x in range(rw):
                if self.spaces[ry + y][rx + x] == "." or self.spaces[ry + y][rx + x] == "X":
                    return False
        return True

    #Creates a room on the map
    def createRoom(self, rx, ry, rw, rh):
        doorOnLeft = 0
        doorOnRight = 0
        doorTop = 0
        doorBottom = 0

        #Creates the room first
        for y in range(rh):
            for x in range(rw):
                if y == 0 or x == 0 or y == rh - 1 or x == rw - 1:
                    self.spaces[ry + y][rx + x] = 'X'
                else:
                    self.spaces[ry + y][rx + x] = '.'

        #Adds doors to the room
        #Left door
        if rx != 0:
            for y in range(rh):
                if y == 0:
                    continue
                if y == rh - 1:
                    break
                doorChance = random.randint(1,4)
                if doorChance == 2:
                    if self.spaces[ry + y][rx - 1] == "&":
                        self.spaces[ry + y][rx] = "d"
                        break
                    elif self.spaces[ry + y][rx - 1] == "#" and rx > 1:
                        self.spaces[ry + y][rx] = "d"
                        self.spaces[ry + y][rx - 1] = "."
                        break
        #Right door
        if rx != len(self.spaces[0]) - 1:
            for y in range(rh):
                if y == 0:
                    continue
                if y == rh - 1:
                    break
                doorChance = random.randint(1,4)
                if doorChance == 2:
                    if self.spaces[ry + y][rx + rw] == "&":
                        self.spaces[ry + y][rx + rw - 1] = "d"
                        break
                    elif self.spaces[ry + y][rx + rw] == "#" and rx <= len(self.spaces[0]) - 2:
                        self.spaces[ry + y][rx + rw - 1] = "d"
                        self.spaces[ry + y][rx + rw] = "."
                        break
        #Top door
        if ry != 0:
            for x in range(rw):
                if x == 0:
                    continue
                if x == rw - 1:
                    break
                doorChance = random.randint(1,4)
                if doorChance == 2:
                    if self.spaces[ry - 1][rx + x] == "&":
                        self.spaces[ry][rx + x] = "d"
                        break
                    elif self.spaces[ry - 1][rx + x] == "#" and ry > 1:
                        self.spaces[ry][rx + x] = "d"
                        self.spaces[ry - 1][rx + x] = "."
                        break
        #Bottom door
        if ry != len(self.spaces) - 1:
            for x in range(rw):
                if x == 0:
                    continue
                if x == rw - 1:
                    break
                doorChance = random.randint(1,3)
                if doorChance == 2:
                    if self.spaces[ry + rh][rx + x] == "&":
                        self.spaces[ry + rh - 1][rx + x] = "d"
                        break
                    elif self.spaces[ry + rh][rx + x] == "#" and ry < len(self.spaces) - 2:
                        self.spaces[ry + rh - 1][rx + x] = "d"
                        self.spaces[ry + rh][rx + x] = "."
                        break

    def distFromPlayer(self, (r, c)):
        return math.sqrt(((player.spot[1]) - c) ** 2 + ((player.spot[0]) - r) ** 2)

    #Define floor printing (Terminal)
    def printFloor(self):
        for i in range(len(self.spaces)): #/ len(self.spaces[0])): #Rows / y values
            for j in range(len(self.spaces[i])): #Columns / x values
                print self.spaces[i][j],
            print ""

    #Define floor drawing (Graphics)
    #TODO
    #Change # to X and & to . when map generation is finished
    def drawFloor(self):
        center = (width / 2, height / 2) #Center spot in the window (x, y)
        drawFrom = (center[0] - (player.spot[1] * 64), center[1] - (player.spot[0] * 64)) #The Player should be the middle of the window
        for i in range(len(self.spaces)): #Rows / y values
            for j in range(len(self.spaces[i])): #Columns / x values
                if self.distFromPlayer((i,j)) < 6:
                    drawSpot = (drawFrom[0] + (j * 64), drawFrom[1] + (i * 64))
                    if self.spaces[i][j] == "X":
                        #pygame.draw.rect(screen, GREEN, [j * 64, i * 64, 64, 64])
                        screen.blit(basicWall, (drawSpot[0], drawSpot[1]))
                        #screen.blit(basicWall, (j * 64, i * 64))
                    elif self.spaces[i][j] == ".":
                        #pygame.draw.rect(screen, BLUE, [j * 64, i * 64, 64, 64])
                        screen.blit(basicTile, (drawSpot[0], drawSpot[1]))
                        #screen.blit(basicTile, (j * 64, i * 64))
                    elif self.spaces[i][j] == "d":
                        screen.blit(basicTile, (drawSpot[0], drawSpot[1]))
                        screen.blit(basicDoor, (drawSpot[0], drawSpot[1]))
                    else:
                        screen.blit(basicEmpty, (drawSpot[0], drawSpot[1]))

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
            other.health -= int(self.strength ** 2 / (other.defense * defenseMultiplier))

    def distFromPlayer(self, (r, c)):
        return math.sqrt(((player.spot[1]) - c) ** 2 + ((player.spot[0]) - r) ** 2)

    #Define drawing for the Slimes
    def draw(self):
        if self.distFromPlayer(self.spot) < 6:
            center = (width / 2, height / 2) #Center spot in the window (x, y)
            drawFrom = (center[0] - (player.spot[1] * 64), center[1] - (player.spot[0] * 64)) #The Player should be the middle of the window
            drawSpot = (drawFrom[0] + (self.spot[1] * 64), drawFrom[1] + (self.spot[0] * 64))
            #pygame.draw.rect(screen, MAGENTA, [self.spot[1] * 64, self.spot[0] * 64, 64, 64])
            #screen.blit(basicSlime, (self.spot[1] * 64, self.spot[0] * 64))
            screen.blit(basicSlime, (drawSpot[0], drawSpot[1]))

    #Define the spawning mechanism
    def spawn(self):
        for r in range(len(floor.spaces)):
            for c in range(len(floor.spaces[r])):
                placementChance = random.randint(1, 100)
                if placementChance == 50 and floor.spaces[r][c] == ".":
                    self.spot = (r, c) #(y, x)

    #Define the dying mechanism
    def die(self):
        player.exp += 1

    #Define a turn taking mechanism
    def takeTurn(self):
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
            other.health -= int(self.strength ** 2 / (other.defense * defenseMultiplier))

    def distFromPlayer(self, (r, c)):
        return math.sqrt(((player.spot[1]) - c) ** 2 + ((player.spot[0]) - r) ** 2)

    #Define drawing for the Rats
    def draw(self):
        if self.distFromPlayer(self.spot) < 6:
            center = (width / 2, height / 2) #Center spot in the window (x, y)
            drawFrom = (center[0] - (player.spot[1] * 64), center[1] - (player.spot[0] * 64)) #The Player should be the middle of the window
            drawSpot = (drawFrom[0] + (self.spot[1] * 64), drawFrom[1] + (self.spot[0] * 64))
            #pygame.draw.rect(screen, CYAN, [self.spot[1] * 64, self.spot[0] * 64, 64, 64])
            #screen.blit(basicRat, (self.spot[1] * 64, self.spot[0] * 64))
            screen.blit(basicRat, (drawSpot[0], drawSpot[1]))

    #Define the spawning mechanism
    def spawn(self):
        for r in range(len(floor.spaces)):
            for c in range(len(floor.spaces[r])):
                placementChance = random.randint(1, 100)
                if placementChance == 50 and floor.spaces[r][c] == ".":
                    self.spot = (r, c) #(y, x)

    #Define the dying mechanism
    def die(self):
        player.exp += 2

    #Define a turn taking mechanism
    def takeTurn(self):
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
            other.health -= int(self.strength ** 2 / (other.defense * defenseMultiplier))

    def distFromPlayer(self, (r, c)):
        return math.sqrt(((player.spot[1]) - c) ** 2 + ((player.spot[0]) - r) ** 2)

    #Define drawing for Invincirat
    def draw(self):
        if self.distFromPlayer(self.spot) < 6:
            center = (width / 2, height / 2) #Center spot in the window (x, y)
            drawFrom = (center[0] - (player.spot[1] * 64), center[1] - (player.spot[0] * 64)) #The Player should be the middle of the window
            drawSpot = (drawFrom[0] + (self.spot[1] * 64), drawFrom[1] + (self.spot[0] * 64))
            #pygame.draw.rect(screen, CYAN, [self.spot[1] * 64, self.spot[0] * 64, 64, 64])
            #screen.blit(basicInvincirat, (self.spot[1] * 64, self.spot[0] * 64))
            screen.blit(basicInvincirat, (drawSpot[0], drawSpot[1]))

    #Define spawning for Invincirat
    def spawn(self):
        pass

    #Define dying for Invincirat
    def die(self):
        player.exp += 15

    #Define a turn taking mechanism
    def takeTurn(self):
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

########################################################################################################################
#End Objects
#Start Game Program

#Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

#Game Window Size
width = 1280
height = 720
size = (width, height)

#Initialize the Game
pygame.init()

#Create the Game Window
screen = pygame.display.set_mode(size)
pygame.display.set_caption("R@ Slayer v1")
ico = pygame.image.load("Assets/SplashScreen/Icon.png")
pygame.display.set_icon(ico)


#Show splash screen
splash = pygame.image.load("Assets/SplashScreen/fluffyAntennaMKI.png")
screen.blit(splash, (0,0))
pygame.display.flip()
for i in range(2):
    pygame.time.Clock().tick(1)

#Set game mode
#1 = Play
#2 = Main Menu
#3 = Lose
#4 = Win
#5 = Instructions
#6 = Credits

#Game loop variable
done = False

#Game clock
clock = pygame.time.Clock()

#Player Creation
#pType = raw_input("Welcome to Roguelike v1! Please choose a character. (Warrior / Rogue):")
player = Player("Warrior")

#Player regenerates 1 health every 7 steps
healthTick = 7

#Set the game level
level = 1

#Generate the first level
floor = Floor()
floor.generate(30, 30)

#Set maximum enemies
maxEnemies = level * 3

#Create initial mobs
enemies = []

for i in range(maxEnemies):
    enemyNum = random.randint(0,1)
    if enemyNum == 0:
        slime = Slime()
        slime.spawn()
        enemies.append(slime)
    elif enemyNum == 1:
        rat = Rat()
        rat.spawn()
        enemies.append(rat)

#slime = Slime()
#rat = Rat()
#invincirat = Invincirat()
#enemies.append(slime)
#enemies.append(rat)
#enemies.append(invincirat)

#Define placeholder tileset
#REPLACE
basicTile = pygame.image.load("Assets/Placeholder/BasicTile.png")
basicWall = pygame.image.load("Assets/Placeholder/BasicWall.png")
basicEmpty = pygame.image.load("Assets/Placeholder/MossyWall.png")
basicDoor = pygame.image.load("Assets/Placeholder/Door.png")

#Define placeholder entities images
basicRat = pygame.image.load("Assets/Placeholder/Rat.png")
basicSlime = pygame.image.load("Assets/Placeholder/Slime.png")
basicPlayer = pygame.image.load("Assets/Placeholder/Player.png")
basicInvincirat = pygame.image.load("Assets/Placeholder/Invincirat.png")

#Initial drawing
screen.fill(BLACK)
floor.drawFloor()
player.drawPlayer()
for e in enemies:
    e.draw()
pygame.display.flip()

#Main Game Loop
while not done:
    #Main Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_a: #Move left
                eToAttack = player.findAdjacentEnemy("left")
                if eToAttack:
                    player.attack(eToAttack)
                    print "Player attacks"
                elif player.spot[1] - 1 >= 0 and (floor.spaces[player.spot[0]][player.spot[1] - 1] == "." or floor.spaces[player.spot[0]][player.spot[1] - 1] == "d"):
                    player.spot = (player.spot[0], player.spot[1] - 1)
            elif event.key == pygame.K_s: #Move down
                eToAttack = player.findAdjacentEnemy("down")
                if eToAttack:
                    player.attack(eToAttack)
                    print "Player attacks"
                elif player.spot[0] + 1 < len(floor.spaces) and (floor.spaces[player.spot[0] + 1][player.spot[1]] == "." or floor.spaces[player.spot[0] + 1][player.spot[1]] == "d"):
                    player.spot = (player.spot[0] + 1, player.spot[1])
            elif event.key == pygame.K_d: #Move right
                eToAttack = player.findAdjacentEnemy("right")
                if eToAttack:
                    player.attack(eToAttack)
                    print "Player attacks"
                elif player.spot[1] + 1 < len(floor.spaces[player.spot[0]]) and (floor.spaces[player.spot[0]][player.spot[1] + 1] == "." or floor.spaces[player.spot[0]][player.spot[1] + 1] == "d"):
                    player.spot = (player.spot[0], player.spot[1] + 1)
            elif event.key == pygame.K_w: #Move up
                eToAttack = player.findAdjacentEnemy("up")
                if eToAttack:
                    player.attack(eToAttack)
                    print "Player attacks"
                elif player.spot[0] - 1 >= 0 and (floor.spaces[player.spot[0] - 1][player.spot[1]] == "." or floor.spaces[player.spot[0] - 1][player.spot[1]] == "d"):
                    player.spot = (player.spot[0] - 1, player.spot[1])
            elif event.key == pygame.K_SPACE:
                pass

            #Game logic
            healthTick -= 1

            #Player regenerates one health every 7 steps
            if healthTick == 0:
                if player.health < player.maxHealth:
                    player.health += 1
                healthTick = 7

            #Enemies take turns
            for e in enemies:
                if e.health > 0:
                    e.takeTurn()
                else:
                    e.die()
                    enemies.remove(e)

            #Spawn more enemies if below max
            while len(enemies) < maxEnemies:
                enemyNum = random.randint(0,1)
                if enemyNum == 0:
                    slime = Slime()
                    slime.spawn()
                    enemies.append(slime)
                elif enemyNum == 1:
                    rat = Rat()
                    rat.spawn()
                    enemies.append(rat)

            print "P:", player.health
            print "EXP:", player.exp
            #End the game when health reaches zero
            if player.health <= 0:
                done = True

            #Clear the screen
            screen.fill(BLACK)

            #Game drawing
            floor.drawFloor()
            for e in enemies:
                e.draw()
                #slime.drawSlime()
                #rat.drawRat()
            player.drawPlayer()

            #Draw the status bar

            #Update the screen
            pygame.display.flip()

            #Limit to 120 frames per second
            clock.tick(120)

pygame.quit()
