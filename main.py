import pygame
import sys

from consts import *
from game import Game
from player import Player

screen = pygame.display.set_mode((2*WIDTH+3*BORDER, HEIGHT+2*BORDER))
pygame.display.set_caption("Chess")
icon = pygame.image.load('imgs/icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

player1_surface = pygame.Surface((WIDTH, HEIGHT))
player2_surface = pygame.Surface((WIDTH, HEIGHT))

game = Game(PieceColor.WHITE, screen)

def main():
    pygame.init()

    player1 = Player(PieceColor.WHITE, player1_surface)
    player2 = Player(PieceColor.BLACK, player2_surface)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x >= BORDER and x <= BORDER + WIDTH and y >= BORDER and y <= BORDER + WIDTH:
                    player1.game.handle_click(x-BORDER, y-BORDER)
                elif x >= 2*BORDER + WIDTH and x <= 2*(BORDER+WIDTH) and y >= BORDER and y <= BORDER + WIDTH:
                    player2.game.handle_click(x-2*BORDER-WIDTH, y-BORDER)

        player1.tick()
        player2.tick()

        screen.fill(BACKGROUND_COLOR)
        screen.blit(player1_surface, (BORDER, BORDER))
        screen.blit(player2_surface, (2*BORDER+WIDTH, BORDER))

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
    