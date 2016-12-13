import pygame

#Define Player Class
class Player(object):
    #Define default values and logistics for Player class
    mapChar = "@"
    under = "."
    spot = (1,1) #(y, x)
    inventory = {
    "Armor" : "Cloth",
    "Weapon" : "Wooden",
    "Gold" : 0
    }

    #Define class specific traits
    def __init__(self, playerType):
        if playerType == "Warrior":
            self.type = "Warrior"
            self.health = 20
            self.evasion = .3
            self.strength = 10
            self.defense = 10
        if playerType == "Rogue":
            self.type = "Rogue"
            self.health = 18
            self.evasion = .6
            self.strength = 10
            self.defense = 8
    def drawPlayer(self):
        pygame.draw.rect(screen, RED, [self.spot[1] * 64, self.spot[0] * 64, 64, 64])

class Floor(object):
    #The floor spaces
    spaces = []
    def __init__(self):
        self.spaces = []

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
        #TODO
        #Generate rooms and corridors
        #For floor zero, place door and up stairs
        #Generate downstairs and up stairs
        #For last floor, place door and down stairs
        #Add Gold and enemies

    def printFloor(self):
        #for s in self.spaces:
            #print " ".join(s)
        for i in range(len(self.spaces)): #Rows / y values
            for j in range(len(self.spaces[i])): #Columns / x values
                print self.spaces[i][j],
            print "\n"

    def drawFloor(self):
        for i in range(len(self.spaces)): #Rows / y values
            for j in range(len(self.spaces[i])): #Columns / x values
                if self.spaces[i][j] == "#":
                    pygame.draw.rect(screen, GREEN, [j * 64, i * 64, 64, 64])
                elif self.spaces[i][j] == "&":
                    pygame.draw.rect(screen, BLUE, [j * 64, i * 64, 64, 64])
                    #screen.blit(basicTile, (j * 64, i * 64))

class Enemy(object):
    spot = (0,0)
    def __init__(self):
        pass
    def attack(self, other):
        pass
    def drawEnemy(self):
        pass
    def spawn(self):
        pass

class Slime(Enemy):
    spot = (3,3)
    def __init__(self):
        self.health = 5
        self.evasion = .1
        self.strength = 1
        self.defense = 11
    def attack(self, other):
        pass
        #TODO
        #Decide on a damage scheme
    def drawSlime(self):
        pygame.draw.rect(screen, MAGENTA, [self.spot[1] * 64, self.spot[0] * 64, 64, 64])
    def spawn():
        pass

class Rat(Enemy):
    spot = (5,7)
    def __init__(self):
        self.health = 6
        self.evasion = .15
        self.strength = 1.5
        self.defense = 1.5
    def attack(self, other):
        pass
    def drawRat(self):
        pygame.draw.rect(screen, YELLOW, [self.spot[1] * 64, self.spot[0] * 64, 64, 64])
    def spawn(self):
        pass

#Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

#Game Window Size
width = 1280
height = 720
size = (width, height)

#Initialize the Game
pygame.init()
#Create the Game Window
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Roguelike v1")

#Show splash screen
splash = pygame.image.load("Assets/SplashScreen/fluffyAntennaMKI.png")
screen.blit(splash, (0,0))
pygame.display.flip()
for i in range(2):
    pygame.time.Clock().tick(1)

#Game loop variable
done = False

#Game clock
clock = pygame.time.Clock()

#Player Creation
#pType = raw_input("Welcome to Roguelike v1! Please choose a character. (Warrior / Rogue):")
player = Player("Warrior")

#Generate the first level
floor = Floor()
floor.create(30, 15)
#floor.printFloor()

#Create initial mobs
slime = Slime()
rat = Rat()

#Define the tileset
basicTile = pygame.image.load("Assets/Tiles/BasicTile.png")

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
                if player.spot[1] - 1 >= 0: # and floor[player.spot[0]][player.spot[1] - 1] == "."
                    player.spot = (player.spot[0], player.spot[1] - 1)
            elif event.key == pygame.K_s: #Move down
                if player.spot[0] + 1 < len(floor.spaces): # and floor[player.spot[0] + 1][player.spot[1]] == "."
                    player.spot = (player.spot[0] + 1, player.spot[1])
            elif event.key == pygame.K_d: #Move right
                if player.spot[1] + 1 < len(floor.spaces[player.spot[0]]): # and floor[player.spot[0]][player.spot[1] + 1] == "."
                    player.spot = (player.spot[0], player.spot[1] + 1)
            elif event.key == pygame.K_w: #Move up
                if player.spot[0] - 1 >= 0: # and floor[player.spot[0]][player.spot[1] - 1] == "."
                    player.spot = (player.spot[0] - 1, player.spot[1])

        #Game logic

        #Clear the screen
        screen.fill(BLACK)

        #Game drawing
        floor.drawFloor()
        slime.drawSlime()
        rat.drawRat()
        player.drawPlayer()

        #Update the screen
        pygame.display.flip()

        #Limit to 60 frames per second
        clock.tick(60)

pygame.quit()
quit()
