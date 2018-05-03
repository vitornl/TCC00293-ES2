# coding=utf-8
from ..Model.board import Board
from ..Model.piece import Piece
from ..Model.player import Player
from ..Controller.util import Util


class Rule:

    def __init__(self):
        self.board = Board()
        self.players, self.turn_player = self._set_players()
        self._init_board(self.board, self.players)

    def _set_players(self):
        p1 = Player('1', 'red')
        p2 = Player('2', 'blue')

        return (p1, p2), p2

    def _init_board(self, board, players):
        pieces = [Piece(players[0]) for i in range(12)]
        k = 0
        for i in range(0, 3):
            for j in range(0, 7, 2):
                board.add_piece(pieces[k], (j + i % 2, i))
                k += 1
        players[0].set_pieces(pieces)

        pieces = [Piece(players[1]) for i in range(12)]
        k = 0
        for i in range(5, 8):
            for j in range(0, 7, 2):
                board.add_piece(pieces[k], (j + i % 2, i))
                k += 1
        players[1].set_pieces(pieces)

    # Pega possibilidades de jogadas, mapeadas como um dicionário Peça -> Lista de Jogadas
    # A lista de jogada é uma lista de tuplas com posições possíveis
    def get_possibilities(self):
        possibilities = {}

        for i in range(0, len(self.turn_player.pieces)):
            possible_movements = self.get_possible_movements(self.turn_player.pieces[i])
            if len(possible_movements) != 0:
                #piece_position_text = Util.int_tuple_to_string(self.turn_player.pieces[i].get_position())
                possibilities[self.turn_player.pieces[i]] = possible_movements

        return possibilities

    # Pega lista de movimentos possíveis para uma peça em particular, dependendo do jogador que está jogando
    def get_possible_movements(self, piece):
        possible_movements = []

        if self.turn_player == self.players[1]: # Player 2 jogando
            candidate_movements = [(piece.position[0] - 1, piece.position[1] - 1),
                                   (piece.position[0] + 1, piece.position[1] - 1)]

        else: # Player 1 jogando
            candidate_movements = [(piece.position[0] - 1, piece.position[1] + 1),
                                   (piece.position[0] + 1, piece.position[1] + 1)]

        for i in range(len(candidate_movements)):
            if self.is_movement_possible(candidate_movements[i]):
                possible_movements.append(candidate_movements[i])

        return possible_movements

    # Checa se o movimento é possível, de acordo com as condições de contorno e ocupação de uma casa
    def is_movement_possible(self, candidate_play):
        # Condições de contorno do tabuleiro
        if candidate_play[0] < 0 or candidate_play[1] < 0 or candidate_play[0] >= len(self.board.board[0]) or \
                candidate_play[1] >= len(self.board.board):
            return False

        # Condição de ter peça na casa
        piece = self.board.get_piece(candidate_play)

        if piece is not None:
            return False

        return True

    def move_piece(self, piece_position, new_position):
        piece = self.board.get_piece(piece_position)
        self.board.move_piece(piece, new_position)

    '''
    def is_movable(self, board, new_position):
        if(self.orientation == 0 and #north
            new_position[1] > self.position[1] and #y
            (new_position[0] != self.position[0]-1 or #x
            new_position[0] != self.position[0]+1) and
            new_position != None): #empty
            return False

        elif(self.orientation == 1 and #north
            new_position[1] < self.position[1] and #y
            (new_position[0] != self.position[0]-1 or #x
            new_position[0] != self.position[0]+1) and
            new_position != None): #empty
            return False
        
        return True
    '''

    def eat_piece(self):
        pass

    '''
    def movable_piece(self, piece):
        neighborhood = self.board.get_surroundings(piece)
        for neighbor in neighborhood:
            if neighbor is None:
                return True
            if not neighbor.player is piece.player:
                return True
        return False
    '''

    def valid_moves(self, piece_position):
        pass

    def valid_pieces(self):
        pass

    def _other_player(self, player):
        if player is self.players[0]:
            return self.players[1]
        return self.players[0]

    def win_condition(self):
        for player in self.players:
            if len(player.pieces) > 0:
                for piece in player.pieces:
                    if self.movable_piece(piece):
                        break
            else:
                return self._other_player(player)
        return None

    def next_turn(self):
        self.turn_player = self._other_player(self.turn_player)