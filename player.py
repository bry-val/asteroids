import pygame
import math
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    # def __init__(self, x, y):
    #     super().__init__(x, y, PLAYER_RADIUS)
    #     self.lives = 2
    #     self.rotation = 0
    #     self.timer = 0
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.lives = 2
        self.rotation = 0
        self.rotation_velocity = 0
        self.rotation_damping = 0.95  # How much rotation slows down per frame
        self.rotation_acceleration = 350  # Acceleration when rotating
        self.timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 300  # Acceleration rate
        self.deceleration = 0.98  # Deceleration rate
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, (149, 107, 255), self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    # def update(self, dt):
    #     keys = pygame.key.get_pressed()

    #     if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    #         self.rotate(-dt)
    #     if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    #         self.rotate(dt)
    #     if keys[pygame.K_UP] or keys[pygame.K_w]:
    #         self.move(dt)
    #     if keys[pygame.K_DOWN] or keys[pygame.K_s]:
    #         self.move(-dt)
    #     if keys[pygame.K_SPACE]:
    #         if self.timer > 0.0:
    #             pass
    #         else:
    #             self.shoot()
    #             self.timer = PLAYER_SHOOT_COOLDOWN
    #     self.timer -= dt
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotation_velocity -= self.rotation_acceleration * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotation_velocity += self.rotation_acceleration * dt
        
        self.rotation_velocity *= self.rotation_damping  # Apply damping to rotation velocity
        self.rotation += self.rotation_velocity * dt  # Update rotation based on velocity

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.apply_thrust(dt)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.apply_thrust(-dt)

        self.velocity *= self.deceleration  # Apply deceleration to velocity
        self.position += self.velocity * dt

        self.wrap_around_screen()
        
        if keys[pygame.K_SPACE]:
            if self.timer > 0.0:
                pass
            else:
                self.shoot()
                self.timer = PLAYER_SHOOT_COOLDOWN
        self.timer -= dt

    def apply_thrust(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * self.acceleration * dt

    def wrap_around_screen(self):
        # Horizontal wrapping
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH

        # Vertical wrapping
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity += pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def collides_with_circle(self, circle):
        # Check if any vertex of the player's triangle is inside the circle
        triangle_vertices = self.triangle()
        if any(self.point_in_circle(vertex, circle) for vertex in triangle_vertices):
            return True
        
        # Check if the circle's center is inside the player's triangle
        if self.point_in_polygon(circle.position, triangle_vertices):
            return True
        
        # Check if any edge of the player's triangle intersects with the circle
        for i in range(len(triangle_vertices)):
            v1 = triangle_vertices[i]
            v2 = triangle_vertices[(i + 1) % len(triangle_vertices)]
            if self.line_intersects_circle(v1, v2, circle):
                return True

        return False

    def point_in_circle(self, point, circle):
        # Check if a point is inside a circle
        return pygame.math.Vector2(point).distance_to(circle.position) <= circle.radius

    def point_in_polygon(self, point, polygon):
        # Check if a point is inside a polygon using the ray-casting algorithm
        x, y = point.x, point.y
        inside = False
        n = len(polygon)
        p1x, p1y = polygon[0].x, polygon[0].y
        for i in range(n + 1):
            p2x, p2y = polygon[i % n].x, polygon[i % n].y
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def line_intersects_circle(self, v1, v2, circle):
        # Check if the line segment from v1 to v2 intersects with the circle
        # Find the closest point on the line segment to the circle center
        line_segment = pygame.math.Vector2(v2.x - v1.x, v2.y - v1.y)
        to_circle = pygame.math.Vector2(circle.position.x - v1.x, circle.position.y - v1.y)
        line_length = line_segment.length()
        line_segment.normalize_ip()
        projection = to_circle.dot(line_segment)

        # Find the closest point on the line segment to the circle center
        if projection < 0:
            closest_point = pygame.math.Vector2(v1.x, v1.y)
        elif projection > line_length:
            closest_point = pygame.math.Vector2(v2.x, v2.y)
        else:
            closest_point = pygame.math.Vector2(v1.x, v1.y) + line_segment * projection

        # Check if the distance from the closest point to the circle center is less than the circle radius
        return pygame.math.Vector2(closest_point.x - circle.position.x, closest_point.y - circle.position.y).length() <= circle.radius
