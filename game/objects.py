import pygame
from pygame.locals import *

class Arrow(pygame.sprite.Sprite):
    def __init__(self, direction, arriveTime, speed, sensitivity, playerData, playerNumber, index, screenWidth, screenHeight):
        self.x = 0
        self.y = 0
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.direction = direction
        self.speed = speed
        self.sensitivity = sensitivity
        self.host = playerData[1]
        self.player = playerNumber
        currentTime = pygame.time.get_ticks() / 1000
        self.arriveTime = arriveTime + currentTime
        # index used to tell which arrows have been hit for opponent
        self.index = index
        self.alive = 1
        self.visible = 0
        self.__determineColour()

    def __determineColour(self):
        # host arrow colouring
        if self.speed and self.host:
            self.colour = (200, 200, 200)
        # opponent arrow colouring
        elif self.speed:
            self.colour = (180, 20, 20)
        # base arrow colouring
        elif self.direction == 0:
            self.colour = (255, 0, 0)
        elif self.direction == 1:
            self.colour = (0, 200, 0)
        elif self.direction == 2:
            self.colour = (0, 0, 255)
        elif self.direction == 3:
            self.colour = (255, 255, 255)
        # default case
        else:
            self.colour = (200, 200, 200)

    def __calculatePosition(self, currentTime):
        self.x = self.screenWidth * (self.direction + 1) / 10 + self.screenWidth / 2 * (self.player) - self.screenWidth/32
        self.y = self.screenHeight / 6 + (self.arriveTime - currentTime) * self.speed - self.screenWidth/32
        # screenWidth/32 is the length of one side of the arrow
        if self.y > (0 - self.screenWidth/16) and self.y < (self.screenHeight + self.screenWidth/16):
            self.visible = 1
        else:
            self.visible = 0
    
    def __calculatePoints(self, currentTime):
        if currentTime - self.arriveTime > self.sensitivity:
            # this is a miss, points are 0
            # could also use this to decrease the score
            # because it is a miss
            self.alive = 1
        elif currentTime - self.arriveTime >= -self.sensitivity:
            # this is a hit, points are maximal if
            # current time - arrive time is small
            self.alive = 0

    def __calculateHit(self, currentTime, pressedKeys):
        if pressedKeys[K_LEFT] and self.direction == 0:
            self.__calculatePoints(currentTime)
        if pressedKeys[K_UP] and self.direction == 1:
            self.__calculatePoints(currentTime)
        if pressedKeys[K_DOWN] and self.direction == 2:
            self.__calculatePoints(currentTime)
        if pressedKeys[K_RIGHT] and self.direction == 3:
            self.__calculatePoints(currentTime)

    def isAlive(self):
        return self.alive

    def draw(self, screen):
        if self.alive and self.visible:
            self.rect = (self.x, self.y, self.screenWidth/32, self.screenWidth/32)
            pygame.draw.rect(screen, self.colour, self.rect)

    # deadArrow is the list: [player, index] of an opponent arrow
    # that has been hit
    def update(self, pressedKeys, deadArrows):
        # if there is a dead arrow and its not the host arrow, kill the
        # correct arrow
        for deadArrow in deadArrows:
            if self.player == deadArrow[0] and self.index == deadArrow[1]:
                self.alive = 0

        if self.alive:
            currentTime = pygame.time.get_ticks() / 1000
            self.__calculatePosition(currentTime)

            if self.speed and self.host:
                self.__calculateHit(currentTime, pressedKeys)
                
                if not self.alive:
                    return [self.player, self.index]

        return 0

class Score():
    def __init__(self, playerName, playerNumber, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.playerNumber = playerNumber
        self.playerName = playerName
        self.score = 0
        self.font = pygame.font.SysFont('arielblack', 35)

    #def draw(self, screen):
        # draw score on screen above the base arrows
        # for each player
    def draw(self, screen):
        x = self.screenWidth / 15 + self.screenWidth / 2 * self.playerNumber
        y = self.screenHeight / 18
        text = self.font.render(self.playerName + " score: " + str(self.score), False, (255, 255, 255))
        screen.blit(text, (x, y))
    
    def update(self, deadArrows):
        for deadArrow in deadArrows:
            if deadArrow[0] == self.playerNumber:
                self.score += 1
