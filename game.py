# Imports
import pygame
import sys
import random
import time
import os

# Function to safely load assets whether running as script or executable
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize Pygame
pygame.init()

# Setup FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen Settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
INITIAL_SPEED = 5
SPEED = INITIAL_SPEED
SCORE = 0
HIGH_SCORE = 0

# Setup Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = font.render("Game Over", True, BLACK)

# Load Background and Assets
background = pygame.image.load(resource_path("assets/AnimatedStreet.png"))

# Setup Display
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Goat Crash")

# Load Crash Sound
crash_sound = pygame.mixer.Sound(resource_path("assets/crash.wav"))

# Classes
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(resource_path("assets/Enemy.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(resource_path("assets/Player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-PLAYER_SPEED, 0)
        if pressed_keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(PLAYER_SPEED, 0)

# Functions
def start_screen():
    DISPLAYSURF.fill(BLUE)
    title = font.render("Goat Crash", True, WHITE)
    prompt = font_small.render("Press any key to start", True, WHITE)
    high_score_display = font_small.render(f"High Score: {HIGH_SCORE}", True, WHITE)
    high_score_rect = high_score_display.get_rect()
    high_score_rect.topright = (SCREEN_WIDTH - 10, 10)
    DISPLAYSURF.blit(title, (50, 200))
    DISPLAYSURF.blit(prompt, (80, 300))
    DISPLAYSURF.blit(high_score_display, high_score_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def game_loop():
    global SPEED, SCORE, HIGH_SCORE
    SPEED = INITIAL_SPEED
    SCORE = 0

    P1 = Player()
    E1 = Enemy()
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)

    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 1500)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                if SPEED < 20:
                    SPEED += 0.5
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.blit(background, (0, 0))
        score_display = font_small.render(f"Score: {SCORE}", True, BLACK)
        high_score_display = font_small.render(f"High Score: {HIGH_SCORE}", True, BLACK)
        high_score_rect = high_score_display.get_rect()
        high_score_rect.topright = (SCREEN_WIDTH - 10, 10)

        DISPLAYSURF.blit(score_display, (10, 10))
        DISPLAYSURF.blit(high_score_display, high_score_rect)

        for entity in all_sprites:
            entity.move()
            DISPLAYSURF.blit(entity.image, entity.rect)

        pygame.display.set_caption(f"Goat Crash - Score: {SCORE}")

        if pygame.sprite.spritecollideany(P1, enemies):
            crash_sound.play()
            time.sleep(1)
            if SCORE > HIGH_SCORE:
                HIGH_SCORE = SCORE
            game_over_screen()
            running = False

        pygame.display.update()
        FramePerSec.tick(FPS)

def game_over_screen():
    DISPLAYSURF.fill(RED)
    DISPLAYSURF.blit(game_over_text, (30, 250))
    prompt_text = font_small.render("Press R to Restart or Q to Quit", True, BLACK)
    DISPLAYSURF.blit(prompt_text, (50, 350))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    waiting = False
                    game_loop()

# Main Execution
start_screen()
game_loop()