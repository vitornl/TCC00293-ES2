from .Piece import Piece
from .Square import Square
from ..ctx import background_colors, squares, piece_color_1, piece_color_2



class Table:
    __slots__ = ('table')
    def __init__(self):
        self.table = []
        for j in range(squares):
            aux = []
            for i in range(squares):
                square = Square(background_colors)
                next(background_colors)
                piece = None
                if j < 3:
                    piece = Piece(piece_color_1, [i, j])
                elif j >4:
                    piece = Piece(piece_color_2, [i, j])
                square.push_piece(piece)
                aux.append(square)
            self.table.append(aux)

    def select_piece(self, piece_position: list) -> Piece:
        return self.table[piece_position[1]][piece_position[0]].piece

    def select_square(self, position: list) -> Square:
        return self.table[position[1]][position[0]]

    def move_piece(self, origin: list, destiny: list):
        piece = self.table[origin[1]][origin[0]].pop_piece()
        piece.set_position(destiny)
        self.table[destiny[1]][destiny[0]].push_piece(piece)

    def remove_piece(self, position: list):
        self.table[position[1]][position[0]].pop_piece()

    def empty_squares(self) -> list:
        resp = []
        for line in self.table:
            for square in line:
                if not square.has_piece():
                    x = self.table.index(line)
                    y = square.index(square)
                    resp.append([y, x])
        return resp
    
    def piece_list(self, piece_color: int) -> list:
        resp = []
        for line in self.table:
            for square in line:
                if square.has_piece():
                    if square.piece.color == piece_color:
                        x = self.table.index(line)
                        y = square.index(square)
                        resp.append([y, x])
        return resp