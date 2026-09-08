import pygame
from pathlib import Path
from consts import *
from board import Board

class GameRenderer:
    def __init__(self, screen) -> None:
        self.screen = screen
        asset_path = Path(__file__).resolve().parent / "imgs" / "pieces.png"
        self.original_image = pygame.image.load(asset_path).convert_alpha()
        self.pieces_image = pygame.transform.smoothscale(self.original_image, (SQSIZE * 6, SQSIZE * 2))
        self.piece_width = self.pieces_image.get_width() // 6
        self.piece_height = self.pieces_image.get_height() // 2
        self.highlighted_squares : list[tuple[int, int]] = []
        self.selected_quare = None

    def set_hightlighted_squares(self, squares : list[tuple[int, int]], selected : tuple[int, int]|None) -> None:
        self.highlighted_squares = squares
        self.selected_quare = selected

    def render(self, board : Board, player_color : PieceColor) -> None:
        # render squares
        for row in range(ROWS):
            for col in range(COLS):
                color = LIGHT_SQUARE_COLOR if ((row + col) % 2) == 0 else DARK_SQUARE_COLOR
                rect = pygame.Rect(col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(self.screen, color, rect)

        # render highlighted squares
        for square in self.highlighted_squares:
            row, col = square
            if player_color == PieceColor.BLACK:
                row = ROWS - row - 1
                col = COLS - col - 1
            color = HIGHLIGHT_LIGHT_SQUARE_COLOR if ((row + col) % 2) == 0 else HIGHLIGHT_DARK_SQUARE_COLOR
            rect = pygame.Rect(col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(self.screen, color, rect)
        if self.selected_quare != None:
            row, col = self.selected_quare
            if player_color == PieceColor.BLACK:
                row = ROWS - row - 1
                col = COLS - col - 1
            color = SELECTED_SQUARE_COLOR
            rect = pygame.Rect(col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(self.screen, color, rect)

        # render pieces
        for row in range(ROWS):
            for col in range(COLS):
                piece = None
                if player_color == PieceColor.WHITE:
                    piece = board.pieces[row][col]
                else:
                    piece = board.pieces[ROWS - row - 1][COLS - col - 1]

                if piece == Piece.NONE:
                    continue
                dst = (col * SQSIZE, row * SQSIZE)
                src = ((piece.value % 6) * self.piece_width, (piece.value // 6) * self.piece_height, self.piece_width, self.piece_height)
                self.screen.blit(self.pieces_image, dst, src)
