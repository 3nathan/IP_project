import pygame
from pygame.locals import *

class Button():
    def __init__(self, game, text, x, y, width, height, colour = (50, 50, 200), size = 80):
        self.game = game
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.size = size
        self.active = 0
        self.mouse = pygame.mouse
        self.font = pygame.font.SysFont('arielblack', self.size)
        self.rect = (self.x - self.width/2, self.y - self.height/2, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.game.screen, self.colour, self.rect)
        text = self.font.render(self.text, False, (255, 255, 255))
        self.game.screen.blit(text, ((self.x - len(self.text)*self.size/5), (self.y - self.size/3.5)))

    def update(self):
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()

        # button is active if it has been clicked, and it is made 'unactive' if a different area has been clicked
        mouseOnButton = (self.x - self.width/2 < pos[0]) and (self.x + self.width/2 > pos[0]) and (self.y - self.height/2 < pos[1]) and (self.y + self.height/2 > pos[1])
        if self.active and not pressed[0]:
            return 1
        if pressed[0]:
            if mouseOnButton:
                self.active = 1
            else:
                self.active = 0


        return 0
