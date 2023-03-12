import pygame
from states.state import State
from states.song import Song
from objects.button import Button

class Menu(State):
    def __init__(self, game):
        State.__init__(self, game)
        buttonX = self.game.screenWidth/2
        buttonY = self.game.screenHeight*5/7
        buttonWidth = self.game.screenWidth/5
        buttonHeight = self.game.screenHeight/8
        self.button = Button(game, 'Go to song', buttonX, buttonY, buttonWidth, buttonHeight, 50)

    def updateObjects(self, pressedKeys):
        # enter song state upon user pressing return
        pressed = self.button.update()
        if pressed:
            newState = Song(self.game)
            newState.enterState()

    def updateScreen(self):
        self.game.screen.fill((0, 0, 0))
        # finish this by displaying the players' names and if they are ready
        self.button.draw()
        pygame.display.update()
