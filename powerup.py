from circleshape import CircleShape
import pygame

class PowerUp(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, radius=30)
    
    def apply(self, player):
        """Override in subclasses to apply the power-up effect"""
        pass
        
    def draw(self, screen):
        pass
    
    def update(self, dt):
        pass


class Special(PowerUp):
    """Spawns one additional bullet per shot"""
    def __init__(self, x, y):
        super().__init__(x, y)
        
    def draw(self, screen):
        pygame.draw.circle(screen, "yellow", self.position, self.radius, 2)
        pygame.draw.line(screen, (255, 0, 0), (self.position.x, self.position.y), (self.position.x - 8, self.position.y), 5)
        pygame.draw.line(screen, (255, 0, 0), (self.position.x, self.position.y), (self.position.x + 8, self.position.y), 5)
        pygame.draw.line(screen, (255, 0, 0), (self.position.x - 8, self.position.y), (self.position.x - 8, self.position.y - 16), 5) 
        pygame.draw.line(screen, (255, 0, 0), (self.position.x + 8, self.position.y - 16), (self.position.x - 8, self.position.y - 16), 5)  
        pygame.draw.line(screen, (255, 0, 0), (self.position.x + 8, self.position.y), (self.position.x + 8, self.position.y + 16), 5)
        pygame.draw.line(screen, (255, 0, 0), (self.position.x - 8, self.position.y + 16), (self.position.x + 8, self.position.y + 16), 5)
    
    def apply(self, player):
        player.power_up()


class Power(PowerUp):
    """Reduces shoot cooldown to 0.05 seconds for 30 seconds"""
    def __init__(self, x, y):
        super().__init__(x, y)
        
    def draw(self, screen):
        pygame.draw.circle(screen, "yellow", self.position, self.radius, 2)
        font = pygame.font.Font(None, 72)
        text = font.render("P", True, "blue")
        text_rect = text.get_rect(center=self.position)
        screen.blit(text, text_rect)
    
    def apply(self, player):
        player.activate_power_cooldown()