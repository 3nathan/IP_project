import pygame
from states.state import State

class LeaderBoard(State):
    def __init__(self, game):
        State.__init__(self, game)
        print('entered leaderboard')
        # get players from the server
        self.players = ['Player 1', 'Player 2']

    def updateObjects(self, pressedKeys):
        pass

    def updateScreen(self):
        self.game.screen.fill((0, 0, 0))
