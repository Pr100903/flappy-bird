import pygame
import os
import random
import time

pygame.init()

# Window setup
WIN_WIDTH = 500
WIN_HEIGHT = 700
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird - Playable")

# Load assets
BIRD_IMG = pygame.image.load(os.path.join("assets", "bird.png"))
PIPE_IMG = pygame.image.load(os.path.join("assets", "pipe.png"))
BASE_IMG = pygame.image.load(os.path.join("assets", "base.png"))
BG_IMG = pygame.image.load(os.path.join("assets", "background.png"))

FONT = pygame.font.SysFont("comicsans", 50)

# Game constants
GRAVITY = 1.5
JUMP_VELOCITY = -10.5
PIPE_GAP = 200
PIPE_VEL = 5

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.tick = 0
        self.img = BIRD_IMG
        self.height = self.y

    def jump(self):
        self.velocity = JUMP_VELOCITY
        self.tick = 0
        self.height = self.y

    def move(self):
        self.tick += 1
        displacement = self.velocity + GRAVITY * self.tick
        if displacement >= 16:
            displacement = 16
        self.y += displacement

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(100, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + PIPE_GAP

    def move(self):
        self.x -= PIPE_VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        return b_point or t_point

class Base:
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = BASE_IMG.get_width()

    def move(self):
        self.x1 -= PIPE_VEL
        self.x2 -= PIPE_VEL
        if self.x1 + BASE_IMG.get_width() < 0:
            self.x1 = self.x2 + BASE_IMG.get_width()
        if self.x2 + BASE_IMG.get_width() < 0:
            self.x2 = self.x1 + BASE_IMG.get_width()

    def draw(self, win):
        win.blit(BASE_IMG, (self.x1, self.y))
        win.blit(BASE_IMG, (self.x2, self.y))

def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(win)
    text = FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    base.draw(win)
    bird.draw(win)
    pygame.display.update()

def game_over_screen(win, score):
    text1 = FONT.render("Game Over!", True, (255, 0, 0))
    text2 = FONT.render(f"Score: {score}", True, (255, 255, 255))
    text3 = pygame.font.SysFont("comicsans", 30).render(
        "Press any key to restart or ESC to quit", True, (255, 255, 255)
    )

    win.blit(BG_IMG, (0, 0))
    win.blit(text1, (WIN_WIDTH//2 - text1.get_width()//2, 200))
    win.blit(text2, (WIN_WIDTH//2 - text2.get_width()//2, 270))
    win.blit(text3, (WIN_WIDTH//2 - text3.get_width()//2, 350))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                else:
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def run_game():
    bird = Bird(200, 300)
    base = Base(630)
    pipes = [Pipe(600)]
    clock = pygame.time.Clock()
    score = 0
    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.move()
        base.move()

        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird):
                print("💥 You Crashed! Game Over.")
                run = False

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        if bird.y + BIRD_IMG.get_height() >= 630 or bird.y < 0:
            print("💥 Hit the ground or flew too high. Game Over.")
            run = False

        draw_window(win, bird, pipes, base, score)

    game_over_screen(win, score)

def main():
    while True:
        run_game()

main()
pygame.quit()
