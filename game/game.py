import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
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
    def __init__(self, direction, colour, arriveTime, speed):
        self.x = 0
        self.y = 0
        self.direction = direction
        self.colour = colour
        self.arriveTime = arriveTime
        self.speed = speed
        self.alive = 1

    def __calculatePosition(self, currentTime):
        self.x = screenWidth * (self.direction + 1) / 10
        self.y = screenHeight / 8 + (self.arriveTime - currentTime) * self.speed
    
    
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
        if self.alive:
            pygame.draw.rect(screen, self.colour, self.rect)

    def update(self, pressedKeys):
        if self.alive:
            currentTime = pygame.time.get_ticks() / 1000
            self.__calculatePosition(currentTime)
            self.rect = (self.x, self.y, screenWidth/32, screenWidth/32)

            if self.speed:
                self.__calculateHit(currentTime, pressedKeys)

pygame.init()
clock = pygame.time.Clock()
fps = 60
speed = 300
sensitivity = 30 / speed

# [direction, rgb, arrive time, speed] 
arrowData = [
        [0, (255, 0, 0), 0, 0],             # base arrows
        [1, (0, 150, 0), 0, 0],
        [2, (0, 0, 255), 0, 0],
        [3, (255, 255, 255), 0, 0],
        [0, (100, 100, 100), 3.1, speed],     # moving arrows
        [3, (100, 100, 100), 4.5, speed],
        [2, (100, 100, 100), 4.9, speed],
        [1, (100, 100, 100), 5.3, speed],
        [2, (100, 100, 100), 6, speed],
             ]
arrows = []

# load arrow objects into arrows
for item in arrowData:
    arrow = Arrow(item[0], item[1], item[2], item[3])
    arrows.append(arrow)

# a good arrow speed is ~200
def updateObjects(arrows):
    pressedKeys = pygame.key.get_pressed()
    i = 0
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
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False
    
        updateObjects(arrows)
        updateScreen(screen, arrows)
    
        clock.tick(fps)
    
    pygame.quit()

main()
