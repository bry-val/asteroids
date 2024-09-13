from starlayer import StarLayer
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
        self.score = None
        self.start_text = pygame_gui.elements.UILabel(
            relative_rect=pg.Rect((SCREEN_WIDTH // 2 - 200, (SCREEN_HEIGHT // 4) + 220), (400, 100)), 
            text=f"Press 'f' to start.", 
            manager=self.manager
        )
        self.star_layers = [StarLayer(speed, NUM_STARS) for speed in PARALLAX_SPEEDS]
    
    def cleanup(self):
        self.manager.clear_and_reset()

    def startup(self):
        # Centered score label
        self.score = pygame_gui.elements.UILabel(
            relative_rect=pg.Rect((SCREEN_WIDTH // 2 - 200, (SCREEN_HEIGHT // 4) + 300), (400, 100)), 
            text=f"Your score was: {States.score}", 
            manager=self.manager
        )
        
        # Centered start text label
        self.start_text = pygame_gui.elements.UILabel(
            relative_rect=pg.Rect((SCREEN_WIDTH // 2 - 200, (SCREEN_HEIGHT // 4) + 220), (400, 100)), 
            text=f"Press 'f' to start.", 
            manager=self.manager
        )


    def get_event(self, event):
        keys = pg.key.get_pressed()
        if keys[pg.K_f]:
            self.done = True

    def update(self, screen, dt):
        self.manager.update(dt)
        self.draw(screen)

        for layer in self.star_layers:
            layer.update(dt)
            layer.draw(screen)
        

    def draw(self, screen):
        screen.fill((45, 34, 56))  # Fill background with black
        self.manager.draw_ui(screen)  # Draw UI elements
        
        # Load and scale the logo
        logo = pg.image.load('logo.png').convert_alpha()
        creds = pg.image.load('credit.png').convert_alpha()

        # Scale factor based on time for a smooth sine wave effect
        scale_factor = 0.50 + 0.025 * math.sin(pg.time.get_ticks() * 0.002)

        # Get original logo dimensions
        logo_width, logo_height = logo.get_size()

        # Calculate new size with scaling
        new_size_x = int(logo_width * scale_factor)
        new_size_y = int(logo_height * scale_factor)

        # Scale the logo surface
        scaled_surface = pg.transform.scale(logo, (new_size_x, new_size_y))

        # Calculate position to center the logo on the screen
        center_x = (SCREEN_WIDTH - new_size_x) // 2
        center_y = (SCREEN_HEIGHT - new_size_y) // 2 - 150

        # Draw the scaled surface centered on the screen
        screen.blit(scaled_surface, (center_x, center_y))
        screen.blit(creds, (SCREEN_WIDTH // 3 - 30, SCREEN_HEIGHT - 50))
