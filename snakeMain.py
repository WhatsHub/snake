import pygame, sys, random, time
from pygame.locals import *
from queue import *
from snake import *

# Initialization for pygame library
pygame.init()

GAMEBOARD = (660, 480)
FPS = 30  # frames per second setting
SPEED = 200
fpsClock = pygame.time.Clock()

# time variable to determine if the snake's position has to update according to the SPEED variable
last = pygame.time.get_ticks()

# set up the window
DISPLAYSURF = pygame.display.set_mode(GAMEBOARD)
pygame.display.set_caption('Snake!')

# set up the colors
BLACK       = (  0,       0,      0)
GREEN       = (  0,     255,      0)
RED         = (255,       0,      0)
YELLOW      = (255,     255,      0)
NAVYBLUE    = ( 60,      60,    100)

# draw the background on the surface object
DISPLAYSURF.fill(NAVYBLUE)

# snake x and y coordinates
snakeHead = snake(5,5)
#snake = [(5, 5)] # snake head start position X = 5, Y = 5

# the apple's position
applePosX = random.randint(0, 10) * 60
applePosY = random.randint(0, 7) * 60

# All Directions
RIGHT = 'right'
LEFT = 'left'
DOWN = 'down'
UP = 'up'

# Queue that manages the input of the player (max size 2)
inputQueue = Queue(2)

# initial direction of the head
direction = RIGHT

# TODO: make gameboard bounds of snakeoutside() not static
# detects if the snake is outside of the Gamescreen
def snakeoutside():
    if snakeHead.getHeadPosX() > 655 or snakeHead.getHeadPosX() < 5:
        return True
    if snakeHead.getHeadPosY() > 475 or snakeHead.getHeadPosY() < 5:
        return True
    return False

# True if the two directions dir1 and dir2 are opposite
def opposite(dir1, dir2):
    if dir1 == RIGHT and dir2 == LEFT:
        return True
    elif dir1 == LEFT and dir2 == RIGHT:
        return True
    elif dir1 == UP and dir2 == DOWN:
        return True
    elif dir1 == DOWN and dir2 == UP:
        return True
    else:
        return False



# gameover routine
def gameover():
    print ("GAME OVER")
    pygame.quit()
    sys.exit()

# main game loop
while True:

    # draw background over the last frame
    DISPLAYSURF.fill(NAVYBLUE)

    # TODO: Create class to handle the apple
    # draw the apple
    pygame.draw.rect(DISPLAYSURF, RED, (applePosX, applePosY, 60, 60))

    #draw the snake
    snakeHead.drawSnake(DISPLAYSURF)

    # get current time
    now = pygame.time.get_ticks()

    # has enough time passed since the last time request?
    if now - last >= SPEED:

        # processing the inputQueue
        if not inputQueue.empty():
            tmp = inputQueue.get()
            if not opposite(direction, tmp):
                direction = tmp;

        # moving the snake's tail accordingly
        snakeHead.moveSnake(direction)

        # if the player hits one of the snakes tails the game is over
        if snakeHead.collides():
            fpsClock.tick(1)
            gameover()


        # what happens when the snake eats the apple
        if snakeHead.getHeadPosX() - 5 == applePosX and snakeHead.getHeadPosY() - 5 == applePosY:
            snakeHead.addSnakePart()
            xyrows = [[True] * 8 for i in range(0, 11)]

            snake = snakeHead.getSnake()
            for i in range(0, 11):
                for j in range(0, 8):
                    for k in range(0, len(snake)):
                        snakeposx = snake[k][0]//60
                        snakeposy = snake[k][1]//60
                        if snakeposx <= 10 and snakeposy <= 7:
                            if snakeposx == i and snakeposy == j:
                                xyrows[i][j] = False

            possiblespawns = [(0, 0)]
            for i in range(0, 11):
                for j in range(0, 8):
                    if xyrows[i][j]:
                        possiblespawns.append((i, j))

            if len(possiblespawns) > 1:
                possiblespawns.remove((0, 0))

            random.shuffle(possiblespawns)
            applePosX = possiblespawns[0][0] * 60
            applePosY = possiblespawns[0][1] * 60


        # set the last time variable to 'now'
        last = now

    # process input from the player
    for event in pygame.event.get():

        if snakeoutside():
            if snakeHead.getHeadPosX() > GAMEBOARD[0]-5:
                inputQueue.queue.clear()
                inputQueue.put(RIGHT)
            elif snakeHead.getHeadPosX() < 5:
                inputQueue.queue.clear()
                inputQueue.put(LEFT)
            elif snakeHead.getHeadPosY() > GAMEBOARD[1]-5:
                inputQueue.queue.clear()
                inputQueue.put(DOWN)
            elif snakeHead.getHeadPosY() < 5:
                inputQueue.queue.clear()
                inputQueue.put(UP)
            else:
                inputQueue.queue.clear()
                inputQueue.put(direction)

        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP and event.key == K_RIGHT:
            if inputQueue.full():
                inputQueue.queue.clear()
                inputQueue.put(RIGHT)
            else:
                inputQueue.put(RIGHT)
        elif event.type == KEYUP and event.key == K_LEFT:
            if inputQueue.full():
                inputQueue.queue.clear()
                inputQueue.put(LEFT)
            else:
                inputQueue.put(LEFT)
        elif event.type == KEYUP and event.key == K_DOWN:
            if inputQueue.full():
                inputQueue.queue.clear()
                inputQueue.put(DOWN)
            else:
                inputQueue.put(DOWN)
        elif event.type == KEYUP and event.key == K_UP:
            if inputQueue.full():
                inputQueue.queue.clear()
                inputQueue.put(UP)
            else:
                inputQueue.put(UP)

    # display the frame and lock the FPS
    pygame.display.update()
    fpsClock.tick(FPS)
