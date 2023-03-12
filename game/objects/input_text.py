import pygame
from pygame.locals import *

class InputText():
    def __init__(self, game, x = 0, y = 0, size = 80, text = 'hello', colour = (255, 255, 255)):
        self.game = game
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.colour = colour
        self.font = pygame.font.SysFont('arielblack', self.size)

    def __getInput(self):
        pass

    def draw(self):
        text = self.font.render(self.text, False, self.colour)
        self.game.screen.blit(text, (self.x, self.y))

    def update(self):
        self.__getInput()
        return self.text
