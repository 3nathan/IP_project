from pygame.locals import *
from states.state import State
from states.song import Song

class Menu(State):
    def __init__(self, game):
        State.__init__(self, game)

    def updateObjects(self, pressedKeys):
        if pressedKeys[K_RETURN]:
            newState = Song(self.game)
            newState.enterState()
        pass

    def updateScreen(self):
        self.game.screen.fill((0, 0, 0))
        # finish this by displaying the players' names and if they are ready
