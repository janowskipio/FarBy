import pygame
import sys
from pygame.locals import *

if not pygame.font.get_init():
    pygame.font.init()


class Menu(object):
    curr_position = 0
    font_size = 60
    font_style = 'bauhaus93'
    ground_colour = (0, 0, 0)
    text_colour = (255, 255, 255)
    curr_selection_colour = (60, 200, 60)

    def __init__(self, text_list):
        self.text_list = text_list
        self.fields_num = len(text_list)

    def set_colors(self, ground_color, text_colour, curr_selection):
        self.ground_colour = ground_color
        self.text_list = text_colour
        self.curr_selection_colour = curr_selection

    def set_fontsize(self, font_size):
        self.font_size = font_size

    def init(self, surface):
        self.font = pygame.font.SysFont(self.font_style, self.font_size)
        self.surface = surface

    def draw(self, move=0):
        self.surface.fill(self.ground_colour)
        if self.curr_position + move in range(self.fields_num):
            self.curr_position += move
        screen_size = self.surface.get_size()
        menu_height = self.font_size * self.fields_num + self.font_size * (self.fields_num - 1)
        center = [screen_size[0] / 2, (screen_size[1] - menu_height) / 2 + self.font_size]
        pos = [0, center[1]]
        for i in range(self.fields_num):
            pos[0] = center[0] - self.font.size(self.text_list[i])[0] / 2
            if i == self.curr_position:
                # text = self.font.render(self.text_list[i], 1, self.text_colour, self.curr_selection_colour)
                text = self.font.render(self.text_list[i], 1, self.curr_selection_colour)
                self.surface.blit(text, pos)
            else:
                text = self.font.render(self.text_list[i], 1, self.text_colour)
                self.surface.blit(text, pos)
            pos[1] += self.font_size * 1.2
        pygame.display.update()

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    shutdown()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        shutdown()
                    if event.key == K_RETURN:
                        # always the last field should be Exit
                        if self.curr_position == self.fields_num - 1:
                            shutdown()
                        elif self.curr_position == 0:
                            return 2
                        elif self.curr_position == 1:
                            return 3
                    if event.key == K_UP:
                        self.draw(-1)
                    if event.key == K_DOWN:
                        self.draw(1)
        pygame.time.wait(10)


def shutdown():
    pygame.quit()
    sys.exit()
