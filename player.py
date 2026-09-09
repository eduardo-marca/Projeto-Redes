import pygame
import os
from pathlib import Path
from queue import Empty

from consts import *
from game import Game

class Player():
    def __init__(self, pieceColor: PieceColor, window_position: tuple[int, int], outgoing_moves, incoming_moves) -> None:
        self.pieceColor = pieceColor
        self.window_position = window_position
        self.outgoing_moves = outgoing_moves
        self.incoming_moves = incoming_moves

    def start(self):
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{self.window_position[0]},{self.window_position[1]}"
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f"Chess - {self.pieceColor.name.title()}")
        self.clock = pygame.time.Clock()
        asset_directory = Path(__file__).resolve().parent / "imgs"
        icon = pygame.image.load(asset_directory / "icon.png")
        pygame.display.set_icon(icon)
        self.game = Game(self.pieceColor, self.screen, self.outgoing_moves)

        try:
            self.run()
        finally:
            # Tell this player's relay thread that no more moves will arrive.
            self.outgoing_moves.put(None)
            pygame.quit()

    def run(self):
        running = True
        while running:
            self.receive_moves()

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

    def receive_moves(self) -> None:
        """Apply every move received since the previous frame without blocking."""
        while True:
            try:
                move_data = self.incoming_moves.get_nowait()
            except Empty:
                return
            self.game.apply_remote_move(move_data)
