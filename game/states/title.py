import pygame
from pygame.locals import *
from states.state import State
from states.menu import Menu
from objects.button import Button

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        buttonX = self.game.screenWidth/2
        buttonY = self.game.screenHeight*3/5
        buttonWidth = self.game.screenWidth/3
        buttonHeight = self.game.screenHeight/6
        self.button = Button(game, 'Go to menu', buttonX, buttonY, buttonWidth, buttonHeight)

    def updateObjects(self, pressedKeys):
        # enter song state upon user pressing return
        pressed = self.button.update()
        if pressed:
            newState = Menu(self.game)
            newState.enterState()

    def updateScreen(self):
        self.game.screen.fill((0, 0, 0))
        # finish this by displaying the players' names and if they are ready
        self.button.draw()
        pygame.display.update()
