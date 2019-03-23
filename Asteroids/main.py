import os
from Game import Game
from config import config


os.environ['SDL_VIDEO_CENTERED'] = '1'
new_game = Game(config)
new_game.start()
