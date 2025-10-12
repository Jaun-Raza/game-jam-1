import pygame, sys
from pygame.locals import *
import time
import random

FPS = 30
WINDOWWIDTH = 1280
WINDOWHEIGHT = 720

GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
NAVYBLUE = ( 60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = ( 0, 255, 255)

BGCOLOR = WHITE
GAMEBGCOLOR = NAVYBLUE

pygame.font.init()
fontObj = pygame.font.Font('fonts/beachday.ttf', 74)
textSurfaceObj = fontObj.render('Endless Runner', True, BLACK)
LogoRectObj = textSurfaceObj.get_rect()
LogoRectObj.center = (640, 200)


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.action = action  # Function to call when button is clicked

        self.font = pygame.font.Font('fonts/beachday.ttf', 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.color
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):  
                if self.action:
                    self.action()


def start_game():
    pygame.mixer.music.load('audio/background-music.mp3')
    pygame.mixer.music.play(-1, 0.0)
    gameBgImage = pygame.image.load("assets/bg.png")
    gameBgImage = pygame.transform.scale(gameBgImage, (WINDOWWIDTH, WINDOWHEIGHT))
    bgx = 0
    bgy = 0
    DISPLAYSURF.blit(gameBgImage, (bgx, bgy))
    landImage = pygame.image.load("assets/brick.png")
    landImage = pygame.transform.scale(landImage, (80, 70))
    land_rect = landImage.get_rect()
    land_y = WINDOWHEIGHT - land_rect.height

    num_bricks = WINDOWWIDTH // land_rect.width
    trench_indices = random.sample(range(num_bricks), 3)  
            
    for i, x in enumerate(range(0, WINDOWWIDTH, land_rect.width)):
        if i not in trench_indices:
            DISPLAYSURF.blit(landImage, (x, land_y))

    catImage = pygame.image.load("assets/cat.png")
    catImage = pygame.transform.scale(catImage, (80, 50))
    catx = 10
    caty = 600
    direction = 'right'

    if direction == 'right':
        catx += 5
        if catx == 1270:
            catx -= 5
    DISPLAYSURF.blit(catImage, (catx, caty))



def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Endless Runner")
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(textSurfaceObj, LogoRectObj)

    start_button = Button(440, 450, 380, 70, "Start The Game!", RED, BLACK, start_game)
    start_button.draw(DISPLAYSURF)

    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            start_button.handle_event(event)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

main()