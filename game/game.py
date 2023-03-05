import pygame

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

screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode([screenWidth, screenHeight])

# arrow direction:
# 0: left
# 1: up
# 2: down
# 3: right

class Arrow(pygame.sprite.Sprite):
    def __init__(self, direction, arriveTime, speed, host, player, index):
        self.x = 0
        self.y = 0
        self.direction = direction
        self.speed = speed
        self.host = host
        self.player = player
        currentTime = pygame.time.get_ticks() / 1000
        self.arriveTime = arriveTime + currentTime
        # index used to tell which arrows have been hit for opponent
        self.index = index
        self.alive = 1
        self.visible = 0
        self.__determineColour()

    def __determineColour(self):
        # host arrow colouring
        if self.speed and self.host:
            self.colour = (200, 200, 200)
        # opponent arrow colouring
        elif self.speed:
            self.colour = (180, 20, 20)
        # base arrow colouring
        elif self.direction == 0:
            self.colour = (255, 0, 0)
        elif self.direction == 1:
            self.colour = (0, 200, 0)
        elif self.direction == 2:
            self.colour = (0, 0, 255)
        elif self.direction == 3:
            self.colour = (255, 255, 255)

    def __calculatePosition(self, currentTime):
        self.x = screenWidth * (self.direction + 1) / 10 + screenWidth / 2 * (self.player) - screenWidth/32
        self.y = screenHeight / 6 + (self.arriveTime - currentTime) * self.speed - screenWidth/32
        # screenWidth/32 is the length of one side of the arrow
        if self.y > (0 - screenWidth/16) and self.y < (screenHeight + screenWidth/16):
            self.visible = 1
        else:
            self.visible = 0
    
    def __calculatePoints(self, currentTime):
        if currentTime - self.arriveTime > sensitivity:
            # this is a miss, points are 0
            # could also use this to decrease the score
            # because it is a miss
            self.alive = 1
        elif currentTime - self.arriveTime >= -sensitivity:
            # this is a hit, points are maximal if
            # current time - arrive time is small
            self.alive = 0

    def __calculateHit(self, currentTime, pressedKeys):
        if pressedKeys[K_LEFT] and self.direction == 0:
            self.__calculatePoints(currentTime)
        if pressedKeys[K_UP] and self.direction == 1:
            self.__calculatePoints(currentTime)
        if pressedKeys[K_DOWN] and self.direction == 2:
            self.__calculatePoints(currentTime)
        if pressedKeys[K_RIGHT] and self.direction == 3:
            self.__calculatePoints(currentTime)

    def draw(self, screen):
        if self.alive and self.visible:
            pygame.draw.rect(screen, self.colour, self.rect)

    # deadArrow is the list: [player, index] of an opponent arrow
    # that has been hit
    def update(self, pressedKeys, deadArrows):
        # if there is a dead arrow and its not the host arrow, kill the
        # correct arrow
        for deadArrow in deadArrows:
            if self.player == deadArrow[0] and self.index == deadArrow[1]:
                self.alive = 0

        if self.alive:
            currentTime = pygame.time.get_ticks() / 1000
            self.__calculatePosition(currentTime)
            self.rect = (self.x, self.y, screenWidth/32, screenWidth/32)

            if self.speed and self.host:
                self.__calculateHit(currentTime, pressedKeys)
                
                if not self.alive:
                    return [self.player, self.index]

        return 0

class Score():
    def __init__(self, player):
        self.player = player
        self.score = 0

    #def draw(self, screen):
        # draw score on screen above the base arrows
        # for each player
    
    # this funciton is only used until I get the graphical score
    # setup
    # for some reason this scoring is not setup
    def __printScore(self):
        print("player", self.player, "score:", self.score)

    def update(self, deadArrows):
        for deadArrow in deadArrows:
            if deadArrow[0] == self.player:
                self.score += 1
                self.__printScore()

def loadArrows(path):
    f = open(path, 'r')
    t = f.read()
    t = t.split('\n')
    t.remove('')
    for i in range(len(t)):
        t[i] = t[i].split(' ')
        for j in range(3):
            t[i][j] = float(t[i][j])

    f.close()
    return t

pygame.init()
clock = pygame.time.Clock()
fps = 60
sensitivity = 0.03
# players list
# the index represents the player and the
# number (0 or 1) represents if the player is playing
# on this machine
players = [1, 0]

# arrowData = [direction, arrive time, speed] 
arrowData = loadArrows('test_arrows')

arrows = []
scores = []

for i in range(len(players)):
    for j in range(len(arrowData)):
        arrow = Arrow(arrowData[j][0], arrowData[j][1], arrowData[j][2], players[i], i, j)
        arrows.append(arrow)
    score = Score(i)
    scores.append(score)

# a good arrow speed is ~200
def updateObjects(arrows):
    pressedKeys = pygame.key.get_pressed()
    # in final version, deadArrow will be sent by the server
    # from the opponent client
    deadArrows = []
    for arrow in arrows:
        deadArrow = arrow.update(pressedKeys, deadArrows)
        if deadArrow:
            deadArrows.append(deadArrow)

    for score in scores:
        score.update(deadArrows)

def updateScreen(screen, arrows):
    screen.fill((0, 0, 0))
    for arrow in arrows:
        arrow.draw(screen)
    pygame.display.update()

def gameLoop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    running = False
            elif event.type == pygame.QUIT:
                running = False
    
        updateObjects(arrows)
        updateScreen(screen, arrows)
    
        clock.tick(fps)
    
    pygame.quit()

gameLoop()