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
    def __init__(self, colour):
        self.x = 0
        self.y = 0
        self.colour = colour

    def __calculatePosition(self, direction, current_time, arrive_time, speed):
        self.x = screenWidth * (direction + 1) / 10
        self.y = screenHeight / 8 + (arrive_time - current_time) * speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)

    def update(self, direction, arrive_time, speed):
        current_time = pygame.time.get_ticks() / 1000
        self.__calculatePosition(direction, current_time, arrive_time, speed)
        self.rect = (self.x, self.y, screenWidth/32, screenWidth/32)

pygame.init()
clock = pygame.time.Clock()
fps = 60
speed = 300

# [direction, rgb, arrive time, speed] 
arrowData = [
        [0, (255, 0, 0), 0, 0],             # base arrows
        [1, (0, 255, 0), 0, 0],
        [2, (0, 255, 255), 0, 0],
        [3, (255, 255, 255), 0, 0],
        [0, (100, 100, 100), 3.1, speed],     # moving arrows
        [3, (100, 100, 100), 4.5, speed],
        [2, (100, 100, 100), 4.9, speed],
        [1, (100, 100, 100), 5.3, speed],
        [2, (100, 100, 100), 6, speed],
             ]
arrows = []

for item in arrowData:
    arrow = Arrow(item[1])
    arrows.append(arrow)

# a good arrow speed is ~200
def updateObjects(arrows):
    i = 0
    for arrow, item in zip(arrows, arrowData):
        arrow.update(item[0], item[2], item[3])

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
