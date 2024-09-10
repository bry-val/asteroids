import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from shot import Shot
from score import Score
from asteroidfield import AsteroidField

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    # intention is to use difficulty as scaler for velocity.
    # difficulty = (score // 1000) + 1

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()


    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    Shot.containers = (updatable, drawable, shots)

    score = Score()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    astfield = AsteroidField()



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill(color="black")

        

        # print(f"Len of {len(updatable)}")

        for u in updatable:
            u.update(dt)
        for a in asteroids:
            score.register_observer(a)
            for s in shots:
                if a.collision(s):
                    s.kill()
                    a.split()
                    score.increase_score(10)
            if a.collision(player):
                print(f"\n\t\tGame over!\t\t\n\t\tScore: {score.score}\n")
                return
        
        for d in drawable:
            d.draw(screen)

        print(score.score)

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
    main()