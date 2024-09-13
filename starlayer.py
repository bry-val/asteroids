import random
from constants import *
import pygame

class StarLayer:
    def __init__(self, speed, num_stars):
        self.speed = speed
        self.stars = [
            [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
            for _ in range(num_stars)
        ]

    def update(self, dt):
        for star in self.stars:
            star[1] += self.speed * dt  # Move the star downwards
            if star[1] > SCREEN_HEIGHT:  # If the star goes beyond the screen, reset its position
                star[0] = random.randint(0, SCREEN_WIDTH)
                star[1] = random.randint(-20, 0)

    def draw(self, screen):
        for star in self.stars:
            pygame.draw.circle(screen, (255, 255, 255), star, 1)  # Draw each star as a small white circle
