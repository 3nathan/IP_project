import pygame
from pygame.locals import *

class Arrow():
    def __init__(self, playerNumber, index, game, song, currentTime):
        self.game = game
        self.song = song
        self.x = 0
        self.y = 0
        self.direction = self.song.arrowData[index][0]
        self.arriveTime = self.song.arrowData[index][1] + currentTime
        self.speed = self.song.arrowData[index][2]
        self.host = self.song.players[playerNumber][1]
        self.player = playerNumber
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
        self.x = self.game.screenWidth * (self.direction + 1) / 10 + self.game.screenWidth / 2 * (self.player) - self.game.screenWidth/32
        self.y = self.game.screenHeight / 6 + (self.arriveTime - currentTime) * self.speed - self.game.screenWidth/32
        # screenWidth/32 is the length of one side of the arrow
        if self.y > (0 - self.game.screenWidth/16) and self.y < (self.game.screenHeight + self.game.screenWidth/16):
            self.visible = 1
        else:
            self.visible = 0
    
    def __calculateScore(self, currentTime):
        if currentTime - self.arriveTime > self.song.sensitivity:
            # this is a miss, points are 0
            # could also use this to decrease the score
            # because it is a miss
            self.alive = 1
        elif currentTime - self.arriveTime >= -self.song.sensitivity:
            # this is a hit, points are maximal if
            # current time - arrive time is small
            self.alive = 0

    def __calculateHit(self, currentTime, pressedKeys):
        if pressedKeys[K_LEFT] and self.direction == 0:
            self.__calculateScore(currentTime)
        if pressedKeys[K_UP] and self.direction == 1:
            self.__calculateScore(currentTime)
        if pressedKeys[K_DOWN] and self.direction == 2:
            self.__calculateScore(currentTime)
        if pressedKeys[K_RIGHT] and self.direction == 3:
            self.__calculateScore(currentTime)

    def isAlive(self):
        return self.alive

    def draw(self, screen):
        if self.alive and self.visible:
            self.rect = (self.x, self.y, self.game.screenWidth/32, self.game.screenWidth/32)
            pygame.draw.rect(screen, self.colour, self.rect)

    # deadArrow is the list: [player, index] of an opponent arrow
    # that has been hit
    def update(self, pressedKeys, deadArrows, currentTime):
        # if there is a dead arrow and its not the host arrow, kill the
        # correct arrow
        for deadArrow in deadArrows:
            if self.player == deadArrow[0] and self.index == deadArrow[1]:
                self.alive = 0

        if self.alive:
            self.__calculatePosition(currentTime)

            if self.speed and self.host:
                self.__calculateHit(currentTime, pressedKeys)
                
                if not self.alive:
                    return [self.player, self.index]

        return 0
