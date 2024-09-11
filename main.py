import pygame
import pygame_gui
from constants import *
from player import Player
from asteroid import Asteroid
from shot import Shot
from score import Score
from asteroidfield import AsteroidField

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_path='theme.json')


    clock = pygame.time.Clock()

    dt = 0
    # intention is to use difficulty as scaler for velocity.w
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

    score_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (300, 100)), text=f"Score: {score.score}", manager=manager, )
    lives = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((SCREEN_WIDTH - 350, 0), (300, 100)), text=f"Lives: {player.lives}", manager=manager, )

    is_running = True

    while is_running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == score_text:
                    print('Hello World!')

            manager.process_events(event)

        manager.update(dt)
        screen.fill(color="black")
        manager.draw_ui(screen)
        
        score.register_observer(astfield)

        for u in updatable:
            u.update(dt)
        for a in asteroids:
            for s in shots:
                if a.collision(s):
                    s.kill()
                    a.split()
                    score.increase_score(100)
                    score_text.set_text(f"Score: {score.score}")
            if a.collision(player):
                a.kill()
                print(player.lives)
                if player.lives <= 0:
                    print(f"\n\t\tGame over!\t\t\n\t\tScore: {score.score}\n")
                    return
                else:
                    player.lives -= 1
                    lives.set_text(f"Lives: {player.lives}")

        
        for d in drawable:
            d.draw(screen)

        # print(score.score)

        pygame.display.flip()
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
    main()