import pygame
from states.title import Title
from pygame.locals import *

class Game():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screenWidth = 1280
        self.screenHeight = 720
        self.screen = pygame.display.set_mode([self.screenWidth, self.screenHeight])
        self.fps = 60
        self.running = True
        self.stateStack = []
        self.__loadStates()

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
        #deadArrows = []
        #for arrow in self.arrows:
        #    deadArrow = arrow.update(pressedKeys, deadArrows)
        #    if deadArrow:
        #        deadArrows.append(deadArrow)
        #for score in self.scores:
        #    score.update(deadArrows)
        self.stateStack[-1].updateObjects(pressedKeys)

    def __updateScreen(self):
        #self.screen.fill((0, 0, 0))
        #for arrow in self.arrows:
        #    arrow.draw(self.screen)
        #for score in self.scores:
        #    score.draw(self.screen)
        #pygame.display.update()
        self.stateStack[-1].updateScreen()

    def __loadStates(self):
        self.title = Title(self)
        self.stateStack.append(self.title)

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

game = Game()

game.gameLoop()
