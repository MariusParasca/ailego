from piece import Piece


class Layer:

    def __init__(self, pieces):
        self.pieces = pieces
        self.merged_pieces = []

    def _merge_pieces(self, p1, p2):
        if p1.piece_type == 0:
            for i in range(0, len(Piece.PIECES_TYPES)):
                if (p1.size_y, 2) == Piece.PIECES_TYPES[i]:
                    return Piece(i, p1.color, p1.x if p1.x < p2.x else p2.x, p1.y if p1.y < p2.y else p2.y,
                                 p1.z if p1.z < p2.z else p2.z, not p1.orientation)
        for i in range(6, len(Piece.PIECES_TYPES)):
            if (2, p1.size_y) == Piece.PIECES_TYPES[i] or (2, p1.size_x) == Piece.PIECES_TYPES[i]:
                return Piece(i, p1.color, p1.x if p1.x < p2.x else p2.x, p1.y if p1.y < p2.y else p2.y,
                             p1.z if p1.z < p2.z else p2.z, p1.orientation)

    def merge_piece(self, merged_pieces, orientation):
        pieces = []
        fail_to_merge = []
        while (1, len(merged_pieces)) not in Piece.PIECES_TYPES:
            fail_to_merge.append(merged_pieces.pop(-1))
        type = 0
        for _type in range(len(Piece.PIECES_TYPES)):
            if Piece.PIECES_TYPES[_type][0] == 1 and len(merged_pieces) == Piece.PIECES_TYPES[_type][1]:
                type = _type
                break
        pieces.append(Piece(type, merged_pieces[0][3], merged_pieces[0][0], merged_pieces[0][1], merged_pieces[0][2],
                            orientation))
        if fail_to_merge != []:
            pieces.append(Piece(0, fail_to_merge[0][3], fail_to_merge[0][0], fail_to_merge[0][1], fail_to_merge[0][2],
                                orientation))
        return pieces

    def merge_pieces(self, orientation):
        layer = self.pieces
        pieces = []
        self.merged_pieces = []
        self.merged_pieces.append(layer[0])
        for i in range(1, len(layer)):
            if (self.merged_pieces[-1][1] == layer[i][1] and self.merged_pieces[-1][0] == layer[i][0] - 1) or \
                    (self.merged_pieces[-1][1] == layer[i][1] - 1 and self.merged_pieces[-1][0] == layer[i][0]):
                self.merged_pieces.append(layer[i])
            else:
                pieces += self.merge_piece(self.merged_pieces, orientation)
                self.merged_pieces = []
                self.merged_pieces.append(layer[i])
        pieces += self.merge_piece(self.merged_pieces, orientation)
        to_pop = []
        for i in range(len(pieces) - 1):
            for j in range(i + 1, len(pieces)):
                if i not in to_pop or j not in to_pop:
                    if (pieces[i].is_valid_merge(pieces[j])):
                        to_pop.append(i)
                        to_pop.append(j)
                        pieces.append(self._merge_pieces(pieces[j], pieces[i]))
        to_pop.sort()
        while to_pop != []:
            pieces.pop(to_pop.pop(-1))
        self.merged_pieces = pieces