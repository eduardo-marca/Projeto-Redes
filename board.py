from consts import *
from move import Move

class Board:
    def __init__(self):
        self.reset()
        self.color_to_move : PieceColor = PieceColor.WHITE

    def make_move(self, move : Move) -> None:
        piece : Piece = self.pieces[move.start[0]][move.start[1]] if not move.is_promotion else (Piece.WQ if self.color_to_move == PieceColor.WHITE else Piece.BQ)
        self.pieces[move.end[0]][move.end[1]] = piece
        self.pieces[move.start[0]][move.start[1]] = Piece.NONE
        if move.is_castling:
            row, col = move.end
            # short castle
            if col == 6:
                self.pieces[row][5] = self.pieces[row][7]
                self.pieces[row][7] = Piece.NONE
            # long castle
            else:
                self.pieces[row][3] = self.pieces[row][0]
                self.pieces[row][0] = Piece.NONE
        self.color_to_move = PieceColor.BLACK if self.color_to_move == PieceColor.WHITE else PieceColor.WHITE

    def reset(self) -> None:
        self.pieces = [[Piece.NONE]*ROWS for col in range(COLS)]

        # pawns
        for col in range(COLS):
            self.pieces[6][col] = Piece.WP
            self.pieces[1][col] = Piece.BP

        # knights
        self.pieces[7][1] = self.pieces[7][6] = Piece.WN
        self.pieces[0][1] = self.pieces[0][6] = Piece.BN

        # bishops
        self.pieces[7][2] = self.pieces[7][5] = Piece.WB
        self.pieces[0][2] = self.pieces[0][5] = Piece.BB


        # rooks
        self.pieces[7][0] = self.pieces[7][7] = Piece.WR
        self.pieces[0][0] = self.pieces[0][7] = Piece.BR

        # queens
        self.pieces[7][3] = Piece.WQ
        self.pieces[0][3] = Piece.BQ

        # kings
        self.pieces[7][4] = Piece.WK
        self.pieces[0][4] = Piece.BK

    def generate_piece_moves(self, square : tuple[int, int]) -> list[Move]:
        moves : list[Move] = []
        match getType(self.pieces[square[0]][square[1]]):
            case PieceType.KING:
                return self.generate_king_moves(square)
            case PieceType.QUEEN:
                return self.generate_queen_moves(square)
            case PieceType.BISHOP:
                return self.generate_bishop_moves(square)
            case PieceType.KNIGHT:
                return self.generate_knight_moves(square)
            case PieceType.ROOK:
                return self.generate_rook_moves(square)
            case PieceType.PAWN:
                return self.generate_pawn_moves(square)
        return moves

    def generate_king_moves(self, square : tuple[int, int]) -> list[Move]:
        moves : list[Move] = []
        row, col = square
        color, type = getInfo(self.pieces[square[0]][square[1]])
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                end = (row + dr, col + dc)
                if not in_board(end):
                    continue
                end_piece = self.pieces[end[0]][end[1]]
                if end_piece == Piece.NONE or getColor(end_piece) != color:
                    moves.append(Move(square, end))
        # castle
        if col == 4 and row == (7 if color == PieceColor.WHITE else 0):
            # short castle
            if (getType(self.pieces[row][7]) == PieceType.ROOK) and (getColor(self.pieces[row][7]) == color) and (self.pieces[row][5] == Piece.NONE) and (self.pieces[row][6] == Piece.NONE):
                moves.append(Move(square, (row, 6), True))
            # long castle
            if (getType(self.pieces[row][0]) == PieceType.ROOK) and (getColor(self.pieces[row][0]) == color) and (self.pieces[row][1] == Piece.NONE) and (self.pieces[row][2] == Piece.NONE) and (self.pieces[row][3] == Piece.NONE):
                moves.append(Move(square, (row, 2), True))
        return moves

    def generate_queen_moves(self, square : tuple[int, int]) -> list[Move]:
        moves : list[Move] = self.generate_bishop_moves(square)
        moves += self.generate_rook_moves(square)
        return moves

    def generate_bishop_moves(self, square : tuple[int, int]) -> list[Move]:
        moves : list[Move] = []
        row, col = square
        piece = self.pieces[row][col]
        for dr in (-1, 1):
            for dc in (-1, 1):
                end = (row + dr, col + dc)
                while(in_board(end)):
                    end_piece = self.pieces[end[0]][end[1]]
                    if(end_piece == Piece.NONE):
                        moves.append(Move(square, end))
                        end = (end[0] + dr, end[1] + dc)
                    elif(getColor(end_piece) != getColor(piece)):
                        moves.append(Move(square, end))
                        break
                    else:
                        break
        return moves

    def generate_knight_moves(self, square : tuple[int, int]) -> list[Move]:
        moves : list[Move] = []
        row, col = square
        piece = self.pieces[row][col]
        for dr in (-2, 2):
            for dc in (-1, 1):
                end = (row + dr, col + dc)
                if not in_board(end):
                    continue
                end_piece = self.pieces[end[0]][end[1]]
                if end_piece == Piece.NONE or getColor(end_piece) != getColor(piece):
                    moves.append(Move(square, end))
        for dc in (-2, 2):
            for dr in (-1, 1):
                end = (row + dr, col + dc)
                if not in_board(end):
                    continue
                end_piece = self.pieces[end[0]][end[1]]
                if end_piece == Piece.NONE or getColor(end_piece) != getColor(piece):
                    moves.append(Move(square, end))
        return moves

    def generate_rook_moves(self, square : tuple[int, int]) -> list[Move]:
        moves : list[Move] = []
        row, col = square
        piece = self.pieces[row][col]
        for dr in (-1, 1):
            end = (row + dr, col)
            while(in_board(end)):
                end_piece = self.pieces[end[0]][end[1]]
                if(end_piece == Piece.NONE):
                    moves.append(Move(square, end))
                    end = (end[0] + dr, end[1])
                elif(getColor(end_piece) != getColor(piece)):
                    moves.append(Move(square, end))
                    break
                else:
                    break
        for dc in (-1, 1):
            end = (row, col + dc)
            while(in_board(end)):
                end_piece = self.pieces[end[0]][end[1]]
                if(end_piece == Piece.NONE):
                    moves.append(Move(square, end))
                    end = (end[0], end[1] + dc)
                elif(getColor(end_piece) != getColor(piece)):
                    moves.append(Move(square, end))
                    break
                else:
                    break
        return moves

    def generate_pawn_moves(self, square : tuple[int, int]) -> list[Move]:
        moves : list[Move] = []
        row, col = square
        piece : Piece = self.pieces[row][col]
        color, type = getInfo(piece)

        if color == PieceColor.WHITE:
            if row != 0:
                if self.pieces[row-1][col] == Piece.NONE:
                    if row == 1:
                        moves.append(Move(square, (row-1, col), False, True))
                    else:
                        moves.append(Move(square, (row-1, col)))
                    if row == 6 and self.pieces[row-2][col] == Piece.NONE:
                        moves.append(Move(square, (row-2, col)))
                if col != 0 and getColor(self.pieces[row-1][col-1]) == PieceColor.BLACK:
                    if row == 1:
                        moves.append(Move(square, (row-1, col-1), False, True)) 
                    else:
                        moves.append(Move(square, (row-1, col-1)))
                if col != 7 and getColor(self.pieces[row-1][col+1]) == PieceColor.BLACK:
                    if row == 1:
                        moves.append(Move(square, (row-1, col+1), False, True))
                    else:
                        moves.append(Move(square, (row-1, col+1)))
        else:
            if row != 7:
                if self.pieces[row+1][col] == Piece.NONE:
                    if row == 6:
                        moves.append(Move(square, (row+1, col), False, True))
                    else:
                        moves.append(Move(square, (row+1, col)))
                    if row == 1 and self.pieces[row+2][col] == Piece.NONE:
                        moves.append(Move(square, (row+2, col)))
                if col != 0 and getColor(self.pieces[row+1][col-1]) == PieceColor.WHITE:
                    if row == 6:
                        moves.append(Move(square, (row+1, col-1), False, True))
                    else:    
                        moves.append(Move(square, (row+1, col-1)))
                if col != 7 and getColor(self.pieces[row+1][col+1]) == PieceColor.WHITE:
                    if row == 6:
                        moves.append(Move(square, (row+1, col-1), False, True))
                    else:    
                        moves.append(Move(square, (row+1, col+1)))
        return moves
