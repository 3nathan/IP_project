import pygame
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
#        self.message = [0, '_retreive']
#        self.game.client.send_message(self.message)
        # send message to server and retreive the list of players
#        self.players = self.game.client.receive_json()
        self.players = [self.game.name, 'Player 2']
        if self.players[0] == self.game.name:
            buttonText = 'Go to song'
            earnedText = 'Earned It'
            earnedX = self.game.screenWidth/3
            earnedY = self.game.screenHeight/3
            self.earnedButton = Button(game, earnedText, earnedX, earnedY, buttonWidth, buttonHeight, 50)
            gangnamText = 'Gangnam Style'
            gangnamX = self.game.screenWidth*2/3
            gangnamY = self.game.screenHeight/3
            self.gangnamButton = Button(game, gangnamText, gangnamX, earnedY, buttonWidth, buttonHeight, 50)
        else:
            buttonText = 'Ready'
        self.button = Button(game, buttonText, buttonX, buttonY, buttonWidth, buttonHeight, 50)

        self.songChoice = 0

    def updateObjects(self, pressedKeys):
        # enter song state upon user pressing return
        # when player 1 chooses the song, the path to the audio and arrow
        # files are sent to the server so that the other player plays the
        # same song
#        if len(self.players) == 1:
#            # send self.message to server and retrieve the list of players
#            self.game.client.send_message(self.message)
#            self.players = self.game.client.receive_json()
#            pass
        if self.players[0] == self.game.name:
            if self.earnedButton.update():
                self.songChoice = 1
            elif self.gangnamButton.update():
                self.songChoice = 2
            pressed = self.button.update()
            # receive song message from the server
#        else:
#            self.game.client.send_message([0, '_songname'])
#            song = self.game.client.receive_json()
#            if song:
#                self.game.song = song
#                newState = Song(self.game)
#                newState.enterState()

        if self.players[0]:
            if pressed and self.songChoice:
                if self.songChoice == 1:
                    self.game.song = 'Earned It'
                else:
                    self.game.song = 'Gangnam Style'
                print(self.players)
    #            self.game.client.send_message([self.game.song, '_songname'])
    #            self.game.client.receive_json()
                newState = Song(self.game)
                newState.enterState()

    def updateScreen(self):
        self.game.screen.fill((0, 0, 0))
        # finish this by displaying the players' names and if they are ready
        if self.players[0] == self.game.name:
            self.button.draw()
            self.earnedButton.draw()
            self.gangnamButton.draw()
        pygame.display.update()
        

