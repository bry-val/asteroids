import pygame_gui
from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import Player
from score import Score
from shot import Shot
from states import States
from constants import *
import pygame as pg

class Game(States):
    def __init__(self) -> None:
        super().__init__()
        self.next = 'menu'
    
    def cleanup(self):
        self.score.score = 0

    def startup(self):
        pg.init()
        self.updatable = pg.sprite.Group()
        self.drawable = pg.sprite.Group()
        self.asteroids = pg.sprite.Group()
        self.shots = pg.sprite.Group()
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_path='theme.json')


        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable)
        Player.containers = (self.updatable, self.drawable)
        Shot.containers = (self.updatable, self.drawable, self.shots)

        self.score = Score()
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.astfield = AsteroidField()
        self.score.register_observer(self.astfield)

        self.score_text = pygame_gui.elements.UILabel(relative_rect=pg.Rect((0, 0), (300, 100)), text=f"Score: {self.score.score}", manager=self.manager, )
        self.lives = pygame_gui.elements.UILabel(relative_rect=pg.Rect((SCREEN_WIDTH - 350, 0), (300, 100)), text=f"Lives: {self.player.lives + 1}", manager=self.manager, )


    def get_event(self, event):
        # if event.type == pg.KEYDOWN:
        #     print('game state Keydown')
        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
            self.done = True
        # if event.type == pg.MOUSEBUTTONDOWN:
        #     self.done = True
    
    def update(self, screen, dt):
        print(f"Number of shots: {len(self.shots)}")
        print(f"Number of asteroids: {len(self.asteroids)}")
        self.draw(screen)

        self.manager.update(dt)
        self.manager.draw_ui(screen)

        for u in self.updatable:
            u.update(dt)
        for a in self.asteroids:
            for s in self.shots:
                if a.collision(s):
                    s.kill()
                    a.split()
                    self.score.increase_score(100)
                    self.score_text.set_text(f"Score: {self.score.score}")
            if a.collision(self.player):
                a.kill()
                print(self.player.lives)
                if self.player.lives <= 0:
                    self.done = True
                    States.score = self.score.score
                    print(f"\n\t\tGame over!\t\t\n\t\tScore: {self.score.score}\n")
                    return
                else:
                    self.player.lives -= 1
                    self.lives.set_text(f"Lives: {self.player.lives + 1}")

        
        for d in self.drawable:
            d.draw(screen)

    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        