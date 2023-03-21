import pygame
from objects.fpga import Fpga

class Score():
    def __init__(self, playerNumber, game, song):
        self.game = game
        self.song = song
        self.playerNumber = playerNumber
        self.playerName = self.song.players[playerNumber][0]
        self.score = 0
        self.font = pygame.font.SysFont('arielblack', 35)
        self.multiplier = 1

    def draw(self):
        x = self.game.screenWidth / 15 + self.game.screenWidth / 2 * self.playerNumber
        y = self.game.screenHeight / 18
        if self.multiplier == 1:
            multiplierText = ''
        else:
            multiplierText = ', multiplier: ' + str(self.multiplier)
        text = self.font.render(self.playerName + " score: " + str(self.score) + multiplierText, False, (255, 255, 255))
        self.game.screen.blit(text, (x, y))
    
    def update(self, deadArrows, missedArrows):
        for arrow in deadArrows:
            if arrow[0] == self.playerNumber:
                self.score += self.multiplier
                self.game.updateScore(self.score)
                if self.multiplier < 8:
                    self.multiplier *= 2
        for arrow in missedArrows:
            if arrow[0] == self.playerNumber:
                self.multiplier = 1
