from consts import *
from game_renderer import GameRenderer
from board import Board
from pygame import Surface

class Game:
    def __init__(self, player_color: PieceColor, screen: Surface, outgoing_moves) -> None:
        self.renderer = GameRenderer(screen)
        self.board = Board()
        self.player_color = player_color
        self.outgoing_moves = outgoing_moves
        self.selected_square = None
        self.selected_piece = Piece.NONE

    def get_clicked_square(self, x : int, y : int) -> tuple[int, int]:
        if self.player_color == PieceColor.WHITE:
            return (y // SQSIZE, x // SQSIZE)
        else:
            return ((HEIGHT - y - 1) // SQSIZE, (WIDTH - x - 1) // SQSIZE)

    def handle_click(self, x : int, y : int) -> None:
        clicked_square = self.get_clicked_square(x, y)
        if(self.selected_square == None):
            self.selected_piece = self.board.pieces[clicked_square[0]][clicked_square[1]]
            if(self.selected_piece != Piece.NONE and getColor(self.selected_piece) == self.board.color_to_move):
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
                    # Send simple data instead of a Move object.  Tuples are
                    # safe to transfer through multiprocessing.Queue.
                    self.outgoing_moves.put(
                        (move.start, move.end, move.is_castling, move.is_promotion)
                    )
                    break
            self.selected_square = None
            self.renderer.set_hightlighted_squares([], None)

    def render(self) -> None:
        self.renderer.render(self.board, self.player_color)

    def apply_remote_move(self, move_data) -> bool:
        """Apply a legal move received from the other process.

        The local board independently generates the move, rather than trusting
        flags from the received message.  This keeps castling and promotion
        behaviour consistent on both boards.
        """
        try:
            start, end, _is_castling, _is_promotion = move_data
            row, col = start
            piece = self.board.pieces[row][col]
        except (TypeError, ValueError, IndexError):
            return False

        if piece == Piece.NONE or getColor(piece) == self.player_color:
            return False

        for move in self.board.generate_piece_moves(start):
            if move.end == end:
                self.board.make_move(move)
                return True
        return False
