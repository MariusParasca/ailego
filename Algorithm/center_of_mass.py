import math

global_layer = 0
weight = 0

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


def is_structure_stable(layers):
    for layer in layers:
        [print('PPieeesele',piece) for piece in layer.merged_pieces]
    contour(layers)

def save_base(building_contour):
    base=list()
    for point in building_contour:
        if point[2]==0:
            base.append(point)
    return base

def center_of_mass(building_contour):
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


def contour(layers):
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
