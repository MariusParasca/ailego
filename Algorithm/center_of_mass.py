import math


def is_structure_stable(layers):
    for layer in layers:
        [print(piece) for piece in layer.merged_pieces]
    centers_of_mass = break_layer(layers)
    print('centers of mass:', centers_of_mass)
    distances = []

    if len(centers_of_mass) == 1:
        print('only one layer in the structure. The structure is stable.')
        return 1
    for i in range(0, len(centers_of_mass) - 1):
        distances.append(distance_3d([centers_of_mass[i][0], centers_of_mass[i][1], i],
                                     [centers_of_mass[i + 1][0], centers_of_mass[i + 1][1], i + 1]))
    coeff = center_of_mass_coefficient(distances)
    if -0.5 < coeff < 0.5:
        print('-----stable-----')
        return 1
    else:
        print('-----NOT-stable-----')
        return 0


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
        layer_contour.add((piece.x, piece.y + types[piece.piece_type][1]))
        layer_contour.add((piece.x + types[piece.piece_type][0], piece.y + types[piece.piece_type][1]))
        layer_contour.add((piece.x + types[piece.piece_type][0], piece.y))
    print('contour points: ', layer_contour)
    return layer_contour


def center_of_mass(layer_contour):
    x = 0
    y = 0
    number = 0
    for x_y in layer_contour:
        x = x + x_y[0]
        y = y + x_y[1]
        number += 1
    return [int(x / number), int(y / number)]


def distance_3d(point1: object, point2: object) -> object:
    #print('points: ', point1, point2)
    #print('distance between points: ', math.sqrt(math.pow((point1[0] - point2[0]),2) + math.pow((point1[1] - point2[1]), 2) + math.pow((point1[2] - point2[2]), 2)))
    return math.sqrt(math.pow((point1[0] - point2[0]),2) + math.pow((point1[1] - point2[1]), 2) + math.pow((point1[2] - point2[2]), 2))


def center_of_mass_coefficient(distances):
    list_of_distances = distances
    while len(list_of_distances) > 1:
        auxiliary = []
        #for i in range(0, len(list_of_distances) - 1):
        #    auxiliary.append(list_of_distances[i] - list_of_distances[i+1])
        #for i in range(0,len(auxiliary)):
        #    if auxiliary[i] < 0:
        #        auxiliary[i] = -auxiliary[i]
        auxiliary.append(list_of_distances[0] - list_of_distances[1])
        if auxiliary[0] < 0:
            auxiliary[0] = -auxiliary[0]
        for i in range(2, len(list_of_distances)):
            auxiliary.append(list_of_distances[i])

        print('trying to get the coefficient of a structure: ', auxiliary)
        list_of_distances = auxiliary
    return list_of_distances[0]
