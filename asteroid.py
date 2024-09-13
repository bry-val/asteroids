import pygame
import random
import math
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.num_vertices = random.randint(6, 12)  # Number of vertices for the polygon
        self.jaggedness = random.uniform(0.7, 1.3)  # Controls how jagged the polygon is
        self.vertices = self.generate_vertices()  # Generates the polygon vertices once

    def generate_vertices(self):
        vertices = []
        for i in range(self.num_vertices):
            angle = (i / self.num_vertices) * 2 * math.pi  # Evenly space the vertices around a circle
            distance = self.radius * random.uniform(0.8, 1.2)  # Vary the distance for irregularity
            x = math.cos(angle) * distance  # Position relative to the center
            y = math.sin(angle) * distance
            vertices.append((x, y))
        return vertices

    def draw(self, screen):
        # Translate the pre-generated vertices to the current position
        translated_vertices = [(self.position.x + vx, self.position.y + vy) for vx, vy in self.vertices]
        pygame.draw.polygon(screen, (232, 232, 232), translated_vertices, 2)  # Draw the irregular polygon
        
        # Optionally, you can still visualize the circle for debugging purposes:
        # pygame.draw.circle(screen, "red", self.position, self.radius, 1)

    def update(self, dt):
        self.position += self.velocity * dt

        if self.position.y > SCREEN_HEIGHT + ASTEROID_MAX_RADIUS:
            self.position.y = 0 - ASTEROID_MAX_RADIUS
        elif self.position.y < 0 - ASTEROID_MAX_RADIUS:
            self.position.y = SCREEN_HEIGHT + ASTEROID_MAX_RADIUS

        if self.position.x > SCREEN_WIDTH + ASTEROID_MAX_RADIUS:
            self.position.x = 0 - ASTEROID_MAX_RADIUS
        elif self.position.x < 0 - ASTEROID_MAX_RADIUS:
            self.position.x = SCREEN_WIDTH + ASTEROID_MAX_RADIUS

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
