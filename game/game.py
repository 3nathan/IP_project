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
        self.name = ''
        self.song = 0

    def __updateEvents(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # send quit message to the server
                    self.running = False
            elif event.type == pygame.QUIT:
                self.running = False

    def __updateObjects(self):
        pressedKeys = pygame.key.get_pressed()
        self.stateStack[-1].updateObjects(pressedKeys)

    def __updateScreen(self):
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

game = Game()

game.gameLoop()
