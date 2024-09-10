import pygame
import time
import random
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        # print(f"time: {time.time()}\nself.x: {self.x}\nself.y {self.y}\nvelo: {self.velocity}\nradius: {self.radius}")
        # print(self.position)
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
        
    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            angle = random.uniform(20, 50)
            pos = self.velocity.rotate(angle)
            neg = self.velocity.rotate(-angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS 
            pos_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            neg_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            pos_asteroid.velocity = pos * 1.2
            neg_asteroid.velocity = neg * 1.2