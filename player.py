import pygame
from pygame import Surface

from consts import *
from game_renderer import GameRenderer
from board import Board
from move import Move
from comunicador import Comunicador

class Player():
    def __init__(self, pieceColor : PieceColor, screen : Surface) -> None:
        self.pieceColor = pieceColor

        self.renderer = GameRenderer(screen)
        self.board = Board()
        self.pieceColor = pieceColor
        self.selected_square = None
        self.selected_piece = Piece.NONE

        self.mec = Comunicador(1)
        self.mensagem = "e$"

    def get_clicked_square(self, x : int, y : int) -> tuple[int, int]:
        if self.pieceColor == PieceColor.WHITE:
            return (y // SQSIZE, x // SQSIZE)
        else:
            return ((HEIGHT - y) // SQSIZE, (WIDTH - x) // SQSIZE)

    def handle_click(self, x : int, y : int) -> None:
        clicked_square = self.get_clicked_square(x, y)
        if(self.selected_square == None):
            self.selected_piece = self.board.pieces[clicked_square[0]][clicked_square[1]]
            if(self.selected_piece != Piece.NONE and getColor(self.selected_piece) == self.pieceColor and getColor(self.selected_piece) == self.board.color_to_move):
                moves : list[Move] = self.board.generate_piece_moves(clicked_square)
                if not moves:
                    return
                self.selected_square = clicked_square 
                highlight_squares = []
                for move in moves:
                    highlight_squares.append(move.end)
                self.renderer.set_hightlighted_squares(highlight_squares, self.selected_square)
        else:
            moves = self.board.generate_piece_moves(self.selected_square)
            for move in moves:
                if clicked_square == move.end:
                    self.board.make_move(move)
                    self.mensagem = "m$" + move.to_string()
                    break
            self.selected_square = None
            self.renderer.set_hightlighted_squares([], None)

    def render(self) -> None:
        self.renderer.render(self.board, self.pieceColor)

    def start_tick(self) -> None:
        self.mec.enviarMensagem(self.mensagem)
        self.mensagem = "e$"

    def tick(self) -> None:
        dados = self.mec.receberMensagem().split("$")
        if dados[0] != "e":
            start = (int(dados[1]), int(dados[2]))
            end = (int(dados[3]), int(dados[4]))
            is_castling = True if dados[5] == "1" else False
            is_promotion = True if dados[6] == "1" else False
            move = Move(start, end, is_castling, is_promotion)
            self.board.make_move(move)

        self.render()
