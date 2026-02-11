import pygame
import random
from constants import ASTEROID_MIN_RADIUS
from circleshape import CircleShape
from constants import LINE_WIDTH
from logger import log_event



class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    
    def update(self, dt):
        self.position += self.velocity * dt  
    
    def split(self):
        self.kill()
        if self.radius == ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            split_angle = random.uniform(20, 50)
            velocity_vector_1 = self.velocity.rotate(split_angle)
            velocity_vector_2 = self.velocity.rotate(-split_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            new_asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_1.velocity = velocity_vector_1 * 1.2
            new_asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_2.velocity = velocity_vector_2 * 1.2
            
