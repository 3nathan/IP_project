import pygame
from states.state import State
from states.menu import Menu
from objects.button import Button
from objects.input_text import InputText

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        buttonX = self.game.screenWidth/2
        buttonY = self.game.screenHeight*5/7
        buttonWidth = self.game.screenWidth/5
        buttonHeight = self.game.screenHeight/8
        self.button = Button(game, 'Go to menu', buttonX, buttonY, buttonWidth, buttonHeight, 50)
        self.titleFont = pygame.font.SysFont('arielblack', 100)
        self.titleText = 'FPGA Rhythm Game'
        self.titleX = self.game.screenWidth/2 - len(self.titleText)*20
        self.titleY = self.game.screenHeight/4 - 30
        self.inputTextX = buttonX
        self.inputTextY = self.game.screenHeight/3
        self.inputText = InputText(game, self.inputTextX, self.inputTextY)

    def __titleText(self):
        text = self.titleFont.render(self.titleText, False, (255, 255, 255))
        self.game.screen.blit(text, (self.titleX, self.titleY))

    def updateObjects(self, pressedKeys):
        self.inputText.update()
        # enter song state upon user pressing return
        pressed = self.button.update()
        if pressed:
            newState = Menu(self.game)
            newState.enterState()

    def updateScreen(self):
        self.game.screen.fill((0, 0, 0))
        # finish this by displaying the players' names and if they are ready
        self.__titleText()
        self.inputText.draw()
        self.button.draw()
        pygame.display.update()
