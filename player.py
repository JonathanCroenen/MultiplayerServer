import pygame


class Player:
    def __init__(self, id: str):
        self.id = id
        
        self.pos = pygame.Vector2()
        
        self.radius = 10.0
        self.color = pygame.Color(240, 240, 50)
        
        
    def draw(self, screen: pygame.surface.Surface):
        pygame.draw.circle(
            screen,
            self.color,
            self.pos,
            self.radius
        )
        
        
    def set_pos(self, x: int, y: int):
        self.pos.x = x
        self.pos.y = y
                