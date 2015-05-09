import random
import sys
import time
import pygame
import pygame.gfxdraw

from menu import *

from math import *
from pygame.locals import *

SPEED = 10       # frames per second setting
WINWIDTH = 1280  # width of the program's window, in pixels
WINHEIGHT = 720  # height in pixels
RADIUS = 5       # radius of the circles
PLAYERS = 1      # number of players

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
P1COLOUR = RED
P2COLOUR = GREEN
P3COLOUR = BLUE


def main():
    global FPS_CLOCK, SCREEN, DISPLAYSURF, MY_FONT, WINNER
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    DISPLAYSURF = pygame.Surface(SCREEN.get_size())
    pygame.display.set_caption('FarBy!')
    # pygame.mixer.music.load('test.mp3')
    # pygame.mixer.music.play(-1, 0.0)
    MY_FONT = pygame.font.SysFont('arial', 30, 1)
    WINNER = 0

    while True:
        start_screen()
        rungame()
        gameover()


class Player(object):  # class which generates random position and angle for players
    def __init__(self):
        self.running = True
        self.colour = None
        self.score = 0

    def gen(self):  # generates random position and direction
        self.x = random.randrange(50, WINWIDTH - 155)
        self.y = random.randrange(50, WINHEIGHT - 50)
        self.angle = random.randrange(0, 360)

    def move(self):  # computes current movement
        self.x += int(RADIUS * 2 * cos(radians(self.angle)))
        self.y += int(RADIUS * 2 * sin(radians(self.angle)))

    def draw(self):  # drawing players
        pygame.gfxdraw.aacircle(DISPLAYSURF, self.x, self.y, RADIUS, self.colour)
        pygame.gfxdraw.filled_circle(DISPLAYSURF, self.x, self.y, RADIUS, self.colour)


def rungame():
    global WINNER
    DISPLAYSURF.fill(BLACK)
    pygame.draw.aaline(DISPLAYSURF, WHITE, (WINWIDTH-105, 0), (WINWIDTH-105, WINHEIGHT))
    first = True
    run = True
    players_running = PLAYERS
    if PLAYERS == 3:
        max_score = 10
    else:
        max_score = 5

    # generating players
    player1 = Player()
    player2 = Player()
    player3 = Player()
    player_t = [player1, player2, player3]
    for i in range(PLAYERS):
        player_t[i].gen()

    while run:  # main loop
        # checking how many players are needed running
        if PLAYERS < 3:
            player3.running = False

        # initializing players colours
        player1.colour = P1COLOUR
        player2.colour = P2COLOUR
        player3.colour = P3COLOUR

        # generating random holes
        hole = random.randrange(1, 20)
        if hole == 3:
            player1.move()
            player1.colour = BLACK
        elif hole == 5:
            player2.move()
            player2.colour = BLACK
        elif hole == 7 and PLAYERS == 3:
            player3.move()
            player3.colour = BLACK

        for i in range(PLAYERS):  # loop for checking positions, drawing, moving and scoring for all players
            if player_t[i].running and players_running > 1:
                if player_t[i].angle < 0:
                    player_t[i].angle += 360
                elif player_t[i].angle >= 360:
                    player_t[i].angle -= 360

                # checking if someone fails
                if (player_t[i].x > WINWIDTH-115 or player_t[i].x < 3 or
                            player_t[i].y > WINHEIGHT-3 or player_t[i].y < 3 or
                            DISPLAYSURF.get_at((player_t[i].x, player_t[i].y)) != BLACK):
                    player_t[i].running = False
                    players_running -= 1

                    if i == 0:
                        if player2.running:
                            player2.score += 1
                        if player3.running:
                            player3.score += 1
                    elif i == 1:
                        if player1.running:
                            player1.score += 1
                        if player3.running:
                            player3.score += 1
                    elif i == 2:
                        if player1.running:
                            player1.score += 1
                        if player2.running:
                            player2.score += 1

                player_t[i].draw()
                player_t[i].move()

        for event in pygame.event.get():
            if event.type == QUIT:
                shutdown()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    shutdown()

        # steering
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player1.angle -= 10
        if keys[pygame.K_RIGHT]:
            player1.angle += 10
        if keys[pygame.K_a]:
            player2.angle -= 10
        if keys[pygame.K_s]:
            player2.angle += 10
        if keys[pygame.K_k]:
            player3.angle -= 10
        if keys[pygame.K_l]:
            player3.angle += 10

        # drawing scores
        scoring(player1.score, player2.score, player3.score, P1COLOUR, P2COLOUR, P3COLOUR)

        # drawing all on the screen
        SCREEN.blit(DISPLAYSURF, (0, 0))
        pygame.display.update()

        # checking if someone reach max score and win
        if players_running == 1:
            if any(n >= max_score for n in (player1.score, player2.score, player3.score)):
                run = False
                for i in range(PLAYERS):
                    if player_t[i].score == max(player1.score, player2.score, player3.score):
                        WINNER = i + 1
                continue
            pygame.time.wait(1000)
            DISPLAYSURF.fill(BLACK)
            pygame.draw.aaline(DISPLAYSURF, WHITE, (WINWIDTH-105, 0), (WINWIDTH-105, WINHEIGHT))
            first = True
            players_running = PLAYERS
            for i in range(PLAYERS):
                player_t[i].gen()
                player_t[i].running = True
            continue

        if first:  # if the game starts, wait some time
            pygame.time.wait(1500)
            first = False

        FPS_CLOCK.tick(SPEED)


def start_screen():
    global PLAYERS
    menu = Menu(['2 Players', '3 Players', 'Help', 'Exit'])
    menu.init(SCREEN)
    menu.draw()
    PLAYERS = menu.start()


def scoring(play1score, play2score, play3score, colour1, colour2, colour3):
    colour0 = WHITE
    if PLAYERS == 2:
        colour3 = BLACK
    elif PLAYERS == 1:
        colour3 = colour2 = colour1 = colour0 = BLACK
    score_msg = MY_FONT.render("Score:", 1, colour0, BLACK)
    score1_msg = MY_FONT.render("P1: " + str(play1score), 1, colour1, BLACK)
    score2_msg = MY_FONT.render("P2: " + str(play2score), 1, colour2, BLACK)
    score3_msg = MY_FONT.render("P3: " + str(play3score), 1, colour3, BLACK)
    DISPLAYSURF.blit(score_msg, (WINWIDTH - 90, WINHEIGHT/10))
    DISPLAYSURF.blit(score1_msg, (WINWIDTH - 85, WINHEIGHT/10 + 30))
    DISPLAYSURF.blit(score2_msg, (WINWIDTH - 85, WINHEIGHT/10 + 60))
    DISPLAYSURF.blit(score3_msg, (WINWIDTH - 85, WINHEIGHT/10 + 90))


def gameover():
    end_msg = MY_FONT.render("Player %d wins! Press button to go to main menu." % WINNER, 1, WHITE, BLACK)
    SCREEN.blit(end_msg, (WINWIDTH/2 - 280, WINHEIGHT/5))
    pygame.display.update()
    end = True
    while end:
        for event in pygame.event.get():
            if event.type == QUIT:
                shutdown()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    shutdown()
                else:
                    end = False
        FPS_CLOCK.tick(10)


if __name__ == '__main__':
    main()
