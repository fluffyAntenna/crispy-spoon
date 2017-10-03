import pygame
import random
import math
from player import *
from floor import *
from enemies import *

#Initialize the Game
pygame.init()

def textObjects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def mainMenu():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(WHITE)
        text = "R@ Slayer"
        TextSurf, TextRect = textObjects(text, fontDV)
        TextRect.center = ((width / 2), (height / 2))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        for i in range(2):
            pygame.time.Clock().tick(1)
        intro = False



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

#Define text fonts
fontDV = pygame.font.Font('Assets/Fonts/DejaVuSans.ttf', 32)

#Game Window Size
width = 1280
height = 720
size = (width, height)

#Create the Game Window
screen = pygame.display.set_mode(size)
pygame.display.set_caption("R@ Slayer v1")
ico = pygame.image.load("Assets/SplashScreen/Icon.png")
pygame.display.set_icon(ico)


#Show splash screen
splash = pygame.image.load("Assets/SplashScreen/fluffyAntennaMKI.png")
screen.blit(splash, (0,0))
pygame.display.update()
for i in range(2):
    pygame.time.Clock().tick(1)

mainMenu()

#Set game mode
#1 = Play
#2 = Main Menu
#3 = New Floor
#4 = Lose
#5 = Win
#6 = Instructions
#7 = Credits

gameMode = 1

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
floorLevel = 1

#Generate the first level
floor = Floor()
floor.generate(30, 30)

#Keep track of the existing floors
floors = []
floors.append(floor)

#Spawn the player once the floor has been generated
player.spawnUp(floor)

#Set maximum enemies
maxEnemies = floorLevel * 3

#Create initial mobs
enemies = []

for i in range(maxEnemies):
    enemyNum = random.randint(0,1)
    if enemyNum == 0:
        slime = Slime()
        slime.spawn(floor)
        enemies.append(slime)
    elif enemyNum == 1:
        rat = Rat()
        rat.spawn(floor)
        enemies.append(rat)

#Initial drawing
screen.fill(BLACK)
floor.drawFloor(width, height, screen, player)
player.drawPlayer(width, height, screen)
for e in enemies:
    e.draw(player)
pygame.display.update()

