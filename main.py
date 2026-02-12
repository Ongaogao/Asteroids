import pygame
import sys
import random
from constants import *
from logger import log_state
from player import Player
from circleshape import CircleShape
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event
from shot import Shot
from powerup import PowerUp, Super, Power



def main():
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}, Screen height: {SCREEN_HEIGHT}")
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    infinite_loop(screen, clock, frame_rate=120, player = player, updatable=updatable, drawable=drawable,asteroids=asteroids, shots=shots, powerups=powerups)

    

    


def infinite_loop(screen, clock, frame_rate, player, updatable, drawable,asteroids, shots, powerups):
    dt = 0
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


        updatable.update(dt)
        
        # Check player-asteroid collisions
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game Over!")
                sys.exit()
        
        # Check asteroid-asteroid collisions
        asteroid_list = list(asteroids)
        for i in range(len(asteroid_list)):
            for j in range(i + 1, len(asteroid_list)):
                if asteroid_list[i].collides_with(asteroid_list[j]):
                    # Resolve overlap by pushing asteroids apart
                    asteroid_list[i]._resolve_collision(asteroid_list[i], asteroid_list[j])
                    # Bounce both asteroids
                    asteroid_list[i].collision()
                    asteroid_list[j].collision()

        
        # Check shot-asteroid collisions
        for shot in shots:
            for asteroid in asteroids:
                if shot.collides_with(asteroid):
                    shot.kill()
                    asteroid.split()
                    log_event("asteroid_shot")
                    power_up = random.uniform(1,20)
                    if power_up >= 19:
                        log_event("powerup_spawned")
                        print("Power-up spawned!")
                        # Randomly choose between Super and Power powerups
                        powerup_type = random.choice([Super, Power])
                        new_powerup = powerup_type(asteroid.position.x, asteroid.position.y)

        
        # Check shot-powerup collisions
        for powerup in powerups:
            if player.collides_with(powerup):
                log_event("powerup_collected")
                print("Power-up collected!")
                powerup_type = type(powerup).__name__
                print(f"Collected {powerup_type} powerup!")
                powerup.kill()
                powerup.apply(player)
                

                    

        screen.fill("black")
        for thing in drawable:
            thing.draw(screen)

        pygame.display.flip()
        dt = clock.tick(frame_rate) / 1000.0
        

            


if __name__ == "__main__":
    main()
