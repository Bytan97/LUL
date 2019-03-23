import pygame as pg
from sys import exit


class Game():
    def __init__(self, config):
        pg.init()
        pg.mixer.init(44100, -16, 2, 2048)
        pg.display.set_caption(config["caption"])
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN])
        pg.mouse.set_visible(0)

        w, h = config['w'], config['h']
        self.DISPLAY = pg.display.set_mode([w, h], pg.DOUBLEBUF)
        self.DISPLAY.set_alpha(0)
        self.FPS_CLOCK = pg.time.Clock()
        self.FPS = 60
        self.KEYS = []

    def start(self):
        while 1:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)

            # test
            cur_fps = self.FPS_CLOCK.get_fps()
            if cur_fps < 60:
                print(cur_fps)
            # test

            pg.display.update()

            self.FPS_CLOCK.tick(self.FPS)
