import pygame
import os
from sys import exit
from random import randint


class Border():
    def __init__(self, surface, x, y, w, h):
        self.rect = pygame.rect.Rect(x, y, w, h)
        self.draw_surf = surface
        self.draw_color = 255, 255, 255

    def draw(self):
        pygame.draw.rect(self.draw_surf, self.draw_color, self.rect)


class Food():
    def __init__(self, surface, scale):
        self.rect = pygame.rect.Rect(0, 0, scale, scale)
        self.scale = scale
        self.draw_surf = surface
        self.area = surface.get_rect()
        self.draw_color = 255, 0, 0
        self.redraw_color = 0, 0, 0
        self.rect.centerx = randint(self.scale, self.area.w - self.scale)
        self.rect.centery = randint(self.scale, self.area.h - self.scale)

    def update(self, ate_flag):
        if ate_flag:
            self.clear()
            self.rect.centerx = randint(self.scale, self.area.w - self.scale)
            self.rect.centery = randint(self.scale, self.area.h - self.scale)

    def draw(self):
        pygame.draw.rect(self.draw_surf, self.draw_color, self.rect)

    def clear(self):
        pygame.draw.rect(self.draw_surf, self.redraw_color, self.rect)


class Snake():
    def __init__(self, surface, scale):
        self.rect = pygame.rect.Rect(0, 0, scale, scale)
        self.draw_surf = surface
        self.area = surface.get_rect()
        self.rect.center = self.area.center
        self.scale = scale
        self.velocity = 0, 0
        self.direction_blocked = ""
        self.size = 0
        self.tail = []

    def update(self):
        self.clear()
        if len(self.tail) != 0:
            del self.tail[0]

        if self.size >= 1:
            self.tail.append(pygame.rect.Rect(self.rect))

        self.rect.centerx += self.velocity[0] * self.scale
        self.rect.centery += self.velocity[1] * self.scale

    def collision(self, border):
        if self.rect.collidelist(border) != -1:
            self.clear()
            self.size = 0
            self.tail = []
            self.velocity = 0, 0
            self.rect.center = self.area.center
            return 1

        if self.rect.collidelist(self.tail) != -1:
            self.clear()
            self.size = 0
            self.tail = []
            self.velocity = 0, 0
            self.rect.center = self.area.center
            return 1

        return 0

    def eat(self, food):
        if self.rect.colliderect(food):
            self.size += 1
            self.tail.append(pygame.rect.Rect(self.rect))

            return 1
        return 0

    def draw(self):
        for elem in self.tail:
            pygame.draw.rect(self.draw_surf, (255, 255, 255), elem)
        pygame.draw.rect(self.draw_surf, (255, 255, 255), self.rect)

    def clear(self):
        for elem in self.tail:
            pygame.draw.rect(self.draw_surf, (0, 0, 0), elem)
        pygame.draw.rect(self.draw_surf, (0, 0, 0), self.rect)

    def left(self):
        if self.direction_blocked != "left":
            self.velocity = -1, 0
            self.direction_blocked = "right"

    def up(self):
        if self.direction_blocked != "up":
            self.velocity = 0, -1
            self.direction_blocked = "down"

    def right(self):
        if self.direction_blocked != "right":
            self.velocity = 1, 0
            self.direction_blocked = "left"

    def down(self):
        if self.direction_blocked != "down":
            self.velocity = 0, 1
            self.direction_blocked = "up"


class Game():
    def __init__(self, screen_w, screen_h, flags, col_depth, caption, fps):
        pygame.init()
        pygame.mixer.init(44100, -16, 2, 2048)
        pygame.display.set_caption(caption)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
        pygame.mouse.set_visible(0)
        self.DISPLAYSURF = pygame.display.set_mode((screen_w, screen_h),
                                                   flags, col_depth)
        self.DISPLAYSURF.set_alpha(0)
        self.FPS_CLOCK = pygame.time.Clock()
        self.FPS = fps
        self.GAME_START_FLAG = 0
        self.PAUSE_GAME_FLAG = 0
        self.keys = []

    def handle_ev(self, snake, sound):
        if self.keys[pygame.K_LCTRL] & self.keys[pygame.K_q]:
            pygame.quit()
            exit()
        if self.PAUSE_GAME_FLAG:
            if self.keys[pygame.K_w]:
                snake.up()
            elif self.keys[pygame.K_s]:
                snake.down()
            elif self.keys[pygame.K_a]:
                snake.left()
            elif self.keys[pygame.K_d]:
                snake.right()
        if self.keys[pygame.K_SPACE] and not self.PAUSE_GAME_FLAG:
            pygame.mixer.Sound.play(sound)
            pygame.mixer.music.load("polk_bc.mp3")
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
            self.PAUSE_GAME_FLAG = 1

    def start(self):
        self.GAME_START_FLAG = 1

        start_sound = pygame.mixer.Sound("1.ogg")
        start_sound.set_volume(0.1)
        pygame.mixer.music.load("main_menu_bc.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        scale = 15
        disp_s = self.DISPLAYSURF.get_size()

        snake = Snake(self.DISPLAYSURF, scale)
        food = Food(self.DISPLAYSURF, scale)

        left_board = Border(self.DISPLAYSURF, 0, 0,
                            scale, disp_s[1])
        top_board = Border(self.DISPLAYSURF, scale, 0,
                           disp_s[0] - scale, scale)
        right_board = Border(self.DISPLAYSURF, disp_s[0] - scale, 0,
                             scale, disp_s[1])
        bottom_board = Border(self.DISPLAYSURF, scale, disp_s[1] - scale,
                              disp_s[0] - scale, scale)

        border = [left_board, top_board, right_board, bottom_board]
        for elem in border:
            elem.draw()

        # create control event
        control_event = pygame.USEREVENT + 1
        pygame.time.set_timer(control_event, 1)

        # main loop
        while self.GAME_START_FLAG:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == control_event:
                    self.keys = pygame.key.get_pressed()
                    self.handle_ev(snake, start_sound)

            # print(self.FPS_CLOCK.get_fps())

            pygame.display.update()
            collision = snake.collision(border)
            ate_flag = snake.eat(food.rect)
            if self.PAUSE_GAME_FLAG:
                snake.update()
                food.update(ate_flag)

            food.draw()
            snake.draw()
            print(collision)
            if collision:
                self.PAUSE_GAME_FLAG = 0
                for elem in border:
                    elem.draw()

            self.FPS_CLOCK.tick(self.FPS)


if __name__ == "__main__":
    FLAGS = pygame.DOUBLEBUF | pygame.NOFRAME
    DEPTH = 8
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    GAME = Game(800, 600, FLAGS, DEPTH, "Snake", 15)
    GAME.start()
