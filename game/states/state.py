class State():
    def __init__(self, game):
        self.game = game
        self.prevState = None

    def updateEvents(self, events):
        pass

    def updateObjects(self, pressedKeys):
        pass

    def updateScreen(self):
        pass

    def enterState(self):
        if len(self.game.stateStack) > 1:
            self.prevState = self.game.stateStack[-1]
        self.game.stateStack.append(self)

    def exitState(self):
        self.game.stateStack.pop()
