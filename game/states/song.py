import pygame
from pygame.locals import *
from states.state import State
from objects.arrow import Arrow
from objects.score import Score

class Song(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.sensitivity = 0.03
        # get players from server
        self.players = [['Player 1', 1], ['Player 2', 0]]
        # get path from the server
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
        currentTime = pygame.time.get_ticks()/1000
        for i in range(len(self.players)):
            for j in range(len(self.arrowData)):
                # Arrow arguments (direction, arriveTime, speed, sensitivity, playerData, playerNumber, index, screenWidth, screenHeight)
                arrow = Arrow(i, j, self.game, self, currentTime)
                self.arrows.append(arrow)
            # Score arguments (playerName, playerNumber, screenWidth, screenHeight)
            score = Score(i, self.game, self)
            self.scores.append(score)

    def updateObjects(self, pressedKeys):
        # change this when integrating the server
        recievedArrows =[]
        deadArrows = []
        missedArrows = []
        for arrow in recievedArrows:
            if arrow[2] == 1:
                deadArrows.append(arrow)
            else:
                missedArrows.append(arrow)
        currentTime = pygame.time.get_ticks()/1000
        for arrow in self.arrows:
            arrowData = arrow.update(pressedKeys, deadArrows, missedArrows, currentTime)
            if arrowData:
                if arrowData[2] == 1:
                    deadArrows.append(arrowData[:-1])
                else:
                    missedArrows.append(arrowData[:-1])
        # change this when integrating the server
        for score in self.scores:
            score.update(deadArrows, missedArrows)

    def updateScreen(self):
        self.game.screen.fill((0, 0, 0))
        for arrow in self.arrows:
            arrow.draw()
        for score in self.scores:
            score.draw()
        pygame.display.update()
