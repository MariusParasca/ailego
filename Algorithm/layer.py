from piece import Piece
import random
import copy

class Layer:

    def __init__(self, pieces):
        self.pieces = pieces
        self.merged_pieces = []

    def merge_piece(self, piece, pieces, type, orientation = True):
        merged_pieces = []
        if orientation is False:
            for x in range(Piece.PIECES_TYPES[type][0]):
                for z in range(Piece.PIECES_TYPES[type][1]):
                    if (piece[0] + x, piece[1], piece[2] + z, piece[3]) not in pieces:
                        for x_back in range(Piece.PIECES_TYPES[type][0] - x):
                            for z_back in range(Piece.PIECES_TYPES[type][1] - z + 1):
                                if (piece[0] - x_back, piece[1], piece[2] - z_back, piece[3]) not in pieces:
                                    return [], orientation
                                else:
                                    merged_pieces.append((piece[0] - x_back, piece[1], piece[2] - z_back, piece[3]))
                        return sorted(set(merged_pieces), key=lambda x: x[2]), orientation
                    else:
                        merged_pieces.append((piece[0] + x, piece[1], piece[2] + z, piece[3]))
            return sorted(set(merged_pieces), key=lambda x: x[2]), orientation
        else:
            for z in range(Piece.PIECES_TYPES[type][0]):
                for x in range(Piece.PIECES_TYPES[type][1]):
                    if (piece[0] + x, piece[1], piece[2] + z, piece[3]) not in pieces:
                        for z_back in range(Piece.PIECES_TYPES[type][0] - z):
                            for x_back in range(Piece.PIECES_TYPES[type][1] - x + 1):
                                if (piece[0] - x_back, piece[1], piece[2] - z_back, piece[3]) not in pieces:
                                    return self.merge_piece(piece, pieces, type, False)
                                else:
                                    merged_pieces.append((piece[0] - x_back, piece[1], piece[2] - z_back, piece[3]))
                        return sorted(set(merged_pieces), key=lambda x: x[0]), orientation
                    else:
                        merged_pieces.append((piece[0] + x, piece[1], piece[2] + z, piece[3]))
        return sorted(set(merged_pieces), key=lambda x: x[0]), orientation

    def merge_pieces(self):
        nr = 1
        steps_per_layer = 50
        steps_per_piece = 50
        self.merged_pieces = []
        pieces = copy.deepcopy(self.pieces)
        random.shuffle(pieces)
        while pieces != []:
            for step_per_layer in range(steps_per_layer):
                if pieces == []:
                    break
                piece = random.choice(pieces)
                random.shuffle(pieces)
                type = 6
                for step_per_piece in range(steps_per_piece):
                    type -= 1
                    while Piece.PIECES_TYPES[type][0] == 2:
                        type = random.randint(0, len(Piece.PIECES_TYPES)) - 1
                    merged_pieces, orientation = self.merge_piece(piece, pieces, type)
                    if merged_pieces == []:
                        continue
                    nr += 1
                    self.merged_pieces.append(Piece(type, merged_pieces[0][3], merged_pieces[0][0],
                                                    merged_pieces[0][1], merged_pieces[0][2], orientation, merged_pieces))
                    for piece in merged_pieces:
                        pieces.remove(piece)
                    break
            self.compress_pieces(steps_per_layer, steps_per_piece)

    def compress_pieces(self, steps_per_layer, steps_per_piece):
        if len(self.merged_pieces) < 2:
            return
        pieces = self.merged_pieces
        random.shuffle(pieces)
        for step_per_layer in range(steps_per_layer):
            if pieces == []:
                break
            if len(pieces) < 2:
                self.merged_pieces = pieces
                return
            p1 = random.choice(pieces)
            for step_per_piece in range(steps_per_piece):
                p2 = random.choice(pieces)
                random.shuffle(pieces)
                while p1 == p2:
                    p2 = random.choice(pieces)
                if p1.piece_type == p2.piece_type and p1.orientation == p2.orientation:
                    if p1.orientation == True:
                        if p1.x == p2.x and ((p1.z + 1) == p2.z or (p1.z - 1) == p2.z ):
                            if (Piece.PIECES_TYPES[p1.piece_type][0]*2,
                                Piece.PIECES_TYPES[p1.piece_type][1]) in Piece.PIECES_TYPES:
                                type = Piece.PIECES_TYPES.index((Piece.PIECES_TYPES[p1.piece_type][0]*2, Piece.PIECES_TYPES[p1.piece_type][1]))
                                pieces.remove(p1)
                                pieces.remove(p2)
                                pieces.append(Piece(type, p1.color, p1.x if p1.x < p2.x else p2.x, p1.y, p1.z if p1.z < p2.z else p2.z, p1.orientation, p1.pieces + p2.pieces))
                                break
                    else:
                        if p1.z == p2.z and ((p1.x + 1) == p2.x or (p1.x - 1) == p2.x):
                            if (Piece.PIECES_TYPES[p1.piece_type][0] * 2,
                                Piece.PIECES_TYPES[p1.piece_type][1]) in Piece.PIECES_TYPES:
                                type = Piece.PIECES_TYPES.index(
                                    (Piece.PIECES_TYPES[p1.piece_type][0] * 2, Piece.PIECES_TYPES[p1.piece_type][1]))
                                pieces.remove(p1)
                                pieces.remove(p2)
                                pieces.append(Piece(type, p1.color, p1.x if p1.x < p2.x else p2.x, p1.y,
                                                    p1.z if p1.z < p2.z else p2.z, p1.orientation,
                                                    p1.pieces + p2.pieces))
                                break

        self.merged_pieces = pieces