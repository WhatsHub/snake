import pygame, sys, random

class snake:

    __snake = []

    def __init__(self, headPosX, headPosY):
        self.__snake.append((headPosX, headPosY))

    # TODO: Make Gameboard bounds not static
    def moveSnake(self, direction):
        # moving the snake's tail accordingly
        for i in range(len(self.__snake) - 1, 0, -1):
            self.__snake[i] =self.__snake[i - 1]

        headposx = self.getHeadPosX()
        headposy = self.getHeadPosY()
        # moving the snake's head according to it's direction
        if direction == 'right':
            headposx += 60
            if 717 <= headposx >= 723:
                headposx = 5

        elif direction == 'down':
            headposy += 60
            if 517 <= headposy >= 523:
                headposy = 5

        elif direction == 'left':
            headposx -= 60
            if -52 >= headposx <= -58:
                headposx = 605

        elif direction == 'up':
            headposy -= 60
            if -57 >= headposy <= -63:
                headposy = 425

        self.setHeadPos(headposx, headposy)

    # TODO: Make snake size not static
    def drawSnake(self, displaysurfaces):

        # draw the snake's head
        pygame.draw.rect(displaysurfaces, (255, 255, 0), (self.getHeadPosX() - 5, self.getHeadPosY() - 5, 60, 60))
        pygame.draw.rect(displaysurfaces, (0, 255, 0), (self.getHeadPosX(), self.getHeadPosY(), 50, 50))

        # draw the tail
        for i in range(1, len(self.__snake)):
            pygame.draw.rect(displaysurfaces, (0, 0, 0), (self.__snake[i][0] - 5, self.__snake[i][1] - 5, 60, 60))
            pygame.draw.rect(displaysurfaces, (0, 255, 0), (self.__snake[i][0], self.__snake[i][1], 50, 50))

    def collides(self):
        for i in range(1, len(self.__snake)):
            if self.__snake[i][0] == self.getHeadPosX() and self.__snake[i][1] == self.getHeadPosY():
                return True
        return False

    def addSnakePart(self):
        self.__snake.append((self.__snake[-1][0], self.__snake[-1][1]))

    def getHeadPosX(self):
        return self.__snake[0][0]

    def getHeadPosY(self):
        return self.__snake[0][1]

    def setHeadPos(self, x, y):
        self.popHead()
        self.__snake = [(x, y)] + self.getSnake()

    def popHead(self):
        return self.__snake.pop(0)

    def getSnake(self):
        return self.__snake
