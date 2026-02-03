import pygame
from constants import *
from logger import log_state
from player import Player
from circleshape import CircleShape



def main():
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}, Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    infinite_loop(screen, clock, frame_rate=60, player = player)
    

    


def infinite_loop(screen, clock, frame_rate, player):
    dt = 0
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        player.draw(screen)
        
        pygame.display.flip()
        dt = clock.tick(frame_rate) / 1000.0
        

            


if __name__ == "__main__":
    main()
