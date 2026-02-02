import pygame
from constants import *
from logger import log_state


def main():
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}, Screen height: {SCREEN_HEIGHT}")
    infinite_loop()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def infinite_loop():
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        pygame.display.flip()
            


if __name__ == "__main__":
    main()
