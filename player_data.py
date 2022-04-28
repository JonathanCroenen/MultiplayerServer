import pygame
import network


class PlayerData:
    def __init__(self, id: str, addr: network.address):
        self.id = id
        self.addr = addr
        self.last_ping = 0.0
        
        self.speed = 200
        self.pos = pygame.Vector2()
        self.vel = pygame.Vector2()
        
        self.radius = 10.0
        self.color = pygame.Color(240, 240, 50)
     
        
    def move(self, x: float, y: float):
        self.vel += pygame.Vector2(x, y)
         
         
    def update(self, delta):
        if self.vel.magnitude_squared() > 0:
            self.vel = self.vel.normalize() * self.speed
            
        self.pos += self.vel * delta
        self.vel = pygame.Vector2()
            
            
    def check_bounds(self, width: int, height: int):
        if self.pos.x - self.radius < 0:
            self.pos.x = self.radius
        elif self.pos.x + self.radius > width:
            self.pos.x = width - self.radius
            
        if self.pos.y - self.radius < 0:
            self.pos.y = self.radius
        elif self.pos.y + self.radius > height:
            self.pos.y = height - self.radius
    
    
    def get_data(self):
        return f"{self.id}:{int(self.pos.x)}:{int(self.pos.y)}".encode()