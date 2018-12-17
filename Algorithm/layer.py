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

    def is_stable_with_layer(self, top_layer):
        # generez suprafetele de contact a ambelor layere
        # la layer-ul actual mai intai tre sa fie piesa apoi coordonata
        self_pieces_with_points_coordinates = []  # list of tuples
        self_layer_surface = 0
        for piece_index, self_piece in enumerate(self.pieces):
            point_coordinates_per_piece_arr = self_piece.contact_surface()  # lista de tuple ce reprezinta coordonate
            self_layer_surface += len(point_coordinates_per_piece_arr)
            piece_with_point_coordinates = {
                'piece_id': piece_index,
                'contact_points': point_coordinates_per_piece_arr
            }
            self_pieces_with_points_coordinates.append(piece_with_point_coordinates)
            # below is not used
            # for point_coordinates in point_coordinates_per_piece_arr:
            #     point_coordinates_with_piece = (point_coordinates, piece_index)  # ((x, y, z), piece_id)
            #     self_pieces_with_points_coordinates.append(point_coordinates_with_piece)
        # reprezentarea e diferita, la top layer mai intai tre sa fie coordonatele
        top_layer_pieces_with_contact_surface_dict = {}
        for piece_index, top_layer_piece in enumerate(top_layer.pieces):
            point_coordinates_per_piece_arr = top_layer_piece.contact_surface()
            # tre sa fie un dictionar cu key = coordonata in string si value piece_id
            for point_coordinates in point_coordinates_per_piece_arr:
                # tre de facut functie
                string_coordinate = str(point_coordinates[0]) + '_' + \
                                    str(point_coordinates[1])
                top_layer_pieces_with_contact_surface_dict[string_coordinate] = piece_index
                # not used below
                # point_coordinates_with_piece = (point_coordinates, piece_index)  # ((x, y, z), piece_id)
                # top_layer_pieces_with_contact_surface.append(point_coordinates_with_piece)

        # pe baza layer-ul actual(self) verific daca e stabil cu cel de sus(top_layer)
        # verific fiecare coordonata din layer-ul actual(self) cu ce piesa exista deasupra lui
        # in layer-ul de sus(top_layer)
        # iterez prin piese nu prin coordonate

        weak_pieces_id = []
        # pieces_ok = 0
        for self_piece_with_points_coordinates in self_pieces_with_points_coordinates:
            top_layer_pieces = set()
            piece_empty_points = 0
            piece_id = self_piece_with_points_coordinates['piece_id']
            for point_coordinates in self_piece_with_points_coordinates['contact_points']:
                string_coordinate = str(point_coordinates[0]) + '_' + \
                                    str(point_coordinates[1])
                top_layer_piece_id = top_layer_pieces_with_contact_surface_dict.get(string_coordinate)
                if top_layer_piece_id is not None:
                    # piesa de pe nivelul superior sa nu fie 1x1
                    if top_layer.pieces[top_layer_piece_id].piece_type is not 0:
                        top_layer_pieces.add(top_layer_piece_id)
                else:
                    piece_empty_points += 1
            if piece_empty_points is len(self_piece_with_points_coordinates['contact_points']):
                if self.pieces[piece_id].piece_type is not 0:
                    weak_pieces_id.append(piece_id)
                    continue
            if len(top_layer_pieces) is 1:
                if self.pieces[piece_id].piece_type is not 0:
                    weak_pieces_id.append(piece_id)
            # else:
            #     pieces_ok += 1

        if len(weak_pieces_id) is 0:
            return True
        else:
            return weak_pieces_id


