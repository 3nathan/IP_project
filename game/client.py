import pygame
import socket
import pickle
from game import Arrow
from game import Score

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_q,
    KEYDOWN,
    QUIT,
)
pygame.init()
pygame.display.set_caption('Client') #doesn't work :(

Arrow
Score
arrows = []
scores = []
players = [0, 1]
speed = 300
sensitivity = 0.02

def loadArrows(path):
    f = open(path, 'r')
    t = f.read()
    t = t.split('\n')
    t.remove('')
    for i in range(len(t)):
        t[i] = t[i].split(' ')
        for j in range(3):
            t[i][j] = float(t[i][j])

    return t

arrowData = loadArrows('test_arrows')
j = 0
for player in players:
    i = 0
    for item in arrowData:
        # i represents the arrow index, and j represents the player index
        arrow = Arrow(item[0], item[1], item[2], player, j, i)
        arrows.append(arrow)
        i += 1
    score = Score(j)
    j += 1


screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode([screenWidth, screenHeight])

#functuion for accessing the server 
def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.11.250.207"
        self.port = 12000
        self.addr = (self.server, self.port)
        self.p = self.connect()
       

#calls the connect function
def getP(self):
        return self.p

#standard TCP connection function that returns the received message
def connect(self):
    try:
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()
    except:
        pass
#fuction that sends the data to the server and receives pickled data
def sendf(self, data):
    try:
        self.client.send(str.encode(data))
        return pickle.loads(self.client.recv(2048*2))
    except socket.error as e:
        print(e)
def sendm(self, data):
    try:
        msg = data
        self.client.send(msg.encode(data))
        msg_received = self.client.recv(1024)
        print("player 2" , msg_received.decode())
    except socket.error as e:
        print(e)





def updateObjects(arrows):
    pressedKeys = pygame.key.get_pressed()
    # in final version, deadArrow will be sent by the server
    # from the opponent client
    deadArrows = []
    for arrow in arrows:
        deadArrow = arrow.update(pressedKeys, deadArrows)
        if deadArrow:
            deadArrows.append(deadArrow)

    score.update(deadArrows)

def updateScreen(screen, arrows):
    screen.fill((0, 0, 0))
    for arrow in arrows:
        arrow.draw(screen)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    player = int(getP())
    print("You are player", player)

    while run:
        clock.tick(120)
        #message version
        sendm(score)
        #receives the data for the game 
        try:
            game = sendf("get")
        except:
            run = False
            print("Couldn't get game")
            break

    
        for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_q:
                        run = False
                elif event.type == pygame.QUIT:
                    run = False
        
        updateObjects(arrows)
        updateScreen(screen, arrows)

main()          
    

