import pygame, sys, random, os
from pygame.locals import *

FPS = 60
WINDOWWIDTH = 1280
WINDOWHEIGHT = 720

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

pygame.font.init()
font_large = pygame.font.Font(resource_path('fonts/beachday.ttf'), 74)
font_small = pygame.font.Font(resource_path('fonts/beachday.ttf'), 36)
textSurfaceObj = font_large.render('Endless Runner', True, BLACK)
LogoRectObj = textSurfaceObj.get_rect(center=(640, 200))


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.action = action
        self.font = pygame.font.Font(resource_path('fonts/beachday.ttf'), 36)
    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        surface.blit(text_surface, text_surface.get_rect(center=self.rect.center))
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.current_color = self.hover_color if self.rect.collidepoint(event.pos) else self.color
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            if self.action: self.action()

def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

def start_game(score=0):
    global music_started

    if not music_started:
        pygame.mixer.music.load(resource_path('audio/background-music.mp3'))
        pygame.mixer.music.play(-1, 0.0)
        music_started = True

    coin_sound = pygame.mixer.Sound(resource_path('audio/orbs.mp3'))
    death_sound = pygame.mixer.Sound(resource_path('audio/death-sound.mp3'))

    gameBgImage = pygame.image.load(resource_path(resource_path("assets/bg.png")))
    gameBgImage = pygame.transform.scale(gameBgImage, (WINDOWWIDTH, WINDOWHEIGHT))
    landImage = pygame.image.load(resource_path("assets/brick.png"))
    landImage = pygame.transform.scale(landImage, (80, 70))
    land_rect = landImage.get_rect()
    land_y = WINDOWHEIGHT - land_rect.height

    num_bricks = WINDOWWIDTH // land_rect.width
    exclude = [0, 15]
    choices = [i for i in range(num_bricks) if i not in exclude]
    trench_indices = random.sample(choices, 3)
    blocks_indices = random.sample(range(num_bricks), num_bricks - 2)

    coinImage = pygame.image.load(resource_path("assets/coin.png"))
    coinImage = pygame.transform.scale(coinImage, (40, 40))
    coins = []
    for _ in range(6):
        x = random.randint(200, WINDOWWIDTH - 100)
        y = random.randint(300, 450)
        coins.append(pygame.Rect(x, y, 40, 40))

    playerimg = pygame.image.load(resource_path("assets/dog.png"))
    playerimg = pygame.transform.scale(playerimg, (80, 70))
    player_x = 10
    player_y = land_y - 50
    player_vel_y = 0
    gravity = 1
    jump_strength = -18
    on_ground = True
    player_speed = 10
    high_score = load_high_score()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            player_x -= player_speed
        if keys[K_RIGHT]:
            player_x += player_speed
        if keys[K_SPACE] and on_ground:
            player_vel_y = jump_strength
            on_ground = False

        player_vel_y += gravity
        player_y += player_vel_y

        floor_y = land_y - 50
        player_rect = pygame.Rect(player_x, player_y, 80, 50)

        on_ground = False
        for i, x in enumerate(range(0, WINDOWWIDTH, land_rect.width)):
            if i not in blocks_indices:
                block_rect = pygame.Rect(x, 500, 80, 70)
                if player_rect.colliderect(block_rect) and player_vel_y >= 0:
                    player_y = block_rect.top - 50
                    player_vel_y = 0
                    on_ground = True
                    break

        player_index = player_x // land_rect.width
        if player_index in trench_indices and player_y >= land_y:
            death_sound.play()
            msg = random.choice([
                "Nice jump… straight to your doom.",
                "Congrats, you invented lava diving.",
                "Outsmarted by a turtle, Impressive.",
                "Missed that jump? Happens… to beginners.",
                "Gravity 1 | You 0.",
                "You walked off again, didn’t you?",
                "Even the enemies feel bad for you.",
                "You really hit rock bottom.",
                "Lost your shine already?",
                "The princess isn’t impressed."
            ])
            game_over_screen(score, high_score, msg)
            return

        if player_y >= land_y - 50 and player_index not in trench_indices:
            player_y = land_y - 50
            player_vel_y = 0
            on_ground = True

        if player_x >= WINDOWWIDTH - 80:
            start_game(score)
            return

        player_x = max(0, min(player_x, WINDOWWIDTH - 80))

        for coin in coins[:]:
            if player_rect.colliderect(coin):
                coins.remove(coin)
                coin_sound.play()
                score += 1

        DISPLAYSURF.blit(gameBgImage, (0, 0))
        for i, x in enumerate(range(0, WINDOWWIDTH, land_rect.width)):
            if i not in trench_indices:
                DISPLAYSURF.blit(landImage, (x, land_y))
        for i, x in enumerate(range(0, WINDOWWIDTH, land_rect.width)):
            if i not in blocks_indices:
                DISPLAYSURF.blit(landImage, (x, 500))
        for coin in coins:
            DISPLAYSURF.blit(coinImage, (coin.x, coin.y))
        score_text = font_small.render(f"Score: {score}  High Score: {high_score}", True, BLACK)
        DISPLAYSURF.blit(score_text, (30, 30))
        DISPLAYSURF.blit(playerimg, (player_x, player_y))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def game_over_screen(score, high_score, msg):
    if score > high_score:
        save_high_score(score)
        high_score = score
    DISPLAYSURF.fill(WHITE)
    over_text = font_large.render("Game Over", True, RED)
    msg_text = font_small.render(msg, True, BLACK)
    score_text = font_small.render(f"Score: {score}  High Score: {high_score}", True, BLACK)
    restart_button = Button(440, 450, 380, 70, "Restart", RED, BLACK, start_game)
    DISPLAYSURF.blit(over_text, over_text.get_rect(center=(640, 200)))
    DISPLAYSURF.blit(msg_text, msg_text.get_rect(center=(640, 300)))
    DISPLAYSURF.blit(score_text, score_text.get_rect(center=(640, 370)))
    restart_button.draw(DISPLAYSURF)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            restart_button.handle_event(event)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def main():
    global FPSCLOCK, DISPLAYSURF, music_started
    pygame.init()
    music_started = False
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
