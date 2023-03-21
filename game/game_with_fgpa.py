import pygame
from states.title_with_fpga import Title
from pygame.locals import *
from objects.fpga import Fpga

class Game():
    def __init__(self):
        pygame.init()
        Fpga.__init__(self)
        self.clock = pygame.time.Clock()
        self.screenWidth = 1280
        self.screenHeight = 720
        self.screen = pygame.display.set_mode([self.screenWidth, self.screenHeight])
        self.fps = 30
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
                    self.exitNios()
                    self.running = False
            elif event.type == pygame.QUIT:
                self.exitNios()
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
