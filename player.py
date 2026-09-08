import pygame
import os
from pathlib import Path

from consts import *
from game import Game

class Player():
    def __init__(self, pieceColor: PieceColor, window_position: tuple[int, int]) -> None:
        self.pieceColor = pieceColor
        self.window_position = window_position

    def start(self):
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{self.window_position[0]},{self.window_position[1]}"
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f"Chess - {self.pieceColor.name.title()}")
        self.clock = pygame.time.Clock()
        asset_directory = Path(__file__).resolve().parent / "imgs"
        icon = pygame.image.load(asset_directory / "icon.png")
        pygame.display.set_icon(icon)
        self.game = Game(self.pieceColor, self.screen)

        self.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.game.handle_click(x, y)
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos

            self.screen.fill(BACKGROUND_COLOR)

            self.game.render()

            pygame.display.flip()

            self.clock.tick(60)
    
        pygame.quit()
