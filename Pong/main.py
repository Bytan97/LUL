import pygame
import sys
import os
from pygame.locals import *

# init constants
BLACK = 0, 0, 0
WHITE = 255, 255, 255
display_size = 800, 600
FPS = 60
assets = 'assets'
img = 'img'
left_text = 'Greeting, use arrows & Q, A to control paddle'
right_text = 'Use Space to start. RCtr + Q to exit'
dir_name = os.path.dirname(__file__)
font_path = os.path.join(dir_name, assets, 'font', 'Inconsolata-Regular.ttf')


def load_image(name):
    fullname = os.path.join(dir_name, assets, img, name)
    image = pygame.image.load(fullname)
    if image.get_alpha is None:
        image = image.convert()
    else:
        image = image.convert_alpha()
    return image, image.get_rect()


class Ball(pygame.sprite.Sprite):
    def __init__(self, image, image_rect, x, y):
        super().__init__()
        self.image = pygame.transform.scale(image, (9, 9))
        self.size = self.image.get_size()
        self.rect = image_rect
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = [0, 0]

    def update(self):
        self.calc_new_pos()

    def calc_new_pos(self):
        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]


class Paddle(pygame.sprite.Sprite):
    def __init__(self, image, image_rect, x, y):
        super().__init__()
        self.area = pygame.display.get_surface().get_rect()
        self.image = image
        self.size = self.image.get_size()
        self.rect = image_rect
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = 12
        self.state = ''

    def update(self):
        pass

    def move_up(self):
        newpos = Rect(self.rect)
        newpos.bottom -= self.velocity
        if self.area.contains(newpos):
            self.rect.centery -= self.velocity
        self.state = 'moveup'

    def move_down(self):
        newpos = Rect(self.rect)
        newpos.bottom += self.velocity
        if self.area.contains(newpos):
            self.rect.centery += self.velocity
        self.state = 'movedown'


def main():
    # main initialize
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode(display_size)
    load = 1
    # waiting until load assets
    while load:
        ball_img, ball_rect = load_image('ball.png')
        player_l_img, player_l_rect = load_image('left_board.png')
        player_r_img, player_r_rect = load_image('right_board.png')
        load = 0
    # basic init
    pygame.display.set_caption('Pong')
    pygame.mouse.set_visible(0)

    fps_clock = pygame.time.Clock()

    # create background
    background = pygame.Surface(display_size)
    background = background.convert()
    background.fill(BLACK)

    # create font, text obj
    font = pygame.font.Font(font_path, 20)
    text_l = font.render(left_text, 1, WHITE)
    text_r = font.render(right_text, 1, WHITE)
    text_l_pos = text_l.get_rect()
    text_r_pos = text_l.get_rect()
    text_l_pos.centerx = background.get_rect().centerx
    text_r_pos.centerx = background.get_rect().centerx
    text_r_pos.centery = text_l_pos.bottom + 10
    # background.blit(text_l, text_l_pos)
    # background.blit(text_r, text_r_pos)

    # create and init ball
    ball = Ball(ball_img, ball_rect, display_size[0]/2, display_size[1]/2)
    ballspite = pygame.sprite.RenderPlain(ball)
    # player_l
    player_l = Paddle(player_l_img, player_l_rect,
                      40, display_size[1]/2)
    player_l_sprite = pygame.sprite.RenderPlain(player_l)
    # player_r
    player_r = Paddle(player_r_img, player_r_rect,
                      display_size[0] - 40, display_size[1]/2)
    player_r_sprite = pygame.sprite.RenderPlain(player_r)

    DISPLAYSURF.blit(background, (0, 0))
    pygame.display.flip()
    getTicksLastFrame = 0
    sums = 0
    # main loop
    while True:
        DISPLAYSURF.fill(BLACK)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # handle users control
        keys = pygame.key.get_pressed()
        if (keys[K_RCTRL] or keys[K_LCTRL]) and keys[K_q]:
            pygame.quit()
            sys.exit()
        if keys[K_q]:
            player_l.move_up()
        if keys[K_a]:
            player_l.move_down()

        if keys[K_UP]:
            player_r.move_up()
        if keys[K_DOWN]:
            player_r.move_down()

        # draw
        ball.update()
        player_l.update()
        player_r.update()
        ballspite.draw(DISPLAYSURF)
        player_l_sprite.draw(DISPLAYSURF)
        player_r_sprite.draw(DISPLAYSURF)
        pygame.display.flip()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    main()
