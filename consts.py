from enum import Enum
from pygame import Color

# Screen dimensions
WIDTH = HEIGHT = 800

# Board dimensions
COLS = 8
ROWS = 8
SQSIZE = WIDTH // COLS

# Colors
BACKGROUND_COLOR = Color(255, 0, 255)
LIGHT_SQUARE_COLOR = Color(235, 236, 208)
DARK_SQUARE_COLOR = Color(119, 149, 86)
HIGHLIGHT_LIGHT_SQUARE_COLOR = Color(255, 18, 70)
HIGHLIGHT_DARK_SQUARE_COLOR = Color(192, 8, 54)
SELECTED_SQUARE_COLOR = Color(25, 128, 220)

# Chess enums
class PieceColor(Enum):
    WHITE = 0
    BLACK = 1
    NONE = 2

class PieceType(Enum):
    KING = 0
    QUEEN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    PAWN = 5

class Piece(Enum):
    WK = 0
    WQ = 1
    WB = 2
    WN = 3
    WR = 4
    WP = 5
    BK = 6
    BQ = 7
    BB = 8
    BN = 9
    BR = 10
    BP = 11
    NONE = 12

def getType(piece : Piece) -> PieceType:
    return PieceType(piece.value % 6)

def getColor(piece : Piece) -> PieceColor:
    return PieceColor(piece.value // 6)

def getInfo(piece : Piece) -> tuple[PieceColor, PieceType]:
    return (getColor(piece), getType(piece))

def in_board(square : tuple[int, int]) -> bool:
    row, col = square
    return row >= 0 and col >= 0 and row <= 7 and col <= 7

class Move:
    def __init__(self, start : tuple[int, int], end : tuple[int, int], is_castling : bool = False, is_promotion : bool = False) -> None:
        self.start = start
        self.end = end
        self.is_castling = is_castling
        self.is_promotion = is_promotion
