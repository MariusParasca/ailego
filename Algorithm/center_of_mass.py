# from Algorithm.model import *


def is_structure_stable(layers):
    for layer in layers:
        [print(piece) for piece in layer.merged_pieces]
    centers_of_mass = break_layer(layers)
    print(centers_of_mass)


def break_layer(layers):
    all_centers = []
    for layer in layers:
        current_layer = -1
        pieces_on_current_layer = []
        for piece in layer.merged_pieces:
            if current_layer == -1:
                current_layer = piece.z
            if piece.z == current_layer:
                pieces_on_current_layer.append(piece)
        all_centers.append(center_of_mass(contour(pieces_on_current_layer)))
    return all_centers


def contour(pieces):
    layer_contour = set()
    types = ((1, 1), (1, 2), (1, 3), (1, 4), (1, 6), (1, 8), (2, 2), (2, 3), (2, 4), (2, 6), (2, 8))
    for piece in pieces:
        layer_contour.add((piece.x, piece.y))
        layer_contour.add((piece.x + types[piece.piece_type][0], piece.y + types[piece.piece_type][1]))
    print('in center_of_mass', layer_contour)
    return layer_contour


def center_of_mass(layer_contour):
    x = 0
    y = 0
    number = 0
    for x_y in layer_contour:
        print('x_y ', x_y)
        x = x + x_y[0]
        y = y + x_y[1]
        number += 1
    return [int(x/number), int(y/number)]


#def distance_3d(set(x1, y1, z1), set(x2, y2, z2)):

