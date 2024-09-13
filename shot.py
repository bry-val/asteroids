from constants import *
import pygame
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.ttl = SHOT_TTL
        self.shotsound = pygame.mixer.Sound('shot2.mp3')
        self.shotsound.set_volume(0.16)

    def draw(self, screen):
    # print(f"time: {time.time()}\nself.x: {self.x}\nself.y {self.y}\nvelo: {self.velocity}\nradius: {self.radius}")
    # print(self.position)
        pygame.draw.circle(screen, (242, 255, 0), self.position, self.radius, 10)
        
    def update(self, dt):
        self.position += self.velocity * dt
        self.ttl -= dt

        if self.ttl <= 0:
            self.kill() 

        if self.position.y > SCREEN_HEIGHT + SHOT_RADIUS:
            self.position.y = 0 - SHOT_RADIUS
        elif self.position.y < 0 - SHOT_RADIUS:
            self.position.y = SCREEN_HEIGHT + SHOT_RADIUS

        if self.position.x > SCREEN_WIDTH + SHOT_RADIUS:
            self.position.x = 0 - SHOT_RADIUS
        elif self.position.x < 0 - SHOT_RADIUS:
            self.position.x = SCREEN_WIDTH + SHOT_RADIUS