import pygame
import os

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode((500, 700))
pygame.display.set_caption("Flappy Bird Asset Test")

# Load images
try:
    bird = pygame.image.load(os.path.join("assets", "bird.png"))
    bg = pygame.image.load(os.path.join("assets", "background.png"))
    pipe = pygame.image.load(os.path.join("assets", "pipe.png"))
    base = pygame.image.load(os.path.join("assets", "base.png"))
    print("✅ All assets loaded successfully.")
except Exception as e:
    print("❌ Error loading assets:", e)
    pygame.quit()
    exit()

# Main loop to display assets
run = True
while run:
    win.blit(bg, (0, 0))
    win.blit(pipe, (300, 400))
    win.blit(base, (0, 600))
    win.blit(bird, (200, 300))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
