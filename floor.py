import random
import math
from tilesetLoad import *

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
        #Create a map template
        self.create(x,y)

        #Create Rooms
        roomAttempts = (x * y) / 4
        for a in range(roomAttempts):
            rx = random.randint(0, x) #Random x placement
            ry = random.randint(0, y) #Random y placement
            rw = random.randint(4, x / 2) #Random width
            rh = random.randint(4, y / 2) #Random height
            if rx + rw < x and ry + rh < y:
                if self.checkRoom(rx, ry, rw, rh):
                    self.createRoom(rx, ry, rw, rh)

        #Recursive Backtracking to form the maze
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

        #Replace any missing blocks
        for r in range(len(self.spaces)):
            for s in range(len(self.spaces[r])):
                if self.spaces[r][s] == "&":
                    self.spaces[r][s] = "."
                elif self.spaces[r][s] == "#":
                    self.spaces[r][s] = "X"

        #Create stairs
        upPlaced = False
        downPlaced = False
        for r in range(len(self.spaces)):
            for c in range(len(self.spaces[r])):
                upStair = random.randint(0,50)
                downStair = random.randint(0,50)
                if upStair == 25 and upPlaced == False and self.spaces[r][c] == ".":
                    self.spaces[r][c] = ">"
                    upPlaced = True
                if downStair == 25 and downPlaced == False and self.spaces[r][c] == ".":
                    self.spaces[r][c] = "<"
                    downPlaced = True

        self.printFloor()


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

    def distFromPlayer(self, (r, c), player):
        return math.sqrt(((player.spot[1]) - c) ** 2 + ((player.spot[0]) - r) ** 2)

    #Define floor printing (Terminal)
    def printFloor(self):
        for i in range(len(self.spaces)): #/ len(self.spaces[0])): #Rows / y values
            for j in range(len(self.spaces[i])): #Columns / x values
                print self.spaces[i][j],
            print ""

    #Define floor drawing (Graphics)

    #Change # to X and & to . when map generation is finished
    def drawFloor(self, width, height, screen, player):
        center = (width / 2, height / 2) #Center spot in the window (x, y)
        drawFrom = (center[0] - (player.spot[1] * 64) - 32, center[1] - (player.spot[0] * 64) - 32) #The Player should be the middle of the window

        for i in range(len(self.spaces)): #Rows / y values
            for j in range(len(self.spaces[i])): #Columns / x values
                if self.distFromPlayer((i,j), player) < 6:
                    drawSpot = (drawFrom[0] + (j * 64), drawFrom[1] + (i * 64))
                    if self.spaces[i][j] == "X":
                        screen.blit(basicWall, (drawSpot[0], drawSpot[1]))
                    elif self.spaces[i][j] == ".":
                        screen.blit(basicTile, (drawSpot[0], drawSpot[1]))
                    elif self.spaces[i][j] == "d":
                        screen.blit(basicTile, (drawSpot[0], drawSpot[1]))
                        screen.blit(basicDoor, (drawSpot[0], drawSpot[1]))
                    elif self.spaces[i][j] == "<":
                        screen.blit(basicTile, (drawSpot[0], drawSpot[1]))
                        screen.blit(basicStairDown, (drawSpot[0], drawSpot[1]))
                    elif self.spaces[i][j] == ">":
                        screen.blit(basicTile, (drawSpot[0], drawSpot[1]))
                        screen.blit(basicStairUp, (drawSpot[0], drawSpot[1]))
                    else:
                        screen.blit(basicEmpty, (drawSpot[0], drawSpot[1]))
