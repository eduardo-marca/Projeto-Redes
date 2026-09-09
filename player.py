import pygame
from pygame import Surface

from consts import PieceColor
from game import Game

class Player():
    def __init__(self, pieceColor : PieceColor, screen : Surface) -> None:
        self.pieceColor = pieceColor
        self.game = Game(pieceColor, screen)

    def tick(self) -> None:
        self.game.render()
