import sys
import socket

from pygame import Surface
from network import NetworkConnection

from consts import *
from game_renderer import GameRenderer
from board import Board
from move import Move

class Player():
    def __init__(self, pieceColor : PieceColor, screen : Surface, connection : NetworkConnection) -> None:
        self.pieceColor = pieceColor

        self.renderer = GameRenderer(screen)
        self.board = Board()
        self.selected_square = None
        self.selected_piece = Piece.NONE
        
        self.connection = connection

    def get_clicked_square(self, x : int, y : int) -> tuple[int, int]:
        if self.pieceColor == PieceColor.WHITE:
            return (y // SQSIZE, x // SQSIZE)
        else:
            return ((HEIGHT - y) // SQSIZE, (WIDTH - x) // SQSIZE)

    def handle_click(self, x : int, y : int) -> None:
        if self.board.color_to_move != self.pieceColor:
            return
        
        clicked_square = self.get_clicked_square(x, y)
        
        if self.selected_square is None:
            self.selected_piece = self.board.pieces[clicked_square[0]][clicked_square[1]]

            if (self.selected_piece != Piece.NONE and getColor(self.selected_piece) == self.pieceColor):
                moves: list[Move] = (self.board.generate_piece_moves(clicked_square))

                if not moves:
                    return

                self.selected_square = clicked_square

                highlight_squares = [move.end for move in moves]

                self.renderer.set_hightlighted_squares(highlight_squares, self.selected_square,)

        else:
            moves = self.board.generate_piece_moves(self.selected_square)

            for move in moves:
                if clicked_square == move.end:
                    self.board.make_move(move)

                    self.connection.send_message("m$" + move.to_string())
                    break

            self.selected_square = None

            self.renderer.set_hightlighted_squares([], None)

    def tick(self) -> None:
        for message in self.connection.receive_messages():
            data = message.split("$")

            if data[0] == "m":
                start = (int(data[1]), int(data[2]))
                end = (int(data[3]), int(data[4]))

                is_castling = data[5] == "1"
                is_promotion = data[6] == "1"

                move = Move(start, end, is_castling, is_promotion)

                self.board.make_move(move)

                self.selected_square = None
                self.renderer.set_hightlighted_squares([], None)
        
    def render(self) -> None:
        self.renderer.render(self.board, self.pieceColor)