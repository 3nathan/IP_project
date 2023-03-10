import pygame
from states.state import State
from objects.objects import *

class Song(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.sensitivity = 0.03
        #self.players = players
        self.players = [['Player 1', 1], ['Player 2', 0]]
        #self.path = path
        self.path = 'test_arrows'
        self.__getData()
        self.__loadData()
        

    def __getData(self):
        f = open(self.path, 'r')
        self.arrowData = f.read()
        self.arrowData = self.arrowData.split('\n')
        self.arrowData.remove('')
        for i in range(len(self.arrowData)):
            self.arrowData[i] = self.arrowData[i].split(' ')
            for j in range(3):
                self.arrowData[i][j] = float(self.arrowData[i][j])
    
        f.close()

    def __loadData(self):
        self.arrows = []
        self.scores = []
        for i in range(len(self.players)):
            for j in range(len(self.arrowData)):
                # Arrow arguments (direction, arriveTime, speed, sensitivity, playerData, playerNumber, index, screenWidth, screenHeight)
                arrow = Arrow(self.arrowData[j][0], self.arrowData[j][1], self.arrowData[j][2], self.sensitivity, self.players[i], i, j, self.game.screenWidth, self.game.screenHeight)
                self.arrows.append(arrow)
            # Score arguments (playerName, playerNumber, screenWidth, screenHeight)
            score = Score(self.players[i][0], i, self.game.screenWidth, self.game.screenHeight)
            self.scores.append(score)

    def updateObjects(self, pressedKeys):
        deadArrows = []
        for arrow in self.arrows:
            deadArrow = arrow.update(pressedKeys, deadArrows)
            if deadArrow:
                deadArrows.append(deadArrow)
        for score in self.scores:
            score.update(deadArrows)

    def updateScreen(self):
        self.game.screen.fill((0, 0, 0))
        for arrow in self.arrows:
            arrow.draw(self.game.screen)
        for score in self.scores:
            score.draw(self.game.screen)
        pygame.display.update()