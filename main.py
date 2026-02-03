import pygame
from constants import *
from logger import log_state



def main():
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}, Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    infinite_loop(screen,clock, frame_rate=60)

    


def infinite_loop(screen, clock, frame_rate):
    dt = 0
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        pygame.display.flip()
        dt = clock.tick(frame_rate) / 1000.0

            


if __name__ == "__main__":
    main()
