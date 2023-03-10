import pygame

class Score():
    def __init__(self, playerNumber, game, song):
        self.game = game
        self.song = song
        self.playerNumber = playerNumber
        self.playerName = self.song.players[playerNumber][0]
        self.score = 0
        self.font = pygame.font.SysFont('arielblack', 35)

    #def draw(self, screen):
        # draw score on screen above the base arrows
        # for each player
    def draw(self, screen):
        x = self.game.screenWidth / 15 + self.game.screenWidth / 2 * self.playerNumber
        y = self.game.screenHeight / 18
        text = self.font.render(self.playerName + " score: " + str(self.score), False, (255, 255, 255))
        self.game.screen.blit(text, (x, y))
    
    def update(self, deadArrows):
        for deadArrow in deadArrows:
            if deadArrow[0] == self.playerNumber:
                self.score += 1
