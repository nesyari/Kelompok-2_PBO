import pygame
import random
import time
from pygame.locals import *

# VARIABLES
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 50

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150

wing = 'assets/audio/wing.wav'
hit = 'assets/audio/hit.wav'

pygame.mixer.init()

class Bird(pygame.sprite.Sprite):
    def __init__(self, bird_type="blackbird"):
        pygame.sprite.Sprite.__init__(self)

        # Load images based on bird type
        self.images = [
            pygame.image.load(f'assets/sprites/{bird_type}-upflap.png').convert_alpha(),
            pygame.image.load(f'assets/sprites/{bird_type}-midflap.png').convert_alpha(),
            pygame.image.load(f'assets/sprites/{bird_type}-downflap.png').convert_alpha()
        ]

        self.speed = SPEED
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize, mode):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
        self.passed = False  # New attribute to track if the pipe has been passed

        # Change color to red if night mode is selected
        if mode == "Night":
            self.image.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = -(self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((GROUND_WIDTH, GROUND_HEIGHT))
        self.image.fill((150, 75, 0))  # Brown color as placeholder

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED

def get_random_pipes(xpos, mode):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size, mode)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP, mode)
    return pipe, pipe_inverted

def mode_selection_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render("Select Mode:", True, (255, 255, 255))
    screen.blit(text, (120, 100))

    modes = ["Day", "Night"]
    positions = [(150, 200), (150, 300)]
    selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    selected = (selected - 1) % len(modes)
                elif event.key == K_DOWN:
                    selected = (selected + 1) % len(modes)
                elif event.key == K_RETURN or event.key == K_SPACE:
                    return modes[selected]

        # Redraw mode options
        screen.fill((0, 0, 0))
        screen.blit(text, (120, 100))
        for i, mode in enumerate(modes):
            color = (255, 255, 255) if i == selected else (150, 150, 150)
            mode_text = font.render(mode, True, color)
            screen.blit(mode_text, positions[i])

        pygame.display.update()

def bird_selection_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render("Select Your Bird:", True, (255, 255, 255))
    screen.blit(text, (100, 100))

    birds = ["blackbird", "whitebird", "greenbird"]
    positions = [(50, 200), (150, 200), (250, 200)]
    selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    selected = (selected - 1) % len(birds)
                elif event.key == K_RIGHT:
                    selected = (selected + 1) % len(birds)
                elif event.key == K_RETURN or event.key == K_SPACE:
                    return birds[selected]

        screen.fill((0, 0, 0))
        screen.blit(text, (100, 100))
        for i, bird in enumerate(birds):
            bird_image = pygame.image.load(f'assets/sprites/{bird}-midflap.png').convert_alpha()
            bird_rect = bird_image.get_rect(center=positions[i])
            screen.blit(bird_image, bird_rect.topleft)
            if i == selected:
                pygame.draw.rect(screen, (255, 0, 0), bird_rect, 3)

        pygame.display.update()

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Select game mode
selected_mode = mode_selection_screen()
if selected_mode == "Day":
    BACKGROUND = pygame.image.load('./assets/sprites/background-day.png')
else:
    BACKGROUND = pygame.image.load('./assets/sprites/background-night.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()

# Select bird color
selected_bird = bird_selection_screen()

# Initialize bird with the selected color
bird_group = pygame.sprite.Group()
bird = Bird(bird_type=selected_bird)
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDHT * i)
    ground_group.add(ground)
    
