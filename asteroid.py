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
            
            # Spawn new asteroids further apart to prevent overlap
            separation_distance = (self.radius + new_radius)
            offset_vector = pygame.Vector2(separation_distance, 0)
            offset_1 = offset_vector.rotate(split_angle)
            offset_2 = offset_vector.rotate(-split_angle)
            
            new_asteroid_1 = Asteroid(self.position.x + offset_1.x, self.position.y + offset_1.y, new_radius)
            new_asteroid_1.velocity = velocity_vector_1 * 1.2
            new_asteroid_2 = Asteroid(self.position.x + offset_2.x, self.position.y + offset_2.y, new_radius)
            new_asteroid_2.velocity = velocity_vector_2 * 1.2
            
            # Immediately bounce new asteroids away from each other
            self._resolve_collision(new_asteroid_1, new_asteroid_2)
    
    def collision(self):
        self.velocity = self.velocity.rotate(random.uniform(20, 50))
    
    def _resolve_collision(self, asteroid1, asteroid2):
        """Push two asteroids apart to prevent overlap"""
        # Calculate separation vector
        separation = asteroid2.position - asteroid1.position
        distance = separation.length()
        
        if distance == 0:
            distance = 1
        
        # Normalize and scale by required separation
        min_distance = asteroid1.radius + asteroid2.radius
        separation = separation.normalize() * (min_distance - distance + 1)
        
        # Push asteroids apart
        asteroid1.position -= separation / 2
        asteroid2.position += separation / 2
