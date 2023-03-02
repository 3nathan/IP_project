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

# guide arrows at y = screenHeight / 6

# speed = distance / time, distance = speed * time
# arrival distance = screen height / 5

class Arrow(pygame.sprite.Sprite):
    def __init__(self, direction, arriveTime, speed, host, player, index):
        self.x = 0
        self.y = 0
        self.direction = direction
        self.speed = speed
        self.host = host
        self.player = player
        self.arriveTime = arriveTime
        # index used to tell which arrows have been hit for opponent
        self.index = index
        self.alive = 1
        self.visible = 0
        self.__determineColour()

    def __determineColour(self):
        # self arrow colouring
        if self.speed and self.host:
            self.colour = (200, 200, 200)
        # opponent arrow colouring
        elif self.speed:
            self.colour = (150, 50, 50)
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
        self.x = screenWidth * (self.direction + 1) / 10 + screenWidth / 2 * (self.player % 2)
        self.y = screenHeight / 8 + (self.arriveTime - currentTime) * self.speed
        # screenWidth/32 is the length of one side of the arrow
        if self.y > (0 - screenWidth/32) and self.y < screenHeight:
            self.visible = 1
        else:
            self.visible = 0
    
    def __calculatePoints(self, currentTime):
        if currentTime - self.arriveTime > sensitivity:
            # this is a miss, points are 0
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

    def update(self, pressedKeys):
        if self.alive:
            currentTime = pygame.time.get_ticks() / 1000
            self.__calculatePosition(currentTime)
            self.rect = (self.x, self.y, screenWidth/32, screenWidth/32)

            if self.speed and self.host:
                self.__calculateHit(currentTime, pressedKeys)
                # if not self.alive send self.player and self self.index
                # to server for opponents

pygame.init()
clock = pygame.time.Clock()
fps = 60
speed = 300
sensitivity = 0.04
# players list
# the index represents the player and the
# number (0 or 1) represents if the player is playing
# on this machine
players = [0, 1]

# [direction, arrive time, speed] 
arrowData = [
        [0, 0, 0],             # base arrows
        [1, 0, 0],
        [2, 0, 0],
        [3, 0, 0],
        [0, 3.1, speed],     # moving arrows
        [3, 3.5, speed],
        [1, 4.1, speed],
        [2, 4.5, speed],
             ]
arrows = []

j = 0
for player in players:
    i = 0
    for item in arrowData:
        arrow = Arrow(item[0], item[1], item[2], player, j, i)
        arrows.append(arrow)
        i += 1
    j += 1

# a good arrow speed is ~200
def updateObjects(arrows):
    pressedKeys = pygame.key.get_pressed()
    for arrow in arrows:
        arrow.update(pressedKeys)

def updateScreen(screen, arrows):
    screen.fill((0, 0, 0))
    for arrow in arrows:
        arrow.draw(screen)
    pygame.display.update()

def main():
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

main()
