import pygame
from pygame.locals import *
from states.state import State
from states.leaderboard import LeaderBoard
from objects.arrow import Arrow
from objects.score import Score

class Song(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.sensitivity = 0.03
        # get players from server
        self.game.client.send_message([0, '_retreive'])
        self.players = self.game.client.receive_json()
        self.game.players = self.players
        for player in self.players:
            if player != self.game.name:
                self.opponent = player
        self.path = self.game.song
        self.background = pygame.image.load('assets/' + self.path + '/background.png')
        self.__getData()
        self.__loadData()
        self.startTime = pygame.time.get_ticks()/1000
        pygame.mixer.music.load("assets/" + self.path + '/music.mp3')
        pygame.mixer.music.play()

    def __getData(self):
        f = open('assets/' + self.path + '/arrows', 'r')
        self.arrowData = f.read()
        self.arrowData = self.arrowData.split('\n')
        self.arrowData.remove('')
        for i in range(len(self.arrowData)):
            self.arrowData[i] = self.arrowData[i].split(' ')
            for j in range(3):
                self.arrowData[i][j] = float(self.arrowData[i][j])
        self.endTime = self.arrowData[-1][1]
        print(self.endTime)
    
        f.close()

    def __loadData(self):
        self.arrows = []
        self.scores = []
        currentTime = pygame.time.get_ticks()/1000
        for i in range(len(self.players)):
            for j in range(len(self.arrowData)):
                # Arrow arguments (direction, arriveTime, speed, sensitivity, playerData, playerNumber, index, screenWidth, screenHeight)
                arrow = Arrow(i, j, self.game, self, currentTime)
                self.arrows.append(arrow)
            # Score arguments (playerName, playerNumber, screenWidth, screenHeight)
            score = Score(i, self.game, self)
            self.scores.append(score)

    def updateObjects(self, pressedKeys):
        # change this when integrating the server
        # list of all arrows
        self.game.client.send_message([self.game.name, []])
        recievedArrows = self.game.client.receive_json()
        deadArrows = []
        missedArrows = []
        for arrow in recievedArrows:
            if arrow[2] == 1:
                deadArrows.append(arrow)
            else:
                missedArrows.append(arrow)
        currentTime = pygame.time.get_ticks()/1000
        for arrow in self.arrows:
            arrowData = arrow.update(pressedKeys, deadArrows, missedArrows, currentTime)
            if arrowData:
                # send arrow data to server
                self.game.client.send_message([self.game.name, arrowData])
                self.game.client.receive_json()
                if arrowData[2] == 1:
                    deadArrows.append(arrowData[:-1])
                else:
                    missedArrows.append(arrowData[:-1])
        # change this when integrating the server
        for score in self.scores:
            score.update(deadArrows, missedArrows)

        if currentTime - self.startTime > self.endTime + 5:
            self.game.scores = []
            for score in self.scores:
                self.game.scores.append(score.getScore())
            if self.players[0] == self.game.name:
                self.game.client.send_message([[self.game.name, self.game.scores[0]], '_putscore'])
                self.game.client.receive_json()
            else:
                self.game.client.send_message([[self.game.name, self.game.scores[1]], '_putscore'])
                self.game.client.receive_json()
            print('leaderboard')
            newState = LeaderBoard(self.game)
            newState.enterState()

    def updateScreen(self):
        self.game.screen.fill((0, 0, 0))
        self.game.screen.blit(self.background, (self.game.screenWidth/12, 0))
        for arrow in self.arrows:
            arrow.draw()
        for score in self.scores:
            score.draw()
        pygame.display.update()
