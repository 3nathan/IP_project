try:
    import pygame
    from pygame.locals import *
except ImportError:
    print(f"couldn't load module.")
    sys.exit(2)

# arrow direction:
# 0: left
# 1: up
# 2: down
# 3: right

class Arrow(pygame.sprite.Sprite):
    def __init__(self, direction, arriveTime, speed, sensitivity, playerData, playerNumber, index, screenWidth, screenHeight):
        self.x = 0
        self.y = 0
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.direction = direction
        self.speed = speed
        self.sensitivity = sensitivity
        self.host = playerData[1]
        self.player = playerNumber
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
        # default case
        else:
            self.colour = (200, 200, 200)

    def __calculatePosition(self, currentTime):
        self.x = self.screenWidth * (self.direction + 1) / 10 + self.screenWidth / 2 * (self.player) - self.screenWidth/32
        self.y = self.screenHeight / 6 + (self.arriveTime - currentTime) * self.speed - self.screenWidth/32
        # screenWidth/32 is the length of one side of the arrow
        if self.y > (0 - self.screenWidth/16) and self.y < (self.screenHeight + self.screenWidth/16):
            self.visible = 1
        else:
            self.visible = 0
    
    def __calculatePoints(self, currentTime):
        if currentTime - self.arriveTime > self.sensitivity:
            # this is a miss, points are 0
            # could also use this to decrease the score
            # because it is a miss
            self.alive = 1
        elif currentTime - self.arriveTime >= -self.sensitivity:
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

    def isAlive(self):
        return self.alive

    def draw(self, screen):
        if self.alive and self.visible:
            self.rect = (self.x, self.y, self.screenWidth/32, self.screenWidth/32)
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

            if self.speed and self.host:
                self.__calculateHit(currentTime, pressedKeys)
                
                if not self.alive:
                    return [self.player, self.index]

        return 0

class Score():
    def __init__(self, playerName, playerNumber, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.playerNumber = playerNumber
        self.playerName = playerName
        self.score = 0
        self.font = pygame.font.SysFont('arielblack', 35)

    #def draw(self, screen):
        # draw score on screen above the base arrows
        # for each player
    def draw(self, screen):
        x = self.screenWidth / 15 + self.screenWidth / 2 * self.playerNumber
        y = self.screenHeight / 18
        text = self.font.render(self.playerName + " score: " + str(self.score), False, (255, 255, 255))
        screen.blit(text, (x, y))
    
    def update(self, deadArrows):
        for deadArrow in deadArrows:
            if deadArrow[0] == self.playerNumber:
                self.score += 1

#class Menu():
#    def __init__(self):
#    
#    def __lobby(self):
#        #get ready and players data from server
#        ready = [1, 0]
#        players = ['Player 1 name', 'Player 2 name']
#        for 



class Game():
    def __init__(self, players, path):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screenWidth = 1280
        self.screenHeight = 720
        self.screen = pygame.display.set_mode([self.screenWidth, self.screenHeight])
        self.fps = 60
        self.sensitivity = 0.03
        self.running = True
        self.players = players
        self.path = path
        self.running = 1
        self.__getData()
        self.__loadData()

    def __getData(self):
        f = open(self.path, 'r')
        self.arrowData = f.read()
        self.arrowData = self.arrowData.split('\n')
        self.arrowData.remove('')
        for i in range(len(self.arrowData)):
            self.arrowData[i] = self.arrowData[i].split(' ')
            for j in range(3):
                self.arrowData[i][j] = float(self.arrowData[i][j])
    
        f.close()

    def __loadData(self):
        self.arrows = []
        self.scores = []
        for i in range(len(self.players)):
            for j in range(len(self.arrowData)):
                # Arrow arguements (direction, arriveTime, speed, sensitivity, playerData, playerNumber, index)
                arrow = Arrow(self.arrowData[j][0], self.arrowData[j][1], self.arrowData[j][2], self.sensitivity, self.players[i], i, j, self.screenWidth, self.screenHeight)
                self.arrows.append(arrow)
            score = Score(self.players[i][0], i, self.screenWidth, self.screenHeight)
            self.scores.append(score)

    # this should be 5-10 seconds after the song ends
    # not after the las arrow has passed
    #def __isGameRunning(self):
    #    lastArrow = self.arrows[len(self.arrows)-1]
    #    if not lastArrow.isAlive():
    #        self.running = 0
    def __updateEvents(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    # send quit message to the server
                    self.running = False
            elif event.type == pygame.QUIT:
                self.running = False

    def __updateObjects(self):
        pressedKeys = pygame.key.get_pressed()
        deadArrows = []
        for arrow in self.arrows:
            deadArrow = arrow.update(pressedKeys, deadArrows)
            if deadArrow:
                deadArrows.append(deadArrow)
        for score in self.scores:
            score.update(deadArrows)

    def __updateScreen(self):
        self.screen.fill((0, 0, 0))
        for arrow in self.arrows:
            arrow.draw(self.screen)
        for score in self.scores:
            score.draw(self.screen)
        pygame.display.update()

    def gameLoop(self):
        while self.running:
            self.__updateEvents()
            self.__updateObjects()
            self.__updateScreen()
            self.clock.tick(self.fps)

        pygame.quit()

# players list
# the index represents the player number
# the string represents the player name
# the number 1 or 0 represents if the player is playing
# on this machine or not respectively
players = [['Player 1', 0], ['Player 2', 1]]

# arrowData = [direction, arrive time, speed] 

game = Game(players, 'test_arrows')

game.gameLoop()
