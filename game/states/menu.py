import pygame
from client import Client
from states.state import State
from states.song import Song
from objects.button import Button

class Menu(State):
    def __init__(self, game):
        State.__init__(self, game)
        buttonX = self.game.screenWidth/2
        buttonY = self.game.screenHeight*5/7
        buttonWidth = self.game.screenWidth/5
        buttonHeight = self.game.screenHeight/8
        # get players from the server
        self.message = [0, '_retreive']
        self.game.client.send_message(self.message)
        # send message to server and retreive the list of players
        self.players = self.client.receive_json()
        if self.players[0] == self.game.name:
            buttonText = 'Go to song'
        else:
            buttonText = 'Ready'
        self.button = Button(game, buttonText, buttonX, buttonY, buttonWidth, buttonHeight, 50)

    def updateObjects(self, pressedKeys):
        # enter song state upon user pressing return
        # when player 1 chooses the song, the path to the audio and arrow
        # files are sent to the server so that the other player plays the
        # same song
        if len(self.players) == 1:
            # send self.message to server and retrieve the list of players
            self.game.client.send_message(self.message)
            self.players = self.client.receive_json()
            pass
        if self.players[0] == self.game.name:
            self.game.song = 'Gangnam Style'
            # receive song message from the server
        else:
            self.game.client.send_message([0, '_songname'])
            song = self.game.client.receive_json()
            if song:
                self.game.song = song
                newState = Song(self.game)
                newState.enterState()

        pressed = self.button.update()

        if pressed and self.players[0] == self.game.name and len(self.players) > 1:
            self.game.client([self.song, '_songname'])
            self.game.client.receive_json()
            newState = Song(self.game)
            newState.enterState()

    def updateScreen(self):
        self.game.screen.fill((0, 0, 0))
        # finish this by displaying the players' names and if they are ready
        self.button.draw()
        pygame.display.update()
        

