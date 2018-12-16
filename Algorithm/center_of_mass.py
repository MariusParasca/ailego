import math

global_layer = 0
weight = 0


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
        distances.append(distance_3d([centers_of_mass[i][0], centers_of_mass[i][1], centers_of_mass[i][2]],
                                     [centers_of_mass[i + 1][0], centers_of_mass[i + 1][1], centers_of_mass[i + 1][2]]))
    coeff = center_of_mass_coefficient(distances) / global_layer
    print('final coefficient: ', coeff)
    if 0.3 < coeff < 1:
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
    global global_layer
    global_layer += 1
    return [x / number, y / number, global_layer - 0.5]


def distance_2d(point1, point2):
    return math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))


def distance_3d(point1: object, point2: object) -> object:
    print('points: ', point1, point2)
    print('distance between points: ', math.sqrt(
        math.pow((point1[0] - point2[0]), 2) + math.pow((point1[1] - point2[1]), 2) + math.pow((point1[2] - point2[2]),
                                                                                               2)))
    global weight
    weight += 0.5
    return math.sqrt(math.pow((point1[0] - point2[0]), 2) + math.pow((point1[1] - point2[1]), 2) + math.pow(
        (point1[2] - point2[2] * weight), 2))


def center_of_mass_coefficient(distances):
    list_of_distances = distances
    while len(list_of_distances) > 1:
        auxiliary = []
        # for i in range(0, len(list_of_distances) - 1):
        #    auxiliary.append(list_of_distances[i] - list_of_distances[i+1])
        # for i in range(0,len(auxiliary)):
        #    if auxiliary[i] < 0:
        #        auxiliary[i] = -auxiliary[i]
        auxiliary.append(list_of_distances[0] - list_of_distances[1] - 1)
        if auxiliary[0] < 0:
            auxiliary[0] = -auxiliary[0]
        for i in range(2, len(list_of_distances)):
            auxiliary.append(list_of_distances[i])

        print('trying to get the coefficient of a structure: ', auxiliary)
        list_of_distances = auxiliary
    return list_of_distances[0]


def is_structure_stable_1(layers):
    for layer in layers:
        [print('PPieeesele',piece) for piece in layer.merged_pieces]
    contour_1(layers)


def center_of_mass_1(building_contour):
    x = 0
    y = 0
    number = 0

    for x_y in building_contour:
        x = x + x_y[0]
        y = y + x_y[1]
        number += 1
    global global_layer
    global_layer += 1
    return [x / number, y / number, global_layer - 0.5]


def contour_1(layers):
    building_contour = list()
    types = ((1, 1), (1, 2), (1, 3), (1, 4), (1, 6), (1, 8), (2, 2), (2, 3), (2, 4), (2, 6), (2, 8))
    for layer in layers:
        for piece in layer.merged_pieces:
            print('Lalala', piece)
            building_contour.append(list((piece.x, piece.y, piece.z)))
            building_contour.append([piece.x, piece.y + types[piece.piece_type][1], piece.z])
            building_contour.append([piece.x + types[piece.piece_type][0], piece.y + types[piece.piece_type][1], piece.z])
            building_contour.append([piece.x + types[piece.piece_type][0], piece.y, piece.z])
        print('contour points: ', building_contour)
    return pop_not_relevant_points(building_contour)


def pop_not_relevant_points(building_contour):
    for point in building_contour:
        min_x = 50
        min_y = 50
        max_x = 0
        max_y = 0
        for subpoint in building_contour:
            if subpoint[2] == point[2]:
                if subpoint[0] < min_x: min_x = subpoint[0]
                if subpoint[0] > max_x: max_x = subpoint[0]
                if subpoint[1] < min_y: min_y = subpoint[1]
                if subpoint[1] > max_y: max_y = subpoint[1]
        for useless_point in building_contour:
            if useless_point != [min_x, min_y, point[2]] or useless_point != [max_x, max_y, point[2]]:
                building_contour.remove(useless_point)
    print(building_contour)
    return building_contour
