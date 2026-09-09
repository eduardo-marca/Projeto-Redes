class Move:
    def __init__(self, start : tuple[int, int], end : tuple[int, int], is_castling : bool = False, is_promotion : bool = False) -> None:
        self.start = start
        self.end = end
        self.is_castling = is_castling
        self.is_promotion = is_promotion

    def to_string(self) -> str:
        (x1, y1) = self.start
        (x2, y2) = self.end
        castle = "1" if self.is_castling else "0"
        promo = "1" if self.is_promotion else "0"
        return str(x1) + "$" + str(y1) + "$" + str(x2) + "$" + str(y2) + "$" + castle + "$" + promo
