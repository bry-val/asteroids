from states import States
from constants import *
import pygame as pg
import pygame_gui
import math

class Menu(States):
    def __init__(self) -> None:
        super().__init__()
        pg.init()
        self.next = 'game'
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_path='theme.json')
    
    def cleanup(self):
        self.manager.clear_and_reset()

    def startup(self):
        self.score = pygame_gui.elements.UILabel(relative_rect=pg.Rect((SCREEN_WIDTH / 4 + 125, (SCREEN_HEIGHT / 4) + 300), (400, 100)), text=f"Your score was: {States.score}", manager=self.manager)


    def get_event(self, event):
        keys = pg.key.get_pressed()
        if keys[pg.K_f]:
            self.done = True
        # if event.type == pg.KEYDOWN:
        #     print('Menu state Keydown')
        # elif event.type == pg.MOUSEBUTTONDOWN:
        #     self.done = True
    
    def update(self, screen, dt):
        self.draw(screen)
        self.manager.update(dt)
        self.start_text = pygame_gui.elements.UILabel(relative_rect=pg.Rect((SCREEN_WIDTH / 4 + 125, (SCREEN_HEIGHT / 4) + 220), (400, 100)), text=f"Press 'f' to start.", manager=self.manager, )


    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        # self.startup()
        self.manager.draw_ui(screen)


        scale_factor = 1.0
        logo = pg.image.load('logo.png').convert_alpha()
        scale_factor = 1 + 0.125 * math.sin(pg.time.get_ticks() * 0.001)
        width = 640
        height = 256
        x, y = width // 2, height // 2
        # Scale the surface
        new_size_x = int(SCREEN_WIDTH / 4  * scale_factor)
        new_size_y = int(SCREEN_WIDTH / 4 * scale_factor)
        scaled_surface = pg.transform.scale(logo, (new_size_x, new_size_y))

        # Draw the scaled surface at the center of the screen
        screen.blit(scaled_surface, ((SCREEN_WIDTH / 8) + 300, SCREEN_HEIGHT / 8))