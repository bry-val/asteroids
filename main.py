from states import *
from gamestate import Game
from menustate import Menu
from constants import *
import sys

settings = {
    'size' : (SCREEN_WIDTH, SCREEN_HEIGHT),
    'fps' : FPS
}

app = Control(**settings)

state_dict = {
    'menu' : Menu(),
    'game' : Game()
}

app.setup_states(state_dict, 'menu')
app.main_game_loop()
pg.quit()
sys.exit()