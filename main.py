import pygame
from consts import *
from game import Game
from threading import Thread

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
icon = pygame.image.load('imgs/icon.png')
pygame.display.set_icon(icon)

game = Game(PieceColor.WHITE, screen)

def main():
    pygame.init()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                game.handle_click(x, y)
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos

        screen.fill(BACKGROUND_COLOR)

        game.render()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
    