import pygame
from states.title import Title
from pygame.locals import *
#import threading
#from client import Client

class Game():
    def __init__(self):
        pygame.init()
#        self.client = Client()
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
#        events_thread = threading.Thread(target=self.__updateEvents)
#        object_thread = threading.Thread(target=self.__updateObjects)
#        screen_thread = threading.Thread(target=self.__updateScreen)
#        while self.running:
#            #self.__updateEvents()
#            #self.__updateObjects()
#            #self.__updateScreen()
#            events_thread.start()
#            object_thread.start()
#            screen_thread.start()
#            events_thread.join()
#            object_thread.join()
#            screen_thread.join()
#            self.clock.tick(self.fps)
        while self.running:
            self.__updateEvents()
            self.__updateObjects()
            self.__updateScreen()
            self.clock.tick(self.fps)

        pygame.quit()

game = Game()

game.gameLoop()