#Main Game Loop
while not done:
    #Main Event Loop
    if gameMode == 1: #Play the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_a: #Move left
                    eToAttack = player.findAdjacentEnemy("left", enemies)
                    if eToAttack:
                        player.attack(eToAttack)
                        print "Player attacks"
                    elif player.spot[1] - 1 >= 0 and (floor.spaces[player.spot[0]][player.spot[1] - 1] == "." or floor.spaces[player.spot[0]][player.spot[1] - 1] == "d" or floor.spaces[player.spot[0]][player.spot[1] - 1] == "<" or floor.spaces[player.spot[0]][player.spot[1] - 1] == ">"):
                        player.spot = (player.spot[0], player.spot[1] - 1)
                elif event.key == pygame.K_s: #Move down
                        eToAttack = player.findAdjacentEnemy("down", enemies)
                        if eToAttack:
                            player.attack(eToAttack)
                            print "Player attacks"
                        elif player.spot[0] + 1 < len(floor.spaces) and (floor.spaces[player.spot[0] + 1][player.spot[1]] == "." or floor.spaces[player.spot[0] + 1][player.spot[1]] == "d" or floor.spaces[player.spot[0] + 1][player.spot[1]] == "<" or floor.spaces[player.spot[0] + 1][player.spot[1]] == ">"):
                            player.spot = (player.spot[0] + 1, player.spot[1])
                elif event.key == pygame.K_d: #Move right
                    eToAttack = player.findAdjacentEnemy("right", enemies)
                    if eToAttack:
                        player.attack(eToAttack)
                        print "Player attacks"
                    elif player.spot[1] + 1 < len(floor.spaces[player.spot[0]]) and (floor.spaces[player.spot[0]][player.spot[1] + 1] == "." or floor.spaces[player.spot[0]][player.spot[1] + 1] == "d" or floor.spaces[player.spot[0]][player.spot[1] + 1] == "<" or floor.spaces[player.spot[0]][player.spot[1] + 1] == ">"):
                        player.spot = (player.spot[0], player.spot[1] + 1)
                elif event.key == pygame.K_w: #Move up
                    eToAttack = player.findAdjacentEnemy("up", enemies)
                    if eToAttack:
                        player.attack(eToAttack)
                        print "Player attacks"
                    elif player.spot[0] - 1 >= 0 and (floor.spaces[player.spot[0] - 1][player.spot[1]] == "." or floor.spaces[player.spot[0] - 1][player.spot[1]] == "d" or floor.spaces[player.spot[0] - 1][player.spot[1]] == "<" or floor.spaces[player.spot[0] - 1][player.spot[1]] == ">"):
                        player.spot = (player.spot[0] - 1, player.spot[1])
                elif event.key == pygame.K_SPACE:
                    pass
                elif event.key == pygame.K_UP and floor.spaces[player.spot[0]][player.spot[1]] == ">":
                    print "FLOOR UP"
                    floors[floorLevel - 1] = floor
                    floorLevel += 1
                    if len(floors) > floorLevel - 1:
                        floor = floors[floorLevel - 1]
                        enemies = []
                        screen.fill(BLACK)
                        floor.drawFloor(width, height, screen, player)
                        player.drawPlayer(width, height, screen)
                        pygame.display.update()
                        clock.tick(120)
                        continue
                    else: #TODO FIX THE BOSS FLOORS
                        floor = Floor()
                        floor.generate(int(len(floors[floorLevel - 2].spaces) * 2), int(len(floors[floorLevel - 2].spaces[0]) * 2))
                        enemies = []
                        floors.append(floor)
                        player.spawnUp(floor)
                        screen.fill(BLACK)
                        floor.drawFloor(width, height, screen, player)
                        player.drawPlayer(width, height, screen)
                        pygame.display.update()
                        clock.tick(120)
                        continue
                elif event.key == pygame.K_DOWN and floor.spaces[player.spot[0]][player.spot[1]] == "<" and floorLevel > 1:
                    floors[floorLevel - 1] = floor
                    floorLevel -= 1
                    floor = floors[floorLevel - 1]
                    enemies = []
                    player.spawnDown(floor)
                    screen.fill(BLACK)
                    floor.drawFloor(width, height, screen, player)
                    pygame.display.update()
                    clock.tick(120)
                    continue
                elif event.key == pygame.K_PERIOD: #TODO FIX THE CHEATS
                    print "GOING UP"
                    floorLevel += 1
                    continue
                elif event.key == pygame.K_COMMA and floorLevel > 1:
                    print "GOING DOWN"
                    floorLevel -= 1
                    continue

                #Game logic

                #Decrement the healthTick every step
                healthTick -= 1

                #Leveling up
                if player.exp >= (player.level ** 2) * 5:
                    player.level += 1
                    player.health += 2
                    player.maxHealth += 2
                    player.strength += 2
                    player.defense += 2

                #Player regenerates one health every 7 steps
                if healthTick == 0:
                    if player.health < player.maxHealth:
                        player.health += 1
                    healthTick = 7

                #Enemies take turns
                for e in enemies:
                    if e.health > 0:
                        e.takeTurn(floor, player)
                    else:
                        e.die(player)
                        enemies.remove(e)

                #Spawn more enemies if below max
                while len(enemies) < maxEnemies:
                    enemyNum = random.randint(0,1)
                    if enemyNum == 0:
                        slime = Slime()
                        slime.spawn(floor)
                        enemies.append(slime)
                    elif enemyNum == 1:
                        rat = Rat()
                        rat.spawn(floor)
                        enemies.append(rat)

                print "P:", player.health
                print "LEV:", player.level
                print "EXP:", player.exp
                print "FLOOR", floorLevel


                #End the game when health reaches zero
                if player.health <= 0:
                    done = True

                #Clear the screen
                screen.fill(BLACK)

                #Game drawing
                floor.drawFloor(width, height, screen, player)
                for e in enemies:
                    e.draw(player)
                player.drawPlayer(width, height, screen)

                #Draw the status bar

                #Update the screen
                pygame.display.update()

                #Limit to 120 frames per second
                clock.tick(120)

pygame.quit()
