import pygame
from pygame.locals import *

class InputText():
    def __init__(self, game, x = 0, y = 0, size = 80, text = '', colour = (255, 255, 255)):
        self.game = game
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.colour = colour
        self.font = pygame.font.SysFont('arielblack', self.size)

    def __getInput(self):
        for event in self.game.events:
            if event.type == KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key != pygame.K_ESCAPE:
                    self.text += event.unicode

    def draw(self):
        text = self.font.render(self.text, False, self.colour)
        self.game.screen.blit(text, (self.x - len(self.text)*self.size*14/100, self.y))

    def update(self):
        self.__getInput()
        return self.text
