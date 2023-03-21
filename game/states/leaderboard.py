import pygame
from states.state import State

class LeaderBoard(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        print('entered leaderboard')
        # get top five scores from server
        self.game.client.send_message(["any", '_getscores'])
        self.topScores = self.game.client.receive_json()
        self.topScoresY = []
        self.topScoresX = self.game.screenWidth/12 + self.game.screenWidth/2
        self.playerScoresX = self.game.screenWidth/12
        self.playerScoresY = []
        self.font = pygame.font.SysFont('arielblack', 35)
        for i in range(len(self.topScores)):
            y = self.game.screenWidth*(i+2)/16
            self.topScoresY.append(y)
        for i in range(len(self.game.players)):
            y = self.game.screenWidth*(i+2)/16
            self.playerScoresY.append(y)

    def __drawTopScores(self):
        for i in range(len(self.topScores)):
            text = self.font.render(self.topScores[i][0] + ': ' + str(self.topScores[i][1]), False, (255, 255, 255))
            self.game.screen.blit(text, (self.topScoresX, self.topScoresY[i]))
        text = self.font.render('Top scores of all time:', False, (255, 255, 255))
        self.game.screen.blit(text, (self.game.screenWidth/15 + self.game.screenWidth/2, self.game.screenHeight/16))

    def __drawPlayerScores(self):
        for i in range(len(self.game.players)):
            text = self.font.render(self.game.players[i] + ': ' + str(self.game.scores[i]), False, (255, 255, 255))
            self.game.screen.blit(text, (self.playerScoresX, self.playerScoresY[i]))
        text = self.font.render('Players scores:', False, (255, 255, 255))
        self.game.screen.blit(text, (self.game.screenWidth/15, self.game.screenHeight/16))

    def updateObjects(self, pressedKeys):
        pass

    def updateScreen(self):
        self.game.screen.fill((0, 0, 0))
        self.__drawTopScores()
        self.__drawPlayerScores()
        pygame.display.update()
