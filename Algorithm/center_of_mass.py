# from Algorithm.model import *


def is_structure_stable(layers):
    for layer in layers:
        [print(piece) for piece in layer.merged_pieces]
    break_layer(layers)


def break_layer(layers):
    for layer in layers:
        current_layer = -1
        pieces_on_current_layer = []
        for piece in layer.merged_pieces:
            if current_layer == -1:
                current_layer = piece.z
            if piece.z == current_layer:
                pieces_on_current_layer.append(piece)
        center_of_mass(pieces_on_current_layer)


def center_of_mass(pieces):
    contour = set()
    for piece in pieces:
        contour.add((piece.x, piece.y))
    print('in center_of_mass', contour)