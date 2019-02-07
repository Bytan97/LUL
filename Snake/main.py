import pygame
import sys
import os
from pygame.locals import *


class GameObject():
    def __init__(self, x, y, w, h, velocity=[0, 0]):
        self.rect = pygame.Rect(x, y, w, h)
        self.velocity = velocity

    def center(self):
        return self.rect.center

    def left(self):
        return self.rect.left

    def top(self):
        return self.rect.top

    def bottom(self):
        return self.rect.bottom

    def draw(self, display):
        pass

    def move(self, dx, dy):
        self.rect = self.rect.move(dx, dy)

    def update(self):
        if self.velocity == [0, 0]:
            return
        self.move(* self.velocity)


class PartOfBoard(GameObject):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, velocity=[0, 0])
        self.color = color

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.rect)


class Block(GameObject):
    def __init__(self, x, y, color, w=10, h=10, velocity=[0, 0]):
        super().__init__(x, y, w, h, velocity=velocity)
        self.rect.center = x, y
        self.color = color

    def clean(self, display):
        pygame.draw.rect(display, (0, 0, 0), self.rect)

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.rect)


class Snake():
    def __init__(self, x, y):
        self.color = 255, 255, 255
        self.velocity = [0, 0]
        # self.head = Block(x, y, self.color, velocity=self.velocity)
        self.snake_list = [
            Block(x, y, self.color, velocity=self.velocity),
            Block(x, y - 15, self.color, velocity=self.velocity)
        ]
        self.tail = self.snake_list[-1]
        self.off = ""

    def draw(self, display):
        for obj in self.snake_list:
            obj.draw(display)

    def clean(self, display):
        for obj in self.snake_list:
            obj.clean(display)

    def update(self):
        self.snake_list[0].update()
        if self.off == "right":
            self.snake_list[1].velocity = []
        # for i, part in enumerate(self.snake_list):
            # if i != 0 :
                # self.snake_list[i].update()
                # self.snake_list[i].velocity = self.snake_list[i - 1].velocity

    def left(self):
        self.off = "right"
        self.velocity[0] = -10
        self.velocity[1] = 0

    def top(self):
        self.off = "bottom"
        self.velocity[1] = -10
        self.velocity[0] = 0

    def right(self):
        self.off = "left"
        self.velocity[0] = 10
        self.velocity[1] = 0

    def bottom(self):
        self.off = "top"
        self.velocity[1] = 10
        self.velocity[0] = 0


class Game():
    def __init__(self, w, h):
        self.DISPLAY_SIZE = w, h
        self.V_FLAGS = DOUBLEBUF | NOFRAME
        self.GAME_START = 0
        self.GAME_PAUSE = 0
        self.FPS = 10

        pygame.init()
        pygame.mixer.init(44100, -16, 2, 2048)
        pygame.font.init()
        pygame.event.set_allowed([QUIT, KEYDOWN])
        pygame.display.set_caption("Pong")

        self.DISPLAY = pygame.display.set_mode(self.DISPLAY_SIZE, self.V_FLAGS)
        self.DISPLAY.set_alpha(None)
        self.fps_clock = pygame.time.Clock()

        self.objects = []
        self.keys = []

    def update(self):
        for obj in self.objects:
            obj.update()

    def draw(self):
        for obj in self.objects:
            obj.draw(self.DISPLAY)

    def clean(self):
        for obj in self.objects:
            obj.clean(self.DISPLAY)

    def keys_handler(self, keys):
        if keys[K_LCTRL] & keys[K_q]:
            pygame.quit()
            sys.exit()
        if keys[K_w] and self.objects[0].off != "top":
            self.objects[0].top()
        if keys[K_s] and self.objects[0].off != "bottom":
            self.objects[0].bottom()
        if keys[K_a] and self.objects[0].off != "left":
            self.objects[0].left()
        if keys[K_d] and self.objects[0].off != "right":
            self.objects[0].right()

    def run(self):
        BlACK = 0, 0, 0
        WHITE = 255, 255, 255
        BORDER_SIZE = 10

        self.DISPLAY.fill(BlACK)

        l_board = PartOfBoard(0, BORDER_SIZE,
                              BORDER_SIZE, self.DISPLAY_SIZE[1] - BORDER_SIZE,
                              WHITE)
        t_board = PartOfBoard(0, 0,
                              self.DISPLAY_SIZE[0], BORDER_SIZE,
                              WHITE)
        r_board = PartOfBoard(self.DISPLAY_SIZE[0] - BORDER_SIZE, BORDER_SIZE,
                              BORDER_SIZE, self.DISPLAY_SIZE[1],
                              WHITE)
        b_board = PartOfBoard(0, self.DISPLAY_SIZE[1] - BORDER_SIZE,
                              self.DISPLAY_SIZE[0], BORDER_SIZE,
                              WHITE)

        self.objects.append(l_board)
        self.objects.append(r_board)
        self.objects.append(t_board)
        self.objects.append(b_board)
        self.draw()
        self.objects = []
        snake = Snake(400, 300)
        self.objects.append(snake)
        # print(self.objects[0].update)

        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.clean()
            self.update()

            self.keys = pygame.key.get_pressed()
            self.keys_handler(self.keys)

            self.draw()

            pygame.display.flip()
            if self.fps_clock.get_fps() < 30:
                print(self.fps_clock.get_fps())
            self.fps_clock.tick(self.FPS)


if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    game = Game(800, 600)
    game.run()
