import pygame
from objects import *
from pygame.locals import *

#class Menu():
#    def __init__(self):
#    
#    def __lobby(self):
#        #get ready and players data from server
#        ready = [1, 0]
#        players = ['Player 1 name', 'Player 2 name']
#        for 



class Game():
    def __init__(self, players, path):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screenWidth = 1280
        self.screenHeight = 720
        self.screen = pygame.display.set_mode([self.screenWidth, self.screenHeight])
        self.fps = 60
        self.sensitivity = 0.03
        self.running = True
        self.players = players
        self.path = path
        self.running = 1
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
                # Arrow arguements (direction, arriveTime, speed, sensitivity, playerData, playerNumber, index)
                arrow = Arrow(self.arrowData[j][0], self.arrowData[j][1], self.arrowData[j][2], self.sensitivity, self.players[i], i, j, self.screenWidth, self.screenHeight)
                self.arrows.append(arrow)
            score = Score(self.players[i][0], i, self.screenWidth, self.screenHeight)
            self.scores.append(score)

    # this should be 5-10 seconds after the song ends
    # not after the las arrow has passed
    #def __isGameRunning(self):
    #    lastArrow = self.arrows[len(self.arrows)-1]
    #    if not lastArrow.isAlive():
    #        self.running = 0
    def __updateEvents(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    # send quit message to the server
                    self.running = False
            elif event.type == pygame.QUIT:
                self.running = False

    def __updateObjects(self):
        pressedKeys = pygame.key.get_pressed()
        deadArrows = []
        for arrow in self.arrows:
            deadArrow = arrow.update(pressedKeys, deadArrows)
            if deadArrow:
                deadArrows.append(deadArrow)
        for score in self.scores:
            score.update(deadArrows)

    def __updateScreen(self):
        self.screen.fill((0, 0, 0))
        for arrow in self.arrows:
            arrow.draw(self.screen)
        for score in self.scores:
            score.draw(self.screen)
        pygame.display.update()

    def gameLoop(self):
        while self.running:
            self.__updateEvents()
            self.__updateObjects()
            self.__updateScreen()
            self.clock.tick(self.fps)

        pygame.quit()

# players list
# the index represents the player number
# the string represents the player name
# the number 1 or 0 represents if the player is playing
# on this machine or not respectively
players = [['Player 1', 0], ['Player 2', 1]]

# arrowData = [direction, arrive time, speed] 

game = Game(players, 'test_arrows')

game.gameLoop()
