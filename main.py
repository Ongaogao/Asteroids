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
from powerup import PowerUp, Special, Power



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
    score = 0
    original_background = pygame.image.load("space.jpg")
    Background = pygame.transform.scale(original_background, (SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2))
    bg_rect = Background.get_rect()
    background_x = SCREEN_WIDTH /2
    background_y = SCREEN_HEIGHT /2
    bg_rect.center = (background_x, background_y)
    font = pygame.font.Font(None, 36)

    # Open the file to read the existing value
    try:
        with open("highscore.txt", "r") as f:
            content = f.read()
            high_score = int(content) if content else 0
    except FileNotFoundError:
        high_score = 0

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
                if score >= high_score:
                    with open("highscore.txt", "w") as f:
                        f.write(str(score))
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
                    score += asteroid.radius * 10
                    shot.kill()
                    asteroid.split()
                    log_event("asteroid_shot")
                    power_up = random.uniform(1,50)
                    if power_up >= 49:
                        log_event("powerup_spawned")
                        print("Power-up spawned!")
                        # Randomly choose between Special and Power powerups
                        powerup_type = random.choice([Special, Power])
                        new_powerup = powerup_type(asteroid.position.x, asteroid.position.y)

        
        # Check shot-powerup collisions
        for powerup in powerups:
            if player.collides_with(powerup):
                log_event("powerup_collected")
                powerup_type = type(powerup).__name__
                print(f"Collected {powerup_type} powerup!")
                powerup.kill()
                powerup.apply(player)
                score += 1000
                
          
        screen.blit(Background, (bg_rect.x, bg_rect.y))
        background_x = SCREEN_WIDTH / 2 - player.position.x * 0.5
        background_y = SCREEN_HEIGHT / 2 - player.position.y * 0.5
        bg_rect.center = (background_x, background_y)
        for thing in drawable:
            thing.draw(screen)

        # Draw score and high score in top-left corner with small margin
        score_text = font.render(f"Score: {score}", True, "white")
        high_score_text = font.render(f"High Score: {high_score}", True, "white")
        margin = 10
        screen.blit(score_text, (margin, margin))
        screen.blit(high_score_text, (margin, margin + 40))

        pygame.display.flip()
        dt = clock.tick(frame_rate) / 1000.0
        

            


if __name__ == "__main__":
    main()
