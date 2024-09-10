from constants import *
import pygame
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
    # print(f"time: {time.time()}\nself.x: {self.x}\nself.y {self.y}\nvelo: {self.velocity}\nradius: {self.radius}")
    # print(self.position)
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
        
    def update(self, dt):
        self.position += self.velocity * dt